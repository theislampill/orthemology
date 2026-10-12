#!/usr/bin/env python3
"""Bounded, portable finite-control replay. No analytic or Lean proof is inferred."""
from pathlib import Path, PurePosixPath
import argparse, hashlib, json, os, platform, shutil, subprocess, sys, time
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parent
A='partial-cumulative-one-hidden-lift-20261010'; AR='partial-cumulative-one-hidden-lift-review-20261010'
B='partial-cumulative-law-persistence-20261010'; BR='review-joint-law-persistence-20261010'
C='valid-initial-partial-escape-20261010'; CR='valid-initial-partial-escape-independent-review-20261010'
def require(v,msg):
    if not v:raise RuntimeError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def dump(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n')
def safe(base,rel):
    q=PurePosixPath(rel)
    require(not q.is_absolute() and '..' not in q.parts and str(q)==rel,'unsafe relative path: '+rel)
    p=base/rel
    require(not any(v.is_symlink() for v in [p,*list(p.parents)[:len(q.parts)]]),'symlink path: '+rel)
    require(p.resolve().is_relative_to(base.resolve()),'path escapes root')
    return p

def integrity(expected):
    require(sha(ROOT/'MANIFEST.json')==expected,'manifest digest does not match supplied binding')
    manifest=read(ROOT/'MANIFEST.json'); rows=manifest['files']
    paths=[r['path'] for r in rows]
    require(len(paths)==len(set(paths)),'duplicate manifest paths')
    actual=[str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file() and p != ROOT/'MANIFEST.json']
    require(not any(p.is_symlink() for p in ROOT.rglob('*')),'packet contains symlink')
    require(set(actual)==set(paths),'packet file set differs from manifest')
    for row in rows:
        p=safe(ROOT,row['path'])
        require(p.is_file() and p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'packet hash/size mismatch: '+row['path'])
    for row in read(ROOT/'COPY_MANIFEST.json')['copies']:
        p=safe(ROOT,row['copy']);require(sha(p)==row['sha256'] and p.stat().st_size==row['bytes'],'copy binding mismatch')
    aliases=read(ROOT/'SOURCE_ROOT_BINDINGS.json')['files']
    for old,row in aliases.items():
        safe(ROOT,old);p=safe(ROOT,row['packet'])
        require(sha(p)==row['sha256'] and p.stat().st_size==row['bytes'],'source alias mismatch')
    acc=read(ROOT/'ACCEPTANCE_BINDINGS.json')
    require(acc['T20']=='ACTIVE' and acc['intermediate_only'] is True and acc['closure'] is False and acc['integration'] is False and acc['analytic_kernel_proof'] is False and isinstance(acc['effectivity_addendum_included'],bool),'unsupported scope escalation')
    frozen=0
    for d,label in [(A,'one_hidden'),(C,'escape')]:
        mf=ROOT/'evidence'/d/'FROZEN_MANIFEST.json'
        require(sha(mf)==acc[label]['manifest_sha256'],'author manifest acceptance mismatch')
        for row in read(mf)['files']:
            p=safe(mf.parent,row['path'])
            require(sha(p)==row['sha256'],'frozen author mismatch')
            if 'bytes' in row:require(p.stat().st_size==row['bytes'],'frozen byte count mismatch')
            frozen+=1
        for row in read(mf.parent/'INPUT_BINDINGS.json')['files']:
            require(aliases[row['original']]['sha256']==row['sha256'],'author input alias mismatch')
            if row.get('copy'):require(sha(safe(mf.parent,row['copy']))==row['sha256'],'author input-copy mismatch')
    r=read(ROOT/'evidence'/AR/'REVIEW_RECEIPT.json')
    require(r['status']==acc['one_hidden']['status'] and r['author_freeze_explicitly_confirmed'] is True and r['blocking_findings']==[] and r['frozen_files_verified_before_and_after']==15,'one-hidden review verdict mismatch')
    require(r['reviewed_author_manifest_sha256']==acc['one_hidden']['manifest_sha256'],'review-author binding mismatch')
    require(r['independent_replay']['exit_code']==0 and r['independent_replay']['passed']==615 and r['independent_replay']['check_records_match_author'] is True,'one-hidden replay acceptance mismatch')
    for p,h in r['artifacts'].items():
        rel='replay/CONTROL_RESULTS.json' if p=='CONTROL_RESULTS.json' else p
        require(sha(ROOT/'evidence'/AR/rel)==h,'one-hidden review artifact mismatch')
    v=read(ROOT/'evidence'/AR/'VERIFIED_AUTHOR_MANIFEST.json')
    require(v['all_manifest_entries_verified'] is True and v['manifest_sha256']==acc['one_hidden']['manifest_sha256'] and v['file_count']==15,'author-verification record mismatch')
    r=read(ROOT/'evidence'/CR/'REVIEW_RECEIPT.json')
    require(r['status']==acc['escape']['status'] and r['mathematical_blockers']==[] and r['frozen_files_verified']==19 and r['bound_source_pairs_verified']==12,'escape review verdict mismatch')
    require(r['target_manifest_sha256']==acc['escape']['manifest_sha256'] and r['target_result_sha256']==sha(ROOT/'evidence'/C/'RESULT.md'),'escape acceptance binding mismatch')
    require(r['author_isolated_replay_assertions']==7888 and r['independently_authored_exact_assertions']==16597 and r['distinct_mutation_variants_rejected']==8,'escape review counts mismatch')
    for row in r['review_files']:require(sha(ROOT/'evidence'/CR/row['path'])==row['sha256'],'escape review artifact mismatch')
    p=acc['persistence']
    require(sha(ROOT/p['result'])==p['sha256'] and sha(ROOT/p['review'])==p['review_sha256'],'persistence review binding mismatch')
    pc=read(ROOT/p['controls'])
    require(pc['passed']==24 and pc['failed']==0 and len(pc['checks'])==24,'persistence receipt mismatch')
    for rel,h in pc['source_bindings'].items():require(aliases[rel]['sha256']==h,'persistence source mismatch')
    # Separate historical object bindings, not a claim that three builds share bytes.
    inherited=read(ROOT/'INHERITED_DEPENDENCIES.json'); s=inherited['scalar_object_receipt_bindings']
    require(s['historical_receipt_object_mismatch'] is False and s['source_freeze_drift_detected'] is False and s['historical_objects_used_as_imports'] is False,'incorrect scalar provenance status')
    require(len(s['bindings'])==3 and len(set(r['object_path'] for r in s['bindings']))==3,'scalar objects conflated')
    for row in s['bindings']:require(row['match'] is True and row['expected_sha256']==row['actual_sha256'],'scalar boolean and digest disagree')
    for row in inherited['companions']:
        require(row['needed_for_this_finite_replay'] is False,'companion scope mismatch')
    added=verify_addenda(aliases,acc)
    return {'addenda':added,'payload_files':len(rows),'copied_original_files':len(read(ROOT/'COPY_MANIFEST.json')['copies']),'author_frozen_files':frozen,'source_aliases':len(aliases),'separate_scalar_bindings':3}

def verify_addenda(aliases,acc):
    if not (ROOT/'ADDENDA_BINDINGS.json').is_file():
        require(acc['effectivity_addendum_included'] is False,'effectivity claimed without addendum')
        return []
    spec=read(ROOT/'ADDENDA_BINDINGS.json')
    require(spec['status']=='ACCEPTED_ORDINARY_ADDENDA' and spec['analytic_kernel_proof'] is False and spec['closure'] is False,'addendum scope escalation')
    require(acc['effectivity_addendum_included']==('effectivity' in spec['names']),'effectivity scope flag mismatch')
    for row in spec['targets']:
        require(sha(safe(ROOT,row['path']))==row['sha256'],'addendum target binding mismatch')
    for row in spec['manifests']:
        m=read(ROOT/row['path']); entries=m['files']
        if isinstance(entries,dict):entries=[{'path':k,'sha256':v} for k,v in entries.items()]
        for ent in entries:
            if row['base']=='source-aliases':h=aliases[ent['path']]['sha256']
            else:h=sha(safe(ROOT/row['base'],ent['path']))
            require(h==ent['sha256'],'addendum frozen manifest mismatch: '+ent['path'])
    for row in spec['receipt_checks']:
        r=read(ROOT/row['path'])
        for pointer,value in row['equals'].items():
            actual=r
            for part in pointer.split('/'):
                actual=actual[int(part)] if isinstance(actual,list) else actual[part]
            require(type(actual)==type(value) and actual==value,'addendum receipt condition mismatch: '+pointer)
    for prog in spec['programs']:
        for row in prog.get('overrides',[]):require(sha(ROOT/row['packet'])==row['sha256'],'pinned historical preimage mismatch')
    return spec['names']

def run_addenda(out,source,env):
    if not (ROOT/'ADDENDA_BINDINGS.json').is_file():return []
    spec=read(ROOT/'ADDENDA_BINDINGS.json');runs=[]
    for prog in spec['programs']:
        workspace=out/'addenda-runs'/prog['name'];shutil.copytree(source,workspace)
        for tree in prog['trees']:
            shutil.copytree(ROOT/'evidence'/tree,workspace/tree,dirs_exist_ok=True)
        for row in prog.get('overrides',[]):
            dst=safe(workspace,row['relative']);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/row['packet'],dst)
            require(sha(dst)==row['sha256'],'pinned-input copy failed')
        for row in prog['results']:
            file=workspace/row['relative']
            if file.exists():file.unlink()
        script=workspace/prog['script'];log=out/'logs'/(prog['name']+'.log')
        start=time.monotonic()
        with log.open('w') as stream:p=subprocess.run([sys.executable,'-B',str(script)],cwd=workspace,env=env,stdout=stream,stderr=subprocess.STDOUT)
        require(p.returncode==0,'addendum control failed: '+prog['name'])
        outputs=[]
        for row in prog['results']:
            file=workspace/row['relative'];require(file.is_file(),'missing fresh addendum result')
            got=read(file);old=read(ROOT/row['historical'])
            for doc in [got,old]:
                require(doc['status'] in ['PASS','passed'],'addendum result not passed')
                for key,value in row.get('equals',{}).items():require(doc[key]==value,'addendum result property mismatch')
                for key,value in row.get('lengths',{}).items():require(len(doc[key])==value,'addendum result count mismatch')
                for key in ['timestamp_utc','elapsed_seconds','python','sympy','sympy_version']:doc.pop(key,None)
            require(got==old,'exact addendum mathematical result mismatch: '+row['relative'])
            outputs.append({'result':str(file.relative_to(out)),'sha256':sha(file),'mathematical_records_match':True,'expected_properties':row.get('equals',{}),'expected_family_counts':row.get('lengths',{})})
        runs.append({'name':prog['name'],'exit_code':0,'script_sha256':sha(script),'script_unmodified':sha(script)==sha(ROOT/'evidence'/prog['script']),'pinned_input_overrides':prog.get('overrides',[]),'outputs':outputs,'log':str(log.relative_to(out)),'log_sha256':sha(log),'seconds':round(time.monotonic()-start,3)})
        require(runs[-1]['script_unmodified'] is True,'addendum script changed')
        print(prog['name']+': PASS',flush=True)
    return runs

