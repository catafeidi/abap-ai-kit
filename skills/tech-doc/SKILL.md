---
name: tech-doc
description: Use when the as-built technical documentation of an ABAP development has to be written or updated, usually as a Word document for the customer or the architecture board - "write the technical documentation", "tech doc for this RICEFW", "update the docx with the final objects", "export the documentation to Word". Writes it in Markdown from the live system and the topic notes, then builds the .docx with scripts/docs/md_to_docx.py (optionally on the company template).
---

# Technical documentation

The Markdown file is the source; the .docx is generated. Never edit the generated .docx by hand,
change the Markdown and build again.

## 1. Collect facts (do not write from memory)
- Topic notes: `<project>/implementations/<ticket>_<slug>/` (`README.md`, `NOTES.md`, the spec).
- The system: read the **active** source of every object (classes, CDS, behaviour definitions,
  service definitions and bindings, DDIC), the package and the transport. Name the system and
  client the facts come from.
- Test results: real counts from the last unit test and ATC runs.

## 2. Write `<ticket>_Technical_Documentation.md` in the topic folder
Default outline (drop sections that do not apply, keep the numbering):
1. **Introduction:** purpose, functional background, scope and assumptions, the stories / tickets.
2. **Solution architecture:** layers, language version and clean core level per package,
   wrappers and why, diagram as a list or table.
3. **Object inventory:** one table, object / type / package / purpose; transport.
4. **Data model:** tables, CDS views (key fields, associations), domains and data elements,
   message classes.
5. **One section per story:** what was built, the key logic in prose, short source excerpts only
   where they explain a rule (never whole classes).
6. **Security and authorization:** authorization objects, access controls, privileged access and
   why.
7. **Configuration and cutover:** customizing, business configuration, service publishing per
   client, manual steps per system.
8. **Testing:** unit tests (classes, methods, result), ATC result, functional test status.
9. **Open items and dependencies.**

Write in plain English for the next developer; established SAP terms; no generation dates or
"last updated" stamps; no passwords or personal data.

## 3. Build the Word document
`python <kit>/scripts/docs/md_to_docx.py <doc.md> [<doc.docx>] [--template <company.docx>]`
- `--template` takes the styles, header and footer of an existing company document and replaces
  its body; use the project's previous technical documentation or the official template.
- Needs `python-docx` (`python -m pip install python-docx`).
- Check the result: convert it back with `scripts/docs/docx_to_md.py` and compare the number of
  headings and table rows with the Markdown source; open it once in Word when it goes to a
  customer.
