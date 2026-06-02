import fitz

doc = fitz.open("/home/david/Downloads/TLE_EXAM/TLE_Exam.pdf")
page = doc[1] # Page 2

# Check full height around figure 3
rect = fitz.Rect(100, 550, 950, 800)
pix = page.get_pixmap(clip=rect)
pix.save("/home/david/Downloads/TLE_EXAM/TLE_exam_clean/figures/fig3_full_test.png")
