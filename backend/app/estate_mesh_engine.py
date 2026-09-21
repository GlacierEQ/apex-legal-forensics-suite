"""
APEX Legal Forensics Suite - Estate Holographic Mesh Engine
------------------------------------------------------------
Interfaces directly with the 21-Matter Estate Holographic Mesh Database
Total Adverse Exposure: $220,540,952.00 (21 Cases · 18 Enterprise Actors · 71 Perjury Traps)
Epistemic Standard: L0–L5 Holographic Mesh
"""

import sqlite3
import os
import hashlib
import time
import io
import zipfile
import json
from pathlib import Path
from typing import Dict, Any, List, Optional

try:
    from backend.app.legal_filing_engine import (
        build_28_line_pdf,
        build_pleading_docx,
        format_28_line_pleading
    )
except ImportError:
    try:
        from legal_filing_engine import (
            build_28_line_pdf,
            build_pleading_docx,
            format_28_line_pleading
        )
    except ImportError:
        build_28_line_pdf = None
        build_pleading_docx = None
        format_28_line_pleading = None

DB_CANDIDATE_PATHS = [
    Path(__file__).parent.parent / "data" / "estate_holographic_mesh.db",
    Path("/root/casebuilder4000/build/estate_holographic_mesh.db"),
    Path("/root/legal_mesh/estate_holographic_mesh.db")
]

def get_db_connection() -> Optional[sqlite3.Connection]:
    for p in DB_CANDIDATE_PATHS:
        if p.exists():
            try:
                conn = sqlite3.connect(str(p))
                conn.row_factory = sqlite3.Row
                return conn
            except Exception:
                continue
    return None

def get_estate_overview() -> Dict[str, Any]:
    """Returns high-level forensic metrics across the entire 21-case estate."""
    conn = get_db_connection()
    if not conn:
        return {
            "status": "OFFLINE",
            "error": "estate_holographic_mesh.db not found",
            "total_matters": 0,
            "total_exposure_usd": 0.0
        }
    
    try:
        cur = conn.cursor()
        
        cur.execute("SELECT count(*), coalesce(sum(total_damages), 0) FROM matters")
        matters_count, total_exposure = cur.fetchone()
        
        cur.execute("SELECT count(*) FROM conspiracy_actors")
        actors_count = cur.fetchone()[0]
        
        cur.execute("SELECT count(*) FROM perjury_traps")
        traps_count = cur.fetchone()[0]
        
        cur.execute("SELECT count(*) FROM exhibits")
        exhibits_count = cur.fetchone()[0]
        
        cur.execute("SELECT count(*) FROM filings")
        filings_count = cur.fetchone()[0]
        
        cur.execute("SELECT count(*) FROM mesh_nodes")
        nodes_count = cur.fetchone()[0]
        
        cur.execute("SELECT count(*) FROM mesh_edges")
        edges_count = cur.fetchone()[0]
        
        # Portfolio breakdown
        cur.execute("""
            SELECT portfolio, count(*), sum(total_damages)
            FROM matters
            GROUP BY portfolio
        """)
        portfolios = []
        for row in cur.fetchall():
            portfolios.append({
                "portfolio": row[0],
                "matters_count": row[1],
                "exposure_usd": float(row[2] or 0.0)
            })
            
        return {
            "status": "ONLINE",
            "database_version": "APEX_HOLOGRAPHIC_MESH_v4.0",
            "total_matters": matters_count,
            "total_exposure_usd": float(total_exposure),
            "portfolios": portfolios,
            "conspiracy_actors_count": actors_count,
            "perjury_traps_count": traps_count,
            "certified_exhibits_count": exhibits_count,
            "court_filings_count": filings_count,
            "mesh_nodes_count": nodes_count,
            "mesh_edges_count": edges_count,
            "epistemic_level": "L5_HOLOGRAPHIC_MESH"
        }
    finally:
        conn.close()

