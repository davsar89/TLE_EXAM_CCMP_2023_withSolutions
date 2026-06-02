#!/usr/bin/env python3
"""Transcribe TLE exam page images with the Gemini API."""

from __future__ import annotations

import argparse
import base64
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
import time

import requests


PROMPT = """\
You are transcribing one photographed scanned page of a French physics exam into LaTeX.

Return only clean LaTeX source for the printed exam content visible on this page.

Rules:
- Preserve all French accents and punctuation.
- Preserve headings, section labels, question numbers, displayed equations, equation numbers, figure captions, and item order.
- Convert mathematical notation and equations to standard LaTeX.
- Use \\section*, \\subsection*, \\paragraph, enumerate, itemize, equation*, align*, and figure captions where appropriate.
- Do not transcribe handwritten check marks, annotations, underlines, page footer numbers, scan shadows, or the phrase "Tournez la page S.V.P.".
- Do not include decorative page headers unless they contain unique exam content.
- If a figure image appears, do not describe the image; write a clear placeholder line exactly like: \\TLEFigure{N}{caption text}, using the printed figure number N and printed caption.
- If a printed character or formula is genuinely unreadable, write [unclear] in place.
- Do not summarize, translate, modernize, omit, or add explanatory text.
- Before returning, verify that the final visible printed line of the page has been included.

Return plain LaTeX text only, without Markdown fences.
"""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_ledger_total(path: Path) -> float:
    if not path.exists():
        return 0.0
    total = 0.0
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            total += float(json.loads(line).get("estimated_cost_usd", 0.0))
        except (json.JSONDecodeError, TypeError, ValueError):
            continue
    return total


def append_ledger(path: Path, row: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, sort_keys=True) + "\n")


def usage_int(usage: dict, key: str) -> int:
    return int(usage.get(key, 0) or 0)


def estimate_cost(usage: dict, input_rate_per_m: float, output_rate_per_m: float) -> tuple[float | None, int, int]:
    prompt_tokens = usage_int(usage, "promptTokenCount")
    candidates = usage_int(usage, "candidatesTokenCount")
    thoughts = usage_int(usage, "thoughtsTokenCount")
    total = usage_int(usage, "totalTokenCount")
    if not (prompt_tokens or candidates or thoughts or total):
        return None, 0, 0
    if total and prompt_tokens:
        output_tokens = max(candidates, thoughts, total - prompt_tokens)
    else:
        output_tokens = candidates + thoughts
    cost = (prompt_tokens * input_rate_per_m + output_tokens * output_rate_per_m) / 1_000_000
    return cost, prompt_tokens, output_tokens


