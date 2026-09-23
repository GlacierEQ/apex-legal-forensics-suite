"""
APEX Legal Forensics Suite - Hospital Healthcare Fraud & EMTALA Inquest Engine (Drill Charlie)
-----------------------------------------------------------------------------------------------
Acute Forensic Actions:
  1. The Queen's Medical Center ($12,950,000.00 Claim)
     - 42 U.S.C. § 1395dd (Emergency Medical Treatment and Active Labor Act - EMTALA)
     - Patient Dumping & Refusal of Mandatory Emergency Stabilization (March 2026)
     - Formal CMS-2567 Statement of Deficiencies Demand & HHS Administrative Inquest
  2. Kapiʻolani Medical Center for Women & Children / Hawaii Pacific Health ($2,500,000.00 Claim)
     - Suppression of Minor Kekoa Barton's Humerus Pinning & Closed-Head Trauma Records
     - HRS § 350-1.1 (Mandatory Reporting of Child Abuse & Pediatric Fractures)
     - HIPAA Privacy Rule 45 C.F.R. § 164.524 (Parental Access Violation)
     - Spoliation & Fraudulent Alteration of EHR / EPIC Audit Logs

Epistemic Standard: L0–L5 Holographic Mesh (FRE 601/602 & HRE 601/602 Direct Eyewitness Weight)
"""

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
        format_28_line_pleading,
        REPORTLAB_AVAILABLE,
        DOCX_AVAILABLE
    )
except ImportError:
    try:
        from legal_filing_engine import (
            build_28_line_pdf,
            build_pleading_docx,
            format_28_line_pleading,
            REPORTLAB_AVAILABLE,
            DOCX_AVAILABLE
        )
    except ImportError:
        build_28_line_pdf = None
        build_pleading_docx = None
        format_28_line_pleading = None
        REPORTLAB_AVAILABLE = False
        DOCX_AVAILABLE = False

HOSPITAL_TARGET_PORTFOLIO: Dict[str, Dict[str, Any]] = {
    "queens_medical_center": {
        "hospital_id": "queens_medical_center",
        "entity_name": "The Queen's Medical Center (The Queen's Health System)",
        "facility_address": "1301 Punchbowl Street, Honolulu, Hawaii 96813",
        "medicare_provider_number": "12-0010",
        "statutory_basis": [
            "42 U.S.C. § 1395dd (EMTALA Private Right of Action)",
            "42 C.F.R. § 489.24 (Special Responsibilities of Medicare Hospitals)",
            "Hawaii Revised Statutes § 671-1 (Medical Malpractice & Abandonment)",
            "Common Law Intentional Infliction of Emotional Distress & Gross Negligence"
        ],
        "incident_date": "March 2026",
        "exposure_usd": 12950000.0,
        "key_allegations": [
            "Refusal to perform appropriate medical screening examination (MSE) under 42 U.S.C. § 1395dd(a)",
            "Failure to stabilize an emergency medical condition prior to transfer or discharge under 42 U.S.C. § 1395dd(b)",
            "Retaliatory patient dumping driven by administrative discrimination and collusive outside pressure",
            "Falsification of emergency room triage acuity scoring in hospital electronic records"
        ]
    },
    "kapiolani_pediatric": {
        "hospital_id": "kapiolani_pediatric",
        "entity_name": "Kapiʻolani Medical Center for Women & Children (Hawaii Pacific Health)",
        "facility_address": "1319 Punahou Street, Honolulu, Hawaii 96826",
        "medicare_provider_number": "12-3300",
        "statutory_basis": [
            "Hawaii Revised Statutes § 350-1.1 (Mandatory Reporting of Child Abuse/Trauma)",
            "HIPAA Privacy Rule 45 C.F.R. § 164.524 (Parental Access to Medical Records)",
            "18 U.S.C. § 1519 (Destruction, Alteration, or Falsification of Records)",
            "Hawaii Revised Statutes § 571-46 (Custodial Rights to Medical History)"
        ],
        "incident_date": "2023 - 2025 Ongoing",
        "exposure_usd": 2500000.0,
        "key_allegations": [
            "Concealment of Kekoa Barton's humerus fracture and orthopedic pinning surgical notes",
            "Failure to mandate reporting of suspicious pediatric trauma pursuant to HRS § 350-1.1",
            "Unlawful denial of biological father's HIPAA § 164.524 access rights despite legal joint custody",
            "Improper restriction and alteration of PACS DICOM radiological imaging audit logs"
        ]
    }
}

