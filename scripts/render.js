/* ═══════════════════════════════════════════════════
   전공영어 기출마스터 — render.js
   JSON → 카드 HTML 동적 렌더링
═══════════════════════════════════════════════════ */

const DATA_PATH = 'data/';

// ── 레이블 매핑 ──────────────────────────────────────

const SUBJECT_KO = {
  linguistics: '영어학',
  education:   '영어교육론',
  general:     '일반영어'
};

const DOMAIN_KO = {
  phonology:       '음운론',
  morphology:      '형태론',
  syntax:          '통사론',
  semantics:       '의미론',
  pragmatics:      '화용론',
  sociolinguistics:'사회언어학',
  acquisition:     '언어습득'
};

const CONN_CLASS = {
  same_concept:  'conn-same',
  same_strategy: 'conn-strat',
  same_text:     'conn-same',
  prerequisite:  'conn-prereq'
};

const SUBJECT_TAG_CLASS = {
  linguistics: 'tag-ling',
  education:   'tag-edu',
  general:     'tag-gen',
  literature:  'tag-lit'
};

function isLiterary(meta) {
  if (!meta.tags?.length) return false;
  const litTypes = ['novel', 'play', 'poem', 'poetry', 'drama', 'fiction', 'essay'];
  return litTypes.some(t => meta.tags.some(tag => tag.toLowerCase().includes(t)));
}

function getSubjectKo(meta) {
  if (meta.subject === 'general' && isLiterary(meta)) return '일반영어(문학)';
  return SUBJECT_KO[meta.subject] ?? meta.subject;
}

function getSubjectClass(meta) {
  if (meta.subject === 'general' && isLiterary(meta)) return 'tag-lit';
  return SUBJECT_TAG_CLASS[meta.subject] ?? 'tag-ling';
}

// ── HTML 유틸 ─────────────────────────────────────────

function esc(s) {
  return String(s ?? '')
    .replace(/&/g, '&amp;').replace(/</g, '&lt;')
    .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

// key_terms 배열로 텍스트 내 첫 등장 <em> 감싸기 (escape 포함)
function hlTerms(text, terms) {
  let s = esc(text).replace(/\n/g, '<br>');
  (terms ?? []).forEach(term => {
    const re = new RegExp(esc(term).replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), '');
    s = s.replace(re, `<em>${esc(term)}</em>`);
  });
  return s;
}

// HTML 텍스트 내 terms를 지정 클래스 span 또는 em으로 자동 감싸기
// 이미 해당 태그로 감싸진 경우 중복 적용 방지
function applyHl(text, terms, cls) {
  if (!text || !terms?.length) return text;
  let s = text;
  terms.forEach(term => {
    if (!term) return;
    const esc_term = term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    if (cls === 'em') {
      if (new RegExp(`<em>${esc_term}</em>`).test(s)) return;
      s = s.replace(new RegExp(esc_term), `<em>${term}</em>`);
    } else {
      if (new RegExp(`class="${cls}"[^>]*>${esc_term}`).test(s)) return;
      s = s.replace(new RegExp(esc_term, 'g'), `<span class="${cls}">${term}</span>`);
    }
  });
  return s;
}

// ── SVG 통사 트리 렌더러 ──────────────────────────────
// 노드 스키마: { label, children?, trace?, empty?, movement_target? }
// movement: root에 movements:[{from:"id", to:"id"}] 배열 (선택)

