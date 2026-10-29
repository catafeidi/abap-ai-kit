---
name: abap-code-review
description: Use when asked to review ABAP - a diff, a transport request or task, a pull request, a class / function module / program, or "check my ABAP before release". Collects the change and its goal, checks facts on the system, runs an independent reviewer pass, and reports findings ranked blocker / should fix / nit with concrete failure scenarios.
---

# ABAP review

SAP's code review guide: `reference/ABAPCodeReview.md` (read the section that fits when the
review is about process or feedback). The checklist and report format are in the kit guideline
`guidelines/abap/code-review.md`
(kit root: environment variable `AI_KIT_HOME`). Style rules: `guidelines/abap/clean-abap.md`; full SAP guide:
the `clean-abap` skill. This skill is the workflow around them.

## Steps

1. **Scope.** Identify what is reviewed: diff, transport objects, PR, or objects. Read the project
   `AGENTS.md` for release level, namespaces, systems and any project override of the checklist.
2. **Collect.** Get the old and new source (git diff, ADT, the system's version history) and the
   goal: ticket, acceptance criteria, specification section. Pull request or non-ABAP change:
   base..head of the PR (not `git diff HEAD`), staged, unstaged and untracked files, CI status.
3. **Check facts on the system** the change depends on, when a system is reachable: function
   module parameters (`FUPARAREF`), table key fields, data elements and lengths, release level
   (`CVERS`), where-used of each changed method. Write down which system and client you checked
   on. Read the syntax check, ATC / abaplint and unit test results yourself; what you did not
   read is reported as missing, not as clean.
4. **Independent pass.** For anything bigger than a few lines, give the `abap-reviewer` agent the
   diff, the new sources, the goal and the facts from step 3, without your own conclusions. For a
   large change run two agents: a defects pass without the specification and a specification
   pass (requirement -> object and method). Then do your own pass with the same checklist.
5. **Verify** each finding against the source before reporting it; drop findings without a
   concrete failure scenario. Dedupe across passes; label each Confirmed or Plausible.
6. **Report** in the format of the guideline, with open questions and the verdict. If the user
   asked for fixes, fix confirmed findings (blockers first), re-run syntax check, unit tests and
   ATC, report the real results, and review the changed objects again.
