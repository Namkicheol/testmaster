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

**JSON `meta.subject`는 항상 `"general"`**. `meta.tags`에 **literary 태그가 포함되어 있는지** 여부로 렌더링/필터가 분기된다.

#### 문학 vs 일반영어 판정 기준

**문학 (literary)** — 상상적(imaginative) 문학 작품에서 발췌:
- 소설·단편소설 → 태그 `novel` 또는 `fiction`
- 희곡·연극 대본 → 태그 `play` 또는 `drama`
- 시·운문 → 태그 `poem` 또는 `poetry`

**일반영어 (non-literary)** — 비문학 산문:
- 학술 에세이·논설문·설명문·평론·저널 기사·요약 지문 등
- 문학 작품을 **논하는** 비평/해설 글도 비문학 → 일반영어

#### literary 태그 정식 집합

`novel`, `fiction`, `play`, `drama`, `poem`, `poetry` — 이 6개만 literary 태그.

> ⚠️ `essay`는 literary 태그가 아니다. 문학적 수필(literary essay)이어도 `essay` 단독으로는 일반영어로 분류.  
> ⚠️ 작가명·작품명·주제 태그(`Lan Cao`, `Monkey Bridge`, `immigrant narrative` 등)는 분류에 영향 없음 — 반드시 위 6개 중 하나가 있어야 문학.

#### 판정 플로우

```
지문 원전이 상상적 창작물인가?
├─ YES → 장르 식별
│   ├─ 소설/단편 → novel (또는 fiction)
│   ├─ 희곡/드라마 → play (또는 drama)
│   └─ 시/운문 → poem (또는 poetry)
│   → 해당 태그를 meta.tags에 반드시 포함
└─ NO (논설·분석·설명·비평·요약 등) → literary 태그 넣지 않음 → 일반영어
```

작성 후 체크: 새 문항이 문학이라면 `meta.tags`에 `novel|fiction|play|drama|poem|poetry` 중 **최소 1개**가 있어야 한다.

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

#### 일반영어·문학 도출 방법론

> 문제 유형별로 구분. 유형을 먼저 파악하고 아래 해당 전략을 적용할 것.

**① 빈칸 기입형 — Parallelism 전략**

1. Commentary 먼저 읽기: 빈칸이 가리키는 범위(의미 방향, 품사)를 좁힌다.
2. 빈칸 주변 관사·수식어 확인 → 단/복수·품사 형태 결정.
   - 관사 없음 → 복수 우선 (marriages, not marriage)
   - 빈칸의 수식어(enlarging, wild 등)가 정답의 속성을 직접 가리킴
3. Commentary 표현과 지문에서 병렬(parallelism)을 이루는 구조를 찾는다.
   - 노랑=노랑, 초록=초록 식의 어휘·구조 대응 관계 파악
4. **passage-bound 원칙**: 정답은 지문(passage) 안에 그 형태 그대로 존재해야 함. 지문에 없는 단어는 오답.
5. 빈칸 문장이 글의 흐름 전환점(긍정→부정, 부정→긍정)이면 방향 반전 적용.

**② 밑줄 의미 설명형 — Paraphrase 전략**

1. Direction(발문)의 핵심 표현이 지문 어디에서 paraphrase되어 나타나는지 찾는다.
   - 예: "not immediately grasp" ↔ "not understand the letter at once"
2. 밑줄 바로 앞뒤 문장에서 답의 핵심을 추출 → paraphrase.
3. 직접 번역 금지 — 맥락 속 의미로 설명. 4단어 초과 연속 인용 금지.
4. 지문 내 대비 구조(A↔B)를 먼저 파악 → 밑줄이 어느 쪽에 위치하는지 확인.

답안 구조:
```
The underlined part means that [맥락 속 의미 paraphrase].
For example, [지문 근거 — 4단어 이하 인용].
```

**③ Summary형 — Conclusion-first 전략**

