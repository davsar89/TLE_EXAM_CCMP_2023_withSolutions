import numpy as np
from PIL import Image
from pathlib import Path

fig_dir = Path('/home/david/Downloads/TLE_EXAM/TLE_exam_clean/figures')

for p in sorted(fig_dir.glob('figure_*.png')):
    img = Image.open(p).convert('L') # Convert to grayscale
    img_data = np.array(img)
    
    # Threshold: values < 200 are considered "dark" (content)
    dark_pixels = np.argwhere(img_data < 200)
    
    if dark_pixels.size > 0:
        y_min, x_min = dark_pixels.min(axis=0)
        y_max, x_max = dark_pixels.max(axis=0)
        
        w = x_max - x_min + 1
        h = y_max - y_min + 1
        
        print(f"{p.name}:")
        print(f"  Current size: {img.width}x{img.height}")
        print(f"  Content rect: x={x_min}, y={y_min}, w={w}, h={h}")
        print(f"  Margins: left={x_min}, top={y_min}, right={img.width - x_max - 1}, bottom={img.height - y_max - 1}")
    else:
        print(f"{p.name}: Empty")
