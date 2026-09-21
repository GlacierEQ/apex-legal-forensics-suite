import unittest
import time
import sys
from pathlib import Path

# Ensure root package is resolvable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from backend.app.main import (
    app,
    IngestRecord,
    ingest_record,
    health_check,
    get_forensics_overview,
    get_allegations,
    get_contradictions,
    get_actors,
    get_events,
    get_motion_to_strike,
    search_case,
    export_motion_document,
    export_proof_matrix,
)

class TestMegaRepoBackend(unittest.TestCase):
    def test_health_check(self):
        res = health_check()
        self.assertEqual(res["status"], "healthy")
        self.assertIn("timestamp", res)
        self.assertEqual(res["case_id"], "1FDV-23-0001009")

    def test_record_ingest_and_hash_integrity(self):
        sample = IngestRecord(
            title="Sworn Statement",
            content="Direct firsthand testimony under penalty of perjury.",
            actor="Casey Barton",
            category="sworn_declaration"
        )
        receipt = ingest_record(sample)
        self.assertTrue(receipt.verified)
        self.assertEqual(len(receipt.sha256), 64)
        self.assertEqual(receipt.operator_authority, "ESTABLISHED_UNDER_FRE_601_602")

    def test_forensics_overview(self):
        overview = get_forensics_overview()
        self.assertEqual(overview["case_id"], "1FDV-23-0001009")
        self.assertIn("counts", overview)
        self.assertGreaterEqual(overview["counts"]["allegations"], 11)

    def test_allegations_retrieval(self):
        alleg_res = get_allegations()
        self.assertGreaterEqual(alleg_res["total"], 11)
        self.assertTrue(any("Structural Due Process" in a.get("title", "") for a in alleg_res["allegations"]))

    def test_contradictions_retrieval(self):
        contra_res = get_contradictions()
        self.assertGreaterEqual(contra_res["total"], 7)
        self.assertTrue(any("Kapolei" in c.get("conflicting_source_or_fact", "") or "exhibits" in c.get("conflicting_source_or_fact", "") for c in contra_res["contradictions"]))

    def test_motion_to_strike(self):
        motion = get_motion_to_strike()
        self.assertIn("HRE 602", motion["motion_title"])
        self.assertIn("SCOT BROWER", motion["adverse_parties"][1])
        self.assertGreaterEqual(len(motion["grounds"]), 4)
        self.assertTrue(motion["receipt_sha256"])

    def test_search_case(self):
        # Search for Brower
        res = search_case("Brower")
        self.assertGreater(res["total_matches"], 0)
        self.assertTrue(any("Brower" in r["title"] or "Brower" in r.get("actor", "") or "Brower" in r.get("summary", "") for r in res["results"]))

        # Search for Kapolei
        res_kap = search_case("Kapolei")
        self.assertGreater(res_kap["total_matches"], 0)

    def test_export_motion_document(self):
        doc = export_motion_document()
        self.assertTrue(doc["verified"])
        self.assertIn("EMERGENCY MOTION TO STRIKE", doc["title"])
        self.assertIn("HRE 602", doc["content"])
        self.assertIn("CASEY BARTON", doc["content"])
        self.assertEqual(len(doc["sha256"]), 64)

    def test_export_proof_matrix(self):
        mat = export_proof_matrix()
        self.assertGreaterEqual(mat["total_allegations"], 11)
        self.assertIn("| ID | Allegation Title |", mat["markdown_table"])
        self.assertEqual(len(mat["sha256"]), 64)

if __name__ == '__main__':
    unittest.main()
