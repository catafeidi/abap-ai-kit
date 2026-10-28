# Sources and credits

What the kit's best practices are based on. **Vendored** material is copied into the kit, pinned
to a commit in `SOURCES.json` and refreshed with `python scripts/update-references.py [--apply]`.
**Referenced** material is linked or queried live and never copied. Licences of vendored material
stay with the copies (`license:` in each `SKILL.md`, `LICENSE` files).

## Vendored

| Source | Licence | In the kit | Backs |
|---|---|---|---|
| [SAP/styleguides](https://github.com/SAP/styleguides) - Clean ABAP | SAP style guides terms | `skills/clean-abap/reference/CleanABAP.md` (+ copy in `sap-abap`) | `guidelines/abap/clean-abap.md`, reviews |
| [SAP-samples/abap-cheat-sheets](https://github.com/SAP-samples/abap-cheat-sheets) | Apache-2.0 | `skills/sap-abap/references/cheat-sheets/` (37 sheets) | syntax per release, OO, design patterns, RAP/EML, ABAP Cloud, unit tests |
| [secondsky/sap-skills](https://github.com/secondsky/sap-skills) | GPL-3.0 | skills `sap-abap`, `sap-abap-cds`, `sap-api-style`, `sap-cap-capire`, `sap-fiori-tools`, `sapui5`, `sapui5-cli`, `sapui5-linter` | SAP development references |
| [likweitan/abap-skills](https://github.com/likweitan/abap-skills) | MIT | skills `abap-cloud`, `abap-cloud-migration`, `atc-cloudification` | clean core levels A-D, wrapper pattern, ATC cloud readiness / clean core variants, classic-to-cloud migration |

## Queried live

| Source | Licence | Used by |
|---|---|---|
| [SAP/abap-atc-cr-cv-s4hc](https://github.com/SAP/abap-atc-cr-cv-s4hc) - Cloudification Repository | Apache-2.0 | `scripts/abap/released-api.py` (release state, successor, clean core level per object; public / private cloud / BTP) |

## Referenced (read when the topic comes up)

| Topic | Source |
|---|---|
| Clean core levels (replaces the 3-tier extensibility model) | SAP: [Clean core extensibility for SAP S/4HANA Cloud (white paper)](https://www.sap.com/documents/2024/09/20aece06-d87e-0010-bca6-c68f7e60039b.html), [SAP News: extend SAP S/4HANA Cloud the right way](https://news.sap.com/2025/08/extend-sap-s4hana-cloud-right-way-clean-clear/), [learning.sap.com: clean core extensibility best practices](https://learning.sap.com/courses/practicing-clean-core-extensibility-for-sap-s-4hana-cloud/explaining-extensibility-model-best-practices_e290f382-800e-40ef-a203-85a13115f487) |
| ABAP Cloud custom code checks | SAP Community: [how to check your custom code for ABAP Cloud](https://blogs.sap.com/2023/03/19/how-to-check-your-custom-code-for-abap-cloud/), [finding APIs for the extensibility model](https://answers.sap.com/t5/technology-blogs-by-sap/how-to-find-sap-apis-for-sap-s-4hana-3-tier-extensibility-model/ba-p/13623819) |
| RAP reference architecture | [SAP-samples/abap-platform-refscen-flight](https://github.com/SAP-samples/abap-platform-refscen-flight), [abap-platform-rap-opensap](https://github.com/SAP-samples/abap-platform-rap-opensap), [abap-platform-rap-workshops](https://github.com/SAP-samples/abap-platform-rap-workshops), [abap-platform-fiori-feature-showcase](https://github.com/SAP-samples/abap-platform-fiori-feature-showcase) (all Apache-2.0) |
| Object orientation, patterns, dependency injection | [SAP-samples/abap-oo-basics](https://github.com/SAP-samples/abap-oo-basics) (Apache-2.0), cheat sheets 04 and 34, [SchwarzIT/abap_oo_patterns](https://github.com/SchwarzIT/abap_oo_patterns) (Apache-2.0, GoF patterns in ABAP, last change 2019), Clean ABAP chapters Classes / Methods |
| Static checks | [abaplint](https://github.com/abaplint/abaplint) (MIT; configs in `templates/abaplint/`, rules at rules.abaplint.org), [SAP/code-pal-for-abap](https://github.com/SAP/code-pal-for-abap) (Apache-2.0, Clean ABAP as ATC checks), [abapedia API intersection 7.40 / cloud](https://github.com/abapedia/steampunk-2305-api-intersect-740) |
| Source control | [abapGit](https://github.com/abapGit/abapGit) (MIT), [SAP/abap-file-formats](https://github.com/SAP/abap-file-formats) (MIT) |
| ABAP keyword documentation | [help.sap.com ABAP keyword documentation](https://help.sap.com/doc/abapdocu_latest_index_htm/latest/en-US/index.htm) |
| Older guideline | DSAG best-practice guideline for ABAP development (PDF, 2016 / English 2018): superseded by Clean ABAP and the sources above; consult only for history |

## Looked at and not taken
- [matt1as/claude-abap-skills](https://github.com/matt1as/claude-abap-skills) (Apache-2.0): rejects
  classic ABAP as a whole, which conflicts with 7.40 projects. Adapted instead: cloud first wherever
  the system offers ABAP Cloud (with cloud-ready Standard ABAP on older releases), hard vs soft clean
  core violations, no pseudo-comment suppressions, behaviour-preserving refactoring passes.
- The other skills of likweitan/abap-skills: overlap with the vendored SAP skills (two skills for one
  topic make the AI choose at random); `released-abap-classes` is replaced by the live
  Cloudification Repository look-up.
