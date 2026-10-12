#!/usr/bin/env python3
from pathlib import Path
import argparse,hashlib,json,os,re,subprocess,tempfile,zipfile

p=argparse.ArgumentParser();p.add_argument('--lean',action='store_true');p.add_argument('--environment',type=Path);a=p.parse_args()
b=Path(__file__).resolve().parent;sha=lambda data:hashlib.sha256(data).hexdigest()
m=json.loads((b/'MANIFEST.json').read_text())
for f in m['files']:
    data=(b/f['path']).read_bytes();assert len(data)==f['bytes'] and sha(data)==f['sha256'],f['path']
assert sha((b/'author-packet.zip').read_bytes())=='a7bc903469a362de66fe8012a616b01d526386c92bf6d5a94e82736620749f2c'
sr=b/'source-reference'
with zipfile.ZipFile(b/'author-packet.zip') as z:
    assert sha(z.read('MANIFEST.json'))=='11619edcc659151ab0aeb1738396b9e180f0e24b3675ef7bc180aed1f49e42d3'
    am=json.loads(z.read('MANIFEST.json'))
    assert set(z.namelist())==set(am)|{'MANIFEST.json'}
    for n,h in am.items():assert z.read(n)==(sr/n).read_bytes() and sha(z.read(n))==h,n
controls=json.loads(subprocess.check_output(['python',str(b/'check_controls.py')],text=True))
assert controls==json.loads((b/'evidence/EXACT_CONTROLS.json').read_text())
sources=list((sr/'src').glob('*.lean'))+[b/'src/CheckerContractProbe.lean']
for s in sources:assert not re.search(r'\b(sorry|admit|native_decide)\b|^\s*(axiom|unsafe)\b',s.read_text(),re.M),s
footprints={}
for log in (b/'evidence').glob('*.log'):
    text=log.read_text();assert 'sorryAx' not in text and 'error:' not in text,log
    for name,body in re.findall(r"'([^']+)' depends on axioms: \[(.*?)\]",text,re.S):
        footprints[name]={x.strip() for x in body.split(',') if x.strip()}
assert len(footprints)==33,len(footprints)
for name,fs in footprints.items():assert fs<={'propext','Classical.choice','Quot.sound'},(name,fs)
if a.lean:
    footprints={}
    e=(a.environment or b.parents[1]/'recovery-20261001/environment').resolve()
    with tempfile.TemporaryDirectory(prefix='pd-checker-review-') as tmp:
        td=Path(tmp)/'custom'
        subprocess.run(['python','-B',str(sr/'replay.py'),'--environment',str(e),'--output',str(td)],check=True,stdout=subprocess.PIPE,text=True)
        for log in td.glob('*.log'):
            for name,body in re.findall(r"'([^']+)' depends on axioms: \[(.*?)\]",log.read_text(),re.S):
                footprints[name]={x.strip() for x in body.split(',') if x.strip()}
        paths=[td,e/'mathlib4/.lake/build/lib/lean']+sorted((e/'mathlib4/.lake/packages').glob('*/.lake/build/lib/lean'))
        s=b/'src/CheckerContractProbe.lean'
        r=subprocess.run([str(e/'toolchain/lean-4.19.0-linux/bin/lean'),'-j1','--root='+str(s.parent),'-o',str(td/'CheckerContractProbe.olean'),str(s)],env=dict(os.environ,LEAN_PATH=':'.join(map(str,paths))),text=True,capture_output=True)
        assert r.returncode==0,r.stdout+r.stderr
        assert 'sorryAx' not in r.stdout
        for name,body in re.findall(r"'([^']+)' depends on axioms: \[(.*?)\]",r.stdout,re.S):
            footprints[name]={x.strip() for x in body.split(',') if x.strip()}
        assert len(footprints)==33,len(footprints)
        for name,fs in footprints.items():assert fs<={'propext','Classical.choice','Quot.sound'},(name,fs)
print(json.dumps({'status':'PASS','sources':7,'exact_assertions':controls['exact_assertions'],
 'lean_replayed':a.lean,'axiom_footprints':len(footprints),'verdict':'ACCEPTED_LOCAL_CONSTRUCTION_AND_RESTRICTION',
 'formal_complexity_credit':False,'global_path_law_credit':False},indent=2))
