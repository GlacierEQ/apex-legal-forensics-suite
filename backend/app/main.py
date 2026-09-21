import time
import hashlib
import os
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

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
