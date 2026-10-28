# abaplint templates

Copy into the root of an abapGit repository (sources under `src/`), keep the configs you need,
and set `syntax.errorNamespace` to your namespace (default here: `Z`, `Y` and local classes).

| File | Checks |
|---|---|
| `abaplint-syntax.json` | Syntax of the lowest supported release (`v740sp08`). Change `syntax.version` for another floor. |
| `abaplint-clean.json` | The Clean ABAP rules abaplint can check (78 rules, naming patterns of the guide). |
| `abaplint-cloud.json` | ABAP Cloud language version, with the SAP objects released in the cloud and present on 7.40 as dependencies. |
| `.github/workflows/abaplint.yml` + `.github/abaplint-annotate.js` | One job per config on every pull request, findings as annotations. |

Inside SAP: abaplint can also run as an ATC/SCI check through an abaplint server; keep
`dependencies` depth at the default (0 = 20) or 20, otherwise the check stops with "Max depth
reached" as a priority 1 finding.

Further sources worth reading (not vendored here):
- abaplint rule documentation: https://rules.abaplint.org
- SAP Clean ABAP guide (bundled in `skills/clean-abap`): https://github.com/SAP/styleguides
- SAP ABAP cheat sheets (bundled in `skills/sap-abap`): https://github.com/SAP-samples/abap-cheat-sheets
- code pal for ABAP (Clean ABAP checks as ATC checks, for systems without an abaplint server):
  https://github.com/SAP/code-pal-for-abap
