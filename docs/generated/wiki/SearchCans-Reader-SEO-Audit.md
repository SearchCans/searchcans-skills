# SearchCans Reader SEO Audit

> An extraction report with observable canonical, H1, meta-description, JSON-LD, file, and screenshot signals

## Best for

Web-to-Markdown extraction, RAG input checks, dynamic pages, PDFs, Office files, and page-level SEO/GEO review.

## SearchCans APIs used

- Reader
- File Extraction
- Screenshot
- Account

## Account-aware behavior

Runs a pre-flight automatically for higher-cost proxy requests and keeps standard extraction lightweight.

## Use it

```text
Use $searchcans-reader-seo-audit to inspect this page for extraction and SEO-ready signals.
```

Read the executable [SKILL.md](https://github.com/SearchCans/searchcans-skills/tree/main/skills/searchcans-reader-seo-audit) for supported flags, evidence boundaries, and report guidance.

## Interpretation boundary

Extract a URL, PDF, or Office document with SearchCans Reader API and audit web-to-Markdown extractability plus SEO-ready HTML signals such as canonical URL, H1s, meta description, and JSON-LD. Use when diagnosing web-content extraction, preparing RAG inputs, checking dynamic pages, or reviewing a page's basic SEO/GEO implementation with cost-aware Reader settings.
