# Protocol — Living Systematic Review of AI-Literacy Implementation & Evaluation

Companion to [RESEARCH_PLAN.md](RESEARCH_PLAN.md). This protocol defines how
papers move from the corpus into the evidence tables and guides. It is a
simplified, solo-operator-viable adaptation of PRISMA.

---

## 1. Scope

**Population:** organizations (SMEs, enterprises, public sector) and
education settings (workplace training, higher ed, professional ed) running
or planning AI-literacy initiatives.

**Intervention:** AI-literacy training programs — workshops, courses,
coaching, e-learning, embedded upskilling, assessments.

**Comparison:** no training; alternative formats; tool-only adoption.

**Outcomes:** literacy/competence gains; attitude/trust change; behavior
change (usage, task-level adoption); training-transfer; productivity/firm
performance; compliance (EU AI Act Art. 4).

**Time frame:** 2021–present (generative-AI era). Pre-2021 papers only for
construct history (RQ1).

---

## 2. Search & Screening

### 2.1 Corpus layer (automated)

Primary source: this corpus (OpenAlex + arXiv + CrossRef/DBLP/EuropePMC,
taxonomy-tagged). Secondary: reference snowballing from included papers.

### 2.2 Priority categories

Shortlists are drawn from these categories (in priority order):

| RQ | Categories |
|----|------------|
| RQ1 | `ai-literacy-construct`, `assessment` |
| RQ2 | `org-implementation`, `learning-design`, `workforce-upskilling`, `sme-training` |
| RQ3 | `assessment`, `program-evaluation` |
| RQ4 | `roi-measurement`, `program-evaluation`, `adoption-behavior` |
| RQ5 | `compliance`, `org-implementation` |

### 2.3 Inclusion criteria

1. Peer-reviewed journal article, conference paper, or arXiv preprint with
   substantive methodology section.
2. Reports primary data (empirical) or is a systematic review/meta-analysis.
   Pure opinion/position papers excluded (except RQ1 construct history).
3. Focus on AI literacy/competence/skills or AI training (not general AI
   adoption without a training component).
4. English or German full text available.
5. 2021+ (empirical); any date (RQ1 constructs).

### 2.4 Screening flow

1. **Title/abstract screen** — from the corpus shortlist (seed lists via
   `tools/brief_generator.py --json`), keep ~30 studies per RQ.
2. **Full-text retrieval** — DOI or arXiv URL from `papers.yaml`.
3. **Eligibility** — against inclusion criteria above.
4. **Extraction** — into the tables below.

---

## 3. Data Extraction

One section per study appended to `docs/research/extraction/` (markdown
table rows), capturing:

| Field | Notes |
|-------|-------|
| Study ID | e.g. `RQ2-01` |
| Citation | title, authors, year, venue, URL |
| Setting | SME / enterprise / public / HE / K-12 |
| Population | N, roles, sector |
| Construct model | which literacy framework/stages used |
| Intervention | format, duration, delivery (human/AI-tool) |
| Measures | instrument(s), self-report vs task-based |
| Outcomes & effects | levels 1–4 (Kirkpatrick), effect sizes if reported |
| Design tier | RCT / quasi / panel / longitudinal / cross-sectional / case |
| Limitations | author-stated + reviewer notes |
| Relevance | which RQ, which guide section |

## 4. Quality Appraisal

Tier-based, deliberately simple:

| Tier | Design | Weight in synthesis |
|------|--------|---------------------|
| A | RCT, meta-analysis | Highest |
| B | Quasi-experimental, panel econometrics | High |
| C | Longitudinal survey, matched designs | Medium |
| D | Cross-sectional survey, case study | Low; claims flagged |
| E | Position, opinion | Context only |

Evidence tables list tier per row. Synthesized claims must state the tier:
"panel evidence (B)" vs "survey evidence (D)".

## 5. Synthesis

- Per RQ: narrative synthesis organized by outcome; evidence table; open
  questions.
- Cross-RQ: the implementation guide (RQ1+RQ2), the evaluation guide
  (RQ3+RQ4+RQ5), and the assessment spec (RQ3).
- Claims with conflicting evidence report both sides and the tier gap.

## 6. Living Updates

- Quarterly: re-run corpus refresh, re-measure target gaps
  (`ai-adoption/development`, `ai-adoption/evaluation` in the source corpus;
  `org-implementation/development`, `assessment/evaluation`,
  `program-evaluation/*` here), screen new papers into shortlists.
- Version guides (`v1, v2, ...`) and record the date of last evidence
  review in each guide.

## 7. Reporting

Each deliverable states: search date, corpus version (commit hash /
statistics.json generated_date), number of studies screened/extracted,
tier distribution, and limitations.

---

*Protocol v1 · 2026-08-11 · Tobias Weiss*