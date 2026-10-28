---
name: spec-intake
description: Use when a functional or technical specification arrives as a Word document (.docx) - a RICEFW, a technical specification attached to a feature or epic, "read this spec", "what do I need to build for this", "break this spec into tasks", "check the tasks against the spec". Converts it to Markdown without struck-through text and with the reviewers' comments, files it in the topic folder, lists the objects to build and the open questions, and maps it to the tickets.
---

# Specification intake

Specs are reviewed in Word: deleted content is often only struck through, and reviewers add
requirements as comments. Reading the .docx as plain text gets both wrong.

## 1. Get the document
- From the ticket (attachment) or from the user. When the ticket only links to SharePoint or
  another store the tools cannot open, ask the user to download the .docx; do not guess its content.
- Topic folder: `<project>/implementations/<ticket>_<slug>/` (`guidelines/notes.md`). Create it with
  a `README.md` from `templates/project/implementations/_template/README.md` if it is missing.
  Keep the .docx there.

## 2. Convert
`python <kit>/scripts/docs/docx_to_md.py <spec.docx> <topic folder>/<spec name>.md`
- Struck-through text and tracked deletions are dropped (`--keep-strike` keeps them, for a diff).
  The script prints how many runs it dropped: say so, so the user can object.
- Word comments appear as `> **Comment (author):** text` under their paragraph. **Comments are
  requirements** until the author says otherwise; they often rename objects or remove parts.
- Images become `[image: name]`; open the image (`word/media/` in the .docx) when it carries a
  requirement (screens, flows) and describe it in the notes.

## 3. Read it as a developer
Write into the topic `README.md` (or `NOTES.md`), keeping established and assumed apart:
- **Scope:** which sections are in this phase, which are not.
- **Objects to build:** one table, type / proposed name / purpose / spec section. Check every
  proposed name against the project's naming rules and every SAP object against the release
  (`scripts/abap/released-api.py` for ABAP Cloud).
- **Comment decisions:** each reviewer comment and what it changes.
- **Open questions:** contradictions, missing values, names that break conventions, statements
  that do not hold on the system (check facts on the system before listing them).

## 4. Map to the tickets
With `work-tracking`: read the feature / epic, its stories and tasks. Map every object and step to a
task; list the gaps as proposed task titles (with an estimate if the project wants one). **Create
nothing before the user agrees**, and follow the project's rules for new tickets (`integrations.json`,
project `AGENTS.md`).

## 5. Keep it current
A new spec version: convert it next to the old one and diff the Markdown files; record what
changed in the topic notes before changing code.
