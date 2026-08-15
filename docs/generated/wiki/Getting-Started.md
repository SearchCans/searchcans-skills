# Getting Started with SearchCans Agent Skills

SearchCans Skills turn current SERP observations and selected page extracts into bounded, traceable agent work.

## Install

```bash
npx skills add SearchCans/searchcans-skills
```

Install an individual Skill with `--skill <name>`. Set `SEARCHCANS_API_KEY` in your execution environment, not in source code or prompts.

## Available Skills

- [SearchCans Deep Research](SearchCans-Deep-Research) — Current market, competitor, technology, policy, company, and product research
- [SearchCans SERP Content Gap](SearchCans-SERP-Content-Gap) — Keyword research, search-intent analysis, competitor-page review, and content opportunity planning
- [SearchCans Reader SEO Audit](SearchCans-Reader-SEO-Audit) — Web-to-Markdown extraction, RAG input checks, dynamic pages, PDFs, Office files, and page-level SEO/GEO review
- [SearchCans Market Watch](SearchCans-Market-Watch) — Competitor, category, launch, PR, and news monitoring with optional snapshot comparison
- [SearchCans Product SERP Brief](SearchCans-Product-SERP-Brief) — E-commerce category research, merchant discovery, product-page planning, and localized merchandising briefs
- [SearchCans Content Format Brief](SearchCans-Content-Format-Brief) — Editorial format discovery, visual/video search research, and SEO/GEO content format planning
- [SearchCans RAG Source Curator](SearchCans-RAG-Source-Curator) — Grounding packs, source curation, knowledge-base intake, and pre-ingestion evidence checks

## Start responsibly

Use both `country` and `language` whenever the target market matters. Begin with the smallest source/result budget that can answer the question. Check output status before interpretation: `ok` is an observed result, `capped` is a partial result, `blocked` means no business requests ran, and `empty`/`error` Reader sources are not claim-ready.