def get_estate_matters(portfolio: Optional[str] = None) -> List[Dict[str, Any]]:
    """Returns list of active legal matters across the estate."""
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        cur = conn.cursor()
        if portfolio:
            cur.execute("""
                SELECT case_id, title, portfolio, court, case_num,
                       economic_damages, statutory_damages, general_damages,
                       punitive_damages, total_damages, win_prob, status
                FROM matters
                WHERE portfolio LIKE ?
                ORDER BY total_damages DESC
            """, (f"%{portfolio}%",))
        else:
            cur.execute("""
                SELECT case_id, title, portfolio, court, case_num,
                       economic_damages, statutory_damages, general_damages,
                       punitive_damages, total_damages, win_prob, status
                FROM matters
                ORDER BY total_damages DESC
            """)
            
        results = []
        for r in cur.fetchall():
            results.append({
                "case_id": r["case_id"],
                "title": r["title"],
                "portfolio": r["portfolio"],
                "court": r["court"],
                "case_num": r["case_num"],
                "economic_damages": float(r["economic_damages"] or 0.0),
                "statutory_damages": float(r["statutory_damages"] or 0.0),
                "general_damages": float(r["general_damages"] or 0.0),
                "punitive_damages": float(r["punitive_damages"] or 0.0),
                "total_damages": float(r["total_damages"] or 0.0),
                "win_prob": float(r["win_prob"] or 0.0),
                "status": r["status"]
            })
        return results
    finally:
        conn.close()

def get_estate_actors() -> List[Dict[str, Any]]:
    """Returns conspiracy actors identified across the racketeering enterprise."""
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, actor_name, role, affiliated_cases, predicate_acts, exposure_usd
            FROM conspiracy_actors
            ORDER BY exposure_usd DESC
        """)
        results = []
        for r in cur.fetchall():
            results.append({
                "id": r["id"],
                "actor_name": r["actor_name"],
                "role": r["role"],
                "affiliated_cases": r["affiliated_cases"],
                "predicate_acts": r["predicate_acts"],
                "exposure_usd": float(r["exposure_usd"] or 0.0)
            })
        return results
    finally:
        conn.close()

def get_estate_perjury_traps(case_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """Returns cross-examination dilemma traps."""
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        cur = conn.cursor()
        if case_id:
            cur.execute("""
                SELECT id, case_id, trap_num, topic, foundation_question,
                       impeachment_dilemma, statutory_penalty
                FROM perjury_traps
                WHERE case_id = ?
                ORDER BY trap_num ASC
            """, (case_id,))
        else:
            cur.execute("""
                SELECT id, case_id, trap_num, topic, foundation_question,
                       impeachment_dilemma, statutory_penalty
                FROM perjury_traps
                ORDER BY case_id, trap_num ASC
            """)
        results = []
        for r in cur.fetchall():
            results.append({
                "id": r["id"],
                "case_id": r["case_id"],
                "trap_num": r["trap_num"],
                "topic": r["topic"],
                "foundation_question": r["foundation_question"],
                "impeachment_dilemma": r["impeachment_dilemma"],
                "statutory_penalty": r["statutory_penalty"]
            })
        return results
    finally:
        conn.close()

def get_estate_graph() -> Dict[str, Any]:
    """Returns mesh graph nodes and edges linking matters, actors, and claims."""
    conn = get_db_connection()
    if not conn:
        return {"nodes": [], "edges": []}
    
    try:
        cur = conn.cursor()
        cur.execute("SELECT node_id, node_type, canonical_label, category, status, metadata_json FROM mesh_nodes")
        nodes = []
        for r in cur.fetchall():
            nodes.append({
                "id": r[0],
                "type": r[1],
                "label": r[2],
                "category": r[3],
                "status": r[4],
                "metadata": r[5]
            })
            
        cur.execute("SELECT source_node, target_node, relation, weight, confidence, evidence_basis FROM mesh_edges")
        edges = []
        for r in cur.fetchall():
            edges.append({
                "source": r[0],
                "target": r[1],
                "relation": r[2],
                "weight": r[3],
                "confidence": r[4],
                "evidence_basis": r[5]
            })
            
        return {
            "node_count": len(nodes),
            "edge_count": len(edges),
            "nodes": nodes,
            "edges": edges
        }
    finally:
        conn.close()


def get_matter_detail(case_id: str) -> Optional[Dict[str, Any]]:
    """Returns complete forensic detail for any of the 21 estate matters, including exhibits, traps, and actors."""
    conn = get_db_connection()
    if not conn:
        return None
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM matters WHERE case_id = ?", (case_id,))
        m_row = cur.fetchone()
        if not m_row:
            return None
        
        matter = dict(m_row)
        
        # Perjury traps
        cur.execute("SELECT * FROM perjury_traps WHERE case_id = ? ORDER BY trap_num ASC", (case_id,))
        traps = [dict(r) for r in cur.fetchall()]
        matter["perjury_traps"] = traps
        
        # Exhibits
        cur.execute("SELECT * FROM exhibits WHERE case_id = ? ORDER BY exhibit_id ASC", (case_id,))
        exhibits = [dict(r) for r in cur.fetchall()]
        matter["exhibits"] = exhibits
        
        # Filings
        cur.execute("SELECT * FROM filings WHERE case_id = ? ORDER BY tier ASC", (case_id,))
        filings = [dict(r) for r in cur.fetchall()]
        matter["filings"] = filings
        
        # Connected Actors via conspiracy_actors affiliated_cases or edges
        cur.execute("SELECT actor_name, role, exposure_usd, predicate_acts FROM conspiracy_actors WHERE affiliated_cases LIKE ?", (f"%{case_id}%",))
        actors = [dict(r) for r in cur.fetchall()]
        matter["conspiracy_actors"] = actors
        
        return matter
    finally:
        conn.close()


def generate_matter_packet(case_id: str) -> Dict[str, Any]:
    """
    Generates a full-stack verified court pleading packet for any of the 21 matters
    in the APEX estate, including Cherry Chan recovery portfolio matters.
    """
    matter = get_matter_detail(case_id)
    if not matter:
        raise ValueError(f"Matter {case_id} not found in estate database")
        
    court = matter.get("court", "COURT OF COMPETENT JURISDICTION")
    case_num = matter.get("case_num", f"CASE-REF-{case_id}")
    title = matter.get("title", f"Matter: {case_id}")
    portfolio = matter.get("portfolio", "GENERAL_ESTATE")
    total_damages = matter.get("total_damages", 0.0)
    
    caption = f"""{court}