1. **결론(마지막 문단) 먼저 읽기** → 무엇을 포함해야 하는지 기준 설정.
2. Topic 파악: 개념 정의가 있으면 포함, 단순 배경 정보는 생략.
3. Supporting ideas: 결론이 요구하는 내용만 paraphrase. 일화·예시는 제외.
4. Conclusion: 실천/제안 부분만 paraphrase. Supporting ideas 재진술은 제외.

답안 구조:
```
[Topic + 핵심 정의/특성]. First, [Supporting idea 1 paraphrase].
Second, [Supporting idea 2 paraphrase]. Thus/In conclusion, [Conclusion paraphrase].
```

**④ 문학(시·희곡·소설) 특화 전략**

- **시(poem)**: Main idea(주제) 파악이 핵심. 키워드 방향성(+/-)에 집중. 각 연의 이미지가 어떤 주제를 형성하는지 파악.
- **희곡(play/drama)**: 인물이 "무엇을 하는지"에 집중. 인물 간 대비 구조(A=영웅↔B=타락) 파악 후 빈칸 도출.
- **소설(novel)**: Direction의 paraphrase 부분을 지문에서 찾기. 밑줄 근처 문장에서 답 구성.

**⑤ derivation steps 표준 라벨 (문제 유형별 고정)**

> ⚠️ **라벨은 아래 표의 문자열을 그대로 사용한다. 자유 작성 금지.**
> 라벨이 제각각이면 기출마스터 시리즈 전체의 톤이 무너진다.

| step | 빈칸 기입형 | 밑줄 의미형 | Summary형 |
|------|------------|------------|----------|
| 1 | `범위 설정 — 발문 조건 확인` | `범위 설정 — 발문 조건 확인` | `범위 설정 — 발문 조건 확인` |
| 2 | `Commentary ↔ 지문 대응` | `밑줄 설명 도출 — [핵심어]` | `Topic ↔ Supporting ideas 추출 (Conclusion-first)` |
| 3 | `후보 소거 (passage-bound 위반 ✗)` | `후보 소거 (passage-bound 위반 ✗)` | `후보 소거 (일화·예시 제외)` |
| 4 | `확정 근거 ([content] + [form])` | `확정 근거 ([content] + [form])` | `확정 근거 ([topic] + [support] + [conclusion])` |
| 5 | `전략 메모 (출제 패턴 + 함정)` | `전략 메모 (출제 패턴 + 함정)` | `전략 메모 (출제 패턴 + 함정)` |

**step 내 본문 표기 약속:**
- step 3 후보 소거: 각 후보는 `- [단어]: ✗ (이유)` 또는 `- [단어]: ✓ (정답)` 형식
- step 4 확정 근거: 본문 내 `[content]` / `[form]` / `[topic]` / `[support]` / `[conclusion]` 태그로 근거 구분
- step 5 전략 메모: `출제 패턴 / 풀이 원칙:` 소제목 + `함정:` 소제목 2개 블록 구성

**translation 한국어 번역 기준 (자연스러운 한국어 필수)**

| ❌ 금지 패턴 | ✅ 올바른 표현 |
|------------|-------------|
| 영어 구조 직역 ("~하지 않을 수 없다", "~한 것은 ~이다") | 한국어 자연 어순으로 재구성 |
| 형용사+명사 직역 ("재앙스러운", "사춘기적") | "재앙 같은", "사춘기 특유의" |
| 피동 남발 ("볶아진다", "졸여진다", "만들어짐") | 능동형 ("볶는다", "조린다", "만든다") |
| 어색한 합성어 ("스토리텔링 기제", "소음 배출") | "스토리텔링 장치", "소음 발생" |
| 명사 남발 ("계절의 도래처럼", "여가 활동의 출구") | "계절처럼", "여가를 즐길 기회" |
| 오역 (sidewalk → "포도") | 정확한 의미 ("인도") |

→ **번역 후 소리 내어 읽었을 때 어색하면 다시 쓸 것.**
- `related.enabled`: false.

