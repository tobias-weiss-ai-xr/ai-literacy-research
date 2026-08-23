# Research Plan — AI-Literacy Implementation & Evaluation

**Status:** active — Phases 0–1 complete; Phase 2 in progress (priority gap
cells shortlisted); Guides 1–2 drafted v1.1; gap-analysis tool shipped
(`tools/research_gap_analyzer.py` → `docs/research/gap_analysis.md`)
**Companion protocol:** [PROTOCOL.md](PROTOCOL.md)
**Evidence base:** this corpus (papers.yaml, **11,640 papers** across 20 categories, 100% saturation)

---

## 1. Problem & Motivation

The business-development corpus identified two almost-empty taxonomy cells as
the biggest white space in AI-adoption research:

| Cell | Papers | Meaning |
|------|-------:|---------|
| `ai-adoption/development` | 5 | finite evidence on *how to implement* AI-literacy programs |
| `ai-adoption/evaluation` | 5 | finite evidence on *how to measure* programs and their ROI |

Yet the adjacent evidence is strong and growing: training mediates adoption
ROI (econometric panel studies), literacy is a staged continuum, and EU AI
Act Art. 4 turns literacy into a compliance obligation. The gap is not
evidence *that* training matters — it is actionable, synthesized guidance on
*how to do it* and *how to prove it*.

**Research program outcome:** two corpus-grounded guides + one assessment
instrument specification that can feed the ALaaS offer, the content site and
the learning platform — and are defensible because they rest on a systematic
evidence base nobody else has assembled.

---

## 2. Research Questions

| # | Question | Primary categories |
|---|----------|--------------------|
| RQ1 | Which conceptualizations and stage models of AI literacy exist, and which have empirical support? | `ai-literacy-construct`, `assessment` |
| RQ2 | Which implementation strategies for organization-level AI-literacy programs are evidenced, and under which conditions do they work? | `org-implementation`, `learning-design`, `workforce-upskilling`, `sme-training` |
| RQ3 | How is AI literacy measured — which instruments exist, with what validity — and which evaluation frameworks apply to programs? | `assessment`, `program-evaluation` |
| RQ4 | What evidence links AI-literacy training to behavior change, productivity and firm performance? | `roi-measurement`, `program-evaluation`, `adoption-behavior` |
| RQ5 | How do organizations operationalize EU AI Act Art. 4 literacy obligations in practice? | `compliance`, `org-implementation` |

---

## 3. Method (Living Systematic Review + Corpus Analytics)

A *living* systematic review: the corpus pipeline refreshes monthly-to-
quarterly, and the synthesis documents track the evidence as it grows.

### 3.1 Quantitative layer (automated, this repo)

- Taxonomy coverage/saturation per cell (`statistics.json`)
- Momentum & bursts per category (12-month windows)
- Gap tracking: the two target gaps are re-measured every refresh
  (`tools/landscape_analyzer.py`, `README.md` gap section)

### 3.2 Qualitative layer (manual, per PROTOCOL.md)

- Inclusion/exclusion criteria (published 2021+, org/workplace or education
  settings, substantive literacy/training focus)
- Priority screening list: papers in the 6 target categories, recent first
  (`tools/brief_generator.py` seed lists)
- Full-text extraction into a shared extraction table
  (`docs/research/extraction/`), one row per study
- Simple quality appraisal (design tier: RCT → quasi-experimental → panel →
  longitudinal survey → cross-sectional survey → case study)
- Synthesis per RQ: narrative + evidence tables (graded by design tier)

---

## 4. Phases & Deliverables

| Phase | What | Deliverable | Exit criterion |
|-------|------|-------------|----------------|
| **0 — Corpus** (done) | 20-category AI-literacy corpus, pipeline, CI | this repo | validate passes; saturation ≥ 95% |

