"""
기출 PDF → JSON 스켈레톤 + 이미지 추출

사용법:
    python scripts/parse_pdf.py <PDF_경로> [--year 2026] [--form B]
    python scripts/parse_pdf.py <PDF_경로> --split            # 문항별 분리 (권장)
    python scripts/parse_pdf.py <PDF_경로> --split --two-col  # 2단 강제

출력:
    data/{subject}_{year}_{form}{num}_draft.json
    images/{id}_p{page}.png
"""

import argparse
import json
import re
import sys
from pathlib import Path

import pdfplumber
import fitz  # PyMuPDF


ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
IMAGES_DIR = ROOT / "images"

IMAGE_DPI = 200
IMAGE_THRESHOLD = 1


# ── 2단 레이아웃 감지 ─────────────────────────────────────────────────────────

def _is_two_column(page) -> bool:
    """
    임용고시 2단 레이아웃 감지.

    2011년 이후 전공영어 시험지(A3, width≈842pt)는 좌우 2단 구성.
    2010 2차 시험(A4±, width≈729pt)은 단일 컬럼.

    헤더 영역(수험번호·지시문)이 페이지 전폭에 걸쳐 있어도
    본문은 2단이므로, width >= 800 이면 무조건 2단으로 간주.
    """
    return page.width >= 800


def _find_col_split(page) -> float:
    """
    좌우 컬럼 경계 x 좌표를 단어 분포에서 자동 탐색.
    중앙 40-60% 구간에서 단어가 가장 적은 x 버킷의 중심 반환.
    없으면 page.width * 0.50 반환.
    """
    words = page.extract_words()
    if not words:
        return page.width * 0.50

    w = page.width
    bins = 40  # 페이지를 40 등분
    bucket_size = w / bins
    lo, hi = int(bins * 0.40), int(bins * 0.60)

    counts = [0] * bins
    for wd in words:
        b = min(int(float(wd["x0"]) / bucket_size), bins - 1)
        counts[b] += 1

    # 중앙 구간에서 최소 버킷
    min_bucket = min(range(lo, hi), key=lambda b: counts[b])
    return (min_bucket + 0.5) * bucket_size


def extract_column_text(page, split_x: float, left: bool) -> str:
    """
    좌/우 컬럼 텍스트 추출.

    extract_text() 는 Y 좌표가 비슷한 좌우 컬럼 단어를 같은 줄로 묶어버리는
    문제가 있으므로, extract_words() 로 단어를 수동 필터링하고 재조합.
    """
    w = page.width
    margin = w * 0.03
    x0_limit = split_x - 2 if left else split_x + 2
    x1_limit = split_x - 2 if not left else w - margin

    all_words = page.extract_words()
    if not all_words:
        return ""

    # 해당 컬럼 범위 단어만 추출
    col_words = [
        wd for wd in all_words
        if (left and float(wd["x0"]) < x0_limit) or
           (not left and float(wd["x0"]) >= x0_limit)
    ]
    if not col_words:
        return ""

    # Y 좌표 기준 라인 그룹핑 (tolerance: 3pt)
    LINE_TOL = 3.0
    col_words.sort(key=lambda wd: (float(wd["top"]), float(wd["x0"])))

    lines: list[list[dict]] = []
    current_line: list[dict] = [col_words[0]]
    for wd in col_words[1:]:
        if abs(float(wd["top"]) - float(current_line[-1]["top"])) <= LINE_TOL:
            current_line.append(wd)
        else:
            lines.append(current_line)
            current_line = [wd]
    lines.append(current_line)

    return "\n".join(" ".join(wd["text"] for wd in line) for line in lines)


def extract_text_by_page(pdf_path: Path, force_two_col: bool = False) -> list[str]:
    """
    페이지별 텍스트 추출.
    2단 레이아웃: 좌측 컬럼 전체 → 우측 컬럼 전체 순서로 합침.
    """
    pages: list[str] = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            if force_two_col or _is_two_column(page):
                split_x = _find_col_split(page)
                left_text = extract_column_text(page, split_x, left=True)
                right_text = extract_column_text(page, split_x, left=False)
                pages.append((left_text + "\n" + right_text).strip())
            else:
                pages.append(page.extract_text() or "")
    return pages


# ── subject 자동 판단 ─────────────────────────────────────────────────────────

