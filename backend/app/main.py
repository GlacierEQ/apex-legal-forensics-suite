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
    from backend.app.legal_filing_engine import generate_hawaii_filing_packet, generate_federal_rico_complaint
except ImportError:
    try:
        from legal_filing_engine import generate_hawaii_filing_packet, generate_federal_rico_complaint
    except ImportError:
        generate_hawaii_filing_packet = None
        generate_federal_rico_complaint = None

try:
    from fastapi import FastAPI, HTTPException, Depends
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
            "/api/v1/forensics/motion-to-strike"
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

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

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
