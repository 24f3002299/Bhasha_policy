/* ─────────────────────────────────────────
   BHASHAPOLICY — script.js
   ───────────────────────────────────────── */

/* ══════════════════════════════════════════
   1. HAMBURGER / MOBILE NAV
   ══════════════════════════════════════════ */
(function () {
  const hamburger = document.getElementById('hamburger');
  const mobileNav = document.getElementById('mobileNav');

  if (!hamburger || !mobileNav) return;

  hamburger.addEventListener('click', () => {
    const isOpen = mobileNav.classList.toggle('open');
    hamburger.setAttribute('aria-expanded', isOpen);
  });

  mobileNav.querySelectorAll('.mobile-nav-link').forEach(link => {
    link.addEventListener('click', () => {
      mobileNav.classList.remove('open');
      hamburger.setAttribute('aria-expanded', 'false');
    });
  });
})();


/* ══════════════════════════════════════════
   2-4. POLICY ANALYSIS — FRONTEND
   Upload → send to backend → render dynamic
   policy name, chat, summary, evidence cards,
   and a 2-policy comparison table.

   ───────────────────────────────────────────
   BACKEND CONTRACT (give this to your friend)
   ───────────────────────────────────────────
   Request:  POST BACKEND_CONFIG.endpoint
             Content-Type: multipart/form-data
             field "file" = the uploaded PDF

   Response: 200 OK, JSON body shaped exactly like:
   {
     "policyName": "Star Health — Family Floater",
     "insurer": "Star Health",
     "policyType": "Health" | "Term Life" | "Motor" | "Other",
     "pageCount": 14,
     "premium": "₹12,400/yr",
     "sumInsured": "₹5,00,000",
     "summary": "2-4 plain-language sentences a non-expert can understand.",
     "chatIntro": "Hi! I've read your ... policy. Ask me anything.",
     "evidenceCards": [
       { "type": "covered"|"excluded"|"limit"|"condition",
         "title": "Daycare procedures",
         "text": "...",
         "clause": "Clause 3.4",
         "page": 6 }
       // 5–8 items, mixing all four types where possible
     ],
     "compareMetrics": {
       "Annual premium": "₹12,400", "Sum insured": "₹5,00,000",
       "Room rent limit": "1% / day", "Daycare procedures": "541 procedures",
       "No-claim bonus": "10% / yr", "Maternity cover": "Yes",
       "Pre-existing wait": "3 years", "Cashless hospitals": "14,000+"
     }
   }
   Any field can be omitted — the frontend fills in sensible fallbacks.
   ══════════════════════════════════════════ */
