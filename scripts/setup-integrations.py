"""Check and wire a project's integrations (code host, tracker, wiki, CI, CRM) on this machine.

Usage:
    python setup-integrations.py --project <project folder> [--dry-run]

Reads <project>/integrations.json (template: kit templates/project/integrations.json) and prints
every step as [AUTO] (done or checked by this script) or [MANUAL] (you do it; the exact command is
printed). Logins are always manual; no token or password is written anywhere. Safe to run again.
Guide: kit guidelines/integrations.md.
"""
import argparse
import datetime
import json
import os
import shutil
import subprocess
import sys

problems = 0


def say(kind, text):
    global problems
    problems += kind == 'MANUAL'
    print(f'[{kind}] {text}')


def run(command, env=None):
    try:
        return subprocess.run(command, capture_output=True, text=True, shell=True, timeout=120,
                              env=dict(os.environ, **(env or {})))
    except Exception as error:  # noqa: BLE001 - report and continue
        return subprocess.CompletedProcess(command, 1, '', str(error))


def have(tool):
    return shutil.which(tool) is not None


def read_json(path, default):
    if not os.path.exists(path):
        return default
    with open(path, encoding='utf-8-sig') as handle:
        return json.load(handle)


def register_mcp(project, name, entry, dry_run):
    path = os.path.join(project, '.mcp.json')
    config = read_json(path, {'mcpServers': {}})
    if config.setdefault('mcpServers', {}).get(name) == entry:
        say('AUTO', f'MCP server {name} already in {path}.')
        return
    if not dry_run:
        if os.path.exists(path):
            shutil.copy2(path, f'{path}.bak-{datetime.datetime.now():%Y%m%d-%H%M%S}')
        config['mcpServers'][name] = entry
        with open(path, 'w', encoding='utf-8') as handle:
            json.dump(config, handle, indent=2)
            handle.write('\n')
    say('AUTO', f'MCP server {name} registered in {path} (approve it once when Claude Code asks).')


def check_github(code):
    if not have('gh'):
        say('MANUAL', 'Install the GitHub CLI: winget install --id GitHub.cli   (then run this again)')
        return
    account = code.get('account')
    status = run('gh auth status')
    if account and account not in (status.stdout + status.stderr):
        say('MANUAL', f'Log in the project account: gh auth login   (as {account}; keep other accounts)')
        return
    say('AUTO', f'gh logged in{" as " + account if account else ""}.')
    token = run(f'gh auth token --user {account}').stdout.strip() if account else ''
    for repo in code.get('repos', []):
        full = repo if '/' in repo else f"{code.get('org', '')}/{repo}"
        result = run(f'gh api repos/{full} --jq .full_name', env={'GH_TOKEN': token} if token else None)
        if result.returncode == 0:
            say('AUTO', f'repo {full} reachable with {account or "the active account"}.')
        else:
            say('MANUAL', f'repo {full} not reachable with {account or "the active account"}: ask for access '
                          f'or fix the name in integrations.json.')


def check_azure(block, project, dry_run, registered):
    org = block.get('organization')
    if not org:
        say('MANUAL', f'{block["type"]}: set "organization" in integrations.json.')
        return
    if org not in registered:
        register_mcp(project, 'azure-devops', {'type': 'http', 'url': f'https://mcp.dev.azure.com/{org}'}, dry_run)
        registered.add(org)
        say('MANUAL', 'Azure DevOps MCP: sign in with your Microsoft account when the server first connects.')
    if 'az' in registered:
        return
    registered.add('az')
    if not have('az'):
        say('MANUAL', 'Optional CLI fallback: winget install --id Microsoft.AzureCLI, then '
                      'az extension add --name azure-devops, then az login')
    elif run('az extension show --name azure-devops').returncode != 0:
        say('MANUAL', 'az extension add --name azure-devops')
    else:
        say('AUTO', 'az with the azure-devops extension found.')


def check_atlassian(block, kind, checked):
    if 'atlassian' not in checked:
        checked.add('atlassian')
        listed = run('claude mcp get atlassian')
        if listed.returncode == 0 and 'atlassian' in listed.stdout.lower():
            say('AUTO', 'Atlassian MCP server is configured.')
            say('MANUAL', 'If /mcp shows atlassian as "needs authentication": /mcp > atlassian > authenticate.')
        else:
            say('MANUAL', 'claude mcp add --scope user --transport http atlassian https://mcp.atlassian.com/v2/mcp   '
                          'then /mcp > atlassian > authenticate')
    if kind == 'tracker' and not str(block.get('cloudId', '')).strip('<>').count('-'):
        say('MANUAL', 'tracker.cloudId missing: ask the AI to call getAccessibleAtlassianResources and put the id '
                      'of your site into integrations.json.')
    if kind == 'tracker' and not block.get('project'):
        say('MANUAL', 'tracker.project missing (project key, e.g. ABC).')
    if kind == 'wiki' and not block.get('spaces'):
        say('MANUAL', 'wiki.spaces missing (space keys the search is limited to).')
    if kind in ('tracker', 'wiki'):
        say('AUTO', f'{kind}: {block["type"]} {block.get("site", "")} {block.get("project") or ",".join(block.get("spaces", []))}')


def check_salesforce(crm):
    if not have('sf'):
        say('MANUAL', 'Install the Salesforce CLI: npm install --global @salesforce/cli   (then run this again)')
        return
    alias = crm.get('alias')
    if not alias:
        say('MANUAL', 'crm.alias missing in integrations.json.')
        return
    result = run(f'sf org display --target-org {alias} --json')
    try:
        connected = json.loads(result.stdout).get('result', {}).get('connectedStatus') == 'Connected'
    except json.JSONDecodeError:
        connected = False
    if connected:
        say('AUTO', f'Salesforce org {alias} connected.')
    else:
        say('MANUAL', f'sf org login web --alias {alias} --instance-url {crm.get("instanceUrl", "<my domain url>")}')


def main():
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('--project', required=True)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    project = os.path.abspath(args.project)
    config = read_json(os.path.join(project, 'integrations.json'), None)
    if config is None:
        kit = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        say('MANUAL', f'No integrations.json: copy {os.path.join(kit, "templates", "project", "integrations.json")} '
                      f'into {project}, fill in what the project uses, delete the rest, run again.')
        sys.exit(1)
    if args.dry_run:
        print('Dry run: nothing is written.')
    checked, registered = set(), set()
    for kind in ('code', 'tracker', 'wiki', 'ci', 'crm'):
        block = config.get(kind)
        if not block:
            continue
        kind_type = block.get('type', '')
        if kind_type == 'github' or (kind == 'ci' and kind_type == 'github-actions') or kind_type == 'github-issues':
            if kind == 'code':
                check_github(block)
            else:
                say('AUTO', f'{kind}: {kind_type} uses gh (checked with code).')
        elif kind_type in ('azure-repos', 'azure-boards', 'azure-wiki', 'azure-pipelines'):
            check_azure(block, project, args.dry_run, registered)
        elif kind_type in ('jira', 'confluence'):
            check_atlassian(block, kind, checked)
        elif kind_type == 'salesforce':
            check_salesforce(block)
        elif kind_type == 'gitlab':
            say('AUTO' if have('glab') else 'MANUAL', 'glab found.' if have('glab') else 'winget install --id GLab.GLab, then glab auth login')
        else:
            say('MANUAL', f'{kind}: type "{kind_type}" has no adapter yet; see guidelines/integrations.md.')
    print(f'\n{problems} manual step(s) open.' if problems else '\nAll integrations ready.')


if __name__ == '__main__':
    main()
