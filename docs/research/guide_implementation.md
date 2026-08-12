# Guide 1 — Implementing AI-Literacy Programs in Organizations

**Phase 3 deliverable (Synthesis A: RQ1 + RQ2)** · draft v1 · 2026-08-12
**Evidence base:** ai-literacy-research corpus (4,414 papers, 100% saturation);
extraction tables `docs/research/extraction/rq1.md` + `rq2.md` (50 studies);
screening tier A–E per PROTOCOL.md §4. Tiers are provisional (abstract-level)
until full-text verification. Claims are graded: **(A)** RCT/meta-analysis,
**(B)** quasi-experimental/panel, **(C)** longitudinal/cross-sectional,
**(D)** case/experience, **(E)** conceptual/position.

**Purpose:** answer, with evidence, the two questions the field has left open —
*what is AI literacy* (construct model) and *how do you build it in an
organization* (implementation playbook). Companion: [Guide 2 (evaluation) →
Phase 4], [assessment instrument spec → Phase 5].

---

## 1. Executive summary

1. **AI literacy is a staged developmental construct, not a binary skill.**
   Converging frameworks (DALF, AI Fluency, RAIL-Ed) and psychometric evidence
   (A-factor, AI Mindset) agree: people move from exposure through reflective
   use to integrated, critical, context-aware practice — and most sit at the
   extremes (avoidance or uncritical reliance).
2. **Training is the documented moderator that makes adoption pay.**
   Panel evidence shows AI adoption pays off *with* complementary training;
   a 35-country study shows workplace training steepens the
   exposure→adoption gradient. The question is no longer *whether* to train
   but *how*.
3. **Implementation succeeds when it is organizational, not curricular.**
   The strongest implementation evidence points to conditions outside the
   classroom: psychological safety, continuous upskilling architecture,
   role-specific curricula, and management support. Technostress is a real,
   measurable barrier; training moderates it.
4. **Design for the job, not the technology.** Assessment and curricula
   aligned to real occupational tasks outperform generic knowledge-based
   programs; self-reported literacy diverges from demonstrated competence,
   so programs must build in objective measures.
5. **Beware the training trap.** Training that optimizes for today's
   AI-teachable skills can over-invest in skills destined for obsolescence;
   curricula must teach meta-skills and adaptability alongside tool use.

---

## 2. Construct model (RQ1 synthesis)

### 2.1 The developmental continuum

Five convergent stage models, ordered by empirical grounding:

| Model | Stages | Setting | Evidence |
|-------|--------|---------|----------|
| DALF — Developmental AI Literacy Framework | 3: foundational awareness → reflective application → integrated professionalization | Counselor education | (E) conceptual |
| AI Fluency framework | 6: exposure → ... → strategic, critical, ethical, contextual use | Higher education | (E) conceptual |
| RAIL-Ed (Responsible AI Literacy in Education) | Integrative, developmental, dialectical; ethics as constitutive | Teacher education | (E) synthesis of 67 studies |
| Five-stage continuum (transfer corpus) | Avoidance ↔ uncritical reliance extremes | Higher education | (E) conceptual |
| AI Mindset (triadic) | Dispositional × contextual × technology appraisals | Teacher use | (C) empirically tested |

**Synthesis:** a usable construct model for program design has three axes:

- **Competence depth** (know → use → evaluate → create/integrate),
  evidenced by the psychometric A-factor (one dominant latent factor across
  interaction tasks, 44% variance; (C), N=517) — i.e., there *is* a coherent
  construct to train, not a grab-bag of tool skills.
- **Autonomy** (dependence → independence), from DALF's parallel to
  professional development.
- **Disposition** (attitudes, self-efficacy, mindset), from AI Mindset's
  empirically tested triadic structure — psychological factors measurably
  shape competence and use.

### 2.2 What literacy is NOT

- **Not self-assessment.** Self-reported and objective measures of AI
  literacy correlate only weakly (C, K-12 teachers; CFA + latent profile).
  Programs that rely on "I know AI" pre-tests mis-measure their baseline.
  → Use objective instruments (Guide 2, RQ3: MAIL-CS, AICOS, SAIL4ALL).
