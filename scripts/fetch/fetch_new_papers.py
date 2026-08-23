#!/usr/bin/env python3
"""Discover AI-literacy research papers from the arXiv API across all 20 taxonomy categories.

Runs 160+ queries spanning AI-literacy constructs, pedagogy, assessment,
workforce upskilling, org implementation, compliance, education sectors,
program evaluation and all other categories in the taxonomy. Each query carries a category (and keyword-derived subcategory)
so new papers are auto-classified into the 20x8 taxonomy on discovery.

Usage:
    python3 scripts/fetch/fetch_new_papers.py --months 3 --dry-run
    python3 scripts/fetch/fetch_new_papers.py --months 1 --create-pr
"""

import argparse
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path

import requests
import yaml

ARXIV_ID_PATTERN = re.compile(r"(\d{4}\.\d{4,5})")
ARXIV_SEARCH_API = (
    "https://export.arxiv.org/api/query?search_query={}&start={}&max_results={}"
)

# (query, category, subcategory-hint). Subcategory is refined by keyword scoring
# on title/abstract; the hint is used as a fallback when nothing matches.
QUERIES = [
    ('abs:"AI literacy" AND abs:"framework"', 'ai-literacy-construct', 'theory'),
    ('abs:"AI literacy" AND abs:"model" AND abs:"competence"', 'ai-literacy-construct', 'theory'),
    ('abs:"AI competence framework"', 'ai-literacy-construct', 'theory'),
    ('abs:"AI literacy" AND abs:"definition"', 'ai-literacy-construct', 'theory'),
    ('abs:"AI literacy" AND abs:"dimension"', 'ai-literacy-construct', 'theory'),
    ('abs:"AI literacy" AND abs:"taxonomy"', 'ai-literacy-construct', 'theory'),
    ('abs:"AI literacy" AND abs:"continuum"', 'ai-literacy-construct', 'theory'),
    ('abs:"AI literacy" AND abs:"construct"', 'ai-literacy-construct', 'method'),
    ('abs:"AI literacy" AND abs:"teaching"', 'ai-literacy-pedagogy', 'method'),
    ('abs:"AI literacy" AND abs:"pedagogy"', 'ai-literacy-pedagogy', 'method'),
    ('abs:"AI literacy education"', 'ai-literacy-pedagogy', 'method'),
    ('abs:"AI literacy" AND abs:"course design"', 'ai-literacy-pedagogy', 'development'),
    ('abs:"AI education" AND abs:"pedagogy"', 'ai-literacy-pedagogy', 'method'),
    ('abs:"AI literacy" AND abs:"curriculum design"', 'ai-literacy-pedagogy', 'development'),
    ('abs:"vibe coding" AND abs:"learning"', 'ai-literacy-pedagogy', 'method'),
    ('abs:"AI literacy" AND abs:"intervention"', 'ai-literacy-pedagogy', 'evaluation'),
    ('abs:"instructional design" AND abs:"artificial intelligence"', 'learning-design', 'method'),
    ('abs:"learning design" AND abs:"AI"', 'learning-design', 'method'),
    ('abs:"AI" AND abs:"training design" AND abs:"adult"', 'learning-design', 'method'),
    ('abs:"workshop" AND abs:"AI literacy" AND abs:"outcome"', 'learning-design', 'evaluation'),
    ('abs:"generative AI" AND abs:"learning experience"', 'learning-design', 'application'),
    ('abs:"AI" AND abs:"micro-learning"', 'learning-design', 'method'),
    ('abs:"spaced" AND abs:"AI" AND abs:"training"', 'learning-design', 'method'),
    ('abs:"AI" AND abs:"active learning" AND abs:"training program"', 'learning-design', 'mechanism'),
    ('abs:"AI literacy" AND abs:"assessment"', 'assessment', 'method'),
    ('abs:"AI literacy" AND abs:"scale" AND abs:"measure"', 'assessment', 'method'),
    ('abs:"AI literacy" AND abs:"test" AND abs:"validity"', 'assessment', 'evaluation'),
    ('abs:"AI literacy" AND abs:"task-based"', 'assessment', 'method'),
    ('abs:"AI competency" AND abs:"evaluation"', 'assessment', 'evaluation'),
    ('abs:"AI literacy" AND abs:"self-assessment"', 'assessment', 'method'),
    ('abs:"AI literacy" AND abs:"instrument"', 'assessment', 'development'),
    ('abs:"AI literacy" AND abs:"psychometric"', 'assessment', 'evaluation'),
    ('abs:"AI" AND abs:"upskilling"', 'workforce-upskilling', 'method'),
    ('abs:"AI" AND abs:"reskilling"', 'workforce-upskilling', 'method'),
    ('abs:"AI training" AND abs:"workplace"', 'workforce-upskilling', 'application'),
    ('abs:"employees" AND abs:"AI skills"', 'workforce-upskilling', 'application'),
    ('abs:"AI" AND abs:"workforce development"', 'workforce-upskilling', 'method'),
    ('abs:"generative AI" AND abs:"worker" AND abs:"training"', 'workforce-upskilling', 'application'),
    ('abs:"future of work" AND abs:"skills" AND abs:"AI"', 'workforce-upskilling', 'mechanism'),
    ('abs:"AI" AND abs:"talent development"', 'workforce-upskilling', 'application'),
    ('abs:"AI literacy" AND abs:"organization"', 'org-implementation', 'mechanism'),
    ('abs:"AI adoption" AND abs:"training" AND abs:"firm"', 'org-implementation', 'application'),
    ('abs:"AI" AND abs:"implementation" AND abs:"change management"', 'org-implementation', 'method'),
    ('abs:"AI readiness" AND abs:"organization"', 'org-implementation', 'method'),
    ('abs:"AI" AND abs:"organizational learning"', 'org-implementation', 'mechanism'),
    ('abs:"AI literacy" AND abs:"enterprise"', 'org-implementation', 'application'),
    ('abs:"AI" AND abs:"capability building" AND abs:"firm"', 'org-implementation', 'method'),
    ('abs:"AI transformation" AND abs:"workforce"', 'org-implementation', 'mechanism'),
    ('abs:"AI" AND abs:"SME" AND abs:"training"', 'sme-training', 'application'),
    ('abs:"small and medium" AND abs:"digital skills"', 'sme-training', 'application'),
    ('abs:"SME" AND abs:"AI adoption" AND abs:"skills"', 'sme-training', 'mechanism'),
    ('abs:"small business" AND abs:"AI education"', 'sme-training', 'application'),
    ('abs:"SME" AND abs:"digital transformation" AND abs:"competence"', 'sme-training', 'application'),
    ('abs:"micro-enterprise" AND abs:"AI"', 'sme-training', 'application'),
    ('abs:"SME" AND abs:"training needs"', 'sme-training', 'method'),
    ('abs:"SME" AND abs:"AI" AND abs:"barriers"', 'sme-training', 'mechanism'),
    ('abs:"EU AI Act"', 'compliance', 'application'),
    ('abs:"EU AI Act" AND abs:"literacy"', 'compliance', 'application'),
    ('abs:"AI Act" AND abs:"Article 4"', 'compliance', 'application'),
    ('abs:"AI" AND abs:"regulation" AND abs:"training"', 'compliance', 'application'),
    ('abs:"AI literacy" AND abs:"compliance"', 'compliance', 'method'),
    ('abs:"EU AI Act" AND abs:"obligations"', 'compliance', 'theory'),
    ('abs:"AI Act" AND abs:"SME" AND abs:"compliance"', 'compliance', 'application'),
    ('abs:"AI literacy" AND abs:"policy"', 'compliance', 'theory'),
    ('abs:"AI literacy" AND abs:"school"', 'k12-education', 'application'),
    ('abs:"AI literacy" AND abs:"K-12"', 'k12-education', 'application'),
    ('abs:"AI education" AND abs:"primary school"', 'k12-education', 'application'),
    ('abs:"AI" AND abs:"secondary education"', 'k12-education', 'application'),
    ('abs:"children" AND abs:"AI literacy"', 'k12-education', 'application'),
    ('abs:"AI curriculum" AND abs:"school"', 'k12-education', 'development'),
    ('abs:"AI literacy" AND abs:"students" AND abs:"K-12"', 'k12-education', 'method'),
    ('abs:"design thinking" AND abs:"AI" AND abs:"school"', 'k12-education', 'method'),
    ('abs:"AI literacy" AND abs:"university"', 'higher-education', 'application'),
    ('abs:"AI literacy" AND abs:"higher education"', 'higher-education', 'application'),
    ('abs:"AI literacy" AND abs:"students" AND abs:"higher education"', 'higher-education', 'method'),
    ('abs:"generative AI" AND abs:"university" AND abs:"education"', 'higher-education', 'application'),
    ('abs:"AI literacy" AND abs:"college"', 'higher-education', 'application'),
    ('abs:"AI" AND abs:"undergraduate" AND abs:"literacy"', 'higher-education', 'method'),
    ('abs:"AI literacy" AND abs:"graduate"', 'higher-education', 'application'),
    ('abs:"AI" AND abs:"academic" AND abs:"integrity" AND abs:"generative"', 'higher-education', 'mechanism'),
    ('abs:"professional development" AND abs:"AI"', 'professional-education', 'method'),
    ('abs:"executive education" AND abs:"AI"', 'professional-education', 'application'),
    ('abs:"vocational" AND abs:"AI" AND abs:"skills"', 'professional-education', 'application'),
    ('abs:"continuing education" AND abs:"AI"', 'professional-education', 'application'),
    ('abs:"corporate training" AND abs:"AI"', 'professional-education', 'application'),
    ('abs:"lifelong learning" AND abs:"professionals" AND abs:"AI"', 'professional-education', 'mechanism'),
    ('abs:"micro-credentials" AND abs:"AI"', 'professional-education', 'development'),
    ('abs:"AI" AND abs:"certification"', 'professional-education', 'development'),
    ('abs:"teachers" AND abs:"AI literacy"', 'teacher-ai-literacy', 'method'),
    ('abs:"teacher training" AND abs:"AI"', 'teacher-ai-literacy', 'method'),
    ('abs:"educators" AND abs:"artificial intelligence"', 'teacher-ai-literacy', 'method'),
    ('abs:"teacher" AND abs:"generative AI"', 'teacher-ai-literacy', 'application'),
    ('abs:"teacher education" AND abs:"AI"', 'teacher-ai-literacy', 'method'),
    ('abs:"pre-service teachers" AND abs:"AI"', 'teacher-ai-literacy', 'evaluation'),
    ('abs:"in-service teachers" AND abs:"AI"', 'teacher-ai-literacy', 'evaluation'),
    ('abs:"teacher attitudes" AND abs:"AI"', 'teacher-ai-literacy', 'mechanism'),
    ('abs:"critical AI literacy"', 'critical-ai-literacy', 'theory'),
    ('abs:"AI literacy" AND abs:"ethics"', 'critical-ai-literacy', 'theory'),
    ('abs:"AI" AND abs:"critical thinking" AND abs:"education"', 'critical-ai-literacy', 'method'),
    ('abs:"AI" AND abs:"media literacy"', 'critical-ai-literacy', 'theory'),
    ('abs:"AI literacy" AND abs:"bias"', 'critical-ai-literacy', 'mechanism'),
    ('abs:"AI" AND abs:"misinformation" AND abs:"literacy"', 'critical-ai-literacy', 'mechanism'),
    ('abs:"AI" AND abs:"deepfake" AND abs:"literacy"', 'critical-ai-literacy', 'mechanism'),
    ('abs:"responsible AI" AND abs:"education"', 'critical-ai-literacy', 'method'),
    ('abs:"prompt engineering"', 'generative-ai-skills', 'method'),
    ('abs:"prompting" AND abs:"skills"', 'generative-ai-skills', 'method'),
    ('abs:"LLM" AND abs:"competence"', 'generative-ai-skills', 'mechanism'),
    ('abs:"generative AI" AND abs:"skills" AND abs:"workplace"', 'generative-ai-skills', 'application'),
    ('abs:"chatgpt" AND abs:"competence"', 'generative-ai-skills', 'mechanism'),
    ('abs:"generative AI literacy"', 'generative-ai-skills', 'theory'),
    ('abs:"AI tools" AND abs:"work tasks"', 'generative-ai-skills', 'application'),
    ('abs:"LLM reliance"', 'generative-ai-skills', 'mechanism'),
    ('abs:"AI" AND abs:"self-efficacy"', 'attitudes-trust', 'mechanism'),
    ('abs:"technology acceptance" AND abs:"AI"', 'attitudes-trust', 'mechanism'),
    ('abs:"AI acceptance" AND abs:"employees"', 'attitudes-trust', 'mechanism'),
    ('abs:"trust" AND abs:"AI" AND abs:"users"', 'attitudes-trust', 'mechanism'),
    ('abs:"attitudes toward AI"', 'attitudes-trust', 'mechanism'),
    ('abs:"AI anxiety"', 'attitudes-trust', 'mechanism'),
    ('abs:"AI" AND abs:"motivation" AND abs:"training"', 'attitudes-trust', 'mechanism'),
    ('abs:"expectation" AND abs:"AI adoption"', 'attitudes-trust', 'mechanism'),
    ('abs:"AI adoption" AND abs:"behavior"', 'adoption-behavior', 'mechanism'),
    ('abs:"AI usage" AND abs:"employees"', 'adoption-behavior', 'application'),
    ('abs:"AI" AND abs:"persona" AND abs:"adoption"', 'adoption-behavior', 'method'),
    ('abs:"AI" AND abs:"engagement" AND abs:"training"', 'adoption-behavior', 'evaluation'),
    ('abs:"generative AI" AND abs:"use patterns"', 'adoption-behavior', 'mechanism'),
    ('abs:"AI tool adoption" AND abs:"workers"', 'adoption-behavior', 'application'),
    ('abs:"digital literacy" AND abs:"AI" AND abs:"practice"', 'adoption-behavior', 'application'),
    ('abs:"AI" AND abs:"behavioral intention"', 'adoption-behavior', 'mechanism'),
    ('abs:"AI training" AND abs:"evaluation"', 'program-evaluation', 'evaluation'),
    ('abs:"training program" AND abs:"AI" AND abs:"outcomes"', 'program-evaluation', 'evaluation'),
    ('abs:"Kirkpatrick" AND abs:"technology training"', 'program-evaluation', 'method'),
    ('abs:"AI literacy program"', 'program-evaluation', 'evaluation'),
    ('abs:"AI upskilling" AND abs:"impact"', 'program-evaluation', 'evaluation'),
    ('abs:"training effectiveness" AND abs:"AI"', 'program-evaluation', 'evaluation'),
    ('abs:"AI course" AND abs:"learning outcomes"', 'program-evaluation', 'evaluation'),
    ('abs:"AI literacy" AND abs:"quasi-experiment"', 'program-evaluation', 'evaluation'),
    ('abs:"AI training" AND abs:"productivity"', 'roi-measurement', 'evaluation'),
    ('abs:"training" AND abs:"return on investment" AND abs:"technology"', 'roi-measurement', 'evaluation'),
    ('abs:"AI adoption" AND abs:"productivity" AND abs:"firm"', 'roi-measurement', 'evaluation'),
    ('abs:"training" AND abs:"firm performance" AND abs:"AI"', 'roi-measurement', 'evaluation'),
    ('abs:"human capital" AND abs:"AI" AND abs:"investment"', 'roi-measurement', 'theory'),
    ('abs:"AI" AND abs:"labor productivity"', 'roi-measurement', 'evaluation'),
    ('abs:"skills" AND abs:"wage" AND abs:"AI"', 'roi-measurement', 'evaluation'),
    ('abs:"training" AND abs:"innovation" AND abs:"firm"', 'roi-measurement', 'evaluation'),
    ('abs:"AI tutor"', 'tooling', 'development'),
    ('abs:"intelligent tutoring" AND abs:"AI literacy"', 'tooling', 'development'),
    ('abs:"chatbot" AND abs:"AI education"', 'tooling', 'development'),
    ('abs:"AI learning companion"', 'tooling', 'development'),
    ('abs:"AI" AND abs:"learning platform" AND abs:"training"', 'tooling', 'systems'),
    ('abs:"AI" AND abs:"LMS"', 'tooling', 'systems'),
    ('abs:"AI-powered" AND abs:"learning tools"', 'tooling', 'development'),
    ('abs:"generative AI" AND abs:"tutoring"', 'tooling', 'development'),
    ('abs:"lifelong learning" AND abs:"AI"', 'lifelong-learning', 'theory'),
    ('abs:"self-directed learning" AND abs:"AI"', 'lifelong-learning', 'method'),
    ('abs:"learning to learn" AND abs:"technology"', 'lifelong-learning', 'theory'),
    ('abs:"continuous learning" AND abs:"AI skills"', 'lifelong-learning', 'method'),
    ('abs:"future of work" AND abs:"learning" AND abs:"AI"', 'lifelong-learning', 'mechanism'),
    ('abs:"learning agility" AND abs:"AI"', 'lifelong-learning', 'mechanism'),
    ('abs:"AI" AND abs:"learning culture"', 'lifelong-learning', 'mechanism'),
    ('abs:"digital transformation" AND abs:"learning organization"', 'lifelong-learning', 'mechanism'),
    ('abs:"AI literacy" AND abs:"review"', 'ai-literacy-construct', 'review'),
    ('abs:"AI literacy" AND abs:"survey"', 'ai-literacy-construct', 'review'),
    ('abs:"AI literacy" AND abs:"systematic review"', 'ai-literacy-construct', 'review'),
    ('abs:"AI literacy" AND abs:"meta-analysis"', 'ai-literacy-construct', 'review'),
    ('abs:"AI" AND abs:"upskilling" AND abs:"review"', 'workforce-upskilling', 'review'),
    ('abs:"AI" AND abs:"training" AND abs:"systematic review"', 'program-evaluation', 'review'),
    ('abs:"AI literacy" AND abs:"measurement" AND abs:"review"', 'assessment', 'review'),
    ('abs:"generative AI" AND abs:"higher education" AND abs:"review"', 'higher-education', 'review'),
    ('abs:"AI in education" AND abs:"review"', 'ai-literacy-pedagogy', 'review'),
    ('abs:"EU AI Act" AND abs:"review"', 'compliance', 'review'),
    ('abs:"prompt engineering" AND abs:"survey"', 'generative-ai-skills', 'review'),
    ('abs:"technology acceptance" AND abs:"AI" AND abs:"review"', 'attitudes-trust', 'review'),
    ('abs:"AI" AND abs:"SME" AND abs:"review"', 'sme-training', 'review'),
    ('abs:"teachers" AND abs:"AI" AND abs:"review"', 'teacher-ai-literacy', 'review'),
    ('abs:"AI literacy" AND abs:"K-12" AND abs:"review"', 'k12-education', 'review'),
    ('abs:"workforce" AND abs:"AI" AND abs:"review"', 'workforce-upskilling', 'review'),
]

