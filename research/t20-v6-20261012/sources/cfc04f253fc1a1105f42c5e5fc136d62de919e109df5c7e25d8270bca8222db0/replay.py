#!/usr/bin/env python3
"""Relocatable, fail-closed, additive-only replay from an immutable extracted packet."""
from pathlib import Path
import argparse,datetime,hashlib,json,os,re,shutil,subprocess,sys,time
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent
ALLOWED={'propext','Classical.choice','Quot.sound'}
def need(ok,msg):
    if not ok: raise ValueError(msg)
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()
def read(p):return json.loads(p.read_text())
def dump(p,j):p.write_text(json.dumps(j,indent=2)+'\n')
def safe(s):
    p=Path(s);need(not p.is_absolute() and '..' not in p.parts,'Unsafe relative path: '+s);return p
def check(p,r):
    need(p.is_file() and not p.is_symlink(),'Missing or symlink prerequisite: '+str(p))
    need(p.stat().st_size==r.get('bytes',p.stat().st_size),'Size mismatch: '+str(p))
    need(sha(p)==r['sha256'],'SHA-256 mismatch: '+str(p))
def verify(root,pin):
    need(sha(root/'MANIFEST.json')==pin,'External manifest pin mismatch')
    rows=read(root/'MANIFEST.json')['files'];names=[r['path'] for r in rows]
    need(len(names)==len(set(names)),'Duplicate manifest paths')
    need(not any(p.is_symlink() for p in root.rglob('*')),'Symlink in immutable packet')
    actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    need(actual==set(names)|{'MANIFEST.json'},'Exact packet inventory differs')
    for r in rows:check(root/safe(r['path']),r)
    c=read(root/'REUSE_CONTRACT.json');E=root/'evidence';A=c['author_directory'];R=c['review_directory']
    for r in c['copied_originals']:check(E/safe(r['path']),r)
    freeze=read(E/A/'validation/CANDIDATE_FREEZE.json')
    for r in freeze['files']:check(E/safe(r['path']),r)
    review=read(E/R/'REVIEW_RECEIPT.json')
    need(review['status']=='PASS' and review['candidate_freeze_sha256']==sha(E/A/'validation/CANDIDATE_FREEZE.json'),'Independent acceptance binding differs')
    for r in review['files']:check(E/safe(r['path']),r)
    need(review['positive_theorem_dependency_closures_independently_audited']==50,'Independent audit scope differs')
    need(read(E/R/'REPLAY_RECEIPT.json')['status']=='PASS','Independent replay is not PASS')
    for m in c['modules']:need(sha(E/A/(m+'.lean'))==sha(E/R/(m+'.lean')),'Author/review source mismatch: '+m)
    return c