(function () {

  /* ---------- 0. CONFIG ----------
     Point this at your friend's real endpoint once it's live.
     Until then, every upload silently falls back to realistic demo
     data so you can preview and demo the full design right now.
  ------------------------------------------------- */
  const BACKEND_CONFIG = {
    endpoint: '/api/analyze-policy', // <-- replace with the real backend URL
  };

  /* ---------- state ---------- */
  const state = { policies: [], activeIndex: 0 };

  /* ---------- DOM refs ---------- */
  const dropZone     = document.getElementById('dropZone');
  const fileInput    = document.getElementById('fileInput');
  const browseBtn    = document.getElementById('browseBtn');
  const fileNameEl   = document.getElementById('fileName');
  const analyzeBtn   = document.getElementById('analyzeBtn');
  const apiStatusMsg = document.getElementById('apiStatusMsg');

  const docCardList   = document.getElementById('docCardList');
  const chatDocName   = document.getElementById('chatDocName');
  const chatMessages  = document.getElementById('chatMessages');
  const chatInput     = document.getElementById('chatInput');
  const sendBtn       = document.getElementById('sendBtn');
  const quickChips    = document.getElementById('quickChips');

  const summaryCard  = document.getElementById('summaryCard');
  const summaryBadge = document.getElementById('summaryBadge');
  const summaryTitle = document.getElementById('summaryTitle');
  const summaryMeta  = document.getElementById('summaryMeta');
  const summaryText  = document.getElementById('summaryText');
  const summaryStats = document.getElementById('summaryStats');

  const evGrid       = document.getElementById('evGrid');
  const evFilterWrap = document.querySelector('.ev-filters');

  const compareTheadRow = document.getElementById('compareTheadRow');
  const compareTbody    = document.getElementById('compareTbody');
  const compareSub      = document.getElementById('compareSub');

  if (!dropZone || !fileInput) return;

  const MAX_FILES = 2;
  let selectedFiles = [];

  /* ---------- upload / drop-zone ---------- */
  browseBtn && browseBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    fileInput.click();
  });

  dropZone.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      fileInput.click();
    }
  });

  dropZone.addEventListener('click', () => fileInput.click());

  fileInput.addEventListener('change', () => {
    const picked = Array.from(fileInput.files).filter(f => f.type === 'application/pdf');
    if (!picked.length) {
      showFileMsg('⚠ Only PDF files are supported.', true);
      return;
    }
    const truncated = fileInput.files.length > MAX_FILES;
    setFiles(picked.slice(0, MAX_FILES), truncated);
  });

  dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('drag-over');
  });

  dropZone.addEventListener('dragleave', (e) => {
    if (!dropZone.contains(e.relatedTarget)) {
      dropZone.classList.remove('drag-over');
    }
  });

  dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('drag-over');
    const dropped = Array.from(e.dataTransfer.files);
    const pdfs = dropped.filter(f => f.type === 'application/pdf');

    if (!pdfs.length) {
      showFileMsg('⚠ Only PDF files are supported.', true);
      return;
    }
    const truncated = dropped.length > MAX_FILES;
    setFiles(pdfs.slice(0, MAX_FILES), truncated);
  });

  function setFiles(files, truncated) {
    selectedFiles = files;

    // Keep the real <input> in sync so it works the same whether files
    // came from drag-drop or the browse button.
    const dt = new DataTransfer();
    files.forEach(f => dt.items.add(f));
    fileInput.files = dt.files;

    if (truncated) {
      showFileMsg('⚠ Up to 2 PDFs at a time — using: ' + files.map(f => f.name).join(', '), true);
    } else {
      const label = files.length === 1
        ? '✓ ' + files[0].name
        : '✓ ' + files.map(f => f.name).join('  +  ');
      showFileMsg(label, false);
    }

    hideApiStatus();
    analyzeBtn.textContent = 'Analyse Policy';
    analyzeBtn.disabled = selectedFiles.length === 0;
  }

  function showFileMsg(text, isError) {
    fileNameEl.textContent = text;
    fileNameEl.style.color = isError ? '#c0392b' : '#800046';
  }

  function setApiStatus(text, kind) {
    apiStatusMsg.textContent = text;
    apiStatusMsg.className = 'api-status status-' + kind;
    apiStatusMsg.style.display = 'block';
  }

  function hideApiStatus() {
    apiStatusMsg.style.display = 'none';
  }

  /* ---------- send file to backend, with demo-data fallback ---------- */
  async function analyzePolicyPDF(file, indexHint) {
    try {
      return await callBackend(file);
    } catch (err) {
      console.warn('Backend not reachable yet, showing demo data instead:', err.message);
      return generateMockResult(file, indexHint);
    }
  }

  async function callBackend(file) {
    const formData = new FormData();
    formData.append('file', file);

    try {
      console.log("Sending PDF to backend for RAG processing...");
      setApiStatus('⏳ Uploading and analyzing document... this takes a few seconds.', 'loading');
      
      const res = await fetch('http://127.0.0.1:5000/upload', { 
        method: 'POST', 
        body: formData 
      });
      
      if (!res.ok) throw new Error('backend returned ' + res.status);
      
      const responseData = await res.json();
      console.log("Analysis Complete:", responseData);
      
      // Use the REAL data from the backend Analyze Agent, not the mock data!
      return normalizeResult(responseData.analysis, file, false);

    } catch (networkErr) {
      console.warn('Backend upload failed.', networkErr);
      setApiStatus('⚠ Upload failed. Is the Flask server running?', 'error');
      throw networkErr;
    }
  }

    // 2. Return her mock data so the beautiful UI dashboards still populate instantly
  //   return generateMockResult(file, 0);
  // }

  function normalizeResult(raw, file, isMock) {
    const typeToBadge = { 'Health': 'badge-health', 'Term Life': 'badge-term', 'Motor': 'badge-motor' };
    return {
      fileName: file.name,
      isMock: !!isMock,
      policyName: raw.policyName || file.name.replace(/\.pdf$/i, ''),
      insurer: raw.insurer || 'Unknown insurer',
      policyType: raw.policyType || 'Other',
      badgeClass: typeToBadge[raw.policyType] || 'badge-other',
      pageCount: raw.pageCount || '—',
      premium: raw.premium || 'Not specified',
      sumInsured: raw.sumInsured || 'Not specified',
      summary: raw.summary || 'No summary available.',
      chatIntro: raw.chatIntro || ('Hi! I\'ve read your ' + (raw.policyName || file.name) + ' policy. Ask me anything.'),
      evidenceCards: Array.isArray(raw.evidenceCards) ? raw.evidenceCards : [],
      compareMetrics: raw.compareMetrics && typeof raw.compareMetrics === 'object' ? raw.compareMetrics : {},
    };
  }
