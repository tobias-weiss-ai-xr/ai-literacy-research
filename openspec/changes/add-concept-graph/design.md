# Design: Concept & Idea Knowledge Graph

## Principle — minimal/stoic Unix
Two single-purpose tools that do one thing and compose via files/JSON:

```
papers.yaml (+ config/taxonomy.yaml, config/concepts.yaml)
        │  tools/extract_concepts.py
        ▼
   concepts.json   ──(piped/referenced)──►  tools/relate_concepts.py
        │                                          │
        │                                    concept_graph.json
        ▼                                    docs/research/concept_map.md
```

Each tool is deterministic (byte-identical re-runs, no timestamps), depends
only on `pyyaml` + stdlib, and runs on **any** repo with `papers.yaml`.

## extract_concepts.py
- Loads papers; builds concept dict from three sources:
  - taxonomy **categories** → `match: {type: field, field: category, value: id}`
    (structural; every paper in the category counts — robust to labels that
    never appear verbatim in text).
  - curated terms (`config/concepts.yaml`) → `match: {type: text, forms: [...]}`.
  - emergent noun **bigrams** (min document frequency) → text match.
- For text concepts, a single pass computes df + top cells (with a token
  prefilter so regex runs only when all concept tokens are present).
- Emits `{"count", "concepts": [{term, kind, df, top_cells, match, ...}]}`.
- Taxonomy **subcategories** are intentionally excluded (generic method
  buckets: `development`, `systems`, `method`, …); they surface via the
  `top_cells` field instead.

## relate_concepts.py
- Reads `concepts.json` + `papers.yaml`. For each concept it rebuilds its
  paper-set from the `match` descriptor:
  - `field` → set of papers whose `category` equals the value.
  - `text` → papers whose title+abstract contain any `form` (word-boundary).
- Inverts paper→concept indices, then counts co-occurring pairs
  (`itertools.combinations`). Edges kept when shared papers ≥ `--min-co`.
- Writes `concept_graph.json` (`{nodes, edges, stats}`) to stdout and, with
  `--write-doc`, a readable `docs/research/concept_map.md` (top concepts +
  their related concepts).

## Why a `match` descriptor (not just text)
Taxonomy category labels (e.g. "AI Literacy Construct") rarely appear verbatim
in abstracts, so pure text-matching yields df=0 dead nodes. The structural
`field` match gives correct, stable df/cells and lets high-level topics
co-occur with the concepts inside their papers.

## Determinism (verified)
Two runs of extract + relate produced byte-identical `concepts.json`,
`concept_graph.json`, and `concept_map.md` (sha256 matched).

## Files
- `tools/extract_concepts.py` (new)
- `tools/relate_concepts.py` (new)
- `config/concepts.yaml` (new, repo-specific curated seeds)
- `concepts.json`, `concept_graph.json`, `docs/research/concept_map.md` (generated)
- `.github/workflows/validate.yml`, `README.md`, `AGENTS.md` (wiring)
