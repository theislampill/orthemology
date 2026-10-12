#!/usr/bin/env python3
"""Seal the existing P01 attempt-0003 workspace; never regenerate predecessors.

This packaging operation checks exact source/evidence bindings, creates a layered
manifest/receipt seal, and writes a detached all-member ledger. The independent
closed-archive verification is a separate process, not an assertion by this file.
"""
from __future__ import annotations
import hashlib
import importlib.util
import json
import stat
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT.parent / 'Orthemology_P01_Research_Checkpoint_attempt-0003.zip'
SEALS = {'MANIFEST.json', 'RECEIPT.json', 'RECEIPT.json.sha256'}


def h(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def encode(obj: object) -> bytes:
    return (json.dumps(obj, indent=2, ensure_ascii=False, sort_keys=True) + '\n').encode()


def identity(data: bytes) -> dict:
    return {'bytes': len(data), 'sha256': h(data)}


def collect() -> dict[str, bytes]:
    result = {}
    for p in sorted(ROOT.rglob('*')):
        if p.is_symlink():
            raise ValueError('Symlink not admitted: ' + str(p))
        if not p.is_file():
            continue
        rel = p.relative_to(ROOT).as_posix()
        if '__pycache__' in p.parts or p.suffix == '.pyc' or rel in SEALS:
            continue
        if p.suffix in {'.olean', '.ilean'}:
            raise ValueError('Unexpected compiled artefact in unqualified packet: ' + rel)
        result[rel] = p.read_bytes()
    return result


def main() -> None:
    for p in [OUTPUT, Path(str(OUTPUT) + '.sha256'), Path(str(OUTPUT) + '.members.json')]:
        if p.exists():
            raise FileExistsError('Refusing to overwrite export: ' + str(p))
    module_path = ROOT / 'handoff' / 'verify_attempt3.py'
    spec = importlib.util.spec_from_file_location('p01_seal_validation', module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError('Cannot load the exact verifier source')
    verifier = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(verifier)
    d = collect()
    statuses = verifier.strict_loads(d['STATUS_RECORDS.json'])
    verifier.check_statuses(statuses)
    for key, record in statuses.items():
        verifier.need(record == verifier.strict_loads(d[f'boundary/{key}_TERMINAL_DISPOSITION.json']),
                      'Per-obligation status differs: ' + key)
        verifier.need(record['kernel_credit'] is False, 'Unverified kernel promotion')
    predecessors = verifier.check_predecessors(d)
    formal = verifier.check_formal(d)
    nodes = verifier.check_dependencies(d)
    inv = verifier.strict_loads(d['INPUT_AND_STATEMENT_IDENTITIES.json'])
    for row in inv['files']:
        verifier.binding(d[row['path']], row, row['path'])
    verifier.need(inv['formal_source_inventory_sha256'] == h(d['formal/SOURCE_INVENTORY.json']),
                  'Input/statement index formal binding')
    fs = verifier.strict_loads(d['formal/FORMAL_STATUS.json'])
    verifier.need(fs['source_inventory_sha256'] == h(d['formal/SOURCE_INVENTORY.json']),
                  'Formal-status inventory binding')
    runs = verifier.strict_loads(d['evidence/FINAL_TEST_RUNS.json'])
    verifier.need(len(runs) == 2 and {r['mode'] for r in runs} == {'normal', 'optimised'},
                  'Final test mode coverage')
    tests = []
    for row in runs:
        count = verifier.check_test_evidence(row, d)
        exit_path = 'evidence/final_tests_' + row['mode'] + '.exit'
        verifier.need(d[exit_path].decode().strip() == str(row['exit_code']), 'Test exit file differs')
        tests.append({'mode': row['mode'], 'tests': count, 'exit_code': row['exit_code']})
    ex = verifier.strict_loads(d['evidence/export_fixtures.json'])
    verifier.need(h(d['formal/P01GeneratedExports.lean']) == ex['generated_source_sha256'],
                  'Generated fixture binding')
    verifier.need(ex['kernel_verified'] is False, 'Generated fixture kernel promotion')
    preseal = {
        'status': 'PASS_PRESEAL_BINDINGS',
        'predecessors': predecessors,
        'formal': formal,
        'dependency_nodes': nodes,
        'tests': tests,
        'input_statement_bindings': len(inv['files']),
        'status_records_checked': 3,
        'mathematical_or_kernel_credit': False,
        'external_review_credit': False,
        'closed_archive_verified_by_this_operation': False,
    }
    (ROOT / 'evidence' / 'PRESEAL_CONSISTENCY.json').write_bytes(encode(preseal))
    d = collect()
    manifest = {
        'schema': 'orthemology-p01-attempt0003-manifest-v1',
        'algorithm': 'sha256',
        'excluded_seal_members': sorted(SEALS),
        'payload_file_count': len(d),
        'payload_bytes': sum(map(len, d.values())),
        'files': [{'path': n, **identity(b)} for n, b in sorted(d.items())],
    }
    mb = encode(manifest)
    receipt = {
        'schema': 'orthemology-p01-attempt0003-receipt-v1',
        'attempt': '0003',
        'programme': 'Orthemology / P01 research-proposal surface',
        'manifest_binding': {'path': 'MANIFEST.json', **identity(mb)},
        'canonical': {
            'main': verifier.MAIN, 'tree': verifier.TREE,
            'PR': 28, 'PR_state': 'MERGED', 'integration_remaining': [],
        },
        'predecessor_identities': {
            n: identity(d[n]) for n in sorted(d)
            if n.startswith('predecessors/') and n.endswith('.zip')
        },
        'attempt2_recovery': {
            'original_archive_recovered': False,
            'complete_workspace_recovered': False,
            'exact_documents_preserved': 6,
            'kind': 'NEW_LIMITED_RECOVERY_PACKET_NOT_ORIGINAL_ATTEMPT2',
        },
        'status_records_sha256': h(d['STATUS_RECORDS.json']),
        'terminal_dispositions': {k: r['terminal_status'] for k, r in statuses.items()},
        'source_inventory_sha256': h(d['formal/SOURCE_INVENTORY.json']),
        'formal_qualification_report_sha256': h(d['evidence/LEAN_QUALIFICATION.json']),
        'test_report_sha256': h(d['evidence/FINAL_TEST_RUNS.json']),
        'preseal_report_sha256': h(d['evidence/PRESEAL_CONSISTENCY.json']),
        'formal_scope': formal,
        'test_evidence': tests,
        'repository_mutation': 'NONE',
        'owner_adoption_credit': False,
        'external_review_credit': False,
        'new_kernel_credit': False,
        'publication_credit': False,
        'historical_recovery_credit': False,
        'live_remote_requalification_claim': False,
        'canonical_status_promotion': False,
        'P02_or_P03_success_assumed': False,
        'scope_note': ('Named candidate proof bodies are authored but uncompiled. Partial exact '
                       'proof replay is not a total JSON-to-dependent interpreter or universal '
                       'machine verification of Python. U10 ordinary replacement is preserved.'),
        'independent_final_reopen': 'REQUIRED_SEPARATE_PROCESS_WITH_DETACHED_REPORT',
        'deterministic_zip_member_timestamp': '2026-09-22T00:00:00',
    }
    rb = encode(receipt)
    d['MANIFEST.json'] = mb
    d['RECEIPT.json'] = rb
    d['RECEIPT.json.sha256'] = (h(rb) + '  RECEIPT.json\n').encode()
    for name in SEALS:
        (ROOT / name).write_bytes(d[name])
    with zipfile.ZipFile(OUTPUT, 'x', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, data in sorted(d.items()):
            info = zipfile.ZipInfo(name, date_time=(2026, 9, 22, 0, 0, 0))
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    raw = OUTPUT.read_bytes()
    Path(str(OUTPUT) + '.sha256').write_text(h(raw) + '  ' + OUTPUT.name + '\n')
    ledger = {
        'schema': 'orthemology-p01-all-member-ledger-v1',
        'archive_bytes': len(raw), 'archive_sha256': h(raw),
        'members': {n: identity(b) for n, b in sorted(d.items())},
    }
    Path(str(OUTPUT) + '.members.json').write_bytes(encode(ledger))
    print(json.dumps({
        'status': 'EXPORTED_REQUIRES_INDEPENDENT_REOPEN',
        'archive': str(OUTPUT), 'bytes': len(raw), 'sha256': h(raw),
        'members': len(d), 'uncompressed_bytes': sum(map(len, d.values())),
        'preseal': preseal,
    }, indent=2))


if __name__ == '__main__':
    main()
