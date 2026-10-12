#!/usr/bin/env python3
"""Portable source/kernel/control replay of this exact public science packet."""
import hashlib,json,os,pathlib,re,subprocess,sys
ROOT=pathlib.Path(__file__).resolve().parent
if len(sys.argv)!=2: raise SystemExit('Usage: python replay_public.py /absolute/fresh/output')
OUT=pathlib.Path(sys.argv[1]).resolve()
if OUT.exists(): raise SystemExit('Output must be fresh: '+str(OUT))
if OUT==ROOT or ROOT in OUT.parents: raise SystemExit('Output must be outside immutable packet')
OUT.mkdir(parents=True)
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def require(ok,msg):
    if not ok: raise RuntimeError(msg)
def verify_manifest(base,name,exact=True):
    manifest=json.loads((base/name).read_text()); paths=set()
    for row in manifest['files']:
        p=pathlib.PurePosixPath(row['path'])
        require(not p.is_absolute() and '..' not in p.parts,'Unsafe manifest path')
        f=base/p;require(f.is_file(),'Missing '+str(f))
        require(f.stat().st_size==row['size'] and digest(f)==row['sha256'],'Hash mismatch '+str(f))
        paths.add(row['path'])
    if exact:
        actual={str(p.relative_to(base)) for p in base.rglob('*') if p.is_file()}
        require(actual==paths|{name},'Unexpected packet inventory')
    return len(paths)
payload_count=verify_manifest(ROOT,'PUBLIC_MANIFEST.json')
science=ROOT/'science';review=ROOT/'review'
science_count=verify_manifest(science,'MANIFEST.json')
binding=json.loads((ROOT/'PUBLIC_BINDING.json').read_text())
require(digest(science/'MANIFEST.json')==binding['science_manifest_sha256'],'Wrong science manifest')
require(digest(review/'REVIEW_RECEIPT_V2.json')==binding['review_receipt_sha256'],'Wrong review receipt')
tools=json.loads((ROOT/'TOOLCHAIN_BINDING.json').read_text())
lean=pathlib.Path(os.environ.get('LEAN_419','private-locator:cb50f30cfa35bdf3a0cf')).resolve()
mathlib=pathlib.Path(os.environ.get('MATHLIB_C44','private-locator:18d48e051fd31eaf177f')).resolve()
require(lean.is_file() and digest(lean)==tools['lean_sha256'],'Official Lean4.19 executable hash mismatch')
for row in json.loads((ROOT/'MATHLIB_SOURCE_MANIFEST.json').read_text())['files']:
    p=mathlib/row['path']
    require(p.is_file() and p.stat().st_size==row['size'] and digest(p)==row['sha256'],'Mathlib source mismatch '+str(p))
env=os.environ.copy();env['LEAN_419']=str(lean);env['MATHLIB_C44']=str(mathlib)
def run(name,args,extra=None):
    e=env.copy()
    if extra: e.update(extra)
    p=subprocess.run(args,cwd=ROOT,env=e,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    (OUT/(name+'.log')).write_text(p.stdout)
    if p.returncode:
        print(p.stdout[-12000:]);raise RuntimeError(name+' exit '+str(p.returncode))
    print('PASS '+name,flush=True)
run('science-replay',['bash',str(science/'verify.sh'),str(OUT/'kernel')])
paths=[str(OUT/'kernel'),str(mathlib/'.lake/build/lib/lean')]
paths += [str(p) for p in sorted((mathlib/'.lake/packages').glob('*/.lake/build/lib/lean'))]
env['LEAN_PATH']=':'.join(paths)
run('independent-proofs',[str(lean),'-o',str(OUT/'kernel/IndependentChecks.olean'),str(review/'IndependentChecks.lean')])
run('all-author-axioms',[str(lean),str(review/'AllAxioms.lean')])
run('independent-primary-mutations',[sys.executable,str(review/'check_primary_mutants.py'),str(science),str(OUT/'primary-mutants'),str(lean)])
run('independent-semantics',[sys.executable,str(review/'independent_semantics.py'),str(OUT/'INDEPENDENT_SEMANTICS.json')])
run('independent-semantics-optimized',[sys.executable,'-O',str(review/'independent_semantics.py'),str(OUT/'INDEPENDENT_SEMANTICS_OPTIMIZED.json')])
require((OUT/'INDEPENDENT_SEMANTICS.json').read_bytes()==(OUT/'INDEPENDENT_SEMANTICS_OPTIMIZED.json').read_bytes(),'Reviewer optimized result differs')
require((OUT/'kernel/SEMANTIC_RESULTS.json').read_bytes()==(science/'tests/SEMANTIC_RESULTS.json').read_bytes(),'Author semantic evidence differs')
require((OUT/'INDEPENDENT_SEMANTICS.json').read_bytes()==(review/'final-replay/SEMANTICS.json').read_bytes(),'Independent semantic evidence differs')
allowed={'propext','Classical.choice','Quot.sound'}
logs=list((OUT/'kernel/logs').glob('*.log'))+[OUT/'independent-proofs.log',OUT/'all-author-axioms.log']
for p in logs:
    text=p.read_text()
    require(not any(x in text for x in ['error:','warning:','sorryAx']),'Unclean successful compiler log '+str(p))
    for match in re.findall(r'depends on axioms: \[([^\]]*)\]',text):
        require({x.strip() for x in match.split(',') if x.strip()}<=allowed,'Unexpected axiom '+str(p))
def axiom_count(p):
    text=p.read_text();return len(re.findall(r'depends on axioms: \[',text))+text.count('does not depend on any axioms')
author_count=axiom_count(OUT/'all-author-axioms.log');review_count=axiom_count(OUT/'independent-proofs.log')
expected=json.loads((review/'final-replay/FINAL_CHECKS.json').read_text())
require(author_count==expected['author_declarations_axiom_checked'],'Author declaration count mismatch')
require(review_count==expected['reviewer_theorems_axiom_checked'],'Reviewer theorem count mismatch')
for file in [OUT/'kernel/MUTATION_RESULTS.json',OUT/'primary-mutants/RESULTS.json']:
    result=json.loads(file.read_text());require(result['status']=='PASS' and len(result['mutations'])==6,'Missing mutation rejection')
require(verify_manifest(ROOT,'PUBLIC_MANIFEST.json')==payload_count,'Packet changed during replay')
result={'status':'PASS','public_manifest_sha256':digest(ROOT/'PUBLIC_MANIFEST.json'),
        'science_manifest_sha256':digest(science/'MANIFEST.json'),'review_receipt_sha256':digest(review/'REVIEW_RECEIPT_V2.json'),
        'public_bound_files':payload_count,'science_bound_files':science_count,
        'author_declarations_axiom_checked':author_count,'independent_theorems_axiom_checked':review_count,
        'author_mutations_rejected':6,'independent_primary_mutations_rejected':6,
        'normal_and_optimized_semantic_results_match_archived_evidence':True,
        'immutable_payload_before_after':True,'successful_compiler_logs_clean':True,
        'original_external_custody_audit':'Archived independent receipt; portable replay verifies the exact bundled copies and source bindings.',
        'lean_sha256':tools['lean_sha256'],'mathlib_revision':tools['mathlib_revision'],'mathlib_source_files_verified':len(json.loads((ROOT/'MATHLIB_SOURCE_MANIFEST.json').read_text())['files'])}
(OUT/'PUBLIC_REPLAY_RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps(result,indent=2,sort_keys=True))
