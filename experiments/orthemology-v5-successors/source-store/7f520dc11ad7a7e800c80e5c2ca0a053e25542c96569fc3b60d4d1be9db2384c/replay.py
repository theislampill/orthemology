#!/usr/bin/env python3
"""Bounded 4.19 replay of the new finite application only; no network or Lake."""
from pathlib import Path
import argparse, os, json, hashlib, re, subprocess, sys, datetime

def guarded_output(requested, protected):
    # Check both the user's lexical path and its actual filesystem destination.
    requested = Path(requested)
    if requested.exists() or requested.is_symlink():
        raise RuntimeError('Refusing an existing output path or symlink')
    lexical = Path(os.path.abspath(requested))
    output = requested.resolve()
    for raw in protected:
        raw = Path(raw)
        lexical_root = Path(os.path.abspath(raw))
        actual_root = raw.resolve()
        if lexical.is_relative_to(lexical_root) or output.is_relative_to(actual_root):
            raise RuntimeError('Output must be outside every protected input tree')
        # Internal cache aliases are allowed. Escaping aliases are unsupported,
        # including a dependency directory symlink into a separate object store.
        if actual_root.is_dir():
            for parent, directories, files in os.walk(actual_root, followlinks=False):
                for name in directories + files:
                    item = Path(parent) / name
                    if item.is_symlink() and not item.resolve().is_relative_to(actual_root):
                        raise RuntimeError('Escaping symlinked input layout is unsupported')
    if not output.parent.is_dir():
        raise RuntimeError('Output parent must already exist')
    return output

def verify_public_package(root):
    manifest = json.loads((root / 'SOURCE_PACKAGE.json').read_text())
    for row in manifest['files']:
        rel = Path(row['path'])
        if rel.is_absolute() or '..' in rel.parts: raise RuntimeError('Unsafe package member')
        path = root / rel
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != row['sha256'] or path.stat().st_size != row['bytes']:
            raise RuntimeError('Selected source package identity mismatch: ' + row['path'])
    return manifest


HERE=Path(__file__).resolve().parent
PACKAGE=HERE.parent
LEAN_SHA='92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def require(ok,msg):
 if not ok:raise RuntimeError(msg)
