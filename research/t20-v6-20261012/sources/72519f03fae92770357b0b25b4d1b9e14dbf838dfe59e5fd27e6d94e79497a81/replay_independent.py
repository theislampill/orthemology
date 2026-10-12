from pathlib import Path
import os,subprocess,time,json,re,hashlib
R=Path(__file__).resolve().parent; W=R.parent; SRC=R/'candidate'; OUT=R/'replay';LOG=R/'evidence/replay-logs';LOG.mkdir(exist_ok=True)
LEAN=W/'.toolchains/lean-4.19.0-linux/bin/lean'
original=W/'lean-truncated-moment-obstruction-20261010'
paths=[str(OUT)]+[p for p in (SRC/'lean_path.txt').read_text().strip().split(':') if p!=str(original)]
assert str(original) not in paths and str(original/'replay-lib') not in paths
env=dict(os.environ,LEAN_PATH=':'.join(paths))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
results=[]
for name in ['TruncatedMoment','ScalarPositivity','DegreeBridge','Certificate','Controls','MomentValues','Verify']:
    source=SRC/(name+'.lean'); dest=OUT/(name+'.olean');t=time.monotonic()
    args=[str(LEAN),'--trust=0','-o',str(dest),str(source)]
    p=subprocess.run(args,cwd=SRC,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    (LOG/(name+'.log')).write_text(p.stdout)
    results.append({'module':name,'command':args,'returncode':p.returncode,'seconds':round(time.monotonic()-t,3),'source_sha256':sha(source),'object_sha256':sha(dest) if dest.exists() else None})
    (R/'evidence/replay-progress.json').write_text(json.dumps(results,indent=2)+'\n')
    assert p.returncode==0 and 'error:' not in p.stdout and 'sorryAx' not in p.stdout,(name,p.stdout)
neg=[]
for source in sorted((SRC/'negative-controls').glob('*.lean')):
    p=subprocess.run([str(LEAN),'--trust=0',str(source)],cwd=SRC,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    (LOG/source.with_suffix('.log').name).write_text(p.stdout)
    assert p.returncode!=0 and 'unsolved goals' in p.stdout and 'False' in p.stdout and not any(w in p.stdout for w in ['unknown module','does not exist','unknown identifier']),(source,p.stdout)
    neg.append({'control':source.name,'expected_rejection':True,'returncode':p.returncode,'log_sha256':sha(LOG/source.with_suffix('.log').name)})
axioms=re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",(LOG/'Verify.log').read_text());assert len(axioms)==16
for name,dep in axioms:assert set(x.strip() for x in dep.split(','))<={'propext','Classical.choice','Quot.sound'},(name,dep)
record={'status':'PASS','lean_version':subprocess.check_output([str(LEAN),'--version'],text=True).strip(),'lean_sha256':sha(LEAN),'trust':0,'isolated_lean_path':paths,'modules':results,'controls':neg,'axioms':axioms}
(R/'REPLAY_RECEIPT.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps({'status':record['status'],'modules':len(results),'rejected_controls':len(neg),'axiom_checks':len(axioms)},indent=2))
