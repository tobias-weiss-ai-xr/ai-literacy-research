# research-concept-graph Specification

## Purpose
Defines the portable knowledge-enrichment workflow that extracts concepts and
ideas from a research corpus and relates them into a co-occurrence knowledge
graph. The same two tools run unchanged in any `*research` repo.

## Requirements

### Requirement: Concept Extraction Tool

The corpus SHALL provide `tools/extract_concepts.py` that extracts a ranked
concept list from `papers.yaml` (plus optional `config/taxonomy.yaml` and
`config/concepts.yaml`), writing `concepts.json`.

Feature: Concept Extraction
Rule: Concepts come from taxonomy categories (structural), curated seeds (text), and emergent bigrams (text).

#### Scenario: Extract runs on a minimal repo
- **GIVEN** a repo with only `papers.yaml` (no taxonomy, no concepts.yaml)
- **WHEN** `tools/extract_concepts.py` runs
- **THEN** it emits `concepts.json` with emergent bigrams and zero errors

#### Scenario: Taxonomy categories are associated structurally
- **GIVEN** a taxonomy category `ai-literacy-construct` with 848 papers
- **WHEN** `extract_concepts.py` runs
- **THEN** the concept "Ai Literacy Construct" has `df` ≈ 848 even if the label rarely appears verbatim in abstracts

#### Scenario: Curated seeds are included from config
- **GIVEN** `config/concepts.yaml` lists `evaluation`
- **WHEN** `extract_concepts.py` runs
- **THEN** `evaluation` appears as a `curated` concept with its text-match df

### Requirement: Concept Relationship Graph

The corpus SHALL provide `tools/relate_concepts.py` that builds a
co-occurrence knowledge graph from `concepts.json` + `papers.yaml`, writing
`concept_graph.json` and (with `--write-doc`) `docs/research/concept_map.md`.

Feature: Concept Relationships
Rule: Two concepts relate when they co-occur in the same paper; edge weight = shared-paper count.

#### Scenario: Co-occurring concepts form an edge
- **GIVEN** concepts `training` and `evaluation` share 177 papers
- **WHEN** `relate_concepts.py` runs
- **THEN** an edge `(training, evaluation, weight=177)` exists in `concept_graph.json`

#### Scenario: Weak co-occurrence is pruned
- **GIVEN** `--min-co 2` and two concepts sharing only 1 paper
- **WHEN** `relate_concepts.py` runs
- **THEN** no edge is emitted for that pair

#### Scenario: Human-readable map is produced
- **GIVEN** `--write-doc`
- **WHEN** `relate_concepts.py` runs
- **THEN** `docs/research/concept_map.md` lists top concepts and their related concepts

### Requirement: Artifacts Are Reproducible

`concepts.json`, `concept_graph.json`, and `docs/research/concept_map.md`
SHALL be generated artifacts that MUST NOT be edited by hand.

Feature: Reproducibility
Rule: Delete the artifacts, run the pipeline, get them back identically.

#### Scenario: Deterministic output
- **GIVEN** unchanged inputs
- **WHEN** extract + relate run twice
- **THEN** all three artifacts are byte-identical (verified by sha256)

#### Scenario: Hand-edited graph is detected by CI
- **GIVEN** `concept_map.md` edited by hand and no longer matching regeneration
- **WHEN** CI runs the regeneration check
- **THEN** the check fails and CI blocks the push/PR

### Requirement: Pipeline Integration

The concept-graph steps SHALL run as part of the standard pipeline and in CI
whenever `papers.yaml`, `config/`, or the tools change.

Feature: Pipeline Order
Rule: statistics → gap analysis → concept graph → visualize.

#### Scenario: CI regenerates and verifies the graph
- **GIVEN** a push changing `papers.yaml` or `tools/extract_concepts.py`
- **WHEN** CI runs
- **THEN** extract + relate run and `git diff --exit-code` on the three artifacts passes (or CI fails)

#### Scenario: Weekly refresh regenerates the graph
- **GIVEN** the scheduled refresh job runs
- **WHEN** it regenerates statistics, gaps, and concepts
- **THEN** `concepts.json`, `concept_graph.json`, and `concept_map.md` are updated and committed

### Requirement: Agent Contract Updated

`README.md` and `AGENTS.md` SHALL document the two tools so agents run them
after any `papers.yaml` change.

Feature: Agent Contract
Rule: Agents learn the concept-graph workflow from README/AGENTS.

#### Scenario: README documents the concept graph
- **GIVEN** the change is applied
- **WHEN** a reader opens README.md
- **THEN** the Tools and Pipeline sections mention `extract_concepts.py` and `relate_concepts.py`

#### Scenario: AGENTS.md lists the task
- **GIVEN** the change is applied
- **WHEN** an agent reads AGENTS.md
- **THEN** a "What concepts/ideas relate in the corpus?" task points to the two tools
