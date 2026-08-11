# Topic Planner — Example Workflow

This guide walks through turning the corpus into research priorities or a
ki-kompetenz-training.org article.

## 1. See what's hot

```bash
python3 tools/trend_scanner.py --months 12
```

Example output (illustrative):

```
🔥 TOP KEYWORD BURSTS
ai literacy      58 recent / 90 total  burst=2.9   ###########
prompt engineering  12 recent / 20 total  burst=2.7   #########
eu ai act         9 recent / 15 total  burst=2.7   #########
```

## 2. Get ranked topics

```bash
python3 tools/topic_planner.py --top 10
```

Writes `docs/topics/ARTICLE_TOPICS.md` with 10 evidence-ranked topics.

## 3. Build a brief for a guide

```bash
python3 tools/brief_generator.py "implementing AI literacy programs" --papers 5
```

Output:

```
📝 ARTICLE BRIEF: Implementing AI literacy programs
   Category: Org Implementation & Change
   Angle: Evidence-based guide to implementing AI literacy programs —
          synthesize the 5 most relevant papers into practical guidance.

Title candidates:
  - Implementing AI Literacy Programs: What the Research Says
  - How to Measure AI Literacy: The Evaluation Gap
  ...

Key papers:
  [2026-02] AI Maturity in SMEs: A Framework of Internal Capabilities  https://doi.org/...
  [2025-09] Artificial intelligence adoption and workplace training      https://doi.org/...
```

## 4. Feed the research program

Use the brief as the seed for a synthesis section in the implementation
guide (see `docs/research/RESEARCH_PLAN.md` and `PROTOCOL.md`).

## 5. Keep the corpus fresh

Weekly CI runs `fetch_new_papers.py --months 1 --create-pr` and opens a PR
with new papers. Review the taxonomy assignments, merge, and the topic list
regenerates automatically.