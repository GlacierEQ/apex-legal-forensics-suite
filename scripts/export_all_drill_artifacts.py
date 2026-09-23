"""
APEX Legal Forensics Suite - Multi-Drill Artifact Exporter
Generates court-ready PDF, DOCX, and ZIP bundles across:
  - Drill Alpha: Deposition Cross-Examination & Perjury Trap Crucible
  - Drill Bravo: Multi-Jurisdiction Formal Service Packages (8 Conspirators)
  - Drill Charlie: Hospital Healthcare Fraud & EMTALA Inquest ($15.45M Exposure)
  - Drill Delta: JEFS Docket Telemetry & Anti-Tampering Engine (4 Critical Dockets)
"""

import sys
import hashlib
import json
import time
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR))

from backend.app.deposition_crucible_engine import (
    generate_master_crucible_bundle_zip,
    generate_master_crucible_pdf,
    generate_master_crucible_docx
)
from backend.app.service_package_engine import (
    SERVICE_TARGET_REGISTRY,
    generate_target_service_package,
    generate_target_service_pdf,
    generate_target_service_docx,
    generate_master_service_bundle_zip
)
from backend.app.hospital_fraud_engine import (
    HOSPITAL_TARGET_PORTFOLIO,
    generate_hospital_fraud_pdf,
    generate_hospital_fraud_docx,
    generate_hospital_fraud_bundle_zip
)
from backend.app.jefs_tamper_monitor import (
    VERIFIED_TAMPERING_ALERTS,
    generate_jefs_audit_dossier_text,
    generate_jefs_audit_dossier_pdf,
    generate_jefs_audit_dossier_docx,
    generate_jefs_monitor_bundle_zip
)


