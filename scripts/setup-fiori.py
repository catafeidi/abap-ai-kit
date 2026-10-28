"""Set up SAP Fiori / UI5 development with AI assistants for one project on this machine.

Usage:
    python setup-fiori.py --project <project folder> [--dry-run]

Every step prints [AUTO] (done or checked by this script) or [MANUAL] (you do it; the how is
printed). No password or token is written anywhere. Existing configuration is kept and backed up
before it is changed. Safe to run again. Guide: kit guidelines/ui5/development.md.

AUTO:  Node.js check; VS Code extensions (SAP Fiori tools extension pack, UI5 Language Assistant,
       SAP CDS Language Support, Connection Manager for SAP Systems); the official UI5 and Fiori MCP
       servers registered for Claude Code (<project>/.mcp.json) and for GitHub Copilot in VS Code
       (<project>/.vscode/mcp.json); <project>/repos/ created for the app repositories.
MANUAL: SAP system connections (Connection Manager) or BTP destinations, logons, first start of the
       MCP servers.
"""
import argparse
import datetime
import json
import os
import shutil
import subprocess
import sys

EXTENSIONS = {
    'SAPSE.sap-ux-fiori-tools-extension-pack': 'SAP Fiori tools (generator, page editor, guided development, service modeler)',
    'SAPOSS.vscode-ui5-language-assistant': 'UI5 Language Assistant (XML views, manifest)',
    'SAPSE.vscode-cds': 'SAP CDS Language Support (CAP and annotations)',
    'SAPOSS.sap-ux-sap-systems-ext': 'Connection Manager for SAP Systems (used by the Fiori MCP server)',
}
# pinned on purpose (SAP recommends pinning the Fiori MCP server); raise after testing
UI5_MCP = '@ui5/mcp-server@0.3.2'
FIORI_MCP = '@sap-ux/fiori-mcp-server@1.15.14'
MIN_NODE = (20, 17)
WINDOWS = os.name == 'nt'


def say(kind, text):
    print(f'[{kind}] {text}')


def run(command):
    try:
        return subprocess.run(command, capture_output=True, text=True, shell=True, timeout=300)
    except Exception as error:  # noqa: BLE001 - report and continue
        return subprocess.CompletedProcess(command, 1, '', str(error))


def npx_server(package, *extra):
    """stdio server started through npx; native Windows needs cmd /c (UI5 MCP server README)."""
    if WINDOWS:
        return {'type': 'stdio', 'command': 'cmd', 'args': ['/c', ' '.join(['npx', '--yes', package, *extra])]}
    return {'type': 'stdio', 'command': 'npx', 'args': ['--yes', package, *extra]}


def merge_servers(path, key, servers, dry_run, label):
    config = {}
    if os.path.exists(path):
        with open(path, encoding='utf-8-sig') as handle:
            config = json.load(handle)
    current = config.setdefault(key, {})
    changed = {name: entry for name, entry in servers.items() if current.get(name) != entry}
    if not changed:
        say('AUTO', f'{label}: UI5 and Fiori MCP servers already in {path}.')
        return
    if not dry_run:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if os.path.exists(path):
            shutil.copy2(path, f'{path}.bak-{datetime.datetime.now():%Y%m%d-%H%M%S}')
        current.update(changed)
        with open(path, 'w', encoding='utf-8') as handle:
            json.dump(config, handle, indent=2)
            handle.write('\n')
    say('AUTO', f'{label}: {", ".join(changed)} registered in {path}.')


def main():
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('--project', required=True)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    project = os.path.abspath(args.project)
    if args.dry_run:
        print('Dry run: nothing is written.')

    node = run('node --version').stdout.strip().lstrip('v')
    if not node:
        say('MANUAL', 'Install Node.js 22 LTS (https://nodejs.org), open a new terminal, run this again.')
        sys.exit(1)
    if tuple(int(p) for p in node.split('.')[:2]) < MIN_NODE:
        say('MANUAL', f'Node.js {node} is too old for the UI5 MCP server (needs 20.17+ or 22.9+): update it.')
        sys.exit(1)
    say('AUTO', f'Node.js {node} found.')

    if run('code --version').returncode != 0:
        say('MANUAL', 'Install VS Code (https://code.visualstudio.com) with "Add to PATH", then run this again.')
    else:
        installed = run('code --list-extensions').stdout.lower().split()
        for extension, purpose in EXTENSIONS.items():
            if extension.lower() in installed:
                say('AUTO', f'{purpose}: already installed.')
                continue
            if args.dry_run:
                say('AUTO', f'(dry run) would install {extension}: {purpose}.')
                continue
            result = run(f'code --install-extension {extension}')
            ok = extension.lower() in run('code --list-extensions').stdout.lower().split()
            if ok:
                say('AUTO', f'{purpose}: installed.')
                continue
            reason = ''
            if 'certificate' in (result.stdout + result.stderr).lower():
                reason = (' The command line was blocked by a company TLS certificate; the Extensions view uses '
                          'the Windows certificate store, or set NODE_EXTRA_CA_CERTS to the company root certificate.')
            say('MANUAL', f'{purpose}: install it in VS Code > Extensions, search the id {extension}.{reason}')

    servers = {'ui5-mcp': npx_server(UI5_MCP), 'fiori-mcp': {**npx_server(FIORI_MCP, 'fiori-mcp'), 'timeout': 600}}
    merge_servers(os.path.join(project, '.mcp.json'), 'mcpServers', servers, args.dry_run, 'Claude Code')
    vscode = {name: {k: v for k, v in entry.items() if k != 'timeout'} for name, entry in servers.items()}
    merge_servers(os.path.join(project, '.vscode', 'mcp.json'), 'servers', vscode, args.dry_run, 'GitHub Copilot (VS Code)')

    repos = os.path.join(project, 'repos')
    if not os.path.isdir(repos) and not args.dry_run:
        os.makedirs(repos)
    say('AUTO', f'App repositories go to {repos}\\<app> (each its own Git repository, ignored by the project notes).')

    print()
    say('MANUAL', '1. SAP systems: VS Code > Connection Manager for SAP Systems > add the ABAP system (or BTP '
                  'destination) the apps use. The Fiori MCP server generates apps only for saved connections.')
    say('MANUAL', '2. Log on once per system in VS Code; never give a password to an AI.')
    say('MANUAL', '3. Claude Code: start it in the project folder, approve "ui5-mcp" and "fiori-mcp", check /mcp.')
    say('MANUAL', '4. Copilot: VS Code > Command Palette > "MCP: List Servers" > start ui5-mcp and fiori-mcp, '
                  'trust them when asked.')
    say('MANUAL', '5. Project AGENTS.md: set "UI technology: Fiori elements | freestyle UI5" and the UI5 version.')
    say('MANUAL', '6. Test: ask the AI "which UI5 version does this project use?" (UI5 MCP get_project_info) or '
                  '"run the UI5 linter".')


if __name__ == '__main__':
    main()