- **Not tool proficiency.** The task-oriented critique (AI Literacy
  Assessment Revisited) shows definitions emphasizing programming/statistics
  miss what workers actually need: interpreting outputs, selecting tools,
  ethical judgment.
- **Not a one-shot workshop.** The LLM-fallacy mechanism (D) shows users
  systematically over-attribute LLM outputs to their own competence — a
  transient workshop without reflective practice can inflate perceived
  competence while real capability lags.

### 2.3 Practical implication for program design

Design programs as **staged, role-specific, and objective-assessed**:
tier the curriculum to the continuum (awareness → application → evaluation →
creation), map each tier to job tasks, and measure with objective instruments
at each gate. This is the construct backbone the ALaaS tiers can be mapped to.

---

## 3. Implementation evidence (RQ2 synthesis)

### 3.1 What the strongest evidence says

| Finding | Design | Tier | Studies |
|---------|--------|------|---------|
| Training complements AI adoption (adoption pays off with training) | Panel econometrics | (B) | AI Adoption and Workplace Training (SSRN 4990293) |
| Workplace training steepens the exposure→adoption gradient at country level | 35-country survey + shift-share | (B) | From Exposure to Adoption (arXiv 2604.18849) |
| Organizational adoption drives self-directed learning via job insecurity + job crafting chain | Survey, N=303, mediation | (C) | Org adoption → learning behavior (2025) |
| Technostress reduces adoption and well-being; training moderates | Cross-sectional SEM, manufacturing SMEs | (C) | The human side of AI adoption (JMTM 2025) |
| Training + leadership support + data readiness drive SME adoption outcomes | Survey, N=400, regression | (D) | SME AI adoption Delta State (2025) |
| Multi-org literacy programs shift adoption behavior (UTAUT) | Multi-organization survey | (C) | From AI Literacy to AI Use (HICSS 2026) |
| Enterprise-scale upskilling works with adaptive design + psychological safety | Practitioner case (Citi 175k) | (D) | Enterprise AI Upskilling at Scale (2025) |
| AI-integrated training sustains performance/readiness over time | Survey, N=174 IT professionals | (C) | Long-term effects of AI-integrated training (2025) |

### 3.2 The implementation conditions framework (from the evidence)

Combine the evidence into four condition clusters — all four are necessary:

1. **Org conditions (antecedents):**
   - Management/leadership support (SME evidence, D)
   - Data readiness (SME evidence, D)
   - Technical capability present; technostress actively managed (C)
   - Psychological safety for experimentation (Citi case, D)
2. **Program conditions (design):**
   - Role-specific, stratified curricula (M-SHALF logic; DGKL; FALCON-AI role
     embeddedness)
   - Continuous upskilling architecture, not one-shot (Citi case; end-to-end
     framework)
   - Adaptive/self-paced delivery options (RAG-PRISM; gAI-PT4I4; ChatGPT
     Python module, D)
3. **Workforce conditions (learners):**
   - Expectation recalibration (from persona-migration evidence in the
     ai-adoption corpus)
   - Cohort-aware delivery (outcome differences by cohort)
   - Meta-skill framing to avoid the training trap (E)
4. **Measurement conditions (proof):**
   - Objective baseline + exit instruments (RQ3)
   - Evaluation design from day one (Guide 2)

### 3.3 Curriculum architecture examples (what exists, what works)

- **UNIV 182 (George Mason, D):** prerequisite-free, five mechanisms —
  conceptual pipeline traversed repeatedly, integrated ethics, AI Studios
  (structured in-class work with real-time critique), cumulative assessment
  portfolio. Best documented course architecture in the corpus.
- **High-school AI Methods PD (D):** 5-day scaffolded units (data analytics →
  transfer learning) with hands-on activities — a compact format for
  professional audiences.
- **MSME 1-day workshop (D):** prompt formulation → copywriting → CTA with
  hands-on mentoring; useful for micro-segments but no follow-up measurement.
- **Radiology training experiment (D, within-subjects):** no-AI vs
  on-demand-AI vs integrated-AI scenarios showed measurable upskilling (and
  deskilling risks) — the clearest template for measuring a training program
  against a real task.
- **Salesperson AI training (D, SEM-PLS, N=178):** customized, performance-
  data-driven training content improved training and performance outcomes.

