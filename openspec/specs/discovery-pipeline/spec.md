# Discovery Pipeline

## Purpose

The discovery pipeline finds new papers across multiple scholarly sources
(arXiv, OpenAlex, dblp, Crossref, Europe PMC) and, optionally, code repos
(GitHub, GitLab, Codeberg). It is driven entirely by `config/taxonomy.yaml`
queries, deduplicates against the existing corpus, and integrates with CI so
the corpus refreshes on a weekly schedule without manual babysitting.

## Requirements

### Requirement: Config-Driven Discovery Queries

All discovery runs SHALL read their queries from `config/taxonomy.yaml`
(`arxiv_queries`, `other_sources_queries`, `openalex_queries`, `github_queries`,
`gitlab_queries`, `codeberg_queries`). No source-specific query is hardcoded
in a script.

Feature: Config-Driven Queries
Rule: Adding a source means adding a query block to taxonomy.yaml, not editing code.

#### Scenario: arXiv discovery reads taxonomy queries
- **GIVEN** `config/taxonomy.yaml` contains `arxiv_queries`
- **WHEN** `scripts/fetch/fetch_new_papers.py` runs
- **THEN** every query in `arxiv_queries` is executed against the arXiv API
- **AND** results are deduplicated against existing papers.yaml entries

#### Scenario: Empty query list exits gracefully
- **GIVEN** `config/taxonomy.yaml` has no `github_queries`
- **WHEN** `scripts/fetch/fetch_github_repos.py` runs
- **THEN** the script prints setup instructions and exits 0

### Requirement: Multi-Source Discovery

The corpus SHALL support discovery from at least arXiv, OpenAlex, dblp,
Crossref, and Europe PMC. Each source fetcher MUST normalize results to the
paper schema and tag the source for provenance tracking.

Feature: Multi-Source Discovery
Rule: One normalized schema, many sources.

#### Scenario: OpenAlex bulk fetch normalizes records
- **GIVEN** `config/taxonomy.yaml` contains `openalex_queries` with categories
- **WHEN** `scripts/fetch/fetch_openalex_bulk.py` runs
- **THEN** each OpenAlex record is normalized to a paper entry with `category`, `subcategory`, normalized url, and `abstract`
- **AND** `topic.openalex_mailto` from taxonomy.yaml is used for the polite-pool

#### Scenario: Other-sources fetcher dispatches by source
- **GIVEN** `config/taxonomy.yaml` contains `other_sources_queries` with `source: dblp` and `source: crossref`
- **WHEN** `scripts/fetch/fetch_other_sources.py` runs
- **THEN** each query is dispatched to the matching fetcher and results are normalized to the paper schema

### Requirement: Deduplication on Ingest

Newly discovered papers SHALL be deduplicated against the existing corpus
before being appended to `papers.yaml`. Dedup keys are normalized url,
arXiv id, and near-identical title under the same cell.

Feature: Ingest Deduplication
Rule: A discovery run never appends a paper that is already in the corpus.

#### Scenario: Duplicate discovery is skipped
- **GIVEN** a discovered paper whose normalized url already exists in papers.yaml
- **WHEN** `scripts/fetch/fetch_new_papers.py --local` runs
- **THEN** the paper is skipped and a skip message is logged

#### Scenario: New paper is appended with taxonomy hint
- **GIVEN** a discovered paper with a `category` and `subcategory_hint` in its query block
- **WHEN** the paper is not a duplicate
- **THEN** it is appended to papers.yaml with the hinted category and subcategory

### Requirement: CI Integration

The repository SHALL validate and regenerate all artifacts on every push and
pull request. A scheduled job SHALL run discovery weekly and open a pull
request with newly found papers.

Feature: CI Integration
Rule: The corpus stays healthy without manual intervention.

#### Scenario: Push triggers validation
- **GIVEN** a push to `main` that changes `papers.yaml`, `scripts/`, `config/`, or `requirements.txt`
- **WHEN** CI runs
- **THEN** `scripts/validate_papers.py` and `scripts/generate_readme.py --check` both run and must pass

#### Scenario: Weekly discovery opens a PR
- **GIVEN** the weekly schedule triggers
- **WHEN** the discover job runs `scripts/fetch/fetch_new_papers.py --months 1 --create-pr`
- **THEN** a pull request is opened with any newly discovered papers
- **AND** the PR body lists the added papers with their categories

#### Scenario: GitHub Pages site is published
- **GIVEN** validation passed on `main`
- **WHEN** the pages job runs
- **THEN** `docs/index.html` (the paper browser) is deployed to GitHub Pages from the regenerated `docs/papers.json`
