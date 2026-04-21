"""
메가쌤 전공영어 기출 분석.pdf (스캔본) → OCR → references/메가쌤_기출분석_OCR.txt

의존: pytesseract, PyMuPDF (fitz), Pillow
언어: kor+eng 혼합
"""

import sys
import os
from pathlib import Path

import fitz          # PyMuPDF
from PIL import Image
import pytesseract

ROOT = Path(__file__).resolve().parent.parent
PDF_PATH = ROOT / "메가쌤 전공영어 기출 분석.pdf"
OUT_PATH = ROOT / "references" / "메가쌤_기출분석_OCR.txt"

# Tesseract 실행파일 경로
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# 커스텀 tessdata 경로 (한글 팩 위치)
TESSDATA_DIR = str(Path.home() / ".tesseract" / "tessdata")
os.environ["TESSDATA_PREFIX"] = TESSDATA_DIR

# OCR 설정
OCR_LANG = "kor+eng"
OCR_CONFIG = "--psm 3"   # 자동 페이지 분할
DPI = 250                # 해상도 (높을수록 정확하나 느림)


def pdf_page_to_image(page: fitz.Page) -> Image.Image:
    mat = fitz.Matrix(DPI / 72, DPI / 72)
    pix = page.get_pixmap(matrix=mat, colorspace=fitz.csRGB)
    return Image.frombytes("RGB", [pix.width, pix.height], pix.samples)


def main():
    if not PDF_PATH.exists():
        print(f"[!] PDF 없음: {PDF_PATH}")
        sys.exit(1)

    # 빠른 설치 확인
    try:
        ver = pytesseract.get_tesseract_version()
        print(f"[*] Tesseract {ver}")
    except Exception as e:
        print(f"[!] Tesseract 오류: {e}")
        sys.exit(1)

    doc = fitz.open(PDF_PATH)
    total = len(doc)
    print(f"[*] {PDF_PATH.name}: {total}페이지")
    print(f"[*] 언어: {OCR_LANG}, DPI: {DPI}")
    print(f"[*] 출력: {OUT_PATH}\n")

    OUT_PATH.parent.mkdir(exist_ok=True)

    with open(OUT_PATH, "w", encoding="utf-8") as fout:
        fout.write(f"=== 메가쌤 전공영어 기출 분석 (OCR) ===\n")
        fout.write(f"총 {total}페이지\n\n")

        for i, page in enumerate(doc, start=1):
            img = pdf_page_to_image(page)
            text = pytesseract.image_to_string(img, lang=OCR_LANG, config=OCR_CONFIG)

            fout.write(f"\n{'─'*60}\n")
            fout.write(f"[p.{i}]\n")
            fout.write(text)
            fout.flush()

            if i % 10 == 0 or i == total:
                kb = OUT_PATH.stat().st_size // 1024
                print(f"  {i:3d}/{total} 완료 ({kb:,} KB)")

    doc.close()
    final_kb = OUT_PATH.stat().st_size // 1024
    print(f"\n완료 — {OUT_PATH.name} ({final_kb:,} KB)")


if __name__ == "__main__":
    main()
