"""Set up SAP Fiori / UI5 development with AI assistants for one project on this machine.

Usage:
    python setup-fiori.py --project <project folder> [--dry-run] [--allow-telemetry]

Every step prints [AUTO] (done or checked by this script) or [MANUAL] (you do it; the how is
printed). No password or token is written anywhere. Existing configuration is kept: entries you
adjusted (for example an `env` with NODE_EXTRA_CA_CERTS) are not overwritten, servers you already
registered under another name are not duplicated, changed files are backed up (*.bak-<time>).
Safe to run again. Guide: kit guidelines/ui5/development.md.

AUTO:  Node.js check; VS Code extensions (SAP Fiori tools extension pack, which includes the UI5
       Language Assistant and the Connection Manager for SAP Systems; SAP CDS Language Support);
       the official UI5 and Fiori MCP servers for Claude Code (<project>/.mcp.json) and GitHub
       Copilot in VS Code (<project>/.vscode/mcp.json), Fiori MCP telemetry off unless
       --allow-telemetry; <project>/repos/ for the app repositories.
MANUAL: SAP system connections or BTP destinations, logons, first start of the MCP servers.
Pinned server versions below: raise them after testing a newer release.
"""
import argparse
import datetime
import json
import os
import shutil
import subprocess
import sys

EXTENSIONS = {
    'SAPSE.sap-ux-fiori-tools-extension-pack': 'SAP Fiori tools extension pack (generator, page editor, '
                                               'service modeler, UI5 Language Assistant, Connection Manager)',
    'SAPSE.vscode-cds': 'SAP CDS Language Support (CAP and annotations)',
}
UI5_MCP = '@ui5/mcp-server@0.3.2'
FIORI_MCP = '@sap-ux/fiori-mcp-server@1.15.14'
MIN_NODE = (22, 9)  # Fiori MCP server: node >=22; UI5 MCP server: ^20.17 || >=22.9
MANAGED = ('type', 'command', 'args', 'timeout')  # the keys this script owns in a server entry
WINDOWS = os.name == 'nt'
DRY = False


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


def package_of(entry):
    text = ' '.join(str(a) for a in entry.get('args', []))
    for package in ('@ui5/mcp-server', '@sap-ux/fiori-mcp-server'):
        if package in text:
            return package
    return None


def merge_servers(path, key, wanted, label):
    """Add or update only the keys this script owns; keep everything else the user put there."""
    config = {}
    if os.path.exists(path):
        try:
            with open(path, encoding='utf-8-sig') as handle:
                config = json.load(handle)
        except json.JSONDecodeError:
            say('MANUAL', f'{label}: {path} is not plain JSON (comments?), so it is not changed. Add under '
                          f'"{key}": ' + json.dumps(wanted))
            return
    servers = config.setdefault(key, {})
    changes = []
    for name, entry in wanted.items():
        package = package_of(entry)
        other = next((n for n, e in servers.items() if n != name and package_of(e) == package), None)
        if other and name not in servers:
            say('AUTO', f'{label}: {package} already registered as "{other}"; kept as it is.')
            continue
        current = servers.setdefault(name, {})
        updated = dict(current)
        updated.update({k: v for k, v in entry.items() if k in MANAGED})
        for env_key, env_value in entry.get('env', {}).items():
            updated.setdefault('env', {}).setdefault(env_key, env_value)  # never override a user value
        if updated != current:
            servers[name] = updated
            changes.append(name)
    if not changes:
        say('AUTO', f'{label}: UI5 and Fiori MCP servers up to date in {path}.')
        return
    if not DRY:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if os.path.exists(path):
            shutil.copy2(path, f'{path}.bak-{datetime.datetime.now():%Y%m%d-%H%M%S}')
        with open(path, 'w', encoding='utf-8') as handle:
            json.dump(config, handle, indent=2)
            handle.write('\n')
    say('AUTO', f'{label}: {", ".join(changes)} ' + ('would be registered' if DRY else 'registered') + f' in {path}.')