def compare_result(current, historical, kind):
    got=read(current); old=read(historical)
    for v in [got,old]:
        if kind=='checks':
            require(v['status']=='PASS' and v['check_count']==len(v['checks']) and all(c['passed'] is True for c in v['checks']),'failed or miscounted check')
        elif kind=='persistence':require(v['failed']==0 and v['passed']==len(v['checks']),'persistence check failure')
        else:require(v['status']=='PASS' and v['assertions']==sum(v['groups'].values()) and len(v['mutations'])==8,'independent check failure')
    # Timestamps and interpreter patch versions are environment provenance, not mathematical results.
    for v in [got,old]:
        for k in ['timestamp_utc','python','sympy','sympy_version']:v.pop(k,None)
    require(got==old,'replayed exact mathematical records differ from retained results')
    return got.get('check_count',got.get('passed',got.get('assertions')))

def main():
    require(sys.flags.optimize==0,'optimized Python disables inherited assertions; refused')
    ap=argparse.ArgumentParser();ap.add_argument('--manifest-sha256',required=True);ap.add_argument('--out');ap.add_argument('--verify-only',action='store_true');args=ap.parse_args()
    checked=integrity(args.manifest_sha256)
    if args.verify_only:print(json.dumps({'status':'PASS_INTEGRITY_ONLY',**checked}));return
    require(args.out is not None,'--out is required for replay')
    out=Path(args.out).resolve()
    require(not out.is_relative_to(ROOT) and not ROOT.is_relative_to(out),'output overlaps packet')
    require(not out.exists(),'output must not already exist')
    require(sys.version_info[:2]==(3,12),'Python 3.12.x is the tested external prerequisite')
    import sympy
    require(sympy.__version__=='1.14.0','SymPy 1.14.0 is required')
    out.mkdir(parents=True); source=out/'source-root';source.mkdir()
    for original,row in read(ROOT/'SOURCE_ROOT_BINDINGS.json')['files'].items():
        dst=safe(source,original);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/row['packet'],dst)
    runs=[]
    env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1';env['LIFT_SOURCE_ROOT']=str(source);env['ESCAPE_SOURCE_ROOT']=str(source)
    for name,d,script,result,kind,count in [
        ('one_hidden_author',A,'check_controls.py','CONTROL_RESULTS.json','checks',615),
        ('law_persistence_review',BR,'check_controls.py','CONTROL_RESULTS.json','persistence',24),
        ('valid_initial_author',C,'check_controls.py','CONTROL_RESULTS.json','checks',7888),
        ('valid_initial_independent',CR,'independent_controls.py','INDEPENDENT_RESULTS.json','independent',16597)]:
        dest=out/'runs'/d;shutil.copytree(ROOT/'evidence'/d,dest)
        file=dest/script;original_hash=sha(file);patch=None
        if d==BR:
            old="ROOT = Path('private-locator:8f24556a330b05a11a95')"
            new='ROOT = Path('+repr(str(source))+')'
            text=file.read_text();require(text.count(old)==1,'unexpected original path-relocation target')
            file.write_text(text.replace(old,new))
            patch={'old':old,'new':new,'occurrences':1,'scope':'Only source-root relocation in this working copy; no arithmetic edit.'}
        (dest/result).unlink() # Never accept a stale archived result after a failed/no-op run.
        log=out/'logs'/f'{name}.log';log.parent.mkdir(exist_ok=True)
        started=time.monotonic()
        with log.open('w') as f:process=subprocess.run([sys.executable,'-B',str(file)],cwd=out,env=env,stdout=f,stderr=subprocess.STDOUT)
        require(process.returncode==0,'control process failed: '+name)
        require((dest/result).is_file(),'control process produced no fresh result')
        got=compare_result(dest/result,ROOT/'evidence'/d/result,kind);require(got==count,'unexpected replay count')
        runs.append({'name':name,'exit_code':process.returncode,'count':got,'mathematical_records_match':True,'script_original_sha256':original_hash,'executed_script_sha256':sha(file),'path_relocation':patch,'result':str((dest/result).relative_to(out)),'result_sha256':sha(dest/result),'log':str(log.relative_to(out)),'log_sha256':sha(log),'seconds':round(time.monotonic()-started,3)})
        print(name+': '+str(got)+' PASS',flush=True)
    added_runs=run_addenda(out,source,env)
    require(integrity(args.manifest_sha256)==checked,'packet changed during replay')
    for original,row in read(ROOT/'SOURCE_ROOT_BINDINGS.json')['files'].items():require(sha(source/original)==row['sha256'],'replay source alias changed')
    receipt={'status':'PASS_FRESH_PARTIAL_LAW_FINITE_REPLAY','utc':datetime.now(timezone.utc).isoformat(),'manifest_sha256':args.manifest_sha256,'python':platform.python_version(),'sympy':sympy.__version__,'integrity':checked,'runs':runs,'addenda_runs':added_runs,'packet_unchanged':True,'source_aliases_unchanged':True,'T20':'ACTIVE','analytic_kernel_proof':False,'Lean_rebuilt':False,'integration':False,'closure':False,'scope':'Exact finite identities and mutation controls only. Universal analytic claims rest on preserved ordinary proofs and reviews; inherited Lean algebra is companion evidence.'}
    dump(out/'REPLAY_RECEIPT.json',receipt)
    print('PASS: all configured finite-control suites; T20 remains ACTIVE.')
if __name__=='__main__':
    try:main()
    except Exception as e:print('REFUSED: '+str(e),file=sys.stderr);sys.exit(1)
