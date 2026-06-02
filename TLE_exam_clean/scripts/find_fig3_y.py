import fitz
import numpy as np

doc = fitz.open("/home/david/Downloads/TLE_EXAM/TLE_Exam.pdf")
page = doc[1] # Page 2

# get a larger block
rect = fitz.Rect(100, 350, 950, 900)
pix = page.get_pixmap(clip=rect)

img_data = np.frombuffer(pix.samples, dtype=np.uint8).reshape((pix.height, pix.width, pix.n))
if pix.n >= 3:
    gray = 0.2989 * img_data[:, :, 0] + 0.5870 * img_data[:, :, 1] + 0.1140 * img_data[:, :, 2]
else:
    gray = img_data[:, :, 0]

# Print row density (dark pixels per row)
rows_dark = np.sum(gray < 150, axis=1)

# Group them into bands
in_band = False
band_start = 0
for i, count in enumerate(rows_dark):
    if count > 5 and not in_band:
        in_band = True
        band_start = i
    elif count <= 5 and in_band:
        in_band = False
        print(f"Content band: y=[{band_start + 350}, {i + 350}], max_dark={np.max(rows_dark[band_start:i])}")

if in_band:
    print(f"Content band: y=[{band_start + 350}, {len(rows_dark) + 350}], max_dark={np.max(rows_dark[band_start:])}")

