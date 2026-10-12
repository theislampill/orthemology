#!/usr/bin/env python3
"""Fresh copied-source replay; official pinned dependency caches are trusted."""
from pathlib import Path
import hashlib,json,re,os,subprocess,datetime,sys
BASE=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
OLD=BASE/'tranche2/crosswalk/evidence/action-decoder-qualification-20260930T221510Z'
NEW=BASE/'tranche3/control/lean'
M=BASE/'tranche2/toolchain/mathlib4'
L=BASE/'tranche2/toolchain/lean-4.19.0-linux/bin/lean'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
record={'status':'RUNNING','started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'modules':[]}
def save(): (OUT/'REPLAY_RESULT.json').write_text(json.dumps(record,indent=2)+'\n')
def strip(s):
    # Lean nested block comments, line comments, and strings are skipped for import/token census.
    ans=[];i=0;depth=0
    while i<len(s):
        if depth:
            if s.startswith('/-',i): depth+=1;i+=2
            elif s.startswith('-/',i): depth-=1;i+=2
            else: ans.append('\n' if s[i]=='\n' else ' ');i+=1
        elif s.startswith('/-',i): depth=1;i+=2
        elif s.startswith('--',i):
            j=s.find('\n',i);i=len(s) if j<0 else j
        elif s[i]=='"':
            i+=1
            while i<len(s):
                if s[i]=='\\': i+=2
                elif s[i]=='"': i+=1;break
                else:i+=1
            ans.append(' ')
        else:ans.append(s[i]);i+=1
    assert depth==0
    return ''.join(ans)
def imports(p):return re.findall(r'^\s*import\s+([^\n]+)',strip(p.read_text()),re.M)
auth=json.loads((OLD/'RESULT.json').read_text()); assert auth['status']=='PASS'
prior={r['module']:r for r in auth['modules']}
pins=json.loads((BASE/'tranche2/toolchain/ACQUISITION.json').read_text())
assert sha(L)==pins['lean_binary_sha256']
record['lean_sha256']=sha(L); record['lean_version']=subprocess.check_output([str(L),'--version'],text=True).strip()
record['official_cache_trust']='Installed pinned official library objects are trusted; no custom author objects used; not a source bootstrap of upstream Lean/Mathlib.'
record['packages']=[]
for row in pins['packages']:
    d=M if row['name']=='mathlib' else M/'.lake/packages'/row['name']
    rev=subprocess.check_output(['git','rev-parse','HEAD'],cwd=d,text=True).strip()
    dirty=subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=d,text=True).strip()
    assert rev==row['revision'] and not dirty,(d,rev,dirty)
    record['packages'].append({'name':row['name'],'revision':rev,'tracked_clean':True})
libs=[M/'.lake/build/lib/lean']+sorted(M.glob('.lake/packages/*/.lake/build/lib/lean'))
sources={}; order=[]; visiting=set(); official={}
def visit(mod):
    if mod in sources:return
    assert mod not in visiting,('cycle',mod)
    rel=Path(mod.replace('.','/')+'.lean')
    p=OLD/'source'/rel if mod in prior else NEW/rel
    if not p.exists():
        for repo in [M]+sorted(M.glob('.lake/packages/*')):
            q=repo/rel
            if q.exists():
                blob=subprocess.check_output(['git','show','HEAD:'+rel.as_posix()],cwd=repo)
                assert blob==q.read_bytes()
                official[mod]={'repo':str(repo.relative_to(BASE)),'source_sha256':sha(q),'git_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()}
                return
        raise AssertionError(('unowned import',mod))
    if mod in prior: assert sha(p)==prior[mod]['source_sha256']
    code=strip(p.read_text())
    assert not re.search(r'\b(sorry|admit|axiom|unsafe|native_decide)\b|debug\.skipKernelTC',code),(mod,'forbidden token')
    for lib in libs+[L.parents[1]/'lib/lean']:
        assert not(lib/rel.with_suffix('.olean')).exists(),('custom shadow in official path',mod,lib)
    visiting.add(mod)
    imps=[i for line in imports(p) for i in line.split()]
    for imp in imps:visit(imp)
    visiting.remove(mod)
    sources[mod]={'module':mod,'origin':str(p.relative_to(BASE)),'source_sha256':sha(p),'imports':imps}
    order.append(mod)
for root in (sys.argv[1:] or ['RecursivePhysicalDecoder']):visit(root)
for name in ['snapshot','build','logs']:(OUT/name).mkdir(exist_ok=True)
for mod in order:
    row=sources[mod];rel=Path(mod.replace('.','/')+'.lean');dst=OUT/'snapshot'/rel
    dst.parent.mkdir(parents=True,exist_ok=True)
    if dst.exists():assert sha(dst)==row['source_sha256']
    else:dst.write_bytes((BASE/row['origin']).read_bytes())
    assert not (OUT/'build'/rel.with_suffix('.olean')).exists(),('refuse reused custom object',mod)
(OUT/'SOURCE_MANIFEST.json').write_text(json.dumps([sources[m] for m in order],indent=2)+'\n')
(OUT/'OFFICIAL_IMPORTS.json').write_text(json.dumps(official,indent=2)+'\n')
env=dict(os.environ,LEAN_PATH=':'.join(map(str,[OUT/'build']+libs)));env.pop('LEAN_SRC_PATH',None)
(OUT/'LEAN_PATH.txt').write_text(env['LEAN_PATH']+'\n')
record['old_author_receipt_sha256']=sha(OLD/'RESULT.json');record['module_count']=len(order);save()
try:
 for mod in order:
    row=sources[mod];rel=Path(mod.replace('.','/'));src=OUT/'snapshot'/rel.with_suffix('.lean');obj=OUT/'build'/rel.with_suffix('.olean');obj.parent.mkdir(parents=True,exist_ok=True)
    cmd=[str(L),'-j1','--root='+str(OUT/'snapshot'),'-o',str(obj),str(src)]
    p=subprocess.run(cmd,env=env,cwd=M,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    log=OUT/'logs'/(mod+'.log');log.write_text(p.stdout)
    record['modules'].append({**row,'command':cmd,'exit':p.returncode,'log_sha256':sha(log),'olean_sha256':sha(obj) if obj.exists() else None});save()
    print(mod,p.returncode,flush=True)
    assert p.returncode==0 and not re.search(r'\berror:|sorryAx|declaration uses .sorry.',p.stdout),p.stdout
 for row in sources.values():assert sha(BASE/row['origin'])==row['source_sha256']
 record['status']='PASS';record['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();save()
except BaseException as e:
 record['status']='FAIL_CLOSED';record['error']=repr(e);save();raise
