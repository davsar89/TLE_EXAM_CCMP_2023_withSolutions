import fitz

doc = fitz.open("/home/david/Downloads/TLE_EXAM/TLE_Exam.pdf")

rects = {
    "figure_03": (1, fitz.Rect(170, 590, 905, 775)),
    "figure_04": (2, fitz.Rect(113, 160, 983, 470)),
    "figure_05": (3, fitz.Rect(245, 845, 785, 1115)),
    "figure_06": (4, fitz.Rect(115, 790, 975, 1185)),
    "figure_07": (6, fitz.Rect(205, 340, 905, 725)),
}

for name, (p, rect) in rects.items():
    page = doc[p]
    pix = page.get_pixmap(clip=rect)
    pix.save(f"/home/david/Downloads/TLE_EXAM/TLE_exam_clean/figures/{name}_val.png")