function renderSVGTree(root) {
  const FONT   = 13;
  const V_GAP  = 54;   // 행 간격
  const H_GAP  = 10;   // 형제 간 최소 간격
  const PAD    = 18;   // 캔버스 패딩
  const CH     = 8;    // 연결선 끝 여백

  // 라벨 폭 추정 (문자 수 기반)
  function labelW(lbl) { return Math.max(38, (lbl ?? '').length * 7.8 + 20); }

  // 서브트리 전체 폭
  function treeW(node) {
    if (!node.children?.length) return labelW(node.label);
    const sum = node.children.reduce((s, c) => s + treeW(c), 0)
              + H_GAP * (node.children.length - 1);
    return Math.max(labelW(node.label), sum);
  }

  // x,y 좌표 배정
  function layout(node, x, y) {
    const tw = treeW(node);
    node._x = x + tw / 2;
    node._y = y;
    if (node.children?.length) {
      let cx = x;
      node.children.forEach(c => {
        layout(c, cx, y + V_GAP);
        cx += treeW(c) + H_GAP;
      });
    }
  }

  // 모든 노드·엣지 수집
  function collect(node, lines, nodes) {
    (node.children ?? []).forEach(c => {
      lines.push([node._x, node._y + CH, c._x, c._y - CH]);
      collect(c, lines, nodes);
    });
    nodes.push(node);
  }

  layout(root, PAD, PAD + 4);
  const lines = [], nodes = [];
  collect(root, lines, nodes);

  const totalW = treeW(root) + PAD * 2;
  const maxY   = Math.max(...nodes.map(n => n._y));
  const totalH = maxY + 26;

  // movement 곡선 화살표 (선택적)
  const byLabel = {};
  nodes.forEach(n => { byLabel[n.id ?? n.label] = n; });
  const moveSVG = (root.movements ?? []).map(m => {
    const a = byLabel[m.from], b = byLabel[m.to];
    if (!a || !b) return '';
    const mx = (a._x + b._x) / 2;
    const cy1 = Math.min(a._y, b._y) - 30;
    return `<path d="M${a._x},${a._y + CH} Q${mx},${cy1} ${b._x},${b._y - CH}" fill="none" stroke="var(--accent4)" stroke-width="1.3" stroke-dasharray="4,3" marker-end="url(#arr)"/>`;
  }).join('');

  const linesSVG = lines.map(([x1,y1,x2,y2]) =>
    `<line x1="${x1.toFixed(1)}" y1="${y1.toFixed(1)}" x2="${x2.toFixed(1)}" y2="${y2.toFixed(1)}" stroke="var(--border2)" stroke-width="1.5"/>`
  ).join('');

  const nodesSVG = nodes.map(n => {
    const isLeaf = !n.children?.length;
    const color  = n.trace  ? 'var(--accent4)'
                 : n.empty  ? 'var(--text-dim)'
                 : isLeaf   ? 'var(--accent2)'
                 : 'var(--accent)';
    const fw = isLeaf ? '400' : '700';
    // 언더스코어를 SVG subscript으로: NP_i → NP<tspan>i</tspan>
    const parts = String(n.label ?? '').split('_');
    const labelSVG = parts[0] === ''
      ? ''
      : esc(parts[0]) + (parts.length > 1
          ? `<tspan dy="3" font-size="10">${esc(parts.slice(1).join('_'))}</tspan>`
          : '');
    return `<text x="${n._x.toFixed(1)}" y="${n._y.toFixed(1)}" text-anchor="middle" font-family="JetBrains Mono,monospace" font-size="${FONT}" font-weight="${fw}" fill="${color}">${labelSVG}</text>`;
  }).join('');

  const arrowDef = root.movements?.length
    ? `<defs><marker id="arr" markerWidth="6" markerHeight="6" refX="3" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="var(--accent4)"/></marker></defs>`
    : '';

  return `<div class="tree-wrap"><svg viewBox="0 0 ${Math.ceil(totalW)} ${Math.ceil(totalH)}" style="width:${Math.ceil(totalW)}px;max-width:100%;">${arrowDef}${linesSVG}${moveSVG}${nodesSVG}</svg></div>`;
}

function subBlanks(text) {
  return text
    .replace(/\[BLANK_①\]/g, '<span class="blank">①</span>')
    .replace(/\[BLANK_②\]/g, '<span class="blank">②</span>')
    .replace(/\[BLANK_③\]/g, '<span class="blank">③</span>')
    .replace(/\[BLANK\]/g, '<span class="blank">　　</span>')
    .replace(/_{5,}/g, '<span class="blank">　　</span>');
}

// ── 지문 렌더러 ──────────────────────────────────────

function renderPassage(text) {
  if (!text) return '';
  const chunks = text.split(/\n{2,}/);
  return chunks.map(renderChunk).filter(Boolean).join('');
}

