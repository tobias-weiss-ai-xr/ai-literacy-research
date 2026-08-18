#!/usr/bin/env python3
"""Bulk-fetch AI-literacy research papers from OpenAlex, one request per category.

Uses OpenAlex cursor pagination with a precise `title_and_abstract.search`
filter (AND semantics) and relevance sorting, so results are on-topic and
spread across the requested time window. Recommended for bootstrapping the
corpus.

Usage:
    python3 scripts/fetch/fetch_openalex_bulk.py --per-category 100 --months 36
"""

import argparse
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests
import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fetch_new_papers import ARXIV_ID_PATTERN, classify_subcategory, load_existing_papers  # noqa: E402

OPENALEX_API = "https://api.openalex.org/works"
MAILTO = os.environ.get("OPENALEX_MAILTO", "business@tobias-weiss.org")

# One main search term per taxonomy category
CATEGORY_TERMS = [
    # (category, [query variants]) — multiple search phrasings per category to tap
    # different literatures (education, HRM/org studies, HCI, regulation, economics).
    # Expanded 2026-08-12 after the saturation analysis: single queries had reached
    # their cursor ceiling; variants reach disjoint paper sets that dedupe against
    # the existing corpus. White-space categories (org-implementation,
    # program-evaluation, roi-measurement, assessment, compliance) get the most.
    ('ai-literacy-construct', [
        'AI literacy framework',
        'AI competency model',
        'AI competence dimensions',
        'artificial intelligence literacy construct',
        'AI literacy conceptualization',
    ]),
    ('ai-literacy-pedagogy', [
        'AI literacy education',
        'teaching artificial intelligence competence',
        'AI literacy instruction',
        'learning AI literacy pedagogy',
    ]),
    ('learning-design', [
        'AI curriculum design',
        'AI literacy curriculum development',
        'AI education course design',
        'AI training curriculum',
    ]),
    ('assessment', [
        'AI literacy assessment',
        'AI competence measurement instrument',
        'AI skills evaluation scale',
        'AI readiness assessment',
        'AI literacy test validation',
    ]),
    ('workforce-upskilling', [
        'AI upskilling workforce',
        'AI reskilling employees',
        'workforce AI skills training',
        'AI skilling program',
    ]),
    ('org-implementation', [
        'AI literacy implementation organization',
        'AI competence development organization',
        'AI capability building enterprise',
        'organizational AI training rollout',
        'workforce AI adoption program',
    ]),
    ('sme-training', [
        'AI training small and medium enterprises',
        'SME AI adoption skills',
        'AI literacy small business',
        'AI training for SMEs',
    ]),
    ('compliance', [
        'EU AI Act literacy',
        'AI Act compliance training',
        'AI regulation workforce skills',
        'artificial intelligence act obligations',
        'AI literacy regulatory requirement',
    ]),
    ('k12-education', [
        'AI literacy school education',
        'teaching AI in schools',
        'AI education secondary school',
        'AI literacy K-12 curriculum',
    ]),
    ('higher-education', [
        'AI literacy higher education',
        'AI competence university students',
        'AI literacy college education',
        'AI skills undergraduate',
    ]),
    ('professional-education', [
        'professional development AI skills',
        'AI continuing education professionals',
        'AI training professional development',
        'workplace AI professional learning',
    ]),
    ('teacher-ai-literacy', [
        'teacher AI literacy training',
        'teacher AI competence',
        'educator AI readiness',
        'pre-service teacher AI education',
    ]),
    ('critical-ai-literacy', [
        'critical AI literacy ethics',
        'AI critical thinking skills',
        'critical evaluation AI outputs',
        'AI ethics education literacy',
    ]),
    ('generative-ai-skills', [
        'generative AI skills prompting',
        'LLM prompting competence',
        'generative AI literacy',
        'prompt engineering skills',
    ]),
    ('attitudes-trust', [
        'AI self-efficacy acceptance',
        'attitudes toward artificial intelligence',
        'AI trust adoption intention',
        'AI anxiety acceptance',
    ]),
    ('adoption-behavior', [
        'AI adoption employee behavior',
        'employee AI usage intention',
        'AI acceptance technology workplace',
        'AI tool adoption workforce',
    ]),
    ('program-evaluation', [
        'training program evaluation AI',
        'AI training effectiveness evaluation',
        'AI upskilling program outcomes',
        'AI workforce training impact',
        'AI education program evaluation',
    ]),
    ('roi-measurement', [
        'AI training productivity firms',
        'AI upskilling return on investment',
        'AI training business performance',
        'AI skills economic impact',
        'AI training cost effectiveness',
    ]),
    ('tooling', [
        'AI tutor learning platform',
        'AI learning tool education',
        'intelligent tutoring system',
        'AI assistant training platform',
    ]),
    ('lifelong-learning', [
        'lifelong learning AI skills',
        'AI literacy lifelong learning',
        'continuous learning AI workplace',
        'adult education artificial intelligence',
    ]),
]


def sanitize_date(date_str):
    """Normalize a date to YYYY-MM, clamping future dates to today."""
    if not date_str:
        return ""
    y = date_str[:4]
    m = date_str[5:7] if len(date_str) >= 7 else "01"
    if not y.isdigit() or not m.isdigit():
        return ""
    now = datetime.now(timezone.utc)
    if (int(y), int(m)) > (now.year, now.month):
        return now.strftime("%Y-%m")
    return f"{y}-{m}"


