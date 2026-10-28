---
applyTo: "**/*.abap,**/*.asddls,**/*.asdcls,**/*.asbdef"
description: ABAP development and review rules (kit guidelines)
---

# ABAP (applies to ABAP and CDS sources)

Full rules: `guidelines/abap/development.md`, `guidelines/abap/clean-abap.md`,
`guidelines/abap/code-review.md`, `guidelines/abap/unit-testing.md` in the kit
(folder in the environment variable `AI_KIT_HOME`). The project `AGENTS.md` gives the release level and namespace.

- Write for the lowest release the code runs on; on 7.40 no `ENUM`, no `RAISE EXCEPTION NEW`,
  no `FINAL( )`.
- Check function module parameter names against the system (`FUPARAREF`); syntax checks do not.
- Descriptive names without abbreviations; `NEW #( )`, functional calls, string templates,
  constructor expressions; `abap_true` / `abap_false`.
- Class-based exceptions with `previous`; evaluate `sy-subrc` right after the statement that sets
  it, never after a functional method call; no empty `CATCH` or `WHEN OTHERS`.
- ABAP SQL: explicit field list, `WHERE` on keys, no `SELECT` in loops, `FOR ALL ENTRIES` only on
  a non-empty driver table.
- Interfaces and constructor injection so units can be tested; members `PRIVATE`, classes `FINAL`.
- Review findings need file, line and a concrete failure scenario; group as Blocker / Should fix /
  Nit.
- **Definition of done for every change:** ABAP Unit tests in the same change (negative cases,
  the fixed bug), dependencies replaced by test doubles (`cl_abap_testdouble` from 7.40 SP09,
  local fakes below), syntax check / ATC / abaplint green with real counts reported, and an
  independent review before release.
