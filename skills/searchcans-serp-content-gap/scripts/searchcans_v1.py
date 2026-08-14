#!/usr/bin/env python3
"""Minimal, dependency-free client for SearchCans API v1."""

from __future__ import annotations

import json
import os
import time
from collections.abc import Mapping
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

API_BASE = "https://www.searchcans.com/api/v1"
RETRYABLE_APP_CODES = {1001, 1002, 1003, 1004, 1005, 1006, 1009, 1010, 443, 10054}
RETRYABLE_HTTP_CODES = {429, 500, 502, 503, 504}
FATAL_HTTP_CODES = {400, 401, 402, 403}


class SearchCansError(RuntimeError):
    """Describe a failed SearchCans request without exposing credentials."""


def is_success_code(code: Any) -> bool:
    return code == 0 or code in {9999, -9999}


def api_key() -> str:
    key = os.environ.get("SEARCHCANS_API_KEY", "").strip()
    if not key:
        raise SearchCansError("Set SEARCHCANS_API_KEY before calling SearchCans.")
    return key


def post(endpoint: str, payload: dict[str, Any], timeout_seconds: int = 35, retries: int = 3) -> dict[str, Any]:
    raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    headers = {"Authorization": f"Bearer {api_key()}", "Content-Type": "application/json", "User-Agent": "searchcans-agent-skills/0.1"}
    last_error: Exception | None = None
    for attempt in range(retries):
        request = Request(f"{API_BASE}/{endpoint}", data=raw, headers=headers, method="POST")
        try:
            with urlopen(request, timeout=timeout_seconds) as response:
                body = json.loads(response.read().decode("utf-8", errors="replace"))
        except HTTPError as error:
            if error.code in FATAL_HTTP_CODES:
                raise SearchCansError(f"HTTP {error.code}: {error.read().decode('utf-8', errors='replace')[:500]}") from error
            last_error = error
            if error.code not in RETRYABLE_HTTP_CODES:
                raise SearchCansError(f"HTTP {error.code}") from error
        except (URLError, TimeoutError, json.JSONDecodeError) as error:
            last_error = error
        else:
            code = body.get("code")
            if is_success_code(code):
                return body
            if isinstance(code, int) and abs(code) in RETRYABLE_APP_CODES:
                last_error = SearchCansError(f"API code {code}: {body.get('msg', '')}")
            else:
                raise SearchCansError(f"API code {code}: {body.get('msg', '')}")
        if attempt < retries - 1:
            time.sleep(min(0.3 * (2**attempt), 2.0))
    raise SearchCansError(f"Request failed after {retries} attempts: {last_error}")


def normalize_organic(data: Any) -> list[dict[str, Any]]:
    raw_results = data.get("organic", []) if isinstance(data, Mapping) else data
    if not isinstance(raw_results, list):
        return []
    normalized: list[dict[str, Any]] = []
    for index, item in enumerate(raw_results, start=1):
        if not isinstance(item, Mapping):
            continue
        normalized.append({"position": item.get("position", index), "title": item.get("title", ""), "url": item.get("link") or item.get("url") or "", "snippet": item.get("snippet") or item.get("content") or "", "source": item.get("source", "")})
    return normalized
