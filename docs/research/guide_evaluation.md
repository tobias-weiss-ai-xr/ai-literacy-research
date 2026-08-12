# Guide 2 — Evaluating AI-Literacy Programs: Measurement, Outcomes, ROI

**Phase 4 deliverable (Synthesis B: RQ3 + RQ4 + RQ5)** · draft v1 · 2026-08-12
**Evidence base:** extraction tables `docs/research/extraction/rq3.md`,
`rq4.md`, `rq5.md` (75 studies); tiers A–E per PROTOCOL.md (provisional at
abstract level). Companion: [Guide 1 — Implementation](../guide_implementation.md),
[assessment instrument spec → Phase 5].

**Purpose:** answer the second open question — *how do you measure an
AI-literacy program and prove its value* — with the instruments, frameworks
and evidence that exist, plus a business-case design organizations can run.

---

## 1. Executive summary

1. **Validated instruments exist.** At least nine psychometrically tested
   AI-literacy scales are documented (MAIL-CS, AICOS, SAIL4ALL, SNAIL,
   FALCON-AI, GenAI-RTS, EUIA, Korean AILS, Arabic AILS) — you do not need to
   build your own; you need to *choose* and *use* them properly.
2. **Self-report is not enough.** Objective and self-report measures of AI
   literacy correlate weakly; evaluation designs that rely on pre/post
   self-assessment systematically overstate gains. Use objective instruments
   (MAIL-CS/AICOS) plus task-based measures.
3. **Task-based evaluation is the emerging standard.** The clearest template
   in the corpus is a within-subjects training experiment (radiology:
   no-AI vs on-demand vs integrated AI on a real diagnostic task) — it
   measured both upskilling and *deskilling* risks. Evaluate on the job's
   actual tasks, not on quiz scores.
4. **The ROI evidence is real but thin and conditional.** The load-bearing
   claim — training mediates whether AI adoption pays off — comes from panel
   econometrics (B). Direct training→productivity quantification is rare
   (practitioner estimates, tier E). Therefore: evaluate programs with
   *designs that generate the missing evidence* (quasi-experimental,
   task-level outcomes) — that is your differentiator and your Art. 4 proof.
5. **Art. 4 makes evaluation a compliance requirement.** Documented,
   role-specific, measurable literacy programs are the operationalization of
   Article 4; an evaluation chain (what was trained → measured with what →
   at what level) is the defensible compliance artifact.

---

## 2. Measurement landscape (RQ3)

### 2.1 Instruments with validity evidence

| Instrument | Items/Factors | Population | Validity evidence | Tier |
|-----------|---------------|------------|-------------------|------|
| MAIL-CS | 32 items, 4 factors (Foundational Knowledge & Ethics; Operational Skills; Critical Evaluation; Application & Innovation) | Chinese university students (N=850) | EFA/CFA split-sample; α=.91, ω=.92; convergent (digital literacy, critical thinking) + discriminant validity | (C) |
| AICOS | Objective AI competency scale, includes GenAI dimension | Adults | Development + validation; objective format | (C) |
| SAIL4ALL | 56 items, 4 themes (What is AI? What can AI do? How does AI work? How should AI be used?) | Adults, any setting | Psychometric validation; themes usable independently | (C) |
| SNAIL | Scale for non-experts' AI literacy | Course participants | Used to measure AI-learning gains; comparability | (C) |
| FALCON-AI | Role-embedded (43 → concise), CTRL framework | University faculty | Development + validation | (C) |
| GenAI-RTS | 20 items, 4 reliance types | Undergraduates (academic writing) | Development + multi-source validation | (C) |
| EUIA | 6 levels of GenAI interaction in assessment | Assessment contexts | Case study + pilot | (D) |
| AILS (KR) | AI literacy dimensions + questionnaire | Korean university students | Validity + reliability study | (C) |
| AILS (Arabic) | Multinational validation of AILS | Arab adults | Multinational validation | (C) |
| G-Factor/A-Factor battery | 18 items, 4 dimensions | Adults (N=517, 3 studies) | A-factor 44% variance; lab validation | (C) |

**Selection guidance:** for organizational programs, prefer **AICOS or
MAIL-CS** (objective/validated, GenAI-era); for cross-population benchmarking
**SAIL4ALL**; for faculty/staff roles **FALCON-AI**; for reliance/behavior
change **GenAI-RTS**. Combine an objective instrument with a task-based
measure (below) — never rely on self-report alone.

### 2.2 The measurement warnings

- **SR vs OB divergence (C):** self-reported and objective literacy correlate
  weakly; experience shapes the relationship. Baseline/exit comparisons must
  use the same instrument type at both points.
- **Task-orientation (E→D):** knowledge-based definitions miss what workers
  need (interpreting outputs, tool selection, ethical judgment). Assessment
  must be aligned to occupational tasks (occupation-aligned task matrices).
- **Construct validity is evolving:** the A-factor suggests one dominant
  literacy factor; MAIL-CS finds four. Instrument choice changes measured
  outcomes — state the construct model explicitly.

### 2.3 Evaluation frameworks (legacy + AI-specific)

- **Kirkpatrick / CIPP (E, legacy):** level 1 reaction, 2 learning,
  3 behavior, 4 results — the organizing skeleton for program evaluation;
  the corpus's generic training-evaluation literature (nuclear, aviation,
  health) provides mature procedures for levels 1–2.
- **ROI methodology (Phillips-style, E, legacy):** cost-capture and
  benefit-isolation procedures for converting level-4 results into ROI;
  not AI-specific but directly applicable.
- **AI-specific additions (from this corpus):** task-level outcome
  measurement (radiology experiment template), SR-vs-OB gap tracking,
  adoption-behavior measures (UTAUT), technostress/well-being monitoring.

