from pathlib import Path
import hashlib,json,re,subprocess,os,time
ROOT=Path(__file__).resolve().parent
SRC=ROOT/'sources'; OUT=ROOT/'build'; LOG=ROOT/'receipts'; [p.mkdir(exist_ok=True) for p in (SRC,OUT,LOG)]
P=Path('private-locator:6e1cdd2685640ba2eef0'); F=Path('private-locator:4b06887cf6b87610e5b8'); M=Path('private-locator:45dfd5c4544eed9a5f10')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
seals={str(M.parent/'Mealy_Measure_Bridge_Stage1_20260930.zip'):'a4755cb68772a0394458fb81a2a77ca4d2388aff6d1f8d4073ecfe8e0da3e590',str(P/'receipts/loop-20260930T142933Z/LOOP_RESULT.json'):'0d7a327ec9d8f73a3481972d31f494258d63613459f0c48f01ada7c24a311a9e',str(P/'receipts/sigma2-20260930T144631Z/SIGMA2_RESULT.json'):'266c4a739a092eb9ba474ebc819b183ef22bc9e7cdf5f7f0ccc6b563694d23de'}
for p,h in seals.items(): assert sha(Path(p))==h,(p,sha(Path(p)))
for line in (M/'SHA256SUMS').read_text().splitlines():
 h,p=line.split(maxsplit=1); assert sha(M/p)==h,p
for seal in list(seals)[1:]:
 r=json.loads(Path(seal).read_text())
 for m,h in r['source_sha256'].items(): assert sha(P/(m+'.lean'))==h,m
mods={};order=[]
def add(m):
 if m in mods:return
 p=next((root/(m.replace('.','/')+'.lean') for root in (M,P,F) if (root/(m.replace('.','/')+'.lean')).is_file()),None)
 if p is None:return
 mods[m]={'origin':str(p),'sha256':sha(p)}
 dst=SRC/(m.replace('.','/')+'.lean');dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(p.read_bytes())
 for line in dst.read_text().splitlines():
  if line.startswith('import '):
   for dep in line[7:].split():add(dep)
 order.append(m)
for m in ['MealyMeasureFixtures','Verification','LoopAudit','Sigma2Audit']:add(m)
(ROOT/'manifest.json').write_text(json.dumps({'seals':seals,'sources':mods,'order':order},indent=2)+'\n')
math=F/'mathlib4';paths=[OUT,math/'.lake/build/lib/lean']+[p/'.lake/build/lib/lean' for p in (math/'.lake/packages').iterdir() if (p/'.lake/build/lib/lean').is_dir()]
env={**os.environ,'PATH':str(F/'lean-4.19.0-linux/bin')+':'+os.environ['PATH'],'LEAN_PATH':':'.join(map(str,paths))};env.pop('LEAN_NUM_THREADS',None)
assert subprocess.check_output(['lean','--version'],env=env,text=True).strip()=='Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)'
assert subprocess.check_output(['git','-C',str(math),'rev-parse','HEAD'],text=True).strip()=='c44e0c8ee63ca166450922a373c7409c5d26b00b'
(ROOT/'env.sh').write_text('export PATH='+str(F/'lean-4.19.0-linux/bin')+':$PATH\nexport LEAN_PATH='+':'.join(map(str,paths))+'\n')
results=[]
for m in order:
 p=SRC/(m.replace('.','/')+'.lean');o=OUT/(m.replace('.','/')+'.olean');o.parent.mkdir(parents=True,exist_ok=True)
 cmd=['lean','-j1','--root='+str(SRC),'-o',str(o),str(p)];t=time.time();res=subprocess.run(cmd,cwd=SRC,env=env,capture_output=True,text=True)
 (LOG/(m+'.log')).write_text(res.stdout+res.stderr)
 record={'module':m,'command':cmd,'exit':res.returncode,'seconds':time.time()-t,'source_sha256':sha(p)};results.append(record)
 (ROOT/'BUILD_RESULTS.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(record),flush=True)
 if res.returncode:print(res.stdout+res.stderr);raise SystemExit(res.returncode)
 for n,a in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",res.stdout+res.stderr): assert set(x.strip() for x in a.split(','))<={'propext','Classical.choice','Quot.sound'},(n,a)
assert all(sha(Path(v['origin']))==v['sha256'] for v in mods.values())
print('FRESH_REBUILD_COMPLETE',len(order),flush=True)
