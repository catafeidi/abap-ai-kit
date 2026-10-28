<p align="center"><img src=".github/assets/hero.jpg" alt="ABAP AI Kit: make Claude, Copilot and Codex write ABAP like a senior developer" width="100%"></p>

<h1 align="center">ABAP AI Kit</h1>

<p align="center"><b>Make Claude, Copilot and Codex write ABAP like a senior developer.</b></p>

<p align="center">
Clean ABAP, clean core (levels A-D), ABAP Cloud, independent code review and unit tests with
test doubles: as rules your AI follows on every prompt, with guardrails it cannot skip.
</p>

<p align="center">
<a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/github/license/catafeidi/abap-ai-kit"></a>
<img alt="Last commit" src="https://img.shields.io/github/last-commit/catafeidi/abap-ai-kit">
<img alt="Works with" src="https://img.shields.io/badge/works%20with-Claude%20Code%20%7C%20GitHub%20Copilot%20%7C%20Codex-1f6feb">
<img alt="Built on" src="https://img.shields.io/badge/built%20on-Clean%20ABAP%20%7C%20SAP%20cheat%20sheets%20%7C%20Cloudification%20Repository-0a7d4f">
</p>

---

## Why

AI assistants write ABAP that compiles and still fails review: `SELECT *` on SAP tables in cloud
code, no `AUTHORITY-CHECK`, `sy-subrc` read after a functional call, no tests, syntax that does not
exist on 7.40. This kit gives your assistant the standards a senior ABAP developer applies without
thinking, and checks it cannot talk its way around.

## What changes when the kit is installed

| Situation | What the AI does with the kit | How |
|---|---|---|
| You ask for new code on S/4HANA 2022+ | Writes **ABAP for Cloud Development** (level A) and checks every SAP object it uses; classic only through a documented wrapper | rule + `released-api.py` |
| It wants to read `MARA` | Finds out it is level C and uses the released successor | `released-api.py` (below) |
| You target 7.40 | Writes 7.40 syntax (no `ENUM`, no `RAISE EXCEPTION NEW`), cloud-ready style | `guidelines/abap/development.md`, abaplint 7.40 config |
| A change is "done" | Only with ABAP Unit tests, test doubles for database / RFC / HTTP, checks green with real counts, and an independent review | definition of done |
| You ask for a review | Findings ranked Blocker / Should fix / Nit, each with file, line and a concrete failure scenario; a read-only reviewer agent gives a second opinion | `abap-code-review` skill + agent, SAP's code review guide |
| It is about to change a system marked read-only, or release a transport | **Blocked** or asks you first, whatever the model decides (Claude Code) | hook `sap-guard.py` |
| It is about to push a secret or an internal name | **Blocked** (Claude Code hook; plus a git pre-push hook for any tool) | `gitleaks-pre-push.py` |

Real output of the clean core look-up (SAP's Cloudification Repository, private cloud / on-premise):

```text
$ python scripts/abap/released-api.py MARA BAPI_USER_GET_DETAIL RFC_READ_TABLE CL_ABAP_RANDOM_INT
MARA [TABL] state=notToBeReleased -> level C (S4CORE LO-MD-MM); successor: I_PRODUCT, I_PRODUCTPROCUREMENT, ...
BAPI_USER_GET_DETAIL [FUNC] state=classicAPI -> level B (SAP_BASIS BC-SEC-USR-ADM)
RFC_READ_TABLE [FUNC] state=noAPI -> level D (SAP_BASIS BC-SEC-AIS-TOO)
CL_ABAP_RANDOM_INT [CLAS] state=released -> level A (SAP_BASIS BC-ABA-LA)
```

## Quickstart (Windows, 2 minutes)

```powershell
git clone https://github.com/catafeidi/abap-ai-kit D:\ai-kit
powershell -ExecutionPolicy Bypass -File D:\ai-kit\scripts\install.ps1
```

Then, in any ABAP project, ask your assistant: *"review this class"*, *"write a unit test with a
test double for this method"*, or *"can I use MARA in ABAP Cloud?"*.

`install.ps1` links the rules, skills, agents and hooks into Claude Code (`~/.claude`), writes the
instructions for GitHub Copilot (`~/.copilot`, VS Code user prompt files) and Codex
(`~/.codex/AGENTS.md`), and can be re-run after every `git pull`. For the hooks, merge the `hooks`
block of `templates/settings.example.json` into `~/.claude/settings.json` once. Needs Python 3 as
`python`.

## What is inside

| Path | What | Loaded |
|---|---|---|
| `AGENTS.md` | Entry point: defaults, rules index, which guideline for which task | Always |
| `rules/` | Short always-on rules: security, decisions, estimation, model choice, sessions and notes, work tracking | Always |
| `guidelines/abap/` | development (cloud first, definition of done), clean-abap, code-review, unit-testing, architecture, security, abap-cloud, sap-systems, adt-vscode-setup | By task |
| `guidelines/` | notes (project folder structure), integrations (GitHub / Azure DevOps, Jira / Azure Boards, Confluence, CI, Salesforce) | By task |
| `skills/` | `clean-abap`, `abap-code-review`, `abap-cloud`, `atc-cloudification`, `abap-cloud-migration`, `sap-abap` (37 SAP cheat sheets), `sap-abap-cds`, `sapui5*`, `sap-fiori-tools`, `sap-cap-capire`, `sap-api-style`, `work-tracking`, `find-information`, `support-case` | When the prompt matches |
| `agents/abap-reviewer.md` | Read-only independent reviewer | On demand (Claude Code) |
| `hooks/` | Guards: `rm -rf`, `.env` edits, injection shapes, gitleaks before push, read-only SAP systems, transport releases (with tests) | Every tool call |
| `scripts/` | `install.ps1`, `new-project.ps1`, `adt-vscode/setup_adt_vscode.py`, `setup-integrations.py`, `abap/released-api.py`, `update-references.py` | By you |
| `templates/` | Project skeleton, abaplint configs (7.40, ABAP Cloud, Clean ABAP + GitHub workflow), settings example | By scripts |

Skills load when your prompt matches their description, so they cost nothing until needed.

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

## Projects and personal settings

Project folders sit next to the kit folders and stay out of its Git (whitelist `.gitignore`).
`scripts\new-project.ps1 -Name X` creates one with `AGENTS.md`, notes structure,
`integrations.json` and its own local Git. ABAP Cloud is the default wherever the system offers it;
a project can fix the language version per package.

Personal settings go into `<kit>\local\` (ignored by Git): `identity.md` (who you are, your
language; loaded after `AGENTS.md`), `skills/` (your own skills), `gitleaks-internal.toml` (names of
your employer and customers, so they can never be pushed). `install.ps1` picks them up.

## Contributing

Ideas, fixes and new skills are welcome: see [CONTRIBUTING.md](CONTRIBUTING.md). Good first
contributions: a macOS / Linux `install.sh`, an abaplint config for 7.50 / 7.52, a tested Azure
DevOps or GitLab adapter, before/after examples from real reviews.

## Licence

MIT for the kit's own files; third-party material keeps its licence (CC-BY-3.0, Apache-2.0,
GPL-3.0, MIT), see `THIRD-PARTY-NOTICES.md`. Not affiliated with or endorsed by SAP SE; SAP and
ABAP are trademarks of SAP SE.
