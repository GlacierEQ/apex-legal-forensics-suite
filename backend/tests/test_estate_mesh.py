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
)
from backend.app.main import (
    get_estate_overview_route,
    get_estate_matters_route,
    get_estate_actors_route,
    get_estate_perjury_traps_route,
    get_estate_graph_route,
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

if __name__ == "__main__":
    unittest.main()