# 영어교육론: 교수법·교실 활동·커리큘럼 관련 전문 용어
EDUCATION_STRONG = [
    # 교수법/교육론 전문 용어 (3점)
    "lesson plan", "corrective feedback", "scaffolding", "task-based",
    "communicative language teaching", "CLT", "content-based instruction",
    "needs analysis", "curriculum development", "syllabus",
    "formative assessment", "summative assessment", "rubric", "portfolio",
    "error correction", "noticing hypothesis", "output hypothesis",
    "input hypothesis", "affective filter", "comprehensible input",
    "second language acquisition", "SLA", "zone of proximal development", "ZPD",
    "extensive reading", "intensive reading", "process writing",
    "think-aloud", "metacognitive", "CLIL", "genre-based",
    "cooperative learning", "collaborative learning",
    "teacher's journal", "teaching journal",
    "textbook selection", "textbook evaluation",
    "test specifications", "test components", "test items",
    # 교실 맥락 명확 지시어
    "teacher", "classroom", "학습자", "교수법", "교육과정", "수업지도안",
]
EDUCATION_WEAK = [
    "student", "learner", "instruction",
    "teaching", "curriculum",
    "assessment", "feedback",
    "textbook",
]

# 영어학: 언어학 이론 용어
LINGUISTICS_STRONG = [
    "phoneme", "allophone", "morpheme", "allomorph",
    "phonological rule", "morphological", "derivational", "inflectional",
    "syntactic", "semantic", "pragmatic",
    "complementary distribution", "minimal pair",
    "X-bar", "phrase structure", "deep structure", "surface structure",
    "coarticulation", "aspiration", "fricative", "plosive", "nasal", "lateral",
    "illocutionary", "perlocutionary", "cooperative principle",
    "presupposition", "entailment", "prototype",
    "word formation", "compounding", "blending", "clipping",
    "sonority", "onset", "nucleus", "coda", "syllable",
    "NP", "VP", "CP", "TP",
    # 음운론 추가
    "homophones", "geminate", "assimilation", "deletion", "insertion",
    "double consonants", "articulated", "place of articulation",
    "manner of articulation", "voiced", "voiceless", "bilabial",
    # 의미론/화용론 추가
    "speech act", "discourse marker", "anaphora", "cataphora",
    # 형태통사론 추가
    "passive voice", "active voice", "transitive", "intransitive",
    # 어휘의미론 추가
    "lexical aspect", "atelic", "telic", "durative", "stative",
    "accomplishment verb", "achievement verb", "activity verb", "state verb",
    # 한국어
    "형태론", "통사론", "음운론", "의미론", "화용론",
]
LINGUISTICS_WEAK = [
    "phonology", "morphology", "syntax", "phonetic",
    "lexical", "consonant", "vowel", "stress", "intonation",
    "parse", "clause", "constituent",
    "pronunciation", "articulation", "accent",
    "discourse",
]

# 일반영어(문학): 문학 장르·작품 관련 용어
GENERAL_STRONG = [
    "novel", "poem", "poetry", "stanza", "rhyme",
    "prose", "fiction", "narrative", "narrator",
    "protagonist", "antagonist", "metaphor", "simile", "imagery",
    "soliloquy", "monologue", "dialogue in a play",
    "excerpt from a play", "excerpt from a novel", "excerpt from a poem",
    "short story", "literary", "dramatist", "playwright",
    "chapter", "verse", "couplet", "sonnet", "allegory",
]
GENERAL_WEAK = [
    "excerpt", "passage", "character", "plot", "theme",
    "setting", "tone", "voice", "symbol",
]


def classify_subject(text: str) -> str:
    """
    개별 문항 텍스트에서 subject 판단.

    우선순위:
    1. 언어학 전문 용어 강 신호 (AND education 신호가 약할 때) → linguistics
    2. 교실/교수법 맥락 (teacher/student/classroom 등) → education
    3. 문학 전문 용어 → general
    4. 언어학 약 신호 → linguistics
    5. 기본값 → general
    """
    t = text.lower()

    ling_strong = sum(1 for kw in LINGUISTICS_STRONG if kw.lower() in t)
    ling_weak   = sum(1 for kw in LINGUISTICS_WEAK   if kw.lower() in t)
    edu_strong  = sum(1 for kw in EDUCATION_STRONG   if kw.lower() in t)
    edu_weak    = sum(1 for kw in EDUCATION_WEAK     if kw.lower() in t)
    gen_strong  = sum(1 for kw in GENERAL_STRONG     if kw.lower() in t)

    ling_score = ling_strong * 3 + ling_weak
    edu_score  = edu_strong  * 3 + edu_weak
    gen_score  = gen_strong  * 3

    # 1. 언어학 강 신호 압도 (교육/문학 신호를 합쳐도 초과) → linguistics
    if ling_strong >= 2 and ling_score > edu_score + gen_score + 2:
        return "linguistics"

    # 2. 문학 지문 (narrator, poem, novel, play excerpt 등) → general
    #    교육론 지문 안에 문학 발췌가 들어있을 수 있으나,
    #    gen_strong >= 1 이면 일반영어로 분류 (임용고시 패턴상 우선)
    if gen_strong >= 1:
        return "general"

    # 3. 교육 맥락 → education
    if edu_strong >= 1 or edu_weak >= 3:
        return "education"

    # 4. 언어학 약한 신호라도 있으면 → linguistics
    if ling_strong >= 1 or ling_weak >= 1:
        return "linguistics"

    # 기본값
    return "general"


