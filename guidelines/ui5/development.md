# SAP Fiori / UI5 development

How to build or change a Fiori app in any project. The project `AGENTS.md` says the UI technology
(`UI technology: Fiori elements | freestyle UI5 | none`), the UI5 version and where the app is
deployed. SAP's rules: skill `ui5-official-guidelines` (official UI5 pages). Tool references: skills
`sapui5`, `sap-fiori-tools`, `sapui5-linter`, `sapui5-cli`. Set-up: `scripts/setup-fiori.py`.

## Before you build
1. **Fiori elements first.** List report, object page, worklist, analytical list page and
   overview page cover most business apps: the UI comes from annotations (CDS / RAP in ABAP, CDS in
   CAP), not from JavaScript. Choose freestyle UI5 only for what Fiori elements cannot do, and
   prefer a building block or an extension point before a whole freestyle app.
2. **Annotations belong in the backend** (CDS metadata extensions, RAP projections, CAP `.cds`);
   local `annotations.xml` only for what the service cannot carry.
3. **OData V4** for new apps (RAP, CAP); V2 only where the service is V2.
4. **Know the target:** UI5 version (and minimum version in `manifest.json`), ABAP front-end server
   or SAP BTP, launchpad (on-premise, SAP Build Work Zone). The app lives in its own Git
   repository under `<project>/repos/<app>`; notes about it in `products/<app>/`.
5. **Generate, do not hand-write the skeleton:** the Fiori MCP server or the Fiori tools
   application generator; the UI5 MCP server (`create_ui5_app`) for freestyle.

## While you build (legacy-free, as SAP defines it)
- No synchronous loading of code or data, no global names, no deprecated APIs (for example
  `sap.ui.getCore()`, `jQuery.sap.*`): `sap.ui.define` modules, `async: true`, manifest-first
  component, `sap.ui.core.IAsyncContentCreation`.
- Texts only in `i18n` resource bundles; no hard-coded user-visible strings.
- Data binding over manual model handling; `$select` / only the fields the view needs; batch and
  metadata caching as in the performance checklist.
- No inline scripts, `eval` or `new Function`: Content Security Policy compliant.
- Untrusted content is never bound to HTML-rendering controls or `formattedText` without
  sanitising; URLs from data are validated.
- Accessibility: every input has a label, icon-only buttons have a tooltip / `ariaLabelledBy`,
  keyboard navigation works, no colour-only information.
- No credentials, hosts or clients in `manifest.json`, `ui5.yaml` or `ui5-deploy.yaml`: use
  destinations or the system connection of the Connection Manager.

## Definition of done (every UI change)
1. **UI5 linter: 0 findings** (`npx @ui5/linter` or MCP `run_ui5_linter`) and manifest validation
   clean (MCP `run_manifest_validation`).
2. **Tests:** QUnit for formatters, controllers, models and other logic; OPA5 journeys for the
   main flows (Fiori elements: the OPA test library generated with the app), run through the Test
   Starter. Report the real counts.
3. **Performance checklist** of the official guidelines walked through for new apps.
4. **Support Assistant** in the running app: no high-priority issues.
5. **Independent review** with `guidelines/ui5/code-review.md` (Claude Code: `ui5-reviewer` agent).
6. **Deploy only through the project's path** (`fiori deploy` / `npm run deploy` into the ABAP
   repository with a transport, or the BTP pipeline); never from an uncommitted working copy.
7. **Launchpad content** (tile, target mapping, catalog, space / page, role) delivered with the app:
   `guidelines/ui5/launchpad.md`.