### 개념 정리(concept_explanation) 언어 규칙

- **영어학·교육론**: 영어 원문 먼저, 한국어 괄호 병기. 영어 용어 원어 사용.
- **일반영어**: 한국어 위주. 영어 인용은 지문 핵심 표현만.
- `definition_en`은 영어로, `definition_ko`는 한국어로. 혼용 금지.

---

## 참조 자료

### 폴더 구분

> **`refs/` MD 먼저 → 없거나 부족하면 `references/` PDF를 Read 툴로 직접 참조**

| 폴더 | 용도 | 접근 방식 |
|------|------|----------|
| `refs/` | MD 변환본 — Grep 검색 최적 | Grep + Read |
| `references/` | PDF 원본 — 그림·표 포함 | Read 툴로 직접 (Grep 불가) |

> 모두 **gitignored** — 로컬 전용. GitHub에 올라가지 않음.

---

### 영어학 refs (우선순위 순)

| 순위 | 파일 | 용도 |
|------|------|------|
| 1 | `refs/역대기출답안.md` | 2014–2023 강사+합격자 모범답안 전체 |
| 1 | `refs/2024 유희태 답안.md` / `refs/2024 조셉신 답안.md` | 2024 강사 답안 |
| 1 | `refs/2025 유희태 답안.md` | 2025 유희태팀 답안 |
| 1 | `refs/2025 전공영어 답안 및 해설_Ver.2.md` | 2025 권두걸팀 답안 (상세 해설) |
| 1 | `refs/2025 전공 기출 김재균해설.md` | 2025 김재균 답안 |
| 1 | `refs/2026 강사별 답안.md` | 2026 강사별 답안 (통합) |
| 1 | `refs/2026 기출 권두걸팀 해설서.md` | 2026 권두걸팀 답안 (상세 해설) |
| 1 | `refs/2026년 기출 조셉신팀 모범정답.md` | 2026 조셉신팀 답안 |
| 2 | `refs/밍우_영어학분석.md` | 밍우 영어학 기출 분석 |
| 2 | `refs/영어학 정리.md` | 영어학 단원별 개념 정리 |
| 2 | `refs/23. 음운론 기출 메타 분석(기출 확장, 기본 개념, 유의점 단원별).pdf.md` | 음운론 기출 메타 분석 |
| 3 | `refs/윤영어학.md` | 윤 영어학 참조서 |
| 3 | `refs/최진호 영어학 중급_OCR.md` | 최진호 영어학 중급 |
| 3 | `refs/An Introduction to Language 10th Edition1.md` | Fromkin et al. 교재 원전 |
| 3 | `refs/2025 최진호 영어학 Intermediate pp. 23~25.md` | 최진호 책 추론본 (비공식, 보조 참고) |
| 3★ | `refs/TG.md` | Radford, *Transformational Grammar* — 통사론 원전 |
| 3★ | `refs/단숲_TG 정리.md` | TG 단권화 정리본 |
| 3★ | `refs/syntax and argumentation 5th.md` | Syntax & Argumentation 원전 |
| 3★ | `refs/movement 단권화.md` | 이동 현상 단권화 |
| 3★ | `refs/Raising And Control .md` | Raising & Control 정리 |
| 3★ | `refs/20. EPP 정리(임용 포인트 정리).md` | EPP 임용 포인트 |

> ★ = 통사론(syntax) 문제 전용. `linguistics_domain: syntax`일 때 우선 참조.

---

### 영어교육론 refs (우선순위 순)

