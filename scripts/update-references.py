"""Compare the vendored third-party material of the kit with its upstream, and update it on request.

Usage:
    python scripts/update-references.py            # report what changed upstream (nothing written)
    python scripts/update-references.py --apply    # copy the upstream files in and pin the new commit
    python scripts/update-references.py --only sap-skills --apply

Sources and pins: SOURCES.json (human list: SOURCES.md). Upstream is fetched with a shallow,
sparse git clone into a temporary folder; nothing from it is executed. After --apply, review
`git diff --stat` in the kit, read the changed skills, then commit. Local edits to vendored files
are overwritten: keep them out of vendored folders (or list the path under "keep").
"""
import argparse
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(KIT, 'SOURCES.json')


def git(*args, cwd=None):
    return subprocess.run(['git', *args], cwd=cwd, capture_output=True, text=True, check=True).stdout.strip()


def fetch(repo, paths, target):
    git('clone', '-q', '--depth', '1', '--filter=blob:none', '--sparse', repo, target)
    sparse = [p for p in paths if p] or ['/*']
    if any(not p for p in paths):  # repository root wanted: no-cone mode, top level files only
        git('sparse-checkout', 'set', '--no-cone', '/*', '!/*/', *[f'/{p}/' for p in paths if p], cwd=target)
    else:
        git('sparse-checkout', 'set', *sparse, cwd=target)
    return git('rev-parse', 'HEAD', cwd=target)


def same_content(first, second):
    """Equal apart from line endings (a Windows checkout turns LF into CRLF)."""
    with open(first, 'rb') as a, open(second, 'rb') as b:
        return a.read().replace(b'\r\n', b'\n') == b.read().replace(b'\r\n', b'\n')


def tree(root, pattern=None, keep=()):
    files = set()
    if not os.path.isdir(root):
        return files
    for base, dirs, names in os.walk(root):
        dirs[:] = [d for d in dirs if d != '.git']
        for name in names:
            rel = os.path.relpath(os.path.join(base, name), root).replace('\\', '/')
            if pattern and ('/' in rel or not re.match(pattern, name)):
                continue
            if any(rel == k or rel.startswith(k.rstrip('/') + '/') for k in keep):
                continue
            files.add(rel)
    return files


def compare_dir(upstream, local, pattern, keep):
    up, here = tree(upstream, pattern, keep), tree(local, pattern, keep)
    changed = sorted(f for f in up & here if not same_content(os.path.join(upstream, f), os.path.join(local, f)))
    return changed, sorted(up - here), sorted(here - up)


def apply_dir(upstream, local, pattern, keep, changed, added, removed):
    for rel in changed + added:
        os.makedirs(os.path.dirname(os.path.join(local, rel)) or local, exist_ok=True)
        shutil.copy2(os.path.join(upstream, rel), os.path.join(local, rel))
    for rel in removed:
        os.remove(os.path.join(local, rel))


def main():
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--only', help='name of one source in SOURCES.json')
    args = parser.parse_args()
    manifest = json.load(open(MANIFEST, encoding='utf-8'))
    total = 0
    for source in manifest['vendored']:
        if args.only and source['name'] != args.only:
            continue
        maps = source.get('files', []) + source.get('dirs', [])
        paths = sorted({os.path.dirname(m['from']) if 'files' in source and m in source['files'] else m['from'] for m in maps})
        with tempfile.TemporaryDirectory() as temp:
            upstream_root = os.path.join(temp, 'repo')
            try:
                head = fetch(source['repo'], paths, upstream_root)
            except subprocess.CalledProcessError as error:
                print(f"[{source['name']}] fetch failed: {error.stderr.strip()[:200]}")
                continue
            pin = (source.get('ref') or 'unpinned')[:10]
            print(f"[{source['name']}] {source['repo']}  kit pin {pin} -> upstream {head[:10]}  ({source.get('license')})")
            differences = 0
            for item in source.get('files', []):
                upstream_file, local_file = os.path.join(upstream_root, item['from']), os.path.join(KIT, item['to'])
                same = os.path.exists(local_file) and same_content(upstream_file, local_file)
                if not same:
                    differences += 1
                    print(f"    changed  {item['to']}")
                    if args.apply:
                        shutil.copy2(upstream_file, local_file)
            for item in source.get('dirs', []):
                upstream_dir, local_dir = os.path.join(upstream_root, item['from']), os.path.join(KIT, item['to'])
                changed, added, removed = compare_dir(upstream_dir, local_dir, item.get('pattern'), item.get('keep', []))
                count = len(changed) + len(added) + len(removed)
                differences += count
                if count:
                    print(f"    {item['to']}: {len(changed)} changed, {len(added)} new, {len(removed)} removed upstream")
                    for rel in (changed + added + removed)[:8]:
                        print(f'        {rel}')
                if args.apply and count:
                    apply_dir(upstream_dir, local_dir, item.get('pattern'), item.get('keep', []), changed, added, removed)
            if not differences:
                print('    up to date')
            total += differences
            if args.apply:
                source['ref'] = head
                source['updated'] = datetime.date.today().isoformat()
    if args.apply:
        with open(MANIFEST, 'w', encoding='utf-8') as handle:
            json.dump(manifest, handle, indent=2)
            handle.write('\n')
        print('\nApplied. Review with: git -C "%s" diff --stat   then read the changed skills and commit.' % KIT)
    else:
        print(f'\n{total} difference(s). Run with --apply to take them.' if total else '\nEverything up to date.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
