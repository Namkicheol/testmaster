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

| 코드 | 과목 | 필터 표시 |
|------|------|----------|
| `linguistics` | 영어학 | 영어학 |
| `education` | 영어교육론 | 영어교육론 |
| `general` (literary 태그 없음) | 일반영어 | 일반영어 |
| `general` + literary 태그 | 일반영어(문학) | 일반영어(문학) |

**literary 태그**: `novel`, `play`, `poem`, `poetry`, `drama`, `fiction`, `essay`
→ JSON `meta.subject`는 항상 `"general"`. 태그로 렌더링/필터 분기.

### 연결문제

* 영어학 ↔ 영어학만 연결
* 영어교육론 ↔ 영어교육론 연결 / 객관식 답안 키워드 링크
* 일반영어 · 일반영어(문학): 연결문제 없음 (`related.enabled: false`)
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
| Washback | "점수와 코멘트의 일치 원칙" | **testing이 teaching/learning에 미치는 영향** (Brown, 2004). 점수-코멘트 불일치 문제는 'feedback consistency'로 구분할 것 |

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
| `step-text em` | orange (`--accent3`) | step explanation — `step.key_terms` + `answerWords` |
| `term-hl` | lavender (`#c4a8ff`) | step explanation — `derivation.key_terms[].term` (이론 용어) |
| `ref-hl` | blue (`--accent`) | ref-quote (수동 span 없으면 allKeyTerms로 fallback) |
| `trans-hl` | teal (`--accent2`) | 지문 해석 (수동 span 없으면 allKeyTerms로 fallback) |

**하이라이트 우선순위**: `term-hl` 먼저 적용 → `em` 적용 시 이미 태그된 용어 건너뜀.

### ⚠️ key_terms 작성 금지 패턴 (하이라이트 실패 원인)

render.js는 `key_terms[].term`을 **문자열 그대로 case-insensitive 검색**하여 `concept_explanation`·`step.explanation`에 하이라이트를 적용한다.  
term 형태가 실제 텍스트와 다르면 매칭 실패 → 하이라이트 없음.

| ❌ 실패 패턴 | 실제 사례 | ✅ 올바른 형태 |
|------------|----------|-------------|
| 괄호로 부가 설명 병기 | `Geminate (consonant)` | `Geminate` |
| 대괄호로 음성 기호 표기 | `[anterior]` | `anterior` |
| 괄호로 별칭(alias) 병기 | `Yod-dropping (j-dropping)` | `Yod-dropping` |
| 괄호로 독일어/학술명 병기 | `Lexical aspect (Aktionsart)` | `lexical aspect` |
| 괄호로 약어 병기 | `Complementizer (C)` | `complementizer` |
| 서술적 구문으로 작성 | `Constructive Alignment`, `Context Clue Strategy` | `alignment`, `context clue` |
| 단어 나열형 | `Grammatical category` (concept에 `category`만 있는 경우) | concept에 맞는 최소 핵심어 |

**규칙 요약:**
1. `term`은 반드시 `concept_explanation` 또는 `step.explanation` 본문에 **그 형태 그대로** 등장해야 한다.
2. 괄호·대괄호·별칭·약어 병기 금지 — 핵심어 단독으로.
3. term 작성 후 concept_explanation에 해당 단어가 포함되어 있는지 **반드시 확인**.
4. concept_explanation이 없으면 term이 있어도 하이라이트 불가 → concept 작성 필수.

### ⚠️ step.key_terms 작성 금지 패턴 (em 하이라이트 실패 원인)

`step.key_terms`는 해당 step의 `explanation` 텍스트에서 em(빨간 배경) 하이라이트로 표시된다.  
텍스트에 없는 문자열을 넣으면 하이라이트 없음.

