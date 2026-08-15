# SearchCans Documentation Automation

`docs/skills.json` is the catalog source for every public English Skill. The generator validates that it covers every `skills/*/SKILL.md`, then updates the README catalog, generated Wiki pages, static HTML documentation, and sitemap.

## Add or change a Skill

1. Create or update `skills/<name>/SKILL.md` and its executable resources.
2. Add or update the matching entry in `docs/skills.json`.
3. Run `python scripts/generate_docs.py`.
4. Run `python scripts/generate_docs.py --check` and `python -m unittest discover -s tests -v`.
5. Commit the Skill, catalog, and generated output together.

Do not manually edit `docs/generated/wiki/` or the generated README catalog block. Any manual change will be replaced on the next generation run.

## One-time GitHub configuration

1. In repository **Settings → Pages**, choose **GitHub Actions** as the publishing source. The `publish-docs.yml` workflow will publish `docs/site/` on future qualifying pushes.
2. Create a dedicated automation credential that can push to `https://github.com/SearchCans/searchcans-skills.wiki.git`. Store it as the repository Actions secret `WIKI_SYNC_TOKEN`.
3. The `sync-wiki.yml` workflow runs only on `main` documentation/Skill changes or from **Actions → Run workflow**. It validates the secret as its first job step, then copies only files in `.searchcans-generated-pages`; it never recursively wipes unknown Wiki pages.

Use a dedicated bot or narrowly scoped token. Never place the token in the repository, generated docs, action logs, or a user-facing page.
