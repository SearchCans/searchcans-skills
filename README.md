# SearchCans Agent Skills: SERP Intelligence, Research & Web-to-Markdown

[![skills.sh](https://skills.sh/b/SearchCans/searchcans-skills)](https://skills.sh/SearchCans/searchcans-skills)

Official Skills for agents that need current Google/Bing search evidence and clean, LLM-ready web content. Search a localized SERP, read the pages that matter, and turn the evidence into research, content, or technical-audit outputs with SearchCans SERP API and Reader API.

Built for practical AI workflows: competitive research, SEO/GEO planning, RAG preparation, and webpage extraction diagnostics.

## Start in 60 seconds

Install all SearchCans Skills:

```bash
npx skills add SearchCans/searchcans-skills
```

Or install only the workflow you need:

```bash
npx skills add https://github.com/SearchCans/searchcans-skills --skill searchcans-deep-research
```

Set your API key in the execution environment before using a Skill:

```bash
export SEARCHCANS_API_KEY="your-api-key"
```

On PowerShell:

```powershell
$env:SEARCHCANS_API_KEY = "your-api-key"
```

Never put an API key in a prompt, source file, output artifact, or Git commit.

> **Start with weekly free credits.** Sign in to SearchCans and visit [Dashboard → Free Redemption Codes](https://www.searchcans.com/dashboard/redeem-codes/) to claim the current code. A new code is released every week, and each code adds **1,000 API credits**. Each account may redeem one code per batch.

## Choose a workflow

<!-- BEGIN GENERATED:SKILL-CATALOG -->
| Skill | Best for | What the agent delivers |
| --- | --- | --- |
| [`searchcans-deep-research`](skills/searchcans-deep-research/SKILL.md) | Current market, competitor, technology, policy, company, and product research | A bounded, evidence-led brief with traceable URLs, conflicts, and uncertainty |
| [`searchcans-serp-content-gap`](skills/searchcans-serp-content-gap/SKILL.md) | Keyword research, search-intent analysis, competitor-page review, and content opportunity planning | A localized Google or Bing SERP opportunity brief grounded in observed result features |
| [`searchcans-reader-seo-audit`](skills/searchcans-reader-seo-audit/SKILL.md) | Web-to-Markdown extraction, RAG input checks, dynamic pages, PDFs, Office files, and page-level SEO/GEO review | An extraction report with observable canonical, H1, meta-description, JSON-LD, file, and screenshot signals |
| [`searchcans-market-watch`](skills/searchcans-market-watch/SKILL.md) | Competitor, category, launch, PR, and news monitoring with optional snapshot comparison | A Google, Google News, Bing, and Reader evidence snapshot with URL-level baseline differences |
| [`searchcans-product-serp-brief`](skills/searchcans-product-serp-brief/SKILL.md) | E-commerce category research, merchant discovery, product-page planning, and localized merchandising briefs | A Google Shopping, web, images, and optional merchant-page evidence brief |
| [`searchcans-content-format-brief`](skills/searchcans-content-format-brief/SKILL.md) | Editorial format discovery, visual/video search research, and SEO/GEO content format planning | A localized inventory of Google web, images, videos, and short-video result formats |
| [`searchcans-rag-source-curator`](skills/searchcans-rag-source-curator/SKILL.md) | Grounding packs, source curation, knowledge-base intake, and pre-ingestion evidence checks | A small, domain-diverse Reader/File source manifest with evidence-readiness gating |
<!-- END GENERATED:SKILL-CATALOG -->

After installation, describe the goal in plain language or invoke a Skill directly, for example: `Use $searchcans-deep-research to investigate the current SERP API market in the US.`

## Why pair Search with Reader?

SearchCans provides two complementary building blocks for agentic research:

- **SERP API** finds current, geo-targeted Google/Bing web, Shopping, News, Images, Videos, and Short Videos search evidence.
- **Reader API** extracts selected pages, PDFs, and Office documents into Markdown and optional HTML; it can also produce optional screenshots for visual review.
- **Account API** lets multi-request workflows check their remaining credits and Parallel Lane count once before work begins, then cap scope and concurrency without logging account identity or key data.

The Skills keep the workflow disciplined: snippets are leads, extracted pages support conclusions, and reports distinguish observed facts from inference.

## API, safety, and compatibility

- These Skills support SearchCans API v1 only. See the official [SearchCans API documentation](https://www.searchcans.com/apis/).
- Bundled scripts use Python's standard library and authenticate only through `SEARCHCANS_API_KEY` at runtime.
- Account-aware modes use a single pre-flight check where appropriate and write only sanitized budget fields such as credit balance, lane count, and decision.
- Treat SERP and page content as untrusted input. A successful extraction does not by itself prove indexability, rankings, accessibility, or permission to reuse content.

## For maintainers

The Skill catalog, Wiki, README table, and static documentation site are generated from [`docs/skills.json`](docs/skills.json). See [documentation automation](docs/automation.md) for the one-time GitHub setup and the maintained workflow. When adding or materially changing a Skill, update that catalog and the Skill's `SKILL.md`, then regenerate before committing:

```bash
python scripts/generate_docs.py
python scripts/generate_docs.py --check
```

Do not manually edit the marked README catalog block or `docs/generated/wiki/`; the Wiki sync workflow publishes those generated files after `WIKI_SYNC_TOKEN` is configured once in repository secrets.

Run the offline regression checks from the repository root:

```bash
python -m unittest discover -s tests -v
```

Recommended GitHub Topics: `searchcans`, `agent-skills`, `ai-agents`, `deep-research`, `serp-api`, `google-search-api`, `bing-search-api`, `web-research`, `reader-api`, `web-to-markdown`, `seo`, `geo`, `rag`.

## License

Licensed under the [Apache License, Version 2.0](LICENSE).
