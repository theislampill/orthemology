#!/usr/bin/env python3
"""Recheck this scoped review; writes only a review-local replay directory."""
from pathlib import Path
from hashlib import sha256
import json
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
AUTHOR = ROOT/'interaction-calibration-anchor'

def digest(p): return sha256(p.read_bytes()).hexdigest()


def main():
    tracked = {}
    def require(path, expected):
        found = digest(path)
        assert found == expected, f'Hash mismatch: {path}'
        tracked[str(path)] = found

    binding = json.loads((HERE/'AUTHOR_BINDING.json').read_text())
    for row in binding['files']:
        require(AUTHOR/row['path'],row['sha256'])
        require(HERE/row['snapshot'],row['sha256'])

    sources = json.loads((HERE/'author_snapshot/SOURCE_BINDINGS.json').read_text())
    source_count = 0
    for record in sources['frozen_manifests']:
        directory = ROOT/record['directory']
        require(directory/'MANIFEST.json',record['manifest_sha256'])
        manifest = json.loads((directory/'MANIFEST.json').read_text())
        listed = {r['path']:r['sha256'] for r in record['payloads']}
        actual = {r['path']:r['sha256'] for r in manifest['files']}
        assert listed == actual, f'Frozen manifest payload list mismatch: {directory}'
        for row in record['payloads']:
            require(directory/row['path'],row['sha256'])
            source_count += 1
    for row in sources['individually_inspected']:
        require(ROOT/row['path'],row['sha256'])

    manifest = json.loads((HERE/'REVIEW_MANIFEST.json').read_text())
    for row in manifest['files']:
        require(HERE/row['path'],row['sha256'])

    replay = HERE/'verification_replay'
    (replay/'results').mkdir(parents=True,exist_ok=True)
    replay_results=[]
    for script, output in [('exact_controls.py','exact_controls'),('panel_controls.py','panel_controls')]:
        shutil.copyfile(HERE/'author_snapshot'/script,replay/script)
        proc=subprocess.run([sys.executable,str(replay/script)],capture_output=True,text=True,check=True)
        expected=(HERE/'author_snapshot/results'/f'{output}.json').read_text()
        assert (replay/'results'/f'{output}.json').read_text()==expected
        assert proc.stdout==(HERE/'author_snapshot/results'/f'{output}.log').read_text()
        replay_results.append({'script':script,'output_byte_identical':True})
    for script,output in [('independent_controls.py','INDEPENDENT_CONTROLS.json'),
                          ('independent_panel_controls.py','INDEPENDENT_PANEL_CONTROLS.json')]:
        expected=(HERE/output).read_text()
        proc=subprocess.run([sys.executable,str(HERE/script)],capture_output=True,text=True,check=True)
        assert proc.stdout==expected
        assert (HERE/output).read_text()==expected
        replay_results.append({'script':script,'output_byte_identical':True})
    for path,expected in tracked.items():
        assert digest(Path(path))==expected, f'Bound input changed during replay: {path}'
    print(json.dumps({'status':'PASS','author_files_bound':len(binding['files']),
                     'frozen_predecessor_payloads':source_count,
                     'individually_listed_sources':len(sources['individually_inspected']),
                     'review_manifest_files':len(manifest['files']),
                     'replays':replay_results,'before_after_identity':True,
                     'scope':'Scoped proof-review reproducibility and byte identity; no integration or closure authority.'},
                     indent=2,sort_keys=True))

if __name__=='__main__': main()
