import unittest
import sys
from pathlib import Path

# Ensure package path is resolvable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from backend.app.legal_filing_engine import (
    format_28_line_pleading,
    generate_hawaii_filing_packet,
    generate_federal_rico_complaint,
    generate_hawaii_packet_pdf,
    generate_hawaii_packet_docx,
    generate_federal_rico_pdf,
    generate_federal_rico_docx,
    generate_hawaii_filing_bundle_zip,
    generate_federal_rico_bundle_zip,
)
from backend.app.main import (
    load_case_ledger_data,
    get_hawaii_filing_packet,
    get_federal_rico_complaint,
    export_hawaii_filing_packet,
    export_federal_rico_complaint,
    download_hawaii_packet_pdf,
    download_hawaii_packet_docx,
    download_federal_rico_pdf,
    download_federal_rico_docx,
    download_hawaii_filing_bundle_zip_route,
    download_federal_rico_bundle_zip_route,
)

class TestLegalFilingEngine(unittest.TestCase):
    def setUp(self):
        self.data = load_case_ledger_data()

    def test_28_line_formatter(self):
        sample = ["Line one of pleading text.", "Line two with more verbose words to verify wrap."]
        res = format_28_line_pleading(sample, "TEST COURT")
        lines = res.splitlines()
        self.assertTrue(lines[0].startswith(" 1  "))
        self.assertIn("TEST COURT", lines[0])
        self.assertTrue(lines[1].startswith(" 2  "))

    def test_vector_1_hawaii_packet(self):
        packet = generate_hawaii_filing_packet(self.data)
        self.assertTrue(packet["verified"])
        self.assertIn("DEFENDANT'S EMERGENCY MOTION TO STRIKE", packet["title"])
        self.assertEqual(packet["case_number"], "FC-D NO. 1FDV-23-0001009")
        self.assertIn("SCOT BROWER", packet["adverse_counsel"])
        self.assertEqual(len(packet["sha256"]), 64)

        # Components check
        comps = packet["components"]
        self.assertIn("Kapolei", comps["exhibit_a"])
        self.assertTrue("WORD-DIFF" in comps["exhibit_b"] or "WORD DIFF" in comps["exhibit_b"])
        self.assertIn("Dkt 193", comps["exhibit_b"])
        self.assertIn("235", comps["exhibit_c"])
        self.assertTrue("PROOF MATRIX" in comps["exhibit_d"] or "Proof Matrix" in comps["exhibit_d"])
        self.assertIn("CERTIFICATE OF SERVICE", comps["certificate_of_service"])
        self.assertIn("HRE 602", comps["declaration"])

        # 28-line format check
        lines = packet["formatted_28_lines"].splitlines()
        self.assertGreaterEqual(len(lines), 100)
        self.assertTrue(lines[0].startswith(" 1  "))

    def test_vector_2_federal_rico(self):
        rico = generate_federal_rico_complaint(self.data)
        self.assertTrue(rico["verified"])
        self.assertIn("DISTRICT OF HAWAII", rico["court"])
        self.assertEqual(rico["damages_actual"], 12800000.0)
        self.assertTrue(any("SCOT BROWER" in d for d in rico["defendants"]))
        self.assertTrue(any("NATASHA SHAW" in d for d in rico["defendants"]))
        self.assertTrue(any("CSEA" in d for d in rico["defendants"]))
        self.assertEqual(len(rico["causes_of_action"]), 6)
        self.assertEqual(len(rico["sha256"]), 64)

        # 28-line format check
        lines = rico["formatted_28_lines"].splitlines()
        self.assertGreaterEqual(len(lines), 100)
        self.assertTrue(lines[0].startswith(" 1  "))

    def test_main_app_filing_endpoints(self):
        hw_res = get_hawaii_filing_packet()
        self.assertTrue(hw_res["verified"])

        rc_res = get_federal_rico_complaint()
        self.assertTrue(rc_res["verified"])
        self.assertEqual(rc_res["damages_trebled"], 38400000.0)

        hw_exp = export_hawaii_filing_packet(format="28_lines")
        self.assertTrue(hw_exp["verified"])
        self.assertIn("28_lines", hw_exp["format"])

        rc_exp = export_federal_rico_complaint(format="28_lines")
        self.assertTrue(rc_exp["verified"])
        self.assertEqual(rc_exp["damages_trebled"], 38400000.0)

    def test_pdf_and_docx_compilation(self):
        # Hawaii packet
        hw_packet = generate_hawaii_filing_packet(self.data)
        hw_pdf = generate_hawaii_packet_pdf(hw_packet)
        self.assertIsInstance(hw_pdf, bytes)
        self.assertGreater(len(hw_pdf), 5000)
        self.assertTrue(hw_pdf.startswith(b"%PDF"))

        hw_docx = generate_hawaii_packet_docx(hw_packet)
        self.assertIsInstance(hw_docx, bytes)
        self.assertGreater(len(hw_docx), 5000)
        self.assertTrue(hw_docx.startswith(b"PK"))

        # Federal RICO
        rico_comp = generate_federal_rico_complaint(self.data)
        rico_pdf = generate_federal_rico_pdf(rico_comp)
        self.assertIsInstance(rico_pdf, bytes)
        self.assertGreater(len(rico_pdf), 5000)
        self.assertTrue(rico_pdf.startswith(b"%PDF"))

        rico_docx = generate_federal_rico_docx(rico_comp)
        self.assertIsInstance(rico_docx, bytes)
        self.assertGreater(len(rico_docx), 5000)
        self.assertTrue(rico_docx.startswith(b"PK"))

    def test_download_endpoints(self):
        # Hawaii PDF download
        hw_pdf_resp = download_hawaii_packet_pdf()
        self.assertEqual(hw_pdf_resp.media_type, "application/pdf")
        self.assertTrue(hw_pdf_resp.body.startswith(b"%PDF"))

        # Hawaii DOCX download
        hw_docx_resp = download_hawaii_packet_docx()
        self.assertIn("wordprocessingml", hw_docx_resp.media_type)
        self.assertTrue(hw_docx_resp.body.startswith(b"PK"))

        # Federal RICO PDF download
        rico_pdf_resp = download_federal_rico_pdf()
        self.assertEqual(rico_pdf_resp.media_type, "application/pdf")
        self.assertTrue(rico_pdf_resp.body.startswith(b"%PDF"))

        # Federal RICO DOCX download
        rico_docx_resp = download_federal_rico_docx()
        self.assertIn("wordprocessingml", rico_docx_resp.media_type)
        self.assertTrue(rico_docx_resp.body.startswith(b"PK"))

    def test_zip_bundle_assembly_and_downloads(self):
        import zipfile
        import io

        # 1. Hawaii filing bundle
        hw_packet = generate_hawaii_filing_packet(self.data)
        hw_zip = generate_hawaii_filing_bundle_zip(hw_packet)
        self.assertIsInstance(hw_zip, bytes)
        self.assertTrue(hw_zip.startswith(b"PK"))

        with zipfile.ZipFile(io.BytesIO(hw_zip), "r") as z:
            names = z.namelist()
            self.assertIn("01_HAWAII_EMERGENCY_MOTION_PACKET_28LINE.pdf", names)
            self.assertIn("01_HAWAII_EMERGENCY_MOTION_PACKET.docx", names)
            self.assertIn("01_HAWAII_EMERGENCY_MOTION_PACKET_FULLTEXT.txt", names)
            self.assertIn("02_EXHIBIT_A_TELEMETRY_KAPOLEI_PRESENCE.txt", names)
            self.assertIn("03_EXHIBIT_B_PRAECIPE_WORD_DIFF_INVERSION.txt", names)
            self.assertIn("04_EXHIBIT_C_JEFS_SEAL_CONCEALMENT_RECEIPT.txt", names)
            self.assertIn("05_EXHIBIT_D_PROOF_CONTRADICTION_MATRIX.txt", names)
            self.assertIn("06_SWORN_DECLARATION_CASEY_BARTON.txt", names)
            self.assertIn("00_FILING_MANIFEST_AND_SHA256_RECEIPTS.json", names)

        # 2. Federal RICO bundle
        rico_comp = generate_federal_rico_complaint(self.data)
        rico_zip = generate_federal_rico_bundle_zip(rico_comp)
        self.assertIsInstance(rico_zip, bytes)
        self.assertTrue(rico_zip.startswith(b"PK"))

        with zipfile.ZipFile(io.BytesIO(rico_zip), "r") as z:
            names = z.namelist()
            self.assertIn("01_FEDERAL_CIVIL_RICO_COMPLAINT_28LINE.pdf", names)
            self.assertIn("01_FEDERAL_CIVIL_RICO_COMPLAINT.docx", names)
            self.assertIn("01_FEDERAL_CIVIL_RICO_COMPLAINT_FULLTEXT.txt", names)
            self.assertIn("02_CAUSES_OF_ACTION_AND_PREDICATE_ACTS.txt", names)
            self.assertIn("00_RICO_FILING_MANIFEST_AND_SHA256_RECEIPTS.json", names)

        # 3. HTTP Download routes
        hw_route_resp = download_hawaii_filing_bundle_zip_route()
        self.assertEqual(hw_route_resp.media_type, "application/zip")
        self.assertTrue(hw_route_resp.body.startswith(b"PK"))

        rico_route_resp = download_federal_rico_bundle_zip_route()
        self.assertEqual(rico_route_resp.media_type, "application/zip")
        self.assertTrue(rico_route_resp.body.startswith(b"PK"))

if __name__ == "__main__":
    unittest.main()
