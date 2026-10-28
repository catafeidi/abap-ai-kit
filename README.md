# abap-ai-kit

A tool-neutral kit of instructions, guidelines, skills, agents and hooks for AI coding assistants
(Claude Code, GitHub Copilot, Codex, Cursor), focused on **SAP ABAP development and review**:
classic ABAP 7.40+, ABAP Cloud and clean core, Clean ABAP, unit tests with test doubles,
security, architecture, and the daily flow around tickets, code hosts and support cases.

Personal kit, shared as-is: no support, issues welcome, no guarantee that every rule fits your
landscape. Adjust `AGENTS.md` (the "Who I am" block) and `rules/` to your own way of working.

## Built on

The rules are the kit's own; the knowledge behind them comes from these sources (full list,
licences and pinned commits: `SOURCES.md`, `THIRD-PARTY-NOTICES.md`, `SOURCES.json`):

| Area | Source |
|---|---|
| Style | [Clean ABAP](https://github.com/SAP/styleguides) (SAP, CC-BY-3.0), vendored in full |
| Code review | [SAP ABAP code review guide](https://github.com/SAP/styleguides/tree/main/abap-code-review) (SAP, CC-BY-3.0), vendored |
| Language, OO, design patterns, RAP/EML, ABAP Cloud, unit tests | [SAP ABAP cheat sheets](https://github.com/SAP-samples/abap-cheat-sheets) (SAP, Apache-2.0), 37 sheets vendored |
| Clean core levels A-D, released APIs | [SAP Cloudification Repository](https://github.com/SAP/abap-atc-cr-cv-s4hc) (queried live by `released-api.py`), [SAP clean core white paper](https://www.sap.com/documents/2024/09/20aece06-d87e-0010-bca6-c68f7e60039b.html) |
| ABAP Cloud, ATC cloud readiness, migration | [likweitan/abap-skills](https://github.com/likweitan/abap-skills) (MIT): `abap-cloud`, `atc-cloudification`, `abap-cloud-migration` |
| SAP development references (ABAP, CDS, UI5, Fiori, CAP, API style) | [secondsky/sap-skills](https://github.com/secondsky/sap-skills) (GPL-3.0) |
| RAP architecture | [SAP Flight reference scenario](https://github.com/SAP-samples/abap-platform-refscen-flight), [RAP workshops](https://github.com/SAP-samples/abap-platform-rap-workshops) |
| Object orientation | [SAP abap-oo-basics](https://github.com/SAP-samples/abap-oo-basics), [abap_oo_patterns](https://github.com/SchwarzIT/abap_oo_patterns) |
| Static checks | [abaplint](https://github.com/abaplint/abaplint) (configs in `templates/abaplint/`), [code pal for ABAP](https://github.com/SAP/code-pal-for-abap) |

`python scripts/update-references.py` shows what changed upstream; `--apply` takes it.

## What is inside

| Path | What | Loaded |
|---|---|---|
| `AGENTS.md` | Entry point: defaults, rules index, which guideline for which task | Always |
| `rules/` | Short always-on rules: security, decisions, estimation, model choice, sessions and notes, work tracking | Always |
| `guidelines/abap/` | development (definition of done), clean-abap, code-review, unit-testing, architecture, security, abap-cloud (per project), sap-systems, adt-vscode-setup | By task |
| `guidelines/` | notes (project folder structure), integrations (GitHub / Azure DevOps, Jira / Azure Boards, Confluence, CI, Salesforce) | By task |
| `skills/` | `clean-abap`, `abap-code-review`, `abap-cloud`, `atc-cloudification`, `abap-cloud-migration`, `sap-abap` (37 SAP cheat sheets), `sap-abap-cds`, `sapui5*`, `sap-fiori-tools`, `sap-cap-capire`, `sap-api-style`, `work-tracking`, `find-information`, `support-case` | On demand |
| `agents/abap-reviewer.md` | Read-only independent reviewer | On demand (Claude Code) |
| `hooks/` | Claude Code guards: `rm -rf`, `.env` edits, injection shapes, gitleaks before push, SAP read-only systems and transport releases (with tests) | Every tool call |
| `scripts/` | `install.ps1`, `new-project.ps1`, `adt-vscode/setup_adt_vscode.py`, `setup-integrations.py`, `abap/released-api.py`, `update-references.py` | By you |
| `templates/` | project skeleton, abaplint configs (7.40, ABAP Cloud, Clean ABAP + GitHub workflow), settings example | By scripts |

Where every best practice comes from: `SOURCES.md`. Licences of third-party material:
`THIRD-PARTY-NOTICES.md`.

## Install (Windows, PowerShell)

```powershell
git clone https://github.com/<you>/abap-ai-kit D:\ai-kit
powershell -ExecutionPolicy Bypass -File D:\ai-kit\scripts\install.ps1 -DryRun
powershell -ExecutionPolicy Bypass -File D:\ai-kit\scripts\install.ps1
```

`install.ps1` links rules, hooks, agents, templates and skills into `~/.claude`, writes
`~/.claude/CLAUDE.md` (imports `AGENTS.md`), Copilot (`~/.copilot/...`, VS Code user prompt files)
and Codex (`~/.codex/AGENTS.md`) copies, and sets `AI_KIT_HOME`. Hooks: merge the `hooks` block of
`templates/settings.example.json` into `~/.claude/settings.json` once. Requires Python 3 on `PATH`
as `python`.

## Projects

Project folders sit next to the kit folders and stay out of its Git (whitelist `.gitignore`).
`scripts\new-project.ps1 -Name X` creates one with `AGENTS.md`, notes structure,
`integrations.json` and its own local Git. A project declares its ABAP language version
(`Standard ABAP`, `ABAP for Cloud Development` or `both`); the ABAP Cloud rules apply only there.

## Useful on their own

- `python scripts/abap/released-api.py MARA CL_ABAP_RANDOM_INT RFC_READ_TABLE`: clean core level
  and successor of SAP objects from SAP's Cloudification Repository.
- `python scripts/update-references.py`: what changed upstream in the vendored SAP material.
- `templates/abaplint/`: ready abaplint configs and a pull request workflow.

## Licence

MIT for the kit's own files; third-party material keeps its licence (CC-BY-3.0, Apache-2.0,
GPL-3.0, MIT), see `THIRD-PARTY-NOTICES.md`.
