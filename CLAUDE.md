# 전공영어 기출마스터 — CLAUDE.md

## 설정

* **기본 모델:** claude-sonnet-4-6
* **프로젝트**: 중등 영어 임용고시 기출문제 분석 웹사이트. GitHub Pages 배포. 순수 HTML/CSS/JS.

---

## 확정 설계

### 카드 탭 순서

문제 → 도출과정 → 정답 → 연결문제
(원전은 정답 탭 하단 구분선 아래 배치)

### 과목 분류

| 코드 | 과목 |
|------|------|
| `linguistics` | 영어학 |
| `education` | 영어교육론 |
| `general` | 일반영어 (문학 포함) |

### 연결문제

* 영어학 ↔ 영어학만 연결
* 영어교육론 ↔ 영어교육론 연결 / 객관식 답안 키워드 링크
* 일반영어: 연결문제 없음 (`related.enabled: false`)
* 미등록 카드: 샘플 안내 표시

### 필터 UI

드롭다운 3개 한 줄: [영역 ▾] [연도 ▾] [문제 선택 ▾]

**문제 선택 정렬**: 전공A → 전공B, 숫자 오름차순. 같은 번호면 연도 최신순.

---

## 답안 작성 기준

### 신뢰도 원칙 (최우선)

> 모든 답안은 역대 강사(이동걸, 최진호, 유희태팀, 권영주, 최시원 등) + 합격자 답안을 1차 근거로 삼는다. Claude 독자 창작 금지.

**단답형**
- 역대 강사 공통 답 = 모범답안. 이견 없으면 그대로.
- 순서 지시(①②) 있으면 반드시 순서 지킴. 대소문자: 문제 요구 형태, 없으면 소문자.
- variants 비워둠 — 단답형은 정답이 하나.
- 강사 간 이견 시: 다수 의견 채택. 소수 의견 기재 안 함.

**서술형**
- 역대 강사 + 합격자 답안 분석 → 공통 채점 포인트 추출 → 재작성.
- 강사/합격자 실명 금지. 문장 그대로 복사 금지 — 반드시 재작성.
- 26년도 강사 답 없음 → variants 비워둠.

### 서술형 작성 스타일

- **분량**: 채점 기준 항목당 1–2문장. 총 3–5문장. 모범답안 ≈ variant 1개 분량 (40–60w). A+B 합산 수준이면 과다.
- **시작**: `The [noun] is...` / `[Subject] [verb]s...` — "In this passage..." 금지.
- **증거**: 지문 인용은 따옴표 + 핵심어만. 4단어 초과 연속 인용 금지.
- 결론 문장("In conclusion...") 불필요. 마지막 채점 포인트로 끝냄.
- 합격자 스타일: 짧고 명확하게. 강사처럼 길게 쓰지 않는다.

### 과목별 서술형 구조

**영어학**
```
[Feature/Process] applies when [environment].          ← 음운론
Sentence (X) is [grammatical/ungrammatical].           ← 통사론
[Violation name] is violated because [explanation].
The [suffix/process] attaches to [condition].          ← 형태론
```

**영어교육론**
```
[Item A] [does/shows] [X] in that [evidence].
[Item B] [does/shows] [Y] since [evidence].
```
- 각 항목 1문장. `in that` / `since` / `by -ing`으로 근거 연결.
- 교사 행동 기술. 평가하지 않음.

**일반영어**
```
The underlined part means that [paraphrase in context].   ← 밑줄
[Topic sentence]. First, [support]. Second, [support].    ← 논술
```
- 직접 번역 금지 — 맥락 속 의미로. 지문 내용만. 외부 지식 추가 금지.

### variants 작성 기준

```
model_answer  → 강사·합격자 공통 포인트 기반, 합격자 스타일 대표 답안
variants[A]   → 강사 답안 스타일 재작성 (문장 구조 변형)
variants[B]   → 합격자 답안 스타일 재작성 (증거 제시 방식 변형)
```
- variants는 model_answer 내용을 벗어나지 않는다.
- **단답형은 variants 작성하지 않음** (서술형 전용).

### 감점 패턴