def dump(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--lean',type=Path,required=True)
 parser.add_argument('--cache',type=Path,required=True)
 parser.add_argument('--output',type=Path,required=True)
 args=parser.parse_args()
 require(not args.output.is_symlink(),'Refusing existing output symlink')
 out=args.output.resolve();PREP=args.cache.resolve();lean=args.lean.resolve()
 require(not out.exists(),'Output must be fresh')
 require(out.parent.is_dir(),'Output parent must exist')
 require(not any(out.is_relative_to(p) for p in [PACKAGE,PREP,lean.parent.parent]),'Output must be outside source, cache and compiler trees')
 out=guarded_output(args.output,[PACKAGE,args.cache,args.lean.parent.parent,lean.parent.parent])
 verify_public_package(PACKAGE)
 require(sha(lean)==LEAN_SHA,'Compiler hash mismatch')
 require(sha(PREP/'PREPARATION_RECEIPT.json')=='4b1c06c026eb6a7e15e6699e67b7322f8514f36fadba9c58e9975e5b0d0dfcf7','Preparation receipt identity mismatch')
 out.mkdir();objs=out/'objects';objs.mkdir()
 packages=json.loads((PREP/'PREPARATION_RECEIPT.json').read_text())['source_revisions']
 paths=[objs]+[PREP/'dependencies'/r['name']/'.lake/build/lib/lean' for r in packages]
 env=os.environ.copy();env['LEAN_PATH']=':'.join(map(str,paths));env['LEAN_NUM_THREADS']='1'
 sources=['TraceControls.lean','RationalFixtures.lean','ReadbackAudit.lean','ImportClosure.lean','tests/Contract.lean','tests/RejectedClaims.lean']
 before={s:sha(HERE/s) for s in sources};commands=[]
 # This is a lexical guard, not a substitute for the kernel or axiom readbacks.
 for s in ['TraceControls.lean','RationalFixtures.lean']:
  body=(HERE/s).read_text();require(not re.search(r'\b(sorry|admit|native_decide|unsafe|axiom)\b',body),'Unexpected authored admission/escape token')
 def run(label,args,expected=0):
  cmd=[str(lean),'-j1','--trust=0']+list(map(str,args));r=subprocess.run(cmd,cwd=HERE,env=env,text=True,capture_output=True,timeout=180);txt=r.stdout+r.stderr;(out/label).write_text(txt);commands.append({'command':cmd,'exit_code':r.returncode,'log':label,'log_sha256':sha(out/label)})
  require((r.returncode==0)==(expected==0),'Unexpected exit: '+label)
  if expected==0:require(not re.search(r'\berror:|\bwarning:|\bsorryAx\b|PANIC',txt),'Unexpected diagnostic: '+label)
  return txt
 run('version.log',['--version'])
 for mod in ['TraceControls','RationalFixtures']:run(mod+'.log',['-o',objs/(mod+'.olean'),HERE/(mod+'.lean')])
 run('contract-green.log',[HERE/'tests/Contract.lean'])
 tx=run('readback.log',[HERE/'ReadbackAudit.lean']);names=json.loads((HERE/'DECLARATIONS.json').read_text());readbacks={}
 for n in names:
  chunks=re.findall(r'^TRACE_BEGIN '+re.escape(n)+r'\n(.*?)^TRACE_END '+re.escape(n)+r'$',tx,re.M|re.S);require(len(chunks)==1,'Readback block '+n);chunk=chunks[0].strip();pivot=chunk.index("'"+n+"' ");typ=chunk[:pivot].strip();ax=chunk[pivot:];axes=[] if 'does not depend on any axioms' in ax else sorted(x.strip() for x in re.search(r'\[([^]]*)\]',ax,re.S)[1].split(','));require(set(axes)<={'propext','Classical.choice','Quot.sound'},'Unexpected axioms '+n);readbacks[n]={'type':typ,'type_sha256':hashlib.sha256(typ.encode()).hexdigest(),'axioms':axes}
 dump(out/'READBACKS.json',readbacks)
 neg=run('rejected.log',[HERE/'tests/RejectedClaims.lean'],expected=1);require(neg.count('error:')==4,'Expected four false-claim rejections');require(neg.count("tactic 'decide' proved that the proposition")==1 and neg.count('unsolved goals')==3 and neg.count('⊢ False')==3,'Rejections must be semantic false propositions')
 closure=run('imports.log',[HERE/'ImportClosure.lean']);mods=re.findall(r'KERNEL_IMPORT (\S+)',closure);require(len(mods)==len(set(mods)) and mods,'Invalid import closure');allpaths=paths+[lean.parent.parent/'lib/lean'];bindings=[]
 for mod in mods:
  found=[p/(mod.replace('.','/')+'.olean') for p in allpaths if (p/(mod.replace('.','/')+'.olean')).is_file()];require(len(found)==1,'Missing or ambiguous object '+mod);f=found[0];bindings.append({'module':mod,'object':str(f),'sha256':sha(f),'fresh_local':f.is_relative_to(objs)})
 dump(out/'IMPORT_BINDINGS.json',bindings)
 require(before=={s:sha(HERE/s) for s in sources},'Source changed during verification')
 require(all(sha(Path(b['object']))==b['sha256'] for b in bindings),'Import object changed during readback')
 verify_public_package(PACKAGE)
 receipt={'status':'AUTHOR_PASS_AWAITING_INDEPENDENT_REVIEW','finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Finite ordered-field length-two deletion-channel application, with exact rational fixtures. No upstream trace theorem/decoder, real-module replay, asymptotic convergence, historical source authenticity, authority or empirical validation.','compiler_sha256':LEAN_SHA,'mathlib_revision':packages[0]['revision'],'dependency_mode':'Existing official pinned objects trusted and hash-bound, not rebuilt; no Lake/network/install.','source_hashes':before,'object_hashes':{f.name:sha(f) for f in objs.glob('*.olean')},'readback_theorems':len(readbacks),'negative_claims_rejected':4,'imported_objects':len(bindings),'axioms_observed':sorted(set(a for r in readbacks.values() for a in r['axioms'])),'readback_sha256':sha(out/'READBACKS.json'),'bindings_sha256':sha(out/'IMPORT_BINDINGS.json'),'commands':commands,'red_contract':'Earlier empty-module missing-endpoint red log retained in logs/contract-red.log; not a mathematical negative result.','ownership':'General information principle inherited H-ICS/T9; this is selected application evidence.','new_upstream_science_admitted':False}
 dump(out/'VERIFICATION.json',receipt);print(json.dumps({k:receipt[k] for k in ['status','readback_theorems','negative_claims_rejected','imported_objects','axioms_observed']},indent=2))
if __name__=='__main__':
 try:main()
 except Exception as e:print('FAIL:',str(e),file=sys.stderr);sys.exit(1)
