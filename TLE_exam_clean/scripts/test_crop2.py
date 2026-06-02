import fitz

doc = fitz.open("/home/david/Downloads/TLE_EXAM/TLE_Exam.pdf")
page = doc[1] # Page 2

for y1 in [700, 690, 680, 670, 660, 650, 640]:
    rect = fitz.Rect(170, 582, 905, y1)
    pix = page.get_pixmap(clip=rect)
    pix.save(f"/home/david/Downloads/TLE_EXAM/TLE_exam_clean/figures/fig3_crop_test_{y1}.png")