# ==============================================================================
# DOCUMENT GENERATOR ENGINES
# ==============================================================================

def get_hospital_fraud_overview() -> Dict[str, Any]:
    """Returns overview statistics across the hospital healthcare fraud inquest."""
    total_exposure = sum(h["exposure_usd"] for h in HOSPITAL_TARGET_PORTFOLIO.values())
    return {
        "status": "OPERATIONAL",
        "title": "APEX HOSPITAL HEALTHCARE FRAUD & EMTALA INQUEST ENGINE",
        "drill": "DRILL CHARLIE: HOSPITAL HEALTHCARE FRAUD & EMTALA INQUEST",
        "epistemic_standard": "L0–L5 Holographic Mesh (FRE 601/602 & HRE 601/602)",
        "total_hospital_entities": len(HOSPITAL_TARGET_PORTFOLIO),
        "total_claims_exposure_usd": total_exposure,
        "hospitals": list(HOSPITAL_TARGET_PORTFOLIO.values())
    }


def generate_queens_emtala_complaint() -> Dict[str, Any]:
    """
    Generates formal federal civil claim and CMS-2567 administrative inquest against
    The Queen's Medical Center for emergency room patient dumping and EMTALA violations.
    """
    q = HOSPITAL_TARGET_PORTFOLIO["queens_medical_center"]
    lines = [
        "IN THE UNITED STATES DISTRICT COURT FOR THE DISTRICT OF HAWAII",
        "",
        "CASEY BARTON,                             CIVIL NO. 1:26-cv-001009",
        "        Plaintiff,",
        "    v.",
        "THE QUEEN'S MEDICAL CENTER;               FIRST AMENDED COMPLAINT FOR DAMAGES:",
        "THE QUEEN'S HEALTH SYSTEM;                VIOLATION OF THE EMERGENCY MEDICAL",
        "JOHN AND JANE DOES 1-10,                  TREATMENT AND ACTIVE LABOR ACT (EMTALA)",
        "        Defendants.                       (42 U.S.C. § 1395dd); MEDICAL ABANDONMENT;",
        "________________________________________/ AND CIVIL CONSPIRACY",
        "",
        "CLAIM FOR RELIEF: VIOLATION OF EMTALA (42 U.S.C. § 1395dd)",
        "",
        "1. Plaintiff Casey Barton incorporates all preceding allegations with full evidentiary",
        "weight under FRE 601 and FRE 602 based upon firsthand personal knowledge.",
        "",
        "2. Defendant The Queen's Medical Center is a participating hospital operating an emergency",
        "department within the meaning of 42 U.S.C. § 1395dd(e)(2) and receives federal Medicare funding.",
        "",
        "3. In March 2026, Plaintiff presented to The Queen's Medical Center Emergency Department",
        "suffering from an acute emergency medical condition manifesting severe physical symptoms,",
        "intense acute pain, and acute physiological distress.",
        "",
        "4. Pursuant to 42 U.S.C. § 1395dd(a), Defendant was under an absolute statutory duty to provide",
        "an 'appropriate medical screening examination within the capability of the hospital's emergency",
        "department, including ancillary services routinely available... to determine whether or not an",
        "emergency medical condition exists.'",
        "",
        "5. In willful and reckless violation of federal law, Defendant failed and refused to provide",
        "standard medical screening, applied disparate non-standard triage criteria, and executed an",
        "abrupt, retaliatory patient dumping discharge while Plaintiff remained acutely unstable.",
        "",
        "6. Defendant's actions violated 42 U.S.C. § 1395dd(b), which mandates that if an emergency",
        "medical condition exists, the hospital must provide 'such further medical examination and such",
        "treatment as may be required to stabilize the medical condition.'",
        "",
        "7. As a direct and proximate result of Defendant's unlawful EMTALA violations, Plaintiff suffered",
        "catastrophic physiological exacerbation, severe physical and emotional distress, and extensive",
        "economic damages. Pursuant to 42 U.S.C. § 1395dd(d)(2)(A), Plaintiff is entitled to recover",
        "all damages available under Hawaii personal injury law, in an amount of $12,950,000.00.",
        "",
        "WHEREFORE, Plaintiff demands trial by jury and judgment against Defendant The Queen's Medical",
        "Center for $12,950,000.00 in compensatory and punitive damages, statutory costs, and referral to CMS."
    ]
    raw_text = "\n".join(lines)
    return {
        "hospital_id": "queens_medical_center",
        "title": "FEDERAL EMTALA COMPLAINT COUNT - THE QUEEN'S MEDICAL CENTER",
        "court": "UNITED STATES DISTRICT COURT FOR THE DISTRICT OF HAWAII",
        "statute": "42 U.S.C. § 1395dd",
        "exposure_usd": 12950000.0,
        "raw_text": raw_text,
        "formatted_28_lines": format_28_line_pleading(raw_text.split("\n\n"), "EMTALA COMPLAINT: QUEEN'S MEDICAL CENTER")
    }


