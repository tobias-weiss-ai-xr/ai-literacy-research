# Tasks: add-concept-graph

## 1. Tools
- [x] 1.1 Create `tools/extract_concepts.py` (taxonomy categories structural + curated + emergent bigrams, deterministic)
- [x] 1.2 Create `tools/relate_concepts.py` (co-occurrence graph, `concept_graph.json` + `--write-doc` map)
- [x] 1.3 Verify byte-identical determinism across re-runs

## 2. Repo configuration
- [x] 2.1 Add `config/concepts.yaml` with ai-literacy curated seeds

## 3. Integration & docs
- [x] 3.1 Wire `extract_concepts.py` + `relate_concepts.py` into `validate.yml` (trigger paths, up-to-date check, weekly refresh)
- [x] 3.2 Update `README.md` (Tools + Pipeline) and `AGENTS.md` (Full Pipeline + Common Tasks)

## 4. OpenSpec
- [x] 4.1 Create change `add-concept-graph` (proposal, design, spec, tasks)

## 5. Portability (post-merge)
- [ ] 5.1 Copy `tools/extract_concepts.py`, `tools/relate_concepts.py` into `skeleton-research` (reference template)
- [ ] 5.2 Add repo-specific `config/concepts.yaml` to each `*research` repo as needed
- [ ] 5.3 Mirror `validate.yml` wiring in `skeleton-research` so all forks inherit it
