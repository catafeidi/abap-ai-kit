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
   - **Incremental visit:** read only items newer than **Last read** in `case.md`. Re-read older
     ones only when new input contradicts **Established**.
   - **After a send:** check that the outgoing email exists in the CRM and carries the promised
     attachments.
3. **Split the problems.** One case may hold several (a reopened case often brings a different
   symptom, system or contact): list them as P1, P2... in `case.md` and keep them apart.
4. **Open every attachment** (logs, screenshots, exports).
   - Prefer the full artifact to a screenshot of it: a screenshot of a log shows the last lines.
   - Unpack containers (zip, archives) and open the nested files.
   - Dedupe images re-embedded by quoted replies; skip signature logos.
5. **Search before concluding** (skill `find-information`): kb and solved-case entries, past
   cases in the CRM with the same symptom, wiki, tracker (existing bug for the symptom), code.
6. **Root cause with evidence:** quote the log line, field or source line; separate
   *established* from *not verified* in `case.md`. Name the system and client a fact was
   verified on, after a connection check; say so when it is not the system that holds the
   source of truth.
7. **Deliver:** what the case is, why it looks like that, root cause, what to tell the customer
   (numbered steps), what is not verified. Always write the reply to the customer as a file
   in the case folder (`reply-draft-<date>.txt`), in the language of the thread, plus an
   English copy when the thread is in another language. Files to send are attached to the
   email itself, never only uploaded to the case. Send only after the user agrees, through the
   channel the project names; record date, content, file and attachments in `case.md`.
8. **Internal note** (when the CRM has internal notes): write `note-draft.txt` in plain text for
   colleagues. Post only after the user agrees; confirm the audience is internal; check the feed
   for an existing post before posting again; record it in `case.md`.
9. **Knowledge:** reusable root cause -> kb entry; anonymised if it leaves the project (no case
   numbers, names, hosts, raw messages). A product defect -> tracker ticket (`work-tracking`).
   Progress of this ticket stays in the case folder; facts still true after the case is closed
   go to the knowledge base or memory.
10. Update `case.md` every visit: status, open questions, not-verified items carried forward,
    and **Last read** with its time zone (CRM API times are often UTC).

## Common traps
- "0 rows, no error": check filter values for a missing conversion (leading zeros, conversion
  exits) and checks that write a log and return without raising.
- Read the whole method, not the context around a search hit.
- Judge a candidate fix by its code change, not by its ticket title.
- Concluding before searching past cases in the CRM for the same symptom (step 5).

## Never
- Paste customer personal data into tickets, wiki pages, prompts or shared notes beyond need.
- Log in to the CRM for the user, or store a token.
