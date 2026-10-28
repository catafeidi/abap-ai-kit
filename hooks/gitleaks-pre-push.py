#!/usr/bin/env python3
"""PreToolUse / Bash hook: run gitleaks before any `git push`, ask before force-push.

Scans the commits actually being pushed for secrets, denies the push on a real
finding, and asks (rather than silently passing) when gitleaks is not installed.
Force pushes always ask, because the default posture here is no force push.

Requires gitleaks on PATH (e.g. `brew install gitleaks`).
Wire it on PreToolUse / Bash. See hooks/README.md.
"""
import json
import os
import re
import subprocess
import sys

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)  # fail-open: never wedge the tool on a parse error
cmd = data.get("tool_input", {}).get("command", "")

# Match `git push` as the start of any segment (start-of-string, ;, &, |, &&, ||), also with
# global options before the subcommand (`git -C <dir> push`, `git -c key=value push`)
GIT_PUSH = r"git(?:\s+-[Cc]\s+(?:\"[^\"]+\"|'[^']+'|\S+))*\s+push\b"
is_push = bool(re.search(r"(^|[;&|(\n]|&&|\|\|)\s*" + GIT_PUSH, cmd))
if not is_push:
    print("{}")
    sys.exit(0)

is_force = bool(re.search(r"\b" + GIT_PUSH + r".*(--force\b|--force-with-lease\b|\s-f\b|\s\+)", cmd))


def repo_dir(command):
    """The repository the push runs in: `git -C <dir> push`, else the last `cd <dir>` /
    `Set-Location <dir>` before the push, else the hook's own working directory."""
    # the real push command starts a segment; text inside a commit message does not
    push = re.search(r"(?:^|[;&|(\n]|&&|\|\|)\s*(" + GIT_PUSH + ")", command)
    before_push = command[:push.start(1)]
    dash_c = re.search(r"\s-C\s+(\"[^\"]+\"|'[^']+'|\S+)", push.group(1))
    found = dash_c.group(1) if dash_c else None
    if not found:
        changes = re.findall(r"(?:^|[;&|(\n]|&&)\s*(?:cd|Set-Location|sl|pushd)\s+(?:/d\s+)?"
                             r"(\"[^\"]+\"|'[^']+'|[^\s;&|]+)", before_push)
        found = changes[-1] if changes else None
    if not found:
        return None
    path = found.strip("\"'")
    drive = re.match(r"^/([a-zA-Z])/(.*)$", path)  # Git Bash /d/x -> D:/x
    if drive:
        path = f"{drive.group(1).upper()}:/{drive.group(2)}"
    path = os.path.expanduser(path)
    return path if os.path.isdir(path) else None


try:
    cwd = repo_dir(cmd)
except Exception:
    cwd = None  # fall back to the hook's working directory, still scanned

# A commit made in the same command does not exist yet when this hook runs, so it cannot be
# scanned: ask, so the push is run as its own command (and scanned then).
try:
    push_at = re.search(r"(?:^|[;&|(\n]|&&|\|\|)\s*(" + GIT_PUSH + ")", cmd).start(1)
    if re.search(r"(?:^|[;&|(\n]|&&|\|\|)\s*git\b(?:\s+-[Cc]\s+\S+)*\s+commit\b", cmd[:push_at]):
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "ask",
            "permissionDecisionReason": "This command commits and pushes in one step, so the secret scan "
                                        "cannot see the new commit. Run the push as a separate command."}}))
        sys.exit(0)
except Exception:
    pass

# Scan git-tracked content, NOT the raw working tree. A `--no-git` filesystem
# scan flags gitignored, never-pushed files (.env.local, build dirs,
# node_modules) — false positives, since none of that reaches the remote.
# Git-mode scans commits instead. Scope to the commits actually being pushed
# (the range the upstream is behind HEAD): fast on big repos, and it won't
# re-nag a secret already in pushed history. No upstream yet (first push of a
# new branch) -> scan full history, which is correct for a first push.
log_opts = None
try:
    up = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}"],
        capture_output=True, text=True, timeout=10, cwd=cwd,
    )
    if up.returncode == 0 and up.stdout.strip():
        log_opts = f"{up.stdout.strip()}..HEAD"
except Exception:
    pass  # any failure -> full-history scan below (conservative)

gitleaks_cmd = ["gitleaks", "detect", "--no-banner", "--redact",
                "--exit-code", "1", "--source", "."]
if log_opts:
    gitleaks_cmd.append(f"--log-opts={log_opts}")

try:
    res = subprocess.run(gitleaks_cmd, capture_output=True, text=True, timeout=45, cwd=cwd)
except FileNotFoundError:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "ask",
            "permissionDecisionReason": (
                "gitleaks not on PATH — run a secret scan before pushing. "
                "Install (`winget install Gitleaks.Gitleaks`) or confirm to bypass."
            ),
        }
    }))
    sys.exit(0)
except subprocess.TimeoutExpired:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "ask",
            "permissionDecisionReason": "gitleaks scan timed out after 45s. Confirm push manually.",
        }
    }))
    sys.exit(0)

if res.returncode != 0:
    body = (res.stdout or res.stderr or "(no output)")[-1500:]
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                "gitleaks BLOCKED push: secret findings before sending to remote.\n"
                + body
            ),
        }
    }))
elif is_force:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "ask",
            "permissionDecisionReason": (
                "Force push detected. Force push is off by default here. "
                "Confirm explicitly to proceed."
            ),
        }
    }))
else:
    print("{}")
