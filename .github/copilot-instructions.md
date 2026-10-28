# GitHub Copilot instructions

Follow the shared kit instructions in `AGENTS.md` at the root of this repository (kit root
in the environment variable `AI_KIT_HOME`): identity, hard defaults, the always-on rules in `rules/`, and the routing table
that says which file in `guidelines/` to read for the task. In a project folder, also read that
project's `AGENTS.md`; the more specific layer wins.

Short version for every chat:
- Reply in English. Direct answer with one recommendation.
- No secrets in code, config, commits or chat. No force push, no recursive deletes, ask before
  anything public or irreversible.
- ABAP: write for the project's release level, follow `guidelines/abap/development.md` and
  `guidelines/abap/clean-abap.md`; review with `guidelines/abap/code-review.md`.
- Use established terms; do not invent names.