| 금지 패턴 | 이유 |
|-----------|------|
| "In this passage, ..." 로 시작 | 불필요한 도입 |
| 4단어 이상 연속 인용 | 채점 기준 위반 |
| ①② 순서 바꾸기 | 지시 위반 |
| 추측성 표현 ("might be...") | 확신 있게 서술 |
| "In conclusion, ..." | 서술형에서 불필요 |
| 과도한 부연 | 채점 기준 초과 |
| 영어교육론 오개념 삽입 | 반드시 원전 정의 기준 |

**영어교육론 핵심 오개념**

| 개념 | 금지 표현 | 올바른 표현 |
|------|-----------|------------|
| Reformulation | "언어적 정확성·적절성 개선" | "어휘·문법·문체를 native-like하게 전체 재작성" (Ellis, 2008) |
| Reformulation | "내용·조직 유지" | "학습자의 의미(meaning) 최대한 유지" — 조직 변경 가능 |
| Pragmatic competence | Canale & Swain (1980) | C&S는 Sociolinguistic Competence; Pragmatic competence는 Bachman (1990) |

---

## 렌더링 규칙 (render.js)

### 정답 탭

- **단답형** (`essay_content` 없음): `blank_answers` 박스만 → 구분선 → 원전 → 개념정리
- **서술형** (`essay_content` 있음): 모범답안 → 채점기준 → 변형답안 → 구분선 → 원전 → 개념정리

### 전체 탭 구조

| 탭 | 내용 |
|----|------|
| 문제 | instruction 박스 + passage (`.blank`, `.eg-block`, `.prob-section-label`) |
| 도출과정 | 5단계 steps + vocabulary(있을 때) + 지문 해석(일반영어만) |
| 정답 | 위 정답 탭 규칙 참조 |
| 연결문제 | `related.enabled: false` 또는 `subject: general`이면 안내 문구 |

### 하이라이트 자동 적용

`allKeyTerms` = `derivation.key_terms[].term` + 각 `step.key_terms[]` + `blank_answers[].answer`

| 클래스 | 색상 | 자동 적용 범위 |
|--------|------|--------------|
| `step-text em` | orange (`--accent3`) | 모든 step explanation (step.key_terms 우선 → allKeyTerms 순) |
| `ref-hl` | blue (`--accent`) | ref-quote (수동 span 없으면 allKeyTerms로 fallback) |
| `trans-hl` | teal (`--accent2`) | 지문 해석 (수동 span 없으면 allKeyTerms로 fallback) |

**trans-hl 적용 기준** (일반영어 translation 필드):
- 단답형: 빈칸 정답의 직접 근거 문장
- 서술형: 채점 포인트별 핵심 근거 문장
- 단락당 1–3개. 과도 적용 금지.

### CSS 태그 색상

| 과목 | 클래스 | 색상 |
|------|--------|------|
| 영어학 | `tag-ling` | 보라 (`#a897f5`) |
| 영어교육론 | `tag-edu` | 연초록 (`#b8d070`) |
| 일반영어 | `tag-gen` | 초록 (`#a8d070`) |
| 소설/희곡/시 | `tag-novel` | 연보라 (`#d097f5`) |

### 통사 트리 (SVG)

- **대상**: `linguistics_domain: syntax`에서 트리 구조 필요 시
- **위치**: `derivation.steps[n].tree` 필드 → render.js가 SVG 자동 렌더링
- **노드**: `{ "label", "children"?, "trace"?(분홍), "empty"?(회색) }`
- **이동 화살표**: root에 `"movements": [{"from": "id", "to": "id"}]`

---

## JSON 스키마

파일명: `{subject}_{year}_{form}{number}.json`

