#!/usr/bin/env python3
"""Generate README.md from statistics.json (ai-literacy-research edition).

Usage:
    python3 scripts/generate_readme.py          # write README.md
    python3 scripts/generate_readme.py --check  # verify README is up to date (CI)
"""

import argparse
import json
import os
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

CATEGORY_DISPLAY = {
    "ai-literacy-construct": "AI Literacy Constructs & Models",
    "ai-literacy-pedagogy": "AI Literacy Pedagogy",
    "learning-design": "Learning Design & Curriculum",
    "assessment": "Assessment & Measurement",
    "workforce-upskilling": "Workforce Upskilling",
    "org-implementation": "Org Implementation & Change",
    "sme-training": "SME Training & Adoption",
    "compliance": "Compliance & AI Act",
    "k12-education": "K-12 Education",
    "higher-education": "Higher Education",
    "professional-education": "Professional & Executive Ed",
    "teacher-ai-literacy": "Teacher AI Literacy",
    "critical-ai-literacy": "Critical & Ethical AI Literacy",
    "generative-ai-skills": "Generative AI Skills",
    "attitudes-trust": "Attitudes, Trust & Acceptance",
    "adoption-behavior": "Adoption Behavior & Engagement",
    "program-evaluation": "Program Evaluation & Outcomes",
    "roi-measurement": "ROI & Business Impact",
    "tooling": "Tools, Platforms & AI Tutors",
    "lifelong-learning": "Lifelong & Self-Directed Learning",
}

SUBCATEGORY_DISPLAY = {
    "theory": "Theory",
    "mechanism": "Mechanism",
    "method": "Method",
    "application": "Application",
    "development": "Development",
    "systems": "Systems & Technology",
    "evaluation": "Evaluation & Benchmarks",
    "review": "Reviews & Surveys",
}


