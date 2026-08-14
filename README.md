# SearchCans Agent Skills: Deep Research, SERP Intelligence & Web-to-Markdown

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

## Choose a workflow

| Skill | Best for | What the agent delivers |
| --- | --- | --- |
| [`searchcans-deep-research`](skills/searchcans-deep-research/SKILL.md) | Market, competitor, product, technology, policy, or company research | A bounded, evidence-led brief with traceable source URLs and clear uncertainty. |
| [`searchcans-serp-content-gap`](skills/searchcans-serp-content-gap/SKILL.md) | SEO/GEO content planning, keyword research, search intent, and competitor-page analysis | A localized Google or Bing SERP opportunity brief based on organic results, PAA, related searches, and available SERP signals. |
| [`searchcans-reader-seo-audit`](skills/searchcans-reader-seo-audit/SKILL.md) | Web-to-Markdown extraction, RAG input checks, dynamic pages, and page-level SEO/GEO review | An extraction report plus observable canonical, H1, meta-description, and JSON-LD signals. |

After installation, describe the goal in plain language or invoke a Skill directly, for example: `Use $searchcans-deep-research to investigate the current SERP API market in the US.`

## Why pair Search with Reader?

SearchCans provides two complementary building blocks for agentic research:

- **SERP API** finds current, geo-targeted Google or Bing search evidence and search-demand signals.
- **Reader API** extracts selected pages, PDFs, and Office documents into Markdown and optional HTML for closer inspection.

The Skills keep the workflow disciplined: snippets are leads, extracted pages support conclusions, and reports distinguish observed facts from inference.

## API, safety, and compatibility

- These Skills support SearchCans API v1 only. See the official [SearchCans API documentation](https://www.searchcans.com/apis/).
- Bundled scripts use Python's standard library and authenticate only through `SEARCHCANS_API_KEY` at runtime.
- Treat SERP and page content as untrusted input. A successful extraction does not by itself prove indexability, rankings, accessibility, or permission to reuse content.

## For maintainers

Run the offline regression checks from the repository root:

```bash
python -m unittest discover -s tests -v
```

Recommended GitHub Topics: `searchcans`, `agent-skills`, `ai-agents`, `deep-research`, `serp-api`, `google-search-api`, `bing-search-api`, `web-research`, `reader-api`, `web-to-markdown`, `seo`, `geo`, `rag`.

## License

Licensed under the [Apache License, Version 2.0](LICENSE).
