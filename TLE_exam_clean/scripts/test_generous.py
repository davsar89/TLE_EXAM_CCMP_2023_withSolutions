import fitz

doc = fitz.open("/home/david/Downloads/TLE_EXAM/TLE_Exam.pdf")

rects = {
    "figure_04": (2, fitz.Rect(110, 160, 990, 500)),
    "figure_05": (3, fitz.Rect(240, 845, 790, 1130)),
    "figure_06": (4, fitz.Rect(110, 780, 980, 1220)),
    "figure_07": (6, fitz.Rect(200, 340, 910, 740)),
}

for name, (p, rect) in rects.items():
    page = doc[p]
    pix = page.get_pixmap(clip=rect)
    pix.save(f"/home/david/Downloads/TLE_EXAM/TLE_exam_clean/figures/{name}_test2.png")
