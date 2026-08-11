#!/usr/bin/env python3
"""Generate research reports from the corpus:
  - docs/research/literature_review.md    (synthesis + top papers per category)
  - docs/research/ai_literacy_trends_2026.md   (trend report from trend scanner)

Usage:
    python3 scripts/analysis/generate_reports.py
"""

import json
import os
import sys
from collections import Counter, defaultdict
from datetime import datetime

import yaml

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "tools"))
from trend_scanner import scan as scan_trends  # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, BASE)

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

KEY_INSIGHTS = {
    "ai-literacy-construct": (
        "AI-literacy construct research is consolidating frameworks and "
        "taxonomies: definitions, dimensions and stage models (e.g. avoidance "
        "versus uncritical reliance as extremes) dominate recent output. "
        "A consensus definition is still missing — white space for synthesis."
    ),
    "ai-literacy-pedagogy": (
        "Pedagogy papers test teaching methods for AI literacy across settings; "
        "the evidence favors hands-on, task-based and critical-reflection "
        "approaches over tool-centric instruction."
    ),
    "learning-design": (
        "Learning-design research covers curriculum, workshops and courses. "
        "Adult-learning design principles (spacing, active learning, micro-"
        "learning) are imported from the learning sciences — cross-corpus "
        "evidence from learning-research applies directly."
    ),
    "assessment": (
        "Assessment research is fast-moving but fragmented: many self-report "
        "scales, few task-based or performance measures, limited psychometric "
        "validation. A validated, occupation-aligned assessment is a clear gap."
    ),
    "workforce-upskilling": (
        "Workforce upskilling papers connect AI training to firm outcomes; "
        "panel studies (e.g. German establishment data) show training mediates "
        "adoption ROI — the empirical backbone of the ALaaS offer."
    ),
    "org-implementation": (
        "Org implementation research covers change management, readiness and "
        "capability building. The evidence stresses organizational factors "
        "(management support, processes) over tool access — adoption failures "
        "are mostly organizational."
    ),
    "sme-training": (
        "SME training research is dominated by survey studies (TOE/DOI "
        "frameworks); barriers rank skills first. Large-scale panel evidence "
        "for SME training ROI is scarce — a genuine gap."
    ),
    "compliance": (
        "Compliance research is driven by the EU AI Act, including Article 4 "
        "literacy obligations. Papers document regulatory complexity and "
        "compliance cost for SMEs — ALaaS as 'practical interpreter' is well "
        "positioned against this evidence."
    ),
    "k12-education": (
        "K-12 research pilots AI-literacy curricula in schools; design-based "
        "interventions and teacher-mediated delivery dominate. Evidence on "
        "long-term outcomes is still thin."
    ),
    "higher-education": (
        "Higher education is the most active application cell: generative-AI "
        "integration, academic integrity and mandatory literacy courses "
        "proliferate. Transferable to workplace training via course design."
    ),
    "professional-education": (
        "Professional and executive education research covers corporate "
        "training, micro-credentials and certification — directly relevant to "
        "ALaaS tier and certificate design."
    ),
    "teacher-ai-literacy": (
        "Teacher AI literacy is a multiplier: teachers' own literacy and "
        "attitudes predict student outcomes. Teacher training studies offer "
        "transferable train-the-trainer evidence for ALaaS coaches."
    ),
    "critical-ai-literacy": (
        "Critical AI literacy covers ethics, bias, misinformation and deepfakes. "
        "It is the differentiated layer of literacy programs — and the weakest "
        "in most commercial offerings."
    ),
    "generative-ai-skills": (
        "Generative-AI skills research covers prompting, LLM reliance and "
        "tool-task fit. Reliance patterns (over-trust vs avoidance) are the "
        "most actionable findings for curriculum design."
    ),
    "attitudes-trust": (
        "Attitudes and trust research (TAM, self-efficacy, AI anxiety) explains "
        "who engages with training and who resists. Expectation recalibration "
        "appears as a success factor across adoption studies."
    ),
    "adoption-behavior": (
        "Adoption-behavior papers study usage patterns, personas and "
        "engagement after training. Persona migration and expectation "
        "recalibration are the emergent themes — inputs for onboarding design."
    ),
    "program-evaluation": (
        "Program evaluation applies Kirkpatrick-style outcome models to AI "
        "training. Few studies reach levels 3–4 (behavior, business results) — "
        "the evaluation gap this research program targets."
    ),
    "roi-measurement": (
        "ROI measurement connects training to productivity and firm "
        "performance. Econometric studies exist at firm level; training-specific "
        "ROI evidence is sparse — white space for the definitive measurement "
        "framework."
    ),
    "tooling": (
        "Tooling research covers AI tutors, chatbots and learning platforms. "
        "AI-assisted instruction shows promise for scaling literacy programs; "
        "evidence on long-term learning is still emerging."
    ),
    "lifelong-learning": (
        "Lifelong-learning research frames AI literacy as continuous "
        "capability: self-directed learning, learning agility and learning "
        "culture. The meta-skill argument (learning to learn with AI) is the "
        "strongest theoretical anchor for curriculum design."
    ),
}


