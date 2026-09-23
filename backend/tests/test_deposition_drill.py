import unittest
import sys
import zipfile
import io
import json
from pathlib import Path

# Ensure package path is resolvable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

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
from backend.app.main import (
    app,
    HAS_FASTAPI,
    get_deposition_crucible_route,
    get_deposition_targets_route,
    get_deposition_target_plan_route,
    download_deposition_crucible_pdf,
    download_deposition_crucible_docx,
    download_deposition_crucible_zip,
    simulate_crucible_route,
    CrucibleSimulateRequest
)

if HAS_FASTAPI:
    from fastapi.testclient import TestClient
else:
    TestClient = None


class TestDepositionDrill(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app) if HAS_FASTAPI else None

    def test_overview_metrics(self):
        ov = get_deposition_crucible_overview()
        self.assertEqual(ov["status"], "OPERATIONAL")
        self.assertIn("DEPOSITION", ov["title"])
        self.assertEqual(ov["total_targets"], 5)
        self.assertGreater(ov["total_examination_phases"], 8)
        self.assertGreater(ov["total_interrogatories"], 5)
        self.assertGreaterEqual(ov["total_perjury_traps_in_db"], 71)
        self.assertGreaterEqual(ov["total_target_exposure_usd"], 90000000.0)

    def test_all_five_targets_exist(self):
        expected = ["scot_brower", "greg_ryan", "csea_officials", "hpd_officers", "hospital_administrators"]
        for tid in expected:
            self.assertIn(tid, TARGET_CRUCIBLE_PROFILES)
            plan = get_target_crucible_plan(tid)
            self.assertIsNotNone(plan)
            self.assertEqual(plan["target_id"], tid)
            self.assertGreater(len(plan["phases"]), 0)
            self.assertIn("criminal_statutes", plan)
            self.assertGreater(len(plan["criminal_statutes"]), 0)

    def test_scot_brower_ghost_hearing_phase(self):
        plan = get_target_crucible_plan("scot_brower")
        phase2 = None
        for p in plan["phases"]:
            if "Ghost Hearing" in p["phase_title"]:
                phase2 = p
                break
        self.assertIsNotNone(phase2, "Ghost Hearing phase must be present in Brower plan")
        q1 = phase2["questions"][0]
        self.assertIn("1:36 PM", q1["interrogatory"])
        self.assertIn("Dkt 190", q1["perjury_dilemma"])
        self.assertIn("BATES-EX-001", q1["impeachment_evidence"])
        self.assertIn("HRS § 710-1017", q1["statutory_penalties"])

    def test_simulation_interrogation_evasions(self):
        # 1. Lack of recollection
        res1 = simulate_interrogation_turn(
            "scot_brower",
            "SB-P02-Q01",
            "I do not recall what time I left the Kapolei parking lot."
        )
        self.assertEqual(res1["status"], "SUCCESS")
        self.assertEqual(res1["classified_tactic"], "FALSE_LACK_OF_RECOLLECTION")
        self.assertEqual(res1["impeachment_status"], "IMPEACHED_BY_L0")
        self.assertIn("BATES-EX-001", res1["impeachment_exhibit"])
        self.assertIn("Exhibit", res1["immediate_follow_up_question"])

        # 2. False privilege claims (Attorney-Client, Work-Product, Civil Standby, HIPAA)
        res2 = simulate_interrogation_turn(
            "scot_brower",
            "SB-P01-Q02",
            "I decline to answer based on attorney-client privilege."
        )
        self.assertEqual(res2["classified_tactic"], "UNFOUNDED_PRIVILEGE_SHIELD")
        self.assertEqual(res2["impeachment_status"], "IMPEACHED_BY_L0")
        self.assertIn("Ninth Circuit", res2["speaking_counter"])

        res2_wp = simulate_interrogation_turn(
            "scot_brower",
            "SB-P01-Q02",
            "Objection: Protected under the work-product doctrine."
        )
        self.assertEqual(res2_wp["classified_tactic"], "UNFOUNDED_PRIVILEGE_SHIELD")

        res2_cs = simulate_interrogation_turn(
            "hpd_officers",
            "HPD-P01-Q01",
            "Officers were merely providing a civil standby."
        )
        self.assertEqual(res2_cs["classified_tactic"], "UNFOUNDED_PRIVILEGE_SHIELD")

        res2_hipaa = simulate_interrogation_turn(
            "hospital_administrators",
            "MED-P01-Q01",
            "Records are confidential under HIPAA."
        )
        self.assertEqual(res2_hipaa["classified_tactic"], "UNFOUNDED_PRIVILEGE_SHIELD")

        # 3. Direct denial
        res3 = simulate_interrogation_turn(
            "scot_brower",
            "SB-P04-Q01",
            "No, I never concealed any exhibits."
        )
        self.assertEqual(res3["classified_tactic"], "DIRECT_DENIAL_CONTRADICTED_BY_L0")
        self.assertEqual(res3["impeachment_status"], "IMPEACHED_BY_L0")
        self.assertEqual(res3["credibility_deduction"], 100)

        # 4. Fatal admission
        res4 = simulate_interrogation_turn(
            "greg_ryan",
            "GR-P01-Q01",
            "Yes, I did not receive written consent from Casey Barton."
        )
        self.assertEqual(res4["classified_tactic"], "FATAL_AFFIRMATIVE_CONCESSION")
        self.assertEqual(res4["impeachment_status"], "LIABILITY_ESTABLISHED")

    def test_28_line_text_and_compilation(self):
        txt = generate_master_crucible_text()
        self.assertIn("CIVIL NO. 1:26-cv-001009", txt)
        self.assertIn("SCOT S. BROWER", txt)
        self.assertIn("GREG RYAN", txt)
        self.assertIn("71 VERIFIED ESTATE PERJURY TRAPS", txt)
        self.assertIn("01", txt)

        # PDF Bytes
        pdf = generate_master_crucible_pdf()
        self.assertIsInstance(pdf, (bytes, bytearray))
        self.assertGreater(len(pdf), 500)

        # DOCX Bytes
        docx = generate_master_crucible_docx()
        self.assertIsInstance(docx, (bytes, bytearray))
        self.assertGreater(len(docx), 500)

    def test_master_bundle_zip(self):
        zip_bytes = generate_master_crucible_bundle_zip()
        self.assertGreater(len(zip_bytes), 1000)
        with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
            names = zf.namelist()
            self.assertIn("01_MASTER_DEPOSITION_PERJURY_CRUCIBLE_28LINE.pdf", names)
            self.assertIn("01_MASTER_DEPOSITION_PERJURY_CRUCIBLE.docx", names)
            self.assertIn("02_TARGET_SCOT_BROWER_CROSS_EXAM_SCRIPT.txt", names)
            self.assertIn("02_TARGET_GREG_RYAN_CROSS_EXAM_SCRIPT.txt", names)
            self.assertIn("06_ALL_71_PERJURY_TRAPS_MAPPED_SCHEDULE.json", names)
            self.assertIn("00_CRUCIBLE_MANIFEST_AND_SHA256_RECEIPTS.json", names)

            # Check JSON traps
            traps_data = json.loads(zf.read("06_ALL_71_PERJURY_TRAPS_MAPPED_SCHEDULE.json"))
            self.assertGreaterEqual(len(traps_data), 71)

    def test_api_routes(self):
        # 1. Overview
        ov = get_deposition_crucible_route()
        self.assertEqual(ov["status"], "OPERATIONAL")

        # 2. Targets list
        targets_res = get_deposition_targets_route()
        self.assertEqual(targets_res["count"], 5)

        # 3. Single target
        brower = get_deposition_target_plan_route("scot_brower")
        self.assertEqual(brower["actor_name"], "Scot S. Brower, Esq.")

        # 4. Downloads
        pdf_res = download_deposition_crucible_pdf()
        self.assertGreater(len(pdf_res.body), 500)

        docx_res = download_deposition_crucible_docx()
        self.assertGreater(len(docx_res.body), 500)

        zip_res = download_deposition_crucible_zip()
        self.assertGreater(len(zip_res.body), 1000)

        # 5. Simulation Route
        req = CrucibleSimulateRequest(
            target_id="scot_brower",
            question_id="SB-P02-Q01",
            witness_statement="I do not recall the time I left."
        )
        sim_res = simulate_crucible_route(req)
        self.assertEqual(sim_res["status"], "SUCCESS")
        self.assertEqual(sim_res["impeachment_status"], "IMPEACHED_BY_L0")

        # 6. TestClient HTTP check if available
        if self.client:
            res = self.client.get("/api/v1/forensics/estate/deposition-crucible")
            self.assertEqual(res.status_code, 200)

            res2 = self.client.get("/api/v1/forensics/estate/deposition-crucible/targets")
            self.assertEqual(res2.status_code, 200)
            self.assertEqual(res2.json()["count"], 5)

            res3 = self.client.get("/api/v1/forensics/estate/deposition-crucible/target/scot_brower")
            self.assertEqual(res3.status_code, 200)

            res4 = self.client.post("/api/v1/forensics/estate/deposition-crucible/simulate", json={
                "target_id": "scot_brower",
                "question_id": "SB-P02-Q01",
                "witness_statement": "I do not recall."
            })
            self.assertEqual(res4.status_code, 200)
            self.assertEqual(res4.json()["impeachment_status"], "IMPEACHED_BY_L0")


if __name__ == "__main__":
    unittest.main()
