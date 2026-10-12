"""Compile review-only probes against freshly replayed candidate modules."""
from pathlib import Path
import hashlib,json,os,re,subprocess
R=Path(__file__).resolve().parent;W=R.parent
LEAN=W/'.toolchains/lean-4.19.0-linux/bin/lean'
core=json.loads((R/'REPLAY_RECEIPT.json').read_text())
env=dict(os.environ,LEAN_PATH=':'.join(core['isolated_lean_path']))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
results=[]
for module,expected in [('IndependentProbes',2),('AllAxiomClosures',72)]:
    source=R/(module+'.lean');obj=R/'replay'/(module+'.olean')
    args=[str(LEAN),'--trust=0','-o',str(obj),str(source)]
    p=subprocess.run(args,cwd=R,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    log=R/'evidence'/(module+'.log');log.write_text(p.stdout)
    assert p.returncode==0 and 'sorryAx' not in p.stdout,(module,p.stdout)
    axioms=re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",p.stdout)
    assert len(axioms)==expected,(module,axioms)
    for _,deps in axioms:assert set(deps.split(', '))<= {'propext','Classical.choice','Quot.sound'}
    results.append({'module':module,'command':args,'returncode':p.returncode,'axiom_closures':len(axioms),'source_sha256':sha(source),'object_sha256':sha(obj),'log_sha256':sha(log)})
(R/'evidence/probe-receipt.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps({'status':'PASS','extra_modules':len(results),'standard_only_axiom_closures':sum(x['axiom_closures'] for x in results)},indent=2))
