# OpenSpec — AI Literacy Research Corpus

> Showcase: Spec-driven development for a research corpus.
> This `openspec/` directory is the **source of truth for behavior**; the
> pipeline code implements these specs.

This directory demonstrates how **OpenSpec** turns research-workflow changes
into verifiable, agent-friendly specifications — the same approach used in
the [skeleton-research](https://github.com/tobias-weiss-ai-xr/skeleton-research)
workshop repo, applied here to a real 9,600-paper corpus.

## Layout

```
openspec/
├── config.yaml            # schema, project context, agent rules
├── specs/                 # behavioral specs (the "what", not the "how")
│   ├── paper-corpus/          # papers.yaml schema, validation, dedup, read-only artifacts
│   ├── discovery-pipeline/    # multi-source discovery, dedup on ingest, CI integration
│   └── analysis-reporting/    # statistics, reports, tools, visualization, reproducibility
└── changes/               # delta specs — one folder per proposed change
    └── add-research-gap-analysis/
        ├── .openspec.yaml     # schema + created date
        ├── proposal.md        # why & what changes
        ├── design.md          # context, goals, gap-score formula, risks
        ├── specs/             # delta spec (ADDED requirements)
        │   └── research-gap-analysis/spec.md
        └── tasks.md           # implementation checklist
```

## How it works

1. **Specs** (`specs/`) describe the *existing* behavior as contracts
   (SHALL/MUST/SHOULD + Given/When/Then). They are the source of truth.
2. **A change** (`changes/<name>/`) proposes a delta: `proposal.md` (why),
   `design.md` (how), `specs/` (ADDED/MODIFIED/REMOVED requirements), and
   `tasks.md` (implementation checklist).
3. An **agent** (OpenCode + SAIA) reads the change, implements the tasks,
   and verifies against the delta spec — no clarification rounds needed
   because the spec is the contract.
4. On completion the change is **archived** and its ADDED requirements are
   **synced** into the main `specs/`, so the spec stays the living source of truth.

## The showcase change: `add-research-gap-analysis`

The corpus README already surfaces "Research Gaps (Thinnest Cells)" — but only
as a static count. This change adds `tools/research_gap_analyzer.py`, which
**joins thinness with momentum** to rank the most promising white space:

```
gap_score = 0.6 × thinness + 0.4 × momentum + floor_bonus(count ≤ 5)
```

It is a clean, self-contained example of the Spec → Change → Implement →
Verify loop:

| Artifact | Purpose |
|----------|---------|
| `proposal.md` | Why: thinness alone is a weak signal; momentum amplifies opportunity |
| `design.md` | Gap-score formula, output format, pipeline position, risks |
| `specs/research-gap-analysis/spec.md` | 4 requirements, 13 Given/When/Then scenarios |
| `tasks.md` | 7 task groups, ~25 checkboxes, verification steps |

## Why this matters for the workshop

- **One config, one re-run** — the agent changes `config/taxonomy.yaml` or
  adds a tool, runs the pipeline, and gets an objective pass/fail signal.
- **Specs are agent-readable contracts** — no re-explaining the pipeline each
  session; the delta spec is the prompt.
- **Reproducibility is testable** — "delete generated files, run the
  pipeline, get them back byte-identical" is a verifiable scenario.
- **CI closes the loop** — validation, regeneration, and gap analysis run on
  every push; a weekly job discovers new papers and opens a PR.

## Related

- Repo: [ai-literacy-research](https://github.com/tobias-weiss-ai-xr/ai-literacy-research)
- Skeleton: [skeleton-research](https://github.com/tobias-weiss-ai-xr/skeleton-research)
- OpenSpec: [github.com/FissionAI/OpenSpec](https://github.com/FissionAI/OpenSpec)
