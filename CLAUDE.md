# 전공영어 기출마스터 — CLAUDE.md

## 설정

* **기본 모델:** claude-sonnet-4-6

## 프로젝트 개요

중등 영어 임용고시 기출문제 분석 웹사이트.
GitHub Pages 배포. 순수 HTML/CSS/JS (프레임워크 없음).

---

## 확정 설계

### 카드 탭 순서

문제 → 도출과정 → 정답 → 연결문제
(원전은 정답 탭 하단 구분선 아래 배치)

### 과목 분류

* `linguistics` — 영어학
* `general` — 일반영어 (문학 포함)
* `education` — 영어교육론

### 답안 규칙

* 단답형: 강사 공통 답 = 모범답안 (blank\_answers)
* 서술형: Claude 작성 모범답안 (간결한 문단, 점수 표시 없음)
* 채점기준: **서술형에만** 별도 회색 박스, 항목별 점수 — **단답형은 표시 안 함**
* 변형 답안(variants):
  - **단답형은 variants 비워둠** — 정답은 하나. 영어교육론·영어학·일반영어 모두 해당.
  - 강사·합격자 간 이견 시: **다수 의견을 모범답안**으로 채택. 소수 의견은 기재하지 않음.
  - 서술형에만 variants 작성. 강사/합격자 이름 없이 → 답안 A / 답안 B.
* 26년도 강사 답 없음 → variants 비워둠

**정답 탭 표시 규칙 (render.js 동작)**
- 단답형(`essay_content` 없음): `blank_answers` 박스만 표시. 채점기준·변형답안 모두 숨김.
- 서술형(`essay_content` 있음): 모범답안 → 채점기준 → 변형답안 순.

### 연결문제

* 영어학 ↔ 영어학만 연결
* 영어교육론 ↔ 영어교육론 연결 / 객관식 답안의 경우 키워드 연결될 수 있도록 링크
* 일반영어: 연결문제 없음
* 미등록 카드: 샘플 안내 표시

### 필터 UI

드롭다운 3개 한 줄: [영역 ▾] [연도 ▾] [문제 선택 ▾]

**문제 선택 드롭다운 정렬 순서**: 번호 순 (전공A → 전공B, 숫자 오름차순). 같은 번호면 연도 최신순.
영역 필터가 별도로 있으므로 과목별 그룹핑 불필요.

---

## 답안 작성 스타일 가이드

> 역대 강사(이동걸, 최진호, 유희태팀, 권영주, 최시원 등) 및 합격자 답안 분석 기반.
> JSON variants 작성 시 반드시 이 기준을 따른다.

### 공통 원칙

**단답형**
- 강사 공통 답 = 모범답안. 이견 없으면 그대로.
- 순서 지시(①②) 있으면 반드시 순서 지킴.
- 대소문자: 문제 요구 형태. 없으면 소문자 기본.

**서술형**
- 길이: 채점 기준 항목당 1–2문장. 총 3–5문장 표준.
- **분량 기준**: 모범답안 ≈ variants A 또는 B 각각과 동등 (40–60w). variants A+B 합산과 비슷하면 과다.
- 시작: `The [noun] is...` / `[Subject] [verb]s...` — "In this passage..." 금지.
- 증거: 지문 인용은 따옴표 + 핵심어만. 4단어 초과 연속 인용 금지.
- 결론 문장("In conclusion...") 불필요. 마지막 채점 포인트로 끝냄.
- **합격자 스타일** 기준: 짧고 명확하게. 강사처럼 길게 쓰지 않는다.
- **답이 최우선 (top priority)**: 신뢰도·정확도가 핵심. 채점 기준을 모두 커버하되 과잉 서술 금지.

### 영어학

**음운론**
```
[Feature/Process] applies when [environment].
In ([data]), [specific evidence] shows that [conclusion].
```
- 답 먼저, 설명 나중.
- 환경은 feature notation으로: `[+coronal, −anterior]`

**통사론**
```
Sentence (X) is [grammatical/ungrammatical].
[Violation name] is violated because [technical explanation].
```
- violation 이름 명시 (NCB, Subjacency 등).
- 정문/비문 판단 먼저, 이유 나중.

**형태론**
```
The [suffix/process] attaches to [condition].
[Example] demonstrates that [generalization].
```
- 조건은 phonological feature로 표현.
- attested / unattested 대비 구조.

### 영어교육론

