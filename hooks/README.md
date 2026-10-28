# hooks/

Scrubbed, working PreToolUse / PostToolUse hooks. These are the deterministic
floor under an autonomous harness: a rule in a config file competes with the
model's habits and loses under load; a hook runs every time.

| File | Event / matcher | What it does |
|------|-----------------|--------------|
| `block-rm-rf.py` | PreToolUse / Bash | hard-deny `rm -rf` at a command boundary; delete specific paths instead |
| `injection-guard.py` | PreToolUse / Bash | ask-confirm on the four injection/exfil shapes (remote-pipe-to-shell, remote-pipe-to-interpreter, inline `ANTHROPIC_BASE_URL`, secret-source + outbound-sink) |
| `block-env-edits.py` | PreToolUse / Edit\|Write | hard-deny edits to `.env` files, exempting `.env.example`/`.template`/`.sample` |
| `gitleaks-pre-push.py` | PreToolUse / Bash | run gitleaks on the commits being pushed; deny on a finding, ask if gitleaks is missing or on a force push |
| `sap-guard.py` | PreToolUse / `mcp__.*` and Bash | SAP systems: deny edit/create/delete on systems a project marks read-only in `<project>/.claude/sap-guard.json` (vsp `SAP` tool and ADT MCP destinations), ask on RFC calls there; ask on every transport release (release FMs, ADT release tools, `*_release.py`). Tests: `python hooks/tests/test_sap_guard.py` |

Shell guards are wired on `Bash|PowerShell`: both shell tools reach the same commands.
Tests: `python hooks/tests/test_sap_guard.py`, `python hooks/tests/test_gitleaks_pre_push.py`.

## Wiring

`scripts/install.ps1` links this folder to `~/.claude/hooks`. Once per machine, merge the
`hooks` block of [`templates/settings.example.json`](../templates/settings.example.json) into
`~/.claude/settings.json` (use `python`, not `python3`, on Windows). The shape of one entry:

```json
"PreToolUse": [
  {
    "matcher": "Bash|PowerShell",
    "hooks": [
      { "type": "command", "command": "python ~/.claude/hooks/block-rm-rf.py", "timeout": 5 },
      { "type": "command", "command": "python ~/.claude/hooks/injection-guard.py", "timeout": 5 },
      { "type": "command", "command": "python ~/.claude/hooks/gitleaks-pre-push.py", "timeout": 60 }
    ]
  }
]
```

## The five principles

1. **Anchor at command boundaries.** `(?:^|[\n;&|(])\s*` in front of any
   command-matching regex, so the hook fires on the command, not on the string
   inside an echo or heredoc.
2. **Fail open. Never wedge the tool.** Every hook exits clean on any internal
   error. A crashing guard that blocks all of Bash is worse than the risk.
3. **Ask, do not deny, except two cases.** Hard-deny only irreversible actions
   with no legitimate agent use (`rm -rf`, editing a secret file) and a
   confirmed secret leak. Everything else asks.
4. **Ship a test suite with the hook.** Name the shapes that should fire and the
   ones that must not, and run them before deploying a change.
5. **Time injection is universal.** Every harness should do it. One line, every
   prompt.

## Before you share your own

`injection-guard.py` carries host-specific allow-heuristics (the `local` test in
section 2 — gateway naming, tailnet hints). Replace those with your own, keep
the four detection shapes, then run your own `gitleaks` pass over this directory
before publishing.