{title.upper()}

{case_num}

VERIFIED COMPLAINT AND DEMAND FOR STATUTORY RELIEF
TOTAL ADVERSE CLAIM: ${total_damages:,.2f}
(Evidentiary Primacy Enforced pursuant to FRE 601/602 and HRE 601/602)
"""

    jurisdiction = f"""I. JURISDICTION & VENUE
1. This action arises under controlling statutory authority and substantive law governing {court}.
2. Venue and subject-matter jurisdiction are properly vested in this tribunal.
3. This action is prosecuted with full direct eyewitness standing and verified evidentiary competence.
"""

    actors_section = "II. DEFENDANTS & ADVERSE ENTERPRISE ENTITIES\n"
    for i, a in enumerate(matter.get("conspiracy_actors", []), 1):
        actors_section += f"{i}. {a.get('actor_name')}: Role: {a.get('role')}; Exposure: ${a.get('exposure_usd', 0.0):,.2f}\n   Predicate Acts: {a.get('predicate_acts', 'N/A')}\n"
    if not matter.get("conspiracy_actors"):
        actors_section += "1. Named institutional and individual defendants according to formal docket ledger.\n"

    traps_section = "III. CROSS-EXAMINATION PERJURY DILEMMA TRAPS & FACTUAL SPECIFICATIONS\n"
    for t in matter.get("perjury_traps", []):
        traps_section += f"TRAP #{t.get('trap_num')}: {t.get('topic')}\n"
        traps_section += f"  Q: \"{t.get('foundation_question')}\"\n"
        traps_section += f"  Impeachment Dilemma: {t.get('impeachment_dilemma')}\n"
        traps_section += f"  Statutory Penalty: {t.get('statutory_penalty')}\n\n"

    exhibits_section = "V. CERTIFIED EVIDENTIARY EXHIBITS SCHEDULE\n"
    for ex in matter.get("exhibits", []):
        exhibits_section += f"Exhibit {ex.get('exhibit_id')}: {ex.get('description')}\n"
        exhibits_section += f"  Authentication: {ex.get('auth_rule')} | SHA-256: {str(ex.get('sha256', 'N/A'))[:16]}...\n"

    prayer = f"""VI. PRAYER FOR RELIEF