function renderChunk(raw) {
  const chunk = raw.trim();
  if (!chunk) return '';

  // 섹션 레이블: <A> <B> <Commentary> 단독 줄
  if (/^<[^>\n]{1,20}>$/.test(chunk)) {
    const inner = chunk.slice(1, -1);
    return `<div class="prob-section-label">&lt;${esc(inner)}&gt;</div>`;
  }

  const lines = chunk.split('\n');
  const first = lines[0].trim();

  // 예문 블록 감지
  const isEgBlock =
    /^[\(（]?\d+[\)）\.]/.test(first) ||   // (1) 또는 1.
    /^[a-d][\.\)]/.test(first) ||           // a. b. c.
    /^[➊➋➌➍①②③④⑤]/.test(first) ||       // 원문자
    /^[A-Z]{2,}:/.test(first) ||            // 희곡 대사 HALIE:
    /^\[.+\]/.test(first);                  // 무대지시 [...]

  if (isEgBlock) {
    const inner = lines.map(l => subBlanks(esc(l.trim()))).join('<br>');
    return `<div class="eg-block">${inner}</div>`;
  }

  // 일반 단락
  const para = subBlanks(lines.map(l => l.trim()).join(' '));
  return `<p>${para}</p>`;
}

// ── 메타 태그 렌더러 ──────────────────────────────────

function renderMeta(meta) {
  const subjectKo = getSubjectKo(meta);
  const subjectClass = getSubjectClass(meta);
  const form = meta.number.startsWith('A') ? '전공A' : '전공B';
  const num  = meta.number.replace(/^[AB]-/, '');
  const isEssay = meta.question_type === 'essay';

  let domainTag = '';
  if (meta.subject === 'linguistics' && meta.linguistics_domain && DOMAIN_KO[meta.linguistics_domain]) {
    domainTag = `<span class="tag tag-sub">${DOMAIN_KO[meta.linguistics_domain]}</span>`;
  }

  // 소설/희곡/시 태그
  const literaryTypes = ['novel','play','poem','essay'];
  let literaryTag = '';
  if (meta.subject === 'general' && meta.tags) {
    const hasLit = literaryTypes.some(t =>
      meta.tags.some(tag => tag.toLowerCase().includes(t)) ||
      (meta.tags.includes('drama') || meta.tags.includes('poetry'))
    );
    if (hasLit) {
      const litLabel = meta.tags.includes('drama') || meta.tags.some(t => t.includes('play')) ? '희곡'
        : meta.tags.some(t => t.includes('poem') || t.includes('poetry')) ? '시'
        : '소설';
      literaryTag = `<span class="tag tag-novel">${litLabel}</span>`;
    }
  }

  const essayTag = isEssay ? `<span class="tag tag-essay">서술형</span>` : '';

  return `
    <div class="card-meta">
      <span class="tag tag-year">${meta.year}</span>
      <span class="tag ${subjectClass}">${subjectKo}</span>
      ${domainTag}
      ${literaryTag}
      <span class="tag tag-num">${form} · ${num}번</span>
      ${essayTag}
      <div class="score-badge"><span class="num">${meta.score}</span>점</div>
    </div>`;
}

// ── 도출과정 렌더러 ──────────────────────────────────

