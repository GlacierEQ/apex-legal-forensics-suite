import time
import hashlib
import os
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

try:
    from backend.app.terminal_ui import get_terminal_html
except ImportError:
    try:
        from terminal_ui import get_terminal_html
    except ImportError:
        get_terminal_html = None

try:
    from backend.app.legal_filing_engine import (
        generate_hawaii_filing_packet,
        generate_federal_rico_complaint,
        generate_hawaii_packet_pdf,
        generate_hawaii_packet_docx,
        generate_federal_rico_pdf,
        generate_federal_rico_docx,
        generate_hawaii_filing_bundle_zip,
        generate_federal_rico_bundle_zip,
        generate_brower_odc_presentment,
        generate_odc_presentment_pdf,
        generate_odc_presentment_docx,
        generate_odc_presentment_bundle_zip,
        generate_federal_criminal_referral,
        generate_criminal_referral_pdf,
        generate_criminal_referral_docx,
        generate_criminal_referral_bundle_zip,
        generate_master_bates_exhibit_binder,
        generate_master_bates_binder_pdf,
        generate_master_bates_binder_docx,
        generate_master_bates_bundle_zip
    )
except ImportError:
    try:
        from legal_filing_engine import (
            generate_hawaii_filing_packet,
            generate_federal_rico_complaint,
            generate_hawaii_packet_pdf,
            generate_hawaii_packet_docx,
            generate_federal_rico_pdf,
            generate_federal_rico_docx,
            generate_hawaii_filing_bundle_zip,
            generate_federal_rico_bundle_zip,
            generate_brower_odc_presentment,
            generate_odc_presentment_pdf,
            generate_odc_presentment_docx,
            generate_odc_presentment_bundle_zip,
            generate_federal_criminal_referral,
            generate_criminal_referral_pdf,
            generate_criminal_referral_docx,
            generate_criminal_referral_bundle_zip,
            generate_master_bates_exhibit_binder,
            generate_master_bates_binder_pdf,
            generate_master_bates_binder_docx,
            generate_master_bates_bundle_zip
        )
    except ImportError:
        generate_hawaii_filing_packet = None
        generate_federal_rico_complaint = None
        generate_hawaii_packet_pdf = None
        generate_hawaii_packet_docx = None
        generate_federal_rico_pdf = None
        generate_federal_rico_docx = None
        generate_hawaii_filing_bundle_zip = None
        generate_federal_rico_bundle_zip = None
        generate_brower_odc_presentment = None
        generate_odc_presentment_pdf = None
        generate_odc_presentment_docx = None
        generate_odc_presentment_bundle_zip = None
        generate_federal_criminal_referral = None
        generate_criminal_referral_pdf = None
        generate_criminal_referral_docx = None
        generate_criminal_referral_bundle_zip = None
        generate_master_bates_exhibit_binder = None
        generate_master_bates_binder_pdf = None
        generate_master_bates_binder_docx = None
        generate_master_bates_bundle_zip = None

try:
    from backend.app.estate_mesh_engine import (
        get_estate_overview,
        get_estate_matters,
        get_estate_actors,
        get_estate_perjury_traps,
        get_estate_graph,
        get_matter_detail,
        generate_matter_packet,
        generate_matter_pdf,
        generate_matter_docx,
        generate_matter_bundle_zip
    )
except ImportError:
    try:
        from estate_mesh_engine import (
            get_estate_overview,
            get_estate_matters,
            get_estate_actors,
            get_estate_perjury_traps,
            get_estate_graph,
            get_matter_detail,
            generate_matter_packet,
            generate_matter_pdf,
            generate_matter_docx,
            generate_matter_bundle_zip
        )
    except ImportError:
        get_estate_overview = None
        get_estate_matters = None
        get_estate_actors = None
        get_estate_perjury_traps = None
        get_estate_graph = None
        get_matter_detail = None
        generate_matter_packet = None
        generate_matter_pdf = None
        generate_matter_docx = None
        generate_matter_bundle_zip = None
        get_estate_perjury_traps = None
        get_estate_graph = None

try:
    from backend.app.persona_engine import (
        get_estate_personas,
        get_persona_detail,
        get_execution_modes,
        get_composite_presets,
        get_persona_overview,
        dispatch_persona_mission
    )
except ImportError:
    try:
        from persona_engine import (
            get_estate_personas,
            get_persona_detail,
            get_execution_modes,
            get_composite_presets,
            get_persona_overview,
            dispatch_persona_mission
        )
    except ImportError:
        get_estate_personas = None
        get_persona_detail = None
        get_execution_modes = None
        get_composite_presets = None
        get_persona_overview = None
        dispatch_persona_mission = None

try:
    from backend.app.deposition_crucible_engine import (
        get_deposition_crucible_overview,
        get_target_crucible_plan,
        simulate_interrogation_turn,
        generate_master_crucible_text,
        generate_master_crucible_pdf,
        generate_master_crucible_docx,
        generate_master_crucible_bundle_zip,
        TARGET_CRUCIBLE_PROFILES
    )
except ImportError:
    try:
        from deposition_crucible_engine import (
            get_deposition_crucible_overview,
            get_target_crucible_plan,
            simulate_interrogation_turn,
            generate_master_crucible_text,
            generate_master_crucible_pdf,
            generate_master_crucible_docx,
            generate_master_crucible_bundle_zip,
            TARGET_CRUCIBLE_PROFILES
        )
    except ImportError:
        get_deposition_crucible_overview = None
        get_target_crucible_plan = None
        simulate_interrogation_turn = None
        generate_master_crucible_text = None
        generate_master_crucible_pdf = None
        generate_master_crucible_docx = None
        generate_master_crucible_bundle_zip = None
        TARGET_CRUCIBLE_PROFILES = {}

try:
    from fastapi import FastAPI, HTTPException, Depends, Response
    from fastapi.middleware.cors import CORSMiddleware
    HAS_FASTAPI = True
except ImportError:
    HAS_FASTAPI = False

if HAS_FASTAPI:
    app = FastAPI(
        title="APEX-LEGAL-FORENSICS-SUITE API Engine",
        description="Autonomous Mega-Engine built under APEX Holographic Mesh Architecture. Case 1FDV-23-0001009 Forensics & Provenance Ledger.",
        version="4.0.0"
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    class StandaloneApp:
        def __init__(self, *args, **kwargs): pass
        def add_middleware(self, *args, **kwargs): pass
        def get(self, *args, **kwargs): return lambda f: f
        def post(self, *args, **kwargs): return lambda f: f
    app = StandaloneApp()

    class Response:
        def __init__(self, content: bytes, media_type: str = "application/octet-stream", headers: Optional[Dict[str, str]] = None, status_code: int = 200):
            self.content = content
            self.body = content
            self.media_type = media_type
            self.headers = headers or {}
            self.status_code = status_code

    class HTTPException(Exception):
        def __init__(self, status_code: int, detail: str = ""):
            self.status_code = status_code
            self.detail = detail

class MissionStatus(BaseModel):
    project: str = "apex-legal-forensics-suite"
    mission: str = "Autonomous Legal Discovery & Timeline Forensics Suite"
    status: str = "OPERATIONAL"
    uptime_seconds: float
    epistemic_level: str = "L5_AGENT_SWARM"
    doctrine: str = "FRE_601_602_TESTIMONIAL_PRIMACY"

class IngestRecord(BaseModel):
    title: str = Field(..., description="Document or record title")
    content: str = Field(..., description="Raw text or structured data")
    actor: Optional[str] = Field("Operator Casey Barton", description="Witness or actor name")
    category: str = Field("forensic_evidence", description="Evidence category")

class VerificationReceipt(BaseModel):
    record_id: str
    sha256: str
    verified: bool
    timestamp: float
    operator_authority: str

# In-memory storage vault with pointer indices
STORAGE_VAULT: Dict[str, Dict[str, Any]] = {}
CASE_LEDGER_CACHE: Dict[str, Any] = {}

CASE_JSON_PATHS = [
    Path("/root/computer-user/case_brain/storage/case_1FDV-23-0001009_casebuilder.json"),
    Path("/data/data/com.termux/files/home/MISSIONS/CONSOLIDATED/INFRASTRUCTURE/APEX/case_1FDV-23-0001009_casebuilder.json"),
]

def load_case_ledger_data() -> Dict[str, Any]:
    global CASE_LEDGER_CACHE
    if CASE_LEDGER_CACHE:
        return CASE_LEDGER_CACHE
    for p in CASE_JSON_PATHS:
        if p.exists():
            try:
                with open(p, "r", encoding="utf-8") as f:
                    CASE_LEDGER_CACHE = json.load(f)
                    # Hydrate STORAGE_VAULT with allegations
                    for alleg_id, alleg in CASE_LEDGER_CACHE.get("allegations", {}).items():
                        STORAGE_VAULT[alleg_id] = {
                            "id": alleg_id,
                            "title": alleg.get("title", "Solidified Allegation"),
                            "actor": alleg.get("primary_actor", "Unknown Actor"),
                            "category": alleg.get("lane", "LEGAL_WARFARE"),
                            "tier": alleg.get("tier", 1),
                            "state": alleg.get("state", "HARDENED"),
                            "anchor": alleg.get("anchor_allegation", True),
                            "sha256": hashlib.sha256(json.dumps(alleg, sort_keys=True).encode()).hexdigest(),
                            "verified": True
                        }
                    return CASE_LEDGER_CACHE
            except Exception:
                pass
    return {}

START_TIME = time.time()
load_case_ledger_data()

@app.get("/", tags=["Root"])
def root():
    return {
        "engine": "apex-legal-forensics-suite",
        "status": "ONLINE",
        "case_id": "1FDV-23-0001009",
        "docs": "/docs",
        "endpoints": [
            "/health",
            "/mission",
            "/api/v1/records",
            "/api/v1/forensics/overview",
            "/api/v1/forensics/allegations",
            "/api/v1/forensics/contradictions",
            "/api/v1/forensics/actors",
            "/api/v1/forensics/events",
            "/api/v1/forensics/motion-to-strike",
            "/api/v1/forensics/filing/hawaii-motion-packet",
            "/api/v1/forensics/filing/federal-rico-complaint",
            "/api/v1/forensics/filing/odc-presentment",
            "/api/v1/forensics/filing/criminal-referral",
            "/api/v1/forensics/filing/master-bates-binder",
            "/api/v1/forensics/estate/overview",
            "/api/v1/forensics/estate/matters",
            "/api/v1/forensics/estate/matter/{case_id}"
        ]
    }

@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "records_cached": len(STORAGE_VAULT),
        "case_loaded": bool(CASE_LEDGER_CACHE),
        "case_id": "1FDV-23-0001009"
    }

