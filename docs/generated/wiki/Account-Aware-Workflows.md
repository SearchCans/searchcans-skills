# Account-Aware Workflows

> Estimate scope, inspect safe account state once, then cap or stop before an oversized job begins.

SearchCans multi-request Skills can use the Account API to estimate planned SERP and Reader/File costs, inspect remaining credits and Parallel Lanes, and choose a safe scope. Reports retain only sanitized budget fields; they never include account email, raw key data, or credentials.

## Common controls

- `--account-mode auto`: use the Skill's safe default policy.
- `warn`: record an account warning without changing the requested scope.
- `enforce`: block an insufficient job before business requests run.
- `cap`: reduce supported variable scope when possible.
- `off`: skip the pre-flight deliberately.

Start at Reader proxy tier 0. Higher proxy tiers change expected cost and should follow an identified access issue, not be used as a default.

## Skill behavior

| Skill | Default account-aware behavior |
| --- | --- |
| [SearchCans Deep Research](SearchCans-Deep-Research) | Checks one pre-flight, caps Reader sources, and limits concurrency to reported lanes. |
| [SearchCans SERP Content Gap](SearchCans-SERP-Content-Gap) | Checks multi-page jobs and caps page scope when the planned request count exceeds the budget. |
| [SearchCans Reader SEO Audit](SearchCans-Reader-SEO-Audit) | Runs a pre-flight automatically for higher-cost proxy requests and keeps standard extraction lightweight. |
| [SearchCans Market Watch](SearchCans-Market-Watch) | Checks one pre-flight, caps selected Reader news sources, and respects reported lane count. |
| [SearchCans Product SERP Brief](SearchCans-Product-SERP-Brief) | Checks the three SERP calls plus explicit Reader URLs and caps only source reads when needed. |
| [SearchCans Content Format Brief](SearchCans-Content-Format-Brief) | Checks one pre-flight per requested format and caps the selected formats in a fixed priority order. |
| [SearchCans RAG Source Curator](SearchCans-RAG-Source-Curator) | Checks search plus Reader/File source budget, caps selected sources, and limits workers to reported lanes. |

A capped run is still useful only within its effective scope. Always report requested versus effective sources/pages/formats, and never invent findings for skipped work.