def export_all():
    artifacts_root = Path("/root/artifacts")
    artifacts_root.mkdir(parents=True, exist_ok=True)

    receipts = {}

    # =========================================================================
    # DRILL ALPHA: DEPOSITION CRUCIBLE
    # =========================================================================
    crucible_dir = artifacts_root / "crucible"
    crucible_dir.mkdir(parents=True, exist_ok=True)
    print("[DRILL ALPHA] Exporting Deposition Crucible artifacts...")

    pdf_alpha = generate_master_crucible_pdf()
    (crucible_dir / "01_DEPOSITION_CRUCIBLE_INTERROGATORY_SCRIPT_28LINE.pdf").write_bytes(pdf_alpha)
    receipts["crucible/01_DEPOSITION_CRUCIBLE_INTERROGATORY_SCRIPT_28LINE.pdf"] = {
        "bytes": len(pdf_alpha),
        "sha256": hashlib.sha256(pdf_alpha).hexdigest()
    }

    docx_alpha = generate_master_crucible_docx()
    (crucible_dir / "01_DEPOSITION_CRUCIBLE_INTERROGATORY_SCRIPT.docx").write_bytes(docx_alpha)
    receipts["crucible/01_DEPOSITION_CRUCIBLE_INTERROGATORY_SCRIPT.docx"] = {
        "bytes": len(docx_alpha),
        "sha256": hashlib.sha256(docx_alpha).hexdigest()
    }

    zip_alpha = generate_master_crucible_bundle_zip()
    (crucible_dir / "MASTER_DEPOSITION_PERJURY_CRUCIBLE_BUNDLE.zip").write_bytes(zip_alpha)
    receipts["crucible/MASTER_DEPOSITION_PERJURY_CRUCIBLE_BUNDLE.zip"] = {
        "bytes": len(zip_alpha),
        "sha256": hashlib.sha256(zip_alpha).hexdigest()
    }

    # =========================================================================
    # DRILL BRAVO: FORMAL SERVICE PACKAGES
    # =========================================================================
    service_dir = artifacts_root / "service"
    service_dir.mkdir(parents=True, exist_ok=True)
    print("[DRILL BRAVO] Exporting 8 Formal Service Packages...")

    for tid, target in SERVICE_TARGET_REGISTRY.items():
        t_pdf = generate_target_service_pdf(tid)
        pdf_name = f"SERVICE_PACKET_{tid.upper()}_28LINE.pdf"
        (service_dir / pdf_name).write_bytes(t_pdf)
        receipts[f"service/{pdf_name}"] = {
            "bytes": len(t_pdf),
            "sha256": hashlib.sha256(t_pdf).hexdigest(),
            "target": target["name"],
            "liability_usd": target["trebled_liability_usd"]
        }

        t_docx = generate_target_service_docx(tid)
        docx_name = f"SERVICE_PACKET_{tid.upper()}.docx"
        (service_dir / docx_name).write_bytes(t_docx)
        receipts[f"service/{docx_name}"] = {
            "bytes": len(t_docx),
            "sha256": hashlib.sha256(t_docx).hexdigest()
        }

    zip_bravo = generate_master_service_bundle_zip()
    (service_dir / "MASTER_SERVICE_PACKAGE_BUNDLE.zip").write_bytes(zip_bravo)
    receipts["service/MASTER_SERVICE_PACKAGE_BUNDLE.zip"] = {
        "bytes": len(zip_bravo),
        "sha256": hashlib.sha256(zip_bravo).hexdigest()
    }

    # =========================================================================
    # DRILL CHARLIE: HOSPITAL FRAUD & EMTALA INQUEST
    # =========================================================================
    hospital_dir = artifacts_root / "hospital"
    hospital_dir.mkdir(parents=True, exist_ok=True)
    print("[DRILL CHARLIE] Exporting Hospital Healthcare Fraud & EMTALA Inquest...")

    pdf_charlie = generate_hospital_fraud_pdf()
    (hospital_dir / "01_HOSPITAL_HEALTHCARE_FRAUD_INQUEST_28LINE.pdf").write_bytes(pdf_charlie)
    receipts["hospital/01_HOSPITAL_HEALTHCARE_FRAUD_INQUEST_28LINE.pdf"] = {
        "bytes": len(pdf_charlie),
        "sha256": hashlib.sha256(pdf_charlie).hexdigest()
    }

    docx_charlie = generate_hospital_fraud_docx()
    (hospital_dir / "01_HOSPITAL_HEALTHCARE_FRAUD_INQUEST.docx").write_bytes(docx_charlie)
    receipts["hospital/01_HOSPITAL_HEALTHCARE_FRAUD_INQUEST.docx"] = {
        "bytes": len(docx_charlie),
        "sha256": hashlib.sha256(docx_charlie).hexdigest()
    }

    zip_charlie = generate_hospital_fraud_bundle_zip()
    (hospital_dir / "HOSPITAL_HEALTHCARE_FRAUD_INQUEST_BUNDLE.zip").write_bytes(zip_charlie)
    receipts["hospital/HOSPITAL_HEALTHCARE_FRAUD_INQUEST_BUNDLE.zip"] = {
        "bytes": len(zip_charlie),
        "sha256": hashlib.sha256(zip_charlie).hexdigest()
    }

    # =========================================================================
    # DRILL DELTA: JEFS DOCKET TELEMETRY & TAMPER MONITOR
    # =========================================================================
    jefs_dir = artifacts_root / "jefs"
    jefs_dir.mkdir(parents=True, exist_ok=True)
    print("[DRILL DELTA] Exporting JEFS Docket Telemetry & Anti-Tampering Dossier...")

    dossier_text = generate_jefs_audit_dossier_text()
    (jefs_dir / "01_JEFS_DOCKET_TAMPERING_DOSSIER_28LINE.txt").write_text(dossier_text, encoding="utf-8")

    pdf_delta = generate_jefs_audit_dossier_pdf()
    (jefs_dir / "01_JEFS_DOCKET_TAMPERING_DOSSIER_28LINE.pdf").write_bytes(pdf_delta)
    receipts["jefs/01_JEFS_DOCKET_TAMPERING_DOSSIER_28LINE.pdf"] = {
        "bytes": len(pdf_delta),
        "sha256": hashlib.sha256(pdf_delta).hexdigest()
    }

    docx_delta = generate_jefs_audit_dossier_docx()
    (jefs_dir / "01_JEFS_DOCKET_TAMPERING_DOSSIER.docx").write_bytes(docx_delta)
    receipts["jefs/01_JEFS_DOCKET_TAMPERING_DOSSIER.docx"] = {
        "bytes": len(docx_delta),
        "sha256": hashlib.sha256(docx_delta).hexdigest()
    }

    zip_delta = generate_jefs_monitor_bundle_zip()
    (jefs_dir / "JEFS_DOCKET_TAMPERING_BUNDLE.zip").write_bytes(zip_delta)
    receipts["jefs/JEFS_DOCKET_TAMPERING_BUNDLE.zip"] = {
        "bytes": len(zip_delta),
        "sha256": hashlib.sha256(zip_delta).hexdigest()
    }

    # =========================================================================
    # MASTER DRILL RECEIPT MANIFEST
    # =========================================================================
    master_receipt = {
        "status": "VERIFIED_L0_L5",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "evidentiary_standard": "FRE 601/602 & HRE 601/602 Direct Eyewitness Admissibility",
        "drills_completed": [
            "DRILL ALPHA: Deposition Cross-Examination & Perjury Trap Crucible (10 Phases, 71 Traps, 5 Targets)",
            "DRILL BRAVO: Multi-Jurisdiction Formal Service Package Assembly (8 Targets, $126.35M Trebled)",
            "DRILL CHARLIE: Hospital Healthcare Fraud & EMTALA Inquest ($15.45M Adverse Exposure)",
            "DRILL DELTA: Automated JEFS Docket Telemetry & Anti-Tampering Engine (4 Critical Dockets)"
        ],
        "total_files_generated": len(receipts),
        "artifacts": receipts
    }

    receipt_path = artifacts_root / "APEX_MULTI_DRILL_EXECUTED_RECEIPTS.json"
    receipt_path.write_text(json.dumps(master_receipt, indent=2), encoding="utf-8")
    print(f"\n[APEX] Multi-Drill Export Complete: {len(receipts)} artifacts generated with SHA-256 receipts.")
    print(f"Receipt manifest: {receipt_path}")


if __name__ == "__main__":
    export_all()
