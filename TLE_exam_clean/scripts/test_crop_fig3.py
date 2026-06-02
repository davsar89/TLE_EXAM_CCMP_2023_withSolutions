from PIL import Image
import numpy as np

for test_y1 in range(650, 715, 10):
    path = f"/home/david/Downloads/TLE_EXAM/TLE_exam_clean/figures/fig3_test_{test_y1}.png"
    img = Image.open(path).convert('L')
    img_data = np.array(img)
    # Check bottom 10 rows for dark pixels
    bottom_rows = img_data[-10:, :]
    dark_pixels = np.sum(bottom_rows < 150)
    print(f"y1={test_y1}, dark pixels in bottom 10 rows: {dark_pixels}")
