# AI-Literacy Assessment Instrument Spec (Phase 5)

**Status:** draft v1.1 (refreshed 2026-08-23) · **Builds on:** Guide 2 §2.1–2.2
(instruments, warnings) and Guide 1 §2.1 (construct model) · **Purpose:**
specification for a task-oriented, occupation-aligned AI-literacy assessment —
the missing *objective* measurement layer for Art. 4 compliance and program
evaluation. Corpus refreshed to **11,640 papers** (see `gap_analysis.md` for
cell-level prioritization).

---

## 1. Design requirements (from the evidence)

| Requirement | Evidence base |
|---|---|
| **Task-based, not self-report-only** | SR-vs-OB divergence (C): self-reported and objective literacy correlate weakly — baseline/exit must use the same objective type |
| **Occupation-aligned tasks** | Task-orientation finding (E→D): knowledge definitions miss what workers need (interpreting outputs, tool selection, ethical judgment); FALCON-AI role-embedding + radiology experiment template |
| **Stage-aware levels** | Convergent frameworks (DALF 3-stage, AI Fluency 6-level, five-stage continuum, RAIL-Ed) → 4 usable levels |
| **Explicit construct model** | A-factor (one dominant factor, 44% variance) vs MAIL-CS (4 factors) — spec must state its model |
| **Art. 4-ready evidence chain** | Compliance requires role × task × measure mapping (Guide 2 §4) |

## 2. Construct model

**Three axes** (Guide 1 §2.1 synthesis):

- **Competence depth** — knowledge → application → evaluation → creation
- **Autonomy** — dependence → independence (with appropriate reliance judgment)
- **Disposition** — attitudes, self-efficacy, mindset (AI Mindset triadic)

**Global stage:** every assessment result maps onto a 4-level continuum that
condenses DALF + AI Fluency + the avoidance↔reliance spectrum:

| Level | Label | Observable behavior (task evidence) |
|-------|-------|-------------------------------------|
| 1 | **Awareness** | Recognizes AI capabilities/limits; can describe what the tool does; needs prompting to use it |
| 2 | **Application** | Uses a given tool on a defined task; checks outputs for obvious errors; follows provided guardrails |
| 3 | **Evaluation** | Selects tools by task fit; interprets and criticizes outputs; handles edge cases and failure modes; documents process |
| 4 | **Integration** | Designs own workflows with AI; evaluates broader consequences (ethics, risk, compliance); teaches others; calibrates reliance (neither avoidant nor uncritical) |

## 3. Instrument architecture

```
┌──────────────────────────────────────────────────────────┐
│ CORE: Task-Based Performance Assessment (objective,       │
│ occupation-aligned) — scored by rubric, not self-report   │
│  • 4-6 tasks drawn from the role's task matrix (§4)       │
│  • each task targets 1-2 levels; rubrics anchor scores    │
│  • session: 45-60 min, proctored or platform-run          │
├──────────────────────────────────────────────────────────┤
│ COMPANION (optional): Self-report battery                 │
│  • disposition items (self-efficacy, attitudes, mindset)  │
│  • GenAI reliance patterns (GenAI-RTS-inspired)           │
│  • used to compute the SR-vs-OB gap — never as the score  │
└──────────────────────────────────────────────────────────┘
```

## 4. Occupation-aligned task matrices

Task matrices are the role-facing interface. Each matrix row is a
`role-task → (evidence, levels, weight)`. Examples:

| Role | Task (workplace-real) | Target level | Evidence captured |
|------|----------------------|--------------|-------------------|
| **Knowledge worker (office)** | Draft a customer reply with an LLM given a policy guardrail; identify the hallucinated claim | 2–3 | Output quality, guardrail adherence, error detection |
| **Sales** | Use CRM copilot to extract deal risks from a call transcript; justify tool choice | 2–3 | Tool selection, judgment, justification |
| **Dev / analyst** | Interpret a model output for a business decision; state assumptions & failure modes | 3–4 | Interpretation, uncertainty handling |
| **Manager** | Design a 1-week AI workflow for a team incl. an ethical/regulatory check | 3–4 | Workflow design, consequence analysis |
| **Support / SME staff** | Handle a customer case with an AI assistant; escalate appropriately | 1–2 | Appropriate reliance, escalation |
| **Compliance-adjacent role** | Draft an AI-use record per Art. 4 expectations; identify missing documentation | 3 | Process conformity, documentation |

Each matrix is generated per customer organization from job analysis (task
inventory × AI-relevance rating); the spec ships default matrices for the 6
most common ALaaS target roles.

## 5. Task templates & scoring rubric

**Task template (one page per task):**
1. *Stimulus* — realistic input (document, transcript, dataset, prompt)
2. *Prompt* — what the worker must produce (deliverable + process notes)
3. *Constraints* — guardrails, tools allowed, time
4. *Evidence points* — 3-5 rubric items with anchors

**Rubric anchor style (5-point per item):** *0 — fails the task / unsafe
output; 1 — completes with major errors or uncaught hallucination; 2 — correct
with minor errors; 3 — correct + verifies output + notes limitations; 4 —
correct + optimizes process + evaluates consequences.* Level = rubric score
mapped to the §2 stage table.

**Item bank example (Level 2, error detection):**
- Stimulus: AI-drafted contract summary containing 2 planted errors (a wrong
  date, a fabricated clause reference)
- Evidence: does the worker catch both errors? Do they re-check the source?

## 6. Administration & scoring

- **Mode:** proctored session or platform-run with session logging
- **Scoring:** rubric scored by trained rater; inter-rater reliability check
  (κ ≥ .7) on 10% sample; or rule-based scoring for platform tasks