# Subcategory keyword rules, applied in order. First match wins.
# Each rule: (subcategory, keywords, title_only?) — title_only restricts
# matching to the paper title (for strong signals like "survey").
SUBCATEGORY_RULES = [
    ("review", ["survey", "systematic review", "state-of-the-art", "sota", "overview of"], True),
    ("review", ["a survey of", "review of", "bibliographic review"], False),
    ("theory", ["expressivity", "expressiveness", "theoretical", "complexity of", "bounds", "fundamental limits", "axiomat", "computational complexity", "approximation guarantees"], False),
    ("application", ["application to", "application of", "case study", "real-world", "in practice", "production", "clinical", "medical", "fraud detection", "drug discovery", "recommender", "supply chain", "bioinformatics", "proteomics", "genomics", "diagnosis", "osint", "cybersecurity", "deployment"], False),
    ("development", ["open-source", "library", "toolkit", "implementation of", "software package", "benchmarking tool", "api for", "python library"], False),
    ("mechanism", ["interpretab", "explainab", "understanding why", "analysis of", "inner workings", "attention analysis", "probing", "mechanism", "why graph"], False),
    ("systems", ["system", "engine", "platform", "infrastructure", "architecture", "pipeline", "distributed", "scalable", "indexing", "storage", "gpu", "parallel"], False),
    ("evaluation", ["benchmark", "empirical study", "empirical comparison", "experimental evaluation", "evaluating", "comparative analysis", "dataset"], False),
]