| 순위 | 파일 | 용도 |
|------|------|------|
| 1 | `refs/역대기출답안.md` | 2014–2023 강사+합격자 모범답안 전체 |
| 1 | `refs/2024 유희태 답안.md` / `refs/2024 조셉신 답안.md` | 2024 강사 답안 |
| 1 | `refs/2025 유희태 답안.md` | 2025 유희태팀 답안 |
| 1 | `refs/2025 전공영어 답안 및 해설_Ver.2.md` | 2025 권두걸팀 답안 (상세 해설) |
| 1 | `refs/2025 전공 기출 김재균해설.md` | 2025 김재균 답안 |
| 1 | `refs/2026 강사별 답안.md` | 2026 강사별 답안 (통합) |
| 1 | `refs/2026 기출 권두걸팀 해설서.md` | 2026 권두걸팀 답안 (상세 해설) |
| 1 | `refs/2026년 기출 조셉신팀 모범정답.md` | 2026 조셉신팀 답안 |
| 2 | `refs/밍우_영교론 영역별 기출분석본.md` | 밍우 영교론 영역별 기출 분석 |
| 2 | `refs/1. 정T_영교론 챕터별 단권화(한글 설명).md` | **정T 영교론 단권화** — 개념 정의 기준 |
| 2 | `refs/2. 정T_영교론 챕터별 키텀 맵핑(한글 설명).md` | **정T 키텀 맵핑** — 개념 계보·연결 |
| 2 | `refs/14. 영교론 헷갈리는 키텀 비교 정리(원서+기본서+글로서리+이티질문) 35p.md` | **정T 헷갈리는 키텀 비교** — 오개념 검증 필수 |
| 2 | `refs/5. 정T_TBP glossary 최종.md` | **정T TBP 글로서리** — Brown 원전 기준 |
| 2 | `refs/6. 정T_PLLT glossary 최종.md` | **정T PLLT 글로서리** — Brown·Atkinson 원전 기준 |
| 3 | `refs/subnote_all.md` | 영교론 서브노트 (Ch.1–13) — 개념·오개념 최우선 기준 |
| 3 | `refs/keywords.md` | 연도별 기출 키워드 + PLLT 출처 |
| 3 | `refs/mapping.md` | 교수법 개념 맵핑 (Behaviorism→Constructivism 계보) |
| 3 | `refs/영교론 기출 키워드 정리.md` | 기출 키워드 + 원전 출처 대조 |
| 4 | `refs/윤도형 영교론 핸드북.md` | 윤도형 영교론 핸드북 |
| 4 | `refs/TEACHING by PRINCIPLES.md` | Brown, *Teaching by Principles* 원전 |
| 4 | `refs/송은우 키텀 마스터 OCR2024.md` | 송은우 키워드 마스터 |
| 4 | `refs/트포 단권화.md` | 트포 단권화 |
| 4 | `refs/카니 서브노트pdf(루이스 합).md` | 카니 서브노트 |
| 4 | `refs/영교론 기출 키텀(루이스).md` | 루이스 기출 키텀 |
| 4 | `refs/메가쌤 전공영어 기출분석.md` | 메가쌤 전공영어 기출 분석 |

---

### 일반영어 refs (우선순위 순)

> ⚠️ 아래 도출과정 분석 파일들은 모두 **2022년 이하 문항만 수록**. 2023년 이후 문항은 강사 답안 MD 기반으로 작성.
> 접근 순서: MD 먼저 → 부족하면 동명 PDF(`references/❤️기출 일영문학 서술형 분석.pdf`, `references/밍우 일영문학 분석집.pdf`)를 Read 툴로 직접 확인.

