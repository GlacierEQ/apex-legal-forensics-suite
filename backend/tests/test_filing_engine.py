import unittest
import sys
from pathlib import Path

# Ensure package path is resolvable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from backend.app.legal_filing_engine import (
    format_28_line_pleading,
    generate_hawaii_filing_packet,
    generate_federal_rico_complaint,
)
from backend.app.main import (
    load_case_ledger_data,
    get_hawaii_filing_packet,
    get_federal_rico_complaint,
    export_hawaii_filing_packet,
    export_federal_rico_complaint,
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

if __name__ == "__main__":
    unittest.main()
