"""
Unit and Integration Tests for APEX Multi-Drill Legal Warfare Suite
Covers:
  - Drill Bravo: Multi-Jurisdiction Formal Service Package Engine (8 Conspirators)
  - Drill Charlie: Hospital Healthcare Fraud & EMTALA Inquest Engine ($15.45M Exposure)
  - Drill Delta: JEFS Docket Telemetry & Anti-Tampering Engine (4 Critical Dockets)
"""

import unittest
import zipfile
import io
import json
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.service_package_engine import (
    SERVICE_TARGET_REGISTRY,
    get_service_directory_overview,
    generate_target_service_package,
    generate_target_service_pdf,
    generate_target_service_docx,
    generate_master_service_bundle_zip
)
from backend.app.hospital_fraud_engine import (
    HOSPITAL_TARGET_PORTFOLIO,
    get_hospital_fraud_overview,
    generate_queens_emtala_complaint,
    generate_queens_cms_complaint,
    generate_kapiolani_hipaa_demand,
    generate_hospital_proof_matrix,
    generate_hospital_fraud_pdf,
    generate_hospital_fraud_docx,
    generate_hospital_fraud_bundle_zip
)
from backend.app.jefs_tamper_monitor import (
    VERIFIED_TAMPERING_ALERTS,
    get_jefs_monitor_status,
    get_tamper_alerts,
    run_docket_integrity_scan,
    generate_jefs_audit_dossier_text,
    generate_jefs_audit_dossier_pdf,
    generate_jefs_audit_dossier_docx,
    generate_jefs_monitor_bundle_zip
)


