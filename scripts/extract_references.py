"""
참고자료 PDF → 텍스트 파일 추출
출력: references/{파일명}.txt (UTF-8)
"""
import sys
from pathlib import Path
import pdfplumber

ROOT = Path(__file__).resolve().parent.parent
REF_DIR = ROOT / "references"
REF_DIR.mkdir(exist_ok=True)

TARGETS = [
    ("역대 기출 강사 및 합격자 모범답안 모음 (최종본).pdf", "모범답안_2014-2023.txt"),
    ("루이스기출문제_OCR.pdf",                               "루이스기출문제.txt"),
    ("메가쌤 전공영어 기출 분석.pdf",                         "메가쌤_기출분석.txt"),
]

for pdf_name, out_name in TARGETS:
    pdf_path = ROOT / pdf_name
    if not pdf_path.exists():
        print(f"[!] 없음: {pdf_name}")
        continue

    out_path = REF_DIR / out_name
    print(f"\n[*] {pdf_name}")

    with pdfplumber.open(pdf_path) as pdf:
        total = len(pdf.pages)
        print(f"    {total}페이지 → {out_name}")
        with open(out_path, "w", encoding="utf-8") as fout:
            fout.write(f"=== {pdf_name} ===\n")
            fout.write(f"총 {total}페이지\n\n")
            for i, page in enumerate(pdf.pages, start=1):
                text = page.extract_text() or ""
                fout.write(f"\n{'─'*60}\n")
                fout.write(f"[p.{i}]\n")
                fout.write(text)
                if i % 50 == 0:
                    print(f"    {i}/{total}페이지 처리 중...")

    size_kb = out_path.stat().st_size // 1024
    print(f"    완료 ({size_kb:,} KB) → {out_path.name}")

print("\n✓ 모든 참고자료 추출 완료")
print(f"  저장 위치: {REF_DIR}")
