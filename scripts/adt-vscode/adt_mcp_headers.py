"""Authorization header for the ADT MCP server of 'ABAP Development Tools for VS Code'.

The extension generates a new bearer token every time its MCP server starts and keeps it
in the VS Code user settings (adt.mcpServer.token). Claude Code calls this script as the
headersHelper of the MCP server 'adt-vscode', so the token is read at connect time and is
never written into a Claude Code configuration file.

Prints one JSON object: {"Authorization": "Bearer <token>"}.
"""
import json
import os
import re
import sys

settings = os.path.join(os.environ.get('APPDATA', ''), 'Code', 'User', 'settings.json')
try:
    text = open(settings, encoding='utf-8').read()
except OSError:
    sys.exit(f'VS Code settings not found: {settings}')

match = re.search(r'"adt\.mcpServer\.token"\s*:\s*"([^"]+)"', text)
if not match:
    sys.exit('No ADT MCP token in the VS Code settings: enable "ADT MCP Server" (adt.mcpServer.enabled) in VS Code')

print(json.dumps({'Authorization': f'Bearer {match.group(1)}'}))
