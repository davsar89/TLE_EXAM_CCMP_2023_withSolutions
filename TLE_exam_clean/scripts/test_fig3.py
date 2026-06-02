import fitz

doc = fitz.open("/home/david/Downloads/TLE_EXAM/TLE_Exam.pdf")
page = doc[1] # Page 2

rect = fitz.Rect(170, 595, 905, 775)
pix = page.get_pixmap(clip=rect)
pix.save("/home/david/Downloads/TLE_EXAM/TLE_exam_clean/figures/fig3_perfect_test.png")