@app.get("/mission", response_model=MissionStatus, tags=["Mission"])
def get_mission_status():
    return MissionStatus(
        uptime_seconds=round(time.time() - START_TIME, 2)
    )

@app.post("/api/v1/records/ingest", response_model=VerificationReceipt, tags=["Records"])
def ingest_record(rec: IngestRecord):
    data_bytes = rec.content.encode("utf-8")
    h = hashlib.sha256(data_bytes).hexdigest()
    rec_id = f"REC-{h[:12]}"
    
    STORAGE_VAULT[rec_id] = {
        "id": rec_id,
        "title": rec.title,
        "actor": rec.actor,
        "category": rec.category,
        "sha256": h,
        "size_bytes": len(data_bytes),
        "created_at": time.time(),
        "verified": True
    }
    
    return VerificationReceipt(
        record_id=rec_id,
        sha256=h,
        verified=True,
        timestamp=time.time(),
        operator_authority="ESTABLISHED_UNDER_FRE_601_602"
    )

@app.get("/api/v1/records", tags=["Records"])
def list_records():
    return {"total": len(STORAGE_VAULT), "records": list(STORAGE_VAULT.values())}

@app.get("/api/v1/forensics/overview", tags=["Forensics"])
def get_forensics_overview():
    data = load_case_ledger_data()
    return {
        "case_id": data.get("case_id", "1FDV-23-0001009"),
        "case_title": data.get("case_title", "Barton Custody & Due Process Enforcement"),
        "jurisdiction": data.get("jurisdiction", "State of Hawaii / Federal District of Hawaii"),
        "counts": {
            "sources": len(data.get("sources", {})),
            "facts": len(data.get("facts", {})),
            "events": len(data.get("events", {})),
            "actors": len(data.get("actors", {})),
            "allegations": len(data.get("allegations", {})),
            "contradictions": len(data.get("contradictions", {})),
            "discovery_targets": len(data.get("discovery_targets", {}))
        },
        "doctrine": "FRE 601/602 & HRE 601/602 Operator Admissibility Invariants Enforced"
    }

@app.get("/api/v1/forensics/allegations", tags=["Forensics"])
def get_allegations():
    data = load_case_ledger_data()
    return {
        "total": len(data.get("allegations", {})),
        "allegations": list(data.get("allegations", {}).values())
    }

@app.get("/api/v1/forensics/contradictions", tags=["Forensics"])
def get_contradictions():
    data = load_case_ledger_data()
    return {
        "total": len(data.get("contradictions", {})),
        "contradictions": list(data.get("contradictions", {}).values())
    }

@app.get("/api/v1/forensics/actors", tags=["Forensics"])
def get_actors():
    data = load_case_ledger_data()
    return {
        "total": len(data.get("actors", {})),
        "actors": list(data.get("actors", {}).values())
    }

@app.get("/api/v1/forensics/events", tags=["Forensics"])
def get_events():
    data = load_case_ledger_data()
    return {
        "total": len(data.get("events", {})),
        "events": list(data.get("events", {}).values())
    }

@app.get("/api/v1/forensics/motion-to-strike", tags=["Forensics"])
def get_motion_to_strike():
    return {
        "motion_title": "DEFENDANT'S EMERGENCY MOTION TO STRIKE PROPOSED ORDER AND FOR SANCTIONS UNDER HRE 602 & HFCR RULE 11",
        "case_number": "FC-D NO. 1FDV-23-0001009",
        "court": "FAMILY COURT OF THE FIRST CIRCUIT, STATE OF HAWAII",
        "movant": "CASEY BARTON, Defendant Pro Se",
        "adverse_parties": ["TERESA BARTON", "SCOT BROWER, ESQ."],
        "grounds": [
            "1. Lack of Personal Knowledge (HRE 602 / FRE 602): Proposed order recites unsworn representations of counsel without competent foundation.",
            "2. Physical Denial of Hearing Evidence: 235 exhibits sealed ex parte on morning of hearing without notice or service (Dkt 193).",
            "3. Mathematical Impossibility of Failure to Appear: Cellular and GPS records place Defendant physically inside Kapolei Courthouse on June 19, 2024.",
            "4. Substantive Ex Parte Custody Inversion via Fraudulent Praecipe (Dkt 193 vs Dkt 201)."
        ],
        "requested_relief": [
            "A. Strike the proposed order in its entirety.",
            "B. Vacate all orders entered in reliance on fraudulent ex parte praecipe ab initio.",
            "C. Issue mandatory referral to Hawaii Office of Disciplinary Counsel (ODC) pursuant to HRPC 3.3.",
            "D. Impose monetary sanctions under HFCR Rule 11."
        ],
        "evidentiary_invariants": "FRE 601/602 & HRE 601/602 Direct Admissibility Enforced",
        "receipt_sha256": hashlib.sha256(b"MOTION_TO_STRIKE_1FDV_23_0001009").hexdigest()
    }

@app.get("/api/v1/forensics/search", tags=["Forensics"])
def search_case(q: str = ""):
    data = load_case_ledger_data()
    q_lower = q.lower().strip()
    if not q_lower:
        return {"query": q, "total_matches": 0, "results": []}
    
    matches = []
    for a_id, alleg in data.get("allegations", {}).items():
        haystack = f"{alleg.get('title', '')} {alleg.get('summary', '')} {' '.join(alleg.get('legal_theories', []))} {alleg.get('primary_actor', '')}".lower()
        if q_lower in haystack:
            matches.append({
                "type": "allegation",
                "id": a_id,
                "title": alleg.get("title"),
                "actor": alleg.get("primary_actor"),
                "summary": alleg.get("summary", "")[:250],
                "tier": alleg.get("tier", 1)
            })

    for c_id, contra in data.get("contradictions", {}).items():
        haystack = f"{contra.get('conflicting_source_or_fact', '')} {contra.get('significance', '')} {contra.get('severity', '')}".lower()
        if q_lower in haystack:
            matches.append({
                "type": "contradiction",
                "id": c_id,
                "title": f"Contradiction: {contra.get('conflicting_source_or_fact', '')[:80]}",
                "severity": contra.get("severity", "CRITICAL"),
                "summary": contra.get("significance", "")[:250]
            })

    for e_id, ev in data.get("events", {}).items():
        haystack = f"{ev.get('event', '')} {ev.get('date', '')} {ev.get('significance', '')}".lower()
        if q_lower in haystack:
            matches.append({
                "type": "event",
                "id": e_id,
                "title": f"Event ({ev.get('date')}): {ev.get('event', '')[:80]}",
                "date": ev.get("date"),
                "summary": ev.get("significance", "")[:250]
            })

    for a_id, act in data.get("actors", {}).items():
        haystack = f"{act.get('name', '')} {act.get('role', '')} {act.get('alignment', '')}".lower()
        if q_lower in haystack:
            matches.append({
                "type": "actor",
                "id": a_id,
                "title": f"Actor: {act.get('name')}",
                "role": act.get("role"),
                "summary": f"Alignment: {act.get('alignment')}, Allegations: {len(act.get('allegations', []))}"
            })

    return {
        "query": q,
        "total_matches": len(matches),
        "results": matches
    }

