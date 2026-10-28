#!/usr/bin/env python3
"""PreToolUse / mcp__.*|Bash|PowerShell hook: guard writes and transport releases on SAP systems.

Two guards, both outside the model's judgement:

1. Read-only systems (per project). `<project>/.claude/sap-guard.json` names the MCP servers
   and ADT destinations that must not be changed:
       {"read_only_servers": ["sap-dev-ref"], "read_only_destinations": ["DEV_"]}
   - Any tool of a read-only server: write-like tools and the vsp `SAP` tool with
     edit / create / delete -> deny; RFC calls and i18n -> ask (an RFC call can write).
   - Tools of other servers (e.g. the official ADT MCP server): a write-like tool whose
     destination field starts with a read-only prefix -> deny.
   No config file: this guard is off.

2. Transport release (every project): releasing a task or request pushes and imports, so it
   always asks: an RFC call of a release function module, a tool with "release" in its name,
   or a shell command running a release script or function.

Fails open on any parse error. Wire it on PreToolUse with matcher "mcp__.*" and on
"Bash|PowerShell". Tests: hooks/tests/test_sap_guard.py. See hooks/README.md.
"""
import json
import os
import re
import sys

WRITE_ACTIONS = {"edit", "create", "delete"}
ASK_ACTIONS = {"i18n"}
RELEASE_FMS = re.compile(r"^(TR_RELEASE_REQUEST|TRINT_RELEASE_REQUEST|BAPI_CTREQUEST_RELEASE|"
                         r"CTS_API_RELEASE_\w+|TR_RELEASE_\w+)$", re.I)
WRITE_TOOL = re.compile(r"(create|update|write|set|change|edit|delete|activate|lock|patch|insert|"
                        r"release|move|rename|import|install|clone|deploy)", re.I)
RFC_TOOL = re.compile(r"rfc", re.I)
RELEASE_SHELL = re.compile(r"(_release\.py|TR_RELEASE_REQUEST|BAPI_CTREQUEST_RELEASE)", re.I)
SHELL_TOOLS = {"Bash", "PowerShell"}


def decide(decision, reason):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": decision,
        "permissionDecisionReason": reason}}))
    sys.exit(0)


def allow():
    print("{}")
    sys.exit(0)


def load_config():
    for root in (os.environ.get("CLAUDE_PROJECT_DIR"), os.getcwd()):
        if not root:
            continue
        path = os.path.join(root, ".claude", "sap-guard.json")
        if os.path.isfile(path):
            try:
                with open(path, encoding="utf-8-sig") as handle:
                    return json.load(handle)
            except Exception:
                return {}
    return {}


def destination_values(value, key=""):
    """Values of fields whose name mentions a destination or system id, at any depth."""
    if isinstance(value, dict):
        for child_key, child in value.items():
            yield from destination_values(child, child_key)
    elif isinstance(value, list):
        for child in value:
            yield from destination_values(child, key)
    elif isinstance(value, str) and re.search(r"dest|system", key, re.I):
        yield value.upper()


def function_names(tool_input):
    """Function module names an RFC-style tool is asked to call."""
    for key in ("target", "function", "functionName", "function_name", "fm", "name"):
        value = tool_input.get(key)
        if isinstance(value, str) and value.strip():
            yield value.split()[-1]


try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

tool = data.get("tool_name", "")
tool_input = data.get("tool_input", {}) or {}
config = load_config()
read_only_servers = {s.lower() for s in config.get("read_only_servers", [])}
read_only_destinations = [d.upper() for d in config.get("read_only_destinations", [])]

if tool in SHELL_TOOLS:
    if RELEASE_SHELL.search(tool_input.get("command", "")):
        decide("ask", "Transport release: releasing pushes to Git and starts imports. "
                      "Confirm that the user asked for this release.")
    allow()

match = re.match(r"^mcp__(.+?)__(.+)$", tool)
if not match:
    allow()
server, name = match.group(1).lower(), match.group(2)
read_only_server = server in read_only_servers

if name == "SAP":  # vsp in hyperfocused mode: one tool, the action says what it does
    action = str(tool_input.get("action", "")).lower()
    params = tool_input.get("params") or {}
    rfc_call = action == "rfc" and str(params.get("op", "")).lower() == "call"  # no op = describe
    if rfc_call and any(RELEASE_FMS.match(fm) for fm in function_names(tool_input)):
        decide("ask", f"Transport release through RFC on {server}. Confirm that the user asked for it.")
    if read_only_server and action in WRITE_ACTIONS:
        decide("deny", f"{server} is read-only for this project (.claude/sap-guard.json): '{action}' is "
                       "not allowed. Prepare the change as a file for the user to apply, or use the "
                       "development system named in AGENTS.md.")
    if read_only_server and (rfc_call or action in ASK_ACTIONS):
        decide("ask", f"{server} is read-only for this project: '{action}' can change data. "
                      "Confirm it only reads.")
    allow()

# every other MCP tool: the tool name says what it does
if RFC_TOOL.search(name):
    if any(RELEASE_FMS.match(fm) for fm in function_names(tool_input)):
        decide("ask", f"Transport release through RFC ({tool}). Confirm that the user asked for it.")
    if read_only_server:
        decide("ask", f"{server} is read-only for this project: {name} can change data. Confirm it only reads.")
    allow()
if WRITE_TOOL.search(name):
    if re.search("release", name, re.I):
        decide("ask", f"Transport release ({tool}). Confirm that the user asked for this release.")
    if read_only_server:
        decide("deny", f"{server} is read-only for this project (.claude/sap-guard.json): {name} is not allowed.")
    hit = next((prefix for value in destination_values(tool_input)
                for prefix in read_only_destinations if value.startswith(prefix)), None)
    if hit:
        decide("deny", f"Destination {hit}* is read-only for this project (.claude/sap-guard.json): "
                       f"{name} is not allowed there.")
allow()