---

## 3. Outcome evidence (RQ4) — what training demonstrably does

| Outcome | Evidence | Tier |
|---------|----------|------|
| Training complements AI adoption; adoption pays off *with* training | Panel econometrics (establishments) | (B) |
| Country-level workplace training steepens the exposure→adoption gradient | 35-country survey, shift-share | (B) |
| Org AI adoption increases self-directed learning (via job insecurity + job crafting) | N=303, mediation | (C) |
| Training moderates technostress → adoption and well-being | SME SEM | (C) |
| AI-integrated training sustains performance, adaptiveness, readiness | N=174 IT professionals | (C) |
| AI-driven training improves salesperson training & performance | N=178, SEM-PLS | (D) |
| AI-supported training measurably upskilled (and could deskill) residents on a real task | Within-subjects experiment, 8 residents/150 CXRs | (D) |
| Direct per-practitioner ROI (training $12–25K → $150–300K) | Practitioner economic analysis | (E, verify) |
| Training-trap risk: over-investing in AI-teachable skills | Theoretical model + pre-registered pilot | (E) |

**Reading:** the causal chain *training → behavior change → productivity* is
supported at each link but rarely measured end-to-end in one study. The
strongest links: training→adoption (B), training→behavior/performance (C/D).
The weakest link: training→firm ROI (only E-level quantification exists).
→ This is the evidence gap your evaluation designs should fill (see §5).

---

## 4. Compliance evaluation (RQ5) — Art. 4 as the proof driver

- **Art. 4 requires a "sufficient level of AI literacy"** — undefined in the
  regulation; interpretation is emerging (M-SHALF; DGKL lab guidance; the
  notion of AI literacy in employment).
- **Operationalization consensus:** role-specific, stratified curricula
  (clinical/admin/technical in M-SHALF) with documented delivery — the
  closest thing to a standard that exists.
- **Readiness gap is documented:** 46% of organizations report readiness gaps
  (McKinsey 2025, cited in the Workforce Readiness analysis); legislation
  literacy measurably predicts adoption intentions (C, N=109 Romanian
  healthcare, confidence as mediator).
- **The weakened-norm warning (E):** Art. 4 was pared down in trilogue;
  efficacy concerns mean compliance *theater* is a real risk — evaluations
  that produce verifiable, role-specific evidence are the antidote.
- **Compliance evidence chain (recommended artifact):** for each role →
  (1) task inventory with AI exposure; (2) objective baseline; (3) curriculum
  delivered (content, hours, mode); (4) objective exit + task-based gain;
  (5) behavior follow-up (adoption, task-level usage); (6) Art. 4
  documentation mapping. This chain *is* the operationalization of
  "sufficient level" for an auditor.

---

## 5. Business-case evaluation design (what to run)

### 5.1 Recommended design: task-based quasi-experiment (mirrors the radiology template)

- **Design:** pre/post with a comparison group (or within-subjects conditions
  per task); measure on real occupational tasks with objective scoring.
- **Instruments:** objective literacy scale (AICOS/MAIL-CS) + task
  performance + SR-vs-OB gap + adoption behavior (UTAUT items) +
  technostress/well-being (for SME/manufacturing settings).
- **Timeline:** baseline (week 0) → training → immediate exit (week 8–12) →
  behavior follow-up (week 24) → business outcomes (quarter 2–4).
- **Sample:** cohort-level (N≥30 per role for within-org comparisons);
  multi-org or multi-cohort for stronger claims (the multi-org UTAUT study
  is the model).
- **Reporting:** Kirkpatrick L1–L4 table + ROI where cost data allows
  (Phillips procedures), with tier labels per claim.

### 5.2 Minimum viable evaluation (for SMEs / €99 tier)

1. Objective baseline + exit (one instrument, 30 min each).
2. One task-based measure per role (pre/post on a scored task).
3. Adoption behavior survey at week 12 (UTAUT short form).
4. One-page report: gains, SR-vs-OB gap, adoption rate, next steps.

### 5.3 What NOT to do

- Pre/post self-assessment only (SR-vs-OB divergence invalidates it).
- Quiz scores as "business impact" (level 2 ≠ level 4).
- No baseline (selection effects; can't attribute change).
- Training-trap curricula measured only on tool proficiency (measure
  meta-skills and task adaptability).

---

## 6. What this means for ALaaS (transfer)

- **Reporting as product:** the L1–L4 + task-gain report is the premium
  upsell (€799 tier) — it produces the outcome evidence the market lacks.
- **Art. 4 package:** the compliance evidence chain (role × task × measure)
  is a sellable artifact and the "practical interpreter" positioning.
- **Instrument licensing/practice:** using validated instruments (MAIL-CS
  style) rather than building bespoke quizzes boosts credibility and legal
  defensibility.
- **The evidence gap is the moat:** most competitors sell training without
  measurement; Guide 2's designs produce the before/after numbers that
  justify renewal and referrals.

---

## 7. Open questions (full-text verification & refresh)

1. Verify MAIL-CS/AICOS item-level details and licensing at full text.
2. Confirm the radiology experiment's quantitative gains/deskilling effect
   sizes (the template design).
3. Confirm the JEBO panel effect size for training-mediation of adoption ROI.
4. Track quarterly: new Art. 4 operationalization studies; new instrument
   validations (instrument registry in the corpus is dated 2025-10).
5. Phase 5: convert §2.1 + task-orientation evidence into the task-oriented
   assessment instrument spec (occupation-aligned, levels 1–4).

---

*Draft v1 · Tobias Weiss · KI-Kompetenz-Training · ki-kompetenz-training@tobias-weiss.org*
*Next: Phase 5 — assessment instrument specification.*
