# Work tracking (every project with a tracker)

Applies when the project has a `tracker` in `integrations.json` (see `guidelines/integrations.md`).
The project config and its own skills give the IDs, templates and exceptions.

- **Everything has a ticket.** New work, a follow-up, a deferred part: find or create the ticket
  as soon as it comes up. Its key goes into branch names, commit messages and pull request titles.
- **Open points become tickets.** Unknown or decision needed -> investigation ticket (Spike);
  wrong behaviour -> Bug; planned work outside the current slice -> Story / Technical Story.
  Link it to the ticket it blocks or belongs to.
- **Check before you write.** Search for an existing ticket before creating one; read the thread
  before commenting (comments often cannot be deleted). Never invent a ticket key or an ID.
- **Every external write is confirmed** (create, edit, comment, transition, page publish, pull
  request), unless the user said to proceed for that item. Draft first, show it, then send.
- **Keep the ticket in step with the work:** read it at the start of a task, compare it with what
  was built at the end, and report plainly: done / partly done / needs changing / decision needed.
  Close only with the user's agreement and the evidence the acceptance criteria ask for.
- **Use the project's words:** ticket types, board process (Kanban: no "sprint"), field names.
- Project rules in `integrations.json` (`rules`) apply on top, e.g. `weekdaysOnly`: no tracker
  writes on Saturday or Sunday; prepare the text and write it on the next weekday.