| 순위 | 파일 | 용도 |
|------|------|------|
| 1 | `refs/역대기출답안.md` | 2014–2023 강사+합격자 모범답안 전체 |
| 1 | `refs/❤️기출 일영문학 서술형 분석.md` | 기출 일영 서술형 도출과정 핵심 기반 (2022 이하) — MD 우선 |
| 1 | `refs/밍우_일영문학분석집.md` | 밍우 일반영어·문학 도출과정 분석 (2022 이하) |
| 1 | `refs/2024 유희태 답안.md` / `refs/2024 조셉신 답안.md` | 2024 강사 답안 |
| 1 | `refs/2025 유희태 답안.md` | 2025 유희태팀 답안 |
| 1 | `refs/2025 전공영어 답안 및 해설_Ver.2.md` | 2025 권두걸팀 답안 (상세 해설) |
| 1 | `refs/2025 전공 기출 김재균해설.md` | 2025 김재균 답안 |
| 1 | `refs/2026 강사별 답안.md` | 2026 강사별 답안 (통합) |
| 1 | `refs/2026 기출 권두걸팀 해설서.md` | 2026 권두걸팀 답안 (상세 해설) |
| 1 | `refs/2026년 기출 조셉신팀 모범정답.md` | 2026 조셉신팀 답안 |
| 2 | `refs/4. 정T_루이스 기출 Chap.1-10 키텀.md` | **정T 루이스 기출 Ch.1–10 키워드** — 도출과정 기준 |
| 3 | `refs/메가쌤 전공영어 기출분석.md` | 메가쌤 전공영어 기출 분석 |
| 3 | `refs/루이스기출 5판.md` | 루이스 기출문제 5판 (2024 이전 문항만) |

---

### 활용 원칙

> ⚠️ **답안 검증은 무조건 1순위. 강사 답안 MD 확인 전에 JSON을 완성 처리하지 않는다.**

1. **강사 답안 최우선**: JSON 작성 시 가장 먼저 해당 연도 강사 답안 MD를 검색하여 `blank_answers` / `essay_content`를 확정한다.
   - 강사 전원 일치 → 그대로 채택.
   - 이견 있음 → 다수 의견 채택, 소수 의견 기재 안 함.
   - **강사 답안 MD에 없거나 불충분하면 → `references/` PDF를 Read 툴로 직접 확인.**
   - **강사 답안 MD + PDF 모두 확인 후에도 불명확하면 → 사용자에게 확인 요청. Claude 독자 판단으로 답안 작성 금지.**
2. **개념 대조 필수**: `subnote_all.md` 서술과 다른 정의는 Claude 독자 판단으로 덮어쓰기 금지.
3. **오개념 취약 항목**: Communicative Competence 계보, WCF 유형, Interaction/Noticing Hypothesis, Washback 등 — refs 대조 필수.
4. **합격자 서술 우선**: 원전 교재와 미세하게 다를 경우 합격자 서술 기준 (시험 채점 기준에 더 근접).
5. **재작성 원칙**: refs 내용은 직접 인용 금지 — 확인 후 JSON에 재작성하여 기재.
6. **순위 준수**: 1순위 확인 후 답안 없거나 개념 불명확할 때만 하위 순위 참조. 모든 파일 동시 로드 금지.

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

**자동 처리 원칙**: Claude는 사용자에게 별도 확인 받지 않고 작업 단위가 끝나면 **자동으로 commit → merge → push**까지 진행한다.

- **트리거**: 사용자가 "끝났다"·"완료"·"마무리"·"깃허브 작업"·"반영해" 등 마무리 의도를 보이면 즉시 실행. 사용자가 별도로 커밋/푸시 지시하지 않아도 실행.
- **순서**: feature 브랜치 작업 → `git add <해당 파일>` + commit → `git checkout main` → `git merge <branch> --no-edit` → `git push origin main`
- **커밋 단위**: 같은 주제(예: 2025·2026 일반영어 정비)는 하나의 커밋으로 묶음. 무관한 변경은 별도 커밋.
- **파일 선택**: `git add .` / `git add -A` 금지. 이번 작업에서 명시적으로 수정한 파일만 지정해서 add.
- **Windows worktree 주의**: filemode 변동(100755↔100644)이 노이즈로 잡히면 `git config core.fileMode false`로 해소.
- **커밋 메시지**: 한국어 제목 1줄 + 빈 줄 + 주요 변경 사항 bullet. 마지막에 `Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>` 포함.
- **충돌·오류 시**: 자동 진행 중단하고 사용자에게 보고. 강제 옵션(`--force`, `reset --hard`) 금지.
