# Evidence Standard

## Research plan

- Define 3–5 subquestions before searching. Cover the main claim, alternatives, primary evidence, material objections, and decision implications.
- Use each subquestion as a bounded search path. Record it in `research_plan`; do not expand the question set without a decision reason.

## Source selection

- Prefer original documents, official documentation, filings, research publishers, and named subject-matter experts.
- Use independent reporting to corroborate important claims.
- Avoid treating search snippets, anonymous posts, SEO listicles, or vendor marketing as sole evidence.
- Preserve source title and URL. Record failed or empty Reader extraction rather than silently replacing it.

## Claim handling

- Support each consequential claim with a URL in `evidence_gate.claim_eligible_urls`. A Reader source is eligible only when its extraction status is `ok`.
- Treat SERP snippets as discovery leads, never claim support.
- Mark direct statements from a source as reported facts, not universal truth.
- Mark conclusions that combine multiple sources as inference.
- State the publication date or extraction date when freshness matters.
- Call out material disagreement, missing primary evidence, and scope limits.

## Budget handling

- Start with 3–5 searches and up to 5 Reader extractions.
- Expand only when the user asks for more coverage or unresolved contradictions justify it.
- Do not recursively crawl domains or exceed the requested source budget.

## Report method

- State the market, plan, executed queries, source budget, and actual extraction outcomes.
- Identify the source type for consequential evidence: primary, official documentation, filing, research publisher, independent reporting, or other.
- Keep failed or empty extractions in the methodology and source list; do not quietly replace them with unsupported claims.
