# Paper Corpus

## Purpose

`papers.yaml` is the single source of truth for the research corpus. Every
other artifact (README, statistics, reports, visualizations, GitHub Pages site)
is generated from it. This spec defines the schema, validation rules, and
taxonomy binding that keep the corpus machine-checkable and agent-safe.

## Requirements

### Requirement: Paper Entry Schema

Every entry in `papers.yaml` SHALL conform to the schema below. The validator
MUST reject entries that miss required fields or carry unknown fields.

Feature: Paper Entry Schema
Rule: Each paper is a structured record with required and optional fields.

#### Scenario: Minimal valid paper entry
- **GIVEN** a paper entry with `title`, `date` (YYYY-MM), `url`, `category`, and `subcategory`
- **WHEN** `scripts/validate_papers.py` runs
- **THEN** the entry passes validation

#### Scenario: Missing required field is rejected
- **GIVEN** a paper entry missing `url`
- **WHEN** `scripts/validate_papers.py` runs
- **THEN** validation fails with a message naming the entry and the missing field

#### Scenario: Optional fields are accepted
- **GIVEN** a paper entry with `authors`, `venue`, `code_url`, `project_url`, `abstract`, and `tags`
- **WHEN** `scripts/validate_papers.py` runs
- **THEN** the optional fields are accepted and preserved

#### Scenario: Unknown field is rejected
- **GIVEN** a paper entry with a field not in the schema (e.g. `doi_legacy`)
- **WHEN** `scripts/validate_papers.py` runs
- **THEN** validation fails with a message naming the unknown field

### Requirement: URL Normalization

All paper URLs SHALL be normalized so that deduplication and CI checks are
deterministic.

Feature: URL Normalization
Rule: arXiv URLs use the canonical `https://arxiv.org/abs/XXXX.XXXXX` form.

#### Scenario: arXiv URL is normalized
- **GIVEN** a paper entry with url `https://arxiv.org/pdf/2601.00001`
- **WHEN** `scripts/validate_papers.py` runs
- **THEN** validation reports the non-canonical form and the `--fix` flag rewrites it to `https://arxiv.org/abs/2601.00001`

#### Scenario: Non-arXiv URLs are kept as-is
- **GIVEN** a paper entry with url `https://aclanthology.org/2026.emnlp-main.42`
- **WHEN** `scripts/validate_papers.py` runs
- **THEN** the url is accepted unchanged

### Requirement: Taxonomy Binding

Every paper's `category` and `subcategory` SHALL match an id defined in
`config/taxonomy.yaml`. Inventing ad-hoc taxonomy values is forbidden.

Feature: Taxonomy Binding
Rule: Category and subcategory ids MUST resolve against config/taxonomy.yaml.

#### Scenario: Valid category and subcategory
- **GIVEN** a paper with `category: compliance` and `subcategory: evaluation`
- **WHEN** `scripts/validate_papers.py` runs
- **THEN** the entry passes (both ids exist in taxonomy.yaml)

#### Scenario: Unknown category is rejected
- **GIVEN** a paper with `category: quantum-computing`
- **WHEN** `scripts/validate_papers.py` runs
- **THEN** validation fails and names the allowed categories

### Requirement: Deduplication

The corpus SHALL be free of duplicate papers. A duplicate is the same arXiv
id, the same normalized url, or a near-identical title under the same
(category, subcategory) cell.

Feature: Deduplication
Rule: No two entries may describe the same paper.

#### Scenario: Duplicate arXiv id is flagged
- **GIVEN** two entries with the same normalized arXiv url
- **WHEN** `scripts/validate_papers.py` runs
- **THEN** validation reports the duplicate pair

#### Scenario: Same title in the same cell is flagged
- **GIVEN** two entries with identical titles under `assessment/evaluation`
- **WHEN** `scripts/validate_papers.py` runs
- **THEN** validation reports the duplicate for human review

### Requirement: Generated Artifacts Are Read-Only

The generated artifacts (README.md, statistics.json, docs/papers.json,
docs/research/*.md, assets/visualizations/*) SHALL NOT be edited by hand.
They are produced by the pipeline and committed only after a successful run.

Feature: Generated Artifacts Read-Only
Rule: Editing a generated file by hand is a violation of the corpus contract.

#### Scenario: Pipeline regenerates README from papers.yaml
- **GIVEN** a papers.yaml change has been committed
- **WHEN** `scripts/generate_readme.py` runs
- **THEN** README.md is overwritten to reflect the current papers.yaml
- **AND** `scripts/generate_readme.py --check` exits 0 when README is up to date

#### Scenario: Stale generated file fails CI
- **GIVEN** README.md was edited by hand and does not match papers.yaml
- **WHEN** CI runs `scripts/generate_readme.py --check`
- **THEN** the check fails and CI blocks the PR
