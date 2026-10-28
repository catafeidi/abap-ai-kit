"""Set up ABAP Development Tools for VS Code and its MCP server for one project.

Usage:
    python setup_adt_vscode.py --project <project folder> --sap-user <USER> [--dry-run]

Reads from the project (both optional, templates in kit templates/project/tools/):
    tools/adt-destinations.json   destinations without passwords; {{SAP_USER}} is replaced
    tools/adt-access.json         {"port": 2236, "packages": "...", "readOnlyDestinations": [...]}

Every step prints [AUTO] (done by this script) or [MANUAL] (you do it, with how). The script
never asks for or stores a password. Existing files are backed up before they are changed;
existing destinations and settings are kept, only missing ones are added. Safe to run again.
Guide: kit guidelines/abap/adt-vscode-setup.md.
"""
import argparse
import datetime
import json
import os
import shutil
import subprocess
import sys

EXTENSION = 'sapse.adt-vscode'
MIN_VSCODE = (1, 109, 5)
KIT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HEADERS_HELPER = os.path.join(KIT, 'scripts', 'adt-vscode', 'adt_mcp_headers.py').replace('\\', '/')


def say(kind, text):
    print(f'[{kind}] {text}')


def backup(path, dry_run):
    if os.path.exists(path) and not dry_run:
        stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        shutil.copy2(path, f'{path}.bak-{stamp}')


def write_json(path, data, dry_run):
    if dry_run:
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
        handle.write('\n')


def read_json(path, default):
    if not os.path.exists(path):
        return default
    with open(path, encoding='utf-8-sig') as handle:
        return json.load(handle)


def run(command):
    try:
        return subprocess.run(command, capture_output=True, text=True, shell=True, timeout=120)
    except Exception as error:  # noqa: BLE001 - report and continue
        return subprocess.CompletedProcess(command, 1, '', str(error))


def step_vscode():
    result = run('code --version')
    if result.returncode != 0 or not result.stdout.strip():
        say('MANUAL', 'Install VS Code (https://code.visualstudio.com), tick "Add to PATH", open a new '
                      'terminal and run this script again.')
        return False
    version = tuple(int(part) for part in result.stdout.split()[0].split('.')[:3])
    if version < MIN_VSCODE:
        say('MANUAL', f'VS Code {".".join(map(str, version))} is older than the extension needs '
                      f'({".".join(map(str, MIN_VSCODE))}): Help > Check for Updates, then run again.')
        return False
    say('AUTO', f'VS Code {".".join(map(str, version))} found.')
    return True


def step_extension(dry_run):
    installed = run('code --list-extensions').stdout.lower().split()
    if EXTENSION in installed:
        say('AUTO', f'Extension {EXTENSION} already installed.')
        return
    if dry_run:
        say('AUTO', f'(dry run) would install {EXTENSION}.')
        return
    result = run(f'code --install-extension {EXTENSION}')
    # judge by the extension list, not the exit code: VS Code prints Node warnings on stderr
    if EXTENSION in run('code --list-extensions').stdout.lower().split():
        say('AUTO', f'Installed {EXTENSION}.')
    else:
        say('MANUAL', f'Install the extension yourself: Extensions view, search "ABAP Development Tools", '
                      f'install "{EXTENSION}". Error was: {result.stderr.strip()[:200]}')


def step_destinations(project, sap_user, dry_run):
    template = read_json(os.path.join(project, 'tools', 'adt-destinations.json'), None)
    if template is None:
        say('MANUAL', 'No tools/adt-destinations.json in the project: create destinations in VS Code with '
                      'Command Palette > "ABAP: New Destination" (RFC for on-premise).')
        return []
    text = json.dumps(template).replace('{{SAP_USER}}', sap_user.upper())
    wanted = json.loads(text)['destinations']
    path = os.path.join(os.path.expanduser('~'), '.adtls', 'destinations.json')
    current = read_json(path, {'formatVersion': '1.0', 'destinations': []})
    known = {entry['id'] for entry in current['destinations']}
    added = [entry for entry in wanted if entry['id'] not in known]
    if added:
        backup(path, dry_run)
        current['destinations'].extend(added)
        write_json(path, current, dry_run)
    say('AUTO', f'Destinations: {len(added)} added, {len(wanted) - len(added)} already present '
                f'({path}).')
    return [entry['id'] for entry in wanted]


