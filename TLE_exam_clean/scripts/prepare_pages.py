#!/usr/bin/env python3
"""Render scanned exam pages to auditable page images for OCR."""

from __future__ import annotations

import argparse
from pathlib import Path

import fitz
from PIL import Image, ImageFilter, ImageOps


def enhance_for_ocr(source: Path, dest: Path) -> None:
    image = Image.open(source).convert("L")
    image = ImageOps.autocontrast(image, cutoff=1)
    image = image.filter(ImageFilter.UnsharpMask(radius=1.2, percent=140, threshold=4))
    dest.parent.mkdir(parents=True, exist_ok=True)
    image.save(dest)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", type=Path, default=Path("TLE_Exam.pdf"))
    parser.add_argument("--out-dir", type=Path, default=Path("TLE_exam_clean/ocr_output/page_images"))
    parser.add_argument(
        "--ocr-dir",
        type=Path,
        default=Path("TLE_exam_clean/ocr_output/page_images_ocr"),
    )
    parser.add_argument("--scale", type=float, default=2.0)
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    args.ocr_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(args.pdf)
    matrix = fitz.Matrix(args.scale, args.scale)
    for index, page in enumerate(doc, start=1):
        stem = f"page_{index:02d}"
        rendered = args.out_dir / f"{stem}.png"
        pix = page.get_pixmap(matrix=matrix, alpha=False)
        pix.save(rendered)
        enhanced = args.ocr_dir / f"{stem}.png"
        enhance_for_ocr(rendered, enhanced)
        print(f"{stem}: rendered {pix.width}x{pix.height} -> {rendered}; OCR image -> {enhanced}")

    doc.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
