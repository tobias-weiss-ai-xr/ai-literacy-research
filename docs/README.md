# AI-Literacy Research — Documentation Index

## Research Program

| Document | Purpose |
|----------|---------|
| [`research/RESEARCH_PLAN.md`](research/RESEARCH_PLAN.md) | The research program: questions, method, phases, deliverables |
| [`research/PROTOCOL.md`](research/PROTOCOL.md) | Systematic review protocol (inclusion, search, extraction, appraisal) |
| [`research/mapping_review.md`](research/mapping_review.md) | Phase 1: cell-level map + per-RQ shortlists (build with `tools/build_shortlists.py`) |
| [`research/taxonomy.md`](research/taxonomy.md) | The 20×8 taxonomy definition |
| [`research/literature_review.md`](research/literature_review.md) | Synthesis of the corpus |
| [`research/ai_literacy_trends_2026.md`](research/ai_literacy_trends_2026.md) | Trend analysis for the research program |
| [`research/landscape_report.md`](research/landscape_report.md) | Full corpus landscape analysis |

## Topics (Generated)

| Document | Purpose |
|----------|---------|
| [`topics/ARTICLE_TOPICS.md`](topics/ARTICLE_TOPICS.md) | Evidence-ranked content topics |

## Data Files

| File | Description |
|------|-------------|
| `../papers.yaml` | Source of truth (paper metadata) |
| `../papers.json` | JSON export of all papers |
| `../statistics.json` | Machine-readable statistics |

## Regenerating

```bash
python3 tools/build_shortlists.py --papers 30   # mapping_review.md + shortlists.json
python3 scripts/analysis/generate_analysis.py   # statistics.json + papers.json
python3 scripts/visualize_statistics.py          # PNG charts
python3 tools/trend_scanner.py --months 6        # trend report
python3 tools/topic_planner.py --top 10          # ARTICLE_TOPICS.md
python3 scripts/analysis/generate_reports.py     # literature review + trends
python3 scripts/generate_readme.py               # README.md
```