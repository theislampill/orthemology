#!/usr/bin/env python3
"""Read-only deterministic source selection/relocation planner. Never copies or runs sources.

This validates an explicitly reviewed selection. It cannot grant distribution rights.
The lookup and old v5 membership are identity indexes, never publication allowlists.
The default stdout is a public-shaped plan; --internal adds private local resolvers.
Do not execute its proposed operations until the parent approves final assembly.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import stat
import unicodedata
import zipfile

SCHEMA = 't20-v6-explicit-selection-plan-v1'
HASH = re.compile(r'[0-9a-f]{64}\Z')
ID = re.compile(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,119}\Z')
SENSITIVE = re.compile(r'libfile_|Sentinel_|file_[0-9a-fA-F]{32}|/workspace/|/mnt/data/|/home/|[?&](?:sig|token|X-Amz-[^=]*)=|-----BEGIN .*PRIVATE KEY', re.I)
HARD_REASONS = {'private_machine_locators', 'private_linkage_identifiers',
                'raw_primary_or_transcript_collection', 'personal_contact_identifiers',
                'signed_or_private_urls', 'explicit_owner_private_custody_only'}
REVIEW_REASONS = {'primary_language_dense_extract_requires_review',
                  'archive_binary_compiled_or_nontext_payload', 'dependency_or_cache_copy',
                  'nonselected_text_or_log_extension'}
BASIS = {'reviewed_owner_authored', 'reviewed_public_projection', 'reviewed_licensed_dependency',
         'reviewed_distribution_metadata', 'reviewed_received_public_version'}

def require(ok, message):
    if not ok:
        raise ValueError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def canonical(value):
    return (json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':')) + '\n').encode()

def unique_pairs(pairs):
    out = {}
    for k, v in pairs:
        require(k not in out, 'duplicate JSON key: ' + k)
        out[k] = v
    return out

def parse(data):
    def reject_constant(value):
        raise ValueError('nonfinite JSON constant: ' + value)
    return json.loads(data, object_pairs_hook=unique_pairs, parse_constant=reject_constant)

def sha(value):
    require(isinstance(value, str) and HASH.fullmatch(value), 'invalid SHA256')
    return value

def identifier(value):
    require(isinstance(value, str) and ID.fullmatch(value) and not SENSITIVE.search(value), 'unsafe identifier')
    return value

def relative(value):
    require(isinstance(value, str) and bool(value), 'empty relative path')
    require(unicodedata.normalize('NFC', value) == value, 'noncanonical Unicode path')
    require(not any(ord(c) < 32 for c in value), 'control character in path')
    require(not any(c in value for c in '\\:\0<>|?*"'), 'platform-unsafe path')
    require(not value.startswith('/') and all(p not in ('', '.', '..') for p in value.split('/')), 'unsafe path component')
    for p in value.split('/'):
        require(not p.endswith((' ', '.')), 'Windows-ambiguous path')
        require(p.split('.')[0].casefold() not in {'con', 'prn', 'aux', 'nul', *('com'+str(i) for i in range(1,10)), *('lpt'+str(i) for i in range(1,10)), *('com'+i for i in '¹²³'), *('lpt'+i for i in '¹²³')}, 'reserved path component')
    require(not SENSITIVE.search(value), 'private linkage in public path')
    return str(PurePosixPath(value))

def checked_read(path, expected):
    path = Path(path).absolute()
    # Reject every existing symlink component, including a source root link.
    for p in (path, *path.parents):
        require(not p.is_symlink(), 'symlink source component: ' + str(p))
    require(path.is_file(), 'missing exact source: ' + str(path))
    data = path.read_bytes()
    require(digest(data) == sha(expected), 'source digest drift: ' + str(path))
    return data

def policy_reasons(record, exclusions):
    reasons = set(record.get('prior_exclusion_reasons', [])) | set(exclusions.get(record['sha256'], []))
    hard = reasons & HARD_REASONS
    # Unknown exclusion classifications require review, never implicit approval.
    review = reasons - HARD_REASONS
    disposition = record.get('distribution_disposition', '')
    if disposition in {'exclude_raw_private_or_sensitive_source_bytes',
                       'exclude_primary_or_binary_bulk_use_scoped_receipt_and_locator'}:
        hard.add('lookup:' + disposition)
    if record.get('sensitive_screen_flags'):
        hard.add('sensitive_screen_flags')
    return sorted(hard), sorted(review)

def validate_received_public_receipt(data, public_sha256, original_sha256):
    """Validate exact received-version evidence without asserting original equivalence."""
    r = parse(data)
    require(isinstance(r, dict) and set(r) == {
        'schema', 'public_sha256', 'original_sha256', 'repository', 'commit',
        'repository_path', 'source_reading', 'equivalence_to_original'},
        'invalid received-public receipt fields')
    require(r['schema'] == 't20-received-public-qualification-v1', 'wrong received-public receipt schema')
    require(sha(r['public_sha256']) == sha(public_sha256) and
            sha(r['original_sha256']) == sha(original_sha256) and
            public_sha256 != original_sha256, 'received-public identity mismatch')
    require(r['repository'] == 'theislampill/orthemology', 'unqualified received-public repository')
    require(isinstance(r['commit'], str) and re.fullmatch('[0-9a-f]{40}', r['commit']),
            'received-public commit must be exact')
    relative(r['repository_path'])
    reading = r['source_reading']
    require(isinstance(reading, dict) and set(reading) == {'ledger_sha256', 'pointer', 'scope'},
            'invalid received-public reading binding')
    sha(reading['ledger_sha256'])
    require(isinstance(reading['pointer'], str) and reading['pointer'].startswith('$/') and
            not SENSITIVE.search(reading['pointer']) and
            not any(ord(c) < 32 for c in reading['pointer']), 'invalid reading pointer')
    require(reading['scope'] == 'complete_body', 'complete received-public reading required')
    require(r['equivalence_to_original'] == 'unverified_original_unavailable',
            'received version must preserve unverified original equivalence')
    return r

def build_plan(selection, lookup, v5, exclusions, workspace, check_bytes=True):
    require(selection.get('schema') == SCHEMA, 'wrong selection schema')
    require(selection.get('assembly_authorized') is False, 'this preparation mechanism is plan-only')
    require(selection.get('audience') in {'owner_private_handoff', 'public_repository'}, 'audience required')
    identifier(selection.get('decision_reference'))
    destination = relative(selection.get('destination'))
    require('v6' in destination.casefold(), 'explicit additive v6 destination required')
    require(selection.get('baseline_policy') == 'separate_unchanged_owner_checkpoint', 'v5 must remain separate and unchanged')
    sha(selection.get('lookup_sha256')); sha(selection.get('v5_index_sha256')); sha(selection.get('exclusions_sha256'))
    require(sha(selection.get('v5_archive_sha256')) == sha(v5['zip_sha256']), 'v5 baseline identity mismatch')
    rows = selection.get('objects')
    require(isinstance(rows, list) and rows, 'explicit nonempty source selection required')
    selected = {}; views = {}; folded = {}; blockers = []; objects = []; internal = []
    v5_by_hash = {}
    for member in v5['members']:
        v5_by_hash.setdefault(sha(member['sha256']), []).append(member)
    for row in rows:
        h = sha(row['sha256']); require(h not in selected, 'duplicate selected identity')
        selected[h] = row
    for h, row in sorted(selected.items()):
        require(h in lookup, 'source absent from frozen lookup: ' + h)
        rec = lookup[h]
        action = row.get('action'); require(action in {'include', 'identity_only', 'omit'}, 'explicit action required')
        hard, review = policy_reasons(rec, exclusions)
        public = {'sha256': h, 'action': action,
                  'reviewed_digest': rec.get('reviewed_digest', h),
                  'current_path_digest': rec.get('current_path_digest'),
                  'scope_status': identifier(row.get('scope_status')),
                  'exclusion_categories': hard + review}
        # Eligibility is evaluated before any baseline reuse or byte-provider choice.
        if action == 'include':
            require(not hard, 'excluded bytes cannot be included: ' + h + ' ' + repr(hard))
            eligibility = row.get('eligibility', {})
            require(eligibility.get('basis') in BASIS, 'independent distribution decision required')
            identifier(eligibility.get('decision_reference'))
            require(eligibility.get('content_reviewed_for_distribution') is True, 'content eligibility review required')
            require(set(eligibility.get('resolved_historical_role_filters', [])) == set(review), 'all historical role filters need explicit current adjudication')
            require(row.get('role') in {'authored_proof', 'authored_code', 'authored_argument', 'consumed_fixture', 'assurance_code', 'qualified_metadata', 'licensed_dependency'}, 'explicit admitted content role required')
            require(rec.get('source_hash_verified') is True, 'exact held source not verified')
            logical = row.get('views', [])
            require(isinstance(logical, list) and logical, 'relative reconstruction view required')
            for view in logical:
                packet = identifier(view['packet']); path = relative(view['path']); key = packet + '/' + path
                low = key.casefold()
                require(key not in views and low not in folded, 'duplicate or case-fold view collision')
                views[key] = h; folded[low] = key
            deps = sorted({sha(x) for x in row.get('required_dependencies', [])})
            for dep in deps:
                require(dep in selected, 'missing explicit dependency disposition: ' + dep)
                if selected[dep]['action'] != 'include':
                    blockers.append({'consumer': h, 'dependency': dep, 'reason': 'required_dependency_not_delivered'})
            public.update(role=row['role'], required_dependencies=deps, eligibility_basis=eligibility['basis'])
            if eligibility['basis'] == 'reviewed_public_projection':
                original = sha(row.get('original_sha256')); transformation = sha(row.get('transformation_receipt_sha256'))
                require(original != h, 'projection must preserve distinct original identity')
                require(original in selected and transformation in selected, 'original identity and transformation receipt must be explicitly accounted for')
                require(selected[transformation]['action'] == 'include', 'transformation receipt must be delivered')
                public.update(original_sha256=original, transformation_receipt_sha256=transformation)
            elif eligibility['basis'] == 'reviewed_received_public_version':
                require('transformation_receipt_sha256' not in row,
                        'received version cannot claim a transformation receipt')
                original = sha(row.get('original_sha256'))
                receipt = sha(row.get('received_public_qualification_sha256'))
                require(original != h and original in selected and
                        selected[original]['action'] == 'identity_only' and
                        lookup.get(original, {}).get('source_hash_verified') is False,
                        'received-public original must remain unavailable identity-only')
                require(receipt in selected and selected[receipt]['action'] == 'include' and
                        selected[receipt].get('role') == 'qualified_metadata',
                        'received-public qualification must be delivered metadata')
                rr = lookup.get(receipt, {})
                require(rr.get('source_hash_verified') is True and isinstance(rr.get('source_path'), str),
                        'received-public qualification exact bytes unavailable')
                raw = checked_read(Path(workspace) / rr['source_path'], receipt)
                require(len(raw) == rr.get('bytes'), 'received-public receipt size mismatch')
                validate_received_public_receipt(raw, h, original)
                public.update(original_sha256=original,
                              received_public_qualification_sha256=receipt,
                              original_equivalence_status='unverified_original_unavailable')
            provider = None
            for member in sorted(v5_by_hash.get(h, []), key=lambda x: x['member']):
                try:
                    name = relative(member['member'])
                except ValueError:
                    continue
                provider = {'kind': 'separate_v5_member', 'archive_sha256': v5['zip_sha256'], 'member': name}
                break
            p = rec.get('source_path')
            if check_bytes:
                require(isinstance(p, str), 'exact source path unavailable')
                data = checked_read(Path(workspace) / p, h)
                require(len(data) == rec['bytes'], 'source length mismatch')
            if provider is None:
                provider = {'kind': 'authored_annex_object', 'path': 'authored_objects/' + h[:2] + '/' + h}
            public.update(bytes=rec['bytes'], provider=provider)
            internal.append({'sha256': h, 'source_path': p, 'proposed_operation': 'resolve_exact_bytes_only', 'provider': provider})
        else:
            require(not row.get('views'), 'excluded/identity-only source must have no materialized views')
            public['availability'] = 'held_excluded' if rec.get('source_hash_verified') else 'exact_snapshot_unavailable'
        objects.append(public)
    # Reject file/directory prefix conflicts before any future write.
    for key in folded:
        parts = key.split('/')
        for depth in range(1, len(parts)):
            require('/'.join(parts[:depth]) not in folded, 'file-directory view conflict')
    plan = {'schema': SCHEMA, 'state': 'PLAN_ONLY_NOT_ASSEMBLED',
            'audience': selection['audience'], 'destination': destination,
            'decision_reference': selection['decision_reference'],
            'input_digests': {k: selection[k] for k in ['lookup_sha256', 'v5_index_sha256', 'exclusions_sha256']},
            'baseline': {'archive_sha256': v5['zip_sha256'], 'policy': selection['baseline_policy'],
                         'whole_archive_publication_selected': False},
            'objects': objects, 'views': [{'path': k, 'sha256': v} for k,v in sorted(views.items())],
            'replay_blockers': sorted(blockers,key=lambda x:(x['consumer'],x['dependency'])),
            'source_execution_selected': False,
            'future_preflight': ['fresh destination', 'disjoint preserved source roots', 'reject symlinks and unsafe archive members before writes',
                                 'verify every exact digest and byte count', 'materialize only selected views',
                                 'do not execute inherited wrappers or installers', 'preserve reviewed and current snapshots separately']}
    return {'public_plan': plan, 'plan_sha256': digest(canonical(plan)), 'private_resolution': internal}

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    for n in ['selection', 'lookup', 'v5-index', 'exclusions']:
        ap.add_argument('--'+n, required=True, type=Path)
    ap.add_argument('--workspace', type=Path, default=Path.cwd())
    ap.add_argument('--internal', action='store_true')
    a = ap.parse_args()
    selection = parse(a.selection.read_bytes())
    lookup_raw = a.lookup.read_bytes(); v5_raw = a.v5_index.read_bytes(); exclusions_raw = a.exclusions.read_bytes()
    for key, raw in [('lookup_sha256',lookup_raw),('v5_index_sha256',v5_raw),('exclusions_sha256',exclusions_raw)]:
        require(digest(raw) == selection[key], 'frozen input changed: ' + key)
    lookup = {}
    for line in lookup_raw.splitlines():
        r = parse(line); h = sha(r['sha256']); require(h not in lookup, 'duplicate lookup identity');lookup[h]=r
    exclusions = {}
    for line in exclusions_raw.splitlines():
        r=parse(line);exclusions.setdefault(sha(r['sha256']),set()).update(r.get('exclusion_reasons', []))
    v5 = parse(v5_raw)
    # Verify baseline bytes and selected reused members read-only; never extract the ZIP.
    checked_read(a.workspace / v5['zip_path'], v5['zip_sha256'])
    result = build_plan(selection,lookup,v5,exclusions,a.workspace)
    with zipfile.ZipFile(a.workspace / v5['zip_path']) as z:
        entries = z.infolist(); names=[x.filename for x in entries]
        require(len(names)==len(set(names)), 'duplicate v5 archive members')
        for obj in result['public_plan']['objects']:
            p=obj.get('provider', {})
            if p.get('kind')=='separate_v5_member':
                info=z.getinfo(p['member']); require(not stat.S_ISLNK(info.external_attr>>16), 'symlink v5 member')
                data=z.read(info); require(digest(data)==obj['sha256'] and len(data)==obj['bytes'], 'v5 member changed')
    if not a.internal:
        del result['private_resolution']
    print(json.dumps(result,sort_keys=True,ensure_ascii=False,indent=2))

if __name__ == '__main__':
    main()
