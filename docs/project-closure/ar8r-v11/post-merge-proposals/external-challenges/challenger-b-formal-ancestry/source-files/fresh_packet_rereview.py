#!/usr/bin/env python3
"""Distinct fresh rereview of the generated non-authoritative challenger packet."""
from __future__ import annotations
import hashlib, json, re, subprocess, sys, yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXPECTED_SHA = 'a8142c3caf103ee46a2cd759c3d319b1e29b40da'
checks: list[dict] = []

def add(name: str, passed: bool, detail: str = '') -> None:
    checks.append({'check': name, 'pass': bool(passed), 'detail': detail})

# Parse structured artifacts.
proposal = yaml.safe_load((ROOT/'bounded_challenger_b_proposal.yaml').read_text())
results = json.loads((ROOT/'deep_bv_challenger_results.json').read_text())
lean = json.loads((ROOT/'lean_static_status.json').read_text())
ancestry = json.loads((ROOT/'repository_ancestry_extract.json').read_text())
report = (ROOT/'BOUNDED_CHALLENGER_B_DEEP_BV_FORMAL_ANCESTRY_SOURCE_FIREWALL_PROPOSAL.md').read_text()

add('reviewed SHA exact in proposal', proposal['repository']['reviewed_main_sha'] == EXPECTED_SHA)
add('reviewed SHA exact in finite results', results['authority']['reviewed_commit'] == EXPECTED_SHA)
add('read-only status', proposal['status'] == 'NON_AUTHORITATIVE_READ_ONLY_PROPOSAL' and proposal['repository']['mutation'] == 'NONE')
add('no new theorem ID recommended', proposal['recommended_family_action']['allocate_new_theorem_id'] is False)
add('canonical owner T294', proposal['recommended_family_action']['canonical_theorem_owner'] == 'AR8R-T294')
add('exact duplicate relation', proposal['recommended_family_action']['relation_edge']['relation'] == 'IDENTICAL_UP_TO_RENAMING')
add('AR-T1 relation classified strict specialization', proposal['classification']['mathematical_core']['relation_to_AR_T1'] == 'STRICT_SPECIALIZATION')
add('primary family fibre', proposal['recommended_family_action']['primary_family'] == 'FAMILY-FIBRE')
add('secondary family causal', proposal['recommended_family_action']['secondary_family'] == 'FAMILY-CAUSAL')
add('finite checker zero mismatches', results['exhaustive_check']['attained_range_equivalence_pass'] is True)
add('full codomain guarded check zero mismatches', results['exhaustive_check']['full_codom_equivalence_pass_under_nonempty_target'] is True)
add('finite case count fixed', results['exhaustive_check']['total_map_pairs_checked'] == 87317)
add('stronger-reading countermodels present', len(results['countermodels']) >= 14, str(len(results['countermodels'])))
add('source-world coordinates all present', len(results['source_world_firewall']['layers_kept_separate']) == 11)
add('Lean parser not overclaimed', lean['parser'] == 'NOT_RUN')
add('Lean elaborator not overclaimed', lean['elaboration'] == 'NOT_RUN')
add('Lean kernel not overclaimed', lean['kernel'] == 'NOT_RUN')
add('no sorry/admit/axiom/opaque declarations in static scan', all(v == 0 for v in lean['static_scan'].values()), json.dumps(lean['static_scan']))
add('ancestry registry source hash recorded', len(ancestry['source_sha256']) == 64)
add('ancestry recommendation exact', ancestry['deep_bv_to_t294_comparison']['recommended_relation'] == 'IDENTICAL_UP_TO_RENAMING')
for heading in [
    '## 2. Typed repaired statement',
    '## 4. Interpretation map by intended lane',
    '## 5. Formal ancestry and prior-art audit',
    '## 6. Countermodels to stronger readings',
    '## 7. Dependency and noncircularity audit',
    '## 8. Source-world firewall',
    '## 10. Lean-oriented signature and formal status',
    '## 11. Specification-fidelity audit',
    '## 12. Cold audit, repair, and fresh rereview',
    '## 13. Exact theorem-family recommendation',
]:
    add(f'report heading: {heading}', heading in report)

# Make sure forbidden positive inferences occur only in negative/firewall context.
add('explicit no Necessary Being inference', 'factorization theorem cannot discharge them' in report and 'Necessary Being' in report)
add('explicit no source authority neutrality', 'Source authority is not neutral experimental semantics' in report)
add('explicit no controlling archive', 'controlling_archive: NOT_CREATED' in report)

passed = all(c['pass'] for c in checks)
payload = {
    'schema': 'bounded-challenger-b-fresh-packet-rereview-v1',
    'status': 'PASS_WITH_EXPLICIT_EXTERNAL_NOT_RUN_GATES' if passed else 'FAIL_REPAIR_REQUIRED',
    'checks': checks,
    'external_not_run_gates': [
        'independent git transport verification',
        'historical Deep BV checker reproduction',
        'Lean parsing',
        'Lean elaboration',
        'Lean kernel checking',
        'Lean axiom dependency report',
        'owner adoption or authoritative theorem-family registration',
        'actual common-intervention experiment',
    ],
}
text = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + '\n'
(ROOT/'fresh_rereview_results.json').write_text(text, encoding='utf-8')
print(json.dumps({'status': payload['status'], 'checks': len(checks), 'failed': [c['check'] for c in checks if not c['pass']]}, indent=2))
sys.exit(0 if passed else 1)
