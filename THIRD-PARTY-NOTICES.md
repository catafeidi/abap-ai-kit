# Third-party notices

`LICENSE` (MIT) covers the kit's own files: instructions, guidelines, rules, hooks, scripts,
templates and the skills written for the kit. The material below is copied from other projects and
keeps its licence. Exact source commits: `SOURCES.json`.

| Material | Location in the kit | Source | Licence | Licence text |
|---|---|---|---|---|
| Clean ABAP style guide | `skills/clean-abap/reference/CleanABAP.md`, `skills/sap-abap/references/clean-abap/CleanABAP.md` | [SAP/styleguides](https://github.com/SAP/styleguides), (c) SAP SE or an SAP affiliate company and styleguides contributors | CC-BY-3.0 | `LICENSE-CC-BY-3.0.txt` beside the copies |
| ABAP code review guide | `skills/abap-code-review/reference/ABAPCodeReview.md` | [SAP/styleguides](https://github.com/SAP/styleguides), same holders | CC-BY-3.0 | `skills/abap-code-review/reference/LICENSE-CC-BY-3.0.txt` |
| ABAP cheat sheets | `skills/sap-abap/references/cheat-sheets/` | [SAP-samples/abap-cheat-sheets](https://github.com/SAP-samples/abap-cheat-sheets), (c) SAP SE or an SAP affiliate company | Apache-2.0 | https://www.apache.org/licenses/LICENSE-2.0 |
| SAP development skills | `skills/sap-abap`, `sap-abap-cds`, `sap-api-style`, `sap-cap-capire`, `sap-fiori-tools`, `sapui5`, `sapui5-cli`, `sapui5-linter` | [secondsky/sap-skills](https://github.com/secondsky/sap-skills) | GPL-3.0 | `LICENSE` in each skill folder |
| ABAP Cloud skills | `skills/abap-cloud`, `abap-cloud-migration`, `atc-cloudification` | [likweitan/abap-skills](https://github.com/likweitan/abap-skills), (c) 2026 Lik Wei | MIT | `LICENSE` in each skill folder |

The Cloudification Repository ([SAP/abap-atc-cr-cv-s4hc](https://github.com/SAP/abap-atc-cr-cv-s4hc),
Apache-2.0) is downloaded at run time by `scripts/abap/released-api.py` and not redistributed.

Changes: the vendored files are unmodified copies of the pinned commits, except line endings and,
in the public copy, one documentation example shaped like a live payment API key
(`skills/sap-api-style/references/quality-processes.md`), which is masked.
The kit's guidelines summarise and link these sources; they are original text.