def generate_queens_cms_complaint() -> Dict[str, Any]:
    """Generates official administrative complaint to CMS Region 9 & Hawaii DOH OHCA."""
    lines = [
        "FORMAL ADMINISTRATIVE COMPLAINT: EMTALA PATIENT DUMPING",
        "================================================================================",
        "TO: CENTERS FOR MEDICARE & MEDICAID SERVICES (CMS) - REGION 9",
        "    Division of Survey & Certification",
        "    90 7th Street, Suite 5-300, San Francisco, CA 94103",
        "",
        "    HAWAII DEPARTMENT OF HEALTH - OFFICE OF HEALTH CARE ASSURANCE (OHCA)",
        "    601 Kamokila Blvd., Room 337, Kapolei, HI 96707",
        "================================================================================",
        "",
        "1. COMPLAINANT: CASEY BARTON | P.O. Box 700444, Kapolei, HI 96709",
        "2. FACILITY: THE QUEEN'S MEDICAL CENTER (CMS Provider #12-0010)",
        "             1301 Punchbowl Street, Honolulu, HI 96813",
        "3. DATE OF VIOLATION: March 2026",
        "",
        "4. SUMMARY OF VIOLATION (42 C.F.R. § 489.24):",
        "   Complainant formally requests an unannounced federal on-site survey and investigation",
        "   of The Queen's Medical Center Emergency Department. On the date specified, Complainant",
        "   presented with an emergency medical condition. Hospital staff deliberately refused an",
        "   appropriate medical screening examination (MSE), falsified triage records, and discharged",
        "   Complainant in an unstable condition without stabilization treatment or written consent.",
        "",
        "5. REQUESTED ENFORCEMENT ACTION:",
        "   - Issuance of Form CMS-2567 (Statement of Deficiencies and Plan of Correction);",
        "   - Initiation of Medicare Provider Termination proceedings under 42 C.F.R. § 489.53;",
        "   - Imposition of maximum civil monetary penalties under 42 U.S.C. § 1395dd(d)(1);",
        "   - Preservation of all video surveillance, EHR audit logs, and triage telemetry.",
        "",
        "DATED: " + time.strftime("%B %d, %2026"),
        "SUBMITTED UNDER PENALTY OF PERJURY: CASEY BARTON, Complainant"
    ]
    raw_text = "\n".join(lines)
    return {
        "agency": "CMS_REGION_9_AND_HAWAII_DOH_OHCA",
        "title": "FORMAL EMTALA ADMINISTRATIVE COMPLAINT (CMS-2567 DEMAND)",
        "raw_text": raw_text
    }