---

## 4. Implementation playbook (10 steps)

**Phase A — Assess (weeks 0–2)**

1. **Readiness audit** (org): management support, data readiness, technical
   capability, technostress level, psychological safety. Instrument: adapt
   the SME survey constructs + T-IPO/LARA task matrix.
2. **Task inventory** (per role): list the actual AI-adjacent tasks per
   occupation; score AI-exposure per task. This defines *what* literacy means
   in this organization (task-oriented, not generic).
3. **Baseline measurement** (objective): MAIL-CS / AICOS / SAIL4ALL (RQ3
   instruments), not self-report alone. Record the SR-vs-OB gap — it is the
   strongest argument for the program's necessity.

**Phase B — Design (weeks 2–6)**

4. **Stage the curriculum**: map roles to continuum levels
   (awareness → application → evaluation → creation); tier content per role.
5. **Build the delivery architecture**: mix of self-paced modules (adaptive)
   + AI Studios-style applied sessions + embedded coaching; continuous
   cadence, not one-shot. Include reflective practice to counter the
   LLM fallacy.
6. **Train the trainers / managers first** (leadership support is an
   evidenced antecedent); then role cohorts.
7. **Expectation recalibration** in onboarding: what AI can/cannot do, what
   the program will/won't deliver — documented churn-reduction factor.

**Phase C — Deliver (weeks 6–12)**

8. **Run cohort 1 as a pilot with measurement built in** (Guide 2 design:
   Kirkpatrick levels 1–4 mapped to this program; objective instruments at
   gates). Manage technostress explicitly (support channels, workload
   protection).
9. **Iterate** on task inventories and materials from pilot data.

**Phase D — Prove & scale (week 12+)**

10. **Report outcomes** (Guide 2) — adoption behavior, task-level usage,
    productivity proxies, compliance posture (Art. 4 documentation). Scale
    only what the pilot evidence supports.

---

## 5. Risks (from the evidence)

| Risk | Evidence | Mitigation |
|------|----------|------------|
| Training trap — teaching skills AI will automate | Training for Obsolescence (E, model) | Meta-skills (critical evaluation, task decomposition) + forward-looking signals |
| Perceived ≠ actual competence | SR-vs-OB misalignment (C) | Objective instruments at every gate |
| Technostress backlash | SME SEM (C) | Explicit stress management; workload protection; psychological safety |
| One-shot effect decay | LLM fallacy (D); long-term training study (C) | Continuous architecture; spaced reinforcement |
| Compliance theater — training to tick Art. 4 box | AI Act norm evolution (E) | Role-specific, documented, measurable programs (Guide 2 evidence chain) |

---

## 6. What this means for ALaaS (transfer)

- **Tier mapping:** ALaaS tiers map directly to the continuum stages
  (Awareness → Application → Evaluation → Creation), giving each tier a
  construct-backed identity instead of a price point.
- **Audit-first selling:** step 1–3 (readiness + task inventory + objective
  baseline) is the lead magnet and the consulting entry point; it is
  evidence-backed (SME antecedents, task-oriented assessment).
- **Program architecture:** continuous, role-specific, applied-session
  design (not webinar bundles) — the corpus's documented success factors.
- **Art. 4 positioning:** the implementation playbook *is* the practical
  interpreter of Article 4; the compliance narrative is anchored by RQ5
  studies (M-SHALF, Workforce Readiness analysis).
- **Proof loop:** measurement built into delivery (Guide 2) produces the
  outcome reports that justify renewal pricing.

---

## 7. Open questions (for full-text extraction & refresh)

1. Confirm the JEBO panel result's effect sizes at full text (training
   mediates adoption ROI — the load-bearing claim).
2. Verify the multi-org UTAUT study's effect sizes and program design.
3. Extract the radiology experiment's quantitative results (deskilling
   conditions) — directly transferable to evaluation design.
4. Track new Art. 4 operationalization studies quarterly (fast-moving).

---

*Draft v1 · Tobias Weiss · KI-Kompetenz-Training · ki-kompetenz-training@tobias-weiss.org*
*Next: Phase 4 — Guide 2 (Evaluation), then Phase 5 — assessment instrument spec.*
