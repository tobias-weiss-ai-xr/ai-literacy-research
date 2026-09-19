#!/usr/bin/env python3
"""Merge a fetched round file into papers.yaml, keeping only AI-literacy-relevant papers.

The incremental OpenAlex `search=` fetch is OR-semantics and returns a lot of
off-topic hits. This gate keeps only entries whose title mentions an AI term
AND (context term in title OR abstract), then appends the clean subset.

Usage:
    python3 scripts/fetch/merge_round.py _distributed/round_2026-09-19.yaml
"""
import re
import sys
from pathlib import Path

import yaml

AI = re.compile(
    r"\b(ai|artificial intelligence|chatgpt|chat ?gpt|gpt-?4|generative ai|genai|"
    r"large language model|large-language model|llm|llms|machine learning|neural network|"
    r"deep learning|prompt|agentic|ai-|copilot|gen ?ai|intelligent tutor|ai-powered|"
    r"ai assisted|ai-assisted|ai-based|ai driven|ai-driven|smart classroom|ai literacy)\b",
    re.I,
)
CTX = re.compile(
    r"\b(literacy|competence|competency|skill|education|educational|learning|teaching|"
    r"teacher|student|pedagogy|training|train |workforce|employee|upskill|reskill|"
    r"organi[sz]ation|school|curriculum|assessment|evaluation|tutor|classroom|profession|"
    r"workplace|firm|enterprise|adult education|higher education|k-?12|academic|learners)\b",
    re.I,
)


def relevant(p):
    title = p["title"]
    abstract = p.get("abstract", "") or ""
    ai = bool(AI.search(title))
    return ai and (bool(CTX.search(title)) or bool(CTX.search(abstract)))


def main():
    round_path = Path(sys.argv[1])
    yaml_path = Path(__file__).resolve().parent.parent.parent / "papers.yaml"

    with open(yaml_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    with open(round_path, encoding="utf-8") as f:
        round_data = yaml.safe_load(f)

    old = data["papers"]
    old_keys = {p.get("url") for p in old}
    old_titles = {p["title"].lower() for p in old}

    added = [
        p
        for p in round_data["papers"]
        if p.get("url") not in old_keys and p["title"].lower() not in old_titles
    ]
    kept = [p for p in added if relevant(p)]

    data["papers"] = old + kept
    with open(yaml_path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    print(f"round={len(added)} kept={len(kept)} dropped={len(added)-len(kept)} "
          f"corpus now {len(data['papers'])}")


if __name__ == "__main__":
    main()