**두 항목 비교/식별**
```
[Item A] [does/shows] [X] in that [evidence].
[Item B] [does/shows] [Y] since [evidence].
```
- 각 항목 1문장씩. 병렬 구조 유지.
- `in that` / `since` / `by -ing`으로 근거 연결.
- 지문 속 교사 행동을 기술. 평가하지 않음.

**제안/비판**
```
[Step X] does not correspond to [suggestion Y].
Instead of [correct approach], the teacher [incorrect approach].
```
- 어느 step이 어느 suggestion과 불일치인지 명확히.
- 교사 행동 기술 시 지문 근거 필수.

### 일반영어

**빈칸**
- 지문에서 직접 찾을 수 있는 단어. 품사/형태 일치 필수.

**밑줄 의미 설명**
```
The underlined part means that [paraphrase in context].
[Subject] [explanation of why/how].
```
- 직접 번역 금지 — 맥락 속 의미로 풀어쓰기.
- 2–3문장 이내.

**요약/논술**
```
[Topic sentence].
First, [support 1 with example].
Second, [support 2 with example].
[Implication — not a repeat of TS].
```
- 지문 내용만. 외부 지식 추가 금지.

### 감점 패턴 (하지 말 것)

| 패턴 | 이유 |
|------|------|
| "In this passage, ..." 로 시작 | 불필요한 도입 |
| 4단어 이상 연속 인용 | 채점 기준 위반 |
| ①② 순서 바꾸기 | 지시 위반 |
| 추측성 표현 ("might be...") | 확신 있게 서술 |
| "In conclusion, ..." | 서술형에서 불필요 |
| 과도한 부연 | 채점 기준 초과 서술 |
| 영어교육론 개념 오개념 삽입 | 오답 유도 위험 — 반드시 원전 정의 기준으로 작성 |

**영어교육론 핵심 오개념 주의 목록**

| 개념 | 잘못된 표현 (금지) | 올바른 표현 |
|------|------------------|-----------|
| Reformulation | "언어적 정확성·적절성 개선" | "어휘·문법·문체를 원어민답게(native-like) 바꾸어 전체를 다시 작성" (Ellis, 2008) |
| Reformulation | "내용·조직 유지" | "학습자의 의미(meaning)를 최대한 유지" — 조직 변경 가능 |
| Pragmatic competence | source: Canale & Swain (1980) | Canale & Swain (1980)은 Sociolinguistic Competence; Pragmatic competence 독립 개념은 Bachman (1990) |

### variants 작성 기준

```
model_answer  → 채점 기준 모두 포함한 완전한 답안 (합격자 스타일)
variants[A]   → 문장 구조 변형 (동일 내용, 다른 표현)
variants[B]   → 증거 제시 방식 변형 (같은 포인트, 다른 근거 문장)
```
- variants는 model_answer 내용을 벗어나지 않는다.
- 저작권 있는 강사/합격자 문장 그대로 사용 금지 — 반드시 재작성.
- **단답형은 variants 작성하지 않음** (서술형 전용).

### 개념 정리(concept_explanation) 언어 규칙

**영어학·영어교육론**
- 영어 원문 먼저, 한국어는 괄호 또는 들여쓰기로 아래에 병기.
- 영어 용어는 원어 그대로 사용. 한국어 번역은 이해 보조용.
- 예:
  ```
  One-way entailment: p ⇒ q, but q ⇏ p.
    (한 방향만 참 보존)
  ```

**일반영어**
- 한국어 위주. 영어 인용은 지문 핵심 표현만.

---

## HTML 미리보기 디자인 규칙

> `preview_*.html` 파일 작성 시 반드시 따를 것. `giulmmaster_v4.html` 디자인 기준.

### CSS 클래스 — 하이라이트

| 클래스 | 색상 | 용도 |
|--------|------|------|
| `trans-hl` | `--accent2` (teal) | 지문 한국어 해석 내 핵심 표현 강조 |
| `ref-hl` | `--accent` (blue/purple) | 원전 인용문(ref-quote) 내 핵심 키워드 강조 |
| `step-text em` | `--accent3` (orange) | 도출과정 스텝 내 핵심 용어 강조 |

### 도출과정 step-text 하이라이트 규칙

