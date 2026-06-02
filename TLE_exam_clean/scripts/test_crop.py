import fitz

FIGURES = {
    "figure_01": {"page": 0, "rect": (215, 453, 875, 875)},
    "figure_02": {"page": 1, "rect": (105, 35, 930, 320)},
    "figure_03": {"page": 1, "rect": (170, 582, 905, 710)},
    "figure_04": {"page": 2, "rect": (113, 165, 983, 460)},
    "figure_05": {"page": 3, "rect": (245, 855, 785, 1095)},
    "figure_06": {"page": 4, "rect": (115, 780, 975, 1185)},
    "figure_07": {"page": 6, "rect": (205, 350, 905, 710)},
}

doc = fitz.open("/home/david/Downloads/TLE_EXAM/TLE_Exam.pdf")

for name, info in FIGURES.items():
    page = doc[info["page"]]
    x0, y0, x1, y1 = info["rect"]
    rect = fitz.Rect(x0, y0, x1, y1)
    pix = page.get_pixmap(clip=rect)
    
    # Save to check visually if we could
    # pix.save(f"/home/david/Downloads/TLE_EXAM/TLE_exam_clean/figures/{name}_test.png")
