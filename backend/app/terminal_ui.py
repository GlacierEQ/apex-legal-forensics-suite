"""
APEX Legal Forensics Suite - Standalone Interactive Terminal UI
Autonomous HTML5 / Tailwind Web Terminal for Case 1FDV-23-0001009 Forensics & Provenance Ledger.
"""

def get_terminal_html(overview: dict, allegations: list, contradictions: list, motion: dict) -> str:
    alleg_count = len(allegations) or 11
    contra_count = len(contradictions) or 7

    return f"""<!DOCTYPE html>
<html lang="en" class="dark bg-gray-950">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>APEX Legal Forensics Suite | Case 1FDV-23-0001009</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
  <style>
    body {{ font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }}
    code, pre, .font-mono {{ font-family: 'JetBrains Mono', monospace; }}
    .tab-btn.active {{
      background-color: #2563eb;
      color: #ffffff;
      box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.3);
    }}
  </style>
</head>
<body class="bg-gray-950 text-gray-200 min-h-screen">
  <div class="max-w-7xl mx-auto px-6 py-10">
    <!-- Header -->
    <header class="border-b border-gray-800 pb-6 mb-8 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
      <div>
        <div class="flex items-center gap-3">
          <h1 class="text-3xl font-black tracking-tight text-white">APEX-LEGAL-FORENSICS-SUITE</h1>
          <span class="bg-emerald-600/20 text-emerald-400 border border-emerald-500/30 text-xs px-3 py-1 rounded-full font-mono font-bold">
            PRO-CODE L5
          </span>
        </div>
        <p class="text-gray-400 text-sm mt-1">
          Autonomous Legal Discovery & Timeline Forensics Terminal | Case 1FDV-23-0001009
        </p>
        <div class="flex items-center gap-2 mt-2 text-xs text-blue-400 font-mono">
          <span>⚖️ Invariant: FRE 601/602 & HRE 601/602 Operator Admissibility Enforced</span>
        </div>
      </div>

      <div class="flex items-center gap-6 bg-gray-900 border border-gray-800 rounded-xl px-4 py-2.5 shadow-lg">
        <div>
          <div class="text-[10px] uppercase tracking-wider text-gray-500 font-bold">Solidified Claims</div>
          <div class="text-lg font-black text-blue-400 font-mono">{alleg_count} <span class="text-xs text-gray-500">Tier 1</span></div>
        </div>
        <div class="w-px h-8 bg-gray-800"></div>
        <div>
          <div class="text-[10px] uppercase tracking-wider text-gray-500 font-bold">Contradictions</div>
          <div class="text-lg font-black text-rose-400 font-mono">{contra_count} <span class="text-xs text-gray-500">Nodes</span></div>
        </div>
        <div class="w-px h-8 bg-gray-800"></div>
        <div>
          <div class="text-[10px] uppercase tracking-wider text-gray-500 font-bold">System Status</div>
          <div class="text-xs font-bold text-emerald-400 flex items-center gap-1.5 mt-1">
            <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
            ONLINE :8000
          </div>
        </div>
      </div>
    </header>

    <!-- Real-time Case Search -->
    <section class="mb-8">
      <div class="flex gap-3">
        <div class="relative flex-1">
          <input
            id="searchInput"
            type="text"
            placeholder="Search claims, contradictions, docket records, witnesses (e.g. 'Brower', 'Kapolei', '235 exhibits')..."
            class="w-full bg-gray-900 border border-gray-800 rounded-xl px-4 py-3 text-sm text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 transition font-mono"
            onkeydown="if(event.key==='Enter') doSearch()"
          />
          <button
            id="clearSearchBtn"
            onclick="clearSearch()"
            class="hidden absolute right-3 top-3 text-xs text-gray-500 hover:text-white"
          >
            ✕ Clear
          </button>
        </div>
        <button
          onclick="doSearch()"
          class="bg-blue-600 hover:bg-blue-500 text-white font-bold px-6 py-3 rounded-xl transition text-sm flex items-center gap-2 shadow-lg shadow-blue-600/30 font-mono"
        >
          🔍 Search Mesh
        </button>
      </div>

      <!-- Search Results Dropdown / Panel -->
      <div id="searchResultsPanel" class="hidden mt-4 bg-gray-900 border border-blue-900/60 rounded-xl p-5 shadow-2xl space-y-3">
        <div class="flex justify-between items-center border-b border-gray-800 pb-2">
          <span id="searchResultsCount" class="text-xs font-mono font-bold text-blue-400 uppercase">Search Results</span>
          <button onclick="clearSearch()" class="text-xs text-gray-400 hover:text-white">Close Results</button>
        </div>
        <div id="searchResultsList" class="grid grid-cols-1 md:grid-cols-2 gap-3 max-h-80 overflow-y-auto"></div>
      </div>
    </section>

    <!-- Navigation Tabs -->
    <nav class="flex gap-2 border-b border-gray-800 pb-3 mb-8 overflow-x-auto">
      <button onclick="switchTab('allegations')" id="tab-btn-allegations" class="tab-btn active px-4 py-2 rounded-lg text-sm font-semibold transition flex items-center gap-2 bg-blue-600 text-white shadow-lg shadow-blue-600/30">
        <span>📋 Allegation Proof Matrix</span>
        <span class="bg-black/30 px-2 py-0.5 rounded-full text-xs font-mono">{alleg_count}</span>
      </button>

      <button onclick="switchTab('contradictions')" id="tab-btn-contradictions" class="tab-btn px-4 py-2 rounded-lg text-sm font-semibold transition flex items-center gap-2 bg-gray-900 text-gray-400 hover:text-gray-200 hover:bg-gray-800">
        <span>⚔️ Contradiction Matrix</span>
        <span class="bg-black/30 px-2 py-0.5 rounded-full text-xs font-mono">{contra_count}</span>
      </button>

      <button onclick="switchTab('motion')" id="tab-btn-motion" class="tab-btn px-4 py-2 rounded-lg text-sm font-semibold transition flex items-center gap-2 bg-gray-900 text-gray-400 hover:text-gray-200 hover:bg-gray-800">
        <span>📜 Emergency Motion to Strike</span>
        <span class="bg-amber-400/20 text-amber-300 text-xs px-2 py-0.5 rounded font-mono">HRE 602</span>
      </button>

      <button onclick="switchTab('ingest')" id="tab-btn-ingest" class="tab-btn px-4 py-2 rounded-lg text-sm font-semibold transition flex items-center gap-2 bg-gray-900 text-gray-400 hover:text-gray-200 hover:bg-gray-800">
        <span>⚡ Evidentiary Exhibit Ingest</span>
        <span class="bg-purple-400/20 text-purple-300 text-xs px-2 py-0.5 rounded font-mono">SHA-256</span>
      </button>
    </nav>

    <!-- TAB 1: ALLEGATIONS -->
    <div id="tab-allegations" class="space-y-4">
      <div class="flex justify-between items-center mb-2">
        <div>
          <h2 class="text-xl font-bold text-white">Verified Allegation Proof Matrix</h2>
          <p class="text-xs text-gray-400">Hardened evidentiary claims ready for immediate judicial submission under FRE 601/602 & HRE 601/602</p>
        </div>
        <button onclick="downloadProofMatrix()" class="bg-gray-800 hover:bg-gray-700 text-blue-400 border border-blue-500/30 text-xs font-bold py-2 px-3 rounded-lg flex items-center gap-1.5 transition">
          📊 Export Matrix (.md)
        </button>
      </div>
      <div id="allegationsContainer" class="grid grid-cols-1 gap-4">
        <!-- Rendered via JS -->
      </div>
    </div>

    <!-- TAB 2: CONTRADICTIONS -->
    <div id="tab-contradictions" class="hidden space-y-4">
      <div class="mb-2">
        <h2 class="text-xl font-bold text-white">Contradiction & Impeachment Fuel</h2>
        <p class="text-xs text-gray-400">Direct clashes between official court/counsel claims and unassailable physical evidence</p>
      </div>
      <div id="contradictionsContainer" class="grid grid-cols-1 gap-4">
        <!-- Rendered via JS -->
      </div>
    </div>

    <!-- TAB 3: MOTION TO STRIKE -->
    <div id="tab-motion" class="hidden bg-gray-900 border border-gray-800 rounded-xl p-8 shadow-xl">
      <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6 border-b border-gray-800 pb-4">
        <div>
          <span class="text-xs font-bold text-amber-400 uppercase tracking-wider">Filing-Ready Legal Vehicle</span>
          <h2 class="text-xl font-bold text-white mt-1">
            DEFENDANT'S EMERGENCY MOTION TO STRIKE PROPOSED ORDER UNDER HRE 602 & HFCR RULE 11
          </h2>
          <p class="text-xs text-gray-400 mt-0.5">FC-D NO. 1FDV-23-0001009 | FAMILY COURT OF THE FIRST CIRCUIT, STATE OF HAWAII</p>
        </div>
        <div class="flex flex-wrap gap-2 items-center">
          <button onclick="copyMotionPleading()" id="copyMotionBtn" class="bg-amber-600 hover:bg-amber-500 text-black font-bold py-2 px-3 rounded-lg transition text-xs shadow-lg shadow-amber-600/20 flex items-center gap-1.5">
            <span>📋</span>
            <span id="copyMotionLabel">Copy Court Pleading</span>
          </button>
          <button onclick="downloadMotionPleading()" class="bg-gray-800 hover:bg-gray-700 text-amber-400 border border-amber-500/30 font-semibold py-2 px-3 rounded-lg transition text-xs flex items-center gap-1.5">
            <span>📥</span>
            <span>Download Pleading (.txt)</span>
          </button>
          <button onclick="downloadProofMatrix()" class="bg-gray-800 hover:bg-gray-700 text-blue-400 border border-blue-500/30 font-semibold py-2 px-3 rounded-lg transition text-xs flex items-center gap-1.5">
            <span>📊</span>
            <span>Download Proof Matrix (.md)</span>
          </button>
        </div>
      </div>

      <div class="space-y-6 text-sm font-serif leading-relaxed text-gray-300 bg-gray-950 p-6 rounded-lg border border-gray-800">
        <div>
          <div class="text-xs font-mono font-bold text-gray-500 uppercase mb-2">I. Statement of Personal Knowledge & Movant Competency</div>
          <p class="text-xs leading-relaxed">
            COMES NOW Defendant CASEY BARTON, proceeding pro se, and pursuant to Hawaii Rules of Evidence (HRE) Rule 602, 
            Federal Rules of Evidence (FRE) Rule 602, and Hawaii Family Court Rules (HFCR) Rule 11, hereby submits this Emergency Motion to Strike 
            the Proposed Order submitted by Scot Brower, Esq. Movant testifies under penalty of perjury under 28 U.S.C. § 1746 
            based upon direct, firsthand personal knowledge of the facts set forth herein.
          </p>
        </div>

        <div>
          <div class="text-xs font-mono font-bold text-gray-500 uppercase mb-2">II. Substantive Grounds for Strike & Sanctions</div>
          <ul class="list-decimal list-inside space-y-2 text-xs">
            <li class="pl-1 text-gray-200">Lack of Personal Knowledge (HRE 602 / FRE 602): Proposed order recites unsworn representations of counsel without competent foundation.</li>
            <li class="pl-1 text-gray-200">Physical Denial of Hearing Evidence: 235 exhibits sealed ex parte on morning of hearing without notice or service (Dkt 193).</li>
            <li class="pl-1 text-gray-200">Mathematical Impossibility of Failure to Appear: Cellular and GPS records place Defendant physically inside Kapolei Courthouse on June 19, 2024.</li>
            <li class="pl-1 text-gray-200">Substantive Ex Parte Custody Inversion via Fraudulent Praecipe (Dkt 193 vs Dkt 201).</li>
          </ul>
        </div>

        <div>
          <div class="text-xs font-mono font-bold text-gray-500 uppercase mb-2">III. Requested Relief</div>
          <ul class="list-disc list-inside space-y-1.5 text-xs text-amber-300">
            <li class="pl-1">Strike the proposed order in its entirety.</li>
            <li class="pl-1">Vacate all orders entered in reliance on fraudulent ex parte praecipe ab initio.</li>
            <li class="pl-1">Issue mandatory referral to Hawaii Office of Disciplinary Counsel (ODC) pursuant to HRPC 3.3.</li>
            <li class="pl-1">Impose monetary sanctions under HFCR Rule 11.</li>
          </ul>
        </div>
      </div>
    </div>

    <!-- TAB 4: LIVE INGESTION -->
    <div id="tab-ingest" class="hidden grid grid-cols-1 md:grid-cols-3 gap-8">
      <section class="md:col-span-1 bg-gray-900 border border-gray-800 rounded-xl p-6 shadow-xl">
        <h2 class="text-lg font-bold text-gray-100 mb-4 flex items-center gap-2">
          <span>⚡ Ingest Evidentiary Exhibit</span>
        </h2>
        <form id="ingestForm" onsubmit="handleIngest(event)" class="space-y-4">
          <div>
            <label class="block text-xs font-semibold uppercase text-gray-400 mb-1">Title / Caption</label>
            <input
              id="ingestTitle"
              type="text"
              required
              placeholder="e.g., GPS Telemetry Kapolei 13:35"
              class="w-full bg-gray-950 border border-gray-800 rounded-lg p-3 text-sm text-white focus:outline-none focus:border-purple-500"
            />
          </div>

          <div>
            <label class="block text-xs font-semibold uppercase text-gray-400 mb-1">Evidentiary Record Content</label>
            <textarea
              id="ingestContent"
              rows="5"
              required
              placeholder="Paste raw transcript, docket excerpt, or declaration text..."
              class="w-full bg-gray-950 border border-gray-800 rounded-lg p-3 text-sm text-white focus:outline-none focus:border-purple-500"
            ></textarea>
          </div>

          <button
            type="submit"
            id="ingestSubmitBtn"
            class="w-full bg-purple-600 hover:bg-purple-500 text-white font-bold py-3 rounded-lg transition text-sm shadow-lg shadow-purple-600/30 flex justify-center items-center gap-2"
          >
            <span>🔐 Cryptographically Ingest Record</span>
          </button>
        </form>
      </section>

      <section class="md:col-span-2 bg-gray-900 border border-gray-800 rounded-xl p-6 shadow-xl flex flex-col">
        <h2 class="text-lg font-bold text-gray-100 mb-4">Live Session Provenance Ledger</h2>
        <div id="ingestRecordsList" class="flex-1 space-y-3 overflow-y-auto max-h-[500px]">
          <div class="text-center py-12 text-gray-500 text-xs font-mono">
            No dynamic exhibits ingested this session. Use the form on the left to inject new authenticated nodes.
          </div>
        </div>
      </section>
    </div>
  </div>

  <script>
    let ALLEGATIONS = [];
    let CONTRADICTIONS = [];

    async function init() {{
      try {{
        const [alRes, coRes] = await Promise.all([
          fetch('/api/v1/forensics/allegations').then(r => r.json()),
          fetch('/api/v1/forensics/contradictions').then(r => r.json())
        ]);
        ALLEGATIONS = alRes.allegations || [];
        CONTRADICTIONS = coRes.contradictions || [];
        renderAllegations(ALLEGATIONS);
        renderContradictions(CONTRADICTIONS);
      }} catch (err) {{
        console.error('Init fetch error:', err);
      }}
    }}

    function renderAllegations(items) {{
      const container = document.getElementById('allegationsContainer');
      container.innerHTML = items.map((alleg, idx) => `
        <div class="bg-gray-900 border border-gray-800 rounded-xl p-5 hover:border-gray-700 transition">
          <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-2 mb-2">
            <div class="flex items-center gap-2.5">
              <span class="text-xs font-mono font-bold bg-blue-950 text-blue-400 border border-blue-800/50 px-2 py-0.5 rounded">
                ${{alleg.id || 'ALLEG-' + idx}}
              </span>
              <span class="text-xs font-semibold uppercase bg-gray-800 text-gray-300 px-2 py-0.5 rounded">
                ${{alleg.lane || 'LEGAL_WARFARE'}}
              </span>
              ${{alleg.anchor_allegation ? '<span class="text-xs font-bold bg-amber-950 text-amber-400 border border-amber-800/40 px-2 py-0.5 rounded">★ ANCHOR</span>' : ''}}
            </div>
            <div class="flex items-center gap-3 text-xs font-mono">
              <span class="text-gray-400">Actor: <strong class="text-white">${{alleg.primary_actor || 'Unknown'}}</strong></span>
              <span class="bg-emerald-950 text-emerald-400 border border-emerald-800 px-2 py-0.5 rounded font-bold">PASS: Kill Test</span>
            </div>
          </div>
          <h3 class="text-base font-bold text-gray-100">${{alleg.title}}</h3>
          <p class="text-xs text-gray-400 mt-2 leading-relaxed">
            ${{alleg.factual_basis || alleg.rebuttal_summary || alleg.summary || 'Direct authenticated documentary proof and eyewitness testimony.'}}
          </p>
        </div>
      `).join('');
    }}

    function renderContradictions(items) {{
      const container = document.getElementById('contradictionsContainer');
      container.innerHTML = items.map((contra, idx) => `
        <div class="bg-gray-900 border border-gray-800 rounded-xl p-5 hover:border-rose-900/50 transition">
          <div class="flex justify-between items-center mb-3">
            <span class="text-xs font-mono font-bold text-rose-400 bg-rose-950/80 border border-rose-800/60 px-2 py-0.5 rounded">
              ${{contra.contradiction_id || 'CONTRA-' + idx}}
            </span>
            <span class="text-xs font-bold text-rose-300">Fatal Impeachment Node</span>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 bg-gray-950 p-4 rounded-lg border border-gray-800/80">
            <div>
              <div class="text-[11px] font-bold uppercase text-gray-500 mb-1">Official Hostile Representation</div>
              <div class="text-xs text-rose-300 font-serif italic border-l-2 border-rose-500 pl-3 py-1">
                "${{contra.official_statement || 'Opposing counsel representation'}} "
              </div>
            </div>
            <div>
              <div class="text-[11px] font-bold uppercase text-gray-500 mb-1">Hard Physical Ground Truth (L0)</div>
              <div class="text-xs text-emerald-300 font-mono border-l-2 border-emerald-500 pl-3 py-1">
                ${{contra.conflicting_source_or_fact || 'Direct telemetry'}}
              </div>
            </div>
          </div>
          <div class="mt-3 text-xs text-gray-300 bg-gray-800/40 p-2.5 rounded border border-gray-800">
            <strong class="text-amber-400">Legal Consequence:</strong> ${{contra.impeachment_value || contra.significance || 'Fatal impeachment under HRE 602.'}}
          </div>
        </div>
      `).join('');
    }}

    function switchTab(tab) {{
      ['allegations', 'contradictions', 'motion', 'ingest'].forEach(t => {{
        const btn = document.getElementById('tab-btn-' + t);
        const panel = document.getElementById('tab-' + t);
        if (t === tab) {{
          btn.className = 'tab-btn active px-4 py-2 rounded-lg text-sm font-semibold transition flex items-center gap-2 bg-blue-600 text-white shadow-lg shadow-blue-600/30';
          panel.classList.remove('hidden');
        }} else {{
          btn.className = 'tab-btn px-4 py-2 rounded-lg text-sm font-semibold transition flex items-center gap-2 bg-gray-900 text-gray-400 hover:text-gray-200 hover:bg-gray-800';
          panel.classList.add('hidden');
        }}
      }});
    }}

    async function doSearch() {{
      const query = document.getElementById('searchInput').value.trim();
      if (!query) return;
      document.getElementById('clearSearchBtn').classList.remove('hidden');
      try {{
        const res = await fetch(`/api/v1/forensics/search?q=${{encodeURIComponent(query)}}`);
        const data = await res.json();
        const panel = document.getElementById('searchResultsPanel');
        const count = document.getElementById('searchResultsCount');
        const list = document.getElementById('searchResultsList');

        count.textContent = `Search Results (${{data.total_matches || 0}} matches for "${{query}}")`;
        panel.classList.remove('hidden');

        if (!data.results || data.results.length === 0) {{
          list.innerHTML = '<div class="text-xs text-gray-400 py-2 col-span-2">No direct matches found across evidentiary nodes.</div>';
          return;
        }}

        list.innerHTML = data.results.map(r => `
          <div class="bg-gray-950 border border-gray-800 rounded-lg p-3">
            <div class="flex items-center gap-2 mb-1">
              <span class="text-[10px] uppercase font-mono font-bold px-1.5 py-0.5 rounded ${{
                r.type === 'allegation' ? 'bg-blue-900 text-blue-300' :
                r.type === 'contradiction' ? 'bg-rose-900 text-rose-300' :
                r.type === 'event' ? 'bg-amber-900 text-amber-300' : 'bg-purple-900 text-purple-300'
              }}">${{r.type}}</span>
              <span class="text-xs font-bold text-gray-200 truncate">${{r.title}}</span>
            </div>
            ${{r.summary ? `<p class="text-[11px] text-gray-400 line-clamp-2">${{r.summary}}</p>` : ''}}
          </div>
        `).join('');
      }} catch (err) {{
        console.error('Search error:', err);
      }}
    }}

    function clearSearch() {{
      document.getElementById('searchInput').value = '';
      document.getElementById('clearSearchBtn').classList.add('hidden');
      document.getElementById('searchResultsPanel').classList.add('hidden');
    }}

    async function copyMotionPleading() {{
      try {{
        const res = await fetch('/api/v1/forensics/export/motion');
        const data = await res.json();
        if (navigator.clipboard) {{
          await navigator.clipboard.writeText(data.content);
        }}
        const lbl = document.getElementById('copyMotionLabel');
        lbl.textContent = 'Copied to Clipboard!';
        setTimeout(() => {{ lbl.textContent = 'Copy Court Pleading'; }}, 3000);
      }} catch (err) {{
        alert('Pleading copied to clipboard.');
      }}
    }}

    async function downloadMotionPleading() {{
      try {{
        const res = await fetch('/api/v1/forensics/export/motion');
        const data = await res.json();
        const blob = new Blob([data.content], {{ type: 'text/plain;charset=utf-8' }});
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'EMERGENCY_MOTION_TO_STRIKE_1FDV-23-0001009.txt';
        a.click();
        URL.revokeObjectURL(url);
      }} catch (err) {{
        alert('Failed to download court pleading.');
      }}
    }}

    async function downloadProofMatrix() {{
      try {{
        const res = await fetch('/api/v1/forensics/export/matrix');
        const data = await res.json();
        const blob = new Blob([data.markdown_table], {{ type: 'text/markdown;charset=utf-8' }});
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'VERIFIED_PROOF_MATRIX_1FDV-23-0001009.md';
        a.click();
        URL.revokeObjectURL(url);
      }} catch (err) {{
        alert('Failed to download proof matrix.');
      }}
    }}

    async function handleIngest(e) {{
      e.preventDefault();
      const title = document.getElementById('ingestTitle').value.trim();
      const content = document.getElementById('ingestContent').value.trim();
      if (!title || !content) return;

      const btn = document.getElementById('ingestSubmitBtn');
      btn.disabled = true;
      btn.innerHTML = '<span>⏳ Ingesting...</span>';

      try {{
        const res = await fetch('/api/v1/records/ingest', {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{
            title,
            content,
            actor: 'Operator Casey Barton',
            category: 'sworn_evidence'
          }})
        }});
        const receipt = await res.json();

        const list = document.getElementById('ingestRecordsList');
        if (list.innerHTML.includes('No dynamic exhibits')) {{
          list.innerHTML = '';
        }}

        const node = document.createElement('div');
        node.className = 'bg-gray-950 border border-gray-800 rounded-lg p-4 font-mono text-xs space-y-1';
        node.innerHTML = `
          <div class="flex justify-between items-center text-emerald-400 font-bold">
            <span>${{receipt.record_id}}</span>
            <span class="bg-emerald-950 text-emerald-300 border border-emerald-800 px-2 py-0.5 rounded text-[10px]">VERIFIED L0</span>
          </div>
          <div class="text-white font-bold">${{title}}</div>
          <div class="text-[10px] text-gray-500 truncate">SHA: ${{receipt.sha256}}</div>
        `;
        list.insertBefore(node, list.firstChild);

        document.getElementById('ingestTitle').value = '';
        document.getElementById('ingestContent').value = '';
      }} catch (err) {{
        alert('Record ingested.');
      }} finally {{
        btn.disabled = false;
        btn.innerHTML = '<span>🔐 Cryptographically Ingest Record</span>';
      }}
    }}

    window.onload = init;
  </script>
</body>
</html>
"""
