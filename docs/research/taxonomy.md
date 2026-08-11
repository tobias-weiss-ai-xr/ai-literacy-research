# AI-Literacy Research — Taxonomy

The corpus classifies every paper into a **20 × 8 taxonomy**: 20 AI-literacy
categories × 8 research aspects. This structure powers saturation tracking,
gap analysis and momentum reporting — and targets the white space identified
in the business-development corpus (`ai-adoption/development`,
`ai-adoption/evaluation`).

---

## Categories (20)

| ID | Category | Focus |
|----|----------|-------|
| `ai-literacy-construct` | AI Literacy Constructs & Models | Definitions, frameworks, dimensions, stage models |
| `ai-literacy-pedagogy` | AI Literacy Pedagogy | Teaching methods, interventions, didactics |
| `learning-design` | Learning Design & Curriculum | Course/workshop design, instructional design |
| `assessment` | Assessment & Measurement | Scales, tests, task-based & psychometric measurement |
| `workforce-upskilling` | Workforce Upskilling | Workplace training, upskilling/reskilling programs |
| `org-implementation` | Org Implementation & Change | Change management, readiness, capability building |
| `sme-training` | SME Training & Adoption | SME-specific training needs, barriers, adoption |
| `compliance` | Compliance & AI Act | EU AI Act Art. 4, regulatory literacy obligations |
| `k12-education` | K-12 Education | School curricula, children's AI literacy |
| `higher-education` | Higher Education | University courses, academic integrity, GenAI |
| `professional-education` | Professional & Executive Ed | Corporate training, micro-credentials, certification |
| `teacher-ai-literacy` | Teacher AI Literacy | Teacher training, educator attitudes |
| `critical-ai-literacy` | Critical & Ethical AI Literacy | Ethics, bias, misinformation, deepfakes |
| `generative-ai-skills` | Generative AI Skills | Prompting, LLM reliance, tool-task fit |
| `attitudes-trust` | Attitudes, Trust & Acceptance | Self-efficacy, TAM, AI anxiety, expectations |
| `adoption-behavior` | Adoption Behavior & Engagement | Usage patterns, personas, engagement |
| `program-evaluation` | Program Evaluation & Outcomes | Kirkpatrick-style outcomes, training effectiveness |
| `roi-measurement` | ROI & Business Impact | Productivity, firm performance, human capital ROI |
| `tooling` | Tools, Platforms & AI Tutors | LMS, chatbots, AI tutors, learning platforms |
| `lifelong-learning` | Lifelong & Self-Directed Learning | Continuous learning, learning agility, meta-skills |

## Research Aspects (8)

| ID | Aspect |
|----|--------|
| `theory` | Theory — frameworks, models, fundamentals |
| `mechanism` | Mechanism — why/how it works, drivers, dynamics |
| `method` | Method — techniques, processes, playbooks |
| `application` | Application — case studies, practice, deployment |
| `development` | Development — tools, software, implementation |
| `systems` | Systems & Technology — infrastructure, platforms |
| `evaluation` | Evaluation & Benchmarks — measurement, studies, KPIs |
| `review` | Reviews & Surveys — syntheses of the literature |

## Cell Notation

A cell is written `category/subcategory`, e.g. `assessment/evaluation`
(validated assessment instruments) or `org-implementation/development`
(implementation playbooks — a target gap). Gaps and momentum are tracked
per cell in `statistics.json` and `README.md`.

## Paper Format

Every paper in `papers.yaml` carries:

```yaml
- title: "AI Literacy: a five-stage developmental continuum"
  date: "2026-04"
  url: https://arxiv.org/abs/2606.00038
  category: ai-literacy-construct
  subcategory: theory
  authors: ["First Author", "Second Author"]
  abstract: "Short abstract..."
  venue: "Computers & Education"
```