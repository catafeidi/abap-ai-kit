# {{NAME}}: project instructions for AI tools

The shared kit (`$AI_KIT_HOME\AGENTS.md`, `rules/`, `guidelines/`) applies; this file adds
what is specific to {{NAME}} and wins on conflict. Keep it short: facts and pointers.

## Context
- What the project is: <one line>
- Customer / employer: <name>, ticket system: <Jira key / none>

## Systems and releases
| System | Role | Release (CVERS) | Notes |
|---|---|---|---|
| <SID> | development / test / reference | <SAP_BASIS 7.xx SPxx> | <read-only? MCP server name> |

## Code conventions (only where they differ from the kit)
- Namespace / packages: <...>
- Lowest release to support: <...>
- **UI technology:** <Fiori elements | freestyle UI5 | none>, UI5 version <1.xxx>, deployed to
  <ABAP front-end server | SAP BTP>; app repositories in `repos/<app>`.
- **ABAP language version:** <leave out to use the kit default: ABAP for Cloud Development where the
  system offers it, cloud-ready Standard ABAP on older releases> or fix it per package:
  <Standard ABAP | ABAP for Cloud Development | both (one source for 7.40 and cloud)>.
- Tightened or relaxed rules: <...>

## Folder map
See `README.md`. Support cases in `support/cases/<id>/`, reusable knowledge in `support/kb/`,
products in `products/`, big implementations in `implementations/`, defects in `bugs/`.

## Working rules
- <e.g. which system is the source of truth for which code>
- <e.g. who releases transports>