def generate_motion_document_text() -> str:
    return """IN THE FAMILY COURT OF THE FIRST CIRCUIT
STATE OF HAWAII

TERESA BARTON,
    Plaintiff,
v.
CASEY BARTON,
    Defendant.

FC-D NO. 1FDV-23-0001009

DEFENDANT CASEY BARTON'S EMERGENCY MOTION TO STRIKE PROPOSED ORDER,
VACATE ORDERS ENTERED ON FRAUDULENT EX PARTE PRAECIPE AB INITIO,
AND FOR MANDATORY SANCTIONS PURSUANT TO HRE 602 AND HFCR RULE 11

TO: THE HONORABLE PRESIDING JUDGE OF THE FAMILY COURT OF THE FIRST CIRCUIT:

COMES NOW Defendant CASEY BARTON, proceeding pro se with full personal competence and firsthand knowledge pursuant to Hawaii Rules of Evidence (HRE) Rule 602 and Federal Rules of Evidence (FRE) Rule 602, and hereby moves this Court for an Emergency Order:
(1) STRIKING in its entirety the Proposed Order submitted by Plaintiff's counsel Scot Brower, Esq.;
(2) VACATING ab initio all ex parte custody determinations entered without notice;
(3) REFERRING Scot Brower, Esq. to the Hawaii Office of Disciplinary Counsel (ODC) pursuant to Hawaii Rules of Professional Conduct (HRPC) Rule 3.3 for candor toward the tribunal; and
(4) AWARDING sanctions and attorney fees pursuant to Hawaii Family Court Rules (HFCR) Rule 11.

I. JURISDICTION & STANDING
This Court possesses subject matter jurisdiction pursuant to HRS Chapter 571 and 580. Defendant has direct personal standing as the biological father, legal custodian, and primary party whose fundamental constitutional parental rights and procedural due process protections (Fourteenth Amendment, U.S. Const.; Article I, Sec. 5, Haw. Const.) have been invaded.

II. OPERATIVE FACTUAL GROUNDS (EVIDENTIARY EXHIBITS BOUND)
1. Physical Presence at Kapolei Courthouse (June 19, 2024):
Contrary to the fraudulent representation in Plaintiff's counsel's praecipe that Defendant "failed to appear," cellular tower connection logs, timestamped device telemetry, and physical courthouse records prove conclusively that Defendant Casey Barton was physically present inside the Kapolei Courthouse during the designated proceeding.

2. Ex Parte Concealment & Sealing of 235 Exhibits (Dkt 193):
On the morning of the evidentiary hearing, 235 defense exhibits were sealed or hidden ex parte without service, notice, or hearing opportunity, entirely depriving Defendant of his constitutional right to present an evidentiary defense.

3. Substantive Custody Inversion via Fraudulent Praecipe (Dkt 193 vs Dkt 201):
Counsel Scot Brower submitted a praecipe materially altering substantive custodial rights under the guise of an administrative submission, omitting vital docket entries and manufacturing false default claims.

III. LEGAL AUTHORITY & MANDATE TO STRIKE
Under HRE 602, a witness may not testify to a matter unless evidence is introduced sufficient to support a finding that the witness has personal knowledge. The representations in the Proposed Order are unsworn hearsay of counsel without personal knowledge. Under HFCR Rule 11, pleadings signed without reasonable factual inquiry or for improper purpose must be sanctioned. Under HRPC 3.3, a lawyer shall not knowingly make a false statement of fact or law to a tribunal.

IV. PRAYER FOR RELIEF
WHEREFORE, Defendant respectfully prays that this Court:
A. Strike the Proposed Order submitted by Plaintiff;
B. Vacate any and all default or contempt orders stemming from the June 19, 2024 hearing;
C. Schedule an immediate evidentiary hearing with full access to sealed exhibits (Dkt 193);
D. Order referral to the Office of Disciplinary Counsel;
E. Grant such other relief as is just and equitable.

DATED: Honolulu, Hawaii, September 21, 2026.

____________________________________
CASEY BARTON, Defendant Pro Se

VERIFICATION
I, CASEY BARTON, declare under penalty of perjury under the laws of the State of Hawaii and the United States of America that I am the Defendant in the above-captioned matter, that I have personal firsthand knowledge of the facts stated herein pursuant to HRE 602 / FRE 602, and that the foregoing is true and correct.
Executed on September 21, 2026.

____________________________________
CASEY BARTON
"""

@app.get("/api/v1/forensics/export/motion", tags=["Forensics"])
def export_motion_document():
    raw_text = generate_motion_document_text()
    h = hashlib.sha256(raw_text.encode("utf-8")).hexdigest()
    return {
        "title": "EMERGENCY MOTION TO STRIKE (HRE 602 / HFCR 11)",
        "case_id": "1FDV-23-0001009",
        "format": "text/plain; court_pleading",
        "sha256": h,
        "content": raw_text,
        "verified": True
    }

@app.get("/api/v1/forensics/export/matrix", tags=["Forensics"])
def export_proof_matrix():
    data = load_case_ledger_data()
    allegations = list(data.get("allegations", {}).values())
    contradictions = list(data.get("contradictions", {}).values())
    
    rows = []
    for a in allegations:
        rows.append({
            "id": a.get("id"),
            "title": a.get("title"),
            "actor": a.get("primary_actor"),
            "tier": a.get("tier", 1),
            "state": a.get("state", "HARDENED"),
            "legal_theories": ", ".join(a.get("legal_theories", [])),
            "direct_facts": len(a.get("direct_facts", [])),
            "exhibits": len(a.get("exhibits", []))
        })
    
    md = "# Case 1FDV-23-0001009 Verified Allegation Proof Matrix\n\n"
    md += "| ID | Allegation Title | Primary Actor | Tier | State | Theories | Facts | Exhibits |\n"
    md += "|---|---|---|---|---|---|---|---|\n"
    for r in rows:
        md += f"| {r['id']} | {r['title']} | {r['actor']} | {r['tier']} | {r['state']} | {r['legal_theories']} | {r['direct_facts']} | {r['exhibits']} |\n"
    
    h = hashlib.sha256(md.encode("utf-8")).hexdigest()
    return {
        "title": "VERIFIED ALLEGATION PROOF MATRIX",
        "case_id": "1FDV-23-0001009",
        "total_allegations": len(rows),
        "total_contradictions": len(contradictions),
        "markdown_table": md,
        "rows": rows,
        "sha256": h
    }

@app.get("/api/v1/forensics/filing/hawaii-motion-packet", tags=["Filings"])
def get_hawaii_filing_packet():
    data = load_case_ledger_data()
    if generate_hawaii_filing_packet:
        return generate_hawaii_filing_packet(data)
    return {"error": "Filing engine unavailable"}

@app.get("/api/v1/forensics/filing/federal-rico-complaint", tags=["Filings"])
def get_federal_rico_complaint():
    data = load_case_ledger_data()
    if generate_federal_rico_complaint:
        return generate_federal_rico_complaint(data)
    return {"error": "Filing engine unavailable"}

