#!/usr/bin/env python3
"""Compile an index without changing the source-owned claim records.

This is a navigation compiler, not a proof checker or a warrant classifier.
"""
import hashlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
TRACKS = {
    'foundations': 'foundations/FOUNDATIONAL_CLAIMS.json',
    'geometry_moments': 'geometry/GEOMETRY_MOMENTS_CLAIMS.json',
    'evidence_transport': 'evidence/MATERIAL_CLAIMS.json',
    'proofs_types_inquiry': 'proofs/PROOF_TYPE_INQUIRY_CLAIMS.json',
}

def main():
    records, corrections, missing = [], [], []
    for track, relative in TRACKS.items():
        path = BASE / relative
        if not path.is_file():
            missing.append(relative)
            continue
        raw = path.read_bytes()
        data = json.loads(raw)
        for c in data['claims']:
            cid = c['id']
            records.append({
                'id': cid,
                'track': track,
                'title': c.get('title') or c.get('exact_statement', c.get('statement', '')),
                'statement': c.get('exact_statement', c.get('statement')),
                'record_file': relative,
                'record_file_sha256': hashlib.sha256(raw).hexdigest(),
                'record_selector': {'array': 'claims', 'id': cid},
                'evidence': c.get('evidence', c.get('evidence_level')),
                'dependencies_as_declared': c.get('dependencies', []),
                'interpretation': 'The complete source-owned record controls scope, hypotheses, verification and residuals. This index adds no verification or discovery credit.',
            })
            for item in c.get('supersessions', []):
                corrections.append({'current_claim': cid, 'record_file': relative, 'correction': item})
    ids = [r['id'] for r in records]
    if len(ids) != len(set(ids)):
        raise SystemExit('Duplicate claim ID; compilation refused.')
    output = {
        'schema': 't20-consolidated-claim-index-v1',
        'status': 'proposed baseline for owner review',
        'research_cutoff_utc': '2026-10-11T11:32:55Z',
        'meaning': 'Navigation over reconciled inherited research, not a new universal theorem catalogue or an adopted repository registry.',
        'claim_count': len(records),
        'missing_track_files': missing,
        'claims': records,
    }
    (BASE / 'CLAIM_REGISTER.json').write_text(json.dumps(output, indent=2, ensure_ascii=False)+'\n')
    (BASE / 'CORRECTION_INDEX.json').write_text(json.dumps({
        'schema': 't20-consolidated-correction-index-v1',
        'meaning': 'Current dispositions do not overwrite historical source bytes. Consult linked records for the exact argument and remaining scope.',
        'corrections': corrections,
        'additional_detailed_map': 'evidence/CORRECTION_MAP.json',
    }, indent=2, ensure_ascii=False)+'\n')
    print(json.dumps({'claims':len(records),'corrections':len(corrections),'missing_tracks':missing}))
    if missing:
        raise SystemExit(2)

if __name__ == '__main__':
    main()
