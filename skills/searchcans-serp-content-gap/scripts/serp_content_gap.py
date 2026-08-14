#!/usr/bin/env python3
"""Collect a localized SERP evidence pack for a content-gap analysis."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from searchcans_v1 import SearchCansError, normalize_organic, post, request_metadata


def domains(results: list[dict[str, Any]]) -> list[str]:
    return sorted({urlparse(str(result.get("url", ""))).netloc.lower() for result in results if result.get("url")})


def value(data: Any, name: str) -> Any:
    return data.get(name, []) if isinstance(data, dict) else []


def build_report(args: argparse.Namespace, body: dict[str, Any] | None = None, error: str | None = None) -> dict[str, Any]:
    request = (
        request_metadata(body)
        if body is not None
        else {
            "status": "failed",
            "api_code": None,
            "api_message": error or "Request failed.",
            "request_id": None,
            "attempts": None,
            "retry_count": None,
        }
    )
    data = body.get("data") or {} if body is not None else {}
    organic = normalize_organic(data)
    return {
        "status": request["status"],
        "request": request,
        "keyword": args.keyword,
        "market": {"engine": args.engine, "country": args.country, "language": args.language, "pages": args.page},
        "organic": organic,
        "competitor_domains": domains(organic),
        "people_also_ask": value(data, "peopleAlsoAsk"),
        "related_searches": value(data, "relatedSearches"),
        "knowledge_graph": data.get("knowledgeGraph") if isinstance(data, dict) else None,
        "top_stories": value(data, "topStories"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("keyword")
    parser.add_argument("--engine", choices=["google", "bing"], default="google")
    parser.add_argument("--country", default="us")
    parser.add_argument("--language", default="en")
    parser.add_argument("--page", type=int, default=1, help="Fetch pages 1 through N; do not combine with a specific SERP page.")
    parser.add_argument("--timeout-ms", type=int, default=30000)
    parser.add_argument("--client-timeout", type=int, default=35)
    parser.add_argument("--retries", type=int, default=2, help="Maximum attempts for transient API or transport errors (default: 2).")
    parser.add_argument("--out", type=Path, help="Write the JSON evidence pack to this file.")
    args = parser.parse_args()
    if args.page < 1:
        parser.error("--page must be at least 1")
    if args.retries < 1 or args.retries > 3:
        parser.error("--retries must be between 1 and 3")

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
    try:
        body = post("search", payload, timeout_seconds=args.client_timeout, retries=args.retries)
        report = build_report(args, body=body)
        exit_code = 0
    except SearchCansError as error:
        report = build_report(args, error=str(error))
        exit_code = 1
    encoded = json.dumps(report, ensure_ascii=False, indent=2)
    if args.out:
        args.out.write_text(encoded + "\n", encoding="utf-8")
    print(encoded)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
