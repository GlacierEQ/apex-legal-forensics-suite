"""
APEX Legal Forensics Suite - Estate Holographic Mesh Engine
------------------------------------------------------------
Interfaces directly with the 21-Matter Estate Holographic Mesh Database
Total Adverse Exposure: $220,540,952.00 (21 Cases · 18 Enterprise Actors · 71 Perjury Traps)
Epistemic Standard: L0–L5 Holographic Mesh
"""

import sqlite3
import os
from pathlib import Path
from typing import Dict, Any, List, Optional

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
