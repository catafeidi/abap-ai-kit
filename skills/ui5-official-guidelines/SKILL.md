---
name: ui5-official-guidelines
description: Use when writing, upgrading or reviewing SAPUI5 / OpenUI5 or SAP Fiori freestyle code and you need SAP's own rules - legacy-free code (no sync loading, no globals, no deprecated APIs such as sap.ui.getCore), asynchronous loading, manifest-first components, performance checklist, Content Security Policy, browser security, accessibility, QUnit / OPA5 testing with the Test Starter. Holds the official UI5 documentation pages; pair with the kit guideline guidelines/ui5/development.md.
---

# UI5 official guidelines

Verbatim pages from the OpenUI5 documentation ([UI5/docs](https://github.com/UI5/docs),
CC-BY-SA-4.0, licence text in `reference/LICENSE-CC-BY-SA-4.0.txt`), pinned in the kit's
`SOURCES.json`. Read the section you need, not the whole page. Links inside the pages point to
other documentation pages: open them on https://ui5.sap.com (SAPUI5) or https://sdk.openui5.org.

| Page | Read when |
|---|---|
| `reference/best-practices-for-developers.md` | writing or upgrading app code: legacy-free goals, deprecated APIs, modules, async loading, data binding, manifest, controllers / views / fragments, models, error handling |
| `reference/performance-checklist.md` | before calling an app done; reviewing a slow app |
| `reference/content-security-policy.md` | anything that loads code, uses inline scripts, `eval`, or third-party libraries |
| `reference/browser-security.md` | output of untrusted data, HTML content, URLs, clickjacking |
| `reference/accessibility.md` | labels, keyboard handling, screen readers, themes |
| `reference/use-asynchronous-loading.md` | bootstrap, component and module loading |
| `reference/performance-speed-up-your-app.md` | the details behind each performance checklist item |
| `reference/make-your-app-csp-compliant.md` | making existing code CSP compliant |
| `reference/testing.md`, `reference/unit-testing-with-qunit.md`, `reference/test-starter.md`, `reference/test-starter-concept-and-setup.md` | writing QUnit / OPA5 tests and the test set-up |

Relative links inside the pages (`xxx-1a2b3c4.md`) point to documentation pages that are not
copied: open them on the online documentation by title, or ask the UI5 MCP server
(`get_guidelines`) or the Fiori MCP server (`search_docs`).

Tools that check these rules: the UI5 linter (`npx @ui5/linter`, or the UI5 MCP server tool
`run_ui5_linter`), manifest validation (`run_manifest_validation`), the UI5 Support Assistant in
the browser.