function renderDerivation(derivation, subject, keyTerms) {
  let html = '';

  // 스텝
  if (derivation.steps?.length) {
    html += `<div class="sec-title">풀이</div><div class="steps">`;
    // derivation.key_terms (이론 용어) → term-hl (보라, 별도 색상)
    const termWords = (derivation.key_terms ?? []).map(k => k.term).filter(Boolean);
    // 나머지 keyTerms (step.key_terms + answerWords) → em (주황)
    const emKeyTerms = (keyTerms ?? []).filter(t => !termWords.includes(t));

    derivation.steps.forEach(s => {
      const terms = (s.key_terms ?? [])
        .map(t => `<span class="kterm">${esc(t)}</span>`).join('');
      let explanation = (s.explanation ?? '').replace(/&/g, '&amp;').replace(/\n/g, '<br>');
      // 1. derivation.key_terms → term-hl (보라, 이론 용어)
      termWords.forEach(term => {
        const ep = term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        if (!new RegExp(`<em>${ep}</em>`).test(explanation) &&
            !new RegExp(`class="term-hl"[^>]*>${ep}`).test(explanation)) {
          explanation = explanation.replace(new RegExp(ep), `<span class="term-hl">${term}</span>`);
        }
      });
      // 2. step.key_terms + emKeyTerms → em (주황, 단계별 키워드)
      const stepEmTerms = [...new Set([...(s.key_terms ?? []), ...emKeyTerms])];
      stepEmTerms.forEach(term => {
        const ep = term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        if (!new RegExp(`<em>${ep}</em>`).test(explanation) &&
            !new RegExp(`class="term-hl"[^>]*>${ep}`).test(explanation)) {
          explanation = explanation.replace(new RegExp(ep), `<em>${term}</em>`);
        }
      });
      html += `
        <div class="step-item">
          <div class="step-num">${s.step}</div>
          <div class="step-body">
            <div class="step-label">${esc(s.label ?? '')}</div>
            <div class="step-text">${explanation}</div>
            ${s.tree ? renderSVGTree(s.tree) : ''}
            ${terms ? `<div class="kterms">${terms}</div>` : ''}
          </div>
        </div>`;
    });
    html += `</div>`;
  }

  // 어휘 테이블
  const vocab = derivation.vocabulary ?? [];
  if (vocab.length) {
    html += `
      <div class="sec-title">핵심 어휘</div>
      <table class="vocab-table">
        <thead><tr><th>단어</th><th>의미 &amp; 용례</th></tr></thead>
        <tbody>`;
    vocab.forEach(v => {
      const def = esc(v.definition_ko ?? v.meaning ?? '');
      const ex  = v.example ? `<div class="vex">${esc(v.example)}</div>` : '';
      html += `
          <tr>
            <td><div class="vword">${esc(v.word)}</div><div class="vpos">${esc(v.pos ?? '')}</div></td>
            <td><div class="vmean">${def}</div>${ex}</td>
          </tr>`;
    });
    html += `</div></table>`;
  }

  // 지문 해석 (일반영어만)
  if (subject === 'general' && derivation.translation) {
    let transText = derivation.translation;
    // 수동 trans-hl이 없으면 keyTerms로 자동 적용
    if (!transText.includes('trans-hl') && keyTerms?.length) {
      transText = applyHl(transText, keyTerms, 'trans-hl');
    }
    html += `<div class="sec-title">지문 해석</div><div class="trans-box">`;
    transText.split(/\n\n+/).forEach(para => {
      if (para.trim()) html += `<p>${para.trim()}</p>`;
    });
    html += `</div>`;
  }

  return html || '<p style="color:var(--text-dim);font-size:13px;">도출과정 준비 중입니다.</p>';
}

// ── 정답 렌더러 ───────────────────────────────────────

function renderAnswer(answer, subject, keyTerms) {
  const ma = answer.model_answer;
  let html = '';

  // 단답형: 빈칸 정답
  if (ma.blank_answers?.length) {
    const rows = ma.blank_answers.map(b =>
      `<div class="blank-row"><span class="bl">${esc(b.label)}</span><span class="ba">${esc(b.answer)}</span></div>`
    ).join('');
    html += `
      <div class="answer-box">
        <div class="answer-box-label">모범답안</div>
        <div class="blank-rows">${rows}</div>
      </div>`;
  }

  // 서술형: 모범답안 본문
  if (ma.essay_content) {
    html += `
      <div class="model-answer">
        <div class="model-answer-label">모범답안</div>
        <div class="ma-body">${hlTerms(ma.essay_content, keyTerms)}</div>
      </div>`;
  }

  // 채점 기준 — 서술형만 표시 (단답형은 blank_answers만)
  if (ma.scoring_criteria?.length && ma.essay_content) {
    const crits = ma.scoring_criteria.map(c =>
      `<div class="crit-line">
        <span class="crit-pts">${c.points}점</span>
        <span class="crit-text">${esc(c.criterion)}</span>
      </div>`
    ).join('');
    html += `
      <div class="criteria-box">
        <div class="criteria-box-label">채점 기준</div>
        <div class="crit-lines">${crits}</div>
      </div>`;
  }

  // 변형 답안 (서술형만)
  const variants = answer.variants ?? [];
  if (variants.length && ma.essay_content) {
    const vbClass = ['vb-a', 'vb-b', 'vb-c'];
    const vItems = variants.map((v, i) => `
      <div class="variant">
        <div class="v-head"><span class="vbadge ${vbClass[i] ?? 'vb-a'}">${esc(v.label)}</span></div>
        <div class="v-text">${hlTerms(v.content ?? '', keyTerms)}</div>
      </div>`).join('');
    html += `<div class="sec-title">변형 답안</div><div class="variants">${vItems}</div>`;
  }

  return html;
}

