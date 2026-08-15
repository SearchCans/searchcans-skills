# Troubleshooting

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