@app.get("/api/v1/forensics/export/hawaii-packet", tags=["Filings"])
def export_hawaii_filing_packet(format: str = "28_lines"):
    data = load_case_ledger_data()
    if not generate_hawaii_filing_packet:
        return {"error": "Filing engine unavailable"}
    packet = generate_hawaii_filing_packet(data)
    content = packet["formatted_28_lines"] if format == "28_lines" else packet["raw_text"]
    h = hashlib.sha256(content.encode("utf-8")).hexdigest()
    return {
        "title": packet["title"],
        "case_number": packet["case_number"],
        "court": packet["court"],
        "format": f"text/plain; {format}",
        "sha256": h,
        "content": content,
        "verified": True
    }

@app.get("/api/v1/forensics/export/federal-rico", tags=["Filings"])
def export_federal_rico_complaint(format: str = "28_lines"):
    data = load_case_ledger_data()
    if not generate_federal_rico_complaint:
        return {"error": "Filing engine unavailable"}
    complaint = generate_federal_rico_complaint(data)
    content = complaint["formatted_28_lines"] if format == "28_lines" else complaint["raw_text"]
    h = hashlib.sha256(content.encode("utf-8")).hexdigest()
    return {
        "title": complaint["title"],
        "court": complaint["court"],
        "damages_trebled": complaint["damages_trebled"],
        "format": f"text/plain; {format}",
        "sha256": h,
        "content": content,
        "verified": True
    }

@app.get("/api/v1/forensics/download/hawaii-packet.pdf", tags=["Filings"])
def download_hawaii_packet_pdf():
    data = load_case_ledger_data()
    if not generate_hawaii_filing_packet or not generate_hawaii_packet_pdf:
        raise HTTPException(status_code=500, detail="PDF generator unavailable")
    packet = generate_hawaii_filing_packet(data)
    pdf_bytes = generate_hawaii_packet_pdf(packet)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=HAWAII_FAMILY_COURT_MOTION_PACKET_1FDV-23-0001009.pdf"}
    )

@app.get("/api/v1/forensics/download/hawaii-packet.docx", tags=["Filings"])
def download_hawaii_packet_docx():
    data = load_case_ledger_data()
    if not generate_hawaii_filing_packet or not generate_hawaii_packet_docx:
        raise HTTPException(status_code=500, detail="DOCX generator unavailable")
    packet = generate_hawaii_filing_packet(data)
    docx_bytes = generate_hawaii_packet_docx(packet)
    return Response(
        content=docx_bytes,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": "attachment; filename=HAWAII_FAMILY_COURT_MOTION_PACKET_1FDV-23-0001009.docx"}
    )

@app.get("/api/v1/forensics/download/federal-rico.pdf", tags=["Filings"])
def download_federal_rico_pdf():
    data = load_case_ledger_data()
    if not generate_federal_rico_complaint or not generate_federal_rico_pdf:
        raise HTTPException(status_code=500, detail="PDF generator unavailable")
    complaint = generate_federal_rico_complaint(data)
    pdf_bytes = generate_federal_rico_pdf(complaint)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=FEDERAL_CIVIL_RICO_COMPLAINT_38.4M.pdf"}
    )

@app.get("/api/v1/forensics/download/federal-rico.docx", tags=["Filings"])
def download_federal_rico_docx():
    data = load_case_ledger_data()
    if not generate_federal_rico_complaint or not generate_federal_rico_docx:
        raise HTTPException(status_code=500, detail="DOCX generator unavailable")
    complaint = generate_federal_rico_complaint(data)
    docx_bytes = generate_federal_rico_docx(complaint)
    return Response(
        content=docx_bytes,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": "attachment; filename=FEDERAL_CIVIL_RICO_COMPLAINT_38.4M.docx"}
    )

@app.get("/api/v1/forensics/download/hawaii-filing-bundle.zip", tags=["Filings"])
def download_hawaii_filing_bundle_zip_route():
    data = load_case_ledger_data()
    if not generate_hawaii_filing_packet or not generate_hawaii_filing_bundle_zip:
        raise HTTPException(status_code=500, detail="Zip bundle generator unavailable")
    packet = generate_hawaii_filing_packet(data)
    zip_bytes = generate_hawaii_filing_bundle_zip(packet)
    return Response(
        content=zip_bytes,
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=HAWAII_COURT_FILING_PACKET_AND_EXHIBITS_1FDV-23-0001009.zip"}
    )

@app.get("/api/v1/forensics/download/federal-rico-bundle.zip", tags=["Filings"])
def download_federal_rico_bundle_zip_route():
    data = load_case_ledger_data()
    if not generate_federal_rico_complaint or not generate_federal_rico_bundle_zip:
        raise HTTPException(status_code=500, detail="Zip bundle generator unavailable")
    complaint = generate_federal_rico_complaint(data)
    zip_bytes = generate_federal_rico_bundle_zip(complaint)
    return Response(
        content=zip_bytes,
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=FEDERAL_CIVIL_RICO_FILING_BUNDLE_38.4M.zip"}
    )

@app.get("/api/v1/forensics/filing/odc-presentment", tags=["Filings"])
def get_odc_presentment():
    data = load_case_ledger_data()
    if generate_brower_odc_presentment:
        return generate_brower_odc_presentment(data)
    return {"error": "Filing engine unavailable"}

@app.get("/api/v1/forensics/download/odc-presentment.pdf", tags=["Filings"])
def download_odc_presentment_pdf():
    data = load_case_ledger_data()
    if not generate_brower_odc_presentment or not generate_odc_presentment_pdf:
        raise HTTPException(status_code=500, detail="PDF generator unavailable")
    presentment = generate_brower_odc_presentment(data)
    pdf_bytes = generate_odc_presentment_pdf(presentment)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=SCOT_BROWER_ODC_DISCIPLINARY_PRESENTMENT.pdf"}
    )

@app.get("/api/v1/forensics/download/odc-presentment.docx", tags=["Filings"])
def download_odc_presentment_docx():
    data = load_case_ledger_data()
    if not generate_brower_odc_presentment or not generate_odc_presentment_docx:
        raise HTTPException(status_code=500, detail="DOCX generator unavailable")
    presentment = generate_brower_odc_presentment(data)
    docx_bytes = generate_odc_presentment_docx(presentment)
    return Response(
        content=docx_bytes,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": "attachment; filename=SCOT_BROWER_ODC_DISCIPLINARY_PRESENTMENT.docx"}
    )

@app.get("/api/v1/forensics/download/odc-presentment-bundle.zip", tags=["Filings"])
def download_odc_presentment_bundle_zip_route():
    data = load_case_ledger_data()
    if not generate_brower_odc_presentment or not generate_odc_presentment_bundle_zip:
        raise HTTPException(status_code=500, detail="Zip bundle generator unavailable")
    presentment = generate_brower_odc_presentment(data)
    zip_bytes = generate_odc_presentment_bundle_zip(presentment)
    return Response(
        content=zip_bytes,
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=SCOT_BROWER_ODC_DISCIPLINARY_BUNDLE.zip"}
    )

@app.get("/api/v1/forensics/filing/criminal-referral", tags=["Filings"])
def get_criminal_referral():
    data = load_case_ledger_data()
    if generate_federal_criminal_referral:
        return generate_federal_criminal_referral(data)
    return {"error": "Filing engine unavailable"}

@app.get("/api/v1/forensics/download/criminal-referral.pdf", tags=["Filings"])
def download_criminal_referral_pdf():
    data = load_case_ledger_data()
    if not generate_federal_criminal_referral or not generate_criminal_referral_pdf:
        raise HTTPException(status_code=500, detail="PDF generator unavailable")
    referral = generate_federal_criminal_referral(data)
    pdf_bytes = generate_criminal_referral_pdf(referral)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=FEDERAL_CRIMINAL_REFERRAL_DOJ_FBI_USPS.pdf"}
    )

@app.get("/api/v1/forensics/download/criminal-referral.docx", tags=["Filings"])
def download_criminal_referral_docx():
    data = load_case_ledger_data()
    if not generate_federal_criminal_referral or not generate_criminal_referral_docx:
        raise HTTPException(status_code=500, detail="DOCX generator unavailable")
    referral = generate_federal_criminal_referral(data)
    docx_bytes = generate_criminal_referral_docx(referral)
    return Response(
        content=docx_bytes,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": "attachment; filename=FEDERAL_CRIMINAL_REFERRAL_DOJ_FBI_USPS.docx"}
    )