def date_filter(months):
    cutoff = datetime.now(timezone.utc) - timedelta(days=months * 30)
    return cutoff.strftime("%Y-%m-%d")


def reconstruct_abstract(inverted):
    if not inverted:
        return ""
    pos = {}
    for word, positions in inverted.items():
        for p in positions:
            pos[p] = word
    return " ".join(pos[i] for i in sorted(pos))


def fetch_category(terms, months, per_category, sleep):
    """Cursor-paginated, relevance-sorted fetch for one category."""
    entries = []
    cursor = "*"
    search_filter = f"title_and_abstract.search:{terms}"
    while len(entries) < per_category and cursor:
        params = {
            "filter": (
                f"from_publication_date:{date_filter(months)},"
                f"{search_filter}"
            ),
            "per-page": 100,
            "mailto": MAILTO,
            "cursor": cursor,
        }
        data = None
        for attempt in range(4):
            try:
                resp = requests.get(OPENALEX_API, params=params, timeout=30)
                if resp.status_code == 429:
                    wait = 5 * (attempt + 1)
                    print(f"    rate-limited (429), waiting {wait}s...", flush=True)
                    time.sleep(wait)
                    continue
                resp.raise_for_status()
                data = resp.json()
                break
            except Exception as e:
                print(f"  WARNING: {e}", flush=True)
                break
        if not data:
            break
        results = data.get("results", [])
        cursor = data.get("meta", {}).get("next_cursor")
        if not results:
            break
        for work in results:
            title = work.get("title") or ""
            if not title:
                continue
            url = ""
            for loc in work.get("locations", []):
                src = (loc.get("source") or {}).get("id", "")
                lurl = loc.get("landing_page_url") or ""
                if "arxiv" in src or "arxiv" in lurl:
                    url = lurl.replace("http://", "https://")
                    url = re.sub(r"(arxiv\.org/abs/\d{4}\.\d{4,5})v\d+", r"\1", url)
                    break
            if not url:
                primary = work.get("primary_location") or {}
                url = (primary.get("landing_page_url") or "").replace("http://", "https://")
            if not url:
                url = work.get("doi") or ""
            if not url:
                continue
            mdoi = re.match(r"https?://doi\.org/10\.48550/arxiv\.(\d{4}\.\d{4,5})", url)
            if mdoi:
                url = "https://arxiv.org/abs/" + mdoi.group(1)
            date = sanitize_date(work.get("publication_date") or "")
            if not date:
                date = sanitize_date(str(work.get("publication_year") or ""))
            abstract = reconstruct_abstract(work.get("abstract_inverted_index"))
            entries.append(
                {
                    "title": title,
                    "date": date,
                    "url": url,
                    "category": None,
                    "subcategory": classify_subcategory(title, abstract),
                    "authors": [a.get("author", {}).get("display_name", "") for a in work.get("authorships", [])][:3],
                    "abstract": abstract[:200],
                    "venue": ((work.get("primary_location") or {}).get("source") or {}).get("display_name") or "",
                }
            )
        print(f"    page: {len(results)} results ({len(entries)} total)", flush=True)
        time.sleep(sleep)
    return entries


def append_papers(yaml_path, new_papers):
    if yaml_path.exists():
        with open(yaml_path, "r") as f:
            data = yaml.safe_load(f) or {}
    else:
        data = {}
    papers = data.get("papers", [])
    for entry in new_papers:
        papers.append(entry)
    data["papers"] = papers
    with open(yaml_path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


def main():
    parser = argparse.ArgumentParser(description="Bulk-fetch graph papers from OpenAlex per category")
    parser.add_argument("--months", type=int, default=36)
    parser.add_argument("--per-category", type=int, default=100)
    parser.add_argument("--sleep", type=float, default=5.0)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--categories", default=None, help="Comma-separated subset of category keys")

    parser.add_argument("--local", action="store_true", help="Run locally without modifying remote repos")
    args = parser.parse_args()

    yaml_path = Path(__file__).resolve().parent.parent.parent / "papers.yaml"
    by_id, titles_lower = load_existing_papers(yaml_path)
    print(f"Loaded {len(by_id)} existing papers", flush=True)

    if args.categories:
        wanted = {c.strip() for c in args.categories.split(",") if c.strip()}
        terms_list = [(c, t) for c, t in CATEGORY_TERMS if c in wanted]
    else:
        terms_list = CATEGORY_TERMS

    for cat, queries in terms_list:
        if isinstance(queries, str):
            queries = [queries]
        print(f"\n=== [{cat}] {len(queries)} query variants ===", flush=True)
        entries = []
        for q in queries:
            entries.extend(fetch_category(q, args.months, args.per_category, args.sleep))
        new = []
        for e in entries:
            m = ARXIV_ID_PATTERN.search(e["url"])
            key = m.group(1) if m else e["url"]
            if key and key in by_id:
                continue
            if any(e["url"] == x["url"] for x in new):
                continue
            t_lower = e["title"].lower().strip()
            if any(t_lower == t for t in titles_lower):
                continue
            e["category"] = cat
            new.append(e)
            by_id[key] = e
            titles_lower.append(t_lower)

        print(f"  {len(new)} new for {cat}", flush=True)
        if args.dry_run:
            continue
        append_papers(yaml_path, new)
        print(f"  saved ({len(by_id)} total)", flush=True)
        time.sleep(args.sleep * 2)

    print("\nDone.", flush=True)


if __name__ == "__main__":
    main()
