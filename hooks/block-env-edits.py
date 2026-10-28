#!/usr/bin/env python3
"""PreToolUse / Edit|Write hook: block edits to .env / .env.<anything> files.

Secrets belong in a password manager, not a file that might get committed.
This is a hard deny on writing any `.env` or `.env.<suffix>`, with an exemption
for placeholder/template env files (.env.example, .env.template, .env.sample) —
they carry no secrets and are meant to be edited and committed.

Wire it on PreToolUse / Edit|MultiEdit|Write. See hooks/README.md.
"""
import json
import re
import sys

# Template/placeholder env files carry no secrets — editing them is fine.
EXEMPT = (".example", ".template", ".sample")

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)  # fail-open: never wedge the tool on a parse error
path = data.get("tool_input", {}).get("file_path", "")

if re.search(r"(^|[\\/])\.env(\.[^\\/]+)?$", path) and not path.lower().endswith(EXEMPT):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                f"Editing .env files is blocked: keep secrets in a password "
                f"manager,
