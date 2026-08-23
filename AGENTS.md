# AGENTS.md — AI Literacy Research Corpus

Guidance for coding/research agents working in this repository. The corpus
(`papers.yaml`, 11k+ papers across a 20×8 taxonomy) is the source of truth
for content; tooling and reports stay reproducible from it.

## Ground Rules

1. **`papers.yaml` is input; everything else is derived.** Never hand-edit
   generated artifacts — see the read-only list below. If a report is stale,
   regenerate it with the pipeline, don't patch it.
2. **Read-only generated artifacts** (regenerate, don't edit, and don't review
   by patching): `README.md` (corpus statistics sections), `statistics.json`,
   `papers.json`, `assets/ai_literacy_analysis.json`,
   `assets/visualizations/*`, `docs/research/gap_analysis.md`,
   `docs/research/literature_review.md`, `docs/research/landscape_report.md`,
   `docs/topics/ARTICLE_TOPICS.md`, `docs/topics/*`.
3. **Taxonomy is config.** Category/subcategory display names live in
   `config/taxonomy.yaml` (fallbacks in `tools/research_config.py`). Adding a
   category is a taxonomy change — propose separately, don't silently extend
   the file.

## Full Pipeline (after any `papers.yaml` change)

```bash
python3 scripts/validate_papers.py
python3 scripts/analysis/generate_analysis.py        # statistics.json
python3 tools/research_gap_analyzer.py --write-doc   # docs/research/gap_analysis.md
python3 scripts/visualize_statistics.py
python3 scripts/refresh_readme_stats.py
python3 tools/topic_planner.py --top 10
python3 scripts/analysis/generate_reports.py
```

Then commit the generated artifacts together with the change (CI checks the
gap report is current).

## Common Tasks

- **What are the research gaps?**
  `python3 tools/research_gap_analyzer.py --write-doc` → ranked thin-and-
  surging cells in `docs/research/gap_analysis.md` (thinness × momentum).
- **Regenerate statistics:**
  `python3 scripts/analysis/generate_analysis.py`
- **Validate the corpus:**
  `python3 scripts/validate_papers.py`
- **Refresh the README:**
  `python3 scripts/refresh_readme_stats.py`
- **Full landscape report:**
  `python3 tools/landscape_analyzer.py --write-doc`
- **Discover new papers (arXiv):**
  `python3 scripts/fetch/fetch_new_papers.py --months 1 --create-pr`
- **OpenAlex refresh (mind free credits):**
  `python3 scripts/fetch/fetch_openalex.py --months 3`

## Speccing Changes

This repo uses OpenSpec (`openspec/`). Behavior changes start as a delta in
`openspec/changes/<name>/` (proposal → design → delta spec → tasks); specs in
`openspec/specs/` are the source of truth. See `openspec/README.md`.