def render_readme(stats):
    meta = stats["metadata"]
    total = meta["total_papers"]
    saturation = meta["taxonomy"]["saturation"]
    filled = meta["taxonomy"]["filled_cells"]
    total_cells = meta["taxonomy"]["total_cells"]
    by_cat = stats["by_category"]
    by_sub = stats["by_subcategory"]
    by_year = stats["by_year"]
    by_cell = stats["by_cell"]
    themes = stats.get("emerging_themes_12m", [])

    years = [y for y in by_year if y != "unknown"]
    ymin = min(years, default="—")
    ymax = max(years, default="—")

    top_cats = sorted(by_cat.items(), key=lambda kv: -kv[1])[:6]
    top_cats_rows = "\n".join(
        f"{i+1}. **{CATEGORY_DISPLAY[c]}** — {n} papers" for i, (c, n) in enumerate(top_cats)
    )

    theme_rows = "\n".join(
        f"{i+1}. **{t['keyword']}** — {t['papers']} papers" for i, t in enumerate(themes[:6])
    )

    momentum = stats.get("momentum", [])[:6]
    mom_rows = "\n".join(
        f"| {m['name']} | {m['total']} | {m['recent']} | "
        + (f"{m['growth_pct']:+}%" if m['growth_pct'] is not None else "—")
        + f" | {m['recent_share']*100:.0f}% |"
        for m in momentum
    )

    thin = sorted(by_cell.items(), key=lambda kv: kv[1])[:8]
    gap_rows = "\n".join(f"- `{c}` — {n} papers" for c, n in thin)

    cat_table = "\n".join(
        f"| {CATEGORY_DISPLAY[c]} | {by_cat.get(c, 0)} |"
        for c in CATEGORY_DISPLAY
    )
    sub_table = "\n".join(
        f"| {SUBCATEGORY_DISPLAY[s]} | {by_sub.get(s, 0)} |"
        for s in SUBCATEGORY_DISPLAY
    )

    return f"""# AI-Literacy Research Corpus

**Research program** — AI-literacy implementation & evaluation. Close the two
emptiest cells of the business-development corpus (`ai-adoption/development`
and `ai-adoption/evaluation`): *how to implement* AI-literacy programs in
organizations and *how to measure* them.

**Author:** Tobias Weiss
**Contact:** ki-kompetenz-training@tobias-weiss.org
**Website:** [ki-kompetenz-training.org](https://www.ki-kompetenz-training.org)

---

## 🎯 Overview

This repository is the evidence base for the AI-literacy research program:
a corpus of {total:,} papers across 20 AI-literacy disciplines, analyzed with
the same taxonomy → momentum → burst → gap pipeline as
[business-development-research](https://github.com/tobias-weiss-ai-xr/business-development-research)
and [graph-research](https://github.com/tobias-weiss-ai-xr/graph-research).

**Research target:** the definitive, corpus-grounded guides on
(1) **implementing** AI-literacy programs (development gap) and
(2) **evaluating** them (evaluation gap, Kirkpatrick levels 3–4) —
feeding the ALaaS offer, the content site and the learning platform.

### Research Scope

| Metric | Value |
|--------|-------|
| **Papers Analyzed** | {total:,} |
| **AI-Literacy Disciplines** | {len(CATEGORY_DISPLAY)} |
| **Time Span** | {ymin}-{ymax} |
| **Research Aspects** | {len(SUBCATEGORY_DISPLAY)} |
| **Taxonomy Cells** | {total_cells} |
| **Saturation** | {saturation}% ({filled}/{total_cells} cells) |

### Top Evidence Areas

{top_cats_rows}

---

## 📊 The 20-Category Taxonomy

| Category | Papers |
|----------|--------|
{cat_table}

### Research Aspects (Subcategories)

| Aspect | Papers |
|--------|--------|
{sub_table}

---

## 🚀 Emerging Themes (Last 12 Months)

{theme_rows}

## 📈 Category Momentum (Last 12 Months)

Ranked by output density × year-over-year growth — the strongest leading indicator for what to study next:

| Category | Total | Last 12m | Growth | 12-m share |
|----------|------:|---------:|-------:|-----------:|
{mom_rows}

---

## 🕳️ Research Gaps (Thinnest Cells)

Cells with the fewest papers mark the white space this program targets
(especially `*/development` and `*/evaluation`):

{gap_rows if gap_rows else "- (corpus still saturating — see `statistics.json`) *"}

---

## 📁 Repository Structure

```
ai-literacy-research/
├── README.md                          # This file
├── papers.json                        # Paper metadata (JSON export)
├── papers.yaml                        # Paper metadata (source of truth)
├── statistics.json                    # Analysis statistics
├── requirements.txt                   # Python dependencies
│
├── assets/visualizations/             # Generated charts and graphs
│
├── docs/
│   ├── research/                      # Research plan, protocol, literature review
│   │   ├── RESEARCH_PLAN.md           # Research program (questions, method) ✨
│   │   ├── PROTOCOL.md                # Systematic review protocol
│   │   └── taxonomy.md                # The 20×8 taxonomy
│   └── topics/                        # Generated content topics
│
├── tools/                             # Research & content tools
│   ├── topic_planner.py               # Topic planner ✨
│   ├── trend_scanner.py               # Emerging trend scanner ✨
│   ├── brief_generator.py             # Brief generator ✨
│   └── landscape_analyzer.py          # Landscape report ✨
│
├── scripts/                           # Research pipeline
│   ├── fetch/                         # OpenAlex (primary), arXiv, DBLP/CrossRef
│   ├── analysis/generate_analysis.py  # Statistics + visualizations
│   ├── validate_papers.py             # Corpus validation
│   └── generate_readme.py             # README generator
│
└── examples/                          # Usage examples
```

---

## 🔬 Research Program

| Deliverable | Targets the gap | Status |
|-------------|-----------------|--------|
| **Guide 1: Implementing AI-literacy programs** | `*/development`, `org-implementation`, `learning-design` | planned (see `docs/research/RESEARCH_PLAN.md`) |
| **Guide 2: Evaluating AI-literacy programs** | `*/evaluation`, `program-evaluation`, `roi-measurement` | planned |
| **Assessment instrument** | `assessment` | planned |

## 🛠️ Tools

```bash
cd tools
python3 topic_planner.py --top 10               # ranked evidence areas
python3 trend_scanner.py --months 6             # keyword bursts
python3 brief_generator.py "EU AI Act literacy obligations" --papers 5
python3 landscape_analyzer.py --write-doc       # full landscape
```

---

## 🔄 Research Pipeline

1. **Discover** — `python3 scripts/fetch/fetch_openalex.py --months 3`
2. **Validate** — `python3 scripts/validate_papers.py`
3. **Analyze** — `python3 scripts/analysis/generate_analysis.py`
4. **Visualize** — `python3 scripts/visualize_statistics.py`
5. **Report** — `python3 scripts/analysis/generate_reports.py`
6. **Generate** — `python3 scripts/generate_readme.py`

CI (`.github/workflows/validate.yml`) validates and regenerates on every push;
a weekly scheduled job opens a PR with newly discovered papers.

---

## 🔗 Related Repositories

- **Source corpus:** [business-development-research](https://github.com/tobias-weiss-ai-xr/business-development-research) — the `ai-adoption` category (380 papers) this program grew out of
- **Content site:** [ki-kompetenz-training](https://github.com/tobias-weiss-ai-xr/ki-kompetenz-training)
- **Analogous corpus:** [learning-research](https://github.com/tobias-weiss-ai-xr/learning-research)
- **Analogous corpus:** [graph-research](https://github.com/tobias-weiss-ai-xr/graph-research)

---

## 📄 License

**© 2026 KI-Kompetenz-Training | Tobias Weiss**

- **Research corpus:** Proprietary
- **Tools:** MIT License

---

## 🙏 Acknowledgments

This corpus synthesizes {total:,} papers across {ymin}-{ymax} to create the
evidence base for the AI-literacy implementation and evaluation research
program — and ultimately for better AI-literacy programs everywhere.

---

**Want to explore the corpus?**
`cd tools && python3 landscape_analyzer.py`
"""


def main():
    parser = argparse.ArgumentParser(description="Generate README.md")
    parser.add_argument("--check", action="store_true", help="Verify README is current")
    args = parser.parse_args()

    stats_path = BASE / "statistics.json"
    if not stats_path.exists():
        print("ERROR: statistics.json not found — run scripts/analysis/generate_analysis.py first")
        sys.exit(1)

    with open(stats_path, encoding="utf-8") as f:
        stats = json.load(f)

    readme = render_readme(stats)
    readme_path = BASE / "README.md"

    if args.check:
        if readme_path.exists() and readme_path.read_text(encoding="utf-8") == readme:
            print("README.md is up to date")
        else:
            print("README.md is OUT OF DATE — run scripts/generate_readme.py")
            sys.exit(1)
    else:
        readme_path.write_text(readme, encoding="utf-8")
        print(f"Wrote README.md ({len(readme)} chars)")


if __name__ == "__main__":
    main()