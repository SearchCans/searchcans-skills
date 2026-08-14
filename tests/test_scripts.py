from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, relative_path: str):
    path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(path.parent))
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path.pop(0)
    return module


class SearchCansScriptTests(unittest.TestCase):
    def test_normalizes_current_and_compatibility_serp_shapes(self) -> None:
        module = load_module("deep_client", "skills/searchcans-deep-research/scripts/searchcans_v1.py")
        current = module.normalize_organic({"organic": [{"position": 2, "title": "Current", "link": "https://example.com", "snippet": "Text"}]})
        compatibility = module.normalize_organic([{"title": "Legacy", "url": "https://legacy.example", "content": "Body"}])
        self.assertEqual(current[0]["url"], "https://example.com")
        self.assertEqual(current[0]["snippet"], "Text")
        self.assertEqual(compatibility[0]["url"], "https://legacy.example")
        self.assertEqual(compatibility[0]["snippet"], "Body")
        self.assertTrue(module.is_success_code(-9999))

    def test_content_gap_labels_no_results_and_preserves_request_metadata(self) -> None:
        module = load_module("content_gap_client", "skills/searchcans-serp-content-gap/scripts/searchcans_v1.py")
        body = module.with_request_metadata({"code": -9999, "msg": "No results", "data": {}}, attempts=1)
        metadata = module.request_metadata(body)
        self.assertEqual(metadata["status"], "no_results")
        self.assertEqual(metadata["api_code"], -9999)
        self.assertEqual(metadata["attempts"], 1)
        self.assertEqual(metadata["retry_count"], 0)

    def test_content_gap_retries_only_transient_api_errors(self) -> None:
        module = load_module("content_gap_retry_client", "skills/searchcans-serp-content-gap/scripts/searchcans_v1.py")

        class Response:
            def __init__(self, body: dict[str, object]) -> None:
                self.body = body

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, traceback) -> bool:
                return False

            def read(self) -> bytes:
                import json

                return json.dumps(self.body).encode("utf-8")

        responses = iter([Response({"code": 1001, "msg": "Timeout"}), Response({"code": 0, "data": {}})])
        delays: list[float] = []
        original_urlopen = module.urlopen
        original_sleep = module.time.sleep
        original_api_key = module.api_key
        module.urlopen = lambda *args, **kwargs: next(responses)
        module.time.sleep = lambda delay: delays.append(delay)
        module.api_key = lambda: "test-key"
        try:
            body = module.post("search", {"t": "google", "s": "test"}, retries=2)
        finally:
            module.urlopen = original_urlopen
            module.time.sleep = original_sleep
            module.api_key = original_api_key

        self.assertEqual(body["_searchcans_client"]["status"], "ok")
        self.assertEqual(body["_searchcans_client"]["attempts"], 2)
        self.assertEqual(body["_searchcans_client"]["retry_count"], 1)
        self.assertEqual(delays, [0.3])

    def test_deep_research_evidence_gate_excludes_unread_sources(self) -> None:
        module = load_module("deep_research", "skills/searchcans-deep-research/scripts/deep_research.py")
        gate = module.evidence_gate(
            [
                {"url": "https://evidence.example", "status": "ok", "claim_ready": True},
                {"url": "https://empty.example", "status": "empty", "claim_ready": False},
            ]
        )
        self.assertEqual(gate["claim_eligible_urls"], ["https://evidence.example"])
        self.assertEqual(gate["ineligible_sources"], [{"url": "https://empty.example", "status": "empty"}])

    def test_extracts_page_signals(self) -> None:
        module = load_module("seo_audit", "skills/searchcans-reader-seo-audit/scripts/reader_page_audit.py")
        parser = module.PageSignalsParser()
        parser.feed("<link rel='canonical' href='https://example.com/canonical'><meta name='description' content='Summary'><h1> One heading </h1><script type='application/ld+json'>{\"@type\":\"Article\"}</script>")
        parser.close()
        self.assertEqual(parser.canonical, "https://example.com/canonical")
        self.assertEqual(parser.meta_description, "Summary")
        self.assertEqual(parser.h1s, ["One heading"])
        self.assertEqual(parser.jsonld_count, 1)
        self.assertEqual(parser.jsonld_invalid, 0)


if __name__ == "__main__":
    unittest.main()
