#!/usr/bin/env python3
"""Build a bounded SearchCans search-and-read research bundle."""

from __future__ import annotations

import argparse
import json
from collections import OrderedDict
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from searchcans_v1 import SearchCansError, normalize_organic, post


def is_http_url(value: str) -> bool:
    return urlparse(value).scheme in {"http", "https"} and bool(urlparse(value).netloc)


def select_sources(results: list[dict[str, Any]], maximum: int) -> list[dict[str, Any]]:
    """Prefer diverse domains while keeping the SERP order inside each domain."""
    by_domain: OrderedDict[str, list[dict[str, Any]]] = OrderedDict()
    for result in results:
        if not is_http_url(str(result.get("url", ""))):
            continue
        domain = urlparse(str(result["url"])).netloc.lower()
        by_domain.setdefault(domain, []).append(result)

    chosen: list[dict[str, Any]] = []
    while by_domain and len(chosen) < maximum:
        for domain in list(by_domain):
            chosen.append(by_domain[domain].pop(0))
            if not by_domain[domain]:
                del by_domain[domain]
            if len(chosen) == maximum:
                break
    return chosen


def search(query: str, args: argparse.Namespace) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "t": args.engine,
        "s": query,
        "d": args.timeout_ms,
        "country": args.country,
        "language": args.language,
        "peopleAlsoAsk": True,
        "knowledgeGraph": True,
        "newsAggregation": True,
    }
    body = post("search", payload, timeout_seconds=args.client_timeout)
    data = body.get("data") or {}
    return {
        "query": query,
        "organic": normalize_organic(data),
        "peopleAlsoAsk": data.get("peopleAlsoAsk", []) if isinstance(data, dict) else [],
        "relatedSearches": data.get("relatedSearches", []) if isinstance(data, dict) else [],
    }


def read(source: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    payload: dict[str, Any] = {"t": "url", "s": source["url"], "d": args.timeout_ms, "proxy": args.proxy}
    if args.headless:
        payload.update({"mode": 1, "w": args.wait_ms})
    try:
        body = post("url", payload, timeout_seconds=args.client_timeout)
        data = body.get("data") or {}
        return {
            "url": source["url"],
            "serp_title": source.get("title", ""),
            "title": data.get("title", ""),
            "description": data.get("description", ""),
            "markdown": data.get("markdown", ""),
            "status": "ok" if data.get("markdown") else "empty",
        }
    except SearchCansError as error:
        return {"url": source["url"], "serp_title": source.get("title", ""), "status": "error", "error": str(error)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("question")
    parser.add_argument("--query", action="append", default=[], help="Additional search query; repeat for a query matrix.")
    parser.add_argument("--engine", choices=["google", "bing"], default="google")
    parser.add_argument("--country", default="us")
    parser.add_argument("--language", default="en")
    parser.add_argument("--max-results-per-query", type=int, default=5)
    parser.add_argument("--max-sources", type=int, default=5)
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--wait-ms", type=int, default=3000)
    parser.add_argument("--proxy", type=int, choices=range(4), default=0)
    parser.add_argument("--timeout-ms", type=int, default=30000)
    parser.add_argument("--client-timeout", type=int, default=35)
    parser.add_argument("--out", type=Path, help="Write the complete JSON bundle to this file.")
    args = parser.parse_args()
    if args.max_results_per_query < 1 or args.max_sources < 1:
        parser.error("--max-results-per-query and --max-sources must be positive")

    queries = list(dict.fromkeys([args.question, *args.query]))
    searches = [search(query, args) for query in queries]
    all_results = [result for search_result in searches for result in search_result["organic"][: args.max_results_per_query]]
    bundle = {
        "question": args.question,
        "queries": queries,
        "searches": searches,
        "sources": [read(source, args) for source in select_sources(all_results, args.max_sources)],
        "limits": {"max_results_per_query": args.max_results_per_query, "max_sources": args.max_sources},
    }
    encoded = json.dumps(bundle, ensure_ascii=False, indent=2)
    if args.out:
        args.out.write_text(encoded + "\n", encoding="utf-8")
        print(
            json.dumps(
                {
                    "question": args.question,
                    "queries": queries,
                    "source_count": len(bundle["sources"]),
                    "output": str(args.out),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        print(encoded)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