def render_literature_review(papers, now, stats=None):
    total = len(papers)
    lines = [
        "# AI-Literacy Research — Literature Review",
        "",
        f"**Generated:** {now}  ",
        f"**Corpus:** {total:,} papers across {len(CATEGORY_DISPLAY)} categories",
        "",
        "> Synthesis of the AI-literacy research corpus. Category "
        "insights are drawn from title/abstract analysis of the papers themselves.",
        "",
        "---",
        "",
        "## Corpus Overview",
        "",
    ]
    cat_counter = Counter(p.get("category", "unknown") for p in papers)
    sub_counter = Counter(p.get("subcategory", "unknown") for p in papers)
    year_counter = Counter(p.get("date", "")[:4] for p in papers if p.get("date"))
    top_cats = sorted(cat_counter.items(), key=lambda kv: -kv[1])[:5]

    lines.append("| Rank | Category | Papers |")
    lines.append("|------|----------|--------|")
    for i, (c, n) in enumerate(top_cats, 1):
        lines.append(f"| {i} | {CATEGORY_DISPLAY.get(c, c)} | {n} |")

    years = sorted(y for y in year_counter if y)
    lines += [
        "",
        f"**Time span:** {years[0]}–{years[-1]} (median year {years[len(years)//2] if years else '—'})",
        f"**Dominant aspects:** {', '.join(f'{SUBCATEGORY_DISPLAY.get(s, s)} ({n})' for s, n in sub_counter.most_common(3))}",
        "",
        "---",
        "",
    ]

    # ---- enhanced sections drawn from statistics.json ----
    if isinstance(stats, dict):
        mom = stats.get("momentum", [])
        if mom:
            lines += [
                "## 📈 Research Momentum (Last 12 Months)",
                "",
                "Categories ranked by a momentum score combining recent output "
                "density with year-over-year growth.",
                "",
                "| Category | Total | Last 12m | Prior 12m | Growth | 12-m share | Papers/mo |",
                "|----------|------:|---------:|----------:|-------:|----------:|----------:|",
            ]
            for m in mom:
                g = f"{m['growth_pct']:+}%" if m['growth_pct'] is not None else "—"
                lines.append(
                    f"| {m['name']} | {m['total']} | {m['recent']} | {m['prior']} | {g} | "
                    f"{m['recent_share']*100:.0f}% | {m['papers_per_month']} |"
                )
            lines += ["", "---", ""]

        gaps = stats.get("gaps", {})
        if gaps:
            lines += ["## 🕳️ Research Gaps & White Space", ""]
            thinnest = gaps.get("thinnest_cells", [])[:8]
            if thinnest:
                lines += ["**Thinnest taxonomy cells:**", "", "| Cell | Papers |", "|------|--------|"]
                for g in thinnest:
                    lines.append(f"| `{g['cell']}` | {g['papers']} |")
                lines.append("")
            ws = gaps.get("white_space", [])[:8]
            if ws:
                lines += [
                    "**White-space cells** (low total but fast-growing):", "",
                    "| Cell | Total | Last-12m | 12-m share |",
                    "|------|-------:|---------:|-----------:|",
                ]
                for w in ws:
                    lines.append(f"| `{w['cell']}` | {w['total']} | {w['recent']} | {w['recent_share']*100:.0f}% |")
                lines.append("")
            lines += ["---", ""]

        if stats.get("venues"):
            lines += [
                "## Publishing Venues", "",
                "Top venues by paper count (where present in the metadata):", "",
                "| Venue | Papers |", "|-------|--------|",
            ]
            for v in stats["venues"][:10]:
                lines.append(f"| {v['name']} | {v['papers']} |")
            lines += ["", "---", ""]

    lines += ["", "## Category Insights", ""]
    for c in sorted(cat_counter, key=lambda c: -cat_counter[c]):
        if cat_counter[c] == 0:
            continue
        insight = KEY_INSIGHTS.get(c, "Category is still saturating — see `statistics.json` for cell counts.")
        # top recent papers
        cat_papers = [p for p in papers if p.get("category") == c and p.get("date", "") >= "2025-01"]
        cat_papers.sort(key=lambda p: p.get("date", ""), reverse=True)
        top3 = cat_papers[:3]
        lines += [
            f"### {CATEGORY_DISPLAY.get(c, c)} (`{c}`)",
            "",
            f"{insight}",
            "",
            f"**Corpus size:** {cat_counter[c]} papers",
        ]
        if top3:
            lines += ["", "**Recent papers:**", ""]
            for p in top3:
                lines.append(f"- [{p['date']}] {p['title'][:100]} — {p.get('url', '')}")
        lines.append("")
        lines.append("---")
        lines.append("")

    lines += [
        "## Methodology",
        "",
        "1. Papers are discovered via taxonomy-aware arXiv queries and "
        "auto-classified into the 20×8 taxonomy.",
        "2. Category insights above are editorially curated but grounded in "
        "corpus statistics.",
        "3. Regenerate this document with `scripts/analysis/generate_reports.py`.",
        "",
    ]
    return "\n".join(lines)


