# SAP Fiori / UI5 development

How to build or change a Fiori app in any project. The project `AGENTS.md` says the UI technology
(`UI technology: Fiori elements | freestyle UI5 | none`), the UI5 version and where the app is
deployed. SAP's rules: skill `ui5-official-guidelines` (official UI5 pages) and the MCP servers'
own tools (`get_guidelines` of the UI5 MCP server, `search_docs` of the Fiori MCP server). Tool
references: skills `sapui5`, `sap-fiori-tools`, `sapui5-linter`, `sapui5-cli`. Set-up:
`scripts/setup-fiori.py`.

## Before you build
1. **Know the runtime.** The UI5 version of the target (front-end server component SAP_UI, or the
   CDN / BTP version) and `minUI5Version` in `manifest.json` decide which APIs exist. Newer best
   practices (for example `sap.ui.core.IAsyncContentCreation`, the Test Starter) need newer UI5
   versions: check the API reference for "since" before using an API.
2. **Fiori elements first.** List report, object page, worklist, analytical list page and overview
   page cover most business apps: the UI comes from annotations, not from JavaScript. Choose
   freestyle UI5 only for what Fiori elements cannot do, and prefer a building block or an
   extension point before a whole freestyle app.
3. **Annotations belong in the backend** (CDS metadata extensions, RAP projections, CAP `.cds`);
   local `annotations.xml` only for what the service cannot carry.
4. **OData V4 where the backend offers it** (RAP on SAP S/4HANA 1909 / ABAP 7.54 or later, CAP, BTP
   ABAP environment); OData V2 (SEGW, or RAP V2 bindings) on older releases.
5. **Where the code lives:** the app is its own Git repository under `<project>/repos/<app>` (run
   `npm install` there); notes about it in `products/<app>/`.
6. **Generate, do not hand-write the skeleton:** the Fiori MCP server or the Fiori tools
   application generator; the UI5 MCP server (`create_ui5_app`) for freestyle.

## While you build (legacy-free, as SAP defines it)
- No synchronous loading of code or data, no global names, no deprecated APIs (for example
  `sap.ui.getCore()`, `jQuery.sap.*`): `sap.ui.define` modules, asynchronous loading,
  manifest-first component (official pages: `use-asynchronous-loading.md`,
  `best-practices-for-developers.md`), within what the target UI5 version supports.
- Texts only in `i18n` resource bundles; no hard-coded user-visible strings.
- Data binding over manual model handling; only the fields the view needs; batch and metadata
  caching (`performance-speed-up-your-app.md`).
- Content Security Policy compliant: no inline scripts, `eval` or `new Function`
  (`make-your-app-csp-compliant.md`).
- Untrusted content is never bound to HTML-rendering controls or `FormattedText` without
  sanitising; URLs from data are validated (`browser-security.md`).
- Accessibility: every input has a label, icon-only buttons have a tooltip / `ariaLabelledBy`,
  keyboard navigation works, no colour-only information.
- **No credentials in the repository:** `ui5.yaml`, `ui5-deploy.yaml` and the `.env` of the app hold
  no user or password (use environment variables, the Connection Manager or BTP destinations).
  Host and client in the generated deploy configuration are fine.

## Definition of done (every UI change)
1. **UI5 linter:** no new findings in the changed files (`npx @ui5/linter`, or the UI5 MCP tool
   `run_ui5_linter`), and manifest validation clean (`run_manifest_validation`). Existing findings in
   a legacy app are listed, not silently fixed in an unrelated change; fixes must exist in the
   target UI5 version.
2. **Tests:** QUnit for formatters, controllers, models and other logic; OPA5 journeys for the
   main flows (Fiori elements: the OPA test library generated with the app); Test Starter where the
   UI5 version has it (`test-starter-concept-and-setup.md`). Report the real counts.
3. **Performance:** the official checklist (`performance-checklist.md`, details in
   `performance-speed-up-your-app.md`) walked through for new apps.
4. **Support Assistant** in the running app: no high-priority issues.
5. **Independent review** with `guidelines/ui5/code-review.md` (Claude Code: `ui5-reviewer` agent).
6. **Deploy only through the project's path** (`npm run deploy` / `fiori deploy` into the ABAP
   repository with a transport, or the BTP pipeline); never from an uncommitted working copy.
7. **Launchpad content** delivered with the app: `guidelines/ui5/launchpad.md`.

## Deploy and run (ABAP front-end server)
- The OData service is active: OData V2 in `/IWFND/MAINT_SERVICE` with the right system alias; OData
  V4 / RAP through the published service binding (and the V4 service group where the release needs
  it).
- The ICF node of the BSP application is active; after a deployment the app index is current
  (`/UI5/APP_INDEX_CALCULATE` runs as part of the deployment on recent releases; run it when an app
  still shows an old version) and browser / front-end caches are invalidated.
- Test as a user with only the business role (`launchpad.md`), not as a developer.

## Official rules from the MCP servers (quoted)
From the [UI5 MCP server README](https://github.com/UI5/mcp-server) (Apache-2.0):
> Use the `get_guidelines` tool of the UI5 MCP server to retrieve the latest coding standards and
> best practices for UI5 development.

From the [Fiori MCP server README](https://github.com/SAP/open-ux-tools/tree/main/packages/fiori-mcp-server)
(Apache-2.0), rules for creating or modifying SAP Fiori elements apps (abridged, wording kept):
> - When asked to create an SAP Fiori elements app check whether the user input can be interpreted
>   as an application organized into one or more pages containing table data or forms, these can
>   be translated into a SAP Fiori elements application, else ask the user for suitable input.
> - The application typically starts with a List Report page showing the data of the base entity of
>   the application in a table. Details of a specific table row are shown in the ObjectPage.
> - An Object Page can contain one or more table sections based on to-many associations of its
>   entity type.
> - The data model must be suitable for usage in a SAP Fiori elements frontend application. So there
>   must be one main entity and one or more navigation properties to related entities.
> - When attempting to modify the SAP Fiori elements application like adding columns you must not
>   use the screen personalization but instead modify the code of the project, before this first
>   check whether an MCP server provides a suitable function.
> - When previewing the SAP Fiori elements application use the most specific `npm run watch-*`
>   script for the app in the `package.json`.

(The README's CAP-specific rules, UUID keys and CSV sample data, apply when the backend is CAP.)
