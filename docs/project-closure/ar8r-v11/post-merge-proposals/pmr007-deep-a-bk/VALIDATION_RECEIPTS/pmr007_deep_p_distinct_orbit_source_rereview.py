# SANITIZED REVIEW COPY: supply owner-controlled evidence paths before execution.
#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
SOURCE = Path('EVIDENCE_ID:OSM_SUN_ET_AL_2025_ACCESS_COPY')
OUT = BASE / 'rereviews' / 'PMR-007_DEEP_P_DISTINCT_ORBIT_SOURCE_REREVIEW_RESULTS.json'


def main():
    # Independent relational/orbit check: no transition-table enumeration.
    orbit_count = 0
    orbit_size_failures = 0
    pf_variation_failures = 0
    invariant_predicate_failures = 0
    neutral_dimensions = 8
    for neutral in itertools.product((0, 1), repeat=neutral_dimensions):
        plus = (neutral, True, True)   # neutral, TL, FIT_O
        minus = (neutral, False, True)
        orbit = {plus, minus}
        orbit_count += 1
        if len(orbit) != 2:
            orbit_size_failures += 1
        pf_plus = plus[1] and plus[2]
        pf_minus = minus[1] and minus[2]
        if pf_plus == pf_minus:
            pf_variation_failures += 1
        # Every coordinate-projection predicate on the neutral reduct is invariant.
        for i in range(neutral_dimensions):
            if plus[0][i] != minus[0][i]:
                invariant_predicate_failures += 1

    src = SOURCE.read_bytes()
    src_hash = hashlib.sha256(src).hexdigest()
    text = src.decode('utf-8', errors='replace').lower()
    source_checks = {
        'expected_hash': '0d097cba7bbb25a949e2bf95af28b5a2259bd8d60b0e5fac5a74cdf7d05aa814',
        'actual_hash': src_hash,
        'hash_match': src_hash == '0d097cba7bbb25a949e2bf95af28b5a2259bd8d60b0e5fac5a74cdf7d05aa814',
        'contains_multiple_models_final_state_language': (
            'final orthogonalized representations' in text or
            'final orthogonalized states' in text
        ),
        'contains_cscg_trajectory_discriminator': (
            'only the cscg consistently reproduced this precise decorrelation trajectory' in text
        ),
        'contains_further_research_caveat': 'further research is needed' in text,
    }
    all_source_checks = all(source_checks[k] for k in [
        'hash_match',
        'contains_multiple_models_final_state_language',
        'contains_cscg_trajectory_discriminator',
        'contains_further_research_caveat',
    ])
    result = {
        'identity': 'PMR-007-TRPF-1',
        'method': 'neutral-orbit relational check plus direct source-string custody check',
        'neutral_profile_orbits': orbit_count,
        'orbit_size_failures': orbit_size_failures,
        'pf_epi_variation_failures': pf_variation_failures,
        'neutral_invariant_projection_failures': invariant_predicate_failures,
        'source_checks': source_checks,
        'overall': 'PASS' if not any([
            orbit_size_failures,
            pf_variation_failures,
            invariant_predicate_failures,
        ]) and all_source_checks else 'FAIL',
        'scope_notes': [
            'Orbit check proves only model-relative nonidentification under closure.',
            'Source check verifies wording in the accessible paper copy; it does not reproduce the neuroscience study.',
            'No external philosophical review or world-level proper-function conclusion is supplied.',
        ],
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
