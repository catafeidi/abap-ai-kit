# Sessions and notes

The project folder is the memory that survives sessions, machines and AI tools. A session is
disposable; the notes are not. Do this without being asked.

## Write as you go, in the project folder
- After every meaningful step (a finding, a root cause, a decision, a working build, a dead end)
  update the file that owns the topic, in the same turn:
  support case -> `support/cases/<id>/case.md`; product -> `products/<p>/STATUS.md` (+ decisions);
  implementation or spike -> `implementations/<topic>/README.md`; defect -> `bugs/<ticket>-<slug>.md`.
  No topic file yet: create it from the structure in `guidelines/notes.md`.
- Keep *established* and *assumed / not verified* separate.
- Before the session ends, or when the user switches topic: write **Now / Next** (where we stopped,
  the first concrete step to resume, open questions) in the topic file or `.claude/CONTINUITY.md`.
  The next session must be able to start from the notes alone.

## One session, one topic
- Start a new session for a new task or topic, after a task is finished, and when the context is
  more than about half full or has been compacted once. Say so when you notice it ("good point to
  start a new session; Now/Next is written in X").
- At session start in a project: read `AGENTS.md`, `.claude/CONTINUITY.md` if present, and the
  topic file of the task before doing anything else.

## Notes vs memory
- Project knowledge (facts about systems, code, cases, decisions) goes into project notes:
  readable by every AI tool, versioned in the project's local git, available on the next machine.
- Tool memory (Claude auto-memory and similar) is only for short preferences and corrections about
  how to work, and pointers to notes. Do not keep project knowledge only in memory.
- A lesson true in every project goes into the kit (`rules/` or `guidelines/`), not into memory.