SUBCATEGORY_FALLBACK = "method"


def classify_subcategory(title, abstract):
    """Assign a subcategory using keyword rules against title + abstract."""
    t_lower = title.lower()
    text = f"{title} {abstract}".lower()
    for subcat, keywords, title_only in SUBCATEGORY_RULES:
        haystack = t_lower if title_only else text
        for kw in keywords:
            if kw in haystack:
                return subcat
    return SUBCATEGORY_FALLBACK


def load_existing_papers(yaml_path):
    if not yaml_path.exists():
        return {}, []
    with open(yaml_path, "r") as f:
        data = yaml.safe_load(f) or {}
    papers = data.get("papers", [])
    by_id = {}
    titles_lower = []
    for p in papers:
        url = p.get("url", "")
        match = ARXIV_ID_PATTERN.search(url)
        if match:
            by_id[match.group(1)] = p
        titles_lower.append(p.get("title", "").lower().strip())
    return by_id, titles_lower


def search_arxiv(query, months, start=0, max_results=100, max_retries=4):
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    cutoff = now - timedelta(days=months * 30)
    date_start = cutoff.strftime("%Y%m%d0000")
    date_end = now.strftime("%Y%m%d") + "2359"

    full_query = f"({query}) AND submittedDate:[{date_start} TO {date_end}]"
    try:
        resp = None
        for attempt in range(max_retries):
            resp = requests.get(
                ARXIV_SEARCH_API.format(
                    requests.utils.quote(full_query), start, max_results
                ),
                timeout=30,
            )
            if resp.status_code == 429:
                wait = 8 * (attempt + 1)
                print(f"    rate-limited (429), waiting {wait}s...", flush=True)
                time.sleep(wait)
                continue
            resp.raise_for_status()
            break
        if resp is None:
            return []
        if resp.status_code != 200:
            print(f"  WARNING: arXiv returned HTTP {resp.status_code}", flush=True)
            return []
        entries = []
        root = resp.text
        for match in re.finditer(r"<entry>(.*?)</entry>", root, re.DOTALL):
            entry_xml = match.group(1)
            entry = {}
            title_m = re.search(r"<title>(.*?)</title>", entry_xml, re.DOTALL)
            if title_m:
                entry["title"] = re.sub(r"\s+", " ", title_m.group(1).strip())
            id_m = re.search(r"<id>(.*?)</id>", entry_xml)
            if id_m:
                entry["url"] = id_m.group(1).strip().replace("http://", "https://")
            published_m = re.search(r"<published>(.*?)</published>", entry_xml)
            if published_m:
                entry["date"] = published_m.group(1).strip()[:7]
            summary_m = re.search(r"<summary>(.*?)</summary>", entry_xml, re.DOTALL)
            if summary_m:
                entry["abstract"] = re.sub(r"\s+", " ", summary_m.group(1).strip())
            authors_m = re.findall(r"<name>(.*?)</name>", entry_xml)
            if authors_m:
                entry["authors"] = [a.strip() for a in authors_m][:3]
            if entry.get("title") and entry.get("url"):
                entries.append(entry)
        return entries
    except Exception as e:
        print(f"  WARNING: arXiv search error: {e}", flush=True)
        return []


