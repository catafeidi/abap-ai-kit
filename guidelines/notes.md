# Project notes: structure and habits

Every project folder (next to the kit, never in the kit repository) uses the same shape, so any AI
finds things without being told. Create it with `scripts/new-project.ps1 -Name <name>`.

```
<project>/
  AGENTS.md            instructions for AI tools: systems, conventions, folder map (short)
  CLAUDE.md            "@AGENTS.md" + Claude-only mechanics (MCP servers, project skills)
  README.md            human map of the folder
  integrations.json    code host, tracker, wiki, CI, CRM of the project (guidelines/integrations.md)
  .claude/             project skills, agents, settings, CONTINUITY.md
  support/
    cases/<case-id>/   one folder per support case: case.md + attachments
    kb/                reusable knowledge: answers, playbooks, root causes
  products/<product>/  ongoing product development (README, STATUS, decisions, specs)
  repos/<repo>/        code checkouts (Fiori apps, abapGit repositories): each its own Git
                       repository with its own remote, ignored by the project notes
  implementations/<topic>/   one folder per big implementation, spike or feature
  bugs/<ticket>-<slug>.md    analysed defects that are not a whole implementation
  docs/                presentations, documents, exported specs
  tools/               scripts and executables the project needs (MCP launchers, ...)
  _inbox/              unsorted files; sort them, do not let them grow
```

Each project folder is its **own local git repository without a remote** (`new-project.ps1` does
it): AI tools key project memory and project-scoped MCP servers on the git root, and you get a
history of the notes. Its `.gitignore` keeps customer evidence, attachments and binaries untracked.
Commit the notes now and then (`git add -A; git commit -m "notes"`).

## Habits
- One topic, one folder, one `README.md` that says goal, status, ticket keys and where the code is.
- Decisions go into a decisions file (`DECISIONS.md` or ADRs) with the reason; settled decisions
  are not re-opened without new facts.
- A support case gets `case.md` from the case template: last read, problems, symptoms,
  established vs not verified, root cause, notes and replies sent. When the root cause is
  reusable, add or update an entry in `support/kb/`.
- Notes say what the code or the ticket does not: facts learned on the system, why a choice was
  made, what was tried and failed.
- No secrets, no customer passwords; customer data only as far as the analysis needs it.
- No generation dates or "last updated" stamps in documents that will be shared.
