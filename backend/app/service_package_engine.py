"""
APEX Legal Forensics Suite - Multi-Jurisdiction Formal Service Package Engine (Drill Bravo)
--------------------------------------------------------------------------------------------
Assembles court-ready, certified process service packages across:
  1. United States District Court for the District of Hawaii (Civil No. 1:26-cv-001009)
     - Form AO 440 (Summons in a Civil Action)
     - Form JS 44 (Federal Civil Cover Sheet)
     - FRCP 4(l) Proof of Service Affidavit
  2. Family Court of the First Circuit, State of Hawaii (FC-D No. 1FDV-23-0001009)
     - Form FC-D (State Family Court Summons & Notice)
     - HFCR 4(g) Return of Service Declaration
  3. Process Server Standing Directives & Anti-Evasion Countermeasures
  4. Master Bates Transmittal Manifests with SHA-256 Checksums

Evidentiary Standard: FRE 601/602 & HRE 601/602 Direct Eyewitness Admissibility
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

# ==============================================================================
# TARGET CONSPIRATOR SERVICE DIRECTORY
# ==============================================================================

SERVICE_TARGET_REGISTRY: Dict[str, Dict[str, Any]] = {
    "scot_brower": {
        "target_id": "scot_brower",
        "name": "Scot S. Brower, Esq.",
        "entity_type": "Individual Attorney / Adverse Lead Counsel",
        "service_address": "1088 Bishop Street, Suite 902, Honolulu, Hawaii 96813",
        "registered_agent": "Self / Personal Service",
        "special_instructions": "Serve personally in law office suite. If reception attempts to shield, document names and record refusal on video pursuant to process directives.",
        "jurisdictions": ["USDC_HAWAII", "HAWAII_FAMILY_COURT"],
        "answer_days": 21,
        "trebled_liability_usd": 38400000.0
    },
    "greg_ryan": {
        "target_id": "greg_ryan",
        "name": "Greg Ryan, Esq.",
        "entity_type": "Individual Attorney / Collusive Defense Counsel",
        "service_address": "737 Bishop Street, Suite 2350, Honolulu, Hawaii 96813",
        "registered_agent": "Self / Personal Service",
        "special_instructions": "Personal service at law firm reception or executive suite. Demand signature on Acknowledgment of Service.",
        "jurisdictions": ["USDC_HAWAII", "HAWAII_FAMILY_COURT"],
        "answer_days": 21,
        "trebled_liability_usd": 15000000.0
    },
    "honolulu_pd": {
        "target_id": "honolulu_pd",
        "name": "City and County of Honolulu / Honolulu Police Department",
        "entity_type": "Municipal Government Entity",
        "service_address": "Corporation Counsel, 530 S. King Street, Room 110, Honolulu, Hawaii 96813",
        "registered_agent": "Department of Corporation Counsel, City and County of Honolulu",
        "special_instructions": "Deliver certified service packet to Corporation Counsel intake desk. Obtain time-stamped receiving copy and officer badge number.",
        "jurisdictions": ["USDC_HAWAII", "HAWAII_FIRST_CIRCUIT"],
        "answer_days": 21,
        "trebled_liability_usd": 12500000.0
    },
    "csea_agency": {
        "target_id": "csea_agency",
        "name": "Child Support Enforcement Agency (CSEA) / Dept of Attorney General",
        "entity_type": "State Government Agency",
        "service_address": "Department of the Attorney General, 425 Queen Street, Honolulu, Hawaii 96813",
        "registered_agent": "Attorney General of the State of Hawaii",
        "special_instructions": "Formal service pursuant to HRCP Rule 4(d)(4) upon Hawaii Attorney General intake desk.",
        "jurisdictions": ["USDC_HAWAII", "HAWAII_FAMILY_COURT"],
        "answer_days": 21,
        "trebled_liability_usd": 25000000.0
    },
    "queens_hospital": {
        "target_id": "queens_hospital",
        "name": "The Queen's Medical Center",
        "entity_type": "Acute Care Hospital Corporation",
        "service_address": "1301 Punchbowl Street, Honolulu, Hawaii 96813",
        "registered_agent": "The Queen's Health System Legal Affairs / Registered Agent",
        "special_instructions": "Deliver to General Counsel / Risk Management office during normal business hours. Obtain signed receiving receipt.",
        "jurisdictions": ["USDC_HAWAII", "HAWAII_FIRST_CIRCUIT"],
        "answer_days": 21,
        "trebled_liability_usd": 12950000.0
    },
    "kapiolani_pediatric": {
        "target_id": "kapiolani_pediatric",
        "name": "Kapiʻolani Medical Center for Women & Children",
        "entity_type": "Pediatric Hospital Corporation (Hawaii Pacific Health)",
        "service_address": "55 Merchant Street, 27th Floor, Honolulu, Hawaii 96813",
        "registered_agent": "Hawaii Pacific Health Registered Agent / Legal Department",
        "special_instructions": "Deliver to corporate legal affairs intake desk. Note recipient name and title.",
        "jurisdictions": ["USDC_HAWAII", "HAWAII_FIRST_CIRCUIT"],
        "answer_days": 21,
        "trebled_liability_usd": 2500000.0
    },
    "nainoa_martin": {
        "target_id": "nainoa_martin",
        "name": "Nainoa Martin",
        "entity_type": "Individual Co-Conspirator / Straw Man",
        "service_address": "c/o Scot S. Brower, Esq., 1088 Bishop Street, Suite 902, Honolulu, Hawaii 96813 (and Last Known Residential Address)",
        "registered_agent": "Personal Service / Substituted Service",
        "special_instructions": "Serve personally. If evasive, execute stakeout verification with GPS timestamped photographs.",
        "jurisdictions": ["USDC_HAWAII", "HAWAII_FAMILY_COURT"],
        "answer_days": 21,
        "trebled_liability_usd": 5000000.0
    },
    "teresa_barton": {
        "target_id": "teresa_barton",
        "name": "Teresa Del Carpio Barton",
        "entity_type": "Adverse Co-Petitioner / Conspirator",
        "service_address": "c/o Scot S. Brower, Esq., 1088 Bishop Street, Suite 902, Honolulu, Hawaii 96813",
        "registered_agent": "c/o Counsel of Record Scot Brower",
        "special_instructions": "Serve upon counsel of record and via certified registered mail to residential domicile.",
        "jurisdictions": ["USDC_HAWAII", "HAWAII_FAMILY_COURT"],
        "answer_days": 21,
        "trebled_liability_usd": 15000000.0
    }
}

# ==============================================================================
# SERVICE PACKAGE GENERATION FUNCTIONS
# ==============================================================================

def get_service_directory_overview() -> Dict[str, Any]:
    """Returns overview metrics across the service package registry."""
    total_liability = sum(t["trebled_liability_usd"] for t in SERVICE_TARGET_REGISTRY.values())
    return {
        "status": "OPERATIONAL",
        "title": "APEX MULTI-JURISDICTION FORMAL SERVICE PACKAGE ENGINE",
        "drill": "DRILL BRAVO: FORMAL SERVICE & SUMMONS ASSEMBLY",
        "epistemic_standard": "L0–L5 Holographic Mesh (FRCP Rule 4 & HFCR Rule 4)",
        "total_targets": len(SERVICE_TARGET_REGISTRY),
        "total_trebled_exposure_usd": total_liability,
        "targets": [
            {
                "target_id": t["target_id"],
                "name": t["name"],
                "entity_type": t["entity_type"],
                "service_address": t["service_address"],
                "registered_agent": t["registered_agent"],
                "answer_days": t["answer_days"],
                "trebled_liability_usd": t["trebled_liability_usd"],
                "jurisdictions": t["jurisdictions"]
            }
            for t in SERVICE_TARGET_REGISTRY.values()
        ]
    }


def generate_federal_summons_ao440(target_id: str) -> Dict[str, Any]:
    """Generates official USDC Hawaii Form AO 440 (Summons in a Civil Action)."""
    target = SERVICE_TARGET_REGISTRY.get(target_id)
    if not target:
        raise ValueError(f"Target {target_id} not found in service registry")

    lines = [
        "AO 440 (Rev. 06/12) Summons in a Civil Action",
        "UNITED STATES DISTRICT COURT FOR THE DISTRICT OF HAWAII",
        "",
        "CASEY BARTON,                             CIVIL ACTION NO. 1:26-cv-001009",
        "        Plaintiff,",
        "    v.",
        f"{target['name'].upper()}; SCOT S. BROWER, ESQ.;",
        "CITY AND COUNTY OF HONOLULU; CSEA; et al.,",
        "        Defendants.",
        "________________________________________/",
        "",
        "SUMMONS IN A CIVIL ACTION",
        "",
        f"TO: {target['name']}",
        f"    {target['service_address']}",
        f"    Attn: {target['registered_agent']}",
        "",
        "A lawsuit has been filed against you.",
        "",
        f"Within {target['answer_days']} days after service of this summons on you (not counting the day you",
        "received it) — or 60 days if you are the United States or a United States agency, or an",
        "officer or employee of the United States — you must serve on the plaintiff an answer to the",
        "attached complaint or a motion under Rule 12 of the Federal Rules of Civil Procedure.",
        "The answer or motion must be served on the plaintiff or plaintiff's representative, whose",
        "name and address are:",
        "",
        "    CASEY BARTON, Pro Se",
        "    P.O. Box 700444",
        "    Kapolei, Hawaii 96709",
        "    Email: casey@glaciereq.com | Phone: (808) 555-APEX",
        "",
        "If you fail to respond, judgment by default will be entered against you for the relief",
        f"demanded in the complaint (including $38,400,000.00 in trebled damages, statutory fees,",
        "and injunctive remedies). You also must file your answer or motion with the court.",
        "",
        "DATED: Honolulu, Hawaii, " + time.strftime("%B %d, %2026"),
        "",
        "CLERK OF COURT, UNITED STATES DISTRICT COURT FOR THE DISTRICT OF HAWAII",
        "",
        "By: _____________________________________, Deputy Clerk",
        "",
        "================================================================================",
        "PROOF OF SERVICE (Federal Rule of Civil Procedure 4(l))",
        "================================================================================",
        "This summons for (name of individual and title, if any) was received by me on (date): _________",
        "",
        "[ ] I personally served the summons on the individual at (place): ___________________________",
        "    on (date): ________________________; or",
        "",
        "[ ] I left the summons at the individual's residence or usual place of abode with (name): ____",
        "    ____________________________, a person of suitable age and discretion who resides there,",
        "    on (date): ________________________, and mailed a copy to the individual's last known address; or",
        "",
        "[ ] I served the summons on (name of individual): __________________________________________,",
        "    who is designated by law to accept service of process on behalf of (name of organization):",
        f"    {target['name']} on (date): ________________________; or",
        "",
        "[ ] Other (specify): ____________________________________________________________________",
        "",
        "I declare under penalty of perjury under the laws of the United States of America that the",
        "foregoing information contained in the Proof of Service is true and correct.",
        "",
        "Date: ________________________        Server's Signature: ______________________________",
        "                                      Server's Address:   ______________________________",
        "                                      Server's Phone:     ______________________________"
    ]
    raw_text = "\n".join(lines)
    return {
        "target_id": target_id,
        "form": "AO_440",
        "court": "UNITED STATES DISTRICT COURT FOR THE DISTRICT OF HAWAII",
        "title": f"SUMMONS IN A CIVIL ACTION - {target['name']}",
        "raw_text": raw_text,
        "formatted_28_lines": format_28_line_pleading(raw_text.split("\n\n"), f"SUMMONS: {target['name']}")
    }


def generate_federal_civil_cover_sheet_js44(target_id: str) -> Dict[str, Any]:
    """Generates official USDC Hawaii Form JS 44 (Civil Cover Sheet)."""
    target = SERVICE_TARGET_REGISTRY.get(target_id)
    lines = [
        "JS 44 (Rev. 04/21) CIVIL COVER SHEET - DISTRICT OF HAWAII",
        "",
        "I. (a) PLAINTIFFS: CASEY BARTON",
        f"   (b) DEFENDANTS: {target['name'].upper()} (Lead Served Party); SCOT S. BROWER, ESQ.;",
        "                   GREG RYAN, ESQ.; CITY AND COUNTY OF HONOLULU; CSEA; et al.",
        "   (c) ATTORNEYS (Firm Name, Address, and Telephone):",
        "       Plaintiff Pro Se: CASEY BARTON, P.O. Box 700444, Kapolei, HI 96709",
        "",
        "II. BASIS OF JURISDICTION:",
        "    [X] 3 Federal Question (U.S. Government Not a Party)",
        "        Primary Statutes: 18 U.S.C. § 1962 (RICO); 42 U.S.C. § 1983; 18 U.S.C. § 1030",
        "",
        "III. CITIZENSHIP OF PRINCIPAL PARTIES (For Diversity Cases Only):",
        "     Plaintiff: Citizen of Hawaii [X] 1",
        "     Defendant: Incorporated or Principal Place of Business in Hawaii [X] 4",
        "",
        "IV. NATURE OF SUIT:",
        "    [X] 470 RACKETEER INFLUENCED AND CORRUPT ORGANIZATIONS (RICO)",
        "    [X] 440 OTHER CIVIL RIGHTS (42 U.S.C. § 1983 - Fourth & Fourteenth Amendments)",
        "    [X] 890 OTHER STATUTORY ACTIONS (Computer Fraud & Abuse Act - 18 U.S.C. § 1030)",
        "",
        "V. ORIGIN:",
        "   [X] 1 Original Proceeding",
        "",
        "VI. CAUSE OF ACTION:",
        "    Cite: 18 U.S.C. § 1962(c), (d); 18 U.S.C. § 1964(c); 42 U.S.C. § 1983",
        "    Brief Description: Civil RICO damages action arising from multi-agency pattern of racketeering",
        "                       activity, predicate acts of mail/wire fraud, obstruction of court proceedings,",
        "                       extortion, and unconstitutional conversion of property under color of state law.",
        "",
        "VII. REQUESTED IN COMPLAINT:",
        "     [X] CHECK IF THIS IS A CLASS ACTION UNDER RULE 23, F.R.Cv.P.",
        "     DEMAND: $38,400,000.00 (Trebled Damages under 18 U.S.C. § 1964(c))",
        "     JURY DEMAND: [X] YES  [ ] NO",
        "",
        "VIII. RELATED CASE(S) IF ANY:",
        "      Judge: Presiding District Judge",
        "      Docket Number: 1FDV-23-0001009 (Family Court of the First Circuit, State of Hawaii)",
        "",
        "DATED: " + time.strftime("%B %d, %2026"),
        "SIGNATURE OF ATTORNEY / PRO SE LITIGANT: ________________________________________"
    ]
    raw_text = "\n".join(lines)
    return {
        "target_id": target_id,
        "form": "JS_44",
        "court": "UNITED STATES DISTRICT COURT FOR THE DISTRICT OF HAWAII",
        "title": f"CIVIL COVER SHEET (JS 44) - {target['name']}",
        "raw_text": raw_text
    }


def generate_process_server_directives(target_id: str) -> Dict[str, Any]:
    """Generates mandatory standing operational directives for the certified process server."""
    target = SERVICE_TARGET_REGISTRY.get(target_id)
    lines = [
        "CERTIFIED PROCESS SERVER STANDING DIRECTIVES & EVASION PROTOCOL",
        "================================================================================",
        f"CLIENT: CASEY BARTON | MATTER: BARTON v. BROWER, ET AL. (CIVIL NO. 1:26-cv-001009)",
        f"TARGET TO BE SERVED: {target['name'].upper()}",
        f"SERVICE ADDRESS: {target['service_address']}",
        f"REGISTERED RECIPIENT: {target['registered_agent']}",
        f"SPECIAL INSTRUCTIONS: {target['special_instructions']}",
        "================================================================================",
        "",
        "1. PERSONAL SERVICE MANDATE (FRCP RULE 4 / HFCR RULE 4)",
        "   - You are instructed to effect personal in-hand delivery of the enclosed service packet",
        "     upon the designated defendant or authorized registered agent.",
        "   - Do NOT leave papers with unauthorized mailroom personnel, building security, or",
        "     common-area receptionists unless they affirmatively execute a written Acknowledgment",
        "     of Authority to accept process on behalf of the entity.",
        "",
        "2. PHOTOGRAPHIC & GPS GEOTAGGING REQUIREMENT",
        "   - Your process vehicle must record GPS coordinates upon arrival and departure.",
        "   - Take time-stamped exterior photographs of the suite entrance and door plaque.",
        "   - If service is contested, this telemetry will be submitted as an L0 exhibit in federal court.",
        "",
        "3. ANTI-EVASION & DROP-SERVICE PROTOCOL",
        "   - If deponent/actor physically flees, refuses to open the door, or retreats into an interior",
        "     office after having been verbally informed of the process, state loudly and clearly:",
        "     'You are being formally served with process in United States District Court Case 1:26-cv-001009.'",
        "   - Place the service packet within the immediate physical presence and sightline of the",
        "     deponent (drop-service pursuant to Ninth Circuit authority, Travelers Cas. & Sur. Co.,",
        "     526 F.3d 465). Photograph the packet at the point of drop-service.",
        "",
        "4. MANDATORY RETENTION OF AFFIDAVIT",
        "   - Complete the Return of Service Affidavit immediately upon departure.",
        "   - Email scanned notarized affidavit to process@glaciereq.com within 2 hours of completion.",
        "",
        "ENCLOSED PLEADING BINDER INVENTORY:",
        "   [X] Summons in a Civil Action (USDC Form AO 440)",
        "   [X] Civil Cover Sheet (Form JS 44)",
        "   [X] Verified Federal Civil RICO & § 1983 Complaint (28-Line Pleading Paper, 42 Pages)",
        "   [X] Emergency Motion to Strike Proposed Order & For Sanctions (Hawaii Family Court)",
        "   [X] Sworn Declaration of Casey Barton (HRE 602 / FRE 602 Direct Eyewitness Admissibility)",
        "   [X] Exhibits A through D (GPS Telemetry, Word-Diff Redline, JEFS Concealment Receipt, Matrix)",
        "   [X] Master Bates Exhibit Binder Index (BATES 0001 - 1450)",
        "",
        "ISSUED BY: CASEY BARTON, Pro Se Litigant",
        "DATE: " + time.strftime("%B %d, %2026")
    ]
    raw_text = "\n".join(lines)
    return {
        "target_id": target_id,
        "title": f"PROCESS SERVER DIRECTIVES - {target['name']}",
        "raw_text": raw_text
    }


def generate_state_family_court_summons(target_id: str) -> Dict[str, Any]:
    """Generates official State of Hawaii Family Court Summons & Notice for Case 1FDV-23-0001009."""
    target = SERVICE_TARGET_REGISTRY.get(target_id)
    lines = [
        "IN THE FAMILY COURT OF THE FIRST CIRCUIT, STATE OF HAWAII",
        "",
        "TERESA BARTON,                             FC-D NO. 1FDV-23-0001009",
        "        Plaintiff,",
        "    v.",
        "CASEY BARTON,",
        "        Defendant.",
        "________________________________________/",
        "",
        "STATE OF HAWAII FAMILY COURT SUMMONS AND NOTICE OF EMERGENCY HEARING",
        "",
        f"TO: {target['name'].upper()}",
        f"    {target['service_address']}",
        f"    Counsel of Record / Adverse Party in FC-D No. 1FDV-23-0001009",
        "",
        "YOU ARE HEREBY SUMMONED and required to appear before the Presiding Judge of the Family",
        "Court of the First Circuit, Kapolei Court Complex, 4675 Kapolei Parkway, Kapolei, Hawaii 96707,",
        "on the date and time designated for hearing on Defendant CASEY BARTON's on-attached:",
        "",
        "    DEFENDANT CASEY BARTON'S EMERGENCY MOTION TO STRIKE PROPOSED ORDER;",
        "    VACATE ORDERS ENTERED ON FRAUDULENT EX PARTE PRAECIPE AB INITIO; AND FOR",
        "    MANDATORY SANCTIONS UNDER HRE 602 & HFCR RULE 11; MEMORANDUM IN SUPPORT;",
        "    DECLARATION OF CASEY BARTON; AND EXHIBITS 'A' THROUGH 'D'",
        "",
        "PLEASE TAKE FURTHER NOTICE that pursuant to Hawaii Family Court Rules (HFCR) Rule 12,",
        "failure to appear or file verified written opposition supported by direct admissible testimony",
        "under HRE Rule 602 will result in the immediate granting of Defendant's requested relief,",
        "including the vacating of fraudulent orders ab initio and referral of counsel to ODC.",
        "",
        "DATED: Kapolei, Hawaii, " + time.strftime("%B %d, %2026"),
        "",
        "BY ORDER OF THE FAMILY COURT OF THE FIRST CIRCUIT",
        "",
        "____________________________________________",
        "Clerk of the Family Court, First Circuit"
    ]
    raw_text = "\n".join(lines)
    return {
        "target_id": target_id,
        "court": "FAMILY COURT OF THE FIRST CIRCUIT, STATE OF HAWAII",
        "title": f"HAWAII FAMILY COURT SUMMONS - {target['name']}",
        "raw_text": raw_text,
        "formatted_28_lines": format_28_line_pleading(raw_text.split("\n\n"), f"STATE SUMMONS: {target['name']}")
    }


def generate_target_service_package(target_id: str) -> Dict[str, Any]:
    """Assembles the complete formal multi-jurisdiction service package for a specific conspirator."""
    target = SERVICE_TARGET_REGISTRY.get(target_id)
    if not target:
        raise ValueError(f"Target {target_id} not found in service registry")

    fed_summons = generate_federal_summons_ao440(target_id)
    fed_js44 = generate_federal_civil_cover_sheet_js44(target_id)
    state_summons = generate_state_family_court_summons(target_id)
    server_directives = generate_process_server_directives(target_id)

    # Master combined text
    combined_sections = [
        "================================================================================",
        f"MASTER SERVICE PACKAGE: {target['name'].upper()}",
        f"CIVIL NO. 1:26-cv-001009 (USDC HAWAII) & FC-D NO. 1FDV-23-0001009 (FIRST CIRCUIT)",
        "================================================================================",
        "",
        "SECTION 1: FEDERAL SUMMONS (FORM AO 440)",
        fed_summons["raw_text"],
        "",
        "SECTION 2: FEDERAL CIVIL COVER SHEET (FORM JS 44)",
        fed_js44["raw_text"],
        "",
        "SECTION 3: STATE FAMILY COURT SUMMONS & NOTICE",
        state_summons["raw_text"],
        "",
        "SECTION 4: PROCESS SERVER STANDING DIRECTIVES",
        server_directives["raw_text"]
    ]
    master_text = "\n".join(combined_sections)

    return {
        "target_id": target_id,
        "target_meta": target,
        "federal_summons": fed_summons,
        "civil_cover_sheet": fed_js44,
        "state_summons": state_summons,
        "server_directives": server_directives,
        "master_service_text": master_text,
        "formatted_28_lines": format_28_line_pleading(master_text.split("\n\n"), f"SERVICE PACKET: {target['name']}")
    }


def generate_target_service_pdf(target_id: str) -> bytes:
    """Generates 28-line numbered PDF service packet for a specific target."""
    pkg = generate_target_service_package(target_id)
    court = "UNITED STATES DISTRICT COURT & HAWAII FIRST CIRCUIT COURT"
    case_num = "CIVIL NO. 1:26-cv-001009 / FC-D NO. 1FDV-23-0001009"
    doc_title = f"OFFICIAL SERVICE PACKET: {pkg['target_meta']['name'].upper()}"
    raw_text = pkg["formatted_28_lines"]
    if build_28_line_pdf:
        return build_28_line_pdf(raw_text, doc_title, case_num, court)
    return raw_text.encode("utf-8")


def generate_target_service_docx(target_id: str) -> bytes:
    """Generates editable DOCX service packet for a specific target."""
    pkg = generate_target_service_package(target_id)
    court = "UNITED STATES DISTRICT COURT & HAWAII FIRST CIRCUIT COURT"
    case_num = "CIVIL NO. 1:26-cv-001009 / FC-D NO. 1FDV-23-0001009"
    doc_title = f"OFFICIAL SERVICE PACKET: {pkg['target_meta']['name'].upper()}"
    raw_text = pkg["formatted_28_lines"]
    if build_pleading_docx:
        return build_pleading_docx(raw_text, doc_title, case_num, court)
    return raw_text.encode("utf-8")


def generate_master_service_bundle_zip() -> bytes:
    """Assembles all 8 conspirator service packages, summonses, and directives into a master ZIP archive."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        manifest_files = {}

        for tid, target in SERVICE_TARGET_REGISTRY.items():
            pkg = generate_target_service_package(tid)
            prefix = f"TARGET_{tid.upper()}"

            # 1. 28-Line PDF
            pdf_bytes = generate_target_service_pdf(tid)
            pdf_filename = f"{prefix}_SERVICE_PACKET_28LINE.pdf"
            zf.writestr(f"{tid}/{pdf_filename}", pdf_bytes)
            manifest_files[f"{tid}/{pdf_filename}"] = hashlib.sha256(pdf_bytes).hexdigest()

            # 2. DOCX
            docx_bytes = generate_target_service_docx(tid)
            docx_filename = f"{prefix}_SERVICE_PACKET.docx"
            zf.writestr(f"{tid}/{docx_filename}", docx_bytes)
            manifest_files[f"{tid}/{docx_filename}"] = hashlib.sha256(docx_bytes).hexdigest()

            # 3. Individual Documents in Text
            zf.writestr(f"{tid}/01_FEDERAL_SUMMONS_AO440.txt", pkg["federal_summons"]["raw_text"])
            zf.writestr(f"{tid}/02_CIVIL_COVER_SHEET_JS44.txt", pkg["civil_cover_sheet"]["raw_text"])
            zf.writestr(f"{tid}/03_STATE_FAMILY_COURT_SUMMONS.txt", pkg["state_summons"]["raw_text"])
            zf.writestr(f"{tid}/04_PROCESS_SERVER_DIRECTIVES.txt", pkg["server_directives"]["raw_text"])

        # 4. Master Transmittal Manifest
        manifest = {
            "title": "APEX MULTI-JURISDICTION FORMAL SERVICE PACKAGE MASTER BUNDLE",
            "drill": "DRILL BRAVO: FORMAL SERVICE & SUMMONS ASSEMBLY",
            "federal_action": "CIVIL NO. 1:26-cv-001009 (USDC HAWAII)",
            "state_action": "FC-D NO. 1FDV-23-0001009 (FAMILY COURT OF THE FIRST CIRCUIT)",
            "generated_timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "total_targets_served": len(SERVICE_TARGET_REGISTRY),
            "total_trebled_exposure_usd": sum(t["trebled_liability_usd"] for t in SERVICE_TARGET_REGISTRY.values()),
            "evidentiary_standard": "FRE 601/602 & HRE 601/602 Direct Eyewitness Competence",
            "files": manifest_files
        }
        zf.writestr("00_MASTER_SERVICE_TRANSMITTAL_MANIFEST.json", json.dumps(manifest, indent=2))

    return buf.getvalue()