def format_yaml_entry(entry, category, subcategory):
    title = entry["title"].replace('"', '\\"')
    authors = ", ".join(entry.get("authors", [])[:3])
    lines = [
        f'  - title: "{title}"',
        f'    date: "{entry.get("date", "")}"',
        f'    url: "{entry.get("url", "")}"',
        f"    category: {category}",
        f"    subcategory: {subcategory}",
        f"    authors: [{authors}]",
    ]
    if entry.get("abstract"):
        abstract = entry["abstract"][:200].replace('"', '\\"')
        lines.append(f'    abstract: "{abstract}..."')
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Discover AI-literacy research papers from arXiv"
    )
    parser.add_argument(
        "--months",
        type=int,
        default=3,
        help="Search papers from the last N months (default: 3)",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Preview without creating anything"
    )
    parser.add_argument(
        "--create-pr", action="store_true", help="Create a GitHub PR with new papers"
    )
    parser.add_argument(
        "--sleep", type=float, default=2.0, help="Seconds between queries"
    )
    parser.add_argument(
        "--max-results",
        type=int,
        default=100,
        help="Max results per arXiv query (default: 100)",
    )
    parser.add_argument(
        "--from",
        dest="from_idx",
        type=int,
        default=0,
        help="Start at query index (0-based, inclusive)",
    )
    parser.add_argument(
        "--to",
        dest="to_idx",
        type=int,
        default=None,
        help="Stop at query index (0-based, inclusive)",
    )
    args = parser.parse_args()

    yaml_path = Path(__file__).resolve().parent.parent.parent / "papers.yaml"
    by_id, titles_lower = load_existing_papers(yaml_path)

    print(f"Loaded {len(by_id)} existing papers from papers.yaml", flush=True)
    print(
        f"Searching arXiv ({len(QUERIES)} queries) for papers from the last {args.months} month(s)...",
        flush=True,
    )

    all_new = []
    CHECKPOINT_EVERY = 10
    to_idx = args.to_idx if args.to_idx is not None else len(QUERIES) - 1
    for qi, qdef in enumerate(QUERIES[args.from_idx:to_idx + 1], start=args.from_idx):
        if len(qdef) == 4:
            query, category, hint, force_sub = qdef
        else:
            query, category, hint = qdef
            force_sub = None
        print(f"Query {qi + 1}/{len(QUERIES)} [{category}] {query[:70]}", flush=True)
        entries = search_arxiv(query, args.months, max_results=args.max_results)
        for entry in entries:
            arxiv_id_match = ARXIV_ID_PATTERN.search(entry.get("url", ""))
            arxiv_id = arxiv_id_match.group(1) if arxiv_id_match else None

            if arxiv_id and arxiv_id in by_id:
                continue

            title_lower = entry.get("title", "").lower().strip()
            if any(title_lower == t for t in titles_lower):
                continue

            if arxiv_id and any(e.get("url", "") == entry["url"] for e in all_new):
                continue

            entry["category"] = category
            entry["subcategory"] = force_sub or classify_subcategory(
                entry.get("title", ""), entry.get("abstract", "")
            )
            all_new.append(entry)
            by_id[arxiv_id] = entry
            titles_lower.append(title_lower)

        # Incremental checkpoint so partial runs are never lost
        if not args.dry_run and all_new and (qi + 1) % CHECKPOINT_EVERY == 0:
            append_papers(yaml_path, all_new)
            print(f"  [checkpoint] saved {len(all_new)} papers so far", flush=True)
            all_new = []
            by_id, titles_lower = load_existing_papers(yaml_path)

        time.sleep(args.sleep)

    print(
        f"\nFound {len(all_new)} new papers ({len(by_id)} already in list)", flush=True
    )

    if not all_new:
        print("No new papers to add.", flush=True)
        return

    print("\n--- New Papers (first 10) ---", flush=True)
    for entry in all_new[:10]:
        print(format_yaml_entry(entry, entry["category"], entry["subcategory"]), flush=True)
        print(flush=True)
    print(f"... and {max(0, len(all_new) - 10)} more", flush=True)

    if args.dry_run:
        print("\nDry run complete — no files modified", flush=True)
        return

    if args.create_pr:
        branch_name = f"add-new-papers-{datetime.now().strftime('%Y%m%d')}"
        print(f"\nCreating branch '{branch_name}' and PR...", flush=True)
        try:
            subprocess.run(
                ["git", "checkout", "-b", branch_name], check=True, cwd=yaml_path.parent
            )
            append_papers(yaml_path, all_new)
            subprocess.run(["git", "add", "papers.yaml"], check=True, cwd=yaml_path.parent)
            subprocess.run(
                ["git", "commit", "-m", f"Add {len(all_new)} new papers from arXiv discovery"],
                check=True,
                cwd=yaml_path.parent,
            )
            subprocess.run(
                ["git", "push", "origin", branch_name], check=True, cwd=yaml_path.parent
            )
            subprocess.run(
                [
                    "gh", "pr", "create",
                    "--title", f"Add {len(all_new)} new papers from arXiv discovery",
                    "--body", "Automatically discovered papers.\n\n**Please review taxonomy assignments.**",
                ],
                check=True,
                cwd=yaml_path.parent,
            )
            print("PR created successfully!", flush=True)
        except subprocess.CalledProcessError as e:
            print(f"ERROR: Failed to create PR: {e}", flush=True)
            sys.exit(1)
    else:
        append_papers(yaml_path, all_new)
        print(f"\nAppended {len(all_new)} papers to papers.yaml", flush=True)
        print(
            "\nNext: run scripts/analysis/generate_analysis.py and scripts/generate_readme.py",
            flush=True,
        )


def append_papers(yaml_path, new_papers):
    """Append new papers to papers.yaml in stable format."""
    if yaml_path.exists():
        with open(yaml_path, "r") as f:
            data = yaml.safe_load(f) or {}
    else:
        data = {}
    papers = data.get("papers", [])
    for entry in new_papers:
        papers.append(
            {
                "title": entry.get("title", ""),
                "date": entry.get("date", ""),
                "url": entry.get("url", ""),
                "category": entry.get("category", ""),
                "subcategory": entry.get("subcategory", ""),
                "authors": entry.get("authors", []),
                "abstract": entry.get("abstract", ""),
            }
        )
    data["papers"] = papers
    with open(yaml_path, "w") as f:
        yaml.dump(
            data, f, default_flow_style=False, allow_unicode=True, sort_keys=False
        )


if __name__ == "__main__":
    main()
