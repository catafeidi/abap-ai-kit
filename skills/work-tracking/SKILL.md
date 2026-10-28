---
name: work-tracking
description: Use when development or investigation work touches the project's tracker, code host or CI - finding or creating the ticket for a task, linking branch / commits / pull request to it, recording open points as tickets, updating or closing tickets, checking pipeline results. Works with Jira, Azure Boards or GitHub Issues and GitHub, Azure Repos or GitLab, as declared in the project's integrations.json.
---

# Work tracking

Rules: kit `rules/work-tracking.md`. Adapters and commands: kit `guidelines/integrations.md`.
Configuration: `<project>/integrations.json` (`tracker`, `code`, `ci`). If `tracker.preferSkill`
names a project skill (team templates), use that skill for creating and editing tickets and this
one only for the flow around it.

## At the start of a task
1. Read `integrations.json`. No `tracker` block: skip the ticket steps and say so once.
2. Find the ticket: by key if the user gave one, else search the project for the topic. None
   fits: draft one (type by the rules, defaults from the config) and ask before creating it.
3. Read the ticket: description, acceptance criteria, links, latest comments. State in one line
   what it asks for and anything that conflicts with the request.
4. Code host: check the account (`code.account`), create the branch with the ticket key
   (`code.rules.branch`).

## While working
- A new open point, risk or follow-up: draft a linked ticket (Spike / Bug / Story) and list it
  for the user; create after confirmation. Record the key in the project notes.
- Commits and pull requests carry the key (`code.rules.prTitle`). Follow project rules that forbid
  hand-made pull requests for some code (e.g. ABAP released through SAP).

## At the end
1. CI: read the pipeline result of the change (`gh pr checks` / `gh run view --log-failed`,
   Azure Pipelines runs); a red result is reported, not hidden.
2. Compare the ticket with what was built: done / partly / needs change / decision needed.
3. Draft the ticket update (comment, fields, transition with the evidence the acceptance
   criteria ask for) and send it only after the user agrees.
4. Write the ticket state into the topic's notes (Now / Next).

## Never
- Invent a ticket key, field ID or transition ID. Look it up, then propose adding it to
  `integrations.json`.
- Write to the tracker on a day or in a way the project rules forbid (`rules.weekdaysOnly`).
