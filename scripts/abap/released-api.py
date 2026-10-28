"""Is an SAP object usable in ABAP Cloud / clean core? Answers from SAP's Cloudification Repository.

Usage:
    python released-api.py CL_ABAP_RANDOM_INT I_PRODUCT MARA BAPI_USER_GET_DETAIL
    python released-api.py --product pce RFC_READ_TABLE      # private cloud / on-premise
    python released-api.py --product btp CL_WEB_HTTP_CLIENT_MANAGER
    python released-api.py --search HTTP_CLIENT               # released objects whose name contains it
    python released-api.py --refresh ...                      # download the files again

Source: https://github.com/SAP/abap-atc-cr-cv-s4hc (Apache-2.0), the data the ATC checks
"Usage of Released APIs" / clean core use. Files are cached in %LOCALAPPDATA%\\ai-kit\\cloudification
(or ~/.cache/ai-kit/cloudification) and refreshed after 7 days.

Clean core level (SAP's level concept A-D), as derived here:
    A  released            (stability contract; deprecated: use the successor)
    B  classicAPI          (classic API nominated by SAP, no formal contract)
    C  not listed / notToBeReleased (internal SAP object; changelog / governance needed)
    D  noAPI               (not recommended)
The ATC check on the system is the final word; this is the quick look-up before writing code.
"""
import argparse
import json
import os
import sys
import time
import urllib.request

BASE = 'https://raw.githubusercontent.com/SAP/abap-atc-cr-cv-s4hc/main/src/'
FILES = {
    'public': 'objectReleaseInfoLatest.json',   # SAP S/4HANA Cloud Public Edition
    'pce': 'objectReleaseInfo_PCELatest.json',  # Private Cloud Edition / on-premise (ABAP Cloud model)
    'btp': 'objectReleaseInfo_BTPLatest.json',  # SAP BTP ABAP environment
    'classification': 'objectClassifications_SAP.json',
}
MAX_AGE = 7 * 24 * 3600
LEVEL = {'released': 'A', 'deprecated': 'A (deprecated)', 'classicAPI': 'B', 'notToBeReleased': 'C', 'noAPI': 'D'}


def cache_dir():
    root = os.environ.get('LOCALAPPDATA') or os.path.join(os.path.expanduser('~'), '.cache')
    path = os.path.join(root, 'ai-kit', 'cloudification')
    os.makedirs(path, exist_ok=True)
    return path


def load(name, refresh):
    path = os.path.join(cache_dir(), FILES[name])
    if refresh or not os.path.exists(path) or time.time() - os.path.getmtime(path) > MAX_AGE:
        print(f'downloading {FILES[name]} ...', file=sys.stderr)
        with urllib.request.urlopen(BASE + FILES[name], timeout=120) as response, open(path, 'wb') as out:
            out.write(response.read())
    with open(path, encoding='utf-8') as handle:
        data = json.load(handle)
    return data.get('objectReleaseInfo') or data.get('objectClassifications') or []


def index(entries):
    result = {}
    for entry in entries:
        for key in {entry.get('objectKey', ''), entry.get('tadirObjName', '')}:
            if key:
                result.setdefault(key.upper(), []).append(entry)
    return result


def describe(name, release, classification):
    hits = release.get(name, []) or classification.get(name, [])
    if not hits:
        return [f'{name}: not listed -> level C (internal SAP object) or not an SAP object. '
                'In ABAP Cloud: not allowed; look for a released successor (--search).']
    lines = []
    for entry in hits:
        state = entry.get('state', '?')
        text = (f"{name} [{entry.get('objectType', '?')}] state={state} -> level {LEVEL.get(state, '?')} "
                f"({entry.get('softwareComponent', '')} {entry.get('applicationComponent', '')})")
        successors = [s.get('objectKey') or s.get('tadirObjName') for s in entry.get('successors', []) or []]
        if successors:
            text += f"; successor: {', '.join(filter(None, successors))}"
        elif entry.get('successorConceptName'):
            text += f"; successor concept: {entry['successorConceptName']}"
        if entry.get('labels'):
            text += f"; labels: {', '.join(entry['labels'])}"
        lines.append(text)
    return lines


def main():
    parser = argparse.ArgumentParser(description='Clean core level of SAP objects (Cloudification Repository)')
    parser.add_argument('names', nargs='*', help='object names (class, interface, CDS view, FM, table, ...)')
    parser.add_argument('--product', choices=['public', 'pce', 'btp'], default='pce',
                        help='public = S/4HANA Cloud Public, pce = Private Cloud / on-premise (default), btp = BTP ABAP')
    parser.add_argument('--search', help='list released objects whose name contains this text')
    parser.add_argument('--refresh', action='store_true')
    args = parser.parse_args()
    if not args.names and not args.search:
        parser.error('give object names or --search')
    release = index(load(args.product, args.refresh))
    classification = index(load('classification', args.refresh)) if args.product != 'btp' else {}
    print(f'product: {args.product} ({FILES[args.product]})')
    if args.search:
        needle = args.search.upper()
        found = sorted({k for k, v in release.items() if needle in k and any(e.get('state') == 'released' for e in v)})
        print(f'{len(found)} released object(s) containing {needle}:')
        for key in found[:60]:
            print(f"  {key} [{release[key][0].get('objectType')}]")
        if len(found) > 60:
            print('  ... narrow the search')
    for name in args.names:
        for line in describe(name.upper(), release, classification):
            print(line)


if __name__ == '__main__':
    main()