| ❌ 실패 패턴 | 실제 사례 | ✅ 올바른 형태 |
|------------|----------|-------------|
| 구조적 레이블 | `"Principle 5 for Material 1"` | `"pragmatic skills"` (step 텍스트에 실제 등장하는 용어) |
| 결론형 레이블 | `"Material 1 → Principle 5 / Material 2 → Principle 2"` | `"communicative drill"` |
| 아이템 번호 | `"Item 1 and Item 20"` | `"main idea"`, `"specific detail"` |
| 설명형 구문 | `"modifying definition"`, `"elimination method"` | `"modifying"`, `"reordering"` |
| 참조-대응형 레이블 | `"Product 4 for Ms. Song"`, `"Tip 2 for Activity 1"`, `"Characteristic 2 for Mr. Kang"` | `"Product 4"`, `"Tip 2"`, `"Characteristic 2"` |
| 소거법 설명 구문 | `"scoring consistency"`, `"cultural comparison"`, `"same task different support"` | 실제 step 텍스트에 등장하는 단어만 |
| 한국어 step에 영어 term | step 텍스트가 한국어인데 `"peer feedback"`, `"mixed-ability"` 등 영어 term 기재 | `[]` — 한국어 텍스트에서는 실제로 쓰인 영어 용어만 추출, 없으면 빈 배열 |
| 비어 있는 step | steps 1·2·5 모두 `[]` | 해당 step 텍스트에서 핵심 용어 추출하여 채움 |

**step.key_terms 작성 원칙:**
1. 모든 step에 key_terms를 채우려 하되, 실제로 step 텍스트에 **그 문자열이 등장**해야 한다.
2. step.key_terms ≠ 그 step의 요약 레이블. 텍스트 내 단어를 그대로 추출.
3. 영어 key_term은 영어로 적힌 step 텍스트에서, **한국어로만 쓰인 step은 `[]`** — 강제로 채우지 않는다.
4. `derivation.key_terms[].term`은 모든 step 텍스트에 term-hl(주황 밑줄)로 자동 적용되므로 step.key_terms와 중복 불필요.
5. "for X", "vs. Y", "→" 등 비교·대응 구문이 포함된 항목은 100% 실패 → 핵심 단어만 단독으로.

**영어교육론·영어학 파일 작성 시 체크리스트:**
- [ ] `derivation.key_terms` 배열이 비어 있지 않은가 (용어 카드 표시 필수)
- [ ] step 1·2·5가 모두 비어 있지는 않은가
- [ ] step.key_terms 각 항목이 해당 step.explanation 텍스트에 실제로 존재하는가

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
| 일반영어(문학) | `tag-lit` | 연보라 (`#d8a0f5`) |
| 소설/희곡/시 세부 | `tag-novel` | 진보라 (`#d097f5`) |

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

1. **`refs/` 합격자 자료** (아래 참조) — 영어교육론 개념·오개념 검증 최우선
2. **서브노트 kimmie** — 영어교육론·영어학 1순위. 시험 출제 맥락 기준.
3. 교재/논문 원전 (Ellis, Richards, Fromkin, Carnie 등)
4. Wikipedia 사용 금지

---

## refs/ 참조 파일 (영어교육론 개념 검증용)

> **gitignored** — 로컬 전용. 영어교육론 JSON 작업 시 개념·오개념 판단의 최우선 기준.  
> 모두 **합격자가 직접 작성**한 자료 → 시험 출제 관점에서 가장 신뢰도 높음.

| 파일 | 내용 | 분량 |
|------|------|------|
| `refs/subnote_all.md` | 영어교육론 서브노트 전체 (Ch.1–13, kimme 기반) | ~4200줄 |
| `refs/keywords.md` | 연도별 기출 키워드 정리 + 출처(PLLT 등) | ~1600줄 |
| `refs/mapping.md` | 교수법 개념 맵핑 (루이스 기반, Behaviorism→Constructivism 계보) | ~1800줄 |

### 언제 참조하는가

- **개념 정의** 작성 시: 이론가·연도·정의 문구가 refs와 일치하는지 확인
- **오개념 의심** 시: `refs/subnote_all.md`에서 해당 이론 챕터 검색 → 정확한 정의 대조
- **키워드 맥락** 확인: `refs/keywords.md`에서 같은 키워드의 연도별 출제 패턴 확인
- **이론 계보·관계** 파악: `refs/mapping.md`에서 상위/하위 개념 위치 확인

### refs/ 활용 원칙

1. `subnote_all.md` 서술과 다른 정의는 **반드시 재확인** — Claude 독자 판단으로 덮어쓰기 금지.
2. 특히 Communicative Competence 계보, WCF 유형, Interaction Hypothesis, Noticing Hypothesis 등 **자주 오개념이 발생하는 항목**은 refs 대조 필수.
3. 합격자 서술이 원전 교재와 미세하게 다를 경우 → **합격자 서술 우선** (시험 채점 기준에 더 근접).
4. `refs/` 파일은 직접 인용 금지 — 내용 확인 후 JSON에는 재작성하여 기재.

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
