#!/usr/bin/env python3
from pathlib import Path
import argparse,datetime,hashlib,json,os,re,subprocess,sys
ROOT=Path(__file__).resolve().parent;BASE=ROOT.parent/'python-bases/source/lean'
MODULES=['InternalPolymorphism','FiniteBridge','SourceTypeOps','SourceHeadStep','SourceChecker','SourceCheckerProofs','SourceResources','SourceRepresentation','SourceResourceBounds','SourceControls','SourceBranchControls','SourceExportBoundary','SourceCheckerAudit','NativeDecoder','NativeDecoderProofs','NativeDecoderSoundness','NativeProofGrammar','NativeProofSoundness','NativeCheckerBridge','NativeFieldLemmas','NativeDecoderCompleteness','NativeRepresentationEquivalence','NativeDecoderControls','NativeDecoderAudit']
TARGETS=['P03Source.sourceScoped_eq','P03Source.sourceInstantiate_eq','P03Source.sourceHeadStep_eq','P03Source.trace_matches','P03Source.source_core_export_square','P03Source.sourceRun_refines_core','P03Source.sourceCheck_refines_core','P03Source.source_checker_constructor_erasure_square','P03Source.source_checker_sound','P03SourceControls.erased_checker_acceptance_is_not_source_acceptance','P03Source.proofTree_shape','P03Source.sourceCheck_input_guards','P03Source.semantic_refusal_preserved','P03Source.semantic_singleton_trace','P03Source.encoded_nodes_le_export_work','P03Source.partial_constructor_export_square','P03Source.source_checker_export_square','P03Source.checker_acceptance_not_total_export']
NATIVE_TARGETS = ['P03Source.decodeType_sound','P03Source.decodeTerm_sound','P03Source.decodeTrace_sound','P03Source.decodeProof_sound','P03Source.decodeNativeProof_roundtrip','P03Source.NativeProofRep.decode_complete','P03Source.NativeProofRep.deterministic','P03Source.nativeCheck_representation_equivalence','P03Source.native_checker_constructor_erasure_square','P03Source.native_checker_sound','P03Source.native_check_rejects_duplicate_fields','P03Source.native_checker_partial_export_square']
TARGETS += NATIVE_TARGETS
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 a=argparse.ArgumentParser();a.add_argument('--out',type=Path,required=True);a.add_argument('--lean',type=Path,default=Path('private-locator:4211d241978f643cb623'));args=a.parse_args();out=args.out.resolve()
 if out.exists():raise SystemExit('Fresh directory required')
 out.mkdir(parents=True);lean=args.lean.resolve();env={**os.environ,'LEAN_PATH':str(out),'PYTHONDONTWRITEBYTECODE':'1'};env.pop('LEAN_SYSROOT',None)
 receipt={'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'native_lean':str(lean),'native_sha256':sha(lean.read_bytes()),'source_files':{},'commands':[],'artifacts':{},'targets':{},'status':'RUNNING','canonical_effect':False,'scope':'Seven-rule modeled source-AST constructor/export square; not CPython/JSON proof'}
 def save(): (out/'RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
 def run(label,args):
  p=subprocess.run(args,cwd=out,env=env,capture_output=True,timeout=180);(out/(label+'.stdout')).write_bytes(p.stdout);(out/(label+'.stderr')).write_bytes(p.stderr);receipt['commands'].append({'label':label,'argv':args,'exit_code':p.returncode,'stdout_sha256':sha(p.stdout),'stderr_sha256':sha(p.stderr)});save()
  if p.returncode or re.search(rb'\berror:|\bsorryAx\b',p.stdout+p.stderr):raise RuntimeError(label+' failed')
  return p.stdout.decode()
 try:
  if lean.read_bytes()[:4]!=b'\x7fELF' or sha(lean.read_bytes())!='92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023':raise RuntimeError('Require exact archived native Linux Lean4.19 binary')
  version=run('version',[str(lean),'--version'])
  if '4.19.0' not in version or '6caaee842e94' not in version:raise RuntimeError('Wrong compiler')
  for name in MODULES:
   source=(BASE if name in MODULES[:2] else ROOT)/(name+'.lean');data=source.read_bytes();(out/source.name).write_bytes(data);receipt['source_files'][source.name]={'origin':str(source),'bytes':len(data),'sha256':sha(data)}
   raw=run(name,[str(lean),'-o',name+'.olean',source.name]);art=out/(name+'.olean')
   if not art.is_file() or art.stat().st_size==0:raise RuntimeError('Missing object '+name)
   receipt['artifacts'][art.name]={'bytes':art.stat().st_size,'sha256':sha(art.read_bytes())};save()
  audit=(out/'SourceCheckerAudit.stdout').read_text()+'\n'+(out/'NativeDecoderAudit.stdout').read_text()
  for target in TARGETS:
   if not re.search(r'(?m)^@?'+re.escape(target)+r'(?:\.\{[^}]*\})?\s*:',audit):raise RuntimeError('Missing type '+target)
   matches=re.findall(r"^'"+re.escape(target)+r"' (does not depend on any axioms|depends on axioms: \[([^\]]*)\])$",audit,re.M)
   if len(matches)!=1:raise RuntimeError('Ambiguous/missing axiom output '+target)
   used=sorted(x.strip() for x in matches[0][1].split(',') if x.strip())
   allowed={'propext','Quot.sound'} | ({'Classical.choice'} if target in NATIVE_TARGETS else set())
   if set(used)-allowed:raise RuntimeError('Unapproved axioms '+target)
   receipt['targets'][target]={'type_readback':True,'axioms':used}
  receipt['status']='FRESH_NATIVE_BUILD_AND_DECLARATION_READBACK_PASS';receipt['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();save();print(json.dumps({'status':receipt['status'],'sources':len(receipt['source_files']),'objects':len(receipt['artifacts']),'targets':len(receipt['targets'])}))
 except Exception as ex:receipt['status']='FAIL';receipt['error']=repr(ex);save();raise
if __name__=='__main__':main()
