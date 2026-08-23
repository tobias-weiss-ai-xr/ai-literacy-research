# Proposal: Concept & Idea Knowledge Graph (portable enrichment workflow)

## Why
The research program extracts evidence into taxonomy cells and gap rankings,
but the corpus still lacks a way to surface **concepts and ideas and how they
relate**. A knowledge graph of co-occurring concepts lets us navigate the
literature by idea ("what connects *training* to *evaluation* and *AI Act
compliance*?"), supports synthesis, and enriches the repo's knowledge between
publishing cycles.

This must be a **general workflow**, not an ai-literacy-specific script: the
same two tools should drop into `skeleton-research` and every other
`*research` repo. All research repos share the skeleton (`papers.yaml` is
universal; `config/taxonomy.yaml` and `tools/` are optional in some).

## What changes
- Two small, composable, deterministic tools (minimal/stoic Unix style):
  - `tools/extract_concepts.py` — reads `papers.yaml` (+ optional
    `config/taxonomy.yaml`, `config/concepts.yaml`) and emits a ranked concept
    list (`concepts.json`).
  - `tools/relate_concepts.py` — reads `concepts.json` + `papers.yaml` and
    builds a co-occurrence knowledge graph, writing `concept_graph.json` and
    (with `--write-doc`) `docs/research/concept_map.md`.
- `config/concepts.yaml` — repo-specific curated concept seeds (portable per
  repo; empty/optional elsewhere).
- CI + README/AGENTS wiring so the graph regenerates and stays current.

## Concept sources
1. **Taxonomy categories** — high-level backbone concepts, associated
   *structurally* (paper `category` field), so multiword labels that never
   appear verbatim in abstracts still count.
2. **Curated seeds** — `config/concepts.yaml` (e.g. `evaluation`,
   `ai act`, `technostress`), associated by text.
3. **Emergent bigrams** — frequent noun bigrams mined from title+abstract,
   associated by text.

Edges = co-occurrence (two concepts appearing in the same paper), weighted by
shared-paper count.

## Out of scope
- Claim/relationship *typing* (causal, contrastive) — v1 is co-occurrence only.
- Full-text idea extraction (corpus abstracts are ~200-char snippets).
- Auto-publishing the graph (it enriches the repo, not external sites).

## Portability
Reference implementation lands in `ai-literacy-research`; the same files copy
into `skeleton-research` (and other repos) unchanged. Only `papers.yaml` is
required; taxonomy/concepts seeds are optional and degrade gracefully.
