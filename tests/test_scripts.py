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

    def test_extracts_page_signals(self) -> None:
        module = load_module("page_audit", "skills/searchcans-reader-page-audit/scripts/reader_page_audit.py")
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
