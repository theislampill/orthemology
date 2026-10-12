"""Additive nonmutating source verifier and optional fresh Lean build.
Never invokes historical scripts that overwrite original verification receipts.
"""
from pathlib import Path
import argparse,concurrent.futures,hashlib,json,os,re,subprocess,sys
R=Path(__file__).resolve().parent;P=R/'payload'
UP='rational-threshold-formal-extension-20261011';LOW='rational-shift-realisation-20261011'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def require(ok,msg):
 if not ok:raise RuntimeError(msg)
def verify():
 for x in json.loads((R/'MANIFEST.json').read_text()):
  p=R/x['path'];require(p.is_file(),'Missing '+x['path']);require(p.stat().st_size==x['bytes'] and sha(p)==x['sha256'],'Manifest mismatch '+x['path'])
 for x in json.loads((R/'PRESERVATION_MAP.json').read_text()):require(sha(R/x['preserved'])==x['sha256'],'Original identity mismatch '+x['source'])
 acq=json.loads((P/UP/'ACQUISITION.json').read_text());require(len(acq['source_members'])==77,'Wrong baseline count')
 for x in acq['source_members']:require(sha(P/x['path'])==x['sha256'],'Acquisition source mismatch '+x['path'])
 for x in json.loads((P/LOW/'FROZEN_SOURCE_MANIFEST.json').read_text())['sources']:require(sha(P/x['path'])==x['sha256'],'Lower frozen source mismatch '+x['path'])
 # Preserve and explicitly check the additive upper prose-binding superseder.
 s=json.loads((P/'rational-threshold-independent-review-20261011/BINDING_SUPERSEDER_20261011T0522Z.json').read_text());text=(P/s['path']).read_text()
 require(sha(P/s['path'])==s['current_sha256'],'Superseded current prose mismatch')
 require(hashlib.sha256(text.replace('horizon 4.','horizon4.').encode()).hexdigest()==s['historical_sha256'],'Historical prose reconstruction mismatch')
 return {'status':'PASS','baseline_sources':77,'frozen_lower_sources':5,'scope':'Delivered source integrity, not dependency-equipped kernel replay'}
