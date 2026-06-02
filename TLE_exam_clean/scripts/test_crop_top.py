import fitz

doc = fitz.open("/home/david/Downloads/TLE_EXAM/TLE_Exam.pdf")
page = doc[1] # Page 2

for y0 in [500, 520, 540, 560, 582, 600]:
    rect = fitz.Rect(170, y0, 905, 650)
    pix = page.get_pixmap(clip=rect)
    pix.save(f"/home/david/Downloads/TLE_EXAM/TLE_exam_clean/figures/fig3_top_test_{y0}.png")
