# research-gap-analysis Specification

## Purpose
TBD - created by archiving change add-research-gap-analysis. Update Purpose after archive.

## Requirements

### Requirement: Research Gap Analysis Tool

The corpus SHALL provide `tools/research_gap_analyzer.py` that identifies
under-saturated taxonomy cells and ranks them by an opportunity score that
combines thinness and momentum, writing the result to
`docs/research/gap_analysis.md`.

Feature: Research Gap Analysis
Rule: The tool reads statistics.json + papers.yaml + taxonomy.yaml and produces a ranked, reproducible gap report.

#### Scenario: Analyzer runs after statistics are generated
- **GIVEN** `statistics.json` exists (produced by `scripts/standard_stats.py`)
- **WHEN** `tools/research_gap_analyzer.py` runs
- **THEN** `docs/research/gap_analysis.md` is written with a ranked gap table and per-cell detail sections

#### Scenario: Gap score combines thinness and momentum
- **GIVEN** a cell with count 2, category average 40, and 12-month growth +150%
- **WHEN** the gap score is computed
- **THEN** the cell scores higher than a cell with count 2, category average 40, and 12-month growth 0%

#### Scenario: Very thin cells receive a floor bonus
- **GIVEN** `--gap-floor 5` and a cell with count 3
- **WHEN** the gap score is computed
- **THEN** a floor bonus is added so very thin cells rank above merely-thin cells with no momentum

#### Scenario: Weights are configurable via CLI
- **GIVEN** the user passes `--thinness-weight 0.7 --momentum-weight 0.3`
- **WHEN** the analyzer runs
- **THEN** the gap score uses the provided weights and the report notes the weights used

#### Scenario: Report lists representative papers per cell
- **GIVEN** a ranked gap cell with at least one paper
- **WHEN** the per-cell section is rendered
- **THEN** up to 5 representative papers (newest first) are listed with title, date, and url

### Requirement: Gap Report Is Generated and Read-Only

`docs/research/gap_analysis.md` SHALL be a generated artifact. It MUST NOT be
edited by hand. The pipeline and CI regenerate it from `statistics.json` and
`papers.yaml`.

Feature: Gap Report Reproducibility
Rule: Delete the report, run the pipeline, get it back identically.

#### Scenario: Full pipeline regenerates the gap report
- **GIVEN** only `papers.yaml`, `config/taxonomy.yaml`, and the scripts exist
- **WHEN** the full pipeline runs including `tools/research_gap_analyzer.py`
- **THEN** `docs/research/gap_analysis.md` is regenerated

#### Scenario: Deterministic output
- **GIVEN** unchanged inputs
- **WHEN** the analyzer runs twice
- **THEN** the generated `docs/research/gap_analysis.md` is byte-identical (no timestamps in the report body)

#### Scenario: Hand-edited report is detected by CI
- **GIVEN** `docs/research/gap_analysis.md` was edited by hand and no longer matches the regenerated output
- **WHEN** CI runs the regeneration check
- **THEN** the check fails and CI blocks the PR

### Requirement: Pipeline Integration

The gap analyzer SHALL run as part of the standard pipeline, after
`scripts/standard_stats.py` (which produces `statistics.json`) and before
`scripts/analysis/generate_reports.py`.

Feature: Pipeline Order
Rule: statistics → gap analysis → reports.

#### Scenario: Pipeline runs the gap analyzer in the correct position
- **GIVEN** the full pipeline is executed
- **WHEN** the pipeline reaches the analysis stage
- **THEN** `standard_stats.py` runs first, then `research_gap_analyzer.py`, then `generate_reports.py`

#### Scenario: CI runs the gap analyzer on every push
- **GIVEN** a push to main that changes `papers.yaml`, `scripts/`, or `config/`
- **WHEN** CI runs
- **THEN** the gap analyzer runs and `docs/research/gap_analysis.md` is regenerated and committed

### Requirement: AGENTS.md Contract Updated

`AGENTS.md` SHALL list the gap analyzer in the common agent tasks and include
it in the full-pipeline command so coding agents know to run it after any
`papers.yaml` change.

Feature: Agent Contract
Rule: Agents learn the new tool from AGENTS.md.

#### Scenario: AGENTS.md documents the gap analyzer
- **GIVEN** the change is applied
- **WHEN** an agent reads AGENTS.md
- **THEN** AGENTS.md contains a "What are the research gaps?" task pointing to `tools/research_gap_analyzer.py`

#### Scenario: AGENTS.md full-pipeline command includes the gap analyzer
- **GIVEN** the change is applied
- **WHEN** an agent follows the AGENTS.md pipeline rule
- **THEN** the full-pipeline command includes `tools/research_gap_analyzer.py` after `scripts/standard_stats.py`
