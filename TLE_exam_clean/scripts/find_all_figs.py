import fitz
import numpy as np

doc = fitz.open("/home/david/Downloads/TLE_EXAM/TLE_Exam.pdf")

FIGURES = {
    "figure_01": {"page": 0, "rect": (150, 400, 950, 950)},
    "figure_02": {"page": 1, "rect": (50, 0, 950, 450)},
    "figure_03": {"page": 1, "rect": (150, 500, 950, 900)},
    "figure_04": {"page": 2, "rect": (100, 100, 990, 600)},
    "figure_05": {"page": 3, "rect": (200, 800, 800, 1200)},
    "figure_06": {"page": 4, "rect": (100, 700, 980, 1250)},
    "figure_07": {"page": 6, "rect": (150, 300, 950, 800)},
}

for name, info in FIGURES.items():
    page = doc[info["page"]]
    x0, y0, x1, y1 = info["rect"]
    rect = fitz.Rect(x0, y0, x1, y1)
    pix = page.get_pixmap(clip=rect)
    
    img_data = np.frombuffer(pix.samples, dtype=np.uint8).reshape((pix.height, pix.width, pix.n))
    if pix.n >= 3:
        gray = 0.2989 * img_data[:, :, 0] + 0.5870 * img_data[:, :, 1] + 0.1140 * img_data[:, :, 2]
    else:
        gray = img_data[:, :, 0]
        
    rows_dark = np.sum(gray < 150, axis=1)
    
    print(f"\n{name} bands in ({x0},{y0}) to ({x1},{y1}):")
    in_band = False
    band_start = 0
    for i, count in enumerate(rows_dark):
        if count > 5 and not in_band:
            in_band = True
            band_start = i
        elif count <= 5 and in_band:
            in_band = False
            print(f"  y=[{band_start + int(y0)}, {i + int(y0)}], height={i-band_start}, max_dark={np.max(rows_dark[band_start:i])}")
    if in_band:
        print(f"  y=[{band_start + int(y0)}, {len(rows_dark) + int(y0)}], height={len(rows_dark)-band_start}, max_dark={np.max(rows_dark[band_start:])}")
