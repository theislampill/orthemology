#!/usr/bin/env python3
"""Replay declared controls in disposable copies; hydrate only exact dependency members."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,importlib.metadata,json,os,shutil,subprocess,sys,tempfile,zipfile
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def snapshot(p):return {v.relative_to(p).as_posix():sha(v) for v in p.rglob('*') if v.is_file()}
parser=argparse.ArgumentParser();parser.add_argument('--output',required=True)
parser.add_argument('--ninth-archive',required=True);parser.add_argument('--tenth-archive',required=True)
a=parser.parse_args();out=Path(a.output).resolve()
assert out!=ROOT and ROOT not in out.parents,'Outputs must stay outside frozen inputs'
out.mkdir(parents=True,exist_ok=True);assert not (out/'REPLAY_RECEIPT.json').exists(),'Existing receipt'
archives={sha(Path(p)):Path(p) for p in [a.ninth_archive,a.tenth_archive]}
assert set(archives)=={'81089a1bd1497982bf80310d191a6b1019462bcb922b1f2fffbefc696853f1ef','a9f2a64c0ac30324c40993ca2a7e3d995858af3242226d7091e50d251acd622a'}
plan=json.loads((ROOT/'PACKING/CONTROL_PLAN.json').read_text());before=snapshot(ROOT);checks=[];hydrated=[]
bindings=json.loads((ROOT/'PACKING/REVIEW_AND_DEPENDENCY_BINDINGS.json').read_text())
with tempfile.TemporaryDirectory(prefix='t20-eleventh-python-') as tmp:
    work=Path(tmp)/'copy';shutil.copytree(ROOT,work)
    for row in bindings['external_predecessor_bindings']:
        with zipfile.ZipFile(archives[row['predecessor_archive_sha256']]) as z: data=z.read(row['archive_member'])
        assert hashlib.sha256(data).hexdigest()==row['sha256']
        rel=Path(row['path']);assert not rel.is_absolute() and '..' not in rel.parts
        p=work/rel;assert not p.exists();p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
        hydrated.append({'path':row['path'],'sha256':row['sha256'],'archive_sha256':row['predecessor_archive_sha256'],'used_for':'Input digest checks only; not executed or rebundled'})
    for cmd in plan['commands']:
        assert sha(ROOT/cmd['script'])==cmd['script_sha256']
        for rel in cmd['generated_outputs']:(work/rel).unlink(missing_ok=True)
        env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONOPTIMIZE='0')
        try:
            proc=subprocess.run([sys.executable,str(work/cmd['script'])],cwd=work/cmd['cwd'],env=env,capture_output=True,timeout=1800)
            stdout,stderr,code=proc.stdout,proc.stderr,proc.returncode
        except subprocess.TimeoutExpired as exc:stdout,stderr,code=exc.stdout or b'',exc.stderr or b'',124
        (out/(cmd['id']+'.stdout.log')).write_bytes(stdout);(out/(cmd['id']+'.stderr.log')).write_bytes(stderr)
        row={'id':cmd['id'],'script':cmd['script'],'script_sha256':cmd['script_sha256'],'exit_code':code,'generated_outputs':[]}
        for rel in cmd['generated_outputs']:
            actual,expected=work/rel,ROOT/rel
            row['generated_outputs'].append({'path':rel,'expected_sha256':sha(expected),'actual_sha256':sha(actual) if actual.is_file() else None,'byte_match':actual.is_file() and actual.read_bytes()==expected.read_bytes()})
        row['status']='PASS' if code==0 and all(r['byte_match'] for r in row['generated_outputs']) else 'FAIL'
        checks.append(row);print(cmd['id'],row['status'],flush=True)
        if row['status']!='PASS': break
    for row in hydrated: assert sha(work/row['path'])==row['sha256']
unchanged=before==snapshot(ROOT)
for digest,p in archives.items(): assert sha(p)==digest
receipt={'created_utc':datetime.now(timezone.utc).isoformat(),'status':'PASS' if unchanged and len(checks)==len(plan['commands']) and all(r['status']=='PASS' for r in checks) else 'FAIL','classification':'FRESH_PACKAGING_REPLAY_NOT_NEW_RESEARCH_OR_ACCEPTANCE','python':sys.version,'dependencies':{x:importlib.metadata.version(x) for x in ['mpmath','sympy']},'checks':checks,'temporary_external_dependencies':hydrated,'predecessor_archives_unchanged':True,'frozen_checkpoint_bytes_unchanged':unchanged,'comparison':'Exact generated-output bytes; no ignored timestamp or scientific fields. Stdout/stderr retained as logs.','proof_by_finite_scan':False,'source_body_rechecks':False,'empirical_validation':False,'new_kernel_verification':False,'research_duration_credit_seconds':0}
(out/'REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');assert receipt['status']=='PASS',receipt
