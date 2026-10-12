from pathlib import Path
import os,sys,json,subprocess,hashlib
ROOT=Path('private-locator:b161f5e6ec5b32183f0f');OUT=ROOT/'constructor-square/work-accounting';sys.path.insert(0,str(ROOT/'python-bases/source'))
import reference as r
ROWS=json.loads((ROOT/'constructor-square/cross-language/CASES.json').read_text())
def ty(A):
 if A[0]=='v':return f'(TypeCode.var {A[1]})'
 if A[0]=='bottom':return 'TypeCode.bottom'
 if A[0]=='arr':return f'(TypeCode.arrow {ty(A[1])} {ty(A[2])})'
 return f'(TypeCode.all {ty(A[1])})'
def term(t):return f'(Term.app {term(t[1])} {term(t[2])})' if t[0]=='app' else f'Term.{t[0]}'
def proof(p):
 k=p['rule']
 if k in ['i','k','s']:return f'(SourceProof.{k} '+ ' '.join(ty(p[a]) for a in {'i':['A'],'k':['A','B'],'s':['A','B','C']}[k])+')'
 if k=='app':return f'(SourceProof.app {proof(p["function"])} {proof(p["argument"])})'
 if k=='all_i':return f'(SourceProof.allI {proof(p["body"])})'
 if k=='all_e':return f'(SourceProof.allE {proof(p["polymorphic"])} {ty(p["type"])})'
 return f'(SourceProof.reduce {proof(p["proof"])} ['+', '.join(term(t) for t in p['trace'])+'])'
original=r.bound_tree;events=[]
def logged(value,*args,**kw):
 work=kw.get('work');before=None if work is None else work[0]
 result=original(value,*args,**kw)
 if before is not None:events.append({'before':before,'after':work[0],'charged':before-work[0],'returned_nodes':result})
 return result
r.bound_tree=logged
records=[];checks=[]
for row in ROWS:
 if row['python_outcome']!='accept':continue
 events.clear();out=r.check(row['source'],row['depth']);assert list(out)==[tuple(out[0]),tuple(out[1])]
 cost=sum(x['charged'] for x in events);assert all(x['charged']==x['returned_nodes'] for x in events)
 records.append({'name':row['name'],'depth':row['depth'],'cost':cost,'output_validations':len(events),'remaining':events[-1]['after'],'consistent':events[0]['before']==2000000 and events[-1]['after']==2000000-cost})
 assert records[-1]['consistent']
 checks.append((row,cost,out))
(OUT/'PYTHON_WORK.json').write_text(json.dumps({'source_reference_sha256':hashlib.sha256((ROOT/'python-bases/source/reference.py').read_bytes()).hexdigest(),'instrumentation':'Transparent proxy records before/after of actual bound_tree work list; original checker and validator run unchanged','cases':records},indent=2)+'\n')
lean='private-locator:4211d241978f643cb623';env={**os.environ,'LEAN_PATH':str(ROOT/'constructor-square/fresh-build-2')};modules=[]
for start in range(0,len(checks),20):
 name=f'Work{start//20:03d}';lines=['import SourceResources','set_option maxRecDepth 200000','set_option maxHeartbeats 0','open P03Source OrthemologyV2 OrthemologyV3']
 for row,cost,(t,A) in checks[start:start+20]:lines.append(f'theorem actual_work_{row["name"]} : sourceRun {row["depth"]} {proof(row["source"])} = some (({term(t)}, {ty(A)}), {cost}) := by decide')
 p=OUT/(name+'.lean');p.write_text('\n'.join(lines)+'\n');proc=subprocess.run([lean,'-o',name+'.olean',p.name],cwd=OUT,env=env,capture_output=True,timeout=300);(OUT/(name+'.stdout')).write_bytes(proc.stdout);(OUT/(name+'.stderr')).write_bytes(proc.stderr)
 item={'module':name,'cases':len(checks[start:start+20]),'exit_code':proc.returncode,'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'olean_bytes':(OUT/(name+'.olean')).stat().st_size if (OUT/(name+'.olean')).exists() else 0};modules.append(item);print(item,flush=True)
 (OUT/'RESULT.json').write_text(json.dumps({'scope':'Instrumented actual Python successful aggregate structural work compared with modeled Lean sourceRun; finite source-mapping evidence only','cases':len(checks),'modules':modules},indent=2)+'\n')
 if proc.returncode:print(proc.stdout.decode());break
