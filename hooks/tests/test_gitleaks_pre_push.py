"""Tests for gitleaks-pre-push.py: the scan runs in the repository the push targets.

Needs git and gitleaks on PATH. Builds two throwaway repositories: one clean, one with a fake
AWS key. Run: python hooks/tests/test_gitleaks_pre_push.py
"""
import json
import os
import subprocess
import tempfile

HOOK = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "gitleaks-pre-push.py")


def make_repo(content):
    path = tempfile.mkdtemp()
    subprocess.run(["git", "init", "-q", path], check=True)
    with open(os.path.join(path, "file.txt"), "w") as handle:
        handle.write(content)
    subprocess.run(["git", "-C", path, "add", "."], check=True)
    subprocess.run(["git", "-C", path, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "x"],
                   check=True)
    return path.replace("\\", "/")


clean = make_repo("hello\n")
# a repository whose local overlay forbids the word "acme": a commit naming it must be refused
internal_repo = make_repo("built for ACME corp\n")
os.makedirs(os.path.join(internal_repo, "local"))
with open(os.path.join(internal_repo, "local", "gitleaks-internal.toml"), "w") as handle:
    handle.write('[extend]\nuseDefault = true\n[[rules]]\nid = "internal"\nregex = \'\'\'(?i)acme\'\'\'\n')
# fake key assembled at run time, so this file itself does not trip the scanner
leaky = make_repo("aws_access_key_id = " + "AKIA" + "Z7Q3" + "EXAMPLE4XYZW" + "\n"
                  + 'aws_secret_access_key = "' + "wJalrXUtnFEMI/K7MDENG/" + "bPxRfiCYzEXAMPLEKEY1" + '"\n')
CASES = [  # (command, working directory of the hook, expected decision)
    (f"cd {clean} && git push", leaky, "allow"),            # cd target wins over the session folder
    (f"cd {leaky} && git push", clean, "deny"),
    (f"git -C {leaky} push", clean, "deny"),
    (f"cd {clean} && git push; cd {leaky} && git log", leaky, "allow"),  # a cd after the push is ignored
    (f'cd {clean} && git log -1 --format="detect git -C push; x" && git push', leaky, "allow"),  # words in an argument
    (f'cd {clean} && git commit -q -m x && git push', leaky, "ask"),  # commit in the same command: cannot be scanned
    (f"cd {clean}\ngit push", leaky, "allow"),               # cd on its own line
    (f"cd {clean} && git push -f", leaky, "ask"),            # short force flag asks
    ("git push", leaky, "deny"),                             # no cd: the session folder is scanned
    ("git status", leaky, "allow"),                          # not a push
    (f"cd {internal_repo} && git push", clean, "deny"),      # local internal-name rule applies
    (f"cd {clean} && git push", internal_repo, "allow"),     # ... only in the repository that has it
]
fails = 0
for command, cwd, expected in CASES:
    out = subprocess.run(["python", HOOK], input=json.dumps({"tool_input": {"command": command}}),
                         capture_output=True, text=True, cwd=cwd).stdout
    got = (json.loads(out or "{}").get("hookSpecificOutput") or {}).get("permissionDecision", "allow")
    fails += got != expected
    print("ok  " if got == expected else "FAIL", f"{command[:60]:60} -> {got}")
print("failures:", fails)
raise SystemExit(1 if fails else 0)
