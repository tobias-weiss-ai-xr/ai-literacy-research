import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import evb_it_compliance_checker as chk  # noqa: E402

# Szenario: Kommune kauft KI-Literacy-Training für Schulen via SaaS
# (Schülerdaten = besondere Kategorie, KI = High-Risk)
MUNICIPAL_SCHOOL_SAAS = {
    "buyer_is_public_sector": True,
    "buyer_type": "kommune",
    "service_type": "cloud_saas",
    "involves_personal_data": True,
    "special_category_data": True,
    "uses_ai": True,
    "ai_high_risk": True,
    "open_source_components": False,
    "sovereignty_required": True,
    "dsgvo_av_contract_in_place": False,
    "subcontracting_approved": False,
    "acceptance_procedure_defined": True,
    "confidentiality_agreed": True,
    "security_toms_defined": False,
    "audit_rights_granted": False,
    "liability_insurance_in_place": True,
    "sovereignty_measured": False,
    "ai_act_conformity_declared": False,
    "oss_license_compliant": True,
    "tender_compliant": True,
    "dsgvo_special_ok": False,
}


@pytest.fixture
def kb():
    return chk.load_kb()


def test_applicable_families_cloud_saas(kb):
    r = chk.evaluate(MUNICIPAL_SCHOOL_SAAS, kb)
    assert "general" in r["applicable_families"]
    assert "cloud" in r["applicable_families"]
    # Nicht anwendbar bei cloud_saas + kein OSS:
    assert "dienstleistung" not in r["applicable_families"]
    assert "transfer" not in r["applicable_families"]


def test_cloud_obligations_grounded_in_vendored_repo(kb):
    r = chk.evaluate(MUNICIPAL_SCHOOL_SAAS, kb)
    ids = [o["id"] for o in r["obligations"]]
    assert "cloud-dsgvo" in ids
    cloud_dsgvo = next(o for o in r["obligations"] if o["id"] == "cloud-dsgvo")
    assert "vendor/evb-it" in cloud_dsgvo["source"]
    # Kritische Pflichten aus dem Cloud-Vertrag sind present
    assert "cloud-subcontract" in ids
    assert "cloud-security" in ids


def test_oss_family_only_when_open_source(kb):
    p = dict(MUNICIPAL_SCHOOL_SAAS, open_source_components=True)
    r = chk.evaluate(p, kb)
    assert "transfer" in r["applicable_families"]
    assert any(o["id"] == "transfer-oss" for o in r["obligations"])


def test_readiness_gap_logic(kb):
    r = chk.evaluate(MUNICIPAL_SCHOOL_SAAS, kb)
    assert r["critical_gap_count"] >= 1
    assert r["readiness_level"] == "nicht bereit"
    assert 0 < r["readiness_score"] < 100
    # Jede Lücke ist im recommendations-Array
    assert len(r["recommendations"]) == len(r["gaps"])


def test_full_ok_profile_is_ready(kb):
    p = dict(MUNICIPAL_SCHOOL_SAAS)
    for k in (
        "dsgvo_av_contract_in_place",
        "dsgvo_special_ok",
        "ai_act_conformity_declared",
        "sovereignty_measured",
        "subcontracting_approved",
        "security_toms_defined",
        "audit_rights_granted",
    ):
        p[k] = True
    r = chk.evaluate(p, kb)
    assert r["critical_gap_count"] == 0
    assert r["readiness_level"] == "bereit"
    assert r["readiness_score"] == 100.0


def test_predicate_dsl_safe(kb):
    # Ungültiges Profil (fehlende Felder) darf nicht crashen
    r = chk.evaluate({}, kb)
    assert r["applicable_families"] == []
    assert r["readiness_score"] == 100.0
