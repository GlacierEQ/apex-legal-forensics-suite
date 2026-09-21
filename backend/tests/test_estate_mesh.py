import unittest
import sys
from pathlib import Path

# Ensure package path is resolvable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from backend.app.estate_mesh_engine import (
    get_estate_overview,
    get_estate_matters,
    get_estate_actors,
    get_estate_perjury_traps,
    get_estate_graph,
    get_matter_detail,
    generate_matter_packet,
    generate_matter_pdf,
    generate_matter_docx,
    generate_matter_bundle_zip,
)
from backend.app.main import (
    get_estate_overview_route,
    get_estate_matters_route,
    get_estate_actors_route,
    get_estate_perjury_traps_route,
    get_estate_graph_route,
    get_matter_detail_route,
    get_matter_packet_route,
    download_matter_pdf_route,
    download_matter_docx_route,
    download_matter_zip_route,
)

class TestEstateMeshEngine(unittest.TestCase):
    def test_estate_overview(self):
        overview = get_estate_overview()
        self.assertEqual(overview["status"], "ONLINE")
        self.assertEqual(overview["total_matters"], 21)
        self.assertGreaterEqual(overview["total_exposure_usd"], 200000000.0)
        self.assertEqual(overview["conspiracy_actors_count"], 18)
        self.assertEqual(overview["perjury_traps_count"], 71)
        self.assertEqual(overview["certified_exhibits_count"], 73)
        self.assertEqual(overview["court_filings_count"], 1365)
        self.assertGreaterEqual(overview["mesh_nodes_count"], 200)
        self.assertGreaterEqual(overview["mesh_edges_count"], 200)

    def test_estate_matters(self):
        matters = get_estate_matters()
        self.assertEqual(len(matters), 21)
        # Verify 1FDV is present
        case_ids = [m["case_id"] for m in matters]
        self.assertIn("CASE_1FDV_23_0001009", case_ids)
        self.assertIn("CASE_RICO_1_26_CV_001009", case_ids)
        
        # Portfolio filter
        barton_matters = get_estate_matters("01_CASEY_BARTON")
        self.assertEqual(len(barton_matters), 12)
        cherry_matters = get_estate_matters("02_CHERRY_CHAN")
        self.assertEqual(len(cherry_matters), 9)

    def test_estate_actors(self):
        actors = get_estate_actors()
        self.assertEqual(len(actors), 18)
        names = [a["actor_name"] for a in actors]
        self.assertTrue(any("Brower" in n for n in names))
        self.assertTrue(any("Shaw" in n for n in names))
        self.assertTrue(any("Barton" in n for n in names))
        self.assertTrue(any("CSEA" in n or "Child Support" in n for n in names))

    def test_estate_perjury_traps(self):
        traps = get_estate_perjury_traps()
        self.assertEqual(len(traps), 71)
        first_trap = traps[0]
        self.assertIn("foundation_question", first_trap)
        self.assertIn("impeachment_dilemma", first_trap)
        self.assertIn("statutory_penalty", first_trap)

    def test_estate_graph(self):
        graph = get_estate_graph()
        self.assertGreaterEqual(graph["node_count"], 200)
        self.assertGreaterEqual(graph["edge_count"], 200)

    def test_estate_main_routes(self):
        ov_route = get_estate_overview_route()
        self.assertEqual(ov_route["total_matters"], 21)

        matters_route = get_estate_matters_route()
        self.assertEqual(matters_route["count"], 21)

        actors_route = get_estate_actors_route()
        self.assertEqual(actors_route["count"], 18)

        traps_route = get_estate_perjury_traps_route()
        self.assertEqual(traps_route["count"], 71)

        graph_route = get_estate_graph_route()
        self.assertGreaterEqual(graph_route["node_count"], 200)

    def test_matter_detail_and_dynamic_synthesis(self):
        import zipfile
        import io

        # Test Navy Federal Credit Union matter ($10.5M)
        matter = get_matter_detail("CASE_CHERRY_NFCU")
        self.assertIsNotNone(matter)
        self.assertEqual(matter["case_id"], "CASE_CHERRY_NFCU")
        self.assertEqual(matter["total_damages"], 10500000.0)
        self.assertGreaterEqual(len(matter["perjury_traps"]), 1)
        self.assertGreaterEqual(len(matter["exhibits"]), 1)

        # Generate full court-ready packet
        packet = generate_matter_packet("CASE_CHERRY_NFCU")
        self.assertTrue(packet["verified"])
        self.assertIn("CASE_CHERRY_NFCU", packet["raw_text"])
        self.assertIn("$10,500,000.00", packet["raw_text"])
        self.assertIn("VERIFIED COMPLAINT", packet["raw_text"])
        self.assertIn("HRE 601/602", packet["raw_text"])

        # Generate PDF, DOCX, ZIP
        pdf = generate_matter_pdf(packet)
        self.assertTrue(pdf.startswith(b"%PDF"))
        self.assertGreater(len(pdf), 5000)

        docx = generate_matter_docx(packet)
        self.assertTrue(docx.startswith(b"PK"))
        self.assertGreater(len(docx), 5000)

        zip_bytes = generate_matter_bundle_zip(packet)
        self.assertTrue(zip_bytes.startswith(b"PK"))
        with zipfile.ZipFile(io.BytesIO(zip_bytes), "r") as z:
            names = z.namelist()
            self.assertIn("01_CASE_CHERRY_NFCU_COMPLAINT_28LINE.pdf", names)
            self.assertIn("01_CASE_CHERRY_NFCU_COMPLAINT.docx", names)
            self.assertIn("00_FILING_MANIFEST.json", names)

        # Route tests
        detail_res = get_matter_detail_route("CASE_CHERRY_NFCU")
        self.assertEqual(detail_res["case_id"], "CASE_CHERRY_NFCU")

        packet_res = get_matter_packet_route("CASE_CHERRY_NFCU")
        self.assertTrue(packet_res["verified"])

        pdf_resp = download_matter_pdf_route("CASE_CHERRY_NFCU")
        self.assertEqual(pdf_resp.media_type, "application/pdf")

        docx_resp = download_matter_docx_route("CASE_CHERRY_NFCU")
        self.assertIn("wordprocessingml", docx_resp.media_type)

        zip_resp = download_matter_zip_route("CASE_CHERRY_NFCU")
        self.assertEqual(zip_resp.media_type, "application/zip")

    def test_cherry_chan_recovery_portfolio(self):
        # Verify all 9 matters in Cherry Chan portfolio can generate packets cleanly
        matters = get_estate_matters("02_CHERRY_CHAN")
        self.assertEqual(len(matters), 9)
        total_recovery_exposure = sum(m["total_damages"] for m in matters)
        self.assertGreaterEqual(total_recovery_exposure, 42000000.0)

        for m in matters:
            cid = m["case_id"]
            packet = generate_matter_packet(cid)
            self.assertTrue(packet["verified"], f"Failed on matter {cid}")
            self.assertGreater(len(packet["raw_text"]), 500)
            self.assertEqual(packet["total_damages"], m["total_damages"])

if __name__ == "__main__":
    unittest.main()