// ── 원전 렌더러 ───────────────────────────────────────

function renderSource(source, subject, keyTerms) {
  let html = `<hr class="source-divider"><div class="sec-title">원전</div>`;

  (source.references ?? []).forEach(ref => {
    const typeLabel = (ref.type ?? 'textbook').charAt(0).toUpperCase() + (ref.type ?? 'textbook').slice(1);
    // ref-hl: 수동 span 없으면 keyTerms로 자동 적용
    let excerptHtml = ref.excerpt ?? '';
    if (excerptHtml && !excerptHtml.includes('ref-hl') && keyTerms?.length) {
      excerptHtml = applyHl(excerptHtml, keyTerms, 'ref-hl');
    }
    const quote = excerptHtml ? `<div class="ref-quote">${excerptHtml}</div>` : '';
    html += `
      <div class="ref">
        <span class="ref-type">${esc(typeLabel)}</span>
        <div class="ref-title">${esc(ref.title ?? '')}</div>
        <div class="ref-author">${esc(ref.author ?? '')} (${ref.year ?? ''}) — ${esc(ref.publisher ?? '')}</div>
        ${ref.pages ? `<div class="ref-pages">${esc(ref.pages)}</div>` : ''}
        ${quote}
      </div>`;
  });

  if (source.concept_explanation) {
    html += `
      <div class="sec-title">개념 정리</div>
      <div class="concept">${hlTerms(source.concept_explanation, keyTerms)}</div>`;
  }

  return html;
}

// ── 연결문제 렌더러 ───────────────────────────────────

function renderRelated(related, subject) {
  if (subject === 'general') {
    return '<div class="no-related">일반영어는 연결문제를 제공하지 않습니다.</div>';
  }
  if (!related?.enabled) {
    return '<div class="related-notice">⚠ 데이터 구축 순서에 따라 순차적으로 추가됩니다.</div>';
  }
  const qs = related.questions ?? [];
  if (!qs.length) {
    return '<div class="related-notice">⚠ 데이터 구축 순서에 따라 순차적으로 추가됩니다.</div>';
  }

  return qs.map(q => {
    const form = q.number?.startsWith('A') ? '전공A' : '전공B';
    const num  = q.number?.replace(/^[AB]-/, '') ?? '';
    const connClass = CONN_CLASS[q.connection_type] ?? 'conn-same';
    const connLabel = q.connection_type?.replace('_', ' ') ?? '';
    const subjClass = SUBJECT_TAG_CLASS[q.subject] ?? 'tag-ling';
    const subjKo    = SUBJECT_KO[q.subject] ?? '';
    const kws = (q.shared_keywords ?? [])
      .map(k => `<span class="skw">${esc(k)}</span>`).join('');
    return `
      <div class="rel-card" data-target="${esc(q.id)}">
        <div class="rel-top">
          <span class="tag tag-year">${q.year}</span>
          <span class="tag ${subjClass}">${subjKo}</span>
          <span class="tag tag-num">${form} · ${num}번</span>
          <span class="conn ${connClass}">${connLabel}</span>
        </div>
        <div class="rel-note">${esc(q.connection_note ?? '')}</div>
        ${kws ? `<div class="skws">${kws}</div>` : ''}
      </div>`;
  }).join('');
}

// ── 카드 전체 렌더러 ──────────────────────────────────