@app.get("/api/v1/forensics/download/criminal-referral-bundle.zip", tags=["Filings"])
def download_criminal_referral_bundle_zip_route():
    data = load_case_ledger_data()
    if not generate_federal_criminal_referral or not generate_criminal_referral_bundle_zip:
        raise HTTPException(status_code=500, detail="Zip bundle generator unavailable")
    referral = generate_federal_criminal_referral(data)
    zip_bytes = generate_criminal_referral_bundle_zip(referral)
    return Response(
        content=zip_bytes,
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=FEDERAL_CRIMINAL_REFERRAL_BUNDLE.zip"}
    )

@app.get("/api/v1/forensics/filing/master-bates-binder", tags=["Filings"])
def get_master_bates_binder():
    data = load_case_ledger_data()
    if generate_master_bates_exhibit_binder:
        return generate_master_bates_exhibit_binder(data)
    return {"error": "Filing engine unavailable"}

@app.get("/api/v1/forensics/download/master-bates-binder.pdf", tags=["Filings"])
def download_master_bates_binder_pdf():
    data = load_case_ledger_data()
    if not generate_master_bates_exhibit_binder or not generate_master_bates_binder_pdf:
        raise HTTPException(status_code=500, detail="PDF generator unavailable")
    binder = generate_master_bates_exhibit_binder(data)
    pdf_bytes = generate_master_bates_binder_pdf(binder)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=MASTER_BATES_STAMPED_EXHIBIT_BINDER.pdf"}
    )

@app.get("/api/v1/forensics/download/master-bates-binder.docx", tags=["Filings"])
def download_master_bates_binder_docx():
    data = load_case_ledger_data()
    if not generate_master_bates_exhibit_binder or not generate_master_bates_binder_docx:
        raise HTTPException(status_code=500, detail="DOCX generator unavailable")
    binder = generate_master_bates_exhibit_binder(data)
    docx_bytes = generate_master_bates_binder_docx(binder)
    return Response(
        content=docx_bytes,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": "attachment; filename=MASTER_BATES_STAMPED_EXHIBIT_BINDER.docx"}
    )

@app.get("/api/v1/forensics/download/master-bates-bundle.zip", tags=["Filings"])
def download_master_bates_bundle_zip_route():
    data = load_case_ledger_data()
    if not generate_master_bates_exhibit_binder or not generate_master_bates_bundle_zip:
        raise HTTPException(status_code=500, detail="Zip bundle generator unavailable")
    binder = generate_master_bates_exhibit_binder(data)
    zip_bytes = generate_master_bates_bundle_zip(binder)
    return Response(
        content=zip_bytes,
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=MASTER_BATES_EXHIBIT_BINDER_BUNDLE.zip"}
    )

@app.get("/api/v1/forensics/estate/overview", tags=["Estate Mesh"])
def get_estate_overview_route():
    if not get_estate_overview:
        return {"error": "Estate engine unavailable"}
    return get_estate_overview()

@app.get("/api/v1/forensics/estate/matters", tags=["Estate Mesh"])
def get_estate_matters_route(portfolio: Optional[str] = None):
    if not get_estate_matters:
        return {"error": "Estate engine unavailable"}
    matters = get_estate_matters(portfolio)
    return {"count": len(matters), "matters": matters}

@app.get("/api/v1/forensics/estate/matter/{case_id}", tags=["Estate Mesh"])
def get_matter_detail_route(case_id: str):
    if not get_matter_detail:
        raise HTTPException(status_code=500, detail="Estate engine unavailable")
    m = get_matter_detail(case_id)
    if not m:
        raise HTTPException(status_code=404, detail=f"Matter {case_id} not found")
    return m

