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
    get_estate_capabilities_route,
    get_strike_manifest_route,
    download_unpacked_file_route,
    get_legal_repositories_route,
    load_legal_repositories,
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

    def test_estate_capabilities_route(self):
        res = get_estate_capabilities_route()
        self.assertGreaterEqual(res["total_capabilities"], 60)
        self.assertGreaterEqual(len(res["domains"]), 8)
        self.assertIn("MEGA_SKILLS", res["domains"])
        self.assertIn("LEGAL_WARFARE", res["domains"])

        skills_res = get_estate_capabilities_route("MEGA_SKILLS")
        self.assertGreaterEqual(skills_res["total_capabilities"], 5)
        for c in skills_res["capabilities"]:
            self.assertEqual(c["domain"], "MEGA_SKILLS")

    def test_strike_manifest_and_unpacked_files(self):
        manifest = get_strike_manifest_route()
        self.assertIn("unpacked_packages", manifest)
        self.assertGreaterEqual(manifest["unpacked_package_count"], 20)
        self.assertGreaterEqual(manifest["total_unpacked_files"], 100)

        # Test downloading an unpacked file from the first available package
        folder = manifest["unpacked_packages"][0]["folder"]
        filename = manifest["unpacked_packages"][0]["files"][0]["name"]
        file_resp = download_unpacked_file_route(folder, filename)
        self.assertEqual(file_resp.status_code, 200)
        self.assertGreater(len(file_resp.body), 0)

    def test_legal_repositories_mesh(self):
        # 1. Total legal repositories catalog
        res = get_legal_repositories_route()
        self.assertEqual(res["total_repositories"], 160)
        self.assertEqual(res["total_estate_legal_nodes"], 160)
        self.assertEqual(len(res["pillars"]), 8)

        # 2. Verify all 8 Strategic Pillars
        pillar_ids = [p["pillar_number"] for p in res["pillars"]]
        self.assertEqual(pillar_ids, [1, 2, 3, 4, 5, 6, 7, 8])

        # 3. Test Pillar 1 filter (Core Litigation & RICO)
        p1_res = get_legal_repositories_route(pillar=1)
        self.assertEqual(p1_res["total_repositories"], 35)
        for r in p1_res["repositories"]:
            self.assertEqual(r["pillar_number"], 1)
            self.assertIn("apex-legal", r["topics"])
            self.assertIn("legal-mesh", r["topics"])
            self.assertIn("core-litigation", r["topics"])

        # 4. Test Pillar 3 filter (Cherry Chan Recovery)
        p3_res = get_legal_repositories_route(pillar=3)
        self.assertEqual(p3_res["total_repositories"], 6)
        p3_names = [r["name"] for r in p3_res["repositories"]]
        self.assertTrue(any("CAMARO" in n for n in p3_names))
        self.assertTrue(any("NV-UI" in n or "MEUC" in n for n in p3_names))

        # 5. Test Pillar 4 filter (Hospital Fraud & Kekoa Child Safety)
        p4_res = get_legal_repositories_route(pillar=4)
        self.assertEqual(p4_res["total_repositories"], 12)
        for r in p4_res["repositories"]:
            self.assertEqual(r["pillar_number"], 4)

        # 6. Test keyword search
        search_res = get_legal_repositories_route(search="USAA")
        self.assertGreaterEqual(search_res["total_repositories"], 7)
        for r in search_res["repositories"]:
            matched = "usaa" in r["name"].lower() or "usaa" in r["description"].lower() or any("usaa" in t.lower() for t in r["topics"])
            self.assertTrue(matched)

        # 7. Check 1FDV flagship presence
        search_1fdv = get_legal_repositories_route(search="1FDV-23-0001009")
        self.assertGreaterEqual(search_1fdv["total_repositories"], 5)

if __name__ == "__main__":
    unittest.main()
