# ABAP code review

Use for a diff, a transport request or task, a pull request, or a single object.
Claude Code: the `abap-code-review` skill runs this, with the read-only `abap-reviewer` agent for an
independent pass. SAP's own guide to running ABAP code reviews (what to look at, how to give
feedback, review culture) is vendored at `skills/abap-code-review/reference/ABAPCodeReview.md`
(SAP/styleguides, CC-BY-3.0); this checklist is the working subset.

## Inputs to collect first
- The change: diff (or the old and new source), the object list of the transport. For a pull
  request or non-ABAP change: base..head of the PR, not `git diff HEAD`; locally, staged,
  unstaged and untracked files; the CI status.
- The goal: ticket, acceptance criteria, specification section.
- The facts about the system the change depends on (release, tables, function module signatures),
  read on the system, not assumed. If a conclusion depends on a fact you could not check, say so.
- The evidence: syntax check, ATC / abaplint, unit test results, each with the system and client.

## Rules
- Be independent: the author's explanation is a claim to check, not a fact.
- Every finding names the file and line and a **concrete failure scenario**: input or state, then
  the wrong output, dump or risk. No scenario, no finding.
- Verify before you report. An active object cannot contain a syntax error; a construct that looks
  wrong may be an obsolete but valid form (`=>` in a logical expression is the old `>=`).
- Look the rule up before judging, and name it in the finding (Clean ABAP section, ABAP keyword
  documentation, guideline).
- Do not repeat what the linter (ATC, abaplint) already reports; look for what it cannot see.
- **Evidence before "clean":** never call code compiled, tested or ATC-clean without a result read
  in this review. Missing evidence is reported as missing. A result saying the object was not
  fully checked (dependency depth reached, class not found) is not a clean result.
- **Large change:** two independent passes as separate agents. Defects pass: without the
  specification. Specification pass: each requirement mapped to object and method; a requirement
  without code, or a deviation not documented, is a finding.

## Checklist (most severe first)
1. **Correctness:** edge cases (empty tables, initial values, CHAR length and truncation,
   conversion exits, time stamps and time zones, client handling), `sy-subrc` read too late or
   after a functional call, wrong `READ TABLE` key, loop changes to the table being looped.
   - `FOR ALL ENTRIES`: driver table empty (selects everything), not deduped, not all key fields
     selected (duplicate result rows are removed), driver and column types differ.
   - Table expressions raise `CX_SY_ITAB_LINE_NOT_FOUND`; they do not set `sy-subrc`.
   - Data references: assign to a `TYPE any` field symbol first; assigning straight to a typed one
     raises a type conflict that `sy-subrc` does not catch.
2. **Errors:** exceptions swallowed, `previous` lost, `OTHERS` ignored, success reported after a
   failure, messages that hide the cause, locks not released on the exception path.
3. **Security** (`guidelines/abap/security.md`): missing `AUTHORITY-CHECK` or unchecked `sy-subrc`
   after it, dynamic SQL or dynamic calls with caller input not escaped with `cl_abap_dyn_prg`
   (injection), file paths from input, unescaped HTTP output, secrets or other users' data in
   logs or responses, `CLIENT SPECIFIED` misuse.
4. **Side effects and cost:** `COMMIT WORK` in reusable code, locks not released, database or RFC
   calls on paths that do not need them, `SELECT` in a loop, missing key fields in `WHERE`.
5. **API contract:** function module and method signatures checked on the system (`FUPARAREF`);
   in ABAP Cloud projects every SAP object released (`scripts/abap/released-api.py`, level A, or a
   documented wrapper; `guidelines/abap/abap-cloud.md`).
   - Remote-enabled function modules: a new required parameter, a changed type or a new
     exception breaks external callers.
   - Refactoring: list every caller (where-used) of each changed method and state what would
     behave differently.
   - Release: the lowest target release decides the syntax. A newer construct (`int8`,
     `FINAL( )`, ...) is a finding; linters miss some, so read for them.
5a. **Design** (`guidelines/abap/architecture.md`): dependencies behind interfaces, layers called
   downward only, no hidden `COMMIT WORK`, no new god class or static utility dump.
5b. **Suppressions:** every new pseudo-comment or pragma has a proven false positive and a reason;
   otherwise it is a finding.
6. **Tests:** new branches and negative cases covered; each rule has a test that fails when the
   rule is removed; a test comparing two empty results proves nothing (assert the expected
   content or count); no test that locks in wrong behaviour; what can only be checked live is
   named as a known limit.
7. **Clean ABAP:** `guidelines/abap/clean-abap.md`. Group style-only findings into one, with 2-3
   examples.
8. **Consistency:** duplicate constants or helpers, a second style for the same thing, a package
   rule broken, coined terms.

## Report format
- Start with one sentence: blockers or none, and whether the change meets its goal.
- Findings grouped **Blocker**, **Should fix**, **Nit**, numbered, most severe first, each labelled
  **Confirmed** (read or run) or **Plausible**:
  `N. [file:line] (Confirmed) title: scenario. Fix: one line.`
- Then **Open questions / assumptions**, then the verdict: ready / ready after fixes / not ready.
  If the full test suite was not run, list what remains unverified.
- End with **What checks out**, so the author knows what was looked at.
- At most about 600 words unless asked for more.

## Review loop
Dedupe the findings of all passes, fix the confirmed ones, re-run the review on the changed
objects.
