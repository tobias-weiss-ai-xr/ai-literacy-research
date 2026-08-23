# Analysis & Reporting

## Purpose

The analysis layer turns `papers.yaml` into insight: statistics, trend/burst
detection, topic planning, landscape reports, and the literature review
synthesis. All outputs are generated and reproducible from the corpus alone.
This spec defines the analyses the pipeline MUST produce and their
reproducibility contract.

## Requirements

### Requirement: Standard Statistics

The pipeline SHALL produce `statistics.json` containing category counts,
subcategory counts, yearly distribution, momentum (12-month output density
and year-over-year growth), keyword bursts, top venues, and top authors.

Feature: Standard Statistics
Rule: statistics.json is a deterministic function of papers.yaml + taxonomy.yaml.

#### Scenario: Statistics reflect the current corpus
- **GIVEN** a papers.yaml with N entries across the configured taxonomy
- **WHEN** `scripts/standard_stats.py` runs
- **THEN** `statistics.json` is written with category counts, subcategory counts, yearly counts, momentum, bursts, venues, and authors
- **AND** re-running with unchanged inputs produces a byte-identical file

#### Scenario: Config-driven trend keywords are used
- **GIVEN** `config/taxonomy.yaml` defines a `trend_keywords` list
- **WHEN** `scripts/standard_stats.py` runs
- **THEN** burst detection uses the configured keywords instead of the built-in default list

### Requirement: Literature Review Report

The pipeline SHALL generate `docs/research/literature_review.md` synthesizing
the corpus by category, with top papers per category and a trends section.

Feature: Literature Review Report
Rule: The report is generated, never hand-written.

#### Scenario: Report groups by taxonomy category
- **GIVEN** a corpus with papers across multiple categories
- **WHEN** `scripts/analysis/generate_reports.py` runs
- **THEN** `docs/research/literature_review.md` is written with one section per category
- **AND** each section lists representative papers sorted by date

#### Scenario: Trends report is generated
- **GIVEN** statistics.json exists
- **WHEN** `scripts/analysis/generate_reports.py` runs
- **THEN** `docs/research/trends.md` is written with a 12-month trend and burst report

### Requirement: Topic Planning & Landscape Tools

The tools (`topic_planner.py`, `trend_scanner.py`, `landscape_analyzer.py`,
`brief_generator.py`) SHALL read the corpus and taxonomy from config and
produce ranked, reproducible outputs.

Feature: Research Tools
Rule: Tools are config-driven and reproducible.

#### Scenario: Topic planner ranks evidence areas
- **GIVEN** the corpus and taxonomy
- **WHEN** `tools/topic_planner.py --top 10` runs
- **THEN** the top 10 categories by paper count and recent activity are printed
- **AND** `docs/topics/ARTICLE_TOPICS.md` is written

#### Scenario: Landscape analyzer writes the full landscape
- **GIVEN** the corpus and taxonomy
- **WHEN** `tools/landscape_analyzer.py --write-doc` runs
- **THEN** the full landscape report is written to `docs/research/landscape_report.md`

#### Scenario: Brief generator produces a topic brief
- **GIVEN** a topic query and a paper budget
- **WHEN** `tools/brief_generator.py "EU AI Act literacy obligations" --papers 5` runs
- **THEN** a brief with the top matching papers and their abstracts is produced

### Requirement: Research Gap Analysis

A `research_gap_analyzer.py` tool SHALL identify under-saturated taxonomy
cells and rank them by an opportunity score that combines thinness (count vs
category average) with 12-month momentum (surging white space wins), writing
the ranked result to `docs/research/gap_analysis.md`.

Feature: Research Gap Analysis
Rule: The tool reads statistics.json + papers.yaml + taxonomy.yaml and produces
a ranked, reproducible gap report. It runs after statistics generation and
before the reports step in the pipeline.

#### Scenario: Analyzer runs after statistics are generated
- **GIVEN** `statistics.json` exists
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

### Requirement: Visualization

The pipeline SHALL produce category-distribution and trend visualizations in
`assets/visualizations/` so the README and reports can embed them.

Feature: Visualization Generation
Rule: Charts are generated from statistics.json.

#### Scenario: Category distribution chart is generated
- **GIVEN** statistics.json exists
- **WHEN** `scripts/visualize_statistics.py` runs
- **THEN** `assets/visualizations/category_distribution.png` is written
- **AND** the image is referenced from README.md

### Requirement: Reproducibility

Every generated artifact SHALL be reproducible from `papers.yaml` and
`config/taxonomy.yaml` alone. No generated file depends on hidden state.

Feature: Reproducibility
Rule: Delete all generated files, run the pipeline, get them back byte-identical.

#### Scenario: Full pipeline regenerates all artifacts
- **GIVEN** only `papers.yaml`, `config/taxonomy.yaml`, and the scripts exist
- **WHEN** the full pipeline runs (validate → readme → stats → reports → visualize)
- **THEN** README.md, statistics.json, docs/papers.json, docs/research/*.md, and assets/visualizations/*.png are all regenerated

#### Scenario: Deterministic output
- **GIVEN** unchanged inputs
- **WHEN** the pipeline runs twice
- **THEN** the generated artifacts are byte-identical between runs (modulo timestamps that the generator omits)