# ── 이미지 추출 ──────────────────────────────────────────────────────────────

def render_image_pages(pdf_path: Path, doc_id_prefix: str) -> list[dict]:
    """이미지가 포함된 페이지를 PNG 로 저장."""
    IMAGES_DIR.mkdir(exist_ok=True, parents=True)
    saved: list[dict] = []
    doc = fitz.open(pdf_path)
    try:
        for i, page in enumerate(doc, start=1):
            images = page.get_images(full=True)
            if len(images) < IMAGE_THRESHOLD:
                continue
            pix = page.get_pixmap(dpi=IMAGE_DPI)
            out_path = IMAGES_DIR / f"{doc_id_prefix}_p{i:02d}.png"
            pix.save(out_path)
            saved.append({
                "page": i,
                "file": str(out_path.relative_to(ROOT)).replace("\\", "/"),
                "image_count": len(images),
            })
    finally:
        doc.close()
    return saved


# ── 문항 블록 분리 ───────────────────────────────────────────────────────────

def detect_question_blocks(full_text: str) -> list[dict]:
    """
    임용고시 문항 번호 패턴으로 텍스트를 문항별로 분리.

    매칭 규칙:
    1) 줄 시작 + 숫자(1-20) + 마침표 + 공백  →  "1. "  "12. "
       (괄호형 "1) "은 지문 내 예제이므로 제외)
    2) 실제 시험 문항 필터: 같은 줄에 배점 표기가 있어야 함
       - "[1.5점]", "[2.5점]"  (2010-2013 형식)
       - "【2 points】", "【4 points】"  (2015+ 형식)
    3) 배점 표기 없는 PDF는 필터 없이 전체 블록 사용(폴백)
    """
    # 임용고시 배점 표기 패턴
    SCORE_RE = re.compile(
        r"[\[【]\s*\d+(?:\.\d+)?\s*(?:점|points?)[\]】]",
        re.IGNORECASE,
    )

    # 문항 번호 패턴 (마침표 only, 1-49)
    # 2011년 이전 시험은 Q1~Q40 범위 사용
    pattern = re.compile(
        r"(?m)^[\s　]*((?:[1-9]|[1-4][0-9]))\.\s+"
    )
    matches = list(pattern.finditer(full_text))
    if not matches:
        return []

    # 각 매치 → (number, 줄 끝까지 텍스트, 시작 위치)
    raw_blocks: list[dict] = []
    for idx, m in enumerate(matches):
        start = m.start()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(full_text)
        num_str = m.group(1)
        block_text = full_text[start:end].strip()
        # 배점은 지문 지시문 안에 있으므로 첫 800자 내에서 탐색
        # (2011년 이전 형식은 긴 지문 뒤에 배점이 오는 경우 있음)
        header = block_text[:800]
        raw_blocks.append({
            "number": num_str,
            "text": block_text,
            "has_score": bool(SCORE_RE.search(header)),
        })

    # 배점 표기가 있는 블록만 취함 (없으면 폴백: 전체)
    scored = [b for b in raw_blocks if b["has_score"]]
    blocks = scored if scored else raw_blocks

    # 너무 짧은 블록(< 80자)은 이전 블록에 병합
    MIN_BLOCK_LEN = 80
    merged: list[dict] = []
    for blk in blocks:
        if merged and len(blk["text"]) < MIN_BLOCK_LEN:
            merged[-1]["text"] += "\n" + blk["text"]
        else:
            merged.append(blk)

    return merged


# ── 파일명 메타데이터 파싱 ────────────────────────────────────────────────────

def parse_metadata_from_stem(pdf_path: Path, year_arg, form_arg) -> tuple[int, str]:
    stem = pdf_path.stem
    if year_arg:
        year = year_arg
    else:
        m = re.search(r"(20\d{2})", stem)
        year = int(m.group(1)) if m else 0

    if form_arg:
        form = form_arg.upper()
    else:
        m = re.search(r"전공\s*([AB])", stem)
        if not m:
            m = re.search(r"[_\-\s]([AB])(?:[_\-\s]|\.pdf|문제지|$)", stem, re.IGNORECASE)
        form = m.group(1).upper() if m else "X"

    return year, form


