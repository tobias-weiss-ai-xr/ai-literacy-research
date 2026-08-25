#!/usr/bin/env python3
"""EVB-IT Compliance Checker.

Deterministic, dependency-light (stdlib + pyyaml) checker that maps an IT/AI
procurement profile to the applicable EVB-IT contract families and their
compliance obligations, and reports a readiness score.

Knowledge base: config/compliance/evb_it.yaml (evidenz-basiert, attributiert;
siehe vendor/evb-it/NOTICE.md). Keine Rechtsberatung.

Usage:
    python tools/evb_it_compliance_checker.py --profile profile.json \
        [--kb config/compliance/evb_it.yaml] [--json out.json] [--markdown out.md]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_KB = ROOT / "config" / "compliance" / "evb_it.yaml"


def load_kb(path: Path | None = None) -> dict:
    p = path or DEFAULT_KB
    with open(p, "r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _cmp(actual, op: str, val) -> bool:
    try:
        if op == "==":
            return actual == val
        if op == "!=":
            return actual != val
        if op == "in":
            return actual in (val or [])
        if op == "not_in":
            return actual not in (val or [])
        if op in (">", "<", ">=", "<="):
            if actual is None:
                return False
            a, v = float(actual), float(val)
            return {"gt": a > v, "lt": a < v, "gte": a >= v, "lte": a <= v}[op]
    except (TypeError, ValueError):
        return False
    raise ValueError(f"unknown op {op!r}")


def eval_pred(pred: dict, profile: dict) -> bool:
    """Evaluate a predicate node from the safe DSL (no eval)."""
    if not isinstance(pred, dict):
        raise ValueError(f"invalid predicate: {pred!r}")
    if "all" in pred:
        return all(eval_pred(p, profile) for p in pred["all"])
    if "any" in pred:
        return any(eval_pred(p, profile) for p in pred["any"])
    if "not" in pred:
        return not eval_pred(pred["not"], profile)
    if "field" in pred:
        return _cmp(profile.get(pred["field"]), pred.get("op", "=="), pred.get("value"))
    raise ValueError(f"invalid predicate node: {pred!r}")


def evaluate(profile: dict, kb: dict) -> dict:
    weights = kb.get("meta", {}).get("severity_weights", {})
    applicable_families: list[str] = []
    obligations: list[dict] = []

    for fname, fam in kb.get("families", {}).items():
        if not eval_pred(fam.get("applies_when", {"all": []}), profile):
            continue
        applicable_families.append(fname)
        for ob in fam.get("obligations", []):
            if "check" in ob and not eval_pred(ob["check"], profile):
                continue
            control = ob.get("control")
            ok = bool(profile.get(control)) if control else False
            obligations.append(
                {
                    "id": ob["id"],
                    "family": fname,
                    "dimension": ob.get("dimension", ""),
                    "severity": ob.get("severity", "medium"),
                    "requirement": ob.get("requirement", ""),
                    "source": ob.get("source", ""),
                    "control": control,
                    "status": "ok" if ok else "gap",
                }
            )

    gaps = [o for o in obligations if o["status"] == "gap"]

    def w(sev: str) -> float:
        return float(weights.get(sev, 1))

    total = sum(w(o["severity"]) for o in obligations) or 0.0
    done = sum(w(o["severity"]) for o in obligations if o["status"] == "ok")
    score = round(100.0 * done / total, 1) if total else 100.0

    critical_gaps = [o for o in gaps if o["severity"] == "critical"]
    if score >= 90 and not critical_gaps:
        level = "bereit"
    elif score >= 70 and not critical_gaps:
        level = "teilweise bereit"
    else:
        level = "nicht bereit"

    return {
        "profile_summary": {
            k: profile.get(k)
            for k in (
                "buyer_is_public_sector",
                "buyer_type",
                "service_type",
                "involves_personal_data",
                "special_category_data",
                "uses_ai",
                "ai_high_risk",
                "open_source_components",
                "sovereignty_required",
            )
        },
        "applicable_families": applicable_families,
        "obligations": obligations,
        "gaps": gaps,
        "readiness_score": score,
        "readiness_level": level,
        "critical_gap_count": len(critical_gaps),
        "recommendations": [
            f"[{o['severity'].upper()}] {o['dimension']}: {o['requirement']} "
            f"(Quelle: {o['source']})"
            for o in gaps
        ],
    }


def to_markdown(report: dict) -> str:
    L: list[str] = ["# EVB-IT Compliance Report\n"]
    ps = report["profile_summary"]
    shown = ", ".join(f"{k}={v}" for k, v in ps.items() if v is not None)
    L.append(f"**Szenario:** {shown}")
    L.append(
        f"\n**Readiness:** {report['readiness_score']}% — *{report['readiness_level']}* "
        f"({report['critical_gap_count']} kritische Lücken)\n"
    )
    L.append(
        f"**Anwendbare EVB-IT-Familien:** {', '.join(report['applicable_families'])}\n"
    )
    L.append("## Pflichten (Anwendbar)\n")
    for o in report["obligations"]:
        mark = "OK " if o["status"] == "ok" else "LÜCKE"
        L.append(
            f"- [{mark}] **{o['id']}** ({o['severity']}, {o['dimension']}): "
            f"{o['requirement']}  \n  _Quelle: {o['source']}_"
        )
    if report["gaps"]:
        L.append("\n## Empfehlungen (Lücken schließen)\n")
        for r in report["recommendations"]:
            L.append(f"- {r}")
    return "\n".join(L) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="EVB-IT Compliance Checker")
    ap.add_argument("--profile", required=True, help="JSON profile path")
    ap.add_argument("--kb", default=str(DEFAULT_KB), help="YAML knowledge base path")
    ap.add_argument("--json", dest="json_out", help="write JSON report to path")
    ap.add_argument("--markdown", dest="md_out", help="write Markdown report to path")
    args = ap.parse_args(argv)

    kb = load_kb(Path(args.kb))
    with open(args.profile, "r", encoding="utf-8") as fh:
        profile = json.load(fh)
    report = evaluate(profile, kb)

    out = json.dumps(report, ensure_ascii=False, indent=2)
    if args.json_out:
        Path(args.json_out).write_text(out, encoding="utf-8")
    if args.md_out:
        Path(args.md_out).write_text(to_markdown(report), encoding="utf-8")
    print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