// COMPARISONS!!!!!!
  /* ---------- demo data (used until the real backend is connected) ---------- */
  const MOCK_TEMPLATES = [
    {
      insurer: 'Star Health', policyType: 'Health',
      premium: '₹12,400/yr', sumInsured: '₹5,00,000',
      summary: 'A family floater health plan covering hospitalisation, daycare procedures and pre/post-hospitalisation expenses for you and your dependents, with a 3-year waiting period on pre-existing conditions.',
      chatIntro: 'Hi! I\'ve read your Star Health policy. Ask me anything about coverage, claims, or exclusions.',
      evidenceCards: [
        { type: 'covered',   title: 'Daycare procedures', text: 'Covers 541 listed daycare procedures requiring less than 24 hours of hospitalisation.', clause: 'Clause 3.4', page: 6 },
        { type: 'excluded',  title: 'Cosmetic treatment', text: 'Cosmetic or plastic surgery is excluded unless required due to an accident covered under the policy.', clause: 'Clause 7.1', page: 12 },
        { type: 'limit',     title: 'Room rent capping', text: 'Room rent is capped at 1% of the sum insured per day for normal rooms.', clause: 'Clause 4.2', page: 8 },
        { type: 'condition', title: 'Pre-existing disease wait', text: 'Pre-existing conditions declared at inception are covered only after a continuous 3-year waiting period.', clause: 'Clause 6.1', page: 11 },
        { type: 'covered',   title: 'Maternity benefit', text: 'Covers normal delivery and C-section after a 2-year waiting period, capped per policy year.', clause: 'Clause 3.9', page: 7 },
        { type: 'excluded',  title: 'Self-inflicted injury', text: 'Treatment for self-inflicted injury or attempted suicide is not covered.', clause: 'Clause 7.5', page: 13 },
      ],
      compareMetrics: {
        'Annual premium': '₹12,400', 'Sum insured': '₹5,00,000', 'Room rent limit': '1% / day',
        'Daycare procedures': '541 procedures', 'No-claim bonus': '10% / yr', 'Maternity cover': 'Yes',
        'Pre-existing wait': '3 years', 'Cashless hospitals': '14,000+',
      },
    },
    {
      insurer: 'HDFC ERGO', policyType: 'Health',
      premium: '₹15,200/yr', sumInsured: '₹7,50,000',
      summary: 'A comprehensive health plan with no room-rent capping and a shorter 2-year pre-existing disease waiting period, aimed at higher-cover seekers willing to pay a higher premium.',
      chatIntro: 'Hi! I\'ve read your HDFC ERGO policy. Ask me anything about coverage, claims, or exclusions.',
      evidenceCards: [
        { type: 'covered',   title: 'No room-rent capping', text: 'No restriction on room category or daily room rent — any room can be chosen.', clause: 'Clause 5.1', page: 9 },
        { type: 'excluded',  title: 'War-related injury', text: 'Injuries arising from war, invasion, or nuclear risk are not covered.', clause: 'Clause 8.2', page: 14 },
        { type: 'limit',     title: 'Cataract surgery cap', text: 'Cataract treatment is capped at ₹40,000 per eye per policy year.', clause: 'Clause 4.6', page: 10 },
        { type: 'condition', title: 'Pre-existing disease wait', text: 'Pre-existing conditions are covered after a continuous 2-year waiting period.', clause: 'Clause 6.3', page: 12 },
        { type: 'covered',   title: 'AYUSH treatment', text: 'Covers inpatient AYUSH treatment (Ayurveda, Yoga, Unani, Siddha, Homeopathy) up to sum insured.', clause: 'Clause 3.7', page: 8 },
        { type: 'excluded',  title: 'Experimental treatment', text: 'Unproven or experimental treatments not recognised by the medical council are excluded.', clause: 'Clause 7.8', page: 15 },
      ],
      compareMetrics: {
        'Annual premium': '₹15,200', 'Sum insured': '₹7,50,000', 'Room rent limit': 'No limit',
        'Daycare procedures': '584 procedures', 'No-claim bonus': '50% (max, over 5 yrs)', 'Maternity cover': 'No',
        'Pre-existing wait': '2 years', 'Cashless hospitals': '13,000+',
      },
    },
  ];

  function generateMockResult(file, indexHint) {
    const template = MOCK_TEMPLATES[indexHint % MOCK_TEMPLATES.length];
    const raw = Object.assign({}, template, {
      policyName: file.name.replace(/\.pdf$/i, ''),
      pageCount: 10 + Math.floor(Math.random() * 12),
    });
    return normalizeResult(raw, file, true);
  }

  /* ---------- Analyse button ---------- */
  analyzeBtn.addEventListener('click', async function () {
    if (!selectedFiles.length) {
      showFileMsg('⚠ Please select at least one PDF first.', true);
      return;
    }

    hideApiStatus();
    const btn = this;
    btn.textContent = '⏳ Analysing…';
    btn.disabled = true;

    const results = [];
    for (let i = 0; i < selectedFiles.length; i++) {
      results.push(await analyzePolicyPDF(selectedFiles[i], i));
    }

    btn.disabled = false;
    btn.textContent = 'Analyse Policy';

    state.policies = results;
    state.activeIndex = 0;

    // We successfully chunked and stored the PDF in ChromaDB!
    setApiStatus('✓ Document vectorized and ready for analysis. Scroll down to chat.', 'success');

    renderSidebar();
    renderActivePolicy();
    renderComparisonTable();

    const chatSection = document.getElementById('chat-section');
    if (chatSection) chatSection.scrollIntoView({ behavior: 'smooth' });
  });

  /* ---------- sidebar (doc switcher) ---------- */
  function renderSidebar() {
    docCardList.innerHTML = '';
    state.policies.forEach((policy, i) => {
      const card = document.createElement('div');
      card.className = 'doc-card' + (i === state.activeIndex ? ' active' : '');
      card.tabIndex = 0;
      card.setAttribute('role', 'button');
      card.setAttribute('aria-pressed', i === state.activeIndex ? 'true' : 'false');
      card.dataset.index = String(i);
      card.innerHTML =
        '<div class="doc-name">' + escapeHtml(policy.policyName) + '</div>' +
        '<div class="doc-meta">' + escapeHtml(String(policy.pageCount)) + ' pages · ' + escapeHtml(policy.insurer) + (policy.isMock ? ' · demo' : '') + '</div>' +
        '<span class="doc-badge ' + policy.badgeClass + '">' + escapeHtml(policy.policyType) + '</span>';
      docCardList.appendChild(card);
    });
  }

  docCardList.addEventListener('click', (e) => {
    const card = e.target.closest('.doc-card');
    if (!card) return;
    selectPolicy(Number(card.dataset.index));
  });

  docCardList.addEventListener('keydown', (e) => {
    const card = e.target.closest('.doc-card');
    if (!card) return;
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      selectPolicy(Number(card.dataset.index));
    }
  });

  function selectPolicy(index) {
    if (index === state.activeIndex || !state.policies[index]) return;
    state.activeIndex = index;
    renderSidebar();
    renderActivePolicy();
  }

  /* ---------- summary + chat + evidence for the active policy ---------- */
  function renderActivePolicy() {
    const policy = state.policies[state.activeIndex];
    if (!policy) return;

    summaryCard.style.display = 'block';
    summaryBadge.className = 'summary-badge ' + policy.badgeClass;
    summaryBadge.textContent = policy.policyType;
    summaryTitle.textContent = policy.policyName;
    summaryMeta.textContent = policy.pageCount + ' pages · ' + policy.insurer + (policy.isMock ? ' · demo data' : '');
    summaryText.textContent = policy.summary;
    summaryStats.innerHTML =
      '<div class="summary-stat"><span class="stat-label">Premium</span><span class="stat-value">' + escapeHtml(policy.premium) + '</span></div>' +
      '<div class="summary-stat"><span class="stat-label">Sum insured</span><span class="stat-value">' + escapeHtml(policy.sumInsured) + '</span></div>';

    chatDocName.textContent = policy.policyName;
    chatMessages.innerHTML = '';
    appendMessage(escapeHtml(policy.chatIntro), 'bot');

    renderEvidenceCards(policy.evidenceCards);
    resetEvidenceFilter();
  }

  /* ---------- evidence cards ---------- */
  const EV_TAG_META = {
    covered:   { label: 'Covered',   cls: 'tag-covered',   icon: '<polyline points="20 6 9 17 4 12"/>' },
    excluded:  { label: 'Excluded',  cls: 'tag-excluded',  icon: '<line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>' },
    limit:     { label: 'Limit',     cls: 'tag-limit',     icon: '<path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>' },
    condition: { label: 'Condition', cls: 'tag-condition', icon: '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>' },
  };

  function renderEvidenceCards(cards) {
    evGrid.innerHTML = '';
    if (!cards || !cards.length) {
      evGrid.innerHTML = '<p style="color:rgba(255,255,255,0.6); font-size:13px;">No evidence cards were returned for this policy.</p>';
      return;
    }
    cards.forEach(c => {
      const meta = EV_TAG_META[c.type] || EV_TAG_META.condition;
      const article = document.createElement('article');
      article.className = 'ev-card';
      article.dataset.type = c.type;
      article.innerHTML =
        '<div class="ev-card-top">' +
          '<span class="ev-tag ' + meta.cls + '">' +
            '<svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + meta.icon + '</svg>' +
            meta.label +
          '</span>' +
          '<h3 class="ev-clause-title">' + escapeHtml(c.title || '') + '</h3>' +
          '<p class="ev-clause-text">' + escapeHtml(c.text || '') + '</p>' +
        '</div>' +
        '<div class="ev-card-bottom">' +
          '<div class="ev-source">' +
            '<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>' +
            // FIX: This forces it to read the dynamic data from the AI
            escapeHtml(c.clause || 'General') + ', Page ' + escapeHtml(String(c.page || '—')) +
          '</div>' +
          '<button class="ev-action view-doc-btn">View in doc' +
            '<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>' +
          '</button>' +
        '</div>';
      evGrid.appendChild(article);
    });
  }

  function resetEvidenceFilter() {
    document.querySelectorAll('.ev-filter').forEach(b => b.classList.remove('active'));
    const allBtn = document.querySelector('.ev-filter[data-filter="all"]');
    if (allBtn) allBtn.classList.add('active');
  }

  // Delegated + re-queried at click-time, so this keeps working after
  // evGrid is regenerated by renderEvidenceCards().
  if (evFilterWrap) {
    evFilterWrap.addEventListener('click', (e) => {
      const btn = e.target.closest('.ev-filter');
      if (!btn) return;
      document.querySelectorAll('.ev-filter').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const filter = btn.dataset.filter;
      document.querySelectorAll('.ev-card').forEach(card => {
        const show = filter === 'all' || card.dataset.type === filter;
        card.classList.toggle('hidden', !show);
      });
    });
  }

  /* ---------- comparison table ---------- */
  function renderComparisonTable() {
    if (state.policies.length < 2) {
      compareSub.textContent = state.policies.length === 1
        ? 'Upload one more policy to compare it here — showing a sample comparison for now.'
        : 'Upload two policies and compare them side-by-side across every dimension.';
      return; // leave the sample table in place
    }

    compareSub.textContent = 'Comparing your two uploaded policies across every dimension.';

    const a = state.policies[0];
    const b = state.policies[1];

    compareTheadRow.innerHTML =
      '<th class="compare-th-label"></th>' +
      '<th class="compare-th featured">' +
        '<div class="compare-insurer">' + escapeHtml(a.insurer) + '</div>' +
        '<div class="compare-plan">' + escapeHtml(a.policyName) + '</div>' +
        '<div class="compare-premium">' + escapeHtml(a.premium) + '</div>' +
      '</th>' +
      '<th class="compare-th">' +
        '<div class="compare-insurer">' + escapeHtml(b.insurer) + '</div>' +
        '<div class="compare-plan">' + escapeHtml(b.policyName) + '</div>' +
        '<div class="compare-premium">' + escapeHtml(b.premium) + '</div>' +
      '</th>';

    const keys = Array.from(new Set([
      ...Object.keys(a.compareMetrics || {}),
      ...Object.keys(b.compareMetrics || {}),
    ]));

    compareTbody.innerHTML = keys.map(key =>
      '<tr>' +
        '<td class="compare-row-label">' + escapeHtml(key) + '</td>' +
        '<td class="compare-cell featured">' + escapeHtml((a.compareMetrics || {})[key] || '—') + '</td>' +
        '<td class="compare-cell">' + escapeHtml((b.compareMetrics || {})[key] || '—') + '</td>' +
      '</tr>'
    ).join('');
  }

  /* ---------- chat ---------- */
  // Canned answers used only before any policy has been analyzed,
  // so the page still feels alive while the backend is being wired up.
  const DEMO_ANSWERS = {
    'What is not covered?': 'Key exclusions: <strong>cosmetic surgery, dental treatment, self-inflicted injuries, war-related injuries, and experimental treatments</strong>. Pre-existing conditions are excluded for the first 3 years.',
    'How do I file a claim?': 'For <strong>cashless claims</strong>: notify Star Health 24 hrs before planned admission (4 hrs for emergencies). Show your e-card at a network hospital. For <strong>reimbursement</strong>: submit bills within 30 days of discharge.',
    'What is the no-claim bonus?': 'You earn a <strong>10% bonus on sum insured for every claim-free year</strong>, up to 50%. After 5 clean years your ₹5L cover grows to ₹7.5L at no extra premium.',
    'Are pre-existing diseases covered?': '<strong>Yes, after a 3-year waiting period.</strong> Conditions declared at policy inception are covered from year 4 onwards. Undisclosed conditions are permanently excluded.',
  };
  const DEMO_FALLBACK = 'I\'ve noted your question. Upload and analyse a policy above to see this respond with real document-grounded answers.';
  const LIVE_FALLBACK = 'I don\'t have a confident answer for that from the extracted evidence cards yet — try one of the quick questions below.';

  quickChips && quickChips.querySelectorAll('.chip').forEach(chip => {
    chip.addEventListener('click', () => sendMessage(chip.dataset.q));
  });

  sendBtn && sendBtn.addEventListener('click', () => {
    const q = chatInput.value.trim();
    if (q) sendMessage(q);
  });

  chatInput && chatInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      const q = chatInput.value.trim();
      if (q) sendMessage(q);
    }
  });

  async function sendMessage(text) {
    // 1. Show user message
    appendMessage(escapeHtml(text), 'user');
    chatInput.value = '';
    
    // 2. Show typing indicator
    const typingEl = appendTyping();

    try {
      // 3. Send query to your multi-agent backend
      const res = await fetch('http://127.0.0.1:5000/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: text })
      });
      
      const data = await res.json();
      typingEl.remove();

      if (data.status === 'success') {
        // 1. First, convert all invisible LLM line breaks into HTML line breaks!
        let formattedText = data.final_verdict.replace(/\n/g, '<br>');
        
        // 2. Then, apply your beautiful maroon bolding to the headers
        formattedText = formattedText
            .replace(/Coverage Status:/g, '<strong style="color: #800046;">Coverage Status:</strong>')
            .replace(/Reason:/g, '<strong style="color: #800046;">Reason:</strong>')
            .replace(/Definitions:/g, '<strong style="color: #800046;">Definitions:</strong>')
            .replace(/Exception:/g, '<strong style="color: #800046;">Exception:</strong>')
            .replace(/Expenses Covered:/g, '<strong style="color: #800046;">Expenses Covered:</strong>')
            .replace(/Evidence:/g, '<strong style="color: #800046;">Evidence:</strong>');
            
        // 3. Clean up the UI by automatically hiding the Definitions section if the AI says N/A
        formattedText = formattedText.replace(/<strong style="color: #800046;">Definitions:<\/strong> N\/A<br>/g, '');
            
        appendMessage(formattedText, 'bot');
      } else {
        appendMessage("Sorry, the AI agents encountered an error.", 'bot');
      }

    } catch (err) {
      typingEl.remove();
      
      // Check if it's likely a token/rate-limit error based on the response
      if (err.message.includes('429') || err.message.includes('limit')) {
        appendMessage("<strong>System Note:</strong> We’ve hit the current token limit for our AI model's free-tier usage. Please wait for some moment for the quota to reset.", 'bot');
      } else {
        appendMessage("<strong>System Note:</strong> The AI backend is temporarily unreachable. Please ensure the server is active.", 'bot');
      }
    }
  }

  function appendMessage(html, role) {
    const div = document.createElement('div');
    div.className = 'msg msg-' + role;
    div.innerHTML = html;
    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return div;
  }

  function appendTyping() {
    const div = document.createElement('div');
    div.className = 'typing-indicator';
    div.innerHTML = '<div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div>';
    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return div;
  }

  /* ---------- tiny helper ---------- */
  function escapeHtml(str) {
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  // Doc-card sidebar click also wires keyboard support via the delegated
  // listeners above; nothing else to do here.

})();


