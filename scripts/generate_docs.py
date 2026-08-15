#!/usr/bin/env python3
"""Generate SearchCans README, GitHub Wiki, and static documentation from one catalog."""

from __future__ import annotations

import argparse
import html
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "docs" / "skills.json"
WIKI_DIR = ROOT / "docs" / "generated" / "wiki"
SITE_DIR = ROOT / "docs" / "site"
START = "<!-- BEGIN GENERATED:SKILL-CATALOG -->"
END = "<!-- END GENERATED:SKILL-CATALOG -->"


def load_catalog() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    raw = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    if raw.get("schema_version") != 1 or not isinstance(raw.get("site"), dict) or not isinstance(raw.get("skills"), list):
        raise ValueError("docs/skills.json must use schema_version 1 with site and skills fields")
    skills = raw["skills"]
    names = [item.get("name") for item in skills if isinstance(item, dict)]
    required = {"name", "title", "category", "best_for", "delivers", "apis", "account_policy", "example"}
    if len(names) != len(set(names)) or any(not isinstance(name, str) for name in names):
        raise ValueError("Skill names must be unique strings")
    for item in skills:
        if not isinstance(item, dict) or required - set(item) or not isinstance(item["apis"], list):
            raise ValueError("Every catalog skill needs all required fields")
    return raw["site"], skills


def skill_metadata(name: str) -> dict[str, str]:
    path = ROOT / "skills" / name / "SKILL.md"
    if not path.is_file():
        raise ValueError(f"Catalog references missing skill: {name}")
    content = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
    if not match:
        raise ValueError(f"Missing frontmatter: {path}")
    fields = dict(re.findall(r"^(name|description):\s*(.+)$", match.group(1), re.MULTILINE))
    if fields.get("name") != name or not fields.get("description"):
        raise ValueError(f"Invalid name or description in {path}")
    return fields