def generate_kapiolani_hipaa_demand() -> Dict[str, Any]:
    """
    Generates mandatory HIPAA 45 C.F.R. § 164.524 Record Production Demand & Child Trauma
    Inquest against Kapiʻolani Medical Center for Women & Children.
    """
    lines = [
        "FORMAL LEGAL DEMAND FOR IMMEDIATE PRODUCTION OF COMPLETE UNREDACTED",
        "PEDIATRIC MEDICAL RECORDS & MANDATORY ABUSE INQUEST (HRS § 350-1.1)",
        "================================================================================",
        "TO: KAPIʻOLANI MEDICAL CENTER FOR WOMEN & CHILDREN",
        "    HAWAII PACIFIC HEALTH - HEALTH INFORMATION MANAGEMENT (HIM)",
        "    1319 Punahou Street, Honolulu, Hawaii 96826",
        "    Attn: Custodian of Records & Legal Department",
        "================================================================================",
        "",
        "RE: MINOR CHILD: KEKOA BARTON",
        "    DEMANDING PARENT: CASEY BARTON (Natural Father & Joint Legal Custodian)",
        "    STATUTORY AUTHORITY: HIPAA 45 C.F.R. § 164.524; HRS § 571-46; HRS § 350-1.1",
        "",
        "1. DEMAND FOR IMMEDIATE UNRESTRICTED ACCESS (45 C.F.R. § 164.524):",
        "   Demand is hereby made by natural father Casey Barton, holding joint legal and physical",
        "   custody of minor child Kekoa Barton, for complete, unredacted, certified copies of all",
        "   medical, surgical, clinical, nursing, radiological, and emergency records, including:",
        "",
        "   a. Complete orthopedic consultation notes regarding humerus fracture, reduction, and pinning;",
        "   b. Full PACS DICOM electronic radiological imaging files (X-rays, CT scans, MRIs);",
        "   c. Emergency Department triage notes regarding closed-head trauma, loss of consciousness, and concussive injury;",
        "   d. Operative and post-anesthesia care unit (PACU) surgical reports;",
        "   e. Complete EPIC / EHR access audit logs showing all electronic user views, redactions, and flag changes.",
        "",
        "2. NOTICE OF WRONGFUL CONCEALMENT & HRS § 350-1.1 MANDATORY INQUEST:",
        "   Notice is hereby given that Kapiʻolani Medical Center personnel unlawfully withheld these",
        "   records from natural father Casey Barton despite repeated written requests, and failed to",
        "   report non-accidental pediatric fractures and closed-head trauma to Child Welfare Services",
        "   or law enforcement as mandated by Hawaii Revised Statutes § 350-1.1.",
        "",
        "3. SPOLIATION WARNING & LITIGATION HOLD:",
        "   All electronic health records, audit trails, and DICOM images are subject to an active",
        "   litigation hold in United States District Court Civil Action No. 1:26-cv-001009. Any deletion,",
        "   alteration, or retroactive modification constitutes intentional spoliation and a felony",
        "   violation of 18 U.S.C. § 1519.",
        "",
        "MANDATORY DEADLINE FOR FULL ELECTRONIC PRODUCTION: TEN (10) BUSINESS DAYS.",
        "",
        "DATED: Honolulu, Hawaii, " + time.strftime("%B %d, %2026"),
        "",
        "CASEY BARTON, Natural Father and Legal Custodian",
        "P.O. Box 700444, Kapolei, HI 96709 | casey@glaciereq.com"
    ]
    raw_text = "\n".join(lines)
    return {
        "hospital_id": "kapiolani_pediatric",
        "title": "HIPAA § 164.524 PEDIATRIC RECORD DEMAND & HRS § 350-1.1 INQUEST",
        "raw_text": raw_text,
        "formatted_28_lines": format_28_line_pleading(raw_text.split("\n\n"), "HIPAA DEMAND: KAPIʻOLANI MEDICAL CENTER")
    }


