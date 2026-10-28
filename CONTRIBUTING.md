# Contributing

Thanks for helping. The kit is small on purpose: every rule competes for the assistant's
attention, so a change must earn its place.

## Before you start
- Open an issue for anything bigger than a fix, so we agree on the place and the scope.
- Read `AGENTS.md` (how the kit is routed) and the file you want to change.

## What goes where
| You want to add | Put it in | Notes |
|---|---|---|
| A habit that applies to every task | `rules/` | a few lines; one line in the `AGENTS.md` rules index |
| Standards for one kind of task | `guidelines/` | link it from the routing table in `AGENTS.md` |
| A procedure or reference the AI loads when needed | `skills/<name>/SKILL.md` | the `description` decides when it triggers: name concrete user phrases; do not overlap an existing skill |
| A check the model must not be able to skip | `hooks/` + `hooks/tests/` | fail open on errors, deny only what is irreversible or a leak, ask otherwise; tests required |
| Third-party material | `SOURCES.json` (pinned) + `SOURCES.md` + `THIRD-PARTY-NOTICES.md` | licence must allow redistribution; keep the licence text beside the copy |

## Rules for changes
- Established terms only (SAP documentation, Clean ABAP, HTTP); no invented names.
- ABAP examples must compile on the release they claim; say which.
- No employer, customer, system or personal data. The secret scan runs on every push.
- Run the tests you touched: `python hooks/tests/test_sap_guard.py`,
  `python hooks/tests/test_gitleaks_pre_push.py`; `install.ps1 -DryRun` must stay quiet on a
  second run.
- One topic per pull request; describe what the assistant does differently afterwards.

## Good first contributions
- `install.sh` for macOS / Linux (same steps as `install.ps1`, symlinks instead of junctions).
- abaplint configurations for 7.50 and 7.52 in `templates/abaplint/`.
- A tested Azure DevOps or GitLab adapter in `guidelines/integrations.md` and
  `scripts/setup-integrations.py`.
- Before / after examples from real reviews (anonymised) in a new `examples/` folder.
