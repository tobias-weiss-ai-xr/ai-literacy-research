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
a corpus of 9,653 papers across 20 AI-literacy disciplines, analyzed with
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
| **Papers Analyzed** | 9,653 |
| **AI-Literacy Disciplines** | 20 |
| **Time Span** | 1984-2026 |
| **Research Aspects** | 8 |
| **Taxonomy Cells** | 160 |
| **Saturation** | 100.0% (160/160 cells) |

### Top Evidence Areas

1. **Compliance & AI Act** — 755 papers
2. **Generative AI Skills** — 734 papers
3. **Attitudes, Trust & Acceptance** — 731 papers
4. **Tools, Platforms & AI Tutors** — 581 papers
5. **AI Literacy Constructs & Models** — 567 papers
6. **Adoption Behavior & Engagement** — 521 papers

---

## 📊 The 20-Category Taxonomy

| Category | Papers |
|----------|--------|
| AI Literacy Constructs & Models | 567 |
| AI Literacy Pedagogy | 392 |
| Learning Design & Curriculum | 466 |
| Assessment & Measurement | 409 |
| Workforce Upskilling | 455 |
| Org Implementation & Change | 443 |
| SME Training & Adoption | 375 |
| Compliance & AI Act | 755 |
| K-12 Education | 340 |
| Higher Education | 437 |
| Professional & Executive Ed | 461 |
| Teacher AI Literacy | 397 |
| Critical & Ethical AI Literacy | 372 |
| Generative AI Skills | 734 |
| Attitudes, Trust & Acceptance | 731 |
| Adoption Behavior & Engagement | 521 |
| Program Evaluation & Outcomes | 409 |
| ROI & Business Impact | 423 |
| Tools, Platforms & AI Tutors | 581 |
| Lifelong & Self-Directed Learning | 385 |

### Research Aspects (Subcategories)

| Aspect | Papers |
|--------|--------|
| Theory | 945 |
| Mechanism | 875 |
| Method | 2164 |
| Application | 2382 |
| Development | 336 |
| Systems & Technology | 1940 |
| Evaluation & Benchmarks | 240 |
| Reviews & Surveys | 771 |

---

## 🚀 Emerging Themes (Last 12 Months)

1. **continuum** — 10 papers
2. **micro-learning** — 2 papers
3. **agentic** — 150 papers
4. **transfer** — 89 papers
5. **avoidance** — 16 papers
6. **agent** — 513 papers

## 📈 Category Momentum (Last 12 Months)

Ranked by output density × year-over-year growth — the strongest leading indicator for what to study next:

| Category | Total | Last 12m | Growth | 12-m share |
|----------|------:|---------:|-------:|-----------:|
| Compliance & AI Act | 755 | 518 | +157.7% | 69% |
| Generative AI Skills | 734 | 431 | +138.1% | 59% |
| Adoption Behavior & Engagement | 521 | 315 | +120.3% | 60% |
| Attitudes, Trust & Acceptance | 731 | 385 | +54.6% | 53% |
| Org Implementation & Change | 443 | 239 | +50.3% | 54% |
| Higher Education | 437 | 240 | +43.7% | 55% |

---

## 🕳️ Research Gaps (Thinnest Cells)

Cells with the fewest papers mark the white space this program targets
(especially `*/development` and `*/evaluation`):

- `org-implementation/evaluation` — 2 papers
- `sme-training/evaluation` — 2 papers
- `k12-education/evaluation` — 4 papers
- `workforce-upskilling/evaluation` — 5 papers
- `compliance/evaluation` — 5 papers
- `lifelong-learning/evaluation` — 5 papers
- `ai-literacy-construct/evaluation` — 6 papers
- `critical-ai-literacy/evaluation` — 6 papers

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

This corpus synthesizes 9,653 papers across 1984-2026 to create the
evidence base for the AI-literacy implementation and evaluation research
program — and ultimately for better AI-literacy programs everywhere.

---

**Want to explore the corpus?**
`cd tools && python3 landscape_analyzer.py`
