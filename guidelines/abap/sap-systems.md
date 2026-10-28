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
