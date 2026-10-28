---
name: find-information
description: Use when a question needs facts from the project's own sources - "where is X documented", "how does Y work in our product", "was this solved before", "what did we decide about Z", "which ticket covers this". Searches project notes, knowledge base, team repositories, wiki (Confluence / Azure Wiki), tracker (Jira / Azure Boards / GitHub Issues) and CRM in a fixed order, as declared in integrations.json, and answers with the source of each fact.
---

# Find information

Search order and adapters: kit `guidelines/integrations.md` (section "Where information is").
Configuration: `<project>/integrations.json` (`knowledge`, `code.repos`, `wiki.spaces`,
`tracker.project`, `crm`).

## Steps
1. Restate the question in one line and pick search terms: object names, error texts, ticket keys,
   product terms. Use the project's own words (from `AGENTS.md` and the notes).
2. Go down the order and stop when the answer is established by a primary source:
   notes -> knowledge list -> code -> wiki -> tracker -> CRM (support questions only) -> web.
   Local files first (grep), then the online tools.
3. Prefer the newest authoritative source: code and system facts beat documents, decisions beat
   discussions, the project's precedence rules (in `AGENTS.md`) beat the order above.
4. Answer: the facts, each with its source (file path, page title + link, ticket key, case
   number); conflicts between sources and which one wins; what you did not find.
5. If the answer was hard to find, propose a note or kb entry so the next search is short.

## Keep it cheap
- Search, then read only the hits; do not load whole knowledge packs or spaces.
- Customer data from the CRM stays in the case folder; quote only what the answer needs.
