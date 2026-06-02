import fitz
from pathlib import Path

doc = fitz.open("/home/david/Downloads/TLE_EXAM/TLE_exam_clean/TLE_Exam.pdf")

print("--- Text Blocks ---")
for page_num in range(7):
    page = doc[page_num]
    blocks = page.get_text("blocks")
    print(f"Page {page_num + 1}:")
    for b in blocks:
        text = b[4].strip()
        if text.startswith("FIGURE") or text.startswith("Ce sujet") or text.startswith("I ") or text.startswith("Du fait") or text.startswith("Afin de") or text.startswith("Sur ces") or text.startswith("Il est difficile") or text.startswith("11. Pour") or text.startswith("17. L'image") or text.startswith("III "):
            # Print first 30 chars
            print(f"  {b[:4]} -> {text[:50].replace('\n', ' ')}")