- render.js는 **`allKeyTerms`** (= `derivation.key_terms[].term` + 각 `step.key_terms[]` + `blank_answers[].answer`) 를 수집해 **모든 step** explanation에 orange `<em>` 자동 적용.
- 각 step 자신의 `key_terms`가 우선, 이후 `allKeyTerms` 전체 순으로 첫 등장에 감쌈. 중복 적용 방지.
- `<em>` 태그는 CSS `.step-text em { color: var(--accent3); font-style: normal; font-weight: 600; }` 으로 orange 강조됨.
- JSON에서 직접 `<em>` 태그를 삽입해도 되고, `key_terms`에만 등록해도 자동 적용됨.
- `key_terms`는 반드시 `explanation` 본문에 **그대로** 등장하는 단어/구로만 등록할 것 (자동 치환 매칭 필요).
- 예:
  ```json
  "explanation": "Principle 5 for Material 1은 화용 기술 연습에 해당한다.",
  "key_terms": ["Principle 5 for Material 1"]
  ```
  → render.js가 `<em>Principle 5 for Material 1</em>` 으로 감쌈.

### 원전(ref-quote) 키워드 하이라이트 규칙

- 원전 인용문 내 **이 문제의 정답 근거가 되는 개념어**에 `ref-hl` 적용.
- 과도하게 많이 적용하지 말 것 — 인용문당 2~4개 키워드.
- CSS: `.ref-hl { color: var(--accent); font-style: normal; font-weight: 600; }`
- **render.js 자동 적용**: JSON `excerpt` 필드에 수동 `ref-hl` span이 없으면, `allKeyTerms`로 자동 적용 (fallback). 수동 span이 있으면 그대로 사용.
- 예:
  ```html
  <div class="ref-quote">"<span class="ref-hl">One-way entailment</span> holds where
  the inference goes <span class="ref-hl">only from p to q but not from q to p</span>."</div>
  ```

### 지문 해석(trans-box) 규칙

- 일반영어만 작성. 영어학·교육론은 빈 문자열.
- **전문 해석 필수** — 요약본 금지. 원문 단락 구조 그대로 유지.
- **`trans-hl` 적용 필수** — 정답 근거가 되는 문장·표현에 반드시 표시:
  - 단답형: 빈칸 정답의 직접 근거가 되는 문장 (정의·대조·환언 포함)
  - 논술형: 채점 포인트별 핵심 근거 문장 (주제문, 핵심 예시, 결론)
  - 서사·문학: 역할 전환·주제 전환·밑줄 의미 근거 표현
- 단락당 1–3개 문장 수준. 과도 적용 금지.
- **render.js 자동 적용**: JSON `translation` 필드에 수동 `trans-hl` span이 없으면, `allKeyTerms`로 자동 적용 (fallback). 수동 span이 있으면 그대로 사용.
- 예:
  ```html
  <span class="trans-hl">우리는 삶을 거꾸로 살아가고 있었고</span>
  ```

### 통사 트리 (SVG) 규칙

- **대상**: `linguistics_domain: syntax` 문제에서 트리 구조 설명이 필요할 때
- **위치**: `derivation.steps[n].tree` 필드에 JSON으로 정의 → render.js가 자동으로 SVG 렌더링
- **노드 스키마**:
  ```json
  {
    "label": "CP",          // 노드 라벨. 언더스코어로 subscript: "NP_i" → NP<sub>i</sub>
    "children": [...],      // 자식 배열. 빈 배열 또는 생략 = 리프(단말) 노드
    "trace": true,          // 흔적(trace) 노드 → 분홍색 (--accent4)
    "empty": true           // 공범주(PRO, pro 등) → 회색 (--text-dim)
  }
  ```
- **색상**: 비단말 노드 = 보라(`--accent`), 단말 = 민트(`--accent2`), trace = 분홍(`--accent4`), 공범주 = 회색(`--text-dim`)
- **이동 화살표** (선택): root에 `"movements": [{"from": "label_id", "to": "label_id"}]` 추가 → 점선 곡선 화살표
- **주의**: 트리가 필요 없는 step에는 `tree` 필드 생략 (선택 필드)
- 예:
  ```json
  "tree": {
    "label": "CP",
    "children": [
      { "label": "who_i", "children": [] },
      { "label": "C'", "children": [
        { "label": "C", "children": [{ "label": "that", "children": [] }] },
        { "label": "TP", "children": [
          { "label": "t_i", "trace": true, "children": [] },
          { "label": "T'", "children": [{ "label": "would come", "children": [] }] }
        ]}
      ]}
    ]
  }
  ```

### 탭별 렌더링 원칙

