---
name: support-case
description: Use when analysing a customer support case or ticket in any project - a case number or CRM link, "look at this customer problem", preparing an answer or a debug session. Generic method (case folder, evidence, root cause, answer, knowledge entry) with the CRM as an adapter (Salesforce via the sf CLI). A project skill for support cases, if the project has one, takes precedence.
---

# Support case

If the project has its own support-case skill (see its `AGENTS.md` / `.claude/skills`), use that
one; this is the generic method. Notes structure: kit `guidelines/notes.md`. CRM adapter:
`crm` in `<project>/integrations.json` and kit `guidelines/integrations.md`.

## Steps
1. **Case folder first:** `support/cases/<case-id>/`. If `case.md` exists, read it before
   fetching anything; it says what is already known. Else create it from the template.
2. **Fetch from the CRM** with the adapter (Salesforce: `sf data query -o <alias>` on Case,
   EmailMessage, FeedItem, ContentDocumentLink / ContentVersion). Save raw exports under
   `support/cases/<id>/sf/` (kept out of git) and attachments under `attachments/`.
3. **Open every attachment** (logs, screenshots, exports). Several problems in one case: split them.
4. **Search before concluding** (skill `find-information`): kb and solved-case entries, wiki,
   tracker (existing bug for the symptom), code.
5. **Root cause with evidence:** quote the log line, field or source line; separate
   *established* from *not verified* in `case.md`.
6. **Deliver:** what the case is, why it looks like that, root cause, what to tell the customer
   (numbered steps), what is not verified. Draft any reply or internal note and send it only
   after the user agrees, through the channel the project names.
7. **Knowledge:** reusable root cause -> kb entry; anonymised if it leaves the project (no case
   numbers, names, hosts, raw messages). A product defect -> tracker ticket (`work-tracking`).
8. Update `case.md` every visit (status, last read, open points).

## Never
- Paste customer personal data into tickets, wiki pages, prompts or shared notes beyond need.
- Log in to the CRM for the user, or store a token.
