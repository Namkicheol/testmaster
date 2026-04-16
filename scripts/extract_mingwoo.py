import pdfplumber, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

files = [
    ("밍우 영어학 분석.pdf", "references/밍우_영어학분석.txt"),
]

for pdf_name, out_name in files:
    pdf_path = ROOT / pdf_name
    out_path = ROOT / out_name
    if not pdf_path.exists():
        sys.stderr.write(f"없음: {pdf_name}\n")
        continue
    with pdfplumber.open(pdf_path) as pdf:
        total = len(pdf.pages)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(f"=== {pdf_name} ===\n총 {total}페이지\n\n")
            for i, page in enumerate(pdf.pages, 1):
                text = page.extract_text() or ""
                f.write(f"\n{'─'*60}\n[p.{i}]\n{text}")
        size_kb = out_path.stat().st_size // 1024
        sys.stderr.write(f"완료: {pdf_name} → {total}페이지, {size_kb}KB\n")