function renderCard(data) {
  const { meta, problem, derivation, answer, source, related } = data;
  const cardId = `card-${meta.id}`;
  const uid    = meta.id; // 탭 ID prefix

  const passageHtml = renderPassage(problem.passage ?? '');
  // 모든 영역 하이라이트용 키워드: derivation.key_terms + 각 step.key_terms + blank_answers
  const answerWords = (answer?.model_answer?.blank_answers ?? []).map(b => b.answer).filter(Boolean);
  const allKeyTerms = [
    ...(derivation?.key_terms ?? []).map(k => k.term),
    ...(derivation?.steps ?? []).flatMap(s => s.key_terms ?? []),
    ...answerWords
  ].filter(Boolean);

  // 문제 탭
  const qTab = `
    <div class="tab-panel active" id="${uid}-q">
      <div class="prob-instruction"><strong>${esc(problem.instruction ?? '')}</strong></div>
      <div class="prob-passage">${passageHtml}</div>
    </div>`;

  // 도출과정 탭
  const dTab = `
    <div class="tab-panel" id="${uid}-d">
      ${renderDerivation(derivation ?? {}, meta.subject, allKeyTerms)}
    </div>`;

  // 정답 탭
  const aTab = `
    <div class="tab-panel" id="${uid}-a">
      ${renderAnswer(answer ?? {}, meta.subject, allKeyTerms)}
      ${renderSource(source ?? {}, meta.subject, allKeyTerms)}
    </div>`;

  // 연결문제 탭
  const rTab = `
    <div class="tab-panel" id="${uid}-r">
      ${renderRelated(related, meta.subject)}
    </div>`;

  return `
    <div class="card" id="${cardId}">
      ${renderMeta(meta)}
      <div class="tabs">
        <button class="tab-btn active" data-tab="q"       onclick="showTab(this,'${uid}-q')">문제</button>
        <button class="tab-btn"        data-tab="derive"  onclick="showTab(this,'${uid}-d')">도출과정</button>
        <button class="tab-btn"        data-tab="answer"  onclick="showTab(this,'${uid}-a')">정답</button>
        <button class="tab-btn"        data-tab="related" onclick="showTab(this,'${uid}-r')">연결문제</button>
      </div>
      ${qTab}${dTab}${aTab}${rTab}
    </div>`;
}

// ── 필터 시스템 ───────────────────────────────────────

let allCards = [];    // 전체 JSON 데이터
let filters  = { domain: 'all', year: 'all' };
let currentId = null; // 현재 표시 중인 카드 ID

function buildFilters() {
  // 연도 목록 자동 수집
  const years = [...new Set(allCards.map(d => String(d.meta.year)))].sort().reverse();
  const yearMenu = document.getElementById('year-menu');
  if (yearMenu) {
    const all = yearMenu.querySelector('[data-val="all"]');
    yearMenu.innerHTML = '';
    if (all) yearMenu.appendChild(all);
    years.forEach(y => {
      const btn = document.createElement('button');
      btn.className = 'dd-item';
      btn.dataset.val = y;
      btn.textContent = y;
      btn.onclick = () => selFilter('year', btn, y);
      yearMenu.appendChild(btn);
    });
  }
  rebuildProbMenu();
}

function rebuildProbMenu() {
  const filtered = allCards.filter(d => {
    let matchDomain;
    if (filters.domain === 'all') {
      matchDomain = true;
    } else if (filters.domain === 'literature') {
      matchDomain = d.meta.subject === 'general' && isLiterary(d.meta);
    } else if (filters.domain === 'general') {
      matchDomain = d.meta.subject === 'general' && !isLiterary(d.meta);
    } else {
      matchDomain = d.meta.subject === filters.domain;
    }
    const matchYear = filters.year === 'all' || String(d.meta.year) === filters.year;
    return matchDomain && matchYear;
  });

  const menu = document.getElementById('prob-menu');
  if (!menu) return;
  menu.innerHTML = '';

  if (!filtered.length) {
    menu.innerHTML = '<div class="dd-item" style="color:var(--text-dim);cursor:default;">해당 문제 없음</div>';
    document.getElementById('prob-label').textContent = '문제 없음';
    return;
  }

  // 번호 순 정렬: 전공A → 전공B, 숫자 오름차순, 같은 번호면 연도 최신순
  filtered.sort((a, b) => {
    const [fa, na] = (a.meta.number ?? '').split('-');
    const [fb, nb] = (b.meta.number ?? '').split('-');
    if (fa !== fb) return fa < fb ? -1 : 1;
    const nd = parseInt(na || 0) - parseInt(nb || 0);
    if (nd !== 0) return nd;
    return b.meta.year - a.meta.year;
  });

  filtered.forEach(d => {
    const subKo = getSubjectKo(d.meta);
    const domKo = d.meta.linguistics_domain ? ` · ${DOMAIN_KO[d.meta.linguistics_domain] ?? ''}` : '';
    const label = `${d.meta.year} ${d.meta.number} · ${subKo}${domKo}`;
    const btn = document.createElement('button');
    btn.className = 'dd-item' + (d.meta.id === currentId ? ' active' : '');
    btn.textContent = label;
    btn.onclick = () => pickCard(d.meta.id, label);
    menu.appendChild(btn);
  });

  // 현재 카드가 필터 결과에 없으면 첫 번째로
  if (!filtered.find(d => d.meta.id === currentId)) {
    const first = filtered[0];
    const subKo = getSubjectKo(first.meta);
    const domKo = first.meta.linguistics_domain ? ` · ${DOMAIN_KO[first.meta.linguistics_domain] ?? ''}` : '';
    pickCard(first.meta.id, `${first.meta.year} ${first.meta.number} · ${subKo}${domKo}`);
  }
}

