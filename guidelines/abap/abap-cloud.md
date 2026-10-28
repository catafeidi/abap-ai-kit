# ABAP Cloud and clean core

## Cloud first, wherever the system allows it

The project's `AGENTS.md` may fix the language version per package; otherwise the target system
decides, and **new development uses ABAP for Cloud Development whenever the system offers it**:

| Target system | Default for new objects |
|---|---|
| SAP BTP ABAP environment, SAP S/4HANA Cloud Public Edition | ABAP for Cloud Development (the only option) |
| SAP S/4HANA 2022 or later, on-premise or Private Cloud (SAP_BASIS 7.57+) | ABAP for Cloud Development, level A. Classic only for what has no released API, through a documented wrapper (level B/C) |
| SAP NetWeaver 7.40-7.5x, ECC, S/4HANA before 2022 | Standard ABAP, **cloud-ready**: released APIs where they exist (`released-api.py --product pce`), released CDS views instead of SAP tables where available, logic in classes behind interfaces, no obsolete statements, so a later move costs little |

Changing existing classic objects: keep their language version; do not convert a whole object as
a side effect of a fix. Moving code to ABAP Cloud is its own change (skill `abap-cloud-migration`).
The rest of this page is the rule set for code in ABAP for Cloud Development, and the scale every
other code is measured on.

Deeper material: skills `abap-cloud` (levels, development models, wrapper pattern),
`atc-cloudification` (ATC variants per product), `abap-cloud-migration` (classic to cloud),
`sap-abap` (cheat sheet `19_ABAP_for_Cloud_Development`, released classes, RAP / EML).

## Clean core levels (SAP, replaces the three-tier extensibility model)
| Level | SAP objects used | Clean core | ATC (clean core check) |
|---|---|---|---|
| **A** | Released APIs and extension points (stability contract) | yes | no finding |
| **B** | Classic APIs nominated by SAP (no formal contract) | yes | priority 3 |
| **C** | Internal SAP objects (anything not classified) | conditional: needs a changelog / governance | priority 2 |
| **D** | Not recommended objects, modifications, techniques | no | priority 1 |

An extension has the level of its least clean part. **Check every SAP object before you use it:**
`python <kit>\scripts\abap\released-api.py <OBJECT> [--product public|pce|btp]` (data: SAP's
Cloudification Repository). Not released: look for the successor it prints, or `--search`.

## Rules in ABAP for Cloud Development
- Only released (level A) SAP objects: CDS views (`I_*`), released classes and interfaces,
  released BAdIs / extension points, released RAP BOs. No `SELECT` on SAP tables (`MARA`, `VBAK`):
  use the released CDS view (`released-api.py MARA` names `I_PRODUCT`).
- Restricted language: no `SUBMIT`, no dynpro / selection screens / `WRITE` lists, no `CALL FUNCTION`
  of unreleased modules, no `CALL TRANSACTION`, no native SQL, no file system access by path, no
  `COMMIT WORK` inside RAP handlers (the RAP framework owns the LUW).
- New business logic in RAP (managed where possible); services through service definitions and
  bindings; output through `if_oo_adt_classrun` or a service, not lists.
- A needed function without a released API: a **wrapper** in a classic-language package
  (level B/C), released for cloud use (C1), owned and documented; the cloud code calls only the
  wrapper. Record the decision; replace the wrapper when SAP releases an API.

## Hard vs soft violations
| | BTP ABAP environment / S/4HANA Cloud Public | S/4HANA on-premise / Private Cloud in the ABAP Cloud model |
|---|---|---|
| Unreleased SAP object, SAP table access, restricted statement | hard: does not compile | hard: ATC error in cloud-language objects |
| Classic API (level B) through a wrapper | not available | allowed, documented |
| Internal object (level C) through a wrapper | not available | allowed only with a changelog / owner, temporary |
| Modification of SAP objects (level D) | not possible | never |

## Checks
- ATC with the clean core variant (`ABAP_CLEAN_CORE_DEVELOPMENT`; the older
  `ABAP_CLOUD_DEVELOPMENT_3TIER` is deprecated in favour of it). Product-specific variants: skill
  `atc-cloudification`.
- abaplint with `templates/abaplint/abaplint-cloud.json` (language version Cloud plus the API
  intersection with 7.40) when the same code also runs on 7.40.
- Do not suppress clean core findings with pseudo-comments; fix or document a wrapper.

Sources: `SOURCES.md` (Cloudification Repository, SAP clean core guidance, RAP reference scenario).

## CDS and RAP in practice (seen on S/4HANA releases; check on yours)
- **Released means `#PUBLIC_API` for custom code.** Views classified for local use only
  (`PUBLIC_LOCAL_API`) and DDIC tables are blocked in ABAP Cloud objects ("use of CDS entity ... is
  not permitted"), sometimes per element or per association of an otherwise usable view. Check
  with `released-api.py`; the syntax check does not always catch it, activation does.
- **No `true` / `false` literals** in some view-entity releases: use
  `cast( case when <cond> then 'X' else ' ' end as abap_boolean )`.
- **Authorization in the save phase.** A validation that reads a CDS view with access control (for
  example `I_Product`) dumps with `BEHAVIOR_ILLEGAL_STATEMENT` ("AUTHORITY-CHECK(DCL) is not allowed
  with this status"). Read reference data `WITH PRIVILEGED ACCESS`; put `#CHECK` and the DCL on the
  projection views, `#NOT_REQUIRED` on the BO's interface views.
- **Calculated elements in a draft BO** are read from the draft table while editing, not computed:
  set them in the determination that changes their source field.
- **Projection views** cannot select fields through an association they define themselves: define
  the association in the interface view and follow the path in the projection.
- **OData bindings** reject non-standard conversion exits on exposed fields (`ALPHA` is fine): cast
  the field to a plain type.
- **Released RAP BOs check every key in `%target`.** In `CREATE BY \_child`, fill the child's full
  key (including the parent key) in each `%target` line, not only `%tky` of the parent.
- **Fiori Elements V4 list-report tabs** ignore `@UI.selectionVariant` `filter` and CDS parameters
  for per-tab filtering, and CDS cannot emit `SelectOptions` on some releases: define the
  `UI.SelectionVariant` with `SelectOptions` in the app's local `annotation.xml` (same term and
  qualifier), keep the `SelectionPresentationVariant` in the metadata extension.
- **VDM layering:** a `#BASIC` view must not select from a `#COMPOSITE` view.
