# Adopting existing work into a kit project

Use when a developer already works with an AI assistant in some folder (specs, notes, sources,
scripts, MCP servers, skills, assistant memory) and wants it as a kit project. Goal: the kit
structure of `guidelines/notes.md`, **nothing lost**, every tool still working.

## Ground rules
- **Copy, never move or delete.** The old folder stays untouched as the backup; the developer
  deletes it after checking the new project. A running assistant session often has the old folder
  as its working directory, so moving it fails half-way on Windows anyway.
- **Show the plan before copying:** a table *source -> target* for every top-level item. Proceed
  after a yes (or directly when the developer said to go ahead).
- **Secrets stay where they are.** Never print, copy into files or commit passwords and tokens from
  MCP configs, `.env` files or settings; re-point configs instead of re-typing their values.
- Back up every global config file before editing it (`<file>.bak-kit-adopt`).

## Steps
1. **Kit installed?** If `AI_KIT_HOME` is not set: clone the kit, run `scripts/install.ps1 -DryRun`,
   show the result, run it, merge the `hooks` block of `templates/settings.example.json` into
   `~/.claude/settings.json`. Hooks need `gitleaks` on `PATH` (`winget install Gitleaks.Gitleaks`).
2. **Inventory (read only).** List the folder tree without `node_modules` / `.git` content; find
   nested git repositories (`.git` below the root) and their remotes; note binaries, generated
   documents and loose files in the root. Assistant config:
   - Claude Code: `<folder>/.claude/` (skills, agents, `settings.local.json`), `<folder>/.mcp.json`,
     project entries in `~/.claude.json` (`projects["<folder path>"].mcpServers`, names only),
     memory in `~/.claude/projects/<folder path with non-alphanumerics as ->/memory/`.
   - Copilot: `.github/copilot-instructions.md`, `.github/instructions/`, `.vscode/mcp.json`.
   - Codex / others: `AGENTS.md` and similar files in the folder.
3. **Name and place.** Ask only what cannot be found out: the project name (customer or programme,
   upper case) and, if not the default next to the kit, the parent folder. If the folder is itself a
   git repository with a remote, do not copy it: add `AGENTS.md` / `CLAUDE.md` at its root and keep
   the notes folders out of its Git (`AGENTS.md`, project layer).
4. **Create the skeleton:** `scripts/new-project.ps1 -Name <NAME>`.
5. **Map every item to its owner** (`guidelines/notes.md`):
   - one topic per folder in `implementations/<ticket>_<slug>/`: spec, technical documentation,
     local sources, review documents and the scripts that build its documents go together;
   - analysed defects -> `bugs/<ticket>-<slug>.md`; reusable system facts -> `support/kb/`;
   - checkouts with their own remote (for example Fiori apps) -> `workspace/<group>/<repo>/`,
     untouched, untracked by the project git;
   - MCP server binaries, generators and helper scripts -> `tools/`;
   - shared build dependencies (`package.json`, `node_modules`) stay at the project root, so scripts
     in the topic folders still resolve them;
   - unclear items -> `_inbox/`, listed in the report. Skip editor lock files (`~$*`).
6. **Copy and verify.** `robocopy <src> <dst> /E` per directory, `Copy-Item` per file. Then check
   that every source file (name + size) exists in the target; report the count, and any file missing.
7. **Fix paths.** Search the copy for the old folder path (scripts, `.bat`, markdown) and point it at
   the new location. Generated documents (`.docx`, `.html`) may keep the old path; mention them.
8. **Carry the assistant config over.**
   - Skills: generic ones (useful in every project) -> `<kit>/local/skills/` and re-run
     `install.ps1`; project-specific ones -> `<project>/.claude/skills/`; skip those the kit already
     ships. Agents -> `<project>/.claude/agents/` (a project agent overrides the kit agent); update
     any path in them that pointed at the old folder or at memory files.
   - MCP servers: Claude Code keys project-scope servers on the folder path, so they do not follow a
     copy. Copy the server entries in `~/.claude.json` from the old project key to the new one
     (forward slashes, e.g. `C:/work/kit/ACME`) with a script, changing only paths such as the
     binary location. Copy `.mcp.json` / `.vscode/mcp.json` as files.
   - Read-only systems: write `<project>/.claude/sap-guard.json` for the servers that must not
     change anything (test clients, quality systems).
9. **Memory to notes** (`rules/sessions-and-notes.md`). Assistant memory is keyed on the folder path
   too. Move project knowledge into notes: project / topic memories -> `implementations/<topic>/
   NOTES.md`, defects -> `bugs/`, system and tool facts -> `support/kb/`; turn `[[links]]` into
   relative links. Preferences and corrections (how to work) go into the memory folder of the new
   path, plus one memory that points at the notes.
10. **Fill the project files** from the inventory, asking only for gaps: `AGENTS.md` (context,
    systems and MCP servers, language version, namespaces and packages, conventions, working rules
    taken from the memories), `CLAUDE.md`, `integrations.json`, a `README.md` per topic (goal,
    tickets, status, code, contents), the project `README.md` index, `.claude/CONTINUITY.md`.
11. **Commit and scan.** `git add -A; git commit` in the project, then `gitleaks git .`; resolve real
    findings, report false positives.
12. **Report:** what went where, what was skipped and why, what changed in global config (with the
    backups), and the developer's next steps: start the assistant in the new folder, accept the
    folder trust prompt, check the MCP servers (`/mcp`), delete the old folder when satisfied.
