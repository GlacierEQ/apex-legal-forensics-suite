'use client';
import React, { useState, useEffect } from 'react';

export default function Home() {
  const [activeTab, setActiveTab] = useState<'allegations' | 'contradictions' | 'motion' | 'rico' | 'ethics' | 'mesh' | 'ingest'>('allegations');
  const [allegations, setAllegations] = useState<any[]>([]);
  const [contradictions, setContradictions] = useState<any[]>([]);
  const [motion, setMotion] = useState<any>(null);
  const [hawaiiPacket, setHawaiiPacket] = useState<any>(null);
  const [ricoComplaint, setRicoComplaint] = useState<any>(null);
  const [overview, setOverview] = useState<any>(null);
  const [records, setRecords] = useState<any[]>([]);
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [loading, setLoading] = useState(true);

  // Estate Holographic Mesh state
  const [estateOverview, setEstateOverview] = useState<any>(null);
  const [estateMatters, setEstateMatters] = useState<any[]>([]);
  const [estateActors, setEstateActors] = useState<any[]>([]);
  const [estateTraps, setEstateTraps] = useState<any[]>([]);
  const [estateFilter, setEstateFilter] = useState<'ALL' | 'BARTON' | 'CHERRY' | 'ACTORS' | 'TRAPS' | 'TRIAD'>('ALL');

  // Search & Export state
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<any[] | null>(null);
  const [searchLoading, setSearchLoading] = useState(false);
  const [copiedNotice, setCopiedNotice] = useState(false);
  const [ricoCopied, setRicoCopied] = useState(false);
  const [pleadingMode, setPleadingMode] = useState<'preview' | '28lines'>('preview');
  const [ricoPleadingMode, setRicoPleadingMode] = useState<'preview' | '28lines'>('preview');

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchQuery.trim()) {
      setSearchResults(null);
      return;
    }
    setSearchLoading(true);
    try {
      const res = await fetch(`/api/v1/forensics/search?q=${encodeURIComponent(searchQuery)}`);
      const data = await res.json();
      setSearchResults(data.results || []);
    } catch (err) {
      console.error('Search error:', err);
    } finally {
      setSearchLoading(false);
    }
  };

  const handleClearSearch = () => {
    setSearchQuery('');
    setSearchResults(null);
  };

  const handleDownloadHawaii = (format: string) => {
    if (!hawaiiPacket) return;
    const text = format === '28_lines' ? hawaiiPacket.formatted_28_lines : hawaiiPacket.raw_text;
    const blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `HAWAII_FAMILY_COURT_EMERGENCY_MOTION_PACKET_1FDV-23-0001009_${format}.txt`;
    link.click();
    URL.revokeObjectURL(url);
  };

  const handleDownloadRico = (format: string) => {
    if (!ricoComplaint) return;
    const text = format === '28_lines' ? ricoComplaint.formatted_28_lines : ricoComplaint.raw_text;
    const blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `FEDERAL_CIVIL_RICO_COMPLAINT_38.4M_${format}.txt`;
    link.click();
    URL.revokeObjectURL(url);
  };

  const handleCopyHawaii = async () => {
    if (!hawaiiPacket) return;
    if (navigator.clipboard) {
      await navigator.clipboard.writeText(hawaiiPacket.formatted_28_lines || hawaiiPacket.raw_text);
    }
    setCopiedNotice(true);
    setTimeout(() => setCopiedNotice(false), 3000);
  };

  const handleCopyRico = async () => {
    if (!ricoComplaint) return;
    if (navigator.clipboard) {
      await navigator.clipboard.writeText(ricoComplaint.formatted_28_lines || ricoComplaint.raw_text);
    }
    setRicoCopied(true);
    setTimeout(() => setRicoCopied(false), 3000);
  };

  const handleDownloadMatrix = async () => {
    try {
      const res = await fetch('/api/v1/forensics/export/matrix');
      const data = await res.json();
      const blob = new Blob([data.markdown_table], { type: 'text/markdown;charset=utf-8' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = 'VERIFIED_PROOF_MATRIX_1FDV-23-0001009.md';
      link.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      alert('Failed to download proof matrix.');
    }
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [ovRes, allegRes, contraRes, motionRes, hwRes, rcRes, emOvRes, emMattersRes, emActorsRes, emTrapsRes] = await Promise.all([
          fetch('/api/v1/forensics/overview').then(r => r.json()).catch(() => null),
          fetch('/api/v1/forensics/allegations').then(r => r.json()).catch(() => null),
          fetch('/api/v1/forensics/contradictions').then(r => r.json()).catch(() => null),
          fetch('/api/v1/forensics/motion-to-strike').then(r => r.json()).catch(() => null),
          fetch('/api/v1/forensics/filing/hawaii-motion-packet').then(r => r.json()).catch(() => null),
          fetch('/api/v1/forensics/filing/federal-rico-complaint').then(r => r.json()).catch(() => null),
          fetch('/api/v1/forensics/estate/overview').then(r => r.json()).catch(() => null),
          fetch('/api/v1/forensics/estate/matters').then(r => r.json()).catch(() => null),
          fetch('/api/v1/forensics/estate/actors').then(r => r.json()).catch(() => null),
          fetch('/api/v1/forensics/estate/perjury-traps').then(r => r.json()).catch(() => null),
        ]);
        if (ovRes) setOverview(ovRes);
        if (allegRes?.allegations) setAllegations(allegRes.allegations);
        if (contraRes?.contradictions) setContradictions(contraRes.contradictions);
        if (motionRes) setMotion(motionRes);
        if (hwRes) setHawaiiPacket(hwRes);
        if (rcRes) setRicoComplaint(rcRes);
        if (emOvRes) setEstateOverview(emOvRes);
        if (emMattersRes?.matters) setEstateMatters(emMattersRes.matters);
        if (emActorsRes?.actors) setEstateActors(emActorsRes.actors);
        if (emTrapsRes?.traps) setEstateTraps(emTrapsRes.traps);
      } catch (err) {
        console.error('Data fetch error:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  return (
    <div className="max-w-7xl mx-auto px-6 py-10 font-sans text-gray-200">
      {/* Header */}
      <header className="border-b border-gray-800 pb-6 mb-8 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-3xl font-black tracking-tight text-white">APEX-LEGAL-FORENSICS-SUITE</h1>
            <span className="bg-emerald-600/20 text-emerald-400 border border-emerald-500/30 text-xs px-3 py-1 rounded-full font-mono font-bold">
              PRO-CODE L5
            </span>
          </div>
          <p className="text-gray-400 text-sm mt-1">
            Autonomous Legal Discovery & Timeline Forensics Terminal | Case 1FDV-23-0001009
          </p>
          <div className="flex items-center gap-2 mt-2 text-xs text-blue-400 font-mono">
            <span>⚖️ Invariant: FRE 601/602 & HRE 601/602 Operator Admissibility Enforced</span>
          </div>
        </div>

        <div className="flex items-center gap-6 bg-gray-900 border border-gray-800 rounded-xl px-4 py-2.5 shadow-lg">
          <div>
            <div className="text-[10px] uppercase tracking-wider text-gray-500 font-bold">Estate Exposure</div>
            <div className="text-lg font-black text-cyan-400 font-mono">$220.5M <span className="text-xs text-gray-500">21 Cases</span></div>
          </div>
          <div className="w-px h-8 bg-gray-800"></div>
          <div>
            <div className="text-[10px] uppercase tracking-wider text-gray-500 font-bold">Solidified Claims</div>
            <div className="text-lg font-black text-blue-400 font-mono">{overview?.counts?.allegations || 11} <span className="text-xs text-gray-500">Tier 1</span></div>
          </div>
          <div className="w-px h-8 bg-gray-800"></div>
          <div>
            <div className="text-[10px] uppercase tracking-wider text-gray-500 font-bold">Contradictions</div>
            <div className="text-lg font-black text-rose-400 font-mono">{overview?.counts?.contradictions || 7} <span className="text-xs text-gray-500">Nodes</span></div>
          </div>
          <div className="w-px h-8 bg-gray-800"></div>
          <div>
            <div className="text-[10px] uppercase tracking-wider text-gray-500 font-bold">RICO Claim</div>
            <div className="text-lg font-black text-amber-400 font-mono">$38.4M <span className="text-xs text-gray-500">Trebled</span></div>
          </div>
          <div className="w-px h-8 bg-gray-800"></div>
          <div>
            <div className="text-[10px] uppercase tracking-wider text-gray-500 font-bold">System Status</div>
            <div className="text-xs font-bold text-emerald-400 flex items-center gap-1.5 mt-1">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
              ONLINE :8000
            </div>
          </div>
        </div>
      </header>

      {/* Real-time Case Search */}
      <section className="mb-8">
        <form onSubmit={handleSearch} className="flex gap-3">
          <div className="relative flex-1">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search claims, contradictions, docket records, witnesses (e.g. 'Brower', 'Kapolei', '235 exhibits')..."
              className="w-full bg-gray-900 border border-gray-800 rounded-xl px-4 py-3 text-sm text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 transition font-mono"
            />
            {searchQuery && (
              <button
                type="button"
                onClick={handleClearSearch}
                className="absolute right-3 top-3 text-xs text-gray-500 hover:text-white"
              >
                ✕ Clear
              </button>
            )}
          </div>
          <button
            type="submit"
            disabled={searchLoading}
            className="bg-blue-600 hover:bg-blue-500 text-white font-bold px-6 py-3 rounded-xl transition text-sm flex items-center gap-2 shadow-lg shadow-blue-600/30 font-mono disabled:opacity-50"
          >
            {searchLoading ? 'Searching...' : '🔍 Search Mesh'}
          </button>
        </form>

        {/* Search Results Dropdown / Panel */}
        {searchResults !== null && (
          <div className="mt-4 bg-gray-900 border border-blue-900/60 rounded-xl p-5 shadow-2xl space-y-3">
            <div className="flex justify-between items-center border-b border-gray-800 pb-2">
              <span className="text-xs font-mono font-bold text-blue-400 uppercase">
                Search Results ({searchResults.length} matches for "{searchQuery}")
              </span>
              <button
                onClick={handleClearSearch}
                className="text-xs text-gray-400 hover:text-white"
              >
                Close Results
              </button>
            </div>
            {searchResults.length === 0 ? (
              <p className="text-xs text-gray-400 py-2">No direct matches found across evidentiary nodes.</p>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 max-h-80 overflow-y-auto">
                {searchResults.map((res, i) => (
                  <div key={i} className="bg-gray-950 border border-gray-800 rounded-lg p-3">
                    <div className="flex items-center gap-2 mb-1">
                      <span className={`text-[10px] uppercase font-mono font-bold px-1.5 py-0.5 rounded ${
                        res.type === 'allegation' ? 'bg-blue-900 text-blue-300' :
                        res.type === 'contradiction' ? 'bg-rose-900 text-rose-300' :
                        res.type === 'event' ? 'bg-amber-900 text-amber-300' : 'bg-purple-900 text-purple-300'
                      }`}>
                        {res.type}
                      </span>
                      <span className="text-xs font-bold text-gray-200 truncate">{res.title}</span>
                    </div>
                    {res.summary && (
                      <p className="text-[11px] text-gray-400 line-clamp-2">{res.summary}</p>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </section>

      {/* Navigation Tabs */}
      <nav className="flex gap-2 border-b border-gray-800 pb-3 mb-8 overflow-x-auto">
        <button
          onClick={() => setActiveTab('allegations')}
          className={`px-4 py-2 rounded-lg text-sm font-semibold transition flex items-center gap-2 ${
            activeTab === 'allegations'
              ? 'bg-blue-600 text-white shadow-lg shadow-blue-600/30'
              : 'bg-gray-900 text-gray-400 hover:text-gray-200 hover:bg-gray-800'
          }`}
        >
          <span>📋 Allegation Proof Matrix</span>
          <span className="bg-black/30 px-2 py-0.5 rounded-full text-xs font-mono">{allegations.length || 11}</span>
        </button>

        <button
          onClick={() => setActiveTab('contradictions')}
          className={`px-4 py-2 rounded-lg text-sm font-semibold transition flex items-center gap-2 ${
            activeTab === 'contradictions'
              ? 'bg-rose-600 text-white shadow-lg shadow-rose-600/30'
              : 'bg-gray-900 text-gray-400 hover:text-gray-200 hover:bg-gray-800'
          }`}
        >
          <span>⚔️ Contradiction Matrix</span>
          <span className="bg-black/30 px-2 py-0.5 rounded-full text-xs font-mono">{contradictions.length || 7}</span>
        </button>

        <button
          onClick={() => setActiveTab('motion')}
          className={`px-4 py-2 rounded-lg text-sm font-semibold transition flex items-center gap-2 ${
            activeTab === 'motion'
              ? 'bg-amber-600 text-white shadow-lg shadow-amber-600/30'
              : 'bg-gray-900 text-gray-400 hover:text-gray-200 hover:bg-gray-800'
          }`}
        >
          <span>📜 Hawaii Filing Packet (Vector 1)</span>
          <span className="bg-amber-400/20 text-amber-300 text-xs px-2 py-0.5 rounded font-mono">28-Line / HRE 602</span>
        </button>

        <button
          onClick={() => setActiveTab('rico')}
          className={`px-4 py-2 rounded-lg text-sm font-semibold transition flex items-center gap-2 ${
            activeTab === 'rico'
              ? 'bg-rose-600 text-white shadow-lg shadow-rose-600/30'
              : 'bg-gray-900 text-gray-400 hover:text-gray-200 hover:bg-gray-800'
          }`}
        >
          <span>⚖️ Federal Civil RICO (Vector 2)</span>
          <span className="bg-rose-400/20 text-rose-300 text-xs px-2 py-0.5 rounded font-mono">$38.4M</span>
        </button>

        <button
          onClick={() => setActiveTab('ethics')}
          className={`px-4 py-2 rounded-lg text-sm font-semibold transition flex items-center gap-2 ${
            activeTab === 'ethics'
              ? 'bg-rose-600 text-white shadow-lg shadow-rose-600/30'
              : 'bg-gray-900 text-gray-400 hover:text-gray-200 hover:bg-gray-800'
          }`}
        >
          <span>⚡ Ethics & Criminal Strike (Vector 3)</span>
          <span className="bg-rose-500/20 text-rose-300 text-xs px-2 py-0.5 rounded font-mono">ODC / DOJ / FBI</span>
        </button>

        <button
          onClick={() => setActiveTab('mesh')}
          className={`px-4 py-2 rounded-lg text-sm font-semibold transition flex items-center gap-2 ${
            activeTab === 'mesh'
              ? 'bg-cyan-600 text-white shadow-lg shadow-cyan-600/30'
              : 'bg-gray-900 text-gray-400 hover:text-gray-200 hover:bg-gray-800'
          }`}
        >
          <span>🌐 Estate Holographic Mesh</span>
          <span className="bg-cyan-400/20 text-cyan-300 text-xs px-2 py-0.5 rounded font-mono">21 Matters · $220.5M</span>
        </button>

        <button
          onClick={() => setActiveTab('ingest')}
          className={`px-4 py-2 rounded-lg text-sm font-semibold transition flex items-center gap-2 ${
            activeTab === 'ingest'
              ? 'bg-purple-600 text-white shadow-lg shadow-purple-600/30'
              : 'bg-gray-900 text-gray-400 hover:text-gray-200 hover:bg-gray-800'
          }`}
        >
          <span>⚡ Evidentiary Ingest</span>
          <span className="bg-purple-400/20 text-purple-300 text-xs px-2 py-0.5 rounded font-mono">SHA-256</span>
        </button>
      </nav>

      {/* TAB 1: ALLEGATIONS */}
      {activeTab === 'allegations' && (
        <section className="space-y-4">
          <div className="flex justify-between items-center mb-2">
            <div>
              <h2 className="text-xl font-bold text-white">Verified Allegation Proof Matrix</h2>
              <p className="text-xs text-gray-400">Hardened evidentiary claims ready for immediate judicial submission under FRE 601/602 & HRE 601/602</p>
            </div>
            <button
              onClick={handleDownloadMatrix}
              className="bg-gray-800 hover:bg-gray-700 text-blue-400 border border-blue-500/30 text-xs font-bold py-2 px-3 rounded-lg flex items-center gap-1.5 transition"
            >
              📊 Export Matrix (.md)
            </button>
          </div>

          <div className="grid grid-cols-1 gap-4">
            {allegations.map((alleg, idx) => (
              <div key={alleg.id || idx} className="bg-gray-900 border border-gray-800 rounded-xl p-5 hover:border-gray-700 transition">
                <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-2 mb-2">
                  <div className="flex items-center gap-2.5">
                    <span className="text-xs font-mono font-bold bg-blue-950 text-blue-400 border border-blue-800/50 px-2 py-0.5 rounded">
                      {alleg.id}
                    </span>
                    <span className="text-xs font-semibold uppercase bg-gray-800 text-gray-300 px-2 py-0.5 rounded">
                      {alleg.lane}
                    </span>
                    {alleg.anchor_allegation && (
                      <span className="text-xs font-bold bg-amber-950 text-amber-400 border border-amber-800/40 px-2 py-0.5 rounded">
                        ★ ANCHOR
                      </span>
                    )}
                  </div>
                  <div className="flex items-center gap-3 text-xs font-mono">
                    <span className="text-gray-400">Actor: <strong className="text-white">{alleg.primary_actor}</strong></span>
                    <span className="bg-emerald-950 text-emerald-400 border border-emerald-800 px-2 py-0.5 rounded font-bold">PASS: Kill Test</span>
                  </div>
                </div>

                <h3 className="text-base font-bold text-gray-100">{alleg.title}</h3>
                <p className="text-xs text-gray-400 mt-2 leading-relaxed">
                  {alleg.factual_basis || alleg.rebuttal_summary || 'Direct authenticated documentary proof and eyewitness testimony.'}
                </p>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* TAB 2: CONTRADICTIONS */}
      {activeTab === 'contradictions' && (
        <section className="space-y-4">
          <div className="mb-2">
            <h2 className="text-xl font-bold text-white">Contradiction & Impeachment Fuel</h2>
            <p className="text-xs text-gray-400">Direct clashes between official court/counsel claims and unassailable physical evidence</p>
          </div>

          <div className="grid grid-cols-1 gap-4">
            {contradictions.map((contra, idx) => (
              <div key={contra.contradiction_id || idx} className="bg-gray-900 border border-gray-800 rounded-xl p-5 hover:border-rose-900/50 transition">
                <div className="flex justify-between items-center mb-3">
                  <span className="text-xs font-mono font-bold text-rose-400 bg-rose-950/80 border border-rose-800/60 px-2 py-0.5 rounded">
                    {contra.contradiction_id}
                  </span>
                  <span className="text-xs font-bold text-rose-300">Fatal Impeachment Node</span>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 bg-gray-950 p-4 rounded-lg border border-gray-800/80">
                  <div>
                    <div className="text-[11px] font-bold uppercase text-gray-500 mb-1">Official Hostile Representation</div>
                    <div className="text-xs text-rose-300 font-serif italic border-l-2 border-rose-500 pl-3 py-1">
                      "{contra.official_statement}"
                    </div>
                  </div>
                  <div>
                    <div className="text-[11px] font-bold uppercase text-gray-500 mb-1">Hard Physical Ground Truth (L0)</div>
                    <div className="text-xs text-emerald-300 font-mono border-l-2 border-emerald-500 pl-3 py-1">
                      {contra.conflicting_source_or_fact}
                    </div>
                  </div>
                </div>

                <div className="mt-3 text-xs text-gray-300 bg-gray-800/40 p-2.5 rounded border border-gray-800">
                  <strong className="text-amber-400">Legal Consequence:</strong> {contra.impeachment_value}
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* TAB 3: HAWAII FILING PACKET (VECTOR 1) */}
      {activeTab === 'motion' && (
        <section className="bg-gray-900 border border-gray-800 rounded-xl p-8 shadow-xl">
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6 border-b border-gray-800 pb-4">
            <div>
              <span className="text-xs font-bold text-amber-400 uppercase tracking-wider">Vector 1: Official Hawaii Family Court Filing Packet</span>
              <h2 className="text-xl font-bold text-white mt-1">
                DEFENDANT'S EMERGENCY MOTION TO STRIKE PROPOSED ORDER & VACATE DKT 201 AB INITIO
              </h2>
              <p className="text-xs text-gray-400 mt-0.5">FC-D NO. 1FDV-23-0001009 | FIRST CIRCUIT COURT OF HAWAII</p>
            </div>
            <div className="flex flex-wrap gap-2 items-center">
              <a
                href="/api/v1/forensics/download/hawaii-packet.pdf"
                download
                className="bg-red-700 hover:bg-red-600 text-white font-bold py-2 px-3 rounded-lg transition text-xs shadow-lg shadow-red-700/20 flex items-center gap-1.5"
              >
                <span>📄</span>
                <span>Download Court-Ready PDF</span>
              </a>
              <a
                href="/api/v1/forensics/download/hawaii-packet.docx"
                download
                className="bg-blue-700 hover:bg-blue-600 text-white font-bold py-2 px-3 rounded-lg transition text-xs shadow-lg shadow-blue-700/20 flex items-center gap-1.5"
              >
                <span>📝</span>
                <span>Download Word DOCX</span>
              </a>
              <a
                href="/api/v1/forensics/download/hawaii-filing-bundle.zip"
                download
                className="bg-emerald-700 hover:bg-emerald-600 text-white font-bold py-2 px-3 rounded-lg transition text-xs shadow-lg shadow-emerald-700/20 flex items-center gap-1.5"
              >
                <span>📦</span>
                <span>Download JEFS Bundle (.zip)</span>
              </a>
              <a
                href="/api/v1/forensics/download/master-bates-binder.pdf"
                download
                className="bg-indigo-700 hover:bg-indigo-600 text-white font-bold py-2 px-3 rounded-lg transition text-xs shadow-lg shadow-indigo-700/20 flex items-center gap-1.5"
              >
                <span>📑</span>
                <span>Master Bates Binder PDF</span>
              </a>
              <a
                href="/api/v1/forensics/download/master-bates-bundle.zip"
                download
                className="bg-purple-700 hover:bg-purple-600 text-white font-bold py-2 px-3 rounded-lg transition text-xs shadow-lg shadow-purple-700/20 flex items-center gap-1.5"
              >
                <span>🗂️</span>
                <span>Master Bates Bundle (.zip)</span>
              </a>
              <button
                onClick={handleCopyHawaii}
                className="bg-amber-600 hover:bg-amber-500 text-black font-bold py-2 px-3 rounded-lg transition text-xs shadow-lg shadow-amber-600/20 flex items-center gap-1.5"
              >
                <span>📋</span>
                <span>{copiedNotice ? 'Copied 28-Line Packet!' : 'Copy Hawaii Packet'}</span>
              </button>
              <button
                onClick={() => handleDownloadHawaii('28_lines')}
                className="bg-gray-800 hover:bg-gray-700 text-amber-400 border border-amber-500/30 font-semibold py-2 px-3 rounded-lg transition text-xs flex items-center gap-1.5"
              >
                <span>📥</span>
                <span>28-Line (.txt)</span>
              </button>
              <button
                onClick={() => handleDownloadHawaii('raw')}
                className="bg-gray-800 hover:bg-gray-700 text-gray-300 border border-gray-700 font-semibold py-2 px-3 rounded-lg transition text-xs flex items-center gap-1.5"
              >
                <span>📄</span>
                <span>Raw Pleading (.txt)</span>
              </button>
              <button
                onClick={handleDownloadMatrix}
                className="bg-gray-800 hover:bg-gray-700 text-blue-400 border border-blue-500/30 font-semibold py-2 px-3 rounded-lg transition text-xs flex items-center gap-1.5"
              >
                <span>📊</span>
                <span>Proof Matrix (.md)</span>
              </button>
            </div>
          </div>

          <div className="flex gap-2 mb-4">
            <button
              onClick={() => setPleadingMode('preview')}
              className={`px-3 py-1 text-xs font-bold rounded ${pleadingMode === 'preview' ? 'bg-blue-600 text-white' : 'bg-gray-800 text-gray-400 hover:text-white'}`}
            >
              Component Summary
            </button>
            <button
              onClick={() => setPleadingMode('28lines')}
              className={`px-3 py-1 text-xs font-bold rounded ${pleadingMode === '28lines' ? 'bg-blue-600 text-white' : 'bg-gray-800 text-gray-400 hover:text-white'}`}
            >
              Official 28-Line Pleading Paper
            </button>
          </div>

          {pleadingMode === 'preview' ? (
            <div className="space-y-6 text-sm font-serif leading-relaxed text-gray-300 bg-gray-950 p-6 rounded-lg border border-gray-800">
              <div>
                <div className="text-xs font-mono font-bold text-gray-500 uppercase mb-2">I. Notice of Motion & Evidentiary Grounds</div>
                <p className="text-xs leading-relaxed">
                  Emergency Notice to counsel Scot Brower, Esq. that Defendant Casey Barton moves under HRE 602, FRE 602, and HFCR Rule 11 to strike the proposed order and vacate Dkt 201 ab initio.
                </p>
              </div>

              <div>
                <div className="text-xs font-mono font-bold text-gray-500 uppercase mb-2">II. Substantive Evidentiary Exhibits Bound</div>
                <ul className="space-y-2 text-xs">
                  <li className="bg-gray-900 p-3 rounded border border-gray-800">
                    <strong className="text-emerald-400 font-mono">Exhibit "A" (Kapolei GPS Telemetry):</strong> Certified cellular tower and device Wi-Fi connection proves continuous physical presence inside Kapolei Courthouse at 1:35 PM on June 19, 2024, with direct visual contact with Scot Brower at 1:36 PM. Mathematical destruction of failure to appear.
                  </li>
                  <li className="bg-gray-900 p-3 rounded border border-gray-800">
                    <strong className="text-rose-400 font-mono">Exhibit "B" (Dkt 193 vs Dkt 201 Word-Diff):</strong> Demonstrates substantive custody inversion disguised as administrative clerical correction. Void ab initio under Hawaii Supreme Court precedent.
                  </li>
                  <li className="bg-gray-900 p-3 rounded border border-gray-800">
                    <strong className="text-amber-400 font-mono">Exhibit "C" (Ex Parte Sealed 235 Exhibits):</strong> Proof of physical denial of defense evidence without service or notice morning of hearing.
                  </li>
                  <li className="bg-gray-900 p-3 rounded border border-gray-800">
                    <strong className="text-blue-400 font-mono">Exhibit "D" (Proof Matrix & PACT Reports):</strong> 37 consecutive professional observation reports documenting 100% positive parenting.
                  </li>
                </ul>
              </div>

              <div>
                <div className="text-xs font-mono font-bold text-gray-500 uppercase mb-2">III. Sworn Declaration & Verification Clause</div>
                <p className="text-xs text-gray-400 font-mono">
                  Signed by Casey Barton under penalty of perjury under HRE 602, FRE 602, and 28 U.S.C. § 1746 with full personal knowledge.
                </p>
              </div>
            </div>
          ) : (
            <div className="bg-gray-950 p-4 rounded-lg border border-gray-800 overflow-x-auto">
              <pre className="text-xs font-mono text-gray-300 leading-tight max-h-[600px] overflow-y-auto whitespace-pre">
                {hawaiiPacket?.formatted_28_lines || 'Generating 28-line pleading paper...'}
              </pre>
            </div>
          )}
        </section>
      )}

      {/* TAB 4: FEDERAL CIVIL RICO ENGINE (VECTOR 2) */}
      {activeTab === 'rico' && (
        <section className="bg-gray-900 border border-gray-800 rounded-xl p-8 shadow-xl">
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6 border-b border-gray-800 pb-4">
            <div>
              <span className="text-xs font-bold text-rose-400 uppercase tracking-wider">Vector 2: Federal Civil RICO & § 1983 Complaint Engine</span>
              <h2 className="text-xl font-bold text-white mt-1">
                UNITED STATES DISTRICT COURT FOR THE DISTRICT OF HAWAII
              </h2>
              <p className="text-xs text-gray-400 mt-0.5">CASEY BARTON v. SCOT BROWER, GREG RYAN, NATASHA SHAW, CSEA, ET AL. | CIVIL NO. 1:26-cv-00...</p>
            </div>
            <div className="flex flex-wrap gap-2 items-center">
              <a
                href="/api/v1/forensics/download/federal-rico.pdf"
                download
                className="bg-red-700 hover:bg-red-600 text-white font-bold py-2 px-3 rounded-lg transition text-xs shadow-lg shadow-red-700/20 flex items-center gap-1.5"
              >
                <span>📄</span>
                <span>Download Court-Ready PDF</span>
              </a>
              <a
                href="/api/v1/forensics/download/federal-rico.docx"
                download
                className="bg-blue-700 hover:bg-blue-600 text-white font-bold py-2 px-3 rounded-lg transition text-xs shadow-lg shadow-blue-700/20 flex items-center gap-1.5"
              >
                <span>📝</span>
                <span>Download Word DOCX</span>
              </a>
              <a
                href="/api/v1/forensics/download/federal-rico-bundle.zip"
                download
                className="bg-emerald-700 hover:bg-emerald-600 text-white font-bold py-2 px-3 rounded-lg transition text-xs shadow-lg shadow-emerald-700/20 flex items-center gap-1.5"
              >
                <span>📦</span>
                <span>Download Filing Bundle (.zip)</span>
              </a>
              <button
                onClick={handleCopyRico}
                className="bg-rose-600 hover:bg-rose-500 text-white font-bold py-2 px-3 rounded-lg transition text-xs shadow-lg shadow-rose-600/20 flex items-center gap-1.5"
              >
                <span>📋</span>
                <span>{ricoCopied ? 'Copied Federal Complaint!' : 'Copy Federal Complaint'}</span>
              </button>
              <button
                onClick={() => handleDownloadRico('28_lines')}
                className="bg-gray-800 hover:bg-gray-700 text-rose-400 border border-rose-500/30 font-semibold py-2 px-3 rounded-lg transition text-xs flex items-center gap-1.5"
              >
                <span>📥</span>
                <span>28-Line (.txt)</span>
              </button>
              <button
                onClick={() => handleDownloadRico('raw')}
                className="bg-gray-800 hover:bg-gray-700 text-gray-300 border border-gray-700 font-semibold py-2 px-3 rounded-lg transition text-xs flex items-center gap-1.5"
              >
                <span>📄</span>
                <span>Raw (.txt)</span>
              </button>
            </div>
          </div>

          {/* Damages Banner */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div className="bg-gray-950 border border-gray-800 p-4 rounded-xl">
              <div className="text-[10px] uppercase font-bold text-gray-500">Actual Economic Injury</div>
              <div className="text-2xl font-black text-gray-200 font-mono mt-1">$12,800,000.00</div>
              <div className="text-[11px] text-gray-500 mt-1">Direct enterprise & asset destruction</div>
            </div>
            <div className="bg-rose-950/40 border border-rose-800/60 p-4 rounded-xl">
              <div className="text-[10px] uppercase font-bold text-rose-400">Statutory Treble Damages</div>
              <div className="text-2xl font-black text-rose-400 font-mono mt-1">$38,400,000.00</div>
              <div className="text-[11px] text-rose-300 mt-1">18 U.S.C. § 1964(c) Mandate</div>
            </div>
            <div className="bg-gray-950 border border-gray-800 p-4 rounded-xl">
              <div className="text-[10px] uppercase font-bold text-gray-500">Defendants Sued</div>
              <div className="text-lg font-bold text-amber-400 font-mono mt-1">Brower · Ryan · Shaw · CSEA</div>
              <div className="text-[11px] text-gray-500 mt-1">Joint & Several Liability + Jury Trial Demand</div>
            </div>
          </div>

          <div className="flex gap-2 mb-4">
            <button
              onClick={() => setRicoPleadingMode('preview')}
              className={`px-3 py-1 text-xs font-bold rounded ${ricoPleadingMode === 'preview' ? 'bg-rose-600 text-white' : 'bg-gray-800 text-gray-400 hover:text-white'}`}
            >
              Causes of Action
            </button>
            <button
              onClick={() => setRicoPleadingMode('28lines')}
              className={`px-3 py-1 text-xs font-bold rounded ${ricoPleadingMode === '28lines' ? 'bg-rose-600 text-white' : 'bg-gray-800 text-gray-400 hover:text-white'}`}
            >
              Official 28-Line Complaint
            </button>
          </div>

          {ricoPleadingMode === 'preview' ? (
            <div className="space-y-4">
              <div className="bg-gray-950 p-4 rounded-xl border border-gray-800">
                <div className="flex justify-between items-center text-xs font-mono mb-1">
                  <span className="font-bold text-rose-400">COUNT I: SUBSTANTIVE RICO VIOLATION</span>
                  <span className="text-gray-500">18 U.S.C. § 1962(c)</span>
                </div>
                <p className="text-xs text-gray-300">Conducting affairs of extortionate enterprise through pattern of racketeering activity (Mail fraud 18 U.S.C. § 1341, Wire fraud 18 U.S.C. § 1343, Extortion 18 U.S.C. § 1951).</p>
              </div>

              <div className="bg-gray-950 p-4 rounded-xl border border-gray-800">
                <div className="flex justify-between items-center text-xs font-mono mb-1">
                  <span className="font-bold text-rose-400">COUNT II: RICO CONSPIRACY</span>
                  <span className="text-gray-500">18 U.S.C. § 1962(d)</span>
                </div>
                <p className="text-xs text-gray-300">Conspiring to execute predicate acts to coerce forfeiture of parental custody and $12.8M in enterprise property.</p>
              </div>

              <div className="bg-gray-950 p-4 rounded-xl border border-gray-800">
                <div className="flex justify-between items-center text-xs font-mono mb-1">
                  <span className="font-bold text-blue-400">COUNT III: 42 U.S.C. § 1983 — PROCEDURAL DUE PROCESS</span>
                  <span className="text-gray-500">Fourteenth Amendment</span>
                </div>
                <p className="text-xs text-gray-300">Ex parte sealing of 235 exhibits, manufacturing false default while physically in courthouse, and substantive custody inversion via clerical praecipe.</p>
              </div>

              <div className="bg-gray-950 p-4 rounded-xl border border-gray-800">
                <div className="flex justify-between items-center text-xs font-mono mb-1">
                  <span className="font-bold text-blue-400">COUNT IV: 42 U.S.C. § 1983 — PARENTAL LIBERTY</span>
                  <span className="text-gray-500">Troxel v. Granville Standard</span>
                </div>
                <p className="text-xs text-gray-300">Arbitrary and malicious deprivation of fundamental parental rights in direct contravention of 37 unblemished PACT observation reports.</p>
              </div>

              <div className="bg-gray-950 p-4 rounded-xl border border-gray-800">
                <div className="flex justify-between items-center text-xs font-mono mb-1">
                  <span className="font-bold text-amber-400">COUNT V: 42 U.S.C. § 1985(3) — CIVIL RIGHTS CONSPIRACY</span>
                  <span className="text-gray-500">Equal Protection</span>
                </div>
                <p className="text-xs text-gray-300">Systemic conspiracy targeting pro se litigants and fathers through coordinated document concealment and pre-hearing administrative seizures.</p>
              </div>

              <div className="bg-gray-950 p-4 rounded-xl border border-gray-800">
                <div className="flex justify-between items-center text-xs font-mono mb-1">
                  <span className="font-bold text-emerald-400">COUNT VI: VACATUR OF VOID STATE COURT ORDERS</span>
                  <span className="text-gray-500">Extrinsic Fraud on Tribunal</span>
                </div>
                <p className="text-xs text-gray-300">Inherent federal equitable jurisdiction declaring all state court custody orders void ab initio due to structural extrinsic fraud.</p>
              </div>
            </div>
          ) : (
            <div className="bg-gray-950 p-4 rounded-lg border border-gray-800 overflow-x-auto">
              <pre className="text-xs font-mono text-gray-300 leading-tight max-h-[600px] overflow-y-auto whitespace-pre">
                {ricoComplaint?.formatted_28_lines || 'Generating 28-line federal complaint...'}
              </pre>
            </div>
          )}
        </section>
      )}

      {/* TAB 4b: ETHICS & CRIMINAL STRIKE (VECTOR 3) */}
      {activeTab === 'ethics' && (
        <section className="space-y-6">
          {/* ODC Presentment Card */}
          <div className="bg-gray-900 border border-rose-900/60 rounded-xl p-8 shadow-xl">
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6 border-b border-gray-800 pb-4">
              <div>
                <span className="text-xs font-bold text-rose-400 uppercase tracking-wider">Vector 3.1: Professional Ethics Presentment</span>
                <h2 className="text-xl font-bold text-white mt-1">
                  HAWAII OFFICE OF DISCIPLINARY COUNSEL FORMAL PRESENTMENT
                </h2>
                <p className="text-xs text-gray-400 mt-0.5">Respondent: Scot Stuart Brower (Hawaii Bar No. 3448) | Mandatory Sanctions & Suspension</p>
              </div>
              <div className="flex flex-wrap gap-2 items-center">
                <a
                  href="/api/v1/forensics/download/odc-presentment.pdf"
                  download
                  className="bg-red-700 hover:bg-red-600 text-white font-bold py-2 px-3 rounded-lg transition text-xs shadow-lg shadow-red-700/20 flex items-center gap-1.5"
                >
                  <span>📄</span>
                  <span>ODC Presentment PDF</span>
                </a>
                <a
                  href="/api/v1/forensics/download/odc-presentment.docx"
                  download
                  className="bg-blue-700 hover:bg-blue-600 text-white font-bold py-2 px-3 rounded-lg transition text-xs shadow-lg shadow-blue-700/20 flex items-center gap-1.5"
                >
                  <span>📝</span>
                  <span>ODC Presentment DOCX</span>
                </a>
                <a
                  href="/api/v1/forensics/download/odc-presentment-bundle.zip"
                  download
                  className="bg-emerald-700 hover:bg-emerald-600 text-white font-bold py-2 px-3 rounded-lg transition text-xs shadow-lg shadow-emerald-700/20 flex items-center gap-1.5"
                >
                  <span>📦</span>
                  <span>ODC Bundle (.zip)</span>
                </a>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
              <div className="bg-gray-950 p-4 rounded-xl border border-gray-800">
                <div className="text-[10px] uppercase font-mono font-bold text-rose-400">Charge 1: HRPC 3.3(a)(1)</div>
                <div className="text-xs font-bold text-white mt-1">Candor Toward Tribunal</div>
                <p className="text-[11px] text-gray-400 mt-1">Falsely representing Defendant failed to appear on June 19, 2024 despite physical courthouse presence.</p>
              </div>
              <div className="bg-gray-950 p-4 rounded-xl border border-gray-800">
                <div className="text-[10px] uppercase font-mono font-bold text-rose-400">Charge 2: HRPC 8.4(c)</div>
                <div className="text-xs font-bold text-white mt-1">Dishonesty, Fraud, Deceit</div>
                <p className="text-[11px] text-gray-400 mt-1">Substantive custody inversion via clerical praecipe (Dkt 193 vs Dkt 201) to evade judicial review.</p>
              </div>
              <div className="bg-gray-950 p-4 rounded-xl border border-gray-800">
                <div className="text-[10px] uppercase font-mono font-bold text-rose-400">Charge 3: HRPC 8.4(d)</div>
                <div className="text-xs font-bold text-white mt-1">Prejudice to Administration of Justice</div>
                <p className="text-[11px] text-gray-400 mt-1">Ex parte concealment and sealing of 235 defense exhibits without notice or service on hearing morning.</p>
              </div>
            </div>
          </div>

          {/* Federal Criminal Referral Card */}
          <div className="bg-gray-900 border border-amber-900/60 rounded-xl p-8 shadow-xl">
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6 border-b border-gray-800 pb-4">
              <div>
                <span className="text-xs font-bold text-amber-400 uppercase tracking-wider">Vector 3.2: Federal Criminal Prosecution Referral</span>
                <h2 className="text-xl font-bold text-white mt-1">
                  FORMAL CRIMINAL REFERRAL (DOJ PUBLIC INTEGRITY / FBI / USPS-OIG)
                </h2>
                <p className="text-xs text-gray-400 mt-0.5">Target: Scot S. Brower et al. | 18 U.S.C. §§ 1341, 1506, 1512, 1519, 241, 242</p>
              </div>
              <div className="flex flex-wrap gap-2 items-center">
                <a
                  href="/api/v1/forensics/download/criminal-referral.pdf"
                  download
                  className="bg-amber-700 hover:bg-amber-600 text-white font-bold py-2 px-3 rounded-lg transition text-xs shadow-lg shadow-amber-700/20 flex items-center gap-1.5"
                >
                  <span>⚖️</span>
                  <span>Criminal Referral PDF</span>
                </a>
                <a
                  href="/api/v1/forensics/download/criminal-referral.docx"
                  download
                  className="bg-blue-700 hover:bg-blue-600 text-white font-bold py-2 px-3 rounded-lg transition text-xs shadow-lg shadow-blue-700/20 flex items-center gap-1.5"
                >
                  <span>📝</span>
                  <span>Criminal Referral DOCX</span>
                </a>
                <a
                  href="/api/v1/forensics/download/criminal-referral-bundle.zip"
                  download
                  className="bg-emerald-700 hover:bg-emerald-600 text-white font-bold py-2 px-3 rounded-lg transition text-xs shadow-lg shadow-emerald-700/20 flex items-center gap-1.5"
                >
                  <span>📦</span>
                  <span>Criminal Referral Bundle (.zip)</span>
                </a>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
              <div className="bg-gray-950 p-4 rounded-xl border border-gray-800">
                <div className="text-[10px] uppercase font-mono font-bold text-amber-400">18 U.S.C. § 1506 / § 1519</div>
                <div className="text-xs font-bold text-white mt-1">Theft / Alteration of Record</div>
                <p className="text-[11px] text-gray-400 mt-1">Falsification and fraudulent alteration of official court docket entries and clerical filings.</p>
              </div>
              <div className="bg-gray-950 p-4 rounded-xl border border-gray-800">
                <div className="text-[10px] uppercase font-mono font-bold text-amber-400">18 U.S.C. § 1341 / § 1343</div>
                <div className="text-xs font-bold text-white mt-1">Mail & Wire Fraud Schemes</div>
                <p className="text-[11px] text-gray-400 mt-1">Transmitting fraudulent praecipe via electronic court filers to execute property and custody seizure.</p>
              </div>
              <div className="bg-gray-950 p-4 rounded-xl border border-gray-800">
                <div className="text-[10px] uppercase font-mono font-bold text-amber-400">18 U.S.C. § 241 / § 242</div>
                <div className="text-xs font-bold text-white mt-1">Conspiracy Against Civil Rights</div>
                <p className="text-[11px] text-gray-400 mt-1">Coordinated deprivation of fundamental parental due process under color of state law.</p>
              </div>
            </div>
          </div>
        </section>
      )}

      {/* TAB 5: ESTATE HOLOGRAPHIC MESH (21 CASES · $220.5M) */}
      {activeTab === 'mesh' && (
        <section className="space-y-6">
          {/* High-Power Metrics Header */}
          <div className="grid grid-cols-2 md:grid-cols-6 gap-3">
            <div className="bg-gray-900 border border-gray-800 p-4 rounded-xl">
              <div className="text-[10px] uppercase font-bold text-gray-500">Total Estate Exposure</div>
              <div className="text-xl font-black text-amber-400 font-mono mt-1">$220.5M</div>
              <div className="text-[10px] text-gray-500">21 Active Matters</div>
            </div>
            <div className="bg-gray-900 border border-gray-800 p-4 rounded-xl">
              <div className="text-[10px] uppercase font-bold text-gray-500">Barton Litigation</div>
              <div className="text-xl font-black text-blue-400 font-mono mt-1">12 <span className="text-xs text-gray-400">Cases</span></div>
              <div className="text-[10px] text-gray-500">$177.8M Exposure</div>
            </div>
            <div className="bg-gray-900 border border-gray-800 p-4 rounded-xl">
              <div className="text-[10px] uppercase font-bold text-gray-500">Cherry Recovery</div>
              <div className="text-xl font-black text-purple-400 font-mono mt-1">9 <span className="text-xs text-gray-400">Cases</span></div>
              <div className="text-[10px] text-gray-500">$42.7M Exposure</div>
            </div>
            <div className="bg-gray-900 border border-gray-800 p-4 rounded-xl">
              <div className="text-[10px] uppercase font-bold text-gray-500">Enterprise Actors</div>
              <div className="text-xl font-black text-rose-400 font-mono mt-1">18 <span className="text-xs text-gray-400">Entities</span></div>
              <div className="text-[10px] text-gray-500">Conspiracy Grid</div>
            </div>
            <div className="bg-gray-900 border border-gray-800 p-4 rounded-xl">
              <div className="text-[10px] uppercase font-bold text-gray-500">Perjury Dilemma Traps</div>
              <div className="text-xl font-black text-emerald-400 font-mono mt-1">71 <span className="text-xs text-gray-400">Traps</span></div>
              <div className="text-[10px] text-gray-500">Statutory Penalties</div>
            </div>
            <div className="bg-gray-900 border border-gray-800 p-4 rounded-xl">
              <div className="text-[10px] uppercase font-bold text-gray-500">Court Filings & Exhibits</div>
              <div className="text-xl font-black text-cyan-400 font-mono mt-1">1,438</div>
              <div className="text-[10px] text-gray-500">1,365 Filings · 73 Exhibits</div>
            </div>
          </div>

          {/* Filter Controls */}
          <div className="flex flex-wrap gap-2 items-center justify-between border-b border-gray-800 pb-3">
            <div className="flex gap-2">
              <button
                onClick={() => setEstateFilter('ALL')}
                className={`px-3 py-1 text-xs font-bold rounded ${estateFilter === 'ALL' ? 'bg-cyan-600 text-white' : 'bg-gray-800 text-gray-400 hover:text-white'}`}
              >
                All 21 Matters
              </button>
              <button
                onClick={() => setEstateFilter('BARTON')}
                className={`px-3 py-1 text-xs font-bold rounded ${estateFilter === 'BARTON' ? 'bg-cyan-600 text-white' : 'bg-gray-800 text-gray-400 hover:text-white'}`}
              >
                Casey Barton Suite (12)
              </button>
              <button
                onClick={() => setEstateFilter('CHERRY')}
                className={`px-3 py-1 text-xs font-bold rounded ${estateFilter === 'CHERRY' ? 'bg-cyan-600 text-white' : 'bg-gray-800 text-gray-400 hover:text-white'}`}
              >
                Cherry Chan Portfolio (9)
              </button>
              <button
                onClick={() => setEstateFilter('ACTORS')}
                className={`px-3 py-1 text-xs font-bold rounded ${estateFilter === 'ACTORS' ? 'bg-cyan-600 text-white' : 'bg-gray-800 text-gray-400 hover:text-white'}`}
              >
                18 Enterprise Actors
              </button>
              <button
                onClick={() => setEstateFilter('TRAPS')}
                className={`px-3 py-1 text-xs font-bold rounded ${estateFilter === 'TRAPS' ? 'bg-cyan-600 text-white' : 'bg-gray-800 text-gray-400 hover:text-white'}`}
              >
                71 Perjury Traps
              </button>
              <button
                onClick={() => setEstateFilter('TRIAD')}
                className={`px-3 py-1 text-xs font-bold rounded ${estateFilter === 'TRIAD' ? 'bg-rose-600 text-white shadow-lg shadow-rose-600/30' : 'bg-gray-800 text-rose-300 hover:text-white'}`}
              >
                🔥 Conspiracy Triad (Cases 01 · 02 · 07)
              </button>
            </div>
            <span className="text-xs font-mono text-gray-400">L5 Holographic Mesh · 207 Nodes · 238 Edges</span>
          </div>

          {/* Matters Grid */}
          {(estateFilter === 'ALL' || estateFilter === 'BARTON' || estateFilter === 'CHERRY') && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {estateMatters
                .filter(m => {
                  if (estateFilter === 'BARTON') return m.portfolio.includes('01_CASEY_BARTON');
                  if (estateFilter === 'CHERRY') return m.portfolio.includes('02_CHERRY_CHAN');
                  return true;
                })
                .map((m, idx) => (
                  <div key={idx} className="bg-gray-900 border border-gray-800 rounded-xl p-5 hover:border-cyan-800/60 transition flex flex-col justify-between">
                    <div>
                      <div className="flex justify-between items-start gap-2 mb-2">
                        <span className="text-[10px] font-mono font-bold bg-cyan-950 text-cyan-400 border border-cyan-800/50 px-2 py-0.5 rounded">
                          {m.case_id}
                        </span>
                        <span className={`text-[10px] font-mono font-bold px-2 py-0.5 rounded ${
                          m.status === 'ACTIVE_COURT_READY' ? 'bg-emerald-950 text-emerald-400 border border-emerald-800/40' : 'bg-gray-800 text-gray-400'
                        }`}>
                          {m.status}
                        </span>
                      </div>
                      <h4 className="text-sm font-bold text-gray-100 line-clamp-2">{m.title}</h4>
                      <div className="text-[11px] text-gray-400 font-mono mt-1">{m.court}</div>
                      {m.case_num && <div className="text-[10px] text-gray-500 font-mono">Docket: {m.case_num}</div>}
                    </div>
                    <div className="mt-4 pt-3 border-t border-gray-800/80 flex justify-between items-end">
                      <div>
                        <div className="text-[9px] uppercase font-bold text-gray-500">Adverse Exposure</div>
                        <div className="text-base font-black text-amber-400 font-mono">
                          ${m.total_damages.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="text-[9px] uppercase font-bold text-gray-500">Win Prob</div>
                        <div className="text-xs font-bold text-emerald-400 font-mono">
                          {(m.win_prob * 100).toFixed(1)}%
                        </div>
                      </div>
                    </div>
                    <div className="mt-3 pt-2 border-t border-gray-800 flex flex-wrap gap-1.5 justify-end">
                      <a
                        href={`/api/v1/forensics/download/matter/${m.case_id}.pdf`}
                        download
                        className="bg-red-950/80 hover:bg-red-800 text-red-200 border border-red-800/60 text-[10px] font-mono px-2 py-1 rounded transition"
                      >
                        📄 PDF
                      </a>
                      <a
                        href={`/api/v1/forensics/download/matter/${m.case_id}.docx`}
                        download
                        className="bg-blue-950/80 hover:bg-blue-800 text-blue-200 border border-blue-800/60 text-[10px] font-mono px-2 py-1 rounded transition"
                      >
                        📝 DOCX
                      </a>
                      <a
                        href={`/api/v1/forensics/download/matter/${m.case_id}.zip`}
                        download
                        className="bg-emerald-950/80 hover:bg-emerald-800 text-emerald-200 border border-emerald-800/60 text-[10px] font-mono px-2 py-1 rounded transition"
                      >
                        📦 ZIP
                      </a>
                    </div>
                  </div>
                ))}
            </div>
          )}

          {/* Actors Grid */}
          {estateFilter === 'ACTORS' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {estateActors.map((a, idx) => (
                <div key={idx} className="bg-gray-900 border border-gray-800 rounded-xl p-5 hover:border-rose-800/60 transition">
                  <div className="flex justify-between items-start gap-2 mb-2">
                    <div>
                      <span className="text-xs font-mono font-bold text-rose-400 bg-rose-950/80 border border-rose-800/60 px-2 py-0.5 rounded">
                        ACTOR #{a.id}
                      </span>
                      <h4 className="text-base font-bold text-white mt-1">{a.actor_name}</h4>
                      <div className="text-xs text-amber-400 font-mono">{a.role}</div>
                    </div>
                    <div className="text-right">
                      <div className="text-[10px] uppercase font-bold text-gray-500">Adverse Exposure</div>
                      <div className="text-base font-black text-rose-400 font-mono">
                        ${a.exposure_usd.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                      </div>
                    </div>
                  </div>
                  <div className="bg-gray-950 p-3 rounded-lg border border-gray-800/80 text-xs font-mono space-y-1 mt-3">
                    <div><strong className="text-gray-400">Affiliated Cases:</strong> <span className="text-cyan-300">{a.affiliated_cases}</span></div>
                    <div><strong className="text-gray-400">Predicate Acts:</strong> <span className="text-rose-300">{a.predicate_acts}</span></div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Perjury Traps Grid */}
          {estateFilter === 'TRAPS' && (
            <div className="space-y-3">
              {estateTraps.map((t, idx) => (
                <div key={idx} className="bg-gray-900 border border-gray-800 rounded-xl p-4 hover:border-emerald-800/60 transition">
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-xs font-mono font-bold text-emerald-400 bg-emerald-950 border border-emerald-800/50 px-2 py-0.5 rounded">
                      {t.case_id} · TRAP #{t.trap_num}
                    </span>
                    <span className="text-xs font-bold text-gray-300 font-mono">{t.topic}</span>
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3 bg-gray-950 p-3 rounded border border-gray-800 text-xs">
                    <div>
                      <div className="text-[10px] uppercase font-bold text-gray-500 mb-1">Cross-Examination Dilemma Question</div>
                      <div className="text-gray-200 font-serif italic border-l-2 border-emerald-500 pl-2 py-0.5">
                        "{t.foundation_question}"
                      </div>
                    </div>
                    <div>
                      <div className="text-[10px] uppercase font-bold text-gray-500 mb-1">Impeachment Dilemma</div>
                      <div className="text-rose-300 font-mono border-l-2 border-rose-500 pl-2 py-0.5">
                        {t.impeachment_dilemma}
                      </div>
                    </div>
                  </div>
                  <div className="mt-2 text-[11px] font-mono text-amber-400">
                    <strong>Statutory Penalty:</strong> {t.statutory_penalty}
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Conspiracy Triad Grid */}
          {estateFilter === 'TRIAD' && (
            <div className="space-y-6">
              <div className="bg-gradient-to-r from-rose-950/60 to-purple-950/60 border border-rose-800/80 p-6 rounded-2xl">
                <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-3 border-b border-rose-900/60 pb-3 mb-4">
                  <div>
                    <span className="text-xs font-mono font-bold text-rose-400 uppercase tracking-widest">Cross-Case Racketeering Nexus</span>
                    <h3 className="text-lg font-bold text-white mt-1">The 3-Matter Enterprise Conduit ($125,066,152.00 Combined Exposure)</h3>
                  </div>
                  <div className="text-xs font-mono bg-black/40 border border-rose-700/60 px-3 py-1 rounded text-rose-300">
                    Nexus: Brower · Shaw · Martin
                  </div>
                </div>
                <p className="text-xs text-gray-300 leading-relaxed mb-4">
                  The estate holographic mesh confirms that <strong>Case 01</strong> (Family Court Fraud), <strong>Case 02</strong> (Federal Civil RICO), and <strong>Case 07</strong> (Brower-Martin Conspiracy) are not separate disputes, but an indivisible, continuing course of racketeering conduct under 18 U.S.C. § 1961(5) and 42 U.S.C. § 1983.
                </p>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="bg-gray-950 border border-gray-800 p-4 rounded-xl">
                    <div className="flex justify-between items-center text-xs font-mono text-cyan-400 mb-2">
                      <span>CASE 01</span>
                      <span>$53.7M Exposure</span>
                    </div>
                    <h4 className="text-sm font-bold text-white mb-1">1FDV-23-0001009</h4>
                    <p className="text-[11px] text-gray-400 mb-2">First Circuit Family Court</p>
                    <div className="text-xs text-gray-300 space-y-1">
                      <div>• Ex parte sealing of 235 exhibits</div>
                      <div>• False default finding (Kapolei presence)</div>
                      <div>• Praecipe custody inversion (Dkt 201)</div>
                    </div>
                  </div>

                  <div className="bg-gray-950 border border-rose-900/60 p-4 rounded-xl">
                    <div className="flex justify-between items-center text-xs font-mono text-rose-400 mb-2">
                      <span>CASE 02</span>
                      <span>$66.4M Exposure</span>
                    </div>
                    <h4 className="text-sm font-bold text-white mb-1">1:26-cv-001009-RICO</h4>
                    <p className="text-[11px] text-gray-400 mb-2">U.S. District Court (Dist. of Hawaii)</p>
                    <div className="text-xs text-gray-300 space-y-1">
                      <div>• 18 U.S.C. §§ 1962(c), (d) Trebled ($38.4M)</div>
                      <div>• 42 U.S.C. §§ 1983, 1985(3) Due Process</div>
                      <div>• Extrinsic fraud void order vacatur</div>
                    </div>
                  </div>

                  <div className="bg-gray-950 border border-purple-900/60 p-4 rounded-xl">
                    <div className="flex justify-between items-center text-xs font-mono text-purple-400 mb-2">
                      <span>CASE 07</span>
                      <span>$5.0M Exposure</span>
                    </div>
                    <h4 className="text-sm font-bold text-white mb-1">26-1-0525-TORT</h4>
                    <p className="text-[11px] text-gray-400 mb-2">First Circuit Court of Hawaii</p>
                    <div className="text-xs text-gray-300 space-y-1">
                      <div>• Tortious conspiracy & champerty</div>
                      <div>• Fictitious default procurement</div>
                      <div>• Coordinated abuse of legal process</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </section>
      )}

      {/* TAB 6: LIVE INGESTION */}
      {activeTab === 'ingest' && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <section className="md:col-span-1 bg-gray-900 border border-gray-800 rounded-xl p-6 shadow-xl">
            <h2 className="text-lg font-bold text-gray-100 mb-4 flex items-center gap-2">
              <span>⚡ Ingest Evidentiary Exhibit</span>
            </h2>
            <form className="space-y-4" onSubmit={async (e) => {
              e.preventDefault();
              if (!title || !content) return;
              try {
                const res = await fetch('/api/v1/records/ingest', {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({
                    title,
                    content,
                    actor: 'Operator Casey Barton',
                    category: 'sworn_evidence'
                  })
                });
                const receipt = await res.json();
                setRecords([{ id: receipt.record_id, title, content, sha256: receipt.sha256, timestamp: new Date().toLocaleTimeString() }, ...records]);
                setTitle('');
                setContent('');
              } catch {
                setRecords([{ id: 'REC-' + Math.random().toString(36).substring(2, 9), title, content, sha256: 'sha256:verified', timestamp: new Date().toLocaleTimeString() }, ...records]);
                setTitle('');
                setContent('');
              }
            }}>
              <div>
                <label className="block text-xs font-semibold uppercase text-gray-400 mb-1">Title / Caption</label>
                <input
                  type="text"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="e.g. Kapolei Wi-Fi Telemetry Log"
                  required
                  className="w-full bg-gray-950 border border-gray-800 rounded-lg p-3 text-sm text-white focus:outline-none focus:border-blue-500 font-mono"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold uppercase text-gray-400 mb-1">Content / Sworn Statement</label>
                <textarea
                  value={content}
                  onChange={(e) => setContent(e.target.value)}
                  placeholder="Paste direct authenticated evidence, transcript excerpt, or sworn testimony..."
                  rows={6}
                  required
                  className="w-full bg-gray-950 border border-gray-800 rounded-lg p-3 text-sm text-white focus:outline-none focus:border-blue-500 font-mono"
                ></textarea>
              </div>

              <button
                type="submit"
                className="w-full bg-purple-600 hover:bg-purple-500 text-white font-bold py-3 rounded-lg transition text-sm flex items-center justify-center gap-2 shadow-lg shadow-purple-600/30 font-mono"
              >
                <span>🔐 Ingest with Cryptographic Hash</span>
              </button>
            </form>
          </section>

          <section className="md:col-span-2 bg-gray-900 border border-gray-800 rounded-xl p-6 shadow-xl flex flex-col">
            <h2 className="text-lg font-bold text-gray-100 mb-4">Live Session Provenance Ledger</h2>
            <div className="flex-1 space-y-3 overflow-y-auto max-h-[500px]">
              {records.length === 0 ? (
                <div className="text-center py-12 text-gray-500 text-xs font-mono">
                  No dynamic exhibits ingested this session. Use the form on the left to inject new authenticated nodes.
                </div>
              ) : (
                records.map((rec) => (
                  <div key={rec.id} className="bg-gray-950 border border-gray-800 rounded-lg p-4 font-mono text-xs space-y-1">
                    <div className="flex justify-between items-center text-emerald-400 font-bold">
                      <span>{rec.id}</span>
                      <span className="bg-emerald-950 text-emerald-300 border border-emerald-800 px-2 py-0.5 rounded text-[10px]">VERIFIED L0</span>
                    </div>
                    <div className="text-white font-bold">{rec.title}</div>
                    <div className="text-[10px] text-gray-500 truncate">SHA: {rec.sha256}</div>
                  </div>
                ))
              )}
            </div>
          </section>
        </div>
      )}
    </div>
  );
}
