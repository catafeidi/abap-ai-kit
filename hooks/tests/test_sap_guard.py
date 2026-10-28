"""Tests for sap-guard.py. Run: python hooks/tests/test_sap_guard.py"""
import json
import os
import subprocess
import tempfile

HOOK = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sap-guard.py")

PROJECT = tempfile.mkdtemp()
os.makedirs(os.path.join(PROJECT, ".claude"))
json.dump({"read_only_servers": ["sap-ref"], "read_only_destinations": ["REF_"]},
          open(os.path.join(PROJECT, ".claude", "sap-guard.json"), "w"))
NO_CONFIG = tempfile.mkdtemp()

CASES = [  # (project, tool, input, expected decision; None = allowed)
    # vsp single-tool mode on a read-only server
    (PROJECT, "mcp__sap-ref__SAP", {"action": "edit", "target": "CLAS ZCL_X", "params": {"source": "x"}}, "deny"),
    (PROJECT, "mcp__sap-ref__SAP", {"action": "create", "target": "PROG ZX"}, "deny"),
    (PROJECT, "mcp__sap-ref__SAP", {"action": "read", "target": "CLAS ZCL_X"}, None),
    (PROJECT, "mcp__sap-ref__SAP", {"action": "grep", "params": {"pattern": "x"}}, None),
    (PROJECT, "mcp__sap-ref__SAP", {"action": "rfc", "target": "STFC_CONNECTION"}, None),   # describe
    (PROJECT, "mcp__sap-ref__SAP", {"action": "rfc", "params": {"op": "read_table"}}, None),
    (PROJECT, "mcp__sap-ref__SAP", {"action": "rfc", "target": "Z_FM", "params": {"op": "call"}}, "ask"),
    # vsp granular mode on a read-only server
    (PROJECT, "mcp__sap-ref__WriteSource", {"object_url": "/x"}, "deny"),
    (PROJECT, "mcp__sap-ref__ImportFromFile", {"file": "x"}, "deny"),
    (PROJECT, "mcp__sap-ref__CallRFC", {"function": "Z_FM"}, "ask"),
    (PROJECT, "mcp__sap-ref__GetSource", {"object_url": "/x"}, None),
    # other servers
    (PROJECT, "mcp__sap-dev__SAP", {"action": "edit", "target": "CLAS ZCL_X"}, None),
    (PROJECT, "mcp__sap-dev__SAP", {"action": "rfc", "target": "TR_RELEASE_REQUEST", "params": {"op": "call"}}, "ask"),
    (PROJECT, "mcp__sap-dev__CallRFC", {"function": "TR_RELEASE_REQUEST"}, "ask"),
    (PROJECT, "mcp__adt__abap_update_source", {"destination": "REF_100_USER_EN", "uri": "x"}, "deny"),
    (PROJECT, "mcp__adt__abap_update_source", {"destination": "DEV_100_USER_EN"}, None),
    (PROJECT, "mcp__adt__abap_update_source", {"destination": "DEV_100_USER_EN", "source": "* see REF_100"}, None),
    (PROJECT, "mcp__adt__abap_get_source", {"destination": "REF_100_USER_EN"}, None),
    (PROJECT, "mcp__adt__abap_release_transport", {"destination": "DEV_100_USER_EN"}, "ask"),
    # shells
    (PROJECT, "Bash", {"command": "python dev_release.py DEVK900001"}, "ask"),
    (PROJECT, "PowerShell", {"command": "python dev_release.py DEVK900001"}, "ask"),
    (PROJECT, "Bash", {"command": "git status"}, None),
    # no config: only the release guard is active
    (NO_CONFIG, "mcp__sap-ref__SAP", {"action": "edit", "target": "CLAS ZCL_X"}, None),
    (PROJECT, "mcp__jira__createIssue", {"summary": "x"}, None),
]
fails = 0
for project, tool, tool_input, expected in CASES:
    env = dict(os.environ, CLAUDE_PROJECT_DIR=project)
    out = subprocess.run(["python", HOOK], input=json.dumps({"tool_name": tool, "tool_input": tool_input}),
                         capture_output=True, text=True, env=env, cwd=project).stdout
    got = (json.loads(out or "{}").get("hookSpecificOutput") or {}).get("permissionDecision")
    fails += got != expected
    print("ok  " if got == expected else "FAIL", tool, tool_input.get("action", ""), "->", got)
print("failures:", fails)
raise SystemExit(1 if fails else 0)
