# SearchCans RAG Source Curator

> A small, domain-diverse Reader/File source manifest with evidence-readiness gating

## Best for

Grounding packs, source curation, knowledge-base intake, and pre-ingestion evidence checks.

## SearchCans APIs used

- Google or Bing Search
- Reader
- File Extraction
- Screenshot
- Account

## Account-aware behavior

Checks search plus Reader/File source budget, caps selected sources, and limits workers to reported lanes.

## Use it

```text
Use $searchcans-rag-source-curator to curate sources for this RAG question.
```

Read the executable [SKILL.md](https://github.com/SearchCans/searchcans-skills/tree/main/skills/searchcans-rag-source-curator) for supported flags, evidence boundaries, and report guidance.

## Interpretation boundary

Build a small, diverse, evidence-ready RAG source manifest from localized Google or Bing results, Reader extracts, direct file extraction, and optional page screenshots. Use for grounding packs, source curation, knowledge-base intake, and pre-ingestion evidence checks.