def generate_hospital_proof_matrix() -> Dict[str, Any]:
    """Generates structured contradiction and evidence proof matrix for healthcare fraud."""
    items = [
        {
            "id": "HOSP-MED-01",
            "hospital": "The Queen's Medical Center",
            "incident": "March 2026 Emergency Dumping",
            "violation": "42 U.S.C. § 1395dd(a), (b)",
            "fact": "Plaintiff presented in acute emergency state; hospital discharged without stabilization treatment.",
            "proof": "Emergency triage records, vital sign telemetry showing instability, audio recordings of staff refusal.",
            "exposure_usd": 12950000.0,
            "statutory_consequence": "Medicare provider decertification; civil damages under § 1395dd(d)(2)(A)."
        },
        {
            "id": "HOSP-MED-02",
            "hospital": "Kapiʻolani Medical Center",
            "incident": "Kekoa Humerus Fracture & Skull Trauma",
            "violation": "HRS § 350-1.1 & 45 C.F.R. § 164.524",
            "fact": "Hospital concealed radiology PACs and surgical pinning records from biological custodial father.",
            "proof": "EHR access audit logs, PACS imaging metadata, written refusal letters from risk management.",
            "exposure_usd": 2500000.0,
            "statutory_consequence": "HHS OCR civil monetary penalties; Class C felony spoliation under 18 U.S.C. § 1519."
        }
    ]
    return {
        "title": "HOSPITAL HEALTHCARE FRAUD & EMTALA PROOF MATRIX",
        "total_items": len(items),
        "total_exposure_usd": sum(i["exposure_usd"] for i in items),
        "proof_items": items
    }


def generate_hospital_fraud_pdf() -> bytes:
    """Compiles the complete Hospital Healthcare Fraud inquest into a 28-line legal PDF."""
    q_comp = generate_queens_emtala_complaint()
    q_cms = generate_queens_cms_complaint()
    k_hipaa = generate_kapiolani_hipaa_demand()
    
    full_text = "\n\n".join([
        "================================================================================",
        "APEX HOSPITAL HEALTHCARE FRAUD & EMTALA INQUEST MASTER DOSSIER",
        "TOTAL ADVERSE HEALTHCARE EXPOSURE: $15,450,000.00",
        "================================================================================",
        q_comp["raw_text"],
        "",
        q_cms["raw_text"],
        "",
        k_hipaa["raw_text"]
    ])
    court = "UNITED STATES DISTRICT COURT & HHS / CMS REGION 9"
    case_num = "CIVIL NO. 1:26-cv-001009 / CMS REF: 12-0010"
    doc_title = "HOSPITAL HEALTHCARE FRAUD & EMTALA INQUEST DOSSIER"
    formatted = format_28_line_pleading(full_text.split("\n\n"), "HEALTHCARE FRAUD INQUEST")
    if build_28_line_pdf:
        return build_28_line_pdf(formatted, doc_title, case_num, court)
    return formatted.encode("utf-8")


def generate_hospital_fraud_docx() -> bytes:
    """Compiles the complete Hospital Healthcare Fraud inquest into an editable DOCX binder."""
    q_comp = generate_queens_emtala_complaint()
    q_cms = generate_queens_cms_complaint()
    k_hipaa = generate_kapiolani_hipaa_demand()
    
    full_text = "\n\n".join([
        "================================================================================",
        "APEX HOSPITAL HEALTHCARE FRAUD & EMTALA INQUEST MASTER DOSSIER",
        "TOTAL ADVERSE HEALTHCARE EXPOSURE: $15,450,000.00",
        "================================================================================",
        q_comp["raw_text"],
        "",
        q_cms["raw_text"],
        "",
        k_hipaa["raw_text"]
    ])
    court = "UNITED STATES DISTRICT COURT & HHS / CMS REGION 9"
    case_num = "CIVIL NO. 1:26-cv-001009 / CMS REF: 12-0010"
    doc_title = "HOSPITAL HEALTHCARE FRAUD & EMTALA INQUEST DOSSIER"
    formatted = format_28_line_pleading(full_text.split("\n\n"), "HEALTHCARE FRAUD INQUEST")
    if build_pleading_docx:
        return build_pleading_docx(formatted, doc_title, case_num, court)
    return formatted.encode("utf-8")


