# Working on live SAP systems (MCP, ADT, RFC)

- **Know which system you are on.** Call the connection or system info tool at the start of the
  session and name the system and client in every claim ("verified on XYZ client 100").
  The project `AGENTS.md` names the source of truth per namespace; a test system may hold an older
  version of the code.
- **Release level from `CVERS`**, never from an add-on version text.
- **Read before write.** Writes only in the packages and systems the project allows, always with
  an explicit transport request. Never write to a system the project marks read-only.
- **No passwords in tool calls, configs or files.** Logon happens in the client tool or through
  environment variables.
- **Live data is customer data.** Do not copy table contents into notes, tickets or prompts beyond
  what the task needs; anonymise in shared documents.
- **Releasing a transport is outward-facing** (it may push to Git or start imports): only when the
  user asks.
- When a tool cannot reach a system (VPN, port, handler missing), say so and say which fallback
  system you used instead. Do not conclude that something does not exist.

## How ADT and ADT-based MCP servers behave (verified in practice)
- **The syntax check is not the release check.** It stops at the first error (to validate code
  after a line that depends on a not-yet-activated object, remove that line and check again), and
  it passes code that uses objects the system blocks for ABAP Cloud. Only ATC with the clean core
  variant, or activation, shows those.
- **Activation and unit tests run in the development client.** A test client whose settings forbid
  repository changes (message `TK730`) is still the right place for data checks; mark it read-only
  in the project.
- **Server settings are read at start.** After changing an MCP server's environment (for example a
  switch that allows transportable edits) restart or reconnect that server; until then the old
  behaviour stays.
- **A blocked write can leave a lock.** Some servers take the ADT lock before checking whether the
  write is allowed. The next attempt then fails with "user X is currently editing"; a lock handle
  from another session cannot release it, the user deletes it in `SM12`.
- **Locks are stateful.** ADT keeps the lock in a stateful HTTP session. Where the client does not
  keep that session between LOCK and PUT (seen on SAP_BASIS 7.40), creating an object works but
  every source update fails with an invalid lock handle. Do not retry: plan the source as a file the
  user pastes.
- **Not every object type can be written.** If the server cannot create an object type (often
  domains, data elements, function groups), generate it with a report or class using the XCO
  library (`XCO_CP_GENERATION`) on releases that have it, or hand the definition to the user.
- **OData V4 service group publishing is per client** (`/IWFND/V4_ADMIN`). Published in the
  development client does not mean available in the test client: a Fiori app then fails with
  "Service group not published" and HTTP 404 on `$metadata`.
- **Cross-client reads:** `SELECT ... FROM ... USING CLIENT '<nnn>'`, with `USING CLIENT` after the
  whole `FROM` / `JOIN` clause.
