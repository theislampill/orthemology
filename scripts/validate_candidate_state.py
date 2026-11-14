#!/usr/bin/env python3
"""Validate current decision authority without replaying historical PR topology.

The decision registry and candidate decision sources own this boundary. Historical
branch observations and generated overlays remain separately qualified evidence;
they are not inputs to this current-authority check. This does not confer adoption,
independent review or empirical validity. The existing owner-controlled adoption
ceiling is unchanged by this extraction.
"""
import io
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAILS = []
STATUS_VOCABULARY = {
    'adopted-merged', 'adopted-with-superseded-clause', 'proposed-candidate',
    'superseded', 'historical', 'rejected',
}


def check(name, ok, detail=''):
    print('[%s] %s%s' % ('PASS' if ok else 'FAIL', name,
                         (' — '+detail) if detail and not ok else ''))
    if not ok:
        FAILS.append(name)


def read(rel):
    path = os.path.join(ROOT, *rel.split('/'))
    if not os.path.exists(path):
        return ''
    with io.open(path, encoding='utf-8') as stream:
        return stream.read()


def collect_authority_issues(decisions, source_documents):
    """Pure current authority checks; source_documents maps IDs to body lists."""
    if not isinstance(decisions, dict) or not decisions:
        return ['decision registry must contain a non-empty decisions mapping']
    issues = []
    for did, row in sorted(decisions.items(), key=lambda pair: str(pair[0])):
        if not isinstance(did, str) or not re.fullmatch(r'[0-9]{4}', did) or int(did) < 1:
            issues.append('decision identifier must be four decimal digits')
            continue
        if not isinstance(row, dict):
            issues.append('decision %s must be a mapping' % did)
            continue
        status = row.get('status')
        if not isinstance(status, str) or status not in STATUS_VOCABULARY:
            issues.append('decision %s has unknown status' % did)
        candidate = 'pr' in row or row.get('stage') == 'local-preparation'
        if candidate:
            if status != 'proposed-candidate':
                issues.append('candidate decision %s must remain proposed-candidate' % did)
            bodies = source_documents.get(did, [])
            if len(bodies) != 1:
                issues.append('candidate decision %s requires exactly one current source' % did)
            elif not isinstance(bodies[0], str) or 'CANDIDATE' not in bodies[0].upper():
                issues.append('candidate decision %s source must carry CANDIDATE' % did)
        elif status == 'proposed-candidate':
            issues.append('decision %s lacks a declared candidate origin' % did)

        # Preserve the pre-existing authority boundary. Git integration of an
        # implementation does not promote its normative decisions to adopted.
        number = int(did)
        if 20 <= number <= 36:
            if 'pr' not in row:
                issues.append('observed candidate decision %s must retain its PR association' % did)
        elif number > 36:
            if status != 'proposed-candidate' or not candidate:
                issues.append('new decision %s requires proposed candidate preparation or a PR' % did)
        elif 'pr' in row:
            issues.append('previously merged decision %s must not acquire a candidate PR' % did)
    return issues


def main():
    FAILS.clear()
    try:
        registry = yaml.safe_load(read('docs/decision-status.yaml'))
        decisions = registry.get('decisions') if isinstance(registry, dict) else None
        source_documents = {}
        directory = os.path.join(ROOT, 'docs', 'decisions')
        names = sorted(os.listdir(directory)) if os.path.isdir(directory) else []
        if isinstance(decisions, dict):
            for did, row in decisions.items():
                if not isinstance(did, str) or not re.fullmatch(r'[0-9]{4}', did):
                    continue
                if not isinstance(row, dict) or not ('pr' in row or row.get('stage') == 'local-preparation'):
                    continue
                source_documents[did] = [read('docs/decisions/'+name) for name in names
                                         if name.startswith(did+'-') and name.endswith('.md')]
        issues = collect_authority_issues(decisions, source_documents)
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        issues = ['current decision inputs cannot be read: '+str(exc)]
    for issue in issues:
        check(issue, False)
    if not issues:
        check('current decision authority and candidate source labels', True)
    print('TOTAL: %d failures' % len(FAILS))
    return 1 if FAILS else 0


if __name__ == '__main__':
    sys.exit(main())