def build(args):
 verify();lean=Path(args.lean).resolve();deps=Path(args.dependencies).resolve();out=Path(args.output).resolve();out.mkdir(parents=True,exist_ok=False)
 version=subprocess.check_output([str(lean),'--version'],text=True).strip();require('version 4.19.0,' in version,'Lean 4.19.0 required')
 pins=json.loads((P/UP/'DEPENDENCY_OBJECT_PINS.json').read_text())['objects'];depchecked=0
 for x in pins:
  marker='/dependency-overlay/.lake/packages/'
  if marker in x['path']:p=deps/x['path'].split(marker,1)[1]
  elif x['path'].startswith('.toolchains/lean-4.19.0-linux/'):p=lean.parent.parent/x['path'].split('.toolchains/lean-4.19.0-linux/',1)[1]
  else:raise RuntimeError('Unexpected dependency pin path '+x['path'])
  require(p.is_file() and sha(p)==x['sha256'],'Dependency pin mismatch '+str(p));depchecked+=1
 paths=[p/'.lake/build/lib/lean' for p in deps.iterdir() if (p/'.lake/build/lib/lean').is_dir()]
 obj=out/'objects';obj.mkdir();logs=out/'logs';logs.mkdir();env=dict(os.environ,LEAN_PATH=':'.join(map(str,[obj]+paths)))
 results=[]
 def compile_one(label,src,module=None,negative=False,allow_warning=False):
  target=obj/Path((module or src.stem).replace('.','/')).with_suffix('.olean');target.parent.mkdir(parents=True,exist_ok=True)
  cmd=[str(lean),'--trust=0']+([] if negative else ['-o',str(target)])+[str(src)]
  p=subprocess.run(cmd,cwd=P,env=env,text=True,capture_output=True);text=p.stdout+p.stderr;(logs/(label+'.log')).write_text(text)
  if negative:
   require(p.returncode!=0 and 'error:' in text and not any(t in text for t in ['unknown module','unknown identifier','file not found','object file']),label+' failed for wrong reason or passed')
  else:require(p.returncode==0 and 'sorryAx' not in text and (allow_warning or 'warning:' not in text),label+' failed: '+text)
  return {'label':label,'source':str(src.relative_to(P)) if src.is_relative_to(P) else str(src),'source_sha256':sha(src),'exit_code':p.returncode,'expected_failure':negative,'log_sha256':sha(logs/(label+'.log'))}
 baseline=P/UP/'baseline';mods={str(p.relative_to(baseline).with_suffix('')).replace('/','.'):p for p in baseline.rglob('*.lean')}
 requires={m:{v for l in p.read_text().splitlines() if l.strip().startswith('import ') for v in l.strip().split()[1:] if v in mods} for m,p in mods.items()};done=set()
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
  while len(done)<len(mods):
   ready=[m for m in mods if m not in done and requires[m]<=done];require(bool(ready),'Baseline cycle')
   results+=list(pool.map(lambda m:compile_one('baseline-'+m,mods[m],m,allow_warning=True),ready));done.update(ready);print('Baseline',len(done),'/ 77',flush=True)
 for name in ['RationalThresholdCuts','RationalThresholdComputable','RationalThresholdUniform','RationalThresholdDefect','RationalThresholdControls','RationalThresholdAudit']:
  results.append(compile_one('upper-'+name,P/UP/(name+'.lean')))
 for x in json.loads((P/LOW/'FROZEN_SOURCE_MANIFEST.json').read_text())['sources']:
  src=P/x['path'];results.append(compile_one('lower-'+src.stem,src))
 # Independent reviewer audits and positive-control source remain separate.
 for directory,name in [('rational-threshold-independent-review-20261011','InspectAxioms'),('rational-shift-independent-review-20261011','InspectAxioms'),('rational-shift-independent-review-20261011','PositiveControls')]:
  results.append(compile_one(directory+'-'+name,P/directory/(name+'.lean')))
 # Parse the original explicit target audits, including fifth-module Sigma2.
 audittext='\n'.join((logs/x).read_text() for x in ['upper-RationalThresholdAudit.log','rational-shift-independent-review-20261011-InspectAxioms.log','lower-Sigma2ThresholdRealisation.log'])
 audits=[]
 for name,body in re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",audittext,re.S):
  axioms=[x.strip() for x in body.split(',') if x.strip()];require(set(axioms)<={'propext','Classical.choice','Quot.sound'},'Unexpected axioms '+name);audits.append({'declaration':name,'axioms':axioms})
 for name in re.findall(r"'([^']+)' does not depend on any axioms",audittext):audits.append({'declaration':name,'axioms':[]})
 require(len(audits)==80,'Expected 38 upper plus 41 lower-review plus one Sigma2 audits, got '+str(len(audits)))
 negatives=list((P/UP/'negative-controls').glob('*.lean'))+list((P/'rational-shift-independent-review-20261011').glob('Wrong*.lean'))
 for src in sorted(negatives):results.append(compile_one('negative-'+src.stem,src,negative=True))
 # Recreate the six author mutant tests as separately identified disposable files.
 mutants=out/'mutants';mutants.mkdir()
 cases=[('wrong_endpoint','weights/BinaryWeights.lean','if a = b then true else digit a b i','if a = b then false else digit a b i'),('missing_zero_terminator_drop','compiler/UnaryPrefixRealisation.lean','(scannedBits n word).drop (i+1)','(scannedBits n word).drop i'),('unreset_base_word','compiler/UnaryPrefixRealisation.lean','F a (n-i-1) (suffixWord n word i)','F a (n-i-1) word'),('reversed_law_rows','UnaryShiftLaw.lean','if digits i then id else base','if digits i then base else id'),('sigma_zero_threshold','Sigma2ThresholdRealisation.lean','0 < r → r ≤ 1 →','0 ≤ r → r ≤ 1 →'),('sigma_threshold_above_one','Sigma2ThresholdRealisation.lean','0 < r → r ≤ 1 →','0 < r → r ≤ 2 →')]
 for label,rel,old,new in cases:
  source=(P/LOW/rel).read_text();require(source.count(old)==1,'Mutant substitution not unique');p=mutants/(label+'.lean');p.write_text(source.replace(old,new));results.append(compile_one('mutant-'+label,p,negative=True))
 # Exact rational root/reviewer controls: run only read-only stdout scripts.
 controls=[]
 for rel in ['rational-threshold-root-controls-20261011/check.py','rational-shift-root-derivation-20261011/check.py']:
  for opt in [False,True]:
   p=subprocess.run([sys.executable]+(['-O'] if opt else [])+[str(P/rel)],cwd=out,text=True,capture_output=True);require(p.returncode==0,'Root rational control failed');controls.append({'script':rel,'optimized':opt,'stdout':p.stdout})
 verify();receipt={'status':'PASS','trust':0,'lean_version':version,'lean_sha256':sha(lean),'dependency_objects_verified':depchecked,'baseline_modules_rebuilt':77,'upper_modules':6,'lower_frozen_modules':5,'axiom_audits':audits,'builds_and_failures':results,'rational_controls':controls,'dependencies_rebuilt':False,'dependencies_reacquired':False,'originals_mutated':False,'scope':'Observed fresh extracted-source build using separately installed pinned dependencies'}
 (out/'BUILD_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print('PASS build receipt '+str(out/'BUILD_RECEIPT.json'),flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--build',action='store_true');p.add_argument('--lean');p.add_argument('--dependencies');p.add_argument('--output');a=p.parse_args()
 if a.build:
  require(all([a.lean,a.dependencies,a.output]),'Build needs --lean --dependencies --output');build(a)
 else:print(json.dumps(verify(),indent=2))
