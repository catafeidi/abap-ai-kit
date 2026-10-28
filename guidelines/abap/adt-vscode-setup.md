# ABAP Development Tools for VS Code + MCP: setup on a machine

Gives every AI tool the SAP systems of a project through SAP's official ADT MCP server:
Copilot in VS Code directly, Claude Code through the project's `.mcp.json`. One run per project
and machine; safe to repeat.

**AI assistants:** when the user asks to set up SAP / ADT access, run step 3 for the project,
show the user the [MANUAL] lines of the output, and stop at the password: never ask for it.

## Steps

| # | Step | Who | How |
|---|---|---|---|
| 1 | Network to the SAP systems (VPN, Cloud Connector, ...) | **MANUAL** | As your company requires. Without it the logon in step 5 fails, nothing else does. |
| 2 | Kit installed | AUTO, once per machine | `powershell -ExecutionPolicy Bypass -File <kit>\scripts\install.ps1` |
| 3 | Run the setup for the project | **MANUAL** start, then AUTO | `python <kit>\scripts\adt-vscode\setup_adt_vscode.py --project <project folder> --sap-user <YOUR_SAP_USER>` (add `--dry-run` first to see what it will do) |
| 3a | VS Code present, version ≥ 1.109.5 | AUTO check | If missing or old the script says [MANUAL]: install VS Code from code.visualstudio.com with "Add to PATH", or Help > Check for Updates; run step 3 again. |
| 3b | Extension `sapse.adt-vscode` | AUTO | `code --install-extension sapse.adt-vscode`; on failure [MANUAL]: Extensions view, search "ABAP Development Tools". |
| 3c | Destinations (system, client, user; **no password**) | AUTO | From `<project>/tools/adt-destinations.json` into `%USERPROFILE%\.adtls\destinations.json`; existing ones kept, file backed up. No project file: [MANUAL] Command Palette > "ABAP: New Destination" (RFC for on-premise). |
| 3d | MCP server on, port, allow list for object changes | AUTO | VS Code user settings `adt.mcpServer.*`, packages from `<project>/tools/adt-access.json`; backed up. Settings file with comments: [MANUAL], the script prints the values. |
| 3e | Claude Code registration | AUTO | `<project>/.mcp.json` server `adt-vscode` (HTTP on localhost, token read at connect by `scripts/adt-vscode/adt_mcp_headers.py`, never stored). |
| 3f | Read-only systems for the AI | AUTO | `readOnlyDestinations` of `adt-access.json` into `<project>/.claude/sap-guard.json` (kit hook `sap-guard.py`). |
| 4 | Open VS Code | **MANUAL** | Open the project's `*.code-workspace` (File > Open Workspace from File) or the folder. The extension starts the MCP server; it runs only while VS Code is open. |
| 5 | Log on to each destination you need | **MANUAL**, once per destination | Open the destination (workspace folder `abap:/...` or the ABAP view); VS Code asks for the password and keeps the session. **Never give the password to an AI.** |
| 6 | Claude Code | **MANUAL** | Start `claude` in the project folder, approve the project server `adt-vscode` when asked, `/mcp` shows it connected. Not connected: VS Code closed (step 4) or `/mcp` > reconnect. |
| 7 | Copilot | none | VS Code Chat > Agent mode > tools: "ADT MCP Server" is provided by the extension. |
| 8 | Test | **MANUAL** | Ask the AI: "list the ADT destinations I am logged on to". Only logged-on destinations appear. |

## Project files (templates in kit `templates/project/tools/`)
- `tools/adt-destinations.json`: export of `%USERPROFILE%\.adtls\destinations.json` with your
  user replaced by `{{SAP_USER}}`. No passwords are in that file.
- `tools/adt-access.json`: `port`, `packages` (object changes allowed only there; the allow list
  is global in VS Code, not per destination), `readOnlyDestinations` (id prefixes the AI must
  not change, enforced by the hook).

## What stays with vsp (or another ADT HTTP client)
Table reads, RFC calls, reports, where-used and source grep, until the official server has them.
Configure those servers per project, passwords from environment variables, and list read-only
ones in `.claude/sap-guard.json` (`read_only_servers`).