def install_extensions():
    if run('code --version').returncode != 0:
        say('MANUAL', 'Install VS Code (https://code.visualstudio.com) with "Add to PATH", then run this again.')
        return
    installed = run('code --list-extensions').stdout.lower().split()
    for extension, purpose in EXTENSIONS.items():
        if extension.lower() in installed:
            say('AUTO', f'{purpose}: already installed.')
            continue
        if DRY:
            say('AUTO', f'(dry run) would install {extension}: {purpose}.')
            continue
        result = run(f'code --install-extension {extension}')
        if extension.lower() in run('code --list-extensions').stdout.lower().split():
            say('AUTO', f'{purpose}: installed.')
            continue
        reason = ''
        if 'certificate' in (result.stdout + result.stderr).lower():
            reason = (' The command line was blocked by a company TLS certificate; the Extensions view uses the '
                      'Windows certificate store, or set NODE_EXTRA_CA_CERTS to the company root certificate.')
        say('MANUAL', f'{purpose}: install it in VS Code > Extensions, search the id {extension}.{reason}')


def main():
    global DRY
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('--project', required=True)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--allow-telemetry', action='store_true', help='leave Fiori MCP telemetry on')
    args = parser.parse_args()
    DRY = args.dry_run
    project = os.path.abspath(args.project)
    if DRY:
        print('Dry run: nothing is written.')

    node = run('node --version').stdout.strip().lstrip('v')
    if not node:
        say('MANUAL', 'Install Node.js 22 LTS (https://nodejs.org), open a new terminal, run this again.')
        sys.exit(1)
    if tuple(int(p) for p in node.split('.')[:2]) < MIN_NODE:
        say('MANUAL', f'Node.js {node} is too old: the Fiori MCP server needs 22, the UI5 MCP server 22.9 or later. '
                      'Install Node.js 22 LTS, then run this again.')
        sys.exit(1)
    say('AUTO', f'Node.js {node} found.')

    install_extensions()

    fiori = {**npx_server(FIORI_MCP, 'fiori-mcp'), 'timeout': 600}
    if not args.allow_telemetry:
        fiori['env'] = {'SAP_UX_FIORI_TOOLS_DISABLE_TELEMETRY': 'true'}
    servers = {'ui5-mcp': npx_server(UI5_MCP), 'fiori-mcp': fiori}
    merge_servers(os.path.join(project, '.mcp.json'), 'mcpServers', servers, 'Claude Code')
    vscode = {name: {k: v for k, v in entry.items() if k != 'timeout'} for name, entry in servers.items()}
    merge_servers(os.path.join(project, '.vscode', 'mcp.json'), 'servers', vscode, 'GitHub Copilot (VS Code)')

    repos = os.path.join(project, 'repos')
    if not os.path.isdir(repos) and not DRY:
        os.makedirs(repos)
    say('AUTO', f'App repositories go to {os.path.join(repos, "<app>")} (each its own Git repository, '
                'ignored by the project notes).')

    print()
    say('MANUAL', '1. SAP systems: VS Code > SAP Fiori > Connection Manager: add the ABAP system or BTP destination '
                  'the apps use (the Fiori MCP server generates OData apps from a saved connection or a metadata file).')
    say('MANUAL', '2. Log on once per system in VS Code; never give a password to an AI.')
    say('MANUAL', '3. Claude Code: start it in the project folder, approve "ui5-mcp" and "fiori-mcp", check /mcp.')
    say('MANUAL', '4. Copilot: VS Code > Command Palette > "MCP: List Servers" > start ui5-mcp and fiori-mcp, trust them.')
    say('MANUAL', '5. Behind TLS inspection the first npx download (and the Fiori search model from HuggingFace) can '
                  'fail with a certificate error: add "NODE_EXTRA_CA_CERTS": "<company root .pem>" to the server env.')
    say('MANUAL', '6. Project AGENTS.md: set "UI technology", the UI5 version and the deployment target.')
    say('MANUAL', '7. Test: ask the AI "which UI5 version does this project use?" (UI5 MCP get_project_info).')


if __name__ == '__main__':
    main()
