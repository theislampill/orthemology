#!/usr/bin/env python3
"""Add the fourth frozen package without editing v2's retained verifier."""
import json
from pathlib import Path
from verify import PACKAGES, sha, verify

PACKAGES['hase-full-per-extension-20261010'] = '151def7fb3c5bf543810c1be42601957bccfddce163571468ae72b17c7db479f'

def verify_v3(root):
    result = verify(root)
    mapping = json.loads((root / 'preservation/V2_PRESERVATION.json').read_text())
    assert len(mapping['files']) == 174
    for item in mapping['files']:
        data = (root / item['v3_path']).read_bytes()
        assert len(data) == item['bytes'] and sha(data) == item['sha256'], item['v2_path']
    review = root / 'hase-full-per-extension-20261010/validation/independent-review/REVIEW.md'
    assert sha(review.read_bytes()) == '8228b3f21537dae3e9ac1162425a9797c2e67c254ce3542bece56e4f1604f1bb'
    result['all_v2_files_preserved'] = 174
    result['new_whole_model_review_bound'] = True
    return result

if __name__ == '__main__':
    print(json.dumps(verify_v3(Path(__file__).resolve().parent), indent=2))
