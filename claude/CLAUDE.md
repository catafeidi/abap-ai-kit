# Claude Code specifics (loaded after the kit AGENTS.md)

`~/.claude/CLAUDE.md` imports the kit `AGENTS.md` and this file (written by `scripts/install.ps1`).
Everything tool-neutral belongs in `AGENTS.md`; only Claude Code mechanics go here.

## How the kit is wired into Claude Code

- `~/.claude/rules`, `~/.claude/hooks`, `~/.claude/agents`, `~/.claude/templates` and each kit
  skill under `~/.claude/skills/<name>` are directory junctions into the kit. Edit the kit, never
  the junction target by another path, and commit in the kit repository.
- Hooks in `hooks/` (wired in `~/.claude/settings.json`) enforce the sharp edges: `rm -rf`,
  `.env` edits, injection shapes, gitleaks before a push. A rule states intent; a hook enforces it.
- Project-only skills and agents live in `<project>/.claude/skills` and `<project>/.claude/agents`.
  A project agent with the same name as a kit agent overrides it (for example a project-specific
  `abap-reviewer`).
- MCP servers for SAP systems are project-scoped (`claude mcp add -s local` or `.mcp.json` in the
  project), never user-scoped: they belong to one landscape. Passwords come from environment
  variables, never from `.mcp.json`.

## Continuity (per project)

Projects with ongoing work keep a tactical ledger at `<project>/.claude/CONTINUITY.md`
(template: `templates/CONTINUITY.md.template`): goal, phase, done/now/next, decisions, open
questions. Read it at session start; update Now/Next before ending a work session.

## Learning loop

When I correct you: memory records the sticky note, and if the cause is a broken skill, rule,
guideline or this file, log a work order in `~/.claude/learnings/LEARNINGS.md` (machine-local; create it if missing) naming the exact
kit file to change. Check `REJECTED.md` before proposing an edit I
already vetoed. Generic lessons (true in any
project) go into the kit; project facts go into project memory or project notes.
