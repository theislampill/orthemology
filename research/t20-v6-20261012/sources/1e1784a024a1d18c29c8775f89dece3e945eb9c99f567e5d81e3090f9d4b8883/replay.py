#!/usr/bin/env python3
from pathlib import Path
import argparse,hashlib,json,os,re,subprocess,sys
P=argparse.ArgumentParser();P.add_argument('--environment',type=Path,required=True);P.add_argument('--output',type=Path,required=True);a=P.parse_args()
b=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
man=json.loads((b/'MANIFEST.json').read_text())
for name,h in man.items():assert sha(b/name)==h,name
actual={str(p.relative_to(b)) for p in b.rglob('*') if p.is_file() and p.name!='PD_Checker_Restriction_Formal_Candidate_1_20261001.zip'}
assert actual==set(man)|{'MANIFEST.json'},actual^(set(man)|{'MANIFEST.json'})
assert not a.output.exists(),'Fresh output must not exist'
assert not a.output.resolve().is_relative_to(b),'Output must be outside candidate'
e=json.loads((b/'ENVIRONMENT.json').read_text());envroot=a.environment.resolve()
lean=envroot/'toolchain/lean-4.19.0-linux/bin/lean';mathlib=envroot/'mathlib4'
assert sha(lean)==e['lean_binary_sha256']
version=subprocess.check_output([str(lean),'--version'],text=True)
assert e['lean_version'] in version and e['lean_commit'] in version
assert sha(mathlib/'lake-manifest.json')==e['lake_manifest_sha256']
paths=[mathlib/'.lake/build/lib/lean']
for path,commit in [(mathlib,e['mathlib_commit'])]+[(mathlib/'.lake/packages'/n,c) for n,c in e['official_packages'].items()]:
 assert subprocess.check_output(['git','-C',str(path),'rev-parse','HEAD'],text=True).strip()==commit
 assert not subprocess.check_output(['git','-C',str(path),'status','--porcelain','--untracked-files=no'],text=True).strip()
 lib=path/'.lake/build/lib/lean'
 if path!=mathlib and lib.is_dir():paths.append(lib)
order=['CheckerKernel','CheckerSemantics','InitialCheckerBelief','CheckerStateObservation','HonestCheckerStep','CheckerControls']
seen={'Mathlib'};expected=[]
for name in order:
 src=(b/'src'/(name+'.lean')).read_text()
 assert not re.search(r'\b(sorry|admit|axiom|unsafe|native_decide)\b',src),name
 for imports in re.findall(r'^import\s+(.+)$',src,re.M):assert set(imports.split())<=seen,(name,imports)
 for lib in paths:assert not (lib/(name+'.olean')).exists(),('custom shadow',lib,name)
 seen.add(name)
 expected+=re.findall(r'^#print axioms\s+(\S+)',src,re.M)
assert len(expected)==24
ordinary=json.loads((b/'SOURCE_PROVENANCE.json').read_text())
assert sha(b/'reference/PD_EXPTIME_HARDNESS_CANDIDATE.md')==ordinary['ordinary_source_sha256']
a.output.mkdir(parents=True)
env=os.environ.copy();env['LEAN_PATH']=':'.join(map(str,[a.output.resolve()]+paths));env['PYTHONDONTWRITEBYTECODE']='1'
prints={}
for name in order:
 cmd=[str(lean),'-j1','--root='+str(b/'src'),'-o',str((a.output/(name+'.olean')).resolve()),str(b/'src'/(name+'.lean'))]
 r=subprocess.run(cmd,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 (a.output/(name+'.log')).write_text(r.stdout)
 assert r.returncode==0,r.stdout
 assert not re.search(r"sorryAx|uses 'sorry'|error:|PANIC|panicked",r.stdout),r.stdout
 for declaration,body in re.findall(r"'([^']+)' depends on axioms: \[(.*?)\]",r.stdout,re.S):
  footprint={s.strip() for s in body.split(',') if s.strip()}
  assert footprint<= {'propext','Classical.choice','Quot.sound'},(declaration,footprint)
  prints[declaration]=sorted(footprint)
assert set(prints)==set(expected),(set(expected)-set(prints),set(prints)-set(expected))
result={'status':'PASS_FRESH_SIX_SOURCE_REPLAY','lean_version':version.strip(),'mathlib_commit':e['mathlib_commit'],'module_count':len(order),'axiom_readbacks':len(prints),'axioms':prints,'official_objects_trusted':True,'custom_objects_reused':False,'formal_ATM_hardness':False}
(a.output/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='axioms'}))
