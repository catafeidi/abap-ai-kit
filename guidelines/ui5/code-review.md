# SAP Fiori / UI5 code review

Same rules as `guidelines/abap/code-review.md` (independent, verify before reporting, every finding
with file, line and a concrete failure scenario, Blocker / Should fix / Nit). Checklist for UI code:

1. **Correctness:** binding paths and model names match the service metadata; `$expand` / `$select`
   fit the view; error handling for failed requests (message manager, no silent catch); navigation
   parameters validated; draft handling (Fiori elements) behaves on cancel and on conflict.
2. **Legacy-free** (official best practices): no sync loading, no globals, no deprecated APIs, async
   component and views, within what the target UI5 version (`minUI5Version`) supports. The UI5
   linter result is attached; findings it reports are not repeated; no new findings in changed files.
3. **Security:** no untrusted data in HTML-rendering controls without sanitising, CSP-compliant (no
   inline script, `eval`), URLs validated, no credentials in the repository (host and client in the
   generated deploy configuration are fine).
4. **Fiori elements:** behaviour comes from annotations; extensions only where annotations cannot
   do it, through the official extension points; no copied framework code.
5. **Performance:** manifest first, preloads, only the needed fields and rows, no requests in loops,
   tables with growing / threshold, no heavy work in formatters.
6. **Accessibility and i18n:** labels, tooltips on icon-only controls, keyboard, all texts in i18n.
7. **Tests:** QUnit / OPA5 cover the new logic and the main journey; no test that only renders.
8. **Launchpad and transport:** target mapping, tile, catalog and role delivered in the right layer
   (`guidelines/ui5/launchpad.md`); deployment configuration without credentials.
