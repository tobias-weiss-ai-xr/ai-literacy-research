# AI-Literacy Research Corpus

**Research program** — AI-literacy implementation & evaluation. Close the two
emptiest cells of the business-development corpus (`ai-adoption/development`
and `ai-adoption/evaluation`): *how to implement* AI-literacy programs in
organizations and *how to measure* them.

**Author:** Tobias Weiss
**Contact:** ki-kompetenz-training@tobias-weiss.org
**Website:** [ki-kompetenz-training.org](https://www.ki-kompetenz-training.org)

---

## 🎯 Overview

This repository is the evidence base for the AI-literacy research program:
a corpus of 1,411 papers across 20 AI-literacy disciplines, analyzed with
the same taxonomy → momentum → burst → gap pipeline as
[business-development-research](https://github.com/tobias-weiss-ai-xr/business-development-research)
and [graph-research](https://github.com/tobias-weiss-ai-xr/graph-research).

**Research target:** the definitive, corpus-grounded guides on
(1) **implementing** AI-literacy programs (development gap) and
(2) **evaluating** them (evaluation gap, Kirkpatrick levels 3–4) —
feeding the ALaaS offer, the content site and the learning platform.

### Research Scope

| Metric | Value |
|--------|-------|
| **Papers Analyzed** | 1,411 |
| **AI-Literacy Disciplines** | 20 |
| **Time Span** | 1984-2026 |
| **Research Aspects** | 8 |
| **Taxonomy Cells** | 160 |
| **Saturation** | 80.0% (128/160 cells) |

### Top Evidence Areas

1. **Attitudes, Trust & Acceptance** — 166 papers
2. **Generative AI Skills** — 153 papers
3. **AI Literacy Constructs & Models** — 117 papers
4. **AI Literacy Pedagogy** — 107 papers
5. **Workforce Upskilling** — 98 papers
6. **Compliance & AI Act** — 96 papers

---

## 📊 The 20-Category Taxonomy

| Category | Papers |
|----------|--------|
| AI Literacy Constructs & Models | 117 |
| AI Literacy Pedagogy | 107 |
| Learning Design & Curriculum | 35 |
| Assessment & Measurement | 45 |
| Workforce Upskilling | 98 |
| Org Implementation & Change | 55 |
| SME Training & Adoption | 18 |
| Compliance & AI Act | 96 |
| K-12 Education | 36 |
| Higher Education | 64 |
| Professional & Executive Ed | 11 |
| Teacher AI Literacy | 55 |
| Critical & Ethical AI Literacy | 90 |
| Generative AI Skills | 153 |
| Attitudes, Trust & Acceptance | 166 |
| Adoption Behavior & Engagement | 86 |
| Program Evaluation & Outcomes | 19 |
| ROI & Business Impact | 74 |
| Tools, Platforms & AI Tutors | 78 |
| Lifelong & Self-Directed Learning | 8 |

### Research Aspects (Subcategories)

| Aspect | Papers |
|--------|--------|
| Theory | 115 |
| Mechanism | 149 |
| Method | 277 |
| Application | 370 |
| Development | 40 |
| Systems & Technology | 309 |
| Evaluation & Benchmarks | 63 |
| Reviews & Surveys | 88 |

---

## 🚀 Emerging Themes (Last 12 Months)

1. **continuum** — 6 papers
2. **micro-learning** — 1 papers
3. **agentic** — 36 papers
4. **ai competence** — 6 papers
5. **avoidance** — 3 papers
6. **pedagogy** — 31 papers

## 📈 Category Momentum (Last 12 Months)

Ranked by output density × year-over-year growth — the strongest leading indicator for what to study next:

| Category | Total | Last 12m | Growth | 12-m share |
|----------|------:|---------:|-------:|-----------:|
| ROI & Business Impact | 74 | 40 | +207.7% | 54% |
| AI Literacy Pedagogy | 107 | 68 | +195.7% | 64% |
| Adoption Behavior & Engagement | 86 | 51 | +200.0% | 59% |
| AI Literacy Constructs & Models | 117 | 68 | +134.5% | 58% |
| Workforce Upskilling | 98 | 53 | +120.8% | 54% |
| K-12 Education | 36 | 16 | +128.6% | 44% |

---

## 🕳️ Research Gaps (Thinnest Cells)

Cells with the fewest papers mark the white space this program targets
(especially `*/development` and `*/evaluation`):

- `ai-literacy-construct/evaluation` — 1 papers
- `ai-literacy-construct/development` — 1 papers
- `learning-design/theory` — 1 papers
- `learning-design/review` — 1 papers
- `workforce-upskilling/evaluation` — 1 papers
- `sme-training/review` — 1 papers
- `sme-training/development` — 1 papers
- `k12-education/theory` — 1 papers

---

## 📁 Repository Structure

```
ai-literacy-research/
├── README.md                          # This file
├── papers.json                        # Paper metadata (JSON export)
├── papers.yaml                        # Paper metadata (source of truth)
├── statistics.json                    # Analysis statistics
├── requirements.txt                   # Python dependencies
│
├── assets/visualizations/             # Generated charts and graphs
│
├── docs/
│   ├── research/                      # Research plan, protocol, literature review
│   │   ├── RESEARCH_PLAN.md           # Research program (questions, method) ✨
│   │   ├── PROTOCOL.md                # Systematic review protocol
│   │   └── taxonomy.md                # The 20×8 taxonomy
│   └── topics/                        # Generated content topics
│
├── tools/                             # Research & content tools
│   ├── topic_planner.py               # Topic planner ✨
│   ├── trend_scanner.py               # Emerging trend scanner ✨
│   ├── brief_generator.py             # Brief generator ✨
│   └── landscape_analyzer.py          # Landscape report ✨
│
├── scripts/                           # Research pipeline
│   ├── fetch/                         # OpenAlex (primary), arXiv, DBLP/CrossRef
│   ├── analysis/generate_analysis.py  # Statistics + visualizations
│   ├── validate_papers.py             # Corpus validation
│   └── generate_readme.py             # README generator
│
└── examples/                          # Usage examples
```

---

## 🔬 Research Program

| Deliverable | Targets the gap | Status |
|-------------|-----------------|--------|
| **Guide 1: Implementing AI-literacy programs** | `*/development`, `org-implementation`, `learning-design` | planned (see `docs/research/RESEARCH_PLAN.md`) |
| **Guide 2: Evaluating AI-literacy programs** | `*/evaluation`, `program-evaluation`, `roi-measurement` | planned |
| **Assessment instrument** | `assessment` | planned |

## 🛠️ Tools

```bash
cd tools
python3 topic_planner.py --top 10               # ranked evidence areas
python3 trend_scanner.py --months 6             # keyword bursts
python3 brief_generator.py "EU AI Act literacy obligations" --papers 5
python3 landscape_analyzer.py --write-doc       # full landscape
```

---

## 🔄 Research Pipeline

1. **Discover** — `python3 scripts/fetch/fetch_openalex.py --months 3`
2. **Validate** — `python3 scripts/validate_papers.py`
3. **Analyze** — `python3 scripts/analysis/generate_analysis.py`
4. **Visualize** — `python3 scripts/visualize_statistics.py`
5. **Report** — `python3 scripts/analysis/generate_reports.py`
6. **Generate** — `python3 scripts/generate_readme.py`

CI (`.github/workflows/validate.yml`) validates and regenerates on every push;
a weekly scheduled job opens a PR with newly discovered papers.

---

## 🔗 Related Repositories

- **Source corpus:** [business-development-research](https://github.com/tobias-weiss-ai-xr/business-development-research) — the `ai-adoption` category (380 papers) this program grew out of
- **Content site:** [ki-kompetenz-training](https://github.com/tobias-weiss-ai-xr/ki-kompetenz-training)
- **Analogous corpus:** [learning-research](https://github.com/tobias-weiss-ai-xr/learning-research)
- **Analogous corpus:** [graph-research](https://github.com/tobias-weiss-ai-xr/graph-research)

---

## 📄 License

**© 2026 KI-Kompetenz-Training | Tobias Weiss**

- **Research corpus:** Proprietary
- **Tools:** MIT License

---

## 🙏 Acknowledgments

This corpus synthesizes 1,411 papers across 1984-2026 to create the
evidence base for the AI-literacy implementation and evaluation research
program — and ultimately for better AI-literacy programs everywhere.

---

**Want to explore the corpus?**
`cd tools && python3 landscape_analyzer.py`
