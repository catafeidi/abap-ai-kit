#!/usr/bin/env python3
"""UserPromptSubmit hook: put the current local date and time into every prompt.

Stdout of a UserPromptSubmit hook is added to the model's context. Fail-open.
"""
from datetime import datetime

try:
    print(f"Current time: {datetime.now().astimezone().strftime('%A, %d %B %Y, %H:%M %Z')}")
except Exception:
    pass