def validate_catalog(skills: list[dict[str, Any]]) -> list[dict[str, Any]]:
    folders = {path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md")}
    catalog_names = {item["name"] for item in skills}
    if folders != catalog_names:
        missing, extra = sorted(folders - catalog_names), sorted(catalog_names - folders)
        raise ValueError(f"Catalog/skill mismatch; missing={missing}, extra={extra}")
    enriched: list[dict[str, Any]] = []
    for item in skills:
        metadata = skill_metadata(item["name"])
        enriched.append({**item, "description": metadata["description"], "wiki_page": f"{item['title'].replace(' ', '-')}.md"})
    return enriched


def markdown_catalog(skills: list[dict[str, Any]]) -> str:
    lines = ["| Skill | Best for | What the agent delivers |", "| --- | --- | --- |"]
    for item in skills:
        name, title = item["name"], item["title"]
        lines.append(f"| [`{name}`](skills/{name}/SKILL.md) | {item['best_for']} | {item['delivers']} |")
    return "\n".join(lines)


def replace_readme(catalog: str) -> str:
    path = ROOT / "README.md"
    current = path.read_text(encoding="utf-8")
    replacement = f"{START}\n{catalog}\n{END}"
    if START not in current or END not in current:
        raise ValueError("README.md is missing generated skill-catalog markers")
    return re.sub(re.escape(START) + r".*?" + re.escape(END), replacement, current, flags=re.DOTALL)


def wiki_home(skills: list[dict[str, Any]]) -> str:
    rows = ["| Need | Start with |", "| --- | --- |"]
    for item in skills:
        rows.append(f"| {item['best_for']} | [{item['title']}]({item['title'].replace(' ', '-')}) |")
    return "\n".join([
        "# SearchCans Agent Skills", "", "> Current, localized search evidence and clean web content for practical AI work.", "",
        "SearchCans Skills pair SERP discovery with Reader, File Extraction, Screenshot, and Account-aware controls. Every multi-request workflow keeps a bounded source scope and records what was actually retrieved.", "",
        "## Start in 60 seconds", "", "```bash", "npx skills add SearchCans/searchcans-skills", "```", "",
        "Install one skill instead:", "", "```bash", "npx skills add https://github.com/SearchCans/searchcans-skills --skill searchcans-deep-research", "```", "",
        "Set `SEARCHCANS_API_KEY` only in the execution environment. Never put a key in a prompt, report, source file, or Git commit.", "",
        "> **Weekly free credits:** Sign in, open [Dashboard → Free Redemption Codes](https://www.searchcans.com/dashboard/redeem-codes/), and claim the current code. A new code is released each week; each code adds **1,000 API credits** and may be redeemed once per account batch.", "",
        "## Choose a Skill", "", *rows, "",
        "## Documentation", "", "- [Getting Started](Getting-Started)", "- [Choose a Workflow](Choose-a-Workflow)", "- [Account-Aware Workflows](Account-Aware-Workflows)", "- [Deep Research Playbook](Deep-Research-Playbook)", "- [Troubleshooting](Troubleshooting)", "",
        "[View API documentation](https://www.searchcans.com/apis/) · [View source repository](https://github.com/SearchCans/searchcans-skills)"
    ]) + "\n"


def wiki_choose(skills: list[dict[str, Any]]) -> str:
    rows = ["| Goal | Skill | Why |", "| --- | --- | --- |"]
    for item in skills:
        rows.append(f"| {item['best_for']} | [{item['title']}]({item['title'].replace(' ', '-')}) | {item['delivers']} |")
    return "\n".join([
        "# Choose a Workflow", "", "Choose the smallest Skill that creates the evidence or artifact you need. Combine Skills only when one output becomes the next Skill's bounded input.", "", *rows, "",
        "## Selection rules", "", "- Use **Deep Research** when an answer needs multiple read sources, a 3–5 question plan, and a formal evidence gate.", "- Use **SERP Content Gap** for one localized keyword/SERP decision; use **Content Format Brief** when images and video formats are part of the decision.", "- Use **Reader SEO Audit** for one known URL or file; use **RAG Source Curator** to find and select a small source set first.", "- Use **Market Watch** for repeatable market/news snapshots; use **Product SERP Brief** for market-specific product and merchant observations.", "", "Do not treat SERP snippets or result appearance as proof. Read a page before using it for a consequential claim."
    ]) + "\n"


def wiki_account(skills: list[dict[str, Any]]) -> str:
    rows = ["| Skill | Default account-aware behavior |", "| --- | --- |"]
    rows.extend(f"| [{item['title']}]({item['title'].replace(' ', '-')}) | {item['account_policy']} |" for item in skills)
    return "\n".join([
        "# Account-Aware Workflows", "", "> Estimate scope, inspect safe account state once, then cap or stop before an oversized job begins.", "",
        "SearchCans multi-request Skills can use the Account API to estimate planned SERP and Reader/File costs, inspect remaining credits and Parallel Lanes, and choose a safe scope. Reports retain only sanitized budget fields; they never include account email, raw key data, or credentials.", "", "## Common controls", "", "- `--account-mode auto`: use the Skill's safe default policy.", "- `warn`: record an account warning without changing the requested scope.", "- `enforce`: block an insufficient job before business requests run.", "- `cap`: reduce supported variable scope when possible.", "- `off`: skip the pre-flight deliberately.", "", "Start at Reader proxy tier 0. Higher proxy tiers change expected cost and should follow an identified access issue, not be used as a default.", "", "## Skill behavior", "", *rows, "", "A capped run is still useful only within its effective scope. Always report requested versus effective sources/pages/formats, and never invent findings for skipped work."
    ]) + "\n"


def wiki_playbook() -> str:
    return """# Deep Research Playbook

> Use current web evidence to answer a defined question without confusing snippets with proof.

## Plan before searching

Write 3–5 distinct subquestions. Cover the central claim, primary evidence, alternatives, material objections, and decision implications. Set a country/language market, a source budget, and a freshness expectation.

## Search, select, and read

Search each subquestion, select a small domain-diverse source set, and read pages with Reader. Use only `claim_eligible_urls` from a successful extraction for consequential claims.

## Report honestly

Deliver the conclusion, supporting source URLs, conflicting evidence, uncertainty, methodology, and the requested versus effective budget. A result can be current without being comprehensive; say what was not checked.

Use [SearchCans Deep Research](SearchCans-Deep-Research) for the executable workflow.
"""


def wiki_troubleshooting() -> str:
    return """# Troubleshooting

Never include an API key, account email, token, or raw Account API body in an issue or screenshot.

## `SEARCHCANS_API_KEY` is missing

Set the key in the execution environment, then rerun the command. Do not add it to `SKILL.md`, JSON output, or a repository file.

## A job is `blocked` or `capped`

Read `account_guard`, requested limits, and effective limits. `blocked` means the selected policy stopped work before the business requests. `capped` means only the recorded effective scope was requested; do not draw conclusions about sources/pages/formats that were skipped.

## Reader extraction is `empty` or `error`

Treat the page as unread. Verify the URL, use `--headless` for a known JavaScript-rendered page, then consider a higher proxy tier only when justified. An empty Reader result is not evidence.

## Results differ by run or engine

SERPs are time- and locale-sensitive. Record query, country, language, engine, retrieval time, and limits. Compare snapshots as observations rather than as a ranking guarantee.

## Need help

Open an issue with the Skill name, sanitized status/request metadata, market, command flags excluding credentials, and expected versus observed behavior.
"""


def wiki_getting_started(skills: list[dict[str, Any]]) -> str:
    names = "\n".join(f"- [{item['title']}]({item['title'].replace(' ', '-')}) — {item['best_for']}" for item in skills)
    return f"""# Getting Started with SearchCans Agent Skills

SearchCans Skills turn current SERP observations and selected page extracts into bounded, traceable agent work.

## Install

```bash
npx skills add SearchCans/searchcans-skills
```

Install an individual Skill with `--skill <name>`. Set `SEARCHCANS_API_KEY` in your execution environment, not in source code or prompts.

## Available Skills

{names}

## Start responsibly

Use both `country` and `language` whenever the target market matters. Begin with the smallest source/result budget that can answer the question. Check output status before interpretation: `ok` is an observed result, `capped` is a partial result, `blocked` means no business requests ran, and `empty`/`error` Reader sources are not claim-ready.
"""


def wiki_skill(item: dict[str, Any]) -> str:
    api_list = "\n".join(f"- {api}" for api in item["apis"])
    return f"""# {item['title']}

> {item['delivers']}

## Best for

{item['best_for']}.

## SearchCans APIs used

{api_list}

## Account-aware behavior

{item['account_policy']}

## Use it

```text
{item['example']}
```

Read the executable [SKILL.md](https://github.com/SearchCans/searchcans-skills/tree/main/skills/{item['name']}) for supported flags, evidence boundaries, and report guidance.

## Interpretation boundary

{item['description']}
"""


def wiki_sidebar(skills: list[dict[str, Any]]) -> str:
    lines = ["## SearchCans Skills", "", "- [Home](Home)", "- [Getting Started](Getting-Started)", "- [Choose a Workflow](Choose-a-Workflow)", "- [Account-Aware Workflows](Account-Aware-Workflows)", "- [Deep Research Playbook](Deep-Research-Playbook)", "- [Troubleshooting](Troubleshooting)", "", "## Skills"]
    lines.extend(f"- [{item['title']}]({item['title'].replace(' ', '-')})" for item in skills)
    return "\n".join(lines) + "\n"


def html_shell(title: str, description: str, body: str) -> str:
    return f"""<!doctype html>
<html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><title>{html.escape(title)}</title><meta name=\"description\" content=\"{html.escape(description)}\"><style>body{{font-family:ui-sans-serif,system-ui,sans-serif;max-width:920px;margin:0 auto;padding:32px;color:#18212f;line-height:1.6}}a{{color:#1265d6}}header{{border-bottom:1px solid #dde3ea;margin-bottom:32px}}nav a{{margin-right:16px}}.tag{{display:inline-block;background:#edf5ff;border-radius:999px;padding:3px 10px;margin:3px;font-size:.86rem}}article{{border:1px solid #e4e8ed;border-radius:12px;padding:22px;margin:18px 0}}</style></head><body><header><h1><a href=\"/searchcans-skills/\">SearchCans Agent Skills</a></h1><nav><a href=\"/searchcans-skills/\">Home</a><a href=\"/searchcans-skills/skills/\">All Skills</a><a href=\"https://github.com/SearchCans/searchcans-skills\">GitHub</a></nav></header>{body}</body></html>\n"""


def site_index(site: dict[str, Any], skills: list[dict[str, Any]]) -> str:
    cards = "".join(f"<article><h2><a href=\"skills/{item['name']}/\">{html.escape(item['title'])}</a></h2><p>{html.escape(item['delivers'])}</p><p><strong>Best for:</strong> {html.escape(item['best_for'])}</p></article>" for item in skills)
    return html_shell(site["title"], site["description"], f"<main><p>{html.escape(site['description'])}</p><p>Install with <code>npx skills add SearchCans/searchcans-skills</code>.</p>{cards}</main>")


def site_skill(site: dict[str, Any], item: dict[str, Any]) -> str:
    tags = "".join(f"<span class=\"tag\">{html.escape(api)}</span>" for api in item["apis"])
    body = f"<main><h2>{html.escape(item['title'])}</h2><p>{html.escape(item['description'])}</p><h3>Best for</h3><p>{html.escape(item['best_for'])}</p><h3>What it delivers</h3><p>{html.escape(item['delivers'])}</p><h3>APIs</h3>{tags}<h3>Account-aware behavior</h3><p>{html.escape(item['account_policy'])}</p><p><a href=\"https://github.com/SearchCans/searchcans-skills/tree/main/skills/{item['name']}\">Open the Skill on GitHub</a></p></main>"
    return html_shell(item["title"], item["description"], body)


def outputs(site: dict[str, Any], skills: list[dict[str, Any]]) -> dict[Path, str]:
    files: dict[Path, str] = {ROOT / "README.md": replace_readme(markdown_catalog(skills))}
    wiki_pages = {
        "Home.md": wiki_home(skills), "Getting-Started.md": wiki_getting_started(skills), "Choose-a-Workflow.md": wiki_choose(skills),
        "Account-Aware-Workflows.md": wiki_account(skills), "Deep-Research-Playbook.md": wiki_playbook(), "Troubleshooting.md": wiki_troubleshooting(), "_Sidebar.md": wiki_sidebar(skills),
    }
    for item in skills:
        wiki_pages[item["wiki_page"]] = wiki_skill(item)
    wiki_pages[".searchcans-generated-pages"] = "\n".join(sorted(name for name in wiki_pages if name.endswith(".md"))) + "\n"
    files.update({WIKI_DIR / name: content for name, content in wiki_pages.items()})
    files[SITE_DIR / ".nojekyll"] = ""
    files[SITE_DIR / "index.html"] = site_index(site, skills)
    files[SITE_DIR / "skills" / "index.html"] = site_index(site, skills)
    for item in skills:
        files[SITE_DIR / "skills" / item["name"] / "index.html"] = site_skill(site, item)
    urls = ["https://searchcans.github.io/searchcans-skills/", "https://searchcans.github.io/searchcans-skills/skills/"] + [f"https://searchcans.github.io/searchcans-skills/skills/{item['name']}/" for item in skills]
    files[SITE_DIR / "sitemap.xml"] = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n" + "".join(f"  <url><loc>{url}</loc></url>\n" for url in urls) + "</urlset>\n"
    files[SITE_DIR / "robots.txt"] = "User-agent: *\nAllow: /\nSitemap: https://searchcans.github.io/searchcans-skills/sitemap.xml\n"
    return files


def write_files(files: dict[Path, str], check: bool) -> list[Path]:
    changed: list[Path] = []
    for path, content in files.items():
        existing = path.read_text(encoding="utf-8") if path.is_file() else None
        if existing != content:
            changed.append(path)
            if not check:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if generated files are stale.")
    args = parser.parse_args()
    site, catalog = load_catalog()
    skills = validate_catalog(catalog)
    changed = write_files(outputs(site, skills), args.check)
    if args.check and changed:
        print("Generated documentation is stale:")
        print("\n".join(str(path.relative_to(ROOT)) for path in changed))
        return 1
    print(f"Documentation {'is current' if args.check else 'generated'} for {len(skills)} Skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
