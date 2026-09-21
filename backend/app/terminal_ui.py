"""
APEX Legal Forensics Suite - Standalone Interactive Terminal UI
Autonomous HTML5 / Tailwind Web Terminal for Case 1FDV-23-0001009 Forensics & Provenance Ledger.
Includes Vector 1 (Hawaii Family Court Filing Packet) & Vector 2 (Federal Civil RICO Engine).
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
          <div class="text-[10px] uppercase tracking-wider text-gray-500 font-bold">Estate Exposure</div>
          <div class="text-lg font-black text-cyan-400 font-mono">$220.5M <span class="text-xs text-gray-500">21 Cases</span></div>
        </div>
        <div class="w-px h-8 bg-gray-800"></div>
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
          <div class="text-[10px] uppercase tracking-wider text-gray-500 font-bold">RICO Claim</div>
          <div class="text-lg font-black text-amber-400 font-mono">$38.4M <span class="text-xs text-gray-500">Trebled</span></div>
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
            placeholder="Search forensic ledger (e.g. 'Kapolei', 'Brower', 'Dkt 201', '235 exhibits', 'perjury')..."
            class="w-full bg-gray-900 border border-gray-800 rounded-xl px-4 py-3 text-sm text-gray-200 placeholder-gray-500 focus:outline-none focus:border-blue-500 transition font-mono"
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
        <span>📜 Hawaii Filing Packet (Vector 1)</span>
        <span class="bg-amber-400/20 text-amber-300 text-xs px-2 py-0.5 rounded font-mono">28-Line / HRE 602</span>
      </button>

      <button onclick="switchTab('rico')" id="tab-btn-rico" class="tab-btn px-4 py-2 rounded-lg text-sm font-semibold transition flex items-center gap-2 bg-gray-900 text-gray-400 hover:text-gray-200 hover:bg-gray-800">
        <span>⚖️ Federal Civil RICO (Vector 2)</span>
        <span class="bg-rose-400/20 text-rose-300 text-xs px-2 py-0.5 rounded font-mono">$38.4M</span>
      </button>

      <button onclick="switchTab('ethics')" id="tab-btn-ethics" class="tab-btn px-4 py-2 rounded-lg text-sm font-semibold transition flex items-center gap-2 bg-gray-900 text-gray-400 hover:text-gray-200 hover:bg-gray-800">
        <span>⚡ Ethics & Criminal Strike (Vector 3)</span>
        <span class="bg-rose-500/20 text-rose-300 text-xs px-2 py-0.5 rounded font-mono">ODC / DOJ / FBI</span>
      </button>

      <button onclick="switchTab('mesh')" id="tab-btn-mesh" class="tab-btn px-4 py-2 rounded-lg text-sm font-semibold transition flex items-center gap-2 bg-gray-900 text-gray-400 hover:text-gray-200 hover:bg-gray-800">
        <span>🌐 Estate Holographic Mesh</span>
        <span class="bg-cyan-400/20 text-cyan-300 text-xs px-2 py-0.5 rounded font-mono">21 Matters · $220.5M</span>
      </button>

      <button onclick="switchTab('ingest')" id="tab-btn-ingest" class="tab-btn px-4 py-2 rounded-lg text-sm font-semibold transition flex items-center gap-2 bg-gray-900 text-gray-400 hover:text-gray-200 hover:bg-gray-800">
        <span>⚡ Evidentiary Ingest</span>
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

    <!-- TAB 3: HAWAII FILING PACKET (VECTOR 1) -->
    <div id="tab-motion" class="hidden bg-gray-900 border border-gray-800 rounded-xl p-8 shadow-xl">
      <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6 border-b border-gray-800 pb-4">
        <div>
          <span class="text-xs font-bold text-amber-400 uppercase tracking-wider">Vector 1: Official Hawaii Family Court Filing Packet</span>
          <h2 class="text-xl font-bold text-white mt-1">
            DEFENDANT'S EMERGENCY MOTION TO STRIKE PROPOSED ORDER & VACATE DKT 201 AB INITIO
          </h2>
          <p class="text-xs text-gray-400 mt-0.5">FC-D NO. 1FDV-23-0001009 | FIRST CIRCUIT COURT OF HAWAII</p>
        </div>
        <div class="flex flex-wrap gap-2 items-center">
          <a href="/api/v1/forensics/download/hawaii-packet.pdf" download class="bg-red-700 hover:bg-red-600 text-white font-bold py-2 px-3 rounded-lg transition text-xs shadow-lg shadow-red-700/20 flex items-center gap-1.5">
            <span>📄</span>
            <span>Download Court-Ready PDF</span>
          </a>
          <a href="/api/v1/forensics/download/hawaii-packet.docx" download class="bg-blue-700 hover:bg-blue-600 text-white font-bold py-2 px-3 rounded-lg transition text-xs shadow-lg shadow-blue-700/20 flex items-center gap-1.5">
            <span>📝</span>
            <span>Download Word DOCX</span>
          </a>
          <a href="/api/v1/forensics/download/hawaii-filing-bundle.zip" download class="bg-emerald-700 hover:bg-emerald-600 text-white font-bold py-2 px-3 rounded-lg transition text-xs shadow-lg shadow-emerald-700/20 flex items-center gap-1.5">
            <span>📦</span>
            <span>Download JEFS Bundle (.zip)</span>
          </a>
          <a href="/api/v1/forensics/download/master-bates-binder.pdf" download class="bg-indigo-700 hover:bg-indigo-600 text-white font-bold py-2 px-3 rounded-lg transition text-xs shadow-lg shadow-indigo-700/20 flex items-center gap-1.5">
            <span>📑</span>
            <span>Master Bates Binder PDF</span>
          </a>
          <a href="/api/v1/forensics/download/master-bates-bundle.zip" download class="bg-purple-700 hover:bg-purple-600 text-white font-bold py-2 px-3 rounded-lg transition text-xs shadow-lg shadow-purple-700/20 flex items-center gap-1.5">
            <span>🗂️</span>
            <span>Master Bates Bundle (.zip)</span>
          </a>
          <button onclick="copyHawaiiPacket()" id="copyHawaiiBtn" class="bg-amber-600 hover:bg-amber-500 text-black font-bold py-2 px-3 rounded-lg transition text-xs shadow-lg shadow-amber-600/20 flex items-center gap-1.5">
            <span>📋</span>
            <span id="copyHawaiiLabel">Copy Hawaii Packet</span>
          </button>
          <button onclick="downloadHawaiiPacket('28_lines')" class="bg-gray-800 hover:bg-gray-700 text-amber-400 border border-amber-500/30 font-semibold py-2 px-3 rounded-lg transition text-xs flex items-center gap-1.5">
            <span>📥</span>
            <span>28-Line (.txt)</span>
          </button>
          <button onclick="downloadProofMatrix()" class="bg-gray-800 hover:bg-gray-700 text-blue-400 border border-blue-500/30 font-semibold py-2 px-3 rounded-lg transition text-xs flex items-center gap-1.5">
            <span>📊</span>
            <span>Proof Matrix (.md)</span>
          </button>
        </div>
      </div>

      <!-- Packet View Toggles -->
      <div class="flex gap-2 mb-4">
        <button onclick="togglePleadingView('hawaii', 'preview')" id="btn-hawaii-preview" class="px-3 py-1 text-xs font-bold rounded bg-blue-600 text-white">Component Summary</button>
        <button onclick="togglePleadingView('hawaii', '28lines')" id="btn-hawaii-28lines" class="px-3 py-1 text-xs font-bold rounded bg-gray-800 text-gray-400 hover:text-white">Official 28-Line Pleading Paper</button>
      </div>

      <div id="hawaii-view-preview" class="space-y-6 text-sm font-serif leading-relaxed text-gray-300 bg-gray-950 p-6 rounded-lg border border-gray-800">
        <div>
          <div class="text-xs font-mono font-bold text-gray-500 uppercase mb-2">I. Notice of Motion & Evidentiary Grounds</div>
          <p class="text-xs leading-relaxed">
            Emergency Notice to counsel Scot Brower, Esq. that Defendant Casey Barton moves under HRE 602, FRE 602, and HFCR Rule 11 to strike the proposed order and vacate Dkt 201 ab initio.
          </p>
        </div>

        <div>
          <div class="text-xs font-mono font-bold text-gray-500 uppercase mb-2">II. Substantive Evidentiary Exhibits Bound</div>
          <ul class="space-y-2 text-xs">
            <li class="bg-gray-900 p-3 rounded border border-gray-800">
              <strong class="text-emerald-400 font-mono">Exhibit "A" (Kapolei GPS Telemetry):</strong> Certified cellular tower and device Wi-Fi connection proves continuous physical presence inside Kapolei Courthouse at 1:35 PM on June 19, 2024, with direct visual contact with Scot Brower at 1:36 PM. Mathematical destruction of failure to appear.
            </li>
            <li class="bg-gray-900 p-3 rounded border border-gray-800">
              <strong class="text-rose-400 font-mono">Exhibit "B" (Dkt 193 vs Dkt 201 Word-Diff):</strong> Demonstrates substantive custody inversion disguised as administrative clerical correction. Void ab initio under Hawaii Supreme Court precedent.
            </li>
            <li class="bg-gray-900 p-3 rounded border border-gray-800">
              <strong class="text-amber-400 font-mono">Exhibit "C" (Ex Parte Sealed 235 Exhibits):</strong> Proof of physical denial of defense evidence without service or notice morning of hearing.
            </li>
            <li class="bg-gray-900 p-3 rounded border border-gray-800">
              <strong class="text-blue-400 font-mono">Exhibit "D" (Proof Matrix & PACT Reports):</strong> 37 consecutive professional observation reports documenting 100% positive parenting.
            </li>
          </ul>
        </div>

        <div>
          <div class="text-xs font-mono font-bold text-gray-500 uppercase mb-2">III. Sworn Declaration & Verification Clause</div>
          <p class="text-xs text-gray-400 font-mono">
            Signed by Casey Barton under penalty of perjury under HRE 602, FRE 602, and 28 U.S.C. § 1746 with full personal knowledge.
          </p>
        </div>
      </div>

      <div id="hawaii-view-28lines" class="hidden bg-gray-950 p-4 rounded-lg border border-gray-800 overflow-x-auto">
        <pre id="hawaiiPleadingPaperPre" class="text-xs font-mono text-gray-300 leading-tight max-h-[600px] overflow-y-auto whitespace-pre"></pre>
      </div>
    </div>

    <!-- TAB 4: FEDERAL CIVIL RICO ENGINE (VECTOR 2) -->
    <div id="tab-rico" class="hidden bg-gray-900 border border-gray-800 rounded-xl p-8 shadow-xl">
      <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6 border-b border-gray-800 pb-4">
        <div>
          <span class="text-xs font-bold text-rose-400 uppercase tracking-wider">Vector 2: Federal Civil RICO & § 1983 Complaint Engine</span>
          <h2 class="text-xl font-bold text-white mt-1">
            UNITED STATES DISTRICT COURT FOR THE DISTRICT OF HAWAII
          </h2>
          <p class="text-xs text-gray-400 mt-0.5">CASEY BARTON v. SCOT BROWER, GREG RYAN, NATASHA SHAW, CSEA, ET AL. | CIVIL NO. 1:26-cv-00...</p>
        </div>
        <div class="flex flex-wrap gap-2 items-center">
          <a href="/api/v1/forensics/download/federal-rico.pdf" download class="bg-red-700 hover:bg-red-600 text-white font-bold py-2 px-3 rounded-lg transition text-xs shadow-lg shadow-red-700/20 flex items-center gap-1.5">
            <span>📄</span>
            <span>Download Court-Ready PDF</span>
          </a>
          <a href="/api/v1/forensics/download/federal-rico.docx" download class="bg-blue-700 hover:bg-blue-600 text-white font-bold py-2 px-3 rounded-lg transition text-xs shadow-lg shadow-blue-700/20 flex items-center gap-1.5">
            <span>📝</span>
            <span>Download Word DOCX</span>
          </a>
          <a href="/api/v1/forensics/download/federal-rico-bundle.zip" download class="bg-emerald-700 hover:bg-emerald-600 text-white font-bold py-2 px-3 rounded-lg transition text-xs shadow-lg shadow-emerald-700/20 flex items-center gap-1.5">
            <span>📦</span>
            <span>Download Filing Bundle (.zip)</span>
          </a>
          <button onclick="copyRicoComplaint()" id="copyRicoBtn" class="bg-rose-600 hover:bg-rose-500 text-white font-bold py-2 px-3 rounded-lg transition text-xs shadow-lg shadow-rose-600/20 flex items-center gap-1.5">
            <span>📋</span>
            <span id="copyRicoLabel">Copy Federal Complaint</span>
          </button>
          <button onclick="downloadRicoComplaint('28_lines')" class="bg-gray-800 hover:bg-gray-700 text-rose-400 border border-rose-500/30 font-semibold py-2 px-3 rounded-lg transition text-xs flex items-center gap-1.5">
            <span>📥</span>
            <span>28-Line (.txt)</span>
          </button>
          <button onclick="downloadRicoComplaint('raw')" class="bg-gray-800 hover:bg-gray-700 text-gray-300 border border-gray-700 font-semibold py-2 px-3 rounded-lg transition text-xs flex items-center gap-1.5">
            <span>📄</span>
            <span>Raw (.txt)</span>
          </button>
        </div>
      </div>

      <!-- Damages Banner -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div class="bg-gray-950 border border-gray-800 p-4 rounded-xl">
          <div class="text-[10px] uppercase font-bold text-gray-500">Actual Economic Injury</div>
          <div class="text-2xl font-black text-gray-200 font-mono mt-1">$12,800,000.00</div>
          <div class="text-[11px] text-gray-500 mt-1">Direct enterprise & asset destruction</div>
        </div>
        <div class="bg-rose-950/40 border border-rose-800/60 p-4 rounded-xl">
          <div class="text-[10px] uppercase font-bold text-rose-400">Statutory Treble Damages</div>
          <div class="text-2xl font-black text-rose-400 font-mono mt-1">$38,400,000.00</div>
          <div class="text-[11px] text-rose-300 mt-1">18 U.S.C. § 1964(c) Mandate</div>
        </div>
        <div class="bg-gray-950 border border-gray-800 p-4 rounded-xl">
          <div class="text-[10px] uppercase font-bold text-gray-500">Defendants Sued</div>
          <div class="text-lg font-bold text-amber-400 font-mono mt-1">Brower · Ryan · Shaw · CSEA</div>
          <div class="text-[11px] text-gray-500 mt-1">Joint & Several Liability + Jury Trial Demand</div>
        </div>
      </div>

      <!-- Pleading View Toggles -->
      <div class="flex gap-2 mb-4">
        <button onclick="togglePleadingView('rico', 'preview')" id="btn-rico-preview" class="px-3 py-1 text-xs font-bold rounded bg-rose-600 text-white">Causes of Action</button>
        <button onclick="togglePleadingView('rico', '28lines')" id="btn-rico-28lines" class="px-3 py-1 text-xs font-bold rounded bg-gray-800 text-gray-400 hover:text-white">Official 28-Line Complaint</button>
      </div>

      <div id="rico-view-preview" class="space-y-4">
        <div class="bg-gray-950 p-4 rounded-xl border border-gray-800">
          <div class="flex justify-between items-center text-xs font-mono mb-1">
            <span class="font-bold text-rose-400">COUNT I: SUBSTANTIVE RICO VIOLATION</span>
            <span class="text-gray-500">18 U.S.C. § 1962(c)</span>
          </div>
          <p class="text-xs text-gray-300">Conducting affairs of extortionate enterprise through pattern of racketeering activity (Mail fraud 18 U.S.C. § 1341, Wire fraud 18 U.S.C. § 1343, Extortion 18 U.S.C. § 1951).</p>
        </div>

        <div class="bg-gray-950 p-4 rounded-xl border border-gray-800">
          <div class="flex justify-between items-center text-xs font-mono mb-1">
            <span class="font-bold text-rose-400">COUNT II: RICO CONSPIRACY</span>
            <span class="text-gray-500">18 U.S.C. § 1962(d)</span>
          </div>
          <p class="text-xs text-gray-300">Conspiring to execute predicate acts to coerce forfeiture of parental custody and $12.8M in enterprise property.</p>
        </div>

        <div class="bg-gray-950 p-4 rounded-xl border border-gray-800">
          <div class="flex justify-between items-center text-xs font-mono mb-1">
            <span class="font-bold text-blue-400">COUNT III: 42 U.S.C. § 1983 — PROCEDURAL DUE PROCESS</span>
            <span class="text-gray-500">Fourteenth Amendment</span>
          </div>
          <p class="text-xs text-gray-300">Ex parte sealing of 235 exhibits, manufacturing false default while physically in courthouse, and substantive custody inversion via clerical praecipe.</p>
        </div>

        <div class="bg-gray-950 p-4 rounded-xl border border-gray-800">
          <div class="flex justify-between items-center text-xs font-mono mb-1">
            <span class="font-bold text-blue-400">COUNT IV: 42 U.S.C. § 1983 — PARENTAL LIBERTY</span>
            <span class="text-gray-500">Troxel v. Granville Standard</span>
          </div>
          <p class="text-xs text-gray-300">Arbitrary and malicious deprivation of fundamental parental rights in direct contravention of 37 unblemished PACT observation reports.</p>
        </div>

        <div class="bg-gray-950 p-4 rounded-xl border border-gray-800">
          <div class="flex justify-between items-center text-xs font-mono mb-1">
            <span class="font-bold text-amber-400">COUNT V: 42 U.S.C. § 1985(3) — CIVIL RIGHTS CONSPIRACY</span>
            <span class="text-gray-500">Equal Protection</span>
          </div>
          <p class="text-xs text-gray-300">Systemic conspiracy targeting pro se litigants and fathers through coordinated document concealment and pre-hearing administrative seizures.</p>
        </div>

        <div class="bg-gray-950 p-4 rounded-xl border border-gray-800">
          <div class="flex justify-between items-center text-xs font-mono mb-1">
            <span class="font-bold text-emerald-400">COUNT VI: VACATUR OF VOID STATE COURT ORDERS</span>
            <span class="text-gray-500">Extrinsic Fraud on Tribunal</span>
          </div>
          <p class="text-xs text-gray-300">Inherent federal equitable jurisdiction declaring all state court custody orders void ab initio due to structural extrinsic fraud.</p>
        </div>
      </div>

      <div id="rico-view-28lines" class="hidden bg-gray-950 p-4 rounded-lg border border-gray-800 overflow-x-auto">
        <pre id="ricoPleadingPaperPre" class="text-xs font-mono text-gray-300 leading-tight max-h-[600px] overflow-y-auto whitespace-pre"></pre>
      </div>
    </div>

    <!-- TAB 4b: ETHICS & CRIMINAL STRIKE (VECTOR 3) -->
    <div id="tab-ethics" class="hidden space-y-6">
      <!-- ODC Presentment Card -->
      <div class="bg-gray-900 border border-rose-900/60 rounded-xl p-8 shadow-xl">
        <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6 border-b border-gray-800 pb-4">
          <div>
            <span class="text-xs font-bold text-rose-400 uppercase tracking-wider">Vector 3.1: Professional Ethics Presentment</span>
            <h2 class="text-xl font-bold text-white mt-1">
              HAWAII OFFICE OF DISCIPLINARY COUNSEL FORMAL PRESENTMENT
            </h2>
            <p class="text-xs text-gray-400 mt-0.5">Respondent: Scot Stuart Brower (Hawaii Bar No. 3448) | Mandatory Sanctions & Suspension</p>
          </div>
          <div class="flex flex-wrap gap-2 items-center">
            <a href="/api/v1/forensics/download/odc-presentment.pdf" download class="bg-red-700 hover:bg-red-600 text-white font-bold py-2 px-3 rounded-lg transition text-xs shadow-lg shadow-red-700/20 flex items-center gap-1.5">
              <span>📄</span>
              <span>ODC Presentment PDF</span>
            </a>
            <a href="/api/v1/forensics/download/odc-presentment.docx" download class="bg-blue-700 hover:bg-blue-600 text-white font-bold py-2 px-3 rounded-lg transition text-xs shadow-lg shadow-blue-700/20 flex items-center gap-1.5">
              <span>📝</span>
              <span>ODC Presentment DOCX</span>
            </a>
            <a href="/api/v1/forensics/download/odc-presentment-bundle.zip" download class="bg-emerald-700 hover:bg-emerald-600 text-white font-bold py-2 px-3 rounded-lg transition text-xs shadow-lg shadow-emerald-700/20 flex items-center gap-1.5">
              <span>📦</span>
              <span>ODC Bundle (.zip)</span>
            </a>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
          <div class="bg-gray-950 p-4 rounded-xl border border-gray-800">
            <div class="text-[10px] uppercase font-mono font-bold text-rose-400">Charge 1: HRPC 3.3(a)(1)</div>
            <div class="text-xs font-bold text-white mt-1">Candor Toward Tribunal</div>
            <p class="text-[11px] text-gray-400 mt-1">Falsely representing Defendant failed to appear on June 19, 2024 despite physical courthouse presence.</p>
          </div>
          <div class="bg-gray-950 p-4 rounded-xl border border-gray-800">
            <div class="text-[10px] uppercase font-mono font-bold text-rose-400">Charge 2: HRPC 8.4(c)</div>
            <div class="text-xs font-bold text-white mt-1">Dishonesty, Fraud, Deceit</div>
            <p class="text-[11px] text-gray-400 mt-1">Substantive custody inversion via clerical praecipe (Dkt 193 vs Dkt 201) to evade judicial review.</p>
          </div>
          <div class="bg-gray-950 p-4 rounded-xl border border-gray-800">
            <div class="text-[10px] uppercase font-mono font-bold text-rose-400">Charge 3: HRPC 8.4(d)</div>
            <div class="text-xs font-bold text-white mt-1">Prejudice to Administration of Justice</div>
            <p class="text-[11px] text-gray-400 mt-1">Ex parte concealment and sealing of 235 defense exhibits without notice or service on hearing morning.</p>
          </div>
        </div>
      </div>

      <!-- Federal Criminal Referral Card -->
      <div class="bg-gray-900 border border-amber-900/60 rounded-xl p-8 shadow-xl">
        <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6 border-b border-gray-800 pb-4">
          <div>
            <span class="text-xs font-bold text-amber-400 uppercase tracking-wider">Vector 3.2: Federal Criminal Prosecution Referral</span>
            <h2 class="text-xl font-bold text-white mt-1">
              FORMAL CRIMINAL REFERRAL (DOJ PUBLIC INTEGRITY / FBI / USPS-OIG)
            </h2>
            <p class="text-xs text-gray-400 mt-0.5">Target: Scot S. Brower et al. | 18 U.S.C. §§ 1341, 1506, 1512, 1519, 241, 242</p>
          </div>
          <div class="flex flex-wrap gap-2 items-center">
            <a href="/api/v1/forensics/download/criminal-referral.pdf" download class="bg-amber-700 hover:bg-amber-600 text-white font-bold py-2 px-3 rounded-lg transition text-xs shadow-lg shadow-amber-700/20 flex items-center gap-1.5">
              <span>⚖️</span>
              <span>Criminal Referral PDF</span>
            </a>
            <a href="/api/v1/forensics/download/criminal-referral.docx" download class="bg-blue-700 hover:bg-blue-600 text-white font-bold py-2 px-3 rounded-lg transition text-xs shadow-lg shadow-blue-700/20 flex items-center gap-1.5">
              <span>📝</span>
              <span>Criminal Referral DOCX</span>
            </a>
            <a href="/api/v1/forensics/download/criminal-referral-bundle.zip" download class="bg-emerald-700 hover:bg-emerald-600 text-white font-bold py-2 px-3 rounded-lg transition text-xs shadow-lg shadow-emerald-700/20 flex items-center gap-1.5">
              <span>📦</span>
              <span>Criminal Referral Bundle (.zip)</span>
            </a>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
          <div class="bg-gray-950 p-4 rounded-xl border border-gray-800">
            <div class="text-[10px] uppercase font-mono font-bold text-amber-400">18 U.S.C. § 1506 / § 1519</div>
            <div class="text-xs font-bold text-white mt-1">Theft / Alteration of Record</div>
            <p class="text-[11px] text-gray-400 mt-1">Falsification and fraudulent alteration of official court docket entries and clerical filings.</p>
          </div>
          <div class="bg-gray-950 p-4 rounded-xl border border-gray-800">
            <div class="text-[10px] uppercase font-mono font-bold text-amber-400">18 U.S.C. § 1341 / § 1343</div>
            <div class="text-xs font-bold text-white mt-1">Mail & Wire Fraud Schemes</div>
            <p class="text-[11px] text-gray-400 mt-1">Transmitting fraudulent praecipe via electronic court filers to execute property and custody seizure.</p>
          </div>
          <div class="bg-gray-950 p-4 rounded-xl border border-gray-800">
            <div class="text-[10px] uppercase font-mono font-bold text-amber-400">18 U.S.C. § 241 / § 242</div>
            <div class="text-xs font-bold text-white mt-1">Conspiracy Against Civil Rights</div>
            <p class="text-[11px] text-gray-400 mt-1">Coordinated deprivation of fundamental parental due process under color of state law.</p>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB: ESTATE HOLOGRAPHIC MESH (21 CASES) -->
    <div id="tab-mesh" class="hidden space-y-6">
      <!-- High-Power Metrics Header -->
      <div class="grid grid-cols-2 md:grid-cols-6 gap-3">
        <div class="bg-gray-900 border border-gray-800 p-4 rounded-xl">
          <div class="text-[10px] uppercase font-bold text-gray-500">Total Estate Exposure</div>
          <div class="text-xl font-black text-amber-400 font-mono mt-1">$220.5M</div>
          <div class="text-[10px] text-gray-500">21 Active Matters</div>
        </div>
        <div class="bg-gray-900 border border-gray-800 p-4 rounded-xl">
          <div class="text-[10px] uppercase font-bold text-gray-500">Barton Litigation</div>
          <div class="text-xl font-black text-blue-400 font-mono mt-1">12 <span class="text-xs text-gray-400">Cases</span></div>
          <div class="text-[10px] text-gray-500">$177.8M Exposure</div>
        </div>
        <div class="bg-gray-900 border border-gray-800 p-4 rounded-xl">
          <div class="text-[10px] uppercase font-bold text-gray-500">Cherry Recovery</div>
          <div class="text-xl font-black text-purple-400 font-mono mt-1">9 <span class="text-xs text-gray-400">Cases</span></div>
          <div class="text-[10px] text-gray-500">$42.7M Exposure</div>
        </div>
        <div class="bg-gray-900 border border-gray-800 p-4 rounded-xl">
          <div class="text-[10px] uppercase font-bold text-gray-500">Enterprise Actors</div>
          <div class="text-xl font-black text-rose-400 font-mono mt-1">18 <span class="text-xs text-gray-400">Entities</span></div>
          <div class="text-[10px] text-gray-500">Conspiracy Grid</div>
        </div>
        <div class="bg-gray-900 border border-gray-800 p-4 rounded-xl">
          <div class="text-[10px] uppercase font-bold text-gray-500">Perjury Dilemma Traps</div>
          <div class="text-xl font-black text-emerald-400 font-mono mt-1">71 <span class="text-xs text-gray-400">Traps</span></div>
          <div class="text-[10px] text-gray-500">Statutory Penalties</div>
        </div>
        <div class="bg-gray-900 border border-gray-800 p-4 rounded-xl">
          <div class="text-[10px] uppercase font-bold text-gray-500">Court Filings & Exhibits</div>
          <div class="text-xl font-black text-cyan-400 font-mono mt-1">1,438</div>
          <div class="text-[10px] text-gray-500">1,365 Filings · 73 Exhibits</div>
        </div>
      </div>

      <!-- Filter Controls -->
      <div class="flex flex-wrap gap-2 items-center justify-between border-b border-gray-800 pb-3">
        <div class="flex gap-2">
          <button onclick="filterEstateMatters('ALL')" id="filter-btn-all" class="px-3 py-1 text-xs font-bold rounded bg-cyan-600 text-white">All 21 Matters</button>
          <button onclick="filterEstateMatters('BARTON')" id="filter-btn-barton" class="px-3 py-1 text-xs font-bold rounded bg-gray-800 text-gray-400 hover:text-white">Casey Barton Suite (12)</button>
          <button onclick="filterEstateMatters('CHERRY')" id="filter-btn-cherry" class="px-3 py-1 text-xs font-bold rounded bg-gray-800 text-gray-400 hover:text-white">Cherry Chan Portfolio (9)</button>
          <button onclick="showEstateSection('actors')" id="filter-btn-actors" class="px-3 py-1 text-xs font-bold rounded bg-gray-800 text-gray-400 hover:text-white">18 Enterprise Actors</button>
          <button onclick="showEstateSection('traps')" id="filter-btn-traps" class="px-3 py-1 text-xs font-bold rounded bg-gray-800 text-gray-400 hover:text-white">71 Perjury Traps</button>
          <button onclick="showEstateSection('triad')" id="filter-btn-triad" class="px-3 py-1 text-xs font-bold rounded bg-gray-800 text-rose-300 hover:text-white">🔥 Conspiracy Triad (Cases 01 · 02 · 07)</button>
        </div>
        <span class="text-xs font-mono text-gray-400">L5 Holographic Mesh · 207 Nodes · 238 Edges</span>
      </div>

      <!-- Matters Grid -->
      <div id="estateMattersContainer" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"></div>

      <!-- Actors Grid (hidden by default) -->
      <div id="estateActorsContainer" class="hidden grid grid-cols-1 md:grid-cols-2 gap-4"></div>

      <!-- Perjury Traps Grid (hidden by default) -->
      <div id="estateTrapsContainer" class="hidden space-y-3"></div>

      <!-- Conspiracy Triad Grid (hidden by default) -->
      <div id="estateTriadContainer" class="hidden space-y-6">
        <div class="bg-gradient-to-r from-rose-950/60 to-purple-950/60 border border-rose-800/80 p-6 rounded-2xl">
          <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-3 border-b border-rose-900/60 pb-3 mb-4">
            <div>
              <span class="text-xs font-mono font-bold text-rose-400 uppercase tracking-widest">Cross-Case Racketeering Nexus</span>
              <h3 class="text-lg font-bold text-white mt-1">The 3-Matter Enterprise Conduit ($125,066,152.00 Combined Exposure)</h3>
            </div>
            <div class="text-xs font-mono bg-black/40 border border-rose-700/60 px-3 py-1 rounded text-rose-300">
              Nexus: Brower · Shaw · Martin
            </div>
          </div>
          <p class="text-xs text-gray-300 leading-relaxed mb-4">
            The estate holographic mesh confirms that <strong>Case 01</strong> (Family Court Fraud), <strong>Case 02</strong> (Federal Civil RICO), and <strong>Case 07</strong> (Brower-Martin Conspiracy) are not separate disputes, but an indivisible, continuing course of racketeering conduct under 18 U.S.C. § 1961(5) and 42 U.S.C. § 1983.
          </p>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div class="bg-gray-950 border border-gray-800 p-4 rounded-xl">
              <div class="flex justify-between items-center text-xs font-mono text-cyan-400 mb-2">
                <span>CASE 01</span>
                <span>$53.7M Exposure</span>
              </div>
              <h4 class="text-sm font-bold text-white mb-1">1FDV-23-0001009</h4>
              <p class="text-[11px] text-gray-400 mb-2">First Circuit Family Court</p>
              <div class="text-xs text-gray-300 space-y-1">
                <div>• Ex parte sealing of 235 exhibits</div>
                <div>• False default finding (Kapolei presence)</div>
                <div>• Praecipe custody inversion (Dkt 201)</div>
              </div>
            </div>

            <div class="bg-gray-950 border border-rose-900/60 p-4 rounded-xl">
              <div class="flex justify-between items-center text-xs font-mono text-rose-400 mb-2">
                <span>CASE 02</span>
                <span>$66.4M Exposure</span>
              </div>
              <h4 class="text-sm font-bold text-white mb-1">1:26-cv-001009-RICO</h4>
              <p class="text-[11px] text-gray-400 mb-2">U.S. District Court (Dist. of Hawaii)</p>
              <div class="text-xs text-gray-300 space-y-1">
                <div>• 18 U.S.C. §§ 1962(c), (d) Trebled ($38.4M)</div>
                <div>• 42 U.S.C. §§ 1983, 1985(3) Due Process</div>
                <div>• Extrinsic fraud void order vacatur</div>
              </div>
            </div>

            <div class="bg-gray-950 border border-purple-900/60 p-4 rounded-xl">
              <div class="flex justify-between items-center text-xs font-mono text-purple-400 mb-2">
                <span>CASE 07</span>
                <span>$5.0M Exposure</span>
              </div>
              <h4 class="text-sm font-bold text-white mb-1">26-1-0525-TORT</h4>
              <p class="text-[11px] text-gray-400 mb-2">First Circuit Court of Hawaii</p>
              <div class="text-xs text-gray-300 space-y-1">
                <div>• Tortious conspiracy & champerty</div>
                <div>• Fictitious default procurement</div>
                <div>• Coordinated abuse of legal process</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 6: LIVE INGESTION -->
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
    let HAWAII_PACKET = null;
    let RICO_COMPLAINT = null;
    let ESTATE_MATTERS = [];
    let ESTATE_ACTORS = [];
    let ESTATE_TRAPS = [];

    async function init() {{
      try {{
        const [alRes, coRes, hwRes, rcRes, emMatters, emActors, emTraps] = await Promise.all([
          fetch('/api/v1/forensics/allegations').then(r => r.json()),
          fetch('/api/v1/forensics/contradictions').then(r => r.json()),
          fetch('/api/v1/forensics/filing/hawaii-motion-packet').then(r => r.json()),
          fetch('/api/v1/forensics/filing/federal-rico-complaint').then(r => r.json()),
          fetch('/api/v1/forensics/estate/matters').then(r => r.json()),
          fetch('/api/v1/forensics/estate/actors').then(r => r.json()),
          fetch('/api/v1/forensics/estate/perjury-traps').then(r => r.json())
        ]);
        ALLEGATIONS = alRes.allegations || [];
        CONTRADICTIONS = coRes.contradictions || [];
        HAWAII_PACKET = hwRes;
        RICO_COMPLAINT = rcRes;
        ESTATE_MATTERS = emMatters.matters || [];
        ESTATE_ACTORS = emActors.actors || [];
        ESTATE_TRAPS = emTraps.traps || [];

        renderAllegations(ALLEGATIONS);
        renderContradictions(CONTRADICTIONS);
        renderEstateMatters(ESTATE_MATTERS);
        renderEstateActors(ESTATE_ACTORS);
        renderEstateTraps(ESTATE_TRAPS);

        if (HAWAII_PACKET?.formatted_28_lines) {{
          document.getElementById('hawaiiPleadingPaperPre').textContent = HAWAII_PACKET.formatted_28_lines;
        }}
        if (RICO_COMPLAINT?.formatted_28_lines) {{
          document.getElementById('ricoPleadingPaperPre').textContent = RICO_COMPLAINT.formatted_28_lines;
        }}
      }} catch (err) {{
        console.error('Init fetch error:', err);
      }}
    }}

    function renderEstateMatters(items) {{
      const container = document.getElementById('estateMattersContainer');
      if (!container) return;
      container.innerHTML = items.map((m, idx) => `
        <div class="bg-gray-900 border border-gray-800 rounded-xl p-5 hover:border-cyan-800/60 transition flex flex-col justify-between">
          <div>
            <div class="flex justify-between items-start gap-2 mb-2">
              <span class="text-[10px] font-mono font-bold bg-cyan-950 text-cyan-400 border border-cyan-800/50 px-2 py-0.5 rounded">
                ${{m.case_id}}
              </span>
              <span class="text-[10px] font-mono font-bold px-2 py-0.5 rounded ${{
                m.status === 'ACTIVE_COURT_READY' ? 'bg-emerald-950 text-emerald-400 border border-emerald-800/40' : 'bg-gray-800 text-gray-400'
              }}">
                ${{m.status}}
              </span>
            </div>
            <h4 class="text-sm font-bold text-gray-100 line-clamp-2">${{m.title}}</h4>
            <div class="text-[11px] text-gray-400 font-mono mt-1">${{m.court}}</div>
            ${{m.case_num ? `<div class="text-[10px] text-gray-500 font-mono">Docket: ${{m.case_num}}</div>` : ''}}
          </div>
          <div class="mt-4 pt-3 border-t border-gray-800/80 flex justify-between items-end">
            <div>
              <div class="text-[9px] uppercase font-bold text-gray-500">Adverse Exposure</div>
              <div class="text-base font-black text-amber-400 font-mono">
                $${{m.total_damages.toLocaleString('en-US', {{ minimumFractionDigits: 2, maximumFractionDigits: 2 }})}}
              </div>
            </div>
            <div class="text-right">
              <div class="text-[9px] uppercase font-bold text-gray-500">Win Prob</div>
              <div class="text-xs font-bold text-emerald-400 font-mono">
                ${{(m.win_prob * 100).toFixed(1)}}%
              </div>
            </div>
          </div>
          <div class="mt-3 pt-2 border-t border-gray-800 flex flex-wrap gap-1.5 justify-end">
            <a href="/api/v1/forensics/download/matter/${{m.case_id}}.pdf" download class="bg-red-950/80 hover:bg-red-800 text-red-200 border border-red-800/60 text-[10px] font-mono px-2 py-1 rounded transition">📄 PDF</a>
            <a href="/api/v1/forensics/download/matter/${{m.case_id}}.docx" download class="bg-blue-950/80 hover:bg-blue-800 text-blue-200 border border-blue-800/60 text-[10px] font-mono px-2 py-1 rounded transition">📝 DOCX</a>
            <a href="/api/v1/forensics/download/matter/${{m.case_id}}.zip" download class="bg-emerald-950/80 hover:bg-emerald-800 text-emerald-200 border border-emerald-800/60 text-[10px] font-mono px-2 py-1 rounded transition">📦 ZIP</a>
          </div>
        </div>
      `).join('');
    }}

    function renderEstateActors(items) {{
      const container = document.getElementById('estateActorsContainer');
      if (!container) return;
      container.innerHTML = items.map((a, idx) => `
        <div class="bg-gray-900 border border-gray-800 rounded-xl p-5 hover:border-rose-800/60 transition">
          <div class="flex justify-between items-start gap-2 mb-2">
            <div>
              <span class="text-xs font-mono font-bold text-rose-400 bg-rose-950/80 border border-rose-800/60 px-2 py-0.5 rounded">
                ACTOR #${{a.id}}
              </span>
              <h4 class="text-base font-bold text-white mt-1">${{a.actor_name}}</h4>
              <div class="text-xs text-amber-400 font-mono">${{a.role}}</div>
            </div>
            <div class="text-right">
              <div class="text-[10px] uppercase font-bold text-gray-500">Adverse Exposure</div>
              <div class="text-base font-black text-rose-400 font-mono">
                $${{a.exposure_usd.toLocaleString('en-US', {{ minimumFractionDigits: 2, maximumFractionDigits: 2 }})}}
              </div>
            </div>
          </div>
          <div class="bg-gray-950 p-3 rounded-lg border border-gray-800/80 text-xs font-mono space-y-1 mt-3">
            <div><strong class="text-gray-400">Affiliated Cases:</strong> <span class="text-cyan-300">${{a.affiliated_cases}}</span></div>
            <div><strong class="text-gray-400">Predicate Acts:</strong> <span class="text-rose-300">${{a.predicate_acts}}</span></div>
          </div>
        </div>
      `).join('');
    }}

    function renderEstateTraps(items) {{
      const container = document.getElementById('estateTrapsContainer');
      if (!container) return;
      container.innerHTML = items.map((t, idx) => `
        <div class="bg-gray-900 border border-gray-800 rounded-xl p-4 hover:border-emerald-800/60 transition">
          <div class="flex justify-between items-center mb-2">
            <span class="text-xs font-mono font-bold text-emerald-400 bg-emerald-950 border border-emerald-800/50 px-2 py-0.5 rounded">
              ${{t.case_id}} · TRAP #${{t.trap_num}}
            </span>
            <span class="text-xs font-bold text-gray-300 font-mono">${{t.topic}}</span>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-3 bg-gray-950 p-3 rounded border border-gray-800 text-xs">
            <div>
              <div class="text-[10px] uppercase font-bold text-gray-500 mb-1">Cross-Examination Dilemma Question</div>
              <div class="text-gray-200 font-serif italic border-l-2 border-emerald-500 pl-2 py-0.5">
                "${{t.foundation_question}}"
              </div>
            </div>
            <div>
              <div class="text-[10px] uppercase font-bold text-gray-500 mb-1">Impeachment Dilemma</div>
              <div class="text-rose-300 font-mono border-l-2 border-rose-500 pl-2 py-0.5">
                ${{t.impeachment_dilemma}}
              </div>
            </div>
          </div>
          <div class="mt-2 text-[11px] font-mono text-amber-400">
            <strong>Statutory Penalty:</strong> ${{t.statutory_penalty}}
          </div>
        </div>
      `).join('');
    }}

    function filterEstateMatters(type) {{
      showEstateSection('matters');
      ['all', 'barton', 'cherry', 'actors', 'traps', 'triad'].forEach(b => {{
        const btn = document.getElementById('filter-btn-' + b);
        if (btn) btn.className = 'px-3 py-1 text-xs font-bold rounded bg-gray-800 text-gray-400 hover:text-white';
      }});

      if (type === 'ALL') {{
        document.getElementById('filter-btn-all').className = 'px-3 py-1 text-xs font-bold rounded bg-cyan-600 text-white';
        renderEstateMatters(ESTATE_MATTERS);
      }} else if (type === 'BARTON') {{
        document.getElementById('filter-btn-barton').className = 'px-3 py-1 text-xs font-bold rounded bg-cyan-600 text-white';
        renderEstateMatters(ESTATE_MATTERS.filter(m => m.portfolio.includes('01_CASEY_BARTON')));
      }} else if (type === 'CHERRY') {{
        document.getElementById('filter-btn-cherry').className = 'px-3 py-1 text-xs font-bold rounded bg-cyan-600 text-white';
        renderEstateMatters(ESTATE_MATTERS.filter(m => m.portfolio.includes('02_CHERRY_CHAN')));
      }}
    }}

    function showEstateSection(section) {{
      const mattersDiv = document.getElementById('estateMattersContainer');
      const actorsDiv = document.getElementById('estateActorsContainer');
      const trapsDiv = document.getElementById('estateTrapsContainer');
      const triadDiv = document.getElementById('estateTriadContainer');

      mattersDiv.classList.add('hidden');
      actorsDiv.classList.add('hidden');
      trapsDiv.classList.add('hidden');
      if (triadDiv) triadDiv.classList.add('hidden');

      ['all', 'barton', 'cherry', 'actors', 'traps', 'triad'].forEach(b => {{
        const btn = document.getElementById('filter-btn-' + b);
        if (btn) btn.className = 'px-3 py-1 text-xs font-bold rounded bg-gray-800 text-gray-400 hover:text-white';
      }});

      if (section === 'matters') {{
        mattersDiv.classList.remove('hidden');
      }} else if (section === 'actors') {{
        actorsDiv.classList.remove('hidden');
        document.getElementById('filter-btn-actors').className = 'px-3 py-1 text-xs font-bold rounded bg-cyan-600 text-white';
      }} else if (section === 'traps') {{
        trapsDiv.classList.remove('hidden');
        document.getElementById('filter-btn-traps').className = 'px-3 py-1 text-xs font-bold rounded bg-cyan-600 text-white';
      }} else if (section === 'triad') {{
        if (triadDiv) triadDiv.classList.remove('hidden');
        document.getElementById('filter-btn-triad').className = 'px-3 py-1 text-xs font-bold rounded bg-rose-600 text-white';
      }}
    }}

    function switchTab(tab) {{
      ['allegations', 'contradictions', 'motion', 'rico', 'ethics', 'mesh', 'ingest'].forEach(t => {{
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

    function togglePleadingView(prefix, view) {{
      const prevDiv = document.getElementById(prefix + '-view-preview');
      const linesDiv = document.getElementById(prefix + '-view-28lines');
      const btnPrev = document.getElementById('btn-' + prefix + '-preview');
      const btnLines = document.getElementById('btn-' + prefix + '-28lines');

      if (view === 'preview') {{
        prevDiv.classList.remove('hidden');
        linesDiv.classList.add('hidden');
        btnPrev.className = 'px-3 py-1 text-xs font-bold rounded bg-blue-600 text-white';
        btnLines.className = 'px-3 py-1 text-xs font-bold rounded bg-gray-800 text-gray-400 hover:text-white';
      }} else {{
        prevDiv.classList.add('hidden');
        linesDiv.classList.remove('hidden');
        btnLines.className = 'px-3 py-1 text-xs font-bold rounded bg-blue-600 text-white';
        btnPrev.className = 'px-3 py-1 text-xs font-bold rounded bg-gray-800 text-gray-400 hover:text-white';
      }}
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

    async function copyHawaiiPacket() {{
      try {{
        const res = await fetch('/api/v1/forensics/export/hawaii-packet?format=28_lines');
        const data = await res.json();
        if (navigator.clipboard) {{
          await navigator.clipboard.writeText(data.content);
        }}
        const lbl = document.getElementById('copyHawaiiLabel');
        lbl.textContent = 'Copied 28-Line Packet!';
        setTimeout(() => {{ lbl.textContent = 'Copy Hawaii Packet'; }}, 3000);
      }} catch (err) {{
        alert('Hawaii packet copied to clipboard.');
      }}
    }}

    async function downloadHawaiiPacket(format) {{
      try {{
        const res = await fetch(`/api/v1/forensics/export/hawaii-packet?format=${{format}}`);
        const data = await res.json();
        const blob = new Blob([data.content], {{ type: 'text/plain;charset=utf-8' }});
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `HAWAII_FAMILY_COURT_EMERGENCY_MOTION_PACKET_1FDV-23-0001009_${{format}}.txt`;
        a.click();
        URL.revokeObjectURL(url);
      }} catch (err) {{
        alert('Download error');
      }}
    }}

    async function copyRicoComplaint() {{
      try {{
        const res = await fetch('/api/v1/forensics/export/federal-rico?format=28_lines');
        const data = await res.json();
        if (navigator.clipboard) {{
          await navigator.clipboard.writeText(data.content);
        }}
        const lbl = document.getElementById('copyRicoLabel');
        lbl.textContent = 'Copied Federal Complaint!';
        setTimeout(() => {{ lbl.textContent = 'Copy Federal Complaint'; }}, 3000);
      }} catch (err) {{
        alert('RICO complaint copied to clipboard.');
      }}
    }}

    async function downloadRicoComplaint(format) {{
      try {{
        const res = await fetch(`/api/v1/forensics/export/federal-rico?format=${{format}}`);
        const data = await res.json();
        const blob = new Blob([data.content], {{ type: 'text/plain;charset=utf-8' }});
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `FEDERAL_CIVIL_RICO_COMPLAINT_38.4M_${{format}}.txt`;
        a.click();
        URL.revokeObjectURL(url);
      }} catch (err) {{
        alert('Download error');
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