def transcribe(
    image: Path,
    model: str,
    api_version: str,
    timeout: int,
    retries: int,
    media_resolution: str | None,
    thinking_level: str | None,
) -> tuple[str, dict]:
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise SystemExit("GEMINI_API_KEY is not set")

    encoded = base64.b64encode(image.read_bytes()).decode("ascii")
    image_part: dict = {"inline_data": {"mime_type": "image/png", "data": encoded}}
    if media_resolution:
        image_part["media_resolution"] = {"level": media_resolution}

    generation_config: dict = {
        "temperature": 0,
        "topP": 0.1,
        "maxOutputTokens": 12000,
    }
    if thinking_level:
        generation_config["thinkingConfig"] = {"thinkingLevel": thinking_level}

    payload = {
        "contents": [{"parts": [{"text": PROMPT}, image_part]}],
        "generationConfig": generation_config,
    }
    url = f"https://generativelanguage.googleapis.com/{api_version}/models/{model}:generateContent"

    response = None
    for attempt in range(retries + 1):
        try:
            response = requests.post(
                url,
                headers={"x-goog-api-key": key},
                json=payload,
                timeout=timeout,
            )
        except requests.RequestException as exc:
            if attempt >= retries:
                raise RuntimeError(f"Gemini API request failed: {exc}") from exc
            time.sleep(2**attempt)
            continue

        if response.status_code in {429, 500, 502, 503, 504} and attempt < retries:
            time.sleep(2**attempt)
            continue
        break

    if response is None:
        raise RuntimeError("Gemini API request did not run")
    if response.status_code != 200:
        raise RuntimeError(f"Gemini API status {response.status_code}: {response.text[:1200]}")

    body = response.json()
    try:
        text = body["candidates"][0]["content"]["parts"][0]["text"].rstrip() + "\n"
    except (KeyError, IndexError) as exc:
        raise RuntimeError(f"Unexpected Gemini response: {body}") from exc
    return text, body


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("images", nargs="+", type=Path)
    parser.add_argument("--out-dir", type=Path, default=Path("TLE_exam_clean/ocr_output/page_tex"))
    parser.add_argument("--ledger", type=Path, default=Path("TLE_exam_clean/ocr_output/gemini_usage.jsonl"))
    parser.add_argument("--model", default="gemini-3.1-pro-preview")
    parser.add_argument("--api-version", default="v1beta")
    parser.add_argument("--media-resolution", default="MEDIA_RESOLUTION_HIGH")
    parser.add_argument("--thinking-level", default="low")
    parser.add_argument("--timeout", type=int, default=160)
    parser.add_argument("--retries", type=int, default=3)
    parser.add_argument("--sleep", type=float, default=1.0)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--max-cost-usd", type=float, default=float(os.environ.get("GEMINI_API_MAX_COST_USD", "5.0")))
    parser.add_argument("--max-request-estimate-usd", type=float, default=0.20)
    parser.add_argument("--input-rate-per-m", type=float, default=2.00)
    parser.add_argument("--output-rate-per-m", type=float, default=12.00)
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    ledger_total = read_ledger_total(args.ledger)
    session_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    print(f"starting ledger ${ledger_total:.4f}/${args.max_cost_usd:.2f}")

    for image in args.images:
        out = args.out_dir / f"{image.stem}.tex"
        if out.exists() and not args.force:
            print(f"skip {image} -> {out}")
            continue
        if ledger_total + args.max_request_estimate_usd > args.max_cost_usd:
            raise SystemExit(
                f"Refusing Gemini call: ledger ${ledger_total:.4f} plus reserve "
                f"${args.max_request_estimate_usd:.4f} would exceed ${args.max_cost_usd:.2f}."
            )

        print(f"transcribe {image} -> {out}", flush=True)
        started = utc_now()
        try:
            text, body = transcribe(
                image,
                args.model,
                args.api_version,
                args.timeout,
                args.retries,
                args.media_resolution,
                args.thinking_level,
            )
            usage = body.get("usageMetadata", {})
            cost, prompt_tokens, output_tokens = estimate_cost(
                usage,
                args.input_rate_per_m,
                args.output_rate_per_m,
            )
            cost_source = "usage_metadata"
            if cost is None:
                cost = args.max_request_estimate_usd
                cost_source = "conservative_request_estimate"
                prompt_tokens = 0
                output_tokens = 0
        except Exception as exc:
            append_ledger(
                args.ledger,
                {
                    "session_id": session_id,
                    "status": "error",
                    "image": str(image),
                    "output_path": str(out),
                    "started_at": started,
                    "finished_at": utc_now(),
                    "estimated_cost_usd": 0.0,
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                    "model": args.model,
                },
            )
            raise

        out.write_text(text, encoding="utf-8")
        ledger_total += cost
        append_ledger(
            args.ledger,
            {
                "session_id": session_id,
                "status": "ok",
                "image": str(image),
                "output_path": str(out),
                "started_at": started,
                "finished_at": utc_now(),
                "estimated_cost_usd": round(cost, 8),
                "cumulative_after_usd": round(ledger_total, 8),
                "cost_source": cost_source,
                "prompt_tokens": prompt_tokens,
                "output_tokens_billed_estimate": output_tokens,
                "usage_metadata": usage,
                "model": args.model,
            },
        )
        print(f"cost ${cost:.4f}; ledger ${ledger_total:.4f}/${args.max_cost_usd:.2f}")
        time.sleep(args.sleep)

    print(f"done; ledger ${ledger_total:.4f}/${args.max_cost_usd:.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
