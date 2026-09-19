#!/usr/bin/env python3
"""Repair papers missing a `url` by looking them up on OpenAlex by title.

Writes the recovered url back into papers.yaml (in place). Only accepts
near-exact title matches. Reports any that stay unresolved.
"""
import re
import sys
import time
from pathlib import Path

import requests
import yaml

MAILTO = "tobias@tobias-weiss.org"
API = "https://api.openalex.org/works"


def norm(t):
    t = re.sub(r"<[^>]+>", " ", t or "")
    t = re.sub(r"[^a-z0-9]+", " ", t.lower())
    return re.sub(r"\s+", " ", t).strip()


def work_url(work):
    for loc in work.get("locations", []):
        src = (loc.get("source") or {}).get("id", "")
        lurl = loc.get("landing_page_url") or ""
        if "arxiv" in src or "arxiv" in lurl:
            m = re.search(r"arxiv\.org/abs/([^\s/]+)", lurl)
            if m:
                return "https://arxiv.org/abs/" + re.sub(r"v\d+$", "", m.group(1))
    primary = work.get("primary_location") or {}
    lurl = (primary.get("landing_page_url") or "").replace("http://", "https://")
    if lurl:
        return lurl
    doi = work.get("doi")
    return doi.replace("http://", "https://") if doi else ""


def lookup(title):
    q = norm(title)[:250]
    for attempt in range(5):
        try:
            r = requests.get(
                API, params={"search": q, "per-page": 5, "mailto": MAILTO}, timeout=30
            )
            if r.status_code == 429:
                wait = 15 * (attempt + 1)
                print(f"    rate-limited, wait {wait}s", flush=True)
                time.sleep(wait)
                continue
            r.raise_for_status()
            for w in r.json().get("results", []):
                t = w.get("title") or ""
                if t and norm(t) == q:
                    return work_url(w)
            return ""
        except Exception as e:
            print(f"    lookup error: {e}", flush=True)
            return ""
    return ""


def main():
    yaml_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("papers.yaml")
    with open(yaml_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    papers = data["papers"]

    missing = [p for p in papers if not p.get("url")]
    print(f"papers missing url: {len(missing)}", flush=True)
    fixed = 0
    for p in missing:
        u = lookup(p["title"])
        if u:
            p["url"] = u
            fixed += 1
            print(f"  FIXED: {p['title'][:55]} -> {u[:55]}", flush=True)
        else:
            print(f"  UNRESOLVED: {p['title'][:55]}", flush=True)
        time.sleep(1)

    with open(yaml_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    print(f"\nDone: fixed {fixed}/{len(missing)}", flush=True)


if __name__ == "__main__":
    main()
