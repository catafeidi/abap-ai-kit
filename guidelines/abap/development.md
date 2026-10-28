# ABAP development

How to write or change ABAP in any project. The project `AGENTS.md` says which release,
namespace and system apply; this file says how to work.

## Before you write

1. **Know the target release.** Read it from the project `AGENTS.md` or from the system
   (`CVERS` / component `SAP_BASIS`), never from an add-on version string. Write for the lowest
   release the code must run on. On 7.40 there is no `ENUM` (7.51), no `RAISE EXCEPTION NEW`
   (7.52), no `FINAL(...)` (7.57) and no `WITH ... INTO TABLE @DATA` in every form; downgrade
   syntax you found in newer examples.
2. **Read the matching cheat sheet** in `skills/sap-abap/references/cheat-sheets/` (router:
   `INDEX.md`) for the statements you use: internal tables, ABAP SQL, exceptions, OO, string
   processing, dates and times, unit tests. Do not claim a pattern is idiomatic without reading it.
3. **Read the code around the change.** Reuse existing constants, exception classes, helper
   methods and naming. A second way of doing the same thing is a finding in review.
4. **Check every API you call against the system.** Syntax checks do not verify `CALL FUNCTION`
   parameter names: check them in table `FUPARAREF` (or the function module signature). For
   classes, read the method signature. Never guess a parameter name or a released API.
5. **Cloud first.** New objects use ABAP for Cloud Development whenever the target system offers it
   (BTP, S/4HANA Cloud, S/4HANA 2022+): `guidelines/abap/abap-cloud.md`, every SAP object checked
   with `scripts/abap/released-api.py`. Older releases (7.40-7.5x): Standard ABAP written
   cloud-ready (released APIs and CDS views where they exist). The project `AGENTS.md` can fix the
   language version per package and wins.
6. **Design first** for anything beyond a small change: `guidelines/abap/architecture.md`
   (interfaces, injection, layers, patterns). Entry points and data access:
   `guidelines/abap/security.md`.

## While you write

- Follow `guidelines/abap/clean-abap.md`. The full SAP guide is in
  `skills/clean-abap/reference/CleanABAP.md`.
- Design for testing: depend on interfaces, inject dependencies through the constructor, keep
  database and RFC access behind an interface so unit tests can replace it.
- Members are `PRIVATE` by default; classes are `FINAL` unless designed for inheritance.
- Evaluate `sy-subrc` right after the statement that sets it. Never after a functional method call.
- One exception super class per component; keep `previous` when you re-raise.
- No `COMMIT WORK` inside reusable code unless that is its documented job.
- No hard-coded clients, users, system IDs, host names or passwords.
- No pseudo-comments (`"#EC ...`, `##...` pragmas) to silence ATC, abaplint or the syntax check
  unless the finding is a proven false positive; then add the reason in a comment on the same
  line or the ticket. Fix the code first.

## Refactoring (behaviour must not change)
- Tests first: if the code has no unit tests for the behaviour you touch, add characterisation
  tests that pin the current behaviour, then refactor.
- One kind of change per pass (names, declarations, expressions, method extraction, error
  handling, class structure), each pass compiled and tested before the next.
- Anything that could change behaviour (order of operations, exception types, `sy-subrc` paths,
  SQL result order, rounding) is not a refactoring: list it and ask before doing it.
- Legacy code you do not own: keep cosmetic changes out of a functional fix; refactor in its own
  change and ticket.

## Definition of done (every ABAP change, not optional)

A change is not done, and is not offered for release, until all of these hold. If one cannot be
met (no system access, legacy code without seams), say which one and why; never skip silently.

1. **Unit tests with the change.** New or changed behaviour has ABAP Unit tests in the same
   transport: the happy path, the negative cases, and the bug being fixed (test first: it fails
   before the fix). See `guidelines/abap/unit-testing.md`.
2. **Dependencies replaced by test doubles.** Database, RFC, HTTP, time, user and other classes
   sit behind interfaces with constructor injection; the tests use doubles:
   `cl_abap_testdouble` (from 7.40 SP09), local fake classes (7.40 SP08 and below),
   `cl_osql_test_environment` / `cl_cds_test_environment` for SQL and CDS (7.51+). Legacy code
   without a seam: add the seam in the change (extract an interface) rather than skip the test.
3. **Checks green, results reported:** syntax check, activation, ABAP Unit, ATC (and abaplint
   where the repository has it, configs in `templates/abaplint/`). Report the real numbers
   ("12 tests, 0 failures; ATC 0 priority 1/2"). "Compiles" is not "works".
4. **Independent review.** Run the `abap-code-review` workflow (`guidelines/abap/code-review.md`);
   anything beyond a few lines goes to the read-only `abap-reviewer` agent with the diff and the
   goal, not with your conclusions. Fix blockers, re-run step 3.
5. **Notes.** Record in the project notes what you learned about the system that the code does
   not show; follow the project's ticket and decision-record rules.