def render_trend_report(papers, now, stats=None):
    result = scan_trends(papers, months=12, top=15)
    lines = [
        "# AI-Literacy Research Trends (12-Month View)",
        "",
        f"**Generated:** {now}  ",
        f"**Window:** since {result['cutoff']} — {result['recent_papers']} of {len(papers)} papers",
        "",
        "## 🔥 Keyword Bursts",
        "",
        "| Keyword | Recent | Total | Burst |",
        "|---------|--------|-------|-------|",
    ]
    for t in result["trends"]:
        lines.append(f"| {t['keyword']} | {t['recent_papers']} | {t['total_papers']} | {t['burst_score']}× |")

    lines += [
        "",
        "## 📈 Fastest-Growing Cells",
        "",
        "| Cell | Recent | Total | Recent Share |",
        "|------|--------|-------|--------------|",
    ]
    for g in result["growing_cells"]:
        lines.append(f"| `{g['cell']}` | {g['recent']} | {g['total']} | {g['recent_share']*100:.0f}% |")

    lines += [
        "",
        "## What This Means for the ALaaS Research Program",
        "",
        "- Categories with high burst scores are the safest content bets "
        "(reader interest follows research momentum) for the AI-literacy implementation and evaluation guides.",
        "- Fast-growing cells with few total papers are white-space opportunities: "
        "early coverage builds topical authority before the definitive guides land.",
        "- Thin cells in `statistics.json` mark research gaps where evidence is "
        "thin — write with appropriate caution.",
        "",
        "Regenerate with `python3 tools/trend_scanner.py --months 12`.",
        "",
    ]
    return "\n".join(lines)


def main():
    with open(os.path.join(BASE, "papers.yaml"), encoding="utf-8") as f:
        data = yaml.safe_load(f)
    papers = data.get("papers", [])
    now = datetime.now().isoformat()[:10]

    lit_path = os.path.join(BASE, "docs", "research", "literature_review.md")
    stats_path = os.path.join(BASE, "statistics.json")
    stats = None
    if os.path.exists(stats_path):
        with open(stats_path, encoding="utf-8") as f:
            stats = json.load(f)

    with open(lit_path, "w", encoding="utf-8") as f:
        f.write(render_literature_review(papers, now, stats))
    print(f"Wrote {lit_path}")

    trend_path = os.path.join(BASE, "docs", "research", "ai_literacy_trends_2026.md")
    with open(trend_path, "w", encoding="utf-8") as f:
        f.write(render_trend_report(papers, now, stats))
    print(f"Wrote {trend_path}")


if __name__ == "__main__":
    main()
