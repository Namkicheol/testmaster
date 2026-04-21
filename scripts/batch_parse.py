"""
giulmmaster 폴더 전체 PDF 일괄 파싱

디렉터리별 규칙:
  기출 raw/           → 연도·형식 파일명 추출, --split (문항별 분리)
  루이스 문제 raw/영어학/    → subject=linguistics
  루이스 문제 raw/영어교육론/ → subject=english_education
  루트 레벨              → subject 미분류, 텍스트만 추출
"""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PYTHON = sys.executable
PARSER = ROOT / "scripts" / "parse_pdf.py"
LOG_FILE = ROOT / "scripts" / "batch_parse.log"

# 로그 핸들러
_log_fh = open(LOG_FILE, "w", encoding="utf-8")


def log(msg: str):
    _log_fh.write(msg + "\n")
    _log_fh.flush()
    safe = msg.encode("utf-8", errors="replace").decode("utf-8", errors="replace")
    try:
        print(safe)
    except UnicodeEncodeError:
        # Windows CP949 콘솔에서 깨지는 문자 ? 대체
        print(safe.encode("cp949", errors="replace").decode("cp949"))


# 정답표·중복·참고자료 파일 제외 패턴
SKIP_PATTERNS = [
    r"정답표",
    r"\(1\)\.pdf$",   # 중복본 예: 2015중등1차-영어_전공A (1).pdf
    r"최종본",
    r"OCR",
    r"기출 분석",
    r"기출분석",
    r"총모음",
]


def should_skip(path: Path) -> bool:
    for pat in SKIP_PATTERNS:
        if re.search(pat, path.name):
            return True
    return False


def parse_exam_filename(stem: str) -> tuple:
    """파일명에서 (연도, 형식) 추출."""
    year = None
    m = re.search(r"(20\d{2}|201\d|200\d)", stem)
    if m:
        year = int(m.group(1))

    form = None
    m = re.search(r"전공\s*([AB])", stem)
    if m:
        form = m.group(1)
    else:
        m = re.search(r"_([AB])(?:\.pdf)?$", stem, re.IGNORECASE)
        if m:
            form = m.group(1).upper()

    return year, form


def run_parser(pdf: Path, extra_args: list, label: str):
    cmd = [PYTHON, str(PARSER), str(pdf)] + extra_args
    log(f"\n{'─'*60}")
    log(f"[{label}]  {pdf.name}")
    log(f"  args: {' '.join(extra_args)}")
    result = subprocess.run(cmd, capture_output=True)
    stdout = result.stdout.decode("utf-8", errors="replace")
    stderr = result.stderr.decode("utf-8", errors="replace")
    for line in stdout.splitlines():
        log(f"  {line}")
    if result.returncode != 0 and stderr:
        log(f"  [!] {stderr[:400]}")


def process_kibchul_raw(folder: Path):
    for pdf in sorted(folder.glob("*.pdf")):
        if should_skip(pdf):
            log(f"  [skip] {pdf.name}")
            continue
        year, form = parse_exam_filename(pdf.stem)
        # subject 는 parse_pdf.py 가 문항별로 자동 판단 (하드코딩 금지)
        args = ["--split"]
        if year:
            args += ["--year", str(year)]
        if form:
            args += ["--form", form]
        run_parser(pdf, args, "기출 raw")


def process_lewis_folder(folder: Path, subject: str):
    for pdf in sorted(folder.glob("*.pdf")):
        if should_skip(pdf):
            log(f"  [skip] {pdf.name}")
            continue
        # 루이스 폴더는 subject 폴더명으로 고정 (교재 문제라 내용 분류 불필요)
        run_parser(pdf, ["--subject", subject, "--split"], f"루이스/{subject}")


def process_root_pdfs(root: Path):
    for pdf in sorted(root.glob("*.pdf")):
        if should_skip(pdf):
            log(f"  [skip] {pdf.name}")
            continue
        run_parser(pdf, ["--subject", "linguistics"], "루트")


def main():
    log(f"ROOT: {ROOT}")
    log(f"PARSER: {PARSER}")

    kibchul_raw = ROOT / "기출 raw"
    if kibchul_raw.exists():
        log("\n" + "=" * 60)
        log("■ 기출 raw 처리")
        process_kibchul_raw(kibchul_raw)

    lewis_ling = ROOT / "루이스 문제 raw" / "영어학"
    if lewis_ling.exists():
        log("\n" + "=" * 60)
        log("■ 루이스 문제 raw / 영어학")
        process_lewis_folder(lewis_ling, "linguistics")

    lewis_edu = ROOT / "루이스 문제 raw" / "영어교육론"
    if lewis_edu.exists():
        log("\n" + "=" * 60)
        log("■ 루이스 문제 raw / 영어교육론")
        process_lewis_folder(lewis_edu, "education")

    log("\n" + "=" * 60)
    log("■ 루트 레벨 PDF")
    process_root_pdfs(ROOT)

    log("\n" + "=" * 60)
    data_dir = ROOT / "data"
    jsons = list(data_dir.glob("*_draft.json")) if data_dir.exists() else []
    log(f"완료 — 생성된 초안 JSON: {len(jsons)}개")
    log(f"로그: {LOG_FILE}")
    _log_fh.close()


if __name__ == "__main__":
    main()