function pickCard(id, label) {
  currentId = id;
  document.querySelectorAll('.card').forEach(c => c.classList.remove('active'));
  const card = document.getElementById(`card-${id}`);
  if (card) {
    card.classList.add('active');
    document.querySelector('.card-view').scrollTop = 0;
  }
  const probLabel = document.getElementById('prob-label');
  if (probLabel) probLabel.textContent = label ?? id;

  // 드롭다운 닫기 & active 표시
  document.querySelectorAll('#prob-menu .dd-item').forEach(btn => {
    btn.classList.toggle('active', btn.textContent === (label ?? id));
  });
  document.getElementById('prob-menu')?.classList.remove('open');
  document.getElementById('prob-select-btn')?.classList.remove('open');
}

function selFilter(type, item, label) {
  item.closest('.dropdown-menu').querySelectorAll('.dd-item').forEach(i => i.classList.remove('active'));
  item.classList.add('active');
  filters[type] = item.dataset.val;
  document.getElementById(type === 'domain' ? 'domain-label' : 'year-label').textContent = label;
  item.closest('.dropdown-menu').classList.remove('open');
  item.closest('.dropdown-wrap').querySelector('.dropdown-btn').classList.remove('open');
  rebuildProbMenu();
}

// ── 탭 전환 ───────────────────────────────────────────

function showTab(btn, id) {
  const card = btn.closest('.card');
  card.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  card.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
  btn.classList.add('active');
  document.getElementById(id)?.classList.add('active');
}

// ── 드롭다운 토글 ─────────────────────────────────────

function toggleDD(id, btn) {
  const isOpen = document.getElementById(id).classList.contains('open');
  document.querySelectorAll('.dropdown-menu').forEach(m => m.classList.remove('open'));
  document.querySelectorAll('.dropdown-btn').forEach(b => b.classList.remove('open'));
  if (!isOpen) {
    document.getElementById(id).classList.add('open');
    btn.classList.add('open');
  }
}

document.addEventListener('click', e => {
  if (!e.target.closest('.dropdown-wrap')) {
    document.querySelectorAll('.dropdown-menu').forEach(m => m.classList.remove('open'));
    document.querySelectorAll('.dropdown-btn').forEach(b => b.classList.remove('open'));
  }
});

// ── 초기화 ────────────────────────────────────────────

async function init() {
  try {
    const manifest = await fetch(DATA_PATH + 'manifest.json').then(r => r.json());

    const results = await Promise.allSettled(
      manifest.files.map(f => fetch(DATA_PATH + f).then(r => r.json()))
    );

    allCards = results
      .filter(r => r.status === 'fulfilled')
      .map(r => r.value);

    // 카드 HTML 삽입
    const view = document.getElementById('card-view');
    view.innerHTML = allCards.map(renderCard).join('');

    // 필터 구성 및 첫 카드 표시
    buildFilters();

  } catch (err) {
    console.error('render.js init error:', err);
    document.getElementById('card-view').innerHTML =
      '<p style="color:var(--accent4);padding:20px;">데이터를 불러올 수 없습니다. 서버에서 실행해 주세요.</p>';
  }
}

document.addEventListener('DOMContentLoaded', init);
