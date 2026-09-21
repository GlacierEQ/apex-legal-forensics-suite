"""
Unit & Integration Tests for APEX Holographic Mesh Swarm Personas Engine
Enforces 18 Canonical Roles, Execution Postures, Composite Presets, and §0 Hard Invariants.
"""

import pytest
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.persona_engine import (
    get_estate_personas,
    get_persona_detail,
    get_execution_modes,
    get_composite_presets,
    get_persona_overview,
    dispatch_persona_mission,
    PERSONA_REGISTRY
)

client = TestClient(app)

class TestPersonaEngine:
    def test_all_18_personas_registered(self):
        personas = get_estate_personas()
        assert len(personas) == 18
        ids = [p["id"] for p in personas]
        expected_roles = [
            "adversarial_counsel", "case_forensics_specialist", "evidence_authenticator",
            "brief_architect", "legal_research_agent", "contradiction_hunter",
            "citation_verifier", "procedural_strategist", "systems_architect",
            "implementation_engineer", "reliability_engineer", "performance_engineer",
            "repository_cartographer", "capability_miner", "connector_broker",
            "red_team_auditor", "holographic_mesh_coordinator", "zero_hallucination_gate"
        ]
        for role in expected_roles:
            assert role in ids, f"Missing role: {role}"

    def test_persona_domain_filtering(self):
        legal_personas = get_estate_personas("legal")
        assert len(legal_personas) >= 5
        for p in legal_personas:
            assert p["domain"] == "legal" or p["category"].lower() == "legal"

        forensics_personas = get_estate_personas("forensics")
        assert len(forensics_personas) >= 3
        for p in forensics_personas:
            assert p["domain"] == "forensics" or p["category"].lower() == "forensics"

    def test_persona_detail(self):
        viper = get_persona_detail("adversarial_counsel")
        assert viper is not None
        assert viper["callsign"] == "REDTEAM-LEGAL-VIPER"
        assert "FRE/HRE 601/602" in viper["system_prompt"]
        assert "elite" in viper["system_prompt"]
        assert len(viper["key_weapons"]) > 0

        invalid = get_persona_detail("nonexistent_persona")
        assert invalid is None

    def test_execution_modes(self):
        modes = get_execution_modes()
        assert len(modes) >= 12
        assert "pro-elite" in modes
        assert "deep-swarm" in modes
        assert "omni-swarm-lifetime" in modes
        assert "conservative" in modes
        assert "aggressive" in modes

    def test_composite_presets(self):
        composites = get_composite_presets()
        assert len(composites) >= 9
        assert "legal-strike" in composites
        assert "litigation-colossus" in composites
        assert "pro-elite" in composites

        # Verify composite references valid roles
        for comp_id, comp in composites.items():
            for role in comp["roles"]:
                assert role in PERSONA_REGISTRY, f"Composite {comp_id} references unknown role {role}"

    def test_persona_overview(self):
        overview = get_persona_overview()
        assert overview["total_personas"] == 18
        assert overview["total_execution_modes"] >= 12
        assert overview["governance_model"] == "Holographic Mesh (Decentralized, Multi-Node)"
        assert "FRE 601/602" in overview["evidentiary_invariant"]

    def test_dispatch_persona_mission(self):
        res = dispatch_persona_mission(
            persona_id="brief_architect",
            objective="Draft Emergency Motion for Full Restitution and Void Orders under HFCR 60(b)(4)",
            execution_mode="conservative"
        )
        assert res["status"] == "INITIALIZED"
        assert res["dispatch_id"].startswith("disp-")
        assert res["persona"]["id"] == "brief_architect"
        assert res["execution_mode"]["mode"] == "conservative"
        assert len(res["directives"]) >= 3
        assert res["receipt"]["verification_status"] == "G6_VERIFIED"
        assert len(res["receipt"]["sha256"]) == 64

    def test_api_personas_endpoints(self):
        # GET all personas
        res = client.get("/api/v1/forensics/estate/personas")
        assert res.status_code == 200
        data = res.json()
        assert data["count"] == 18
        assert len(data["personas"]) == 18

        # GET filtered personas
        res_filter = client.get("/api/v1/forensics/estate/personas?domain=legal")
        assert res_filter.status_code == 200
        assert res_filter.json()["count"] >= 5

        # GET overview
        res_ov = client.get("/api/v1/forensics/estate/personas/overview")
        assert res_ov.status_code == 200
        assert res_ov.json()["total_personas"] == 18

        # GET modes & composites
        res_modes = client.get("/api/v1/forensics/estate/personas/modes")
        assert res_modes.status_code == 200
        assert "pro-elite" in res_modes.json()

        res_comp = client.get("/api/v1/forensics/estate/personas/composites")
        assert res_comp.status_code == 200
        assert "litigation-colossus" in res_comp.json()

        # GET specific persona
        res_spec = client.get("/api/v1/forensics/estate/persona/case_forensics_specialist")
        assert res_spec.status_code == 200
        assert res_spec.json()["callsign"] == "CHRONO-FORENSIC-HAWK"

        # POST dispatch
        dispatch_payload = {
            "persona_id": "adversarial_counsel",
            "mission_objective": "Red-team the 28-line Civil RICO Complaint against Scot Brower & Greg Ryan",
            "execution_mode": "pro-elite"
        }
        res_disp = client.post("/api/v1/forensics/estate/personas/dispatch", json=dispatch_payload)
        assert res_disp.status_code == 200
        disp_data = res_disp.json()
        assert disp_data["status"] == "INITIALIZED"
        assert disp_data["receipt"]["verification_status"] == "G6_VERIFIED"