def main():
    if not __debug__:raise SystemExit('Python optimization is unsupported for preserved historical evidence.')
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--expected-manifest-sha256',required=True)
    ap.add_argument('--lean-home',type=Path);ap.add_argument('--packages-dir',type=Path);ap.add_argument('--retained-root',type=Path)
    ap.add_argument('--output-dir',type=Path,required=True);a=ap.parse_args();out=a.output_dir.resolve()
    roots={'lean_home':a.lean_home.resolve() if a.lean_home else None,'packages':a.packages_dir.resolve() if a.packages_dir else None,'retained':a.retained_root.resolve() if a.retained_root else None}
    need(not out.exists(),'Output already exists; refusing to overwrite')
    need(out!=ROOT and ROOT not in out.parents and out not in ROOT.parents,'Output must be separate from immutable packet')
    for name,p in roots.items():
        # A retained workspace may contain the additive output; no historical path may.
        if p and name!='retained':need(out!=p and p not in out.parents and out not in p.parents,'Output overlaps external prerequisites')
    c=verify(ROOT,a.expected_manifest_sha256)
    bindings=read(ROOT/'prerequisites/IMPORT_BINDINGS.json');extra=read(ROOT/'prerequisites/RETAINED_PIN_BINDINGS.json')
    all_specs=[r[k] for r in bindings if r['kind']=='retained' for k in ['source','object']]+extra
    runtime=read(ROOT/'prerequisites/RUNTIME_PINS.json');all_specs+=runtime['binaries']
    def resolve(r):return roots[r['root']]/safe(r['path'])
    for r in all_specs:
        if roots[r['root']]:
            p=resolve(r);need(out!=p and p not in out.parents and out not in p.parents,'Output overlaps a retained prerequisite')
    # Refuse an output in any original author/review or retained source/object directory.
    if roots['retained']:
        for rel in c['protected_directories']:
            p=roots['retained']/safe(rel);need(out!=p and p not in out.parents and out not in p.parents,'Output overlaps an original evidence directory')
    out.mkdir(parents=True)
    receipt={'status':'STARTED','runs':[],'packet_manifest_sha256':a.expected_manifest_sha256,'baseline_modules_rebuilt':0,'new_independent_review':False,'integration':False,'closure':False,'protected_edits':False,'upload_performed':False}
    def save():dump(out/'REPLAY_RECEIPT.json',receipt)
    try:
        if any(p is None or not p.is_dir() for p in roots.values()):
            receipt.update(status='BLOCKED_MISSING_PREREQUISITES');save();print('BLOCKED: supply all three explicit prerequisite roots; no compiler ran.');return 2
        unique={(r['root'],r['path']):r for r in all_specs}
        for r in all_specs:need(unique[(r['root'],r['path'])]['sha256']==r['sha256'],'Conflicting prerequisite identities')
        for r in unique.values():check(resolve(r),r)
        receipt['external_files_verified']=len(unique);save()
        clean=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED='0')
        for k in ['LEAN_PATH','LEAN_SYSROOT','LEAN_SRC_PATH','LD_LIBRARY_PATH','LD_PRELOAD','PYTHONPATH','PYTHONOPTIMIZE']:clean.pop(k,None)
        lean=roots['lean_home']/'bin/lean'
        ver=subprocess.check_output([str(lean),'--version'],env=clean,text=True).strip();need(ver==runtime['lean_version'],'Lean version differs')
        receipt['lean_version']=ver
        work=out/'work';fresh=work/'fresh';retained=work/'retained';logs=out/'logs';sources=work/'sources'
        for p in [fresh,retained,logs,sources]:p.mkdir(parents=True)
        # Closed search path: stage the precise non-core retained object bytes only.
        # No historical candidate object can satisfy any additive import.
        expected_objects={};expected_sources={}
        for r in bindings:
            if r['kind']=='fresh':continue
            o=r['object'];p=resolve(o)
            if o['root']!='lean_home':
                target=retained/(r['module'].replace('.','/')+'.olean');target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,target);check(target,o);p=target
            expected_objects[str(p.resolve())]=o['sha256'];expected_sources[r['module']]=r['source']['sha256']
        env=dict(clean,LEAN_PATH=str(fresh)+':'+str(retained));direct={};fresh_objects={}
        def run_module(src,m,extra_check=None):
            p=sources/(m+'.lean');shutil.copyfile(src,p);need(sha(p)==sha(src),'Source copy differs')
            dep=subprocess.run([str(lean),'--deps',str(p)],cwd=work,env=env,text=True,capture_output=True,timeout=120)
            need(dep.returncode==0,'Import discovery failed: '+m+' '+dep.stdout+dep.stderr)
            imports=[]
            for line in dep.stdout.splitlines():
                q=Path(line.strip()).resolve();known=expected_objects|fresh_objects
                need(str(q) in known and sha(q)==known[str(q)],'Unbound or stale direct import: '+str(q));imports.append({'path':str(q),'sha256':sha(q),'fresh':str(q) in fresh_objects})
            direct[m]=imports
            start=time.monotonic();cmd=[str(lean),'--trust=0','-o',str(fresh/(m+'.olean')),str(p)]
            result=subprocess.run(cmd,cwd=work,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=900)
            log=logs/(m+'.log');log.write_text(result.stdout)
            record={'module':m,'exit_code':result.returncode,'source_sha256':sha(p),'log_sha256':sha(log),'seconds':round(time.monotonic()-start,3)};receipt['runs'].append(record);save()
            need(result.returncode==0 and not any(x in result.stdout for x in ['error:','warning:','sorryAx']),'Fresh compile failed: '+m+'\n'+result.stdout)
            axioms=[sorted({s.strip() for s in block.split(',') if s.strip()}) for block in re.findall(r'depends on axioms:\s*\[([^\]]*)\]',result.stdout)]
            need(all(set(a)<=ALLOWED for a in axioms),'Unexpected theorem axiom')
            record['printed_axiom_sets']=axioms;record['object_sha256']=sha(fresh/(m+'.olean'));fresh_objects[str((fresh/(m+'.olean')).resolve())]=record['object_sha256']
            if extra_check:extra_check(result.stdout)
            print('PASS '+m,flush=True);return result.stdout
        for m in c['modules']:run_module(ROOT/'evidence'/c['author_directory']/(m+'.lean'),m)
        def independent_check(s):need('independently inspected 50 positive helper/public theorem dependency closures' in s,'Independent closure audit count differs')
        run_module(ROOT/'evidence'/c['review_directory']/'IndependentChecks.lean','IndependentChecks',independent_check)
        s=run_module(ROOT/'tools/ImportInventory.lean','ImportInventory')
        names=re.findall(r'^PRESERVE_IMPORT (.+)$',s,re.M)
        need(len(names)==len(set(names)) and names==[r['module'] for r in bindings],'Actual transitive import environment differs')
        dump(out/'DIRECT_IMPORTS.json',direct)
        for r in unique.values():check(resolve(r),r)
        for p,h in expected_objects.items():need(sha(Path(p))==h,'Staged or toolchain object changed')
        verify(ROOT,a.expected_manifest_sha256)
        receipt.update(status='PASS_CUSTODY_AND_FRESH_NARROW_REPLAY',finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),trust=0,additive_modules=10,independent_check_modules=1,import_inventory_modules=1,actual_imported_modules=len(names),retained_imported_modules=sum(r['kind']=='retained' for r in bindings),audited_positive_dependency_closures=50,external_inputs_and_packet_unchanged=True,original_source_scripts_executed=False,source_object_correspondence_rebuilt=False)
        save();print(receipt['status'],flush=True);return 0
    except BaseException as e:
        receipt.update(status='FAIL',error=str(e));save();raise
if __name__=='__main__':sys.exit(main())