/* ══════════════════════════════════════════
   5. ADD PLAN BUTTON (Comparison)
   ══════════════════════════════════════════ */
(function () {
  const addPlanBtn = document.getElementById('addPlanBtn');
  if (!addPlanBtn) return;

  addPlanBtn.addEventListener('click', () => {
    const uploadSection = document.getElementById('upload-section');
    if (uploadSection) {
      uploadSection.scrollIntoView({ behavior: 'smooth' });
    }
  });
})();


/* ══════════════════════════════════════════
   6. ACTIVE NAV LINK ON SCROLL
   ══════════════════════════════════════════ */
(function () {
  const sections = [
    { id: 'upload-section',   href: '#upload-section' },
    { id: 'chat-section',     href: '#chat-section' },
    { id: 'evidence-section', href: '#evidence-section' },
    { id: 'compare-section',  href: '#compare-section' },
  ];

  const navLinks = document.querySelectorAll('.nav-link');

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const active = sections.find(s => s.id === entry.target.id);
          if (!active) return;
          navLinks.forEach(link => {
            link.style.color =
              link.getAttribute('href') === active.href
                ? '#fff'
                : 'rgba(255,255,255,0.75)';
          });
        }
      });
    },
    { rootMargin: '-40% 0px -55% 0px' }
  );

  sections.forEach(({ id }) => {
    const el = document.getElementById(id);
    if (el) observer.observe(el);
  });
})();

  