#!/usr/bin/env python3
"""Lightweight checks for the reconstructed TLE exam artifacts."""

from __future__ import annotations

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
TEX = ROOT / "TLE_Exam.tex"
PDF = ROOT / "TLE_Exam.pdf"
FIGURES = ROOT / "figures"


def main() -> int:
    errors: list[str] = []
    if not TEX.exists():
        errors.append(f"missing {TEX}")
    if not PDF.exists():
        errors.append(f"missing {PDF}")
    if TEX.exists():
        text = TEX.read_text(encoding="utf-8")
        for needle in ("Les sylphes", "Observation des sylphes", "Une atmosphère électrique", "Formation avalancheuse de courant"):
            if needle not in text:
                errors.append(f"missing heading/text: {needle}")
        for number in range(1, 25):
            if not re.search(rf"\\question(?:\[[^\]]+\])?\s*\{{\s*{number}\s*\}}", text):
                errors.append(f"missing question macro for {number}")
        for number in range(1, 8):
            figure = FIGURES / f"figure_{number:02d}.png"
            if not figure.exists():
                errors.append(f"missing figure asset {figure}")
            if f"figure_{number:02d}.png" not in text:
                errors.append(f"figure_{number:02d}.png not included in TeX")
        if "[unclear]" in text:
            errors.append("TeX still contains [unclear]")
    if errors:
        print("verification failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("verification passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