```json
{
  "meta": {
    "id": "linguistics_2026_B01",
    "year": 2026,
    "number": "B-1",
    "subject": "linguistics",
    "linguistics_domain": "morphology",
    "question_type": "short_answer",
    "score": 2,
    "tags": ["inflectional suffix"],
    "parse_source": "PDF 파일명",
    "parse_confidence": "high",
    "verified": false
  },
  "problem": {
    "instruction": "Fill in each blank...",
    "passage": "지문 전체",
    "blanks": [{ "label": "①", "context": "grammatical ___ of the stem" }]
  },
  "derivation": {
    "steps": [
      {
        "step": 1,
        "label": "범위 설정",
        "explanation": "설명 텍스트",
        "key_terms": ["핵심용어"]
      }
    ],
    "key_terms": [
      {
        "term": "Noticing Hypothesis",
        "definition_en": "영어 정의",
        "definition_ko": "한국어 정의",
        "source_author": "Schmidt",
        "source_year": 1990,
        "related_terms": ["intake"],
        "exam_usage": "출제 맥락"
      }
    ],
    "vocabulary": [{ "word": "단어", "pos": "n.", "definition_ko": "뜻", "example": "예문" }],
    "translation": "일반영어만. 영어학·교육론은 빈 문자열. trans-hl 포함."
  },
  "answer": {
    "model_answer": {
      "blank_answers": [{ "label": "①", "answer": "category" }],
      "essay_content": "서술형만. 단답형은 빈 문자열.",
      "scoring_criteria": [{ "criterion": "① category", "points": 1 }]
    },
    "variants": [
      { "label": "답안 A", "source_type": "instructor", "content": "재작성" },
      { "label": "답안 B", "source_type": "passer",     "content": "재작성" }
    ]
  },
  "source": {
    "references": [{
      "type": "textbook",
      "author": "Fromkin, Rodman & Hyams",
      "title": "An Introduction to Language (11th ed.)",
      "year": 2018,
      "publisher": "Cengage Learning",
      "pages": "pp. 64-72",
      "excerpt": "원전 발췌문. ref-hl 포함."
    }],
    "concept_explanation": "개념 보충. Wikipedia 지양."
  },
  "related": {
    "enabled": true,
    "questions": [{
      "id": "linguistics_2022_A03",
      "year": 2022,
      "number": "A-3",
      "subject": "linguistics",
      "connection_type": "same_concept",
      "connection_note": "연결 이유",
      "shared_keywords": ["ordering constraint"]
    }]
  }
}
```

### 과목별 derivation 작성 규칙

> 과목 간 풀이 방식 혼용 금지. 특히 영어학·교육론에 일반영어 방식 적용 금지.

**영어학**: 이론 개념 식별 → 지문 데이터 적용 → 이론 귀속
- `key_terms`: 반드시 작성. `source_author` + `source_year` 필수.
- `translation`: 빈 문자열.
- `linguistics_domain` 필수: `phonology | morphology | syntax | semantics | pragmatics | sociolinguistics | acquisition`

**영어교육론**: 지문 속 교사·학습자 행동 → 교수법/이론 정의 매핑 → 소거
- `key_terms`: 반드시 작성. 교수법/가설 이론가 명시.
- `translation`: 빈 문자열.
- 후보 소거는 교수법 정의 범위로 (passage-bound 단어 검색 아님).

**일반영어·문학**: 지문 ↔ commentary/발문 대응 → passage-bound 단어 검색
- `key_terms`: 빈 배열.
- `translation`: 지문 전문 한국어 해석. 요약본 금지. trans-hl 적용 필수.
- `related.enabled`: false.

### 개념 정리(concept_explanation) 언어 규칙

- **영어학·교육론**: 영어 원문 먼저, 한국어 괄호 병기. 영어 용어 원어 사용.
- **일반영어**: 한국어 위주. 영어 인용은 지문 핵심 표현만.
- `definition_en`은 영어로, `definition_ko`는 한국어로. 혼용 금지.

---

## 참조 우선순위

1. **서브노트 kimmie** — 영어교육론·영어학 1순위. 시험 출제 맥락 기준.
2. 교재/논문 원전 (Ellis, Richards, Fromkin, Carnie 등)
3. Wikipedia 사용 금지

---

## 현재 데이터 현황 (2026-04-16 기준)

| 과목 | 완성본 | draft |
|------|--------|-------|
| `education` | 8 | 111 |
| `general` | 7 | 117 |
| `linguistics` | 8 | 90 |

- 완성본 기준 파일: `linguistics_2026_B01.json`
- 다른 연도 작업 시 2026년도 구조 참조.
- `parse_confidence: low` → 수동 검토 후 `verified: true` 처리.

---

## Git 워크플로우

- **Claude가 직접** feature 브랜치 커밋 → main merge → push 까지 처리.
- 사용자가 GitHub에서 별도 merge 불필요.
- 순서: feature 브랜치 작업 → `git checkout main` → `git merge <branch>` → `git push origin main`
