# Security policy

The kit contains hooks and scripts that run on developers' machines and can guard SAP systems, so
security reports are welcome.

## Report a vulnerability
Please **do not open a public issue**. Use
[private vulnerability reporting](https://github.com/catafeidi/abap-ai-kit/security/advisories/new)
on this repository. Include the file, the input that triggers the problem and what an attacker
gains (for example: a hook that can be bypassed, a script that executes downloaded content, a
secret that reaches a push).

You get an answer within a week. Fixes are released on `main`; there are no maintained older
versions.

## Scope
- In scope: `hooks/`, `scripts/`, `install.ps1`, anything that could run code, leak data or let
  an assistant bypass a guard.
- Out of scope: the content of vendored third-party skills (report to their upstream, see
  `SOURCES.md`) and the behaviour of the AI assistants themselves.