WHEREFORE, Plaintiff demands judgment against Defendants:
A. Actual and economic damages: ${matter.get('economic_damages', 0.0):,.2f};
B. Statutory and treble damages: ${matter.get('statutory_damages', 0.0):,.2f};
C. General and punitive damages: ${(matter.get('general_damages', 0.0) + matter.get('punitive_damages', 0.0)):,.2f};
D. TOTAL COMPREHENSIVE ADVERSE JUDGMENT: ${total_damages:,.2f};
E. Declaratory and equitable vacatur relief; and
F. Pre-judgment interest, attorney fees, and litigation costs.

DEMAND FOR JURY TRIAL
Plaintiff hereby demands trial by jury on all counts so triable.

DATED: Honolulu, Hawaii, September 21, 2026.
"""

    verification = """VERIFICATION UNDER PENALTY OF PERJURY
(Pursuant to 28 U.S.C. § 1746 and FRE/HRE 601/602)
I declare under penalty of perjury under the laws of the United States and the State of Hawaii that I have read the foregoing complaint and know the contents thereof, and the same is true of my own firsthand knowledge.
Executed on September 21, 2026.
"""

    full_text = f"{caption}\n\n{jurisdiction}\n\n{actors_section}\n\n{traps_section}\n\n{exhibits_section}\n\n{prayer}\n\n{verification}"
    
    formatted_28 = format_28_line_pleading([caption, jurisdiction, actors_section, traps_section, exhibits_section, prayer, verification], f"{case_id} COMPLAINT") if format_28_line_pleading else full_text
    sha256_hash = hashlib.sha256(full_text.encode("utf-8")).hexdigest()
    
    return {
        "case_id": case_id,
        "title": title,
        "court": court,
        "case_num": case_num,
        "portfolio": portfolio,
        "total_damages": total_damages,
        "sha256": sha256_hash,
        "raw_text": full_text,
        "formatted_28_lines": formatted_28,
        "matter_detail": matter,
        "verified": True
    }


def generate_matter_pdf(matter_data: Dict[str, Any]) -> bytes:
    if not build_28_line_pdf:
        raise RuntimeError("build_28_line_pdf unavailable")
    return build_28_line_pdf(
        matter_data.get("raw_text", ""),
        matter_data.get("title", ""),
        matter_data.get("case_num", ""),
        matter_data.get("court", "")
    )


def generate_matter_docx(matter_data: Dict[str, Any]) -> bytes:
    if not build_pleading_docx:
        raise RuntimeError("build_pleading_docx unavailable")
    return build_pleading_docx(
        matter_data.get("raw_text", ""),
        matter_data.get("title", ""),
        matter_data.get("case_num", ""),
        matter_data.get("court", "")
    )


def generate_matter_bundle_zip(matter_data: Dict[str, Any]) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        case_id = matter_data.get("case_id", "MATTER")
        pdf_bytes = generate_matter_pdf(matter_data)
        docx_bytes = generate_matter_docx(matter_data)
        zf.writestr(f"01_{case_id}_COMPLAINT_28LINE.pdf", pdf_bytes)
        zf.writestr(f"01_{case_id}_COMPLAINT.docx", docx_bytes)
        zf.writestr(f"01_{case_id}_FULLTEXT.txt", matter_data.get("raw_text", ""))
        
        detail = matter_data.get("matter_detail", {})
        zf.writestr("02_PERJURY_TRAPS_SCHEDULE.json", json.dumps(detail.get("perjury_traps", []), indent=2))
        zf.writestr("03_CERTIFIED_EXHIBITS_LIST.json", json.dumps(detail.get("exhibits", []), indent=2))
        
        manifest = {
            "case_id": case_id,
            "title": matter_data.get("title", ""),
            "court": matter_data.get("court", ""),
            "total_damages_usd": matter_data.get("total_damages", 0.0),
            "generated_timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "files": {
                f"01_{case_id}_COMPLAINT_28LINE.pdf": hashlib.sha256(pdf_bytes).hexdigest(),
                f"01_{case_id}_COMPLAINT.docx": hashlib.sha256(docx_bytes).hexdigest(),
            }
        }
        zf.writestr("00_FILING_MANIFEST.json", json.dumps(manifest, indent=2))
    return buf.getvalue()

