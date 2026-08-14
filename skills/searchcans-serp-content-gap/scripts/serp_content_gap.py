#!/usr/bin/env python3
"""Collect a localized SERP evidence pack for a content-gap analysis."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from searchcans_v1 import normalize_organic, post


def domains(results: list[dict[str, Any]]) -> list[str]:
    return sorted({urlparse(str(result.get("url", ""))).netloc.lower() for result in results if result.get("url")})


def value(data: Any, name: str) -> Any:
    return data.get(name, []) if isinstance(data, dict) else []


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("keyword")
    parser.add_argument("--engine", choices=["google", "bing"], default="google")
    parser.add_argument("--country", default="us")
    parser.add_argument("--language", default="en")
    parser.add_argument("--page", type=int, default=1, help="Fetch pages 1 through N; do not combine with a specific SERP page.")
    parser.add_argument("--timeout-ms", type=int, default=30000)
    parser.add_argument("--client-timeout", type=int, default=35)
    parser.add_argument("--out", type=Path, help="Write the JSON evidence pack to this file.")
    args = parser.parse_args()
    if args.page < 1:
        parser.error("--page must be at least 1")

    payload = {
        "t": args.engine,
        "s": args.keyword,
        "country": args.country,
        "language": args.language,
        "page": args.page,
        "d": args.timeout_ms,
        "peopleAlsoAsk": True,
        "peopleAlsoSearchFor": True,
        "knowledgeGraph": True,
        "newsAggregation": True,
    }
    body = post("search", payload, timeout_seconds=args.client_timeout)
    data = body.get("data") or {}
    organic = normalize_organic(data)
    report = {
        "keyword": args.keyword,
        "market": {"engine": args.engine, "country": args.country, "language": args.language, "pages": args.page},
        "organic": organic,
        "competitor_domains": domains(organic),
        "people_also_ask": value(data, "peopleAlsoAsk"),
        "related_searches": value(data, "relatedSearches"),
        "knowledge_graph": data.get("knowledgeGraph") if isinstance(data, dict) else None,
        "top_stories": value(data, "topStories"),
    }
    encoded = json.dumps(report, ensure_ascii=False, indent=2)
    if args.out:
        args.out.write_text(encoded + "\n", encoding="utf-8")
    print(encoded)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
