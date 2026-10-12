#!/usr/bin/env python3
"""Verify included bytes, then replay copied suites without modifying evidence."""
import argparse, hashlib, json, platform, shutil, subprocess, sys
from pathlib import Path
import sympy

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--output',required=True,help='New, nonexistent replay output directory')
    args=ap.parse_args()
    root=Path(__file__).resolve().parent
    out=Path(args.output).resolve()
    if out.exists():
        raise SystemExit('Output must not already exist; original evidence is never overwritten.')
    manifest=json.loads((root/'MANIFEST.json').read_text())
    actual={str(p.relative_to(root)):sha(p) for p in root.rglob('*') if p.is_file() and p.name!='MANIFEST.json'}
    assert actual==manifest['files'], 'Included-file manifest mismatch'
    out.mkdir(parents=True)
    work=out/'work'
    shutil.copytree(root/'evidence',work)
    config=json.loads((root/'REPLAY_CONFIG.json').read_text())
    records=[]
    for suite in config['suites']:
        script=work/suite['script']
        command=[sys.executable,str(script)]
        if suite.get('fresh_output'):
            command += ['--output-dir',str(out/suite['fresh_output'])]
        result=subprocess.run(command,cwd=script.parent,text=True,capture_output=True)
        (out/(suite['name']+'.stdout.txt')).write_text(result.stdout)
        (out/(suite['name']+'.stderr.txt')).write_text(result.stderr)
        output=(out/suite['fresh_output']/suite['generated_name']) if suite.get('fresh_output') else work/suite['result']
        expected=root/'evidence'/suite['result']
        record={'name':suite['name'],'returncode':result.returncode,'script_sha256':sha(script),'output_sha256':sha(output) if output.exists() else None,'expected_output_sha256':sha(expected),'output_matches_preserved':output.exists() and output.read_bytes()==expected.read_bytes()}
        records.append(record)
        assert result.returncode==0 and record['output_matches_preserved'], record
    binding_records=[]
    for record in config['digest_bindings']:
        local=root/'evidence'/record['target']
        assert local.is_file(), record['target']
        assert sha(local)==record['sha256'], record
        binding_records.append({**record,'verified':True})
    assert actual=={str(p.relative_to(root)):sha(p) for p in root.rglob('*') if p.is_file() and p.name!='MANIFEST.json'},'Replay mutated evidence'
    receipt={'status':'PASS','python':platform.python_version(),'sympy':sympy.__version__,'manifest_sha256':sha(root/'MANIFEST.json'),'included_files_verified':len(actual),'suites':records,'accepted_and_input_bindings':binding_records,'coverage':'Included-file integrity and full new author83 categorical plus independent154 controls. Author83 means39 localization,7 beyond-H² discriminators,16 inherited regressions,21 integrity checks. No source-byte exclusions from these suites; historical narrow source suite is not replayed. Ordinary analysis, inherited static results and source readings not kernel-verified. No upload/integration/closure.'}
    (out/'REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({'status':'PASS','receipt':str(out/'REPLAY_RECEIPT.json'),'suites':len(records)}))
if __name__=='__main__': main()
