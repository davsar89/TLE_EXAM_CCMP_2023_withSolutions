#!/usr/bin/env python3
"""Extract printed figures from the scanned TLE exam PDF."""

from __future__ import annotations

import argparse
from pathlib import Path

import fitz


# Coordinates are in original PDF points/pixels: x0, y0, x1, y1.
# The source scan pages are 1080 x 1440, and the PDF page coordinate system
# matches those dimensions.
FIGURES = {
    "figure_01": {
        "page": 0,
        "rect": (215, 453, 875, 875),
        "caption": "Différentes formes de phénomènes lumineux éphémères atmosphériques.",
    },
    "figure_02": {
        "page": 1,
        "rect": (105, 35, 930, 340),
        "caption": "À gauche : spectre d'émission d'un sylphe. À droite : coefficient de transmission de l'atmosphère avec deux raies d'absorption.",
    },
    "figure_03": {
        "page": 1,
        "rect": (170, 590, 905, 775),
        "caption": "Photos tirées de l'article Sprites rouges, Jets Bleus et elfes.",
    },
    "figure_04": {
        "page": 2,
        "rect": (113, 160, 983, 490),
        "caption": "Enregistrements effectués depuis l'Est par la microcaméra filtrée à gauche et par la microcaméra dans le visible à droite.",
    },
    "figure_05": {
        "page": 3,
        "rect": (245, 845, 785, 1130),
        "caption": "Pression de l'air atmosphérique.",
    },
    "figure_06": {
        "page": 4,
        "rect": (115, 780, 975, 1220),
        "caption": "Carte d'échos radar à 2,2 MHz depuis le sol pour l'événement enregistré à 18h39 le 15 octobre 1994.",
    },
    "figure_07": {
        "page": 6,
        "rect": (205, 340, 905, 745),
        "caption": "Représentation graphique des fonctions.",
    },
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", type=Path, default=Path("TLE_Exam.pdf"))
    parser.add_argument("--out-dir", type=Path, default=Path("TLE_exam_clean/figures"))
    parser.add_argument("--scale", type=float, default=2.0)
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(args.pdf)
    matrix = fitz.Matrix(args.scale, args.scale)
    for name, info in FIGURES.items():
        page = doc[info["page"]]
        clip = fitz.Rect(*info["rect"])
        pix = page.get_pixmap(matrix=matrix, clip=clip, alpha=False)
        output = args.out_dir / f"{name}.png"
        pix.save(output)
        print(
            f"{name}: page {info['page'] + 1}, rect={info['rect']}, "
            f"size={pix.width}x{pix.height} -> {output}"
        )
    doc.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