def generate_hospital_fraud_bundle_zip() -> bytes:
    """Assembles all hospital complaints, demands, proof matrices, and manifests into a ZIP archive."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        # 1. 28-Line PDF
        pdf_bytes = generate_hospital_fraud_pdf()
        zf.writestr("01_HOSPITAL_HEALTHCARE_FRAUD_INQUEST_28LINE.pdf", pdf_bytes)

        # 2. DOCX
        docx_bytes = generate_hospital_fraud_docx()
        zf.writestr("01_HOSPITAL_HEALTHCARE_FRAUD_INQUEST.docx", docx_bytes)

        # 3. Individual Documents
        q_comp = generate_queens_emtala_complaint()
        q_cms = generate_queens_cms_complaint()
        k_hipaa = generate_kapiolani_hipaa_demand()
        proof = generate_hospital_proof_matrix()

        zf.writestr("02_QUEENS_MEDICAL_CENTER_EMTALA_COMPLAINT_COUNT.txt", q_comp["raw_text"])
        zf.writestr("03_QUEENS_CMS_REGION_9_ADMINISTRATIVE_COMPLAINT.txt", q_cms["raw_text"])
        zf.writestr("04_KAPIOLANI_PEDIATRIC_HIPAA_164_524_DEMAND.txt", k_hipaa["raw_text"])
        zf.writestr("05_HEALTHCARE_FRAUD_PROOF_MATRIX.json", json.dumps(proof, indent=2))

        # 4. Transmittal Manifest
        manifest = {
            "title": "APEX HOSPITAL HEALTHCARE FRAUD & EMTALA INQUEST BUNDLE",
            "drill": "DRILL CHARLIE: HOSPITAL HEALTHCARE FRAUD & EMTALA INQUEST",
            "generated_timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "total_hospitals": len(HOSPITAL_TARGET_PORTFOLIO),
            "total_exposure_usd": sum(h["exposure_usd"] for h in HOSPITAL_TARGET_PORTFOLIO.values()),
            "files": {
                "01_HOSPITAL_HEALTHCARE_FRAUD_INQUEST_28LINE.pdf": hashlib.sha256(pdf_bytes).hexdigest(),
                "01_HOSPITAL_HEALTHCARE_FRAUD_INQUEST.docx": hashlib.sha256(docx_bytes).hexdigest(),
                "02_QUEENS_MEDICAL_CENTER_EMTALA_COMPLAINT_COUNT.txt": hashlib.sha256(q_comp["raw_text"].encode("utf-8")).hexdigest(),
                "03_QUEENS_CMS_REGION_9_ADMINISTRATIVE_COMPLAINT.txt": hashlib.sha256(q_cms["raw_text"].encode("utf-8")).hexdigest(),
                "04_KAPIOLANI_PEDIATRIC_HIPAA_164_524_DEMAND.txt": hashlib.sha256(k_hipaa["raw_text"].encode("utf-8")).hexdigest(),
                "05_HEALTHCARE_FRAUD_PROOF_MATRIX.json": hashlib.sha256(json.dumps(proof).encode("utf-8")).hexdigest()
            }
        }
        zf.writestr("00_HOSPITAL_FRAUD_MANIFEST_AND_SHA256_RECEIPTS.json", json.dumps(manifest, indent=2))

    return buf.getvalue()
