# Audit Interpretation

## Signal limits

- No returned HTML means canonical, H1, meta-description, and JSON-LD results are unavailable, not necessarily absent.
- Reader Markdown length measures extractability only. It does not measure content quality, traffic, or rankings.
- A canonical URL, H1, or JSON-LD item is an observed signal. Validate final implementation in the page source and relevant search tooling.

## Triage order

1. Resolve a failed or empty extraction before assessing content.
2. Use headless rendering only for JavaScript-dependent pages.
3. Start proxy escalation at tier 0 and stop at the first working tier.
4. Report invalid JSON-LD separately from missing JSON-LD.
5. Treat document extraction as a file-content check, not an HTML SEO audit.
