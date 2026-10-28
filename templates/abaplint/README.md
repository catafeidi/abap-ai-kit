# abaplint templates

Copy into the root of an abapGit repository (sources under `src/`), keep the configs you need,
and set `syntax.errorNamespace` to your namespace (default here: `Z`, `Y` and local classes).

| File | Checks |
|---|---|
| `abaplint-syntax.json` | Syntax of the lowest supported release: 7.40 SP08 (`v740sp08`). |
| `abaplint-syntax-750.json` | Same for a 7.50 floor (`v750`). |
| `abaplint-syntax-752.json` | Same for a 7.52 floor (`v752`). Other floors: copy one and change `syntax.version`. |
| `abaplint-clean.json` | The Clean ABAP rules abaplint can check (78 rules, naming patterns of the guide). |
| `abaplint-cloud.json` | ABAP Cloud language version, with the SAP objects released in the cloud and present on 7.40 as dependencies. |
| `.github/workflows/abaplint.yml` + `.github/abaplint-annotate.js` | One job per config on every pull request, findings as annotations. |

**Pick the syntax config of the lowest release the code must run on**: in the workflow, set
`SYNTAX_CONFIG` and `SYNTAX_LABEL` in the `env` of the `syntax` job (the annotations then name the
right release). Set `syntax.version` in `abaplint-clean.json` to the same release, otherwise the
Clean ABAP rules do not parse the newer statements. Checked with `@abaplint/cli` 2.120.67 and
2.120.90 (same results):

| Statement (first release) | 7.40 SP08 config | 7.50 config | 7.52 config |
|---|---|---|---|
| `SELECT FROM t000 FIELDS mandt INTO TABLE @DATA(clients).` (7.50) | flagged | passes | passes |
| `TYPES: BEGIN OF ENUM ty_color, red, green, END OF ENUM ty_color.` (7.51) | flagged | flagged | passes |
| `RAISE EXCEPTION NEW cx_sy_zerodivide( ).` (7.52) | flagged | flagged | passes |

**What the syntax configs check, and what they do not:** they switch on only `parser_error`, which
checks the statement grammar per release. Features inside expressions, such as the inline
declaration `FINAL(x) = ...` (7.57), need the rule `check_syntax` as well: with it, `FINAL( )` is
flagged on 7.40 and 7.52. `check_syntax` resolves every object the code uses, so turn it on only
with `dependencies` set up (otherwise it reports your own Z objects as unknown). `RAISE SHORTDUMP`
(7.53) passed every configuration tried, so abaplint does not catch it. Activation on a system of
the lowest release stays the proof.

Inside SAP: abaplint can also run as an ATC/SCI check through an abaplint server; keep
`dependencies` depth at the default (0 = 20) or 20, otherwise the check stops with "Max depth
reached" as a priority 1 finding.

Further sources worth reading (not vendored here):
- abaplint rule documentation: https://rules.abaplint.org
- SAP Clean ABAP guide (bundled in `skills/clean-abap`): https://github.com/SAP/styleguides
- SAP ABAP cheat sheets (bundled in `skills/sap-abap`): https://github.com/SAP-samples/abap-cheat-sheets
- code pal for ABAP (Clean ABAP checks as ATC checks, for systems without an abaplint server):
  https://github.com/SAP/code-pal-for-abap