- **Reporting:** level per axis (competence / autonomy / disposition) + global
  stage + SR-vs-OB gap + task-level strengths
- **Baseline/exit protocol:** identical instrument at both points (the SR-vs-OB
  warning); retest interval ≥ 6 weeks to avoid practice effects

## 7. Psychometric validation protocol (to run)

| Step | Method | Success criterion |
|------|--------|-------------------|
| Content validity | Expert panel on task matrices (role SMEs + AI experts) | CVI ≥ .80 per item |
| Pilot | N ≥ 30 per role; item analysis | item-total r ≥ .3; no ceiling/floor > 60% |
| Construct validity | EFA/CFA on rubric scores across roles | model fit: CFI ≥ .90, RMSEA ≤ .08 |
| Reliability | α / ω per level+axis | ≥ .80 |
| Criterion validity | task scores vs job performance ratings / AICOS | r ≥ .3 |
| SR-vs-OB calibration | companion battery vs task scores | report gap; do not merge into one score |

## 8. Art. 4 evidence chain (compliance use)

For each role: **role → task matrix → assessment result → stored evidence.**
The assessment output doubles as Art. 4-compliant documentation:

```
Role definition (job analysis)
  → task matrix (which AI tasks the role performs)
    → assessed level per task (task-based, objective)
      → evidence record (session log, rubric scores, date, rater)
        → aggregate readiness report (levels by role, gap analysis)
```

SME-minimum variant (€99 tier): 4-task subset + platform auto-scoring + the
same evidence record format, so customers can upgrade to the full battery
without re-doing baseline.

## 9. Versioning & living updates

- Spec versioned in-repo (`v1`); instrument items versioned separately
  (`AILA-T v1.0`)
- Item-bank refresh quarterly (new tool classes, prompt-injection/agentic
  scenarios as they enter the corpus — see `fetch_news.py` alerts as leading
  indicators)
- Validation data published to the corpus as tier (B/C) evidence once N ≥ 150

---

## 10. Instrument reference — corpus-grounded selection (2026-08-23)

The §3 architecture is deliberately *instrument-agnostic* (it specifies the
measurement **layer**, not a fixed questionnaire). But the refreshed corpus now
contains enough validated instruments to seed both layers concretely. Use this
table to pick what to license/adapt rather than building from zero.

| Instrument | Construct coverage (axes) | Level range | Population / role fit | Spec layer to seed |
|-----------|--------------------------|-------------|----------------------|--------------------|
| **AICOS** (objective competency, GenAI dimension) | Competence depth, Autonomy | 2–4 | Adults, general | **CORE** objective proxy (preferred) |
| **MAIL-CS** (32 items, 4 factors; α=.91, ω=.92) | Competence depth, Disposition | 2–4 | University students | CORE / criterion-validity anchor |
| **SFAILQ** (six facets; adolescents→midlife) | Competence depth, Disposition | 1–4 | Multi-cohort adults | CORE for adult, cross-age programs |
| **SAIL4ALL** (56 items, 4 themes) | Competence depth | 1–3 | Adults, any setting | CORE screening |
| **FALCON-AI** (role-embedded, CTRL) | Autonomy, Occupation-alignment | 2–3 | Faculty / professional | CORE task-design template |
| **EUIA** (6 GenAI-in-assessment levels) | Competence depth, Autonomy | 1–4 | Assessment contexts | CORE level anchors |
| **AILS (KR)** / **AILS (Arabic)** | Competence depth, Disposition | 1–3 | Students / cross-cultural | COMPANION cross-cultural |
| **SNAIL** (non-experts, gains) | Competence depth | 1–2 | Course participants | COMPANION pre/post gains |
| **GenAI-RTS** (20 items, 4 reliance types) | Disposition (reliance) | — | Writing contexts | **COMPANION** reliance pattern |
| **G-Factor / A-Factor battery** (18 items, 4 dims) | Construct model (A-factor 44%) | — | Adults (N=517) | COMPANION construct evidence |

**Selection rule for ALaaS:** CORE = an *objective* instrument (AICOS or
MAIL-CS/SFAILQ where population-matched) **plus** the §4 task matrix; COMPANION
= GenAI-RTS-style reliance battery to compute the SR-vs-OB gap (§2 warning).
Never let a self-report instrument become the score.

**Newest corpus entry (2026):** SFAILQ (Six-Facet AI Literacy Questionnaire,
adolescents→midlife adults — <https://doi.org/10.3390/bs16071110>) extends the
multi-cohort objective option and should be piloted in the §7 validation track.

## 11. Gap alignment — why this spec is the Phase-2 priority payoff

The gap analyzer (`gap_analysis.md`) ranks `compliance/evaluation` and the
other `*/evaluation` cells as the corpus's thinnest, most-surging white space —
i.e. the field has instruments but almost no *evidence that programs using them
worked*, especially for Art. 4. This spec is the deliverable that closes that
loop: it turns the §10 instruments into an **evaluation chain** (role → task →
measured level → stored evidence) that is simultaneously a program-evaluation
artifact and an Art. 4 compliance record (§8). The pinned `rq3.md` gap-cell
shortlists (e.g. *Dutch municipalities' AI Act compliance readiness*, the
*AIconomics Maturity Model*) are the first real-world targets to run §7
validation against.

**Next steps (Phase 6):** pilot the 6 default task matrices with 2-3
customer-aligned roles; run validation steps §7 (seed with SFAILQ + AICOS as the
objective anchors); fold results into the ALaaS reporting/upsell design.
