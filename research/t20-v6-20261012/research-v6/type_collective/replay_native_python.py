import pathlib,json,hashlib,sqlite3,sys,importlib,platform
root=pathlib.Path(__file__).resolve().parent; ws=root.parents[1];out=root/'fresh_lean/native_python';out.mkdir(parents=True,exist_ok=True)
files={'reference.py':'398fdecf3c125f29fbbf7d242327cae0c5044440d58d5d8cdad9297b6e76ea77','boundaries.py':'86794c3b03f26421dd007e0d317930fd57fd27dc042342b56815c8ec561eb7c4','proof_export.py':'6980b13029b17602c1eb516b8cc6ffa6b750e3e226513ba4fd8b7a52fb65467b'}
for n,h in files.items():
 b=(ws/'t20-consolidation-20261011/catalogue/objects'/h[:2]/h).read_bytes()
 if hashlib.sha256(b).hexdigest()!=h:raise RuntimeError('Hash mismatch '+n)
 (out/n).write_bytes(b)
sys.path.insert(0,str(out));sys.dont_write_bytecode=True
r=importlib.import_module('reference');b=importlib.import_module('boundaries');ex=importlib.import_module('proof_export')
c=sqlite3.connect(ws/'t20-consolidation-20261011/catalogue/catalogue.sqlite3');c.row_factory=sqlite3.Row
rs=c.execute("select distinct name,sha256,object_path from locations where location like '%P03_Qualified_Native_Refinement_20260930.zip!/constructor-square/native-cross-language-final/case%.json'").fetchall()
meta=next(x for x in rs if x['name']=='CASES.json');cases=json.loads((ws/meta['object_path']).read_text());byname={x['name']:x for x in rs};results=[]
for case in cases:
 row=byname[case['name']+'.json'];raw=(ws/row['object_path']).read_bytes()
 if hashlib.sha256(raw).hexdigest()!=case['raw_sha256']:raise RuntimeError('Fixture binding mismatch')
 try:
  val=r.check_json(raw,case['depth']);actual='accept';detail=json.loads(json.dumps(val));match=actual==case['outcome'] and detail==case.get('output')
 except b.Rejection as e:
  actual='refuse';detail=str(e);match=actual==case['outcome']
 results.append({'name':case['name'],'sha256':row['sha256'],'kind':case['kind'],'duplicate_field_wire':case['duplicate_field_wire'],'depth':case['depth'],'actual':actual,'details':detail,'expected_match':match})
 if not match:raise RuntimeError('Fixture outcome mismatch '+case['name'])
p={'rule':'all_i','body':{'rule':'i','A':['v',0]}};q={'rule':'reduce','proof':p,'trace':[['i']]};costs=[];original=r.bound_tree
for proof in [p,q]:
 events=[]
 def wrapped(value,*args,**kw):
  work=kw.get('work');before=None if work is None else work[0];ret=original(value,*args,**kw)
  if before is not None:events.append(before-work[0])
  return ret
 r.bound_tree=wrapped;value=r.check(proof);r.bound_tree=original;budget=[512];cert=ex._cert(proof,budget);costs.append({'result':value,'source_work':sum(events),'export_work':512-budget[0],'certificate_text':cert})
if costs[0]['source_work']!=22 or costs[1]['source_work']!=34 or costs[0]['certificate_text']!=costs[1]['certificate_text'] or costs[0]['result']!=costs[1]['result'] or [x['export_work'] for x in costs]!=[2,3]:raise RuntimeError('Cost obstruction did not reproduce')
receipt={'scope':'Fresh actual Python replay of exact archived native-cross-language-final raw fixtures, plus concrete source erasure/work counterexample. No Python-to-Lean universal refinement theorem.','python':sys.executable,'python_version':platform.python_version(),'python_sha256':hashlib.sha256(pathlib.Path(sys.executable).read_bytes()).hexdigest(),'source_hashes':files,'fixture_cases_sha256':meta['sha256'],'cases':results,'case_count':len(results),'accepted':sum(x['actual']=='accept' for x in results),'refused':sum(x['actual']=='refuse' for x in results),'duplicate_count':sum(x['duplicate_field_wire'] for x in results),'cost_counterexample':costs,'status':'ALL_PASS'}
(out/'FRESH_PYTHON_REPLAY.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({k:receipt[k] for k in ['status','case_count','accepted','refused','duplicate_count','cost_counterexample']}))
