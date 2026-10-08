#!/usr/bin/env python3
"""Regression: rejected reuse must not alter preexisting work or receipts."""
import argparse, hashlib, json, subprocess, sys, tempfile
from pathlib import Path
p=argparse.ArgumentParser()
for k in ['base','sources','toolchain']:p.add_argument('--'+k,required=True)
a=p.parse_args();r=Path(__file__).resolve().parent
with tempfile.TemporaryDirectory(prefix='refusal-test-') as tmp:
    work=Path(tmp)/'already-existing';e=work/'evidence';e.mkdir(parents=True)
    (e/'PREPARED.json').write_text(json.dumps({'status':'PASS'}))
    (e/'ACQUISITION.json').write_text('{"status":"PASS","sentinel":"immutable previous receipt"}\n')
    (e/'prepare_FAILURE.json').write_text('original retained failure sentinel\n')
    (e/'acquire_FAILURE.json').write_text('another retained failure sentinel\n')
    def inventory():return {str(f.relative_to(work)):hashlib.sha256(f.read_bytes()).hexdigest() for f in work.rglob('*') if f.is_file()}
    before=inventory()
    for stage in ['prepare','acquire']:
        cmd=[sys.executable,'-B',str(r/'provision.py'),stage,'--base',a.base,'--sources',a.sources,'--toolchain',a.toolchain,'--work',str(work)]
        result=subprocess.run(cmd,text=True,capture_output=True)
        assert result.returncode!=0,(stage,result.stdout,result.stderr)
        phrase='refuse existing work directory' if stage=='prepare' else 'one acquisition already started; no relaunch'
        assert phrase in result.stderr,(stage,result.stderr)
        assert inventory()==before,(stage,'preexisting custody changed')
        print(stage+': refusal PASS; all sentinel receipts and file set unchanged')