class TestMultiDrills(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    # ==========================================================================
    # DRILL BRAVO: FORMAL SERVICE PACKAGES
    # ==========================================================================
    def test_drill_bravo_service_directory_overview(self):
        overview = get_service_directory_overview()
        self.assertEqual(overview["total_targets"], 8)
        self.assertEqual(overview["total_trebled_exposure_usd"], 126350000.0)
        self.assertEqual(len(overview["targets"]), 8)

        expected_targets = {
            "scot_brower", "greg_ryan", "honolulu_pd", "csea_agency",
            "queens_hospital", "kapiolani_pediatric", "nainoa_martin", "teresa_barton"
        }
        actual_targets = {t["target_id"] for t in overview["targets"]}
        self.assertEqual(expected_targets, actual_targets)

    def test_drill_bravo_target_package_generation(self):
        pkg = generate_target_service_package("scot_brower")
        self.assertEqual(pkg["target_id"], "scot_brower")
        self.assertIn("federal_summons", pkg)
        self.assertIn("civil_cover_sheet", pkg)
        self.assertIn("state_summons", pkg)
        self.assertIn("server_directives", pkg)
        self.assertIn("formatted_28_lines", pkg)
        self.assertIn("AO 440", pkg["federal_summons"]["raw_text"])
        self.assertIn("1088 Bishop Street", pkg["target_meta"]["service_address"])
        self.assertEqual(pkg["target_meta"]["trebled_liability_usd"], 38400000.0)

    def test_drill_bravo_pdf_docx_zip_generation(self):
        # 1. Target PDF
        pdf_bytes = generate_target_service_pdf("scot_brower")
        self.assertIsInstance(pdf_bytes, bytes)
        self.assertTrue(len(pdf_bytes) > 1000)
        self.assertTrue(pdf_bytes.startswith(b"%PDF"))

        # 2. Target DOCX
        docx_bytes = generate_target_service_docx("scot_brower")
        self.assertIsInstance(docx_bytes, bytes)
        self.assertTrue(len(docx_bytes) > 1000)

        # 3. Master Bundle ZIP
        zip_bytes = generate_master_service_bundle_zip()
        self.assertIsInstance(zip_bytes, bytes)
        self.assertTrue(len(zip_bytes) > 10000)
        with zipfile.ZipFile(io.BytesIO(zip_bytes), "r") as zf:
            namelist = zf.namelist()
            self.assertIn("00_MASTER_SERVICE_TRANSMITTAL_MANIFEST.json", namelist)
            self.assertIn("scot_brower/TARGET_SCOT_BROWER_SERVICE_PACKET_28LINE.pdf", namelist)
            self.assertIn("queens_hospital/TARGET_QUEENS_HOSPITAL_SERVICE_PACKET_28LINE.pdf", namelist)
            self.assertIn("honolulu_pd/01_FEDERAL_SUMMONS_AO440.txt", namelist)

    def test_drill_bravo_api_endpoints(self):
        res = self.client.get("/api/v1/forensics/estate/service-packages")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["total_targets"], 8)

        res_target = self.client.get("/api/v1/forensics/estate/service-packages/target/greg_ryan")
        self.assertEqual(res_target.status_code, 200)
        t_data = res_target.json()
        self.assertEqual(t_data["target_meta"]["name"], "Greg Ryan, Esq.")

        res_zip = self.client.get("/api/v1/forensics/estate/service-packages/download/zip")
        self.assertEqual(res_zip.status_code, 200)
        self.assertEqual(res_zip.headers["content-type"], "application/zip")
        self.assertTrue(len(res_zip.content) > 10000)

    # ==========================================================================
    # DRILL CHARLIE: HOSPITAL FRAUD & EMTALA INQUEST
    # ==========================================================================
    def test_drill_charlie_hospital_overview(self):
        overview = get_hospital_fraud_overview()
        self.assertEqual(overview["total_hospital_entities"], 2)
        self.assertEqual(overview["total_claims_exposure_usd"], 15450000.0)
        self.assertEqual(len(overview["hospitals"]), 2)

    def test_drill_charlie_queens_emtala_complaint(self):
        comp = generate_queens_emtala_complaint()
        self.assertIn("raw_text", comp)
        self.assertIn("42 U.S.C. § 1395dd", comp["raw_text"])
        self.assertIn("$12,950,000.00", comp["raw_text"])
        self.assertIn("The Queen's Medical Center", comp["raw_text"])
        self.assertIn("March 2026", comp["raw_text"])

    def test_drill_charlie_kapiolani_hipaa_demand(self):
        demand = generate_kapiolani_hipaa_demand()
        self.assertIn("raw_text", demand)
        self.assertIn("45 C.F.R. § 164.524", demand["raw_text"])
        self.assertIn("Kekoa Barton", demand["raw_text"])
        self.assertIn("humerus", demand["raw_text"])
        self.assertIn("closed-head trauma", demand["raw_text"])

    def test_drill_charlie_proof_matrix(self):
        matrix = generate_hospital_proof_matrix()
        self.assertEqual(matrix["total_exposure_usd"], 15450000.0)
        self.assertEqual(len(matrix["proof_items"]), 2)
        self.assertEqual(matrix["proof_items"][0]["hospital"], "The Queen's Medical Center")

    def test_drill_charlie_pdf_docx_zip(self):
        pdf_bytes = generate_hospital_fraud_pdf()
        self.assertTrue(pdf_bytes.startswith(b"%PDF"))

        docx_bytes = generate_hospital_fraud_docx()
        self.assertTrue(len(docx_bytes) > 1000)

        zip_bytes = generate_hospital_fraud_bundle_zip()
        with zipfile.ZipFile(io.BytesIO(zip_bytes), "r") as zf:
            namelist = zf.namelist()
            self.assertIn("00_HOSPITAL_FRAUD_MANIFEST_AND_SHA256_RECEIPTS.json", namelist)
            self.assertIn("01_HOSPITAL_HEALTHCARE_FRAUD_INQUEST_28LINE.pdf", namelist)
            self.assertIn("02_QUEENS_MEDICAL_CENTER_EMTALA_COMPLAINT_COUNT.txt", namelist)
            self.assertIn("04_KAPIOLANI_PEDIATRIC_HIPAA_164_524_DEMAND.txt", namelist)

    def test_drill_charlie_api_endpoints(self):
        res = self.client.get("/api/v1/forensics/estate/hospital-fraud")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["total_claims_exposure_usd"], 15450000.0)

        res_q = self.client.get("/api/v1/forensics/estate/hospital-fraud/queens-emtala")
        self.assertEqual(res_q.status_code, 200)
        self.assertIn("EMTALA", res_q.json()["title"])

        res_k = self.client.get("/api/v1/forensics/estate/hospital-fraud/kapiolani-hipaa")
        self.assertEqual(res_k.status_code, 200)

        res_zip = self.client.get("/api/v1/forensics/estate/hospital-fraud/download/zip")
        self.assertEqual(res_zip.status_code, 200)
        self.assertEqual(res_zip.headers["content-type"], "application/zip")

    # ==========================================================================
    # DRILL DELTA: JEFS DOCKET TELEMETRY & TAMPER MONITOR
    # ==========================================================================
    def test_drill_delta_tamper_alerts(self):
        alerts = get_tamper_alerts()
        self.assertEqual(len(alerts), 4)

        dockets = {str(a["docket_number"]) for a in alerts}
        self.assertIn("190", dockets)
        self.assertIn("193", dockets)
        self.assertIn("201", dockets)
        self.assertIn("186", dockets)

    def test_drill_delta_integrity_scan(self):
        scan = run_docket_integrity_scan("1FDV-23-0001009")
        self.assertEqual(scan["case_id"], "1FDV-23-0001009")
        self.assertIn("compromised_entries", scan)
        self.assertEqual(len(scan["compromised_entries"]), 4)
        self.assertEqual(scan["status"], "TAMPERING_DETECTED")

    def test_drill_delta_dossier_text_pdf_docx_zip(self):
        text = generate_jefs_audit_dossier_text()
        self.assertIn("TELEMETRY DOSSIER", text)
        self.assertIn("DOCKET #190", text)
        self.assertIn("DOCKET #193", text)
        self.assertIn("DOCKET #201", text)
        self.assertIn("DOCKET #186", text)

        pdf_bytes = generate_jefs_audit_dossier_pdf()
        self.assertTrue(pdf_bytes.startswith(b"%PDF"))

        docx_bytes = generate_jefs_audit_dossier_docx()
        self.assertTrue(len(docx_bytes) > 1000)

        zip_bytes = generate_jefs_monitor_bundle_zip()
        with zipfile.ZipFile(io.BytesIO(zip_bytes), "r") as zf:
            namelist = zf.namelist()
            self.assertIn("00_JEFS_TELEMETRY_MANIFEST_AND_SHA256_RECEIPTS.json", namelist)
            self.assertIn("01_JEFS_DOCKET_TAMPERING_DOSSIER_28LINE.pdf", namelist)
            self.assertIn("03_VERIFIED_TAMPERING_ALERTS.json", namelist)

    def test_drill_delta_api_endpoints(self):
        res = self.client.get("/api/v1/forensics/estate/jefs-monitor")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["total_tampering_alerts"], 4)

        res_alerts = self.client.get("/api/v1/forensics/estate/jefs-monitor/alerts")
        self.assertEqual(res_alerts.status_code, 200)
        self.assertEqual(res_alerts.json()["count"], 4)

        res_scan = self.client.get("/api/v1/forensics/estate/jefs-monitor/scan")
        self.assertEqual(res_scan.status_code, 200)
        self.assertEqual(res_scan.json()["status"], "TAMPERING_DETECTED")

        res_zip = self.client.get("/api/v1/forensics/estate/jefs-monitor/download/zip")
        self.assertEqual(res_zip.status_code, 200)
        self.assertEqual(res_zip.headers["content-type"], "application/zip")


if __name__ == "__main__":
    unittest.main()
