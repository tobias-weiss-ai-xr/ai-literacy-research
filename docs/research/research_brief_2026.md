# The AI-Literacy Evidence Gap: Where 11,640 Papers Go Silent

*Research brief · 2026-08-23 · companion to `gap_analysis.md`, Guides 1–2, and the
Assessment Instrument Spec. Reproducible from this corpus (`tools/research_gap_analyzer.py`).*

## The headline

The AI-literacy literature is no longer thin — it is **lopsided**. Our living
corpus now holds **11,640 papers** across 20 categories, fully saturated (every
taxonomy cell has at least one study). But saturation is not the same as
coverage. When you score each cell by how *under-supplied* it is relative to its
category — and weight that by how *fast it is growing* — a clear white space
emerges that almost no one is writing about, and that organizations most need
answered.

## How we found it

We ranked all 160 taxonomy cells with an *opportunity score*:

```
score = 0.6 × (1 − count/category_average)        # thinness
      + 0.4 × normalized 12-month growth         # momentum
      + 0.15  if count ≤ 5                        # floor bonus
```

Thin alone is not interesting — a dead topic should stay dead. The cells that
*win* are **thin-and-surging**: barely studied, but accelerating. Those are the
research and product gaps worth filling first.

## The finding

The top of the ranking is dominated by **evaluation** and **implementation**
cells:

| Rank | Cell | Papers | 12-mo growth |
|------|------|--------|--------------|
| 1 | `compliance/evaluation` | 5 | +300% |
| 2 | `org-implementation/evaluation` | 5 | +100% |
| 3 | `workforce-upskilling/evaluation` | 7 | +33% |
| 4 | `ai-literacy-construct/evaluation` | 12 | +1000% |
| 5 | `teacher-ai-literacy/evaluation` | 11 | +75% |

In plain terms: we have plenty of papers *describing* AI literacy, but almost
none that **prove a program worked** — especially for the EU AI Act's Article 4
literacy obligation. That is the gap the field has left open, and it is exactly
where organizations are now legally and operationally exposed.

## Why it matters for organizations

- **Article 4 makes "did our people get literate?" a compliance question**, not a
  nice-to-have. The corpus shows readiness-evaluation work is just starting
  (e.g. *Digital transformation readiness: evaluating Dutch municipalities'
  compliance with the AI Act*) — thin, surging, and wide open.
- **Implementation evidence concentrates in the wrong places.** Most
  implementation studies are classroom case reports; the organizational,
  role-specific, *measured* evidence (maturity models, task-based evaluation)
  is scarce. The *AIconomics Maturity Model* and similar diagnostic frameworks
  are the exceptions that prove the need.
- **The instrument layer finally exists.** Validated scales (MAIL-CS, AICOS,
  SAIL4ALL, and the new multi-cohort **SFAILQ**) mean you no longer have to build
  your own — you have to *choose and use* one properly, and pair it with
  task-based measurement because self-report diverges from demonstrated skill.

## How we close it

This is not a research curiosity — it is a product and service blueprint:

1. **Guide 1 (Implementation)** turns the implementation white space into a
   10-step playbook with a compliance track.
2. **Guide 2 (Evaluation)** catalogues the instruments and gives a task-based
   quasi-experiment design — the template for proving a program worked.
3. **The Assessment Instrument Spec** seeds that design in corpus-validated
   measures (AICOS / MAIL-CS / SFAILQ) and an occupation-aligned task matrix,
   doubling as the Art. 4 evidence record.

The organizations that move first on *measured* AI-literacy — not just trained,
but assessed against real tasks — will own the defensible compliance story the
rest of the market is silently missing.

---

*Generated as a Phase 6 transfer piece from the ai-literacy-research corpus.
Numbers are reproducible via `tools/research_gap_analyzer.py` and
`scripts/analysis/generate_analysis.py`.*