# ── JSON 스켈레톤 ────────────────────────────────────────────────────────────

def build_skeleton(doc_id: str, year: int, number: str, subject: str,
                   raw_text: str, image_pages: list[dict]) -> dict:
    return {
        "meta": {
            "id": doc_id,
            "year": year,
            "number": number,
            "subject": subject,
            "question_type": "short_answer",
            "score": 0,
            "tags": [],
        },
        "problem": {
            "instruction": "",
            "passage": raw_text.strip(),
            "blanks": [],
        },
        "derivation": {
            "steps": [],
            "vocabulary": [],
            "translation": "",
        },
        "answer": {
            "model_answer": {
                "blank_answers": [],
                "essay_content": "",
                "scoring_criteria": [],
            },
            "variants": [],
        },
        "source": {
            "references": [],
            "concept_explanation": "",
        },
        "related": {
            "enabled": subject != "general",
            "questions": [],
        },
        "_extraction": {
            "image_pages": image_pages,
            "note": "자동 추출 초안. passage/meta/answer 모두 수동 보완 필요.",
        },
    }


# ── main ─────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(description="기출 PDF → JSON 스켈레톤 변환")
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--year", type=int)
    parser.add_argument("--subject", choices=["linguistics", "general", "education"],
                        help="생략 시 문항별로 내용 자동 판단")
    parser.add_argument("--form", choices=["A", "B", "X"])
    parser.add_argument("--number", help="단일 파일 출력 시 문항 번호")
    parser.add_argument("--split", action="store_true", help="문항별 JSON 분리 생성")
    parser.add_argument("--two-col", action="store_true", help="2단 레이아웃 강제")
    args = parser.parse_args()

    if not args.pdf.exists():
        print(f"[!] PDF 없음: {args.pdf}", file=sys.stderr)
        return 1

    DATA_DIR.mkdir(exist_ok=True, parents=True)

    year, form = parse_metadata_from_stem(args.pdf, args.year, args.form)

    # 2단 감지 결과 표시 (텍스트 추출 전에 확인)
    with pdfplumber.open(args.pdf) as pdf:
        two_col_detected = args.two_col or (
            bool(pdf.pages) and _is_two_column(pdf.pages[0])
        )

    # 텍스트 추출
    pages = extract_text_by_page(args.pdf, force_two_col=args.two_col)
    full_text = "\n\n".join(pages)

    print(f"[*] PDF   : {args.pdf.name}")
    print(f"[*] 연도  : {year}  form: {form}  pages: {len(pages)}")
    print(f"[*] 텍스트: {len(full_text):,}자")
    print(f"[*] 2단   : {'강제' if args.two_col else ('감지됨' if two_col_detected else '단일컬럼')}")

    # 이미지 추출 (prefix용 임시 ID)
    img_prefix = f"img_{year}_{form}"
    image_pages = render_image_pages(args.pdf, img_prefix)
    if image_pages:
        print(f"[*] 이미지 {len(image_pages)}페이지 → images/")

    if args.split:
        blocks = detect_question_blocks(full_text)
        print(f"[*] 감지된 문항: {len(blocks)}개")
        if not blocks:
            print("[!] 문항 패턴 미감지 → 전체 단일 파일로 저장")
            subject = args.subject or classify_subject(full_text)
            doc_id = f"{subject}_{year}_{form}00"
            skel = build_skeleton(doc_id, year, f"{form}-0", subject, full_text, image_pages)
            out = DATA_DIR / f"{doc_id}_draft.json"
            out.write_text(json.dumps(skel, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"    → {out.relative_to(ROOT)}")
        else:
            for blk in blocks:
                num_int = int(blk["number"])
                # subject: CLI 고정 또는 문항별 자동 판단
                subject = args.subject or classify_subject(blk["text"])
                num_label = f"{form}-{num_int}"
                doc_id = f"{subject}_{year}_{form}{num_int:02d}"
                skel = build_skeleton(doc_id, year, num_label, subject,
                                      blk["text"], image_pages)
                out = DATA_DIR / f"{doc_id}_draft.json"
                out.write_text(json.dumps(skel, ensure_ascii=False, indent=2), encoding="utf-8")
                print(f"    [{subject:12s}] {num_label} → {out.name}")
    else:
        subject = args.subject or classify_subject(full_text)
        number = args.number or f"{form}-0"
        doc_id = f"{subject}_{year}_{form}00"
        skel = build_skeleton(doc_id, year, number, subject, full_text, image_pages)
        out = DATA_DIR / f"{doc_id}_draft.json"
        out.write_text(json.dumps(skel, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[*] 저장: {out.relative_to(ROOT)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