def step_settings(project, destination_ids, dry_run):
    access = read_json(os.path.join(project, 'tools', 'adt-access.json'), {})
    port = access.get('port', 2236)
    path = os.path.join(os.environ.get('APPDATA', ''), 'Code', 'User', 'settings.json')
    try:
        settings = read_json(path, {})
    except json.JSONDecodeError:
        say('MANUAL', f'{path} has comments or trailing commas, so it is not changed automatically. Add: '
                      f'"adt.mcpServer.enabled": true, "adt.mcpServer.port": {port}, '
                      f'"adt.mcpServer.accessRestrictionsEnabled": true and the access restrictions below.')
        return port
    restrictions = settings.get('adt.mcpServer.accessRestrictions', {})
    systems = sorted({d.split('_')[0] for d in destination_ids})
    allowed = [d for d in (restrictions.get('destinations') or '').split(',') if d]
    allowed += [d for d in destination_ids + systems if d not in allowed]
    packages = restrictions.get('packages-objectChanges') or access.get('packages', '$TMP')
    wanted = {
        'adt.mcpServer.enabled': True,
        'adt.mcpServer.port': settings.get('adt.mcpServer.port', port),
        'adt.mcpServer.accessRestrictionsEnabled': True,
        'adt.mcpServer.accessRestrictions': {'destinations': ','.join(allowed),
                                             'packages-objectChanges': packages},
    }
    changed = {key: value for key, value in wanted.items() if settings.get(key) != value}
    if changed:
        backup(path, dry_run)
        settings.update(changed)
        write_json(path, settings, dry_run)
    say('AUTO', f'VS Code settings: {len(changed)} changed (MCP server on, port {wanted["adt.mcpServer.port"]}, '
                f'object changes only in {packages}).')
    return wanted['adt.mcpServer.port']


def step_claude(project, port, dry_run):
    path = os.path.join(project, '.mcp.json')
    config = read_json(path, {'mcpServers': {}})
    entry = {'type': 'http', 'url': f'http://localhost:{port}/mcp',
             'headersHelper': f'python {HEADERS_HELPER}'}
    if config.setdefault('mcpServers', {}).get('adt-vscode') == entry:
        say('AUTO', f'Claude Code: adt-vscode already registered in {path}.')
        return
    backup(path, dry_run)
    config['mcpServers']['adt-vscode'] = entry
    write_json(path, config, dry_run)
    say('AUTO', f'Claude Code: adt-vscode registered in {path} (token read at connect time, not stored).')


def step_guard(project, dry_run):
    access = read_json(os.path.join(project, 'tools', 'adt-access.json'), {})
    read_only = access.get('readOnlyDestinations')
    if not read_only:
        return
    path = os.path.join(project, '.claude', 'sap-guard.json')
    guard = read_json(path, {})
    current = guard.get('read_only_destinations', [])
    merged = current + [d for d in read_only if d not in current]
    if merged != current:
        backup(path, dry_run)
        guard['read_only_destinations'] = merged
        write_json(path, guard, dry_run)
    say('AUTO', f'Guard: read-only destinations {", ".join(merged)} (.claude/sap-guard.json).')


def main():
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('--project', required=True)
    parser.add_argument('--sap-user', required=True, help='SAP logon user, replaces {{SAP_USER}}')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    project = os.path.abspath(args.project)
    if args.dry_run:
        print('Dry run: nothing is written.')
    if not step_vscode():
        sys.exit(1)
    step_extension(args.dry_run)
    ids = step_destinations(project, args.sap_user, args.dry_run)
    port = step_settings(project, ids, args.dry_run)
    step_claude(project, port, args.dry_run)
    step_guard(project, args.dry_run)
    workspace = next((f for f in os.listdir(project) if f.endswith('.code-workspace')), None)
    print()
    say('MANUAL', '1. Connect the VPN or network that reaches the SAP systems.')
    say('MANUAL', f'2. Open VS Code with {"the workspace " + workspace if workspace else "the project folder"} '
                  '(File > Open Workspace from File). The extension starts the MCP server.')
    say('MANUAL', '3. Log on once per destination you need: open it in VS Code (a workspace folder '
                  'abap:/... or the destination in the ABAP view); VS Code asks for the password and keeps '
                  'the session. Never give the password to an AI.')
    say('MANUAL', '4. Claude Code: start it in the project folder, approve the project server "adt-vscode" '
                  'when asked, check /mcp shows it connected.')
    say('MANUAL', '5. Copilot: VS Code Chat > Agent mode > tools: "ADT MCP Server" is there without setup.')
    say('MANUAL', '6. Test: ask the AI to "list the ADT destinations I am logged on to".')


if __name__ == '__main__':
    main()