- **문제 탭**: instruction 박스 + passage (빈칸 `.blank` 스팬, 예문 `.eg-block`, 섹션 레이블 `.prob-section-label`)
- **도출과정 탭**: 5단계 steps + vocabulary 테이블(있을 때) + 지문 해석(일반영어만)
- **정답 탭**:
  - 단답형: 모범답안(`blank_answers`) **만** → 구분선 → 원전 → 개념정리
  - 서술형: 모범답안 → 채점기준 → 변형답안 → 구분선 → 원전 → 개념정리
- **연결문제 탭**: `related.enabled: false` 또는 `subject: general`이면 탭 숨김 또는 안내 문구

### 과목별 태그 색상

| 과목 | 클래스 | 색상 |
|------|--------|------|
| 영어학 | `tag-ling` | 보라 (`#a897f5`) |
| 영어교육론 | `tag-edu` | 연초록 (`#b8d070`) |
| 일반영어 | `tag-gen` | 초록 (`#a8d070`) |
| 소설/희곡/시 | `tag-novel` | 연보라 (`#d097f5`) |

---

## 목표 파일 구조

```
giulmmaster/
├── CLAUDE.md
├── index.html          ← 메인 (필터 + 카드 뷰)
├── data/
│   ├── linguistics_2026_B01.json
│   ├── linguistics_2026_A09.json
│   ├── general_2026_A11.json
│   └── ...
└── scripts/
    ├── render.js       ← JSON → HTML 카드 렌더링
    └── filter.js       ← 필터 로직
```

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
    "tags": ["inflectional suffix", "derivational suffix"],
    "parse_source": "파싱된 PDF 파일명",
    "parse_confidence": "high",
    "verified": false
  },
  "problem": {
    "instruction": "Fill in each of the blanks ① and ② with the ONE most appropriate word.",
    "passage": "지문 전체 텍스트...",
    "blanks": [
      { "label": "①", "context": "grammatical ___ of the stem" },
      { "label": "②", "context": "the ___ of an inflectional suffix is predictable" }
    ]
  },
  "derivation": {
    "step1_scope": {
      "read_first": "commentary | direction | blank_context | underlined",
      "predicted_direction": "빈칸에 들어갈 방향 예측 — 긍정/부정, 품사, 의미 범위",
      "key_constraint": [
        "형태 제약 예: 관사 없음 → 복수 또는 추상명사",
        "전치사 of 뒤 → 명사형",
        "조동사 뒤 → 동사원형"
      ]
    },
    "step2_parallel": {
      "pairs": [
        {
          "text_a": "지문 측 표현",
          "text_b": "commentary 또는 발문 측 대응 표현",
          "color": "yellow | green | blue | gray",
          "relation": "synonym | paraphrase | antonym | structural"
        }
      ],
      "blank_target_pair": "빈칸이 속한 대응쌍 color 또는 text_a"
    },
    "step3_candidates": {
      "candidates": [
        {
          "word": "후보 단어",
          "eliminated": true,
          "elimination_reason": "탈락 이유 설명",
          "elimination_type": "pos | number | collocation | meaning | too_general | not_in_text"
        },
        {
          "word": "최종 정답 후보",
          "eliminated": false
        }
      ]
    },
    "step4_evidence": {
      "final_answer_word": "최종 정답",
      "evidence": [
        {
          "type": "content | form | collocation | parallel | context_flow",
          "description": "근거 설명 — 지문 인용 포함",
          "supporting_text": "근거가 되는 지문 원문 (해당 시)"
        }
      ]
    },
    "step5_strategy": {
      "strategy_type": "기입형 | 서술형_밑줄 | 서술형_summary | 공통",
      "principles": [
        "이 문제에서 추출한 일반화 가능한 풀이 원칙"
      ],
      "pitfalls": [
        "함정 또는 자주 틀리는 포인트"
      ],
      "related_exams": ["유사 전략 적용 기출 id"]
    },
    "key_terms": [
      {
        "term": "Noticing Hypothesis",
        "definition_en": "학습자가 의식적으로 주목한 언어 형식만 습득됨",
        "definition_ko": "Schmidt (1990) 제안. intake는 conscious attention 필요.",
        "source_author": "Schmidt",
        "source_year": 1990,
        "related_terms": ["intake", "implicit learning"],
        "exam_usage": "지문에서 어떤 맥락으로 출제됐는지"
      }
    ],
    "vocabulary": [
      { "word": "단어", "pos": "n/v/adj", "definition_ko": "뜻", "example": "예문 (선택)" }
    ],
    "translation": "일반영어·문학 전용 지문 해석. 영어학·교육론은 빈 문자열."
  },
  "answer": {
    "model_answer": {
      "blank_answers": [
        { "label": "①", "answer": "category" },
        { "label": "②", "answer": "meaning" }
      ],
      "essay_content": "서술형 모범답안 전문. 단답형은 빈 문자열.",
      "scoring_criteria": [
        { "criterion": "① category", "points": 1 },
        { "criterion": "② meaning", "points": 1 }
      ]
    },
    "variants": [
      {
        "source_type": "instructor | passer",
        "label": "답안 A",
        "content": "재작성된 변형 답안"
      },
      {
        "source_type": "instructor | passer",
        "label": "답안 B",
        "content": "재작성된 변형 답안"
      }
    ]
  },
  "source": {
    "references": [
      {
        "type": "textbook | paper | novel | poem | play | essay",
        "author": "Fromkin, Rodman & Hyams",
        "title": "An Introduction to Language (11th ed.)",
        "year": 2018,
        "publisher": "Cengage Learning",
        "pages": "pp. 64-72",
        "excerpt": "원전 핵심 발췌문 (선택)"
      }
    ],
    "concept_explanation": "개념 보충 설명. Wikipedia 지양 — 논문/교재 기준."
  },
  "related": {
    "enabled": true,
    "questions": [
      {
        "id": "linguistics_2022_A03",
        "year": 2022,
        "number": "A-3",
        "subject": "linguistics",
        "connection_type": "same_concept | same_strategy | same_text",
        "connection_note": "연결 이유 설명",
        "shared_keywords": ["ordering constraint", "derivational morpheme"]
      }
    ]
  }
}
```

### 과목별 derivation 작성 규칙

> **중요**: 각 과목은 서로 다른 풀이 논리를 사용한다. 과목 간 방식 혼용 금지.
> 특히 영어학·영어교육론에 일반영어 방식(commentary 대응, passage-bound 검색)을 적용하지 말 것.

**영어학 (linguistics)**
- 핵심 논리: 언어학 이론 개념 식별 → 지문 데이터에 적용 → 이론 귀속
- `step1_scope`: 발문·빈칸 조건 확인. 어떤 linguistics_domain인지 먼저 파악.
- `step2_parallel`: 지문 표현 ↔ 이론 정의 대응 (이론 용어가 지문 기술과 어떻게 대응되는지)
- `step3_candidates`: 이론 귀속 범위·개념 정의로 후보 소거
- `step4_evidence`: 지문 데이터(예문, 규칙 등)를 근거로 최종 정답 확정
- `step5_strategy`: 해당 linguistics_domain 풀이 원칙 일반화
- `key_terms`: 반드시 작성. `source_author` + `source_year` 필수
- `translation`: 빈 문자열
- `linguistics_domain` 필수: `phonology | morphology | syntax | semantics | pragmatics | sociolinguistics | acquisition`

**영어교육론 (education)**
- 핵심 논리: 지문 속 교사·학습자 행동 식별 → 교수법/이론 정의와 매핑 → 소거
- `step1_scope`: 발문 조건 확인. 어떤 교수법/이론 영역인지 먼저 파악.
- `step2_parallel`: 지문 교사·학습자 행동 ↔ 이론/교수법 정의 대응
- `step3_candidates`: 교수법 정의 범위로 후보 소거 (일반영어처럼 passage-bound 단어 검색 아님)
- `step4_evidence`: 지문 속 구체적 행동·표현을 근거로 정답 확정
- `step5_strategy`: 해당 교수법 식별 원칙 일반화
- `key_terms`: 반드시 작성. 교수법/가설 이론가 명시
- `translation`: 빈 문자열

**일반영어·문학 (general)**
- 핵심 논리: 지문 ↔ commentary/발문 대응 → passage-bound 단어 검색
- `step2_parallel`: 지문 표현 ↔ commentary 또는 발문 대응
- `step3_candidates`: 지문에 실제 등장한 단어인지 확인 (passage-bound 규칙)
- `key_terms`: 빈 배열
- `translation`: 지문 **전문** 한국어 해석 작성. 요약본 금지. 핵심 표현은 trans-hl로 강조.
- `related.enabled`: false (연결문제 없음)

---

## Claude Code 할 일 (순서대로)

### Step 1 — 폴더 세팅

```bash
mkdir -p giulmmaster/{data,scripts}
cd giulmmaster
git init
```

`giulmmaster_v4.html`을 `index.html`로 복사해서 디자인 기준으로 사용.

### Step 2 — PDF 파싱 스크립트

```bash
pip install pdfplumber pymupdf
```

`scripts/parse_pdf.py` 작성:
* 입력: 기출 PDF 경로
* 텍스트 추출 → JSON 스켈레톤 자동 생성
* `parse_confidence` 자동 판정: 텍스트 추출 완전하면 `high`, 표/수식 포함 시 `med`, 이미지만 있으면 `low`
* 이미지(수형도 등) 감지 시 PNG 저장 → `images/` 폴더
* 출력: `data/{id}_draft.json` (수동 보완 필요한 초안)

### Step 3 — JSON → 카드 렌더러

`scripts/render.js` 작성:
* `data/*.json` 읽어서 카드 HTML 동적 생성
* `question_type` 분기: `short_answer` vs `essay`
* `subject: general` → 연결문제 탭 숨김
* `derivation` 5단계를 순서대로 렌더링:
  - step1: 범위 설정 박스
  - step2: 대응쌍 색상 하이라이트 테이블
  - step3: 후보 단어 카드 (탈락=취소선, 정답=강조)
  - step4: 확정 근거 리스트
  - step5: 전략 메모 박스
* `giulmmaster_v4.html` 디자인 그대로 유지

### Step 4 — index.html 동적화

* 하드코딩된 카드 3개 → render.js 기반 동적 렌더링으로 교체
* `data/` JSON 목록 읽어 필터 드롭다운 자동 구성

### Step 5 — GitHub Pages 배포

```bash
git add .
git commit -m "init: 기출마스터 v1"
git remote add origin https://github.com/namkicheol/giulmmaster.git
git push -u origin main
```

GitHub → Settings → Pages → Source: main branch / root

---

## 현재 데이터 현황 (2026-04-16 기준)

### data/ 폴더 — 총 341개 draft JSON

| 과목 | draft 수 | 비고 |
|-|-|-|
| `education` (영어교육론) | 119 | |
| `general` (일반영어) | 124 | |
| `linguistics` (영어학) | 98 | |

### 완성본 작업 계획

* **2026년도 23개**: claude.ai에서 완성본 작성 후 draft 교체 예정
* **다른 연도**: 완성본 작성 시 **2026년도 JSON 파일 구조를 기준으로 참조**

### 기존 기준 파일

| 파일 | 설명 |
|-|-|
| `giulmmaster_v4.html` | 디자인 기준 파일 (3문제 하드코딩) |
| `question_schema.json` | JSON 스키마 전체 정의 |
| `linguistics_2026_B01.json` | 전공B 1번 샘플 JSON (완성본 구조 기준) |

---

## 개념 정리 참조 우선순위

1. **서브노트 kimmie** — 영어교육론·영어학 개념 정리 1순위 참조. 시험 출제 맥락에 맞는 정의와 예시 기준.
2. 교재/논문 원전 (Ellis, Richards, Fromkin, Carnie 등)
3. Wikipedia 사용 금지

**용어 표기 원칙** (영어교육학·영어학):
- 개념 용어는 **원어(영어) 우선** 표기. 한국어 번역은 필요한 경우만 괄호로 병기/ 작성 지양.
- 예: Reformulation (재구성), Communicative Competence (의사소통 능력), That-trace Effect (that-흔적 효과)
- JSON `definition_en`은 영어로, `definition_ko`는 한국어로 작성. 혼용 금지.

## Git 워크플로우

- 작업은 feature 브랜치에서 진행 후, **Claude가 직접 main으로 merge + push**까지 처리.
- 사용자가 별도로 GitHub에서 merge할 필요 없음.
- 순서: feature 브랜치 커밋 → `git checkout main` → `git merge <branch>` → `git push origin main`

---

## 주의

* 원전: Wikipedia 지양, 서브노트 kimmie → 논문/교재 순
* 강사/합격자 실명 금지
* 모범답안 문단에 점수 표시 금지
* 채점기준은 서술형에만 별도 박스 — 단답형은 채점기준 표시 안 함
* 역대 강사/합격자 답안 그대로 사용 금지 — 반드시 재작성
* `parse_confidence: low` 파일은 반드시 수동 검토 후 `verified: true` 처리
* 서술형 모범답안 분량이 variants A+B 합산과 비슷하면 과다 — 반드시 압축