*Seed grew to **11,640 papers**, 100% saturation (2026-08-23); original
seed snapshot was 4,414 papers (2026-08-12): OpenAlex bulk (~2,700) +
arXiv + CrossRef/DBLP/EuropePMC. Fine-grained OpenAlex refresh
(`scripts/fetch/fetch_openalex.py`) can be added later — mind the 1,000
credits/day free budget (10 credits per page, resets at midnight UTC);
the weekly CI discovery job keeps the arXiv side fresh automatically.
| **1 — Mapping** (done) | Cell-level map of the 6 target categories; 25–40 papers shortlisted per RQ | `docs/research/mapping_review.md` | shortlist table complete |
| **2 — Extraction** (in progress) | Abstract screening done: 72/150 included, refilled to 25/RQ; evidence tables `rq1-5.md` created, 17 key studies pre-extracted; 109 rows await full-text extraction; **priority gap-cell shortlists pinned into `rq2.md`/`rq3.md`**; **9 gap-cell studies extracted as abstract-level rows (RQ2-26–29, RQ3-26–30) from `gap_analysis.md`** | `docs/research/extraction/*.md` + evidence tables | ≥ 80% of shortlist extracted |
| **3 — Synthesis A: Implementation Guide** (draft v1.1, refreshed with 11.6k corpus + gap-cell evidence) | RQ1+RQ2: construct model (continuum × 3 axes) + implementation conditions framework + 10-step playbook + risks + §8 white-space-cell evidence | **Guide 1** (`docs/research/guide_implementation.md`) | expert review (2 readers) |
| **4 — Synthesis B: Evaluation Guide** (draft v1.1, refreshed with 11.6k corpus + gap-cell evidence) | RQ3+RQ4+RQ5: 10+ instruments catalogued (incl. SFAILQ), outcome evidence table, Art. 4 evidence chain, business-case designs (task-based quasi-experiment + SME-minimum) + §8 white-space-cell evidence | **Guide 2** (`docs/research/guide_evaluation.md`) | expert review |
| **5 — Instrument spec** (draft v1.1, refreshed with 11.6k corpus instruments) | Task-oriented AI-literacy assessment (occupation-aligned, levels 1–4) informed by RQ3; §10 instrument reference grounds CORE/COMPANION in corpus-validated measures (AICOS, MAIL-CS, SFAILQ, …); §11 aligns spec to the `compliance/evaluation` white space | `docs/research/assessment_spec.md` | pilot in ALaaS cohort |
| **6 — Publication & transfer** (in progress: 6 content pieces drafted) | Articles, newsletter, ALaaS offer redesign, platform integration, EU AI Act compliance mapping; **drafted 2026-08-23 (all corpus-grounded):** `research_brief_2026.md` (evidence-gap brief), `readiness_mini_audit.md` (lead magnet), `compliance_mapping.md` (Art. 4 mapping), `alaas_offer_redesign.md` (offer tiers), `newsletter_draft.md`, `linkedin_post.md` | 6+ pieces + offer changes | published & live |
| **Ongoing — Refresh** | Quarterly corpus update + gap re-measurement + guide updates | updated artifacts | CI green |

**Target timeline (indicative):** Phases 1–2 in weeks 1–4, 3–4 in weeks
5–8, 5–6 in weeks 9–12; refresh quarterly thereafter.

---

## 5. Outputs & Transfer (why this research pays back)

| Output | Transfer target |
|--------|-----------------|
| Guide 1 — implementation playbook | ALaaS offer design (tiers, delivery, onboarding); lead magnet (readiness mini-audit); consulting collateral |
| Guide 2 — evaluation framework | ALaaS reporting ("what you get": measured outcomes); platform features (assessments, dashboards); premium upsell |
| Assessment instrument | Product: validated baseline/exit assessments per occupation |
| 6+ content pieces | ki-kompetenz-training.org, newsletter, LinkedIn (title authority in the gap nobody covers) |
| EU AI Act compliance mapping | Compliance-aware positioning ("practical interpreter") |

## 6. Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Corpus too thin in target cells | Multi-source fetchers (CrossRef/DBLP); hand-adding via `paper_submission` template; snowballing from cited references |
| Evidence quality low (surveys dominating) | Quality-tier grading; clearly label survey-only claims; lean on panel/econometric studies where they exist |
| Scope creep | RQ-scoped shortlists capped at ~30 papers each; synthesis under 15 pages per guide |
| Findings become stale | Living-review refresh quarterly; CI-driven discovery keeps the corpus current |
| Time box | Solo operator reality: phases 3–6 are the *minimum* viable synthesis — extraction capped, guides lean |

## 7. How to Execute (tools)

```bash
# 1. Refresh evidence (quarterly)
python3 scripts/fetch/fetch_openalex.py --months 3
python3 scripts/validate_papers.py
python3 scripts/analysis/generate_analysis.py
python3 scripts/generate_readme.py

# 2. Check target gaps (should be shrinking in future refreshes)
python3 tools/landscape_analyzer.py | grep -A8 "Thinnest"

# 3. Build shortlists per RQ
python3 tools/brief_generator.py "implementing AI literacy programs" --papers 30 --json > docs/research/extraction/seed_rq2.json
python3 tools/brief_generator.py "measuring AI literacy evaluation" --papers 30 --json > docs/research/extraction/seed_rq3.json

# 4. Track trends for content timing
python3 tools/trend_scanner.py --months 12
```

---

*Author: Tobias Weiss · KI-Kompetenz-Training · ki-kompetenz-training@tobias-weiss.org*
*Last updated: 2026-08-11*