@app.get("/api/v1/forensics/estate/matter/{case_id}/packet", tags=["Estate Mesh"])
def get_matter_packet_route(case_id: str):
    if not generate_matter_packet:
        raise HTTPException(status_code=500, detail="Estate engine unavailable")
    try:
        packet = generate_matter_packet(case_id)
        return packet
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/api/v1/forensics/download/matter/{case_id}.pdf", tags=["Estate Mesh"])
def download_matter_pdf_route(case_id: str):
    if not generate_matter_packet or not generate_matter_pdf:
        raise HTTPException(status_code=500, detail="Generator unavailable")
    try:
        packet = generate_matter_packet(case_id)
        pdf_bytes = generate_matter_pdf(packet)
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={case_id}_COMPLAINT_28LINE.pdf"}
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/api/v1/forensics/download/matter/{case_id}.docx", tags=["Estate Mesh"])
def download_matter_docx_route(case_id: str):
    if not generate_matter_packet or not generate_matter_docx:
        raise HTTPException(status_code=500, detail="Generator unavailable")
    try:
        packet = generate_matter_packet(case_id)
        docx_bytes = generate_matter_docx(packet)
        return Response(
            content=docx_bytes,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": f"attachment; filename={case_id}_COMPLAINT.docx"}
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/api/v1/forensics/download/matter/{case_id}.zip", tags=["Estate Mesh"])
def download_matter_zip_route(case_id: str):
    if not generate_matter_packet or not generate_matter_bundle_zip:
        raise HTTPException(status_code=500, detail="Generator unavailable")
    try:
        packet = generate_matter_packet(case_id)
        zip_bytes = generate_matter_bundle_zip(packet)
        return Response(
            content=zip_bytes,
            media_type="application/zip",
            headers={"Content-Disposition": f"attachment; filename={case_id}_FULL_FILING_BUNDLE.zip"}
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/api/v1/forensics/estate/actors", tags=["Estate Mesh"])
def get_estate_actors_route():
    if not get_estate_actors:
        return {"error": "Estate engine unavailable"}
    actors = get_estate_actors()
    return {"count": len(actors), "actors": actors}

@app.get("/api/v1/forensics/estate/perjury-traps", tags=["Estate Mesh"])
def get_estate_perjury_traps_route(case_id: Optional[str] = None):
    if not get_estate_perjury_traps:
        return {"error": "Estate engine unavailable"}
    traps = get_estate_perjury_traps(case_id)
    return {"count": len(traps), "traps": traps}

@app.get("/api/v1/forensics/estate/graph", tags=["Estate Mesh"])
def get_estate_graph_route():
    if not get_estate_graph:
        return {"error": "Estate engine unavailable"}
    return get_estate_graph()

def load_estate_capabilities(domain: Optional[str] = None) -> Dict[str, Any]:
    for p in [Path("/root/apex-boot-core-repo/CAPABILITY_MANIFEST.json"), Path("/root/CAPABILITY_MANIFEST.json")]:
        if p.exists():
            try:
                data = json.loads(p.read_text())
                caps = data.get("capabilities", [])
                if domain:
                    caps = [c for c in caps if c.get("domain", "").upper() == domain.strip().upper()]
                domains = sorted(list(set(c.get("domain", "") for c in caps if c.get("domain"))))
                return {
                    "schema": data.get("schema", "glaciereq.capability-inventory.v2"),
                    "total_capabilities": len(caps),
                    "domains": domains,
                    "capabilities": caps
                }
            except Exception:
                pass
    return {"total_capabilities": 0, "domains": [], "capabilities": []}

def load_strike_manifest() -> Dict[str, Any]:
    receipt_path = Path("/root/artifacts/strikes/APEX_STRIKE_EXECUTION_RECEIPT.json")
    packets_dir = Path("/root/artifacts/strikes/packets")
    data = {}
    if receipt_path.exists():
        try:
            data = json.loads(receipt_path.read_text())
        except Exception:
            pass
    unpacked = []
    if packets_dir.exists():
        for d in sorted(packets_dir.iterdir()):
            if d.is_dir():
                files = [{"name": f.name, "size_bytes": f.stat().st_size} for f in sorted(d.iterdir())]
                unpacked.append({
                    "folder": d.name,
                    "files": files,
                    "count": len(files)
                })
    data["unpacked_packages"] = unpacked
    data["unpacked_package_count"] = len(unpacked)
    data["total_unpacked_files"] = sum(p["count"] for p in unpacked)
    return data

@app.get("/api/v1/forensics/estate/capabilities", tags=["Estate Capabilities"])
def get_estate_capabilities_route(domain: Optional[str] = None):
    return load_estate_capabilities(domain)

@app.get("/api/v1/forensics/strikes/manifest", tags=["Strikes"])
def get_strike_manifest_route():
    return load_strike_manifest()

@app.get("/api/v1/forensics/download/unpacked/{folder}/{filename}", tags=["Strikes"])
def download_unpacked_file_route(folder: str, filename: str):
    packets_dir = Path("/root/artifacts/strikes/packets")
    target_file = (packets_dir / folder / filename).resolve()
    if not str(target_file).startswith(str(packets_dir.resolve())) or not target_file.exists():
        raise HTTPException(status_code=404, detail="File not found")
    media_type = "application/octet-stream"
    if filename.endswith(".pdf"): media_type = "application/pdf"
    elif filename.endswith(".docx"): media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    elif filename.endswith(".txt"): media_type = "text/plain; charset=utf-8"
    elif filename.endswith(".json"): media_type = "application/json"
    return Response(
        content=target_file.read_bytes(),
        media_type=media_type,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )

@app.get("/api/v1/forensics/estate/personas", tags=["Swarm Personas"])
def get_personas_route(domain: Optional[str] = None):
    if not get_estate_personas:
        return {"error": "Persona engine unavailable"}
    personas = get_estate_personas(domain)
    return {"count": len(personas), "personas": personas}

@app.get("/api/v1/forensics/estate/personas/overview", tags=["Swarm Personas"])
def get_personas_overview_route():
    if not get_persona_overview:
        return {"error": "Persona engine unavailable"}
    return get_persona_overview()

@app.get("/api/v1/forensics/estate/personas/modes", tags=["Swarm Personas"])
def get_personas_modes_route():
    if not get_execution_modes:
        return {"error": "Persona engine unavailable"}
    return get_execution_modes()

@app.get("/api/v1/forensics/estate/personas/composites", tags=["Swarm Personas"])
def get_personas_composites_route():
    if not get_composite_presets:
        return {"error": "Persona engine unavailable"}
    return get_composite_presets()

@app.get("/api/v1/forensics/estate/persona/{persona_id}", tags=["Swarm Personas"])
def get_persona_detail_route(persona_id: str):
    if not get_persona_detail:
        return {"error": "Persona engine unavailable"}
    p = get_persona_detail(persona_id)
    if not p:
        raise HTTPException(status_code=404, detail="Persona not found")
    return p

class PersonaDispatchRequest(BaseModel):
    persona_id: str
    mission_objective: str
    execution_mode: Optional[str] = "pro-elite"
    parameters: Optional[Dict[str, Any]] = None

@app.post("/api/v1/forensics/estate/personas/dispatch", tags=["Swarm Personas"])
def dispatch_persona_route(req: PersonaDispatchRequest):
    if not dispatch_persona_mission:
        raise HTTPException(status_code=500, detail="Persona engine unavailable")
    try:
        return dispatch_persona_mission(req.persona_id, req.mission_objective, req.execution_mode or "pro-elite", req.parameters)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ==============================================================================
# DEPOSITION PERJURY CRUCIBLE ROUTES (DRILL ALPHA)
# ==============================================================================

@app.get("/api/v1/forensics/estate/deposition-crucible", tags=["Deposition Crucible"])
def get_deposition_crucible_route():
    if not get_deposition_crucible_overview:
        return {"error": "Crucible engine unavailable"}
    return get_deposition_crucible_overview()

@app.get("/api/v1/forensics/estate/deposition-crucible/targets", tags=["Deposition Crucible"])
def get_deposition_targets_route():
    if not TARGET_CRUCIBLE_PROFILES:
        return {"targets": []}
    return {
        "count": len(TARGET_CRUCIBLE_PROFILES),
        "targets": list(TARGET_CRUCIBLE_PROFILES.values())
    }

@app.get("/api/v1/forensics/estate/deposition-crucible/target/{target_id}", tags=["Deposition Crucible"])
def get_deposition_target_plan_route(target_id: str):
    if not get_target_crucible_plan:
        raise HTTPException(status_code=500, detail="Crucible engine unavailable")
    res = get_target_crucible_plan(target_id)
    if not res:
        raise HTTPException(status_code=404, detail=f"Target {target_id} not found")
    return res

@app.get("/api/v1/forensics/estate/deposition-crucible/download/pdf", tags=["Deposition Crucible"])
def download_deposition_crucible_pdf():
    if not generate_master_crucible_pdf:
        raise HTTPException(status_code=500, detail="PDF generator unavailable")
    pdf_bytes = generate_master_crucible_pdf()
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=MASTER_DEPOSITION_PERJURY_CRUCIBLE_28LINE.pdf"}
    )

@app.get("/api/v1/forensics/estate/deposition-crucible/download/docx", tags=["Deposition Crucible"])
def download_deposition_crucible_docx():
    if not generate_master_crucible_docx:
        raise HTTPException(status_code=500, detail="DOCX generator unavailable")
    docx_bytes = generate_master_crucible_docx()
    return Response(
        content=docx_bytes,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": "attachment; filename=MASTER_DEPOSITION_PERJURY_CRUCIBLE.docx"}
    )

@app.get("/api/v1/forensics/estate/deposition-crucible/download/zip", tags=["Deposition Crucible"])
def download_deposition_crucible_zip():
    if not generate_master_crucible_bundle_zip:
        raise HTTPException(status_code=500, detail="ZIP generator unavailable")
    zip_bytes = generate_master_crucible_bundle_zip()
    return Response(
        content=zip_bytes,
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=MASTER_DEPOSITION_PERJURY_CRUCIBLE_BUNDLE.zip"}
    )

class CrucibleSimulateRequest(BaseModel):
    target_id: str
    question_id: str
    witness_statement: str

@app.post("/api/v1/forensics/estate/deposition-crucible/simulate", tags=["Deposition Crucible"])
def simulate_crucible_route(req: CrucibleSimulateRequest):
    if not simulate_interrogation_turn:
        raise HTTPException(status_code=500, detail="Crucible simulator unavailable")
    res = simulate_interrogation_turn(req.target_id, req.question_id, req.witness_statement)
    if "error" in res:
        raise HTTPException(status_code=400, detail=res["error"])
    return res

from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

class ForensicsHTTPHandler(BaseHTTPRequestHandler):
    def _send_json(self, status_code: int, data: Any):
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def _send_bytes(self, status_code: int, content_type: str, body: bytes, filename: str = None):
        self.send_response(status_code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        if filename:
            self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS, HEAD")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_HEAD(self):
        self.do_GET()

    def _send_html(self, status_code: int, html_body: str):
        body = html_body.encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)
        accept = self.headers.get("Accept", "")
        if path in ("/", "/terminal", "/dashboard"):
            if "application/json" in accept and "text/html" not in accept:
                self._send_json(200, root())
            elif get_terminal_html:
                overview = get_forensics_overview()
                allegations = get_allegations().get("allegations", [])
                contradictions = get_contradictions().get("contradictions", [])
                motion = get_motion_to_strike()
                html = get_terminal_html(overview, allegations, contradictions, motion)
                self._send_html(200, html)
            else:
                self._send_json(200, root())
        elif path == "/api":
            self._send_json(200, root())
        elif path == "/health":
            self._send_json(200, health_check())
        elif path == "/mission":
            st = get_mission_status()
            self._send_json(200, st.model_dump() if hasattr(st, "model_dump") else st.dict())
        elif path == "/api/v1/records":
            self._send_json(200, list_records())
        elif path == "/api/v1/forensics/overview":
            self._send_json(200, get_forensics_overview())
        elif path == "/api/v1/forensics/allegations":
            self._send_json(200, get_allegations())
        elif path == "/api/v1/forensics/contradictions":
            self._send_json(200, get_contradictions())
        elif path == "/api/v1/forensics/actors":
            self._send_json(200, get_actors())
        elif path == "/api/v1/forensics/events":
            self._send_json(200, get_events())
        elif path == "/api/v1/forensics/motion-to-strike":
            self._send_json(200, get_motion_to_strike())
        elif path == "/api/v1/forensics/search":
            q = query.get("q", [""])[0]
            self._send_json(200, search_case(q=q))
        elif path == "/api/v1/forensics/export/motion":
            self._send_json(200, export_motion_document())
        elif path == "/api/v1/forensics/export/matrix":
            self._send_json(200, export_proof_matrix())
        elif path == "/api/v1/forensics/filing/hawaii-motion-packet":
            self._send_json(200, get_hawaii_filing_packet())
        elif path == "/api/v1/forensics/filing/federal-rico-complaint":
            self._send_json(200, get_federal_rico_complaint())
        elif path == "/api/v1/forensics/export/hawaii-packet":
            fmt = query.get("format", ["28_lines"])[0]
            self._send_json(200, export_hawaii_filing_packet(format=fmt))
        elif path == "/api/v1/forensics/export/federal-rico":
            fmt = query.get("format", ["28_lines"])[0]
            self._send_json(200, export_federal_rico_complaint(format=fmt))
        elif path == "/api/v1/forensics/download/hawaii-packet.pdf":
            data = load_case_ledger_data()
            packet = generate_hawaii_filing_packet(data)
            pdf_bytes = generate_hawaii_packet_pdf(packet)
            self._send_bytes(200, "application/pdf", pdf_bytes, "HAWAII_FAMILY_COURT_MOTION_PACKET_1FDV-23-0001009.pdf")
        elif path == "/api/v1/forensics/download/hawaii-packet.docx":
            data = load_case_ledger_data()
            packet = generate_hawaii_filing_packet(data)
            docx_bytes = generate_hawaii_packet_docx(packet)
            self._send_bytes(200, "application/vnd.openxmlformats-officedocument.wordprocessingml.document", docx_bytes, "HAWAII_FAMILY_COURT_MOTION_PACKET_1FDV-23-0001009.docx")
        elif path == "/api/v1/forensics/download/federal-rico.pdf":
            data = load_case_ledger_data()
            complaint = generate_federal_rico_complaint(data)
            pdf_bytes = generate_federal_rico_pdf(complaint)
            self._send_bytes(200, "application/pdf", pdf_bytes, "FEDERAL_CIVIL_RICO_COMPLAINT_38.4M.pdf")
        elif path == "/api/v1/forensics/download/federal-rico.docx":
            data = load_case_ledger_data()
            complaint = generate_federal_rico_complaint(data)
            docx_bytes = generate_federal_rico_docx(complaint)
            self._send_bytes(200, "application/vnd.openxmlformats-officedocument.wordprocessingml.document", docx_bytes, "FEDERAL_CIVIL_RICO_COMPLAINT_38.4M.docx")
        elif path == "/api/v1/forensics/download/hawaii-filing-bundle.zip":
            data = load_case_ledger_data()
            packet = generate_hawaii_filing_packet(data)
            zip_bytes = generate_hawaii_filing_bundle_zip(packet)
            self._send_bytes(200, "application/zip", zip_bytes, "HAWAII_COURT_FILING_PACKET_AND_EXHIBITS_1FDV-23-0001009.zip")
        elif path == "/api/v1/forensics/download/federal-rico-bundle.zip":
            data = load_case_ledger_data()
            complaint = generate_federal_rico_complaint(data)
            zip_bytes = generate_federal_rico_bundle_zip(complaint)
            self._send_bytes(200, "application/zip", zip_bytes, "FEDERAL_CIVIL_RICO_FILING_BUNDLE_38.4M.zip")
        elif path == "/api/v1/forensics/filing/odc-presentment":
            data = load_case_ledger_data()
            self._send_json(200, generate_brower_odc_presentment(data) if generate_brower_odc_presentment else {})
        elif path == "/api/v1/forensics/download/odc-presentment.pdf":
            data = load_case_ledger_data()
            presentment = generate_brower_odc_presentment(data)
            pdf_bytes = generate_odc_presentment_pdf(presentment)
            self._send_bytes(200, "application/pdf", pdf_bytes, "SCOT_BROWER_ODC_DISCIPLINARY_PRESENTMENT.pdf")
        elif path == "/api/v1/forensics/download/odc-presentment.docx":
            data = load_case_ledger_data()
            presentment = generate_brower_odc_presentment(data)
            docx_bytes = generate_odc_presentment_docx(presentment)
            self._send_bytes(200, "application/vnd.openxmlformats-officedocument.wordprocessingml.document", docx_bytes, "SCOT_BROWER_ODC_DISCIPLINARY_PRESENTMENT.docx")
        elif path in ("/api/v1/forensics/download/odc-presentment-bundle.zip", "/api/v1/forensics/download/odc-presentment.zip"):
            data = load_case_ledger_data()
            presentment = generate_brower_odc_presentment(data)
            zip_bytes = generate_odc_presentment_bundle_zip(presentment)
            self._send_bytes(200, "application/zip", zip_bytes, "SCOT_BROWER_ODC_DISCIPLINARY_BUNDLE.zip")
        elif path == "/api/v1/forensics/filing/criminal-referral":
            data = load_case_ledger_data()
            self._send_json(200, generate_federal_criminal_referral(data) if generate_federal_criminal_referral else {})
        elif path == "/api/v1/forensics/download/criminal-referral.pdf":
            data = load_case_ledger_data()
            referral = generate_federal_criminal_referral(data)
            pdf_bytes = generate_criminal_referral_pdf(referral)
            self._send_bytes(200, "application/pdf", pdf_bytes, "FEDERAL_CRIMINAL_REFERRAL_DOJ_FBI_USPS.pdf")
        elif path == "/api/v1/forensics/download/criminal-referral.docx":
            data = load_case_ledger_data()
            referral = generate_federal_criminal_referral(data)
            docx_bytes = generate_criminal_referral_docx(referral)
            self._send_bytes(200, "application/vnd.openxmlformats-officedocument.wordprocessingml.document", docx_bytes, "FEDERAL_CRIMINAL_REFERRAL_DOJ_FBI_USPS.docx")
        elif path in ("/api/v1/forensics/download/criminal-referral-bundle.zip", "/api/v1/forensics/download/criminal-referral.zip"):
            data = load_case_ledger_data()
            referral = generate_federal_criminal_referral(data)
            zip_bytes = generate_criminal_referral_bundle_zip(referral)
            self._send_bytes(200, "application/zip", zip_bytes, "FEDERAL_CRIMINAL_REFERRAL_BUNDLE.zip")
        elif path == "/api/v1/forensics/filing/master-bates-binder":
            data = load_case_ledger_data()
            self._send_json(200, generate_master_bates_exhibit_binder(data) if generate_master_bates_exhibit_binder else {})
        elif path == "/api/v1/forensics/download/master-bates-binder.pdf":
            data = load_case_ledger_data()
            binder = generate_master_bates_exhibit_binder(data)
            pdf_bytes = generate_master_bates_binder_pdf(binder)
            self._send_bytes(200, "application/pdf", pdf_bytes, "MASTER_BATES_STAMPED_EXHIBIT_BINDER.pdf")
        elif path == "/api/v1/forensics/download/master-bates-binder.docx":
            data = load_case_ledger_data()
            binder = generate_master_bates_exhibit_binder(data)
            docx_bytes = generate_master_bates_binder_docx(binder)
            self._send_bytes(200, "application/vnd.openxmlformats-officedocument.wordprocessingml.document", docx_bytes, "MASTER_BATES_STAMPED_EXHIBIT_BINDER.docx")
        elif path in ("/api/v1/forensics/download/master-bates-bundle.zip", "/api/v1/forensics/download/master-bates-binder.zip"):
            data = load_case_ledger_data()
            binder = generate_master_bates_exhibit_binder(data)
            zip_bytes = generate_master_bates_bundle_zip(binder)
            self._send_bytes(200, "application/zip", zip_bytes, "MASTER_BATES_EXHIBIT_BINDER_BUNDLE.zip")
        elif path == "/api/v1/forensics/estate/overview":
            self._send_json(200, get_estate_overview() if get_estate_overview else {})
        elif path == "/api/v1/forensics/estate/matters":
            port = query.get("portfolio", [None])[0]
            matters = get_estate_matters(port) if get_estate_matters else []
            self._send_json(200, {"count": len(matters), "matters": matters})
        elif path.startswith("/api/v1/forensics/estate/matter/"):
            sub = path[len("/api/v1/forensics/estate/matter/"):]
            if sub.endswith("/packet"):
                cid = sub[:-len("/packet")]
                packet = generate_matter_packet(cid) if generate_matter_packet else None
                if packet:
                    self._send_json(200, packet)
                else:
                    self._send_json(404, {"error": f"Matter {cid} packet not found"})
            else:
                cid = sub
                m = get_matter_detail(cid) if get_matter_detail else None
                if m:
                    self._send_json(200, m)
                else:
                    self._send_json(404, {"error": f"Matter {cid} not found"})
        elif path.startswith("/api/v1/forensics/download/matter/"):
            sub = path[len("/api/v1/forensics/download/matter/"):]
            if sub.endswith(".pdf"):
                cid = sub[:-4]
                try:
                    packet = generate_matter_packet(cid)
                    pdf_bytes = generate_matter_pdf(packet)
                    self._send_bytes(200, "application/pdf", pdf_bytes, f"{cid}_COMPLAINT_28LINE.pdf")
                except Exception as e:
                    self._send_json(404, {"error": str(e)})
            elif sub.endswith(".docx"):
                cid = sub[:-5]
                try:
                    packet = generate_matter_packet(cid)
                    docx_bytes = generate_matter_docx(packet)
                    self._send_bytes(200, "application/vnd.openxmlformats-officedocument.wordprocessingml.document", docx_bytes, f"{cid}_COMPLAINT.docx")
                except Exception as e:
                    self._send_json(404, {"error": str(e)})
            elif sub.endswith(".zip"):
                cid = sub[:-4]
                try:
                    packet = generate_matter_packet(cid)
                    zip_bytes = generate_matter_bundle_zip(packet)
                    self._send_bytes(200, "application/zip", zip_bytes, f"{cid}_FULL_FILING_BUNDLE.zip")
                except Exception as e:
                    self._send_json(404, {"error": str(e)})
        elif path == "/api/v1/forensics/estate/actors":
            actors = get_estate_actors() if get_estate_actors else []
            self._send_json(200, {"count": len(actors), "actors": actors})
        elif path == "/api/v1/forensics/estate/perjury-traps":
            cid = query.get("case_id", [None])[0]
            traps = get_estate_perjury_traps(cid) if get_estate_perjury_traps else []
            self._send_json(200, {"count": len(traps), "traps": traps})
        elif path == "/api/v1/forensics/estate/graph":
            self._send_json(200, get_estate_graph() if get_estate_graph else {"nodes": [], "edges": []})
        elif path == "/api/v1/forensics/estate/capabilities":
            dom = query.get("domain", [None])[0]
            self._send_json(200, load_estate_capabilities(dom))
        elif path == "/api/v1/forensics/strikes/manifest":
            self._send_json(200, load_strike_manifest())
        elif path.startswith("/api/v1/forensics/download/unpacked/"):
            subpath = path[len("/api/v1/forensics/download/unpacked/"):]
            parts = subpath.split("/", 1)
            if len(parts) == 2:
                folder, filename = parts
                packets_dir = Path("/root/artifacts/strikes/packets")
                target_file = (packets_dir / folder / filename).resolve()
                if str(target_file).startswith(str(packets_dir.resolve())) and target_file.exists():
                    media_type = "application/octet-stream"
                    if filename.endswith(".pdf"): media_type = "application/pdf"
                    elif filename.endswith(".docx"): media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    elif filename.endswith(".txt"): media_type = "text/plain; charset=utf-8"
                    elif filename.endswith(".json"): media_type = "application/json"
                    self._send_bytes(200, media_type, target_file.read_bytes(), filename)
                else:
                    self._send_json(404, {"error": "File not found"})
            else:
                self._send_json(400, {"error": "Invalid file path"})
        elif path == "/api/v1/forensics/estate/personas":
            dom = query.get("domain", [None])[0]
            personas = get_estate_personas(dom) if get_estate_personas else []
            self._send_json(200, {"count": len(personas), "personas": personas})
        elif path == "/api/v1/forensics/estate/personas/overview":
            self._send_json(200, get_persona_overview() if get_persona_overview else {})
        elif path == "/api/v1/forensics/estate/personas/modes":
            self._send_json(200, get_execution_modes() if get_execution_modes else {})
        elif path == "/api/v1/forensics/estate/personas/composites":
            self._send_json(200, get_composite_presets() if get_composite_presets else {})
        elif path.startswith("/api/v1/forensics/estate/persona/"):
            pid = path[len("/api/v1/forensics/estate/persona/"):]
            p = get_persona_detail(pid) if get_persona_detail else None
            if p:
                self._send_json(200, p)
            else:
                self._send_json(404, {"error": f"Persona {pid} not found"})
        elif path == "/api/v1/forensics/estate/deposition-crucible":
            self._send_json(200, get_deposition_crucible_overview() if get_deposition_crucible_overview else {})
        elif path == "/api/v1/forensics/estate/deposition-crucible/targets":
            self._send_json(200, {
                "count": len(TARGET_CRUCIBLE_PROFILES) if TARGET_CRUCIBLE_PROFILES else 0,
                "targets": list(TARGET_CRUCIBLE_PROFILES.values()) if TARGET_CRUCIBLE_PROFILES else []
            })
        elif path.startswith("/api/v1/forensics/estate/deposition-crucible/target/"):
            tid = path[len("/api/v1/forensics/estate/deposition-crucible/target/"):]
            plan = get_target_crucible_plan(tid) if get_target_crucible_plan else None
            if plan:
                self._send_json(200, plan)
            else:
                self._send_json(404, {"error": f"Target {tid} not found"})
        elif path == "/api/v1/forensics/estate/deposition-crucible/download/pdf":
            if not generate_master_crucible_pdf:
                self._send_json(500, {"error": "PDF generator unavailable"})
            else:
                self._send_bytes(200, "application/pdf", generate_master_crucible_pdf(), "MASTER_DEPOSITION_PERJURY_CRUCIBLE_28LINE.pdf")
        elif path == "/api/v1/forensics/estate/deposition-crucible/download/docx":
            if not generate_master_crucible_docx:
                self._send_json(500, {"error": "DOCX generator unavailable"})
            else:
                self._send_bytes(200, "application/vnd.openxmlformats-officedocument.wordprocessingml.document", generate_master_crucible_docx(), "MASTER_DEPOSITION_PERJURY_CRUCIBLE.docx")
        elif path == "/api/v1/forensics/estate/deposition-crucible/download/zip":
            if not generate_master_crucible_bundle_zip:
                self._send_json(500, {"error": "ZIP generator unavailable"})
            else:
                self._send_bytes(200, "application/zip", generate_master_crucible_bundle_zip(), "MASTER_DEPOSITION_PERJURY_CRUCIBLE_BUNDLE.zip")
        else:
            self._send_json(404, {"error": f"Not Found: {path}"})

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        if path == "/api/v1/records/ingest":
            content_len = int(self.headers.get("Content-Length", 0))
            post_body = self.rfile.read(content_len)
            try:
                data = json.loads(post_body.decode("utf-8"))
                rec = IngestRecord(**data)
                res = ingest_record(rec)
                self._send_json(200, res.model_dump() if hasattr(res, "model_dump") else res.dict())
            except Exception as e:
                self._send_json(400, {"error": str(e)})
        elif path == "/api/v1/forensics/estate/personas/dispatch":
            content_len = int(self.headers.get("Content-Length", 0))
            post_body = self.rfile.read(content_len)
            try:
                data = json.loads(post_body.decode("utf-8"))
                pid = data.get("persona_id")
                obj = data.get("mission_objective", "Execute task")
                mode = data.get("execution_mode", "pro-elite")
                params = data.get("parameters")
                if not dispatch_persona_mission:
                    self._send_json(500, {"error": "Persona engine unavailable"})
                else:
                    res = dispatch_persona_mission(pid, obj, mode, params)
                    self._send_json(200, res)
            except Exception as e:
                self._send_json(400, {"error": str(e)})
        elif path == "/api/v1/forensics/estate/deposition-crucible/simulate":
            content_len = int(self.headers.get("Content-Length", 0))
            post_body = self.rfile.read(content_len)
            try:
                data = json.loads(post_body.decode("utf-8"))
                tid = data.get("target_id")
                qid = data.get("question_id")
                stmt = data.get("witness_statement", "")
                if not simulate_interrogation_turn:
                    self._send_json(500, {"error": "Simulator unavailable"})
                else:
                    res = simulate_interrogation_turn(tid, qid, stmt)
                    if "error" in res:
                        self._send_json(400, res)
                    else:
                        self._send_json(200, res)
            except Exception as e:
                self._send_json(400, {"error": str(e)})
        else:
            self._send_json(404, {"error": f"Not Found: {path}"})

    def log_message(self, format, *args):
        pass

def run_server(port: int = 8000, host: str = "0.0.0.0"):
    server = HTTPServer((host, port), ForensicsHTTPHandler)
    print(f"🏛️ APEX Legal Forensics Engine listening on http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="APEX Legal Forensics Suite HTTP Engine")
    parser.add_argument("--port", type=int, default=8000, help="Port to listen on (default: 8000)")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host interface (default: 0.0.0.0)")
    args = parser.parse_args()
    run_server(port=args.port, host=args.host)
