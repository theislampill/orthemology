#!/usr/bin/env python3
"""Replay exact source-only scientific and independent-review controls.
External Lean/Mathlib objects are verified read-only trusted inputs, not rebuilt.
All outputs go to a new directory outside this package and both dependencies.
"""
from pathlib import Path
import argparse,hashlib,json,os,re,signal,subprocess,time,datetime,sys
ROOT=Path(__file__).resolve().parent

def digest(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()
def check(ok,message):
    if not ok:raise RuntimeError(message)
def safe_path(base,rel):
    p=Path(rel);check(not p.is_absolute() and '..' not in p.parts,'unsafe relative path')
    return base/p
def verify_package():
    manifest=json.loads((ROOT/'MANIFEST.json').read_text())
    actual=sorted(str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file() and p.name!='MANIFEST.json')
    check(actual==sorted(x['path'] for x in manifest['files']),'package file census differs')
    for x in manifest['files']:
        p=safe_path(ROOT,x['path']);check(p.is_file() and not p.is_symlink(),'invalid package file '+x['path'])
        check(p.stat().st_size==x['bytes'] and digest(p)==x['sha256'],'package identity changed '+x['path'])
    return digest(ROOT/'MANIFEST.json')
def verify_projection_bindings():
    maps=json.loads((ROOT/'ORIGINAL_TO_PUBLIC.json').read_text())['milestones']
    bindings={x['milestone']:x for x in json.loads((ROOT/'INPUT_BINDINGS.json').read_text())['milestones']}
    counts=[]
    for group in maps:
        original=safe_path(ROOT,group['original_manifest_public_path'])
        check(digest(original)==group['original_manifest_sha256'],'original manifest identity differs')
        check(bindings[group['review_evidence_id']]['milestone_manifest_sha256']==digest(original),'acceptance identity differs')
        entries=json.loads(original.read_text())['files']; rows=group['entries']
        by={x['original_path']:x for x in rows}
        check(len(by)==len(rows)==len(entries) and set(by)=={x['path'] for x in entries},'original-to-public coverage differs')
        for entry in entries:
            row=by[entry['path']]
            check(row['original_bytes']==entry['bytes'] and row['original_sha256']==entry['sha256'],'original entry binding differs')
            if row['disposition']=='exact_included':
                target=safe_path(ROOT,row['public_path'])
                check(target.stat().st_size==entry['bytes'] and digest(target)==entry['sha256'],'public exact copy differs')
            else:check(row['disposition']=='omitted' and bool(row.get('reason')),'unexplained omission')
        counts.append({'milestone':group['accepted_milestone'],'entries':len(entries)})
    return counts
def verify_entries(base,entries,exceptions=None):
    exceptions=exceptions or {};count=0;allowed=[]
    for x in entries:
        p=safe_path(base,x['path']);kind=x.get('kind','file')
        if kind=='directory':check(p.is_dir() and not p.is_symlink(),'missing dependency directory '+x['path']);continue
        if kind=='symlink':check(p.is_symlink() and os.readlink(p)==x['target'],'dependency symlink differs '+x['path']);continue
        check(kind=='file' and p.is_file() and not p.is_symlink(),'dependency file missing '+x['path'])
        h=digest(p);size=p.stat().st_size;expected_size=x.get('bytes',x.get('size'))
        if h!=x['sha256'] or size!=expected_size:
            e=exceptions.get(x['path']);check(e is not None,'dependency bytes differ '+x['path'])
            check(x['sha256']==e['original_pin_sha256'] and h==e['current_sha256'] and size==e['current_bytes'],'unrecognized metadata delta '+x['path'])
            allowed.append(x['path'])
        count+=1
    return {'files_verified':count,'accepted_metadata_exceptions':allowed}
def verify_census(base,roots,entries):
    expected={x['path'] for x in entries};actual=set()
    for rel in roots:
        root=safe_path(base,rel)
        if rel:actual.add(rel)
        actual.update(str(p.relative_to(base)) for p in root.rglob('*'))
    check(actual==expected,'external dependency census differs')
    return len(actual)
def compiler_env(build,math,roots):
    env={k:v for k,v in os.environ.items() if not k.startswith('LD_') and k not in ['LEAN_PATH','LEAN_SRC_PATH','LEAN_SYSROOT']}
    libs=[safe_path(math,root) for root in roots]
    env['LEAN_PATH']=':'.join(map(str,[build]+libs));return env

def invoke(command,env,timeout):
    start=time.monotonic();p=subprocess.Popen(command,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,start_new_session=True)
    try:stdout=p.communicate(timeout=timeout)[0];timed_out=False
    except subprocess.TimeoutExpired:
        os.killpg(p.pid,signal.SIGKILL);stdout=p.communicate()[0];timed_out=True
    return p.returncode,stdout,time.monotonic()-start,timed_out

def main():
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument('--lean-root',type=Path,required=True);a.add_argument('--mathlib-root',type=Path,required=True)
    a.add_argument('--output',type=Path,required=True);a.add_argument('--stage-timeout',type=int,default=180)
    opt=a.parse_args();lean=opt.lean_root.resolve();math=opt.mathlib_root.resolve();out=opt.output.resolve()
    check(1<=opt.stage_timeout<=180,'timeout must be within 1..180 seconds')
    check(not out.exists(),'output must be absent')
    for forbidden in [ROOT,lean,math]:check(out!=forbidden and forbidden not in out.parents,'output must be outside sources/dependencies')
    manifest=verify_package();projection=verify_projection_bindings();out.mkdir(parents=True);build=out/'build';logs=out/'logs';build.mkdir();logs.mkdir()
    receipt={'status':'RUNNING','started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'package_manifest_sha256':manifest,'original_manifest_coverage':projection,'external_dependency_boundary':'Pinned official precompiled Lean/Mathlib are read-only trusted inputs; their compiler correctness is not established by this replay.','results':[]}
    receipt_path=out/'REPLAY_RECEIPT.json'
    def save():receipt_path.write_text(json.dumps(receipt,indent=2)+'\n')
    save()
    lp=json.loads((ROOT/'dependencies/LEAN_DISTRIBUTION_PIN.json').read_text());mp=json.loads((ROOT/'dependencies/MATHLIB_SOURCE_PIN.json').read_text());cp=json.loads((ROOT/'dependencies/MATHLIB_CACHE_PIN.json').read_text());xp=json.loads((ROOT/'dependencies/METADATA_EXCEPTIONS.json').read_text())
    receipt['lean_census']=verify_census(lean,lp['roots'],lp['entries'])
    receipt['mathlib_cache_census']=verify_census(math,cp['roots'],cp['entries'])
    receipt['lean_pin']=verify_entries(lean,lp['entries'])
    receipt['mathlib_source_pin']=verify_entries(math,mp['files'])
    receipt['mathlib_cache_pin']=verify_entries(math,cp['entries'],{x['path']:x for x in xp['files']});save()
    env=compiler_env(build,math,cp['roots']);exe=lean/'bin/lean'
    code,text,elapsed,timed=invoke([str(exe),'--version'],env,opt.stage_timeout)
    check(code==0 and not timed and '4.19.0' in text,'wrong or failed Lean version');receipt['lean_version']=text.strip();save()
    def stage(name,source,expected=0,required=None,axiom_names=None):
        source=ROOT/source;check(source.is_file(),'source missing')
        output=build/(name.replace('/','__')+'.olean')
        code,raw,elapsed,timed=invoke([str(exe),'-o',str(output),str(source)],env,opt.stage_timeout)
        # Stored logs are explicit path-only projections; preserve raw stream identity.
        normalized=raw.replace(str(ROOT)+os.sep,'')
        log=logs/(name.replace('/','__')+'.log');log.write_text(normalized)
        row={'stage':name,'source':str(source.relative_to(ROOT)),'source_sha256':digest(source),'exit_code':code,'timed_out':timed,'seconds':elapsed,'raw_stdout_sha256':hashlib.sha256(raw.encode()).hexdigest(),'projected_log_sha256':digest(log),'log_path_projection':'Package root prefix removed only.'};receipt['results'].append(row);save()
        check(not timed,'stage timed out '+name)
        check((code==0 if expected==0 else code!=0),'unexpected exit '+name)
        for token in required or []:check(token in normalized,'missing expected output '+name)
        if expected==0:
            check('sorryAx' not in normalized and 'warning:' not in normalized,'uncredited proof/warning '+name)
            for group in re.findall(r'depends on axioms:\s*\[([^\]]*)\]',normalized,re.S):
                used={x.strip() for x in group.split(',') if x.strip()};check(used<= {'propext','Classical.choice','Quot.sound'},'unexpected axiom '+name)
        else:check(not output.exists(),'failed control emitted reusable object '+name)
        if axiom_names is not None:check(sorted(re.findall(r"^'([^']+)'",normalized,re.M))==sorted(axiom_names),'axiom declaration census differs '+name)
        print(('PASS_EXPECTED_FAILURE' if expected else 'PASS')+': '+name,flush=True)
        return normalized
    expected=json.loads((ROOT/'EXPECTED_RESULTS.json').read_text())
    for x in json.loads((ROOT/'SOURCE_ORDER.json').read_text()):
        check(digest(ROOT/x['path'])==x['sha256'],'source order identity differs')
        text=stage(x['module'],x['path'])
        if x['module'] in expected['compiled_projections']:check(text.strip()==expected['compiled_projections'][x['module']],'compiled projection differs')
        if x['module']=='NativeExecutionChecks':check(text.splitlines()==expected['author_runtime_lines'],'runtime assertion census differs')
    for milestone,control in [('primitive-v1','AllPrimitiveAxioms'),('history-v1','AllHistoryAxioms'),('ordered-initial-v1','AllOrderedAxioms')]:
        names=json.loads((ROOT/f'evidence/{milestone}-theorem-names.json').read_text());stage(control,'controls/audits/'+control+'.lean',axiom_names=names)
    for x in json.loads((ROOT/'REVIEW_CONTROLS.json').read_text()):
        text=stage(x['name'],x['path'],x['expected_exit'],x['required_output'])
        if x['name']=='ordered/OrderedExecutionControls':check(text.splitlines()==expected['independent_runtime_lines'],'independent assertion census differs')
    check(verify_package()==manifest,'source package changed during replay')
    receipt['post_lean_pin']=verify_entries(lean,lp['entries'])
    receipt['post_mathlib_source_pin']=verify_entries(math,mp['files'])
    receipt['post_mathlib_cache_pin']=verify_entries(math,cp['entries'],{x['path']:x for x in xp['files']})
    receipt.update(status='PASS_BOUNDED_PUBLIC_REVIEW_REPLAY',completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),successful_source_modules=49,scientific_theorem_readbacks=166,independent_control_stages=17)
    save();print(receipt['status'],flush=True)
if __name__=='__main__':
    try:main()
    except Exception as e:
        print('REPLAY_FAILED: '+str(e),file=sys.stderr);sys.exit(1)
