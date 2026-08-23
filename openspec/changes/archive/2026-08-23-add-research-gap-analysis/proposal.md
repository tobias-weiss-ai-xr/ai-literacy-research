# Change: Add Research Gap Analysis

- **Status:** proposed
- **Created:** 2026-08-19
- **Advances:** RQ2, RQ3 (see `docs/research/RESEARCH_PLAN.md`)

## Why

The corpus already surfaces "Research Gaps (Thinnest Cells)" in the generated
README — but only as a static count of the sparsest taxonomy cells. There is
no tool that turns those counts into an actionable analysis: which cells are
thin, how thin relative to the category average, which of them are also
*surging* (high momentum) and therefore the most promising white space to
target next.

This change adds a `tools/research_gap_analyzer.py` that produces a
ranked gap report (`docs/research/gap_analysis.md`), wired into the standard
pipeline and the AGENTS.md contract so agents can drive it.

## What Changes

- **NEW capability:** `research-gap-analysis` — identify, rank, and report
  under-saturated taxonomy cells, cross-referenced with momentum.
- **NEW generated artifact:** `docs/research/gap_analysis.md` (generated,
  read-only like the other reports).
- **NEW pipeline step:** `tools/research_gap_analyzer.py` runs after
  `scripts/standard_stats.py` (it consumes `statistics.json`).
- **UPDATED contract:** `AGENTS.md` lists the gap analyzer in the common
  tasks and re-runs it in the full pipeline.
- **UPDATED CI:** `validate.yml` runs the gap analyzer in the regeneration
  step so the report stays fresh on every push.

## Research Questions Addressed

| RQ | How this change helps |
|----|-----------------------|
| RQ2 (implementation strategies) | Highlights `*/development` cells that are thin AND surging — the cells where implementation evidence is most needed |
| RQ3 (measurement & evaluation) | Highlights `*/evaluation` cells — the README already flags these as the thinnest; this tool ranks them by opportunity |

## Out of Scope

-自动 paper discovery for thin cells (that is the discovery pipeline's job).
- Writing the actual gap-closing research (that is the human/agent author's job).
- Changes to the taxonomy itself (a separate change would add/remove categories).

## Open Questions

1. Should the gap score weight momentum more than absolute count? (Proposal:
   yes — a thin-but-surging cell is more promising than a thin-and-flat one.)
2. Should the report live under `docs/research/` (with the other reports) or
   `docs/topics/`? (Proposal: `docs/research/`, alongside `landscape_report.md`.)
