# SearchCans Agent Skills

Official, portable agent Skills for SearchCans SERP API and Reader API.

## Included Skills

- `searchcans-deep-research` — produce evidence-led research bundles from current web sources.
- `searchcans-serp-content-gap` — turn a localized SERP into a content opportunity brief.
- `searchcans-reader-page-audit` — inspect extractability and SEO-ready page signals.

## Install

```bash
npx skills add SearchCans/searchcans-skills
```

Each Skill requires an API key supplied at runtime through `SEARCHCANS_API_KEY`. Never add a key to a prompt, source file, output artifact, or Git commit.

## Development

The bundled scripts use Python's standard library. Run their offline tests with:

```bash
python -m unittest discover -s tests -v
```

API v1 is the only supported API version. See the official [SearchCans API documentation](https://www.searchcans.com/apis/).

## License

Licensed under the [Apache License, Version 2.0](LICENSE).
