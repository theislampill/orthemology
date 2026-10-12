from pathlib import Path
import sys,json,hashlib,subprocess,os,itertools
ROOT=Path('private-locator:b161f5e6ec5b32183f0f');BASE=ROOT/'python-bases/source';OUT=Path(os.environ.get('P03_CROSS_OUT',str(ROOT/'constructor-square/cross-language')));OUT.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(BASE))
import reference as r
from boundaries import Rejection,dump_json

def ty(A):
 if A[0]=='v':return f'(TypeCode.var {A[1]})'
 if A[0]=='bottom':return 'TypeCode.bottom'
 if A[0]=='arr':return f'(TypeCode.arrow {ty(A[1])} {ty(A[2])})'
 return f'(TypeCode.all {ty(A[1])})'
def term(t):
 if t[0]=='app':return f'(Term.app {term(t[1])} {term(t[2])})'
 return f'Term.{t[0]}'
def proof(p):
 tag=p['rule']
 if tag in ['i','k','s']:
  fields={'i':['A'],'k':['A','B'],'s':['A','B','C']}[tag]
  return f'(SourceProof.{tag} '+ ' '.join(ty(p[k]) for k in fields)+')'
 if tag=='app':return f'(SourceProof.app {proof(p["function"])} {proof(p["argument"])})'
 if tag=='all_i':return f'(SourceProof.allI {proof(p["body"])})'
 if tag=='all_e':return f'(SourceProof.allE {proof(p["polymorphic"])} {ty(p["type"])})'
 return f'(SourceProof.reduce {proof(p["proof"])} ['+', '.join(term(t) for t in p['trace'])+'])'
V=('v',0);BOT=('bottom',);ID=('all',('arr',V,V));pid={'rule':'all_i','body':{'rule':'i','A':V}}
rows=[]
for p in sorted((ROOT/'export-probes').glob('probe*.json')):
 rows.append({'name':p.stem,'source':json.loads(p.read_text()),'depth':0,'class':'previous-positive'})
# All combinations of valid-shape but potentially ill-scoped typed constructors.
types=[BOT,V,('v',1),ID,('arr',V,BOT),('all',('v',1))]
for d,A in itertools.product([0,1,2,100,101],types):
 rows.append({'name':f'scope{len(rows)}','source':{'rule':'i','A':A},'depth':d,'class':'scope-or-depth'})
for d in [0,1,2]:
 for A,B in itertools.product(types,repeat=2):
  rows.append({'name':f'app{len(rows)}','source':{'rule':'app','function':{'rule':'i','A':A},'argument':{'rule':'i','A':B}},'depth':d,'class':'application'})
  rows.append({'name':f'elim{len(rows)}','source':{'rule':'all_e','polymorphic':{'rule':'i','A':A},'type':B},'depth':d,'class':'nonpoly'})
selfp={'rule':'app','function':{'rule':'all_e','polymorphic':pid,'type':ID},'argument':pid}
terms=[('i',),('k',),('zero',),('app',('i',),('i',))]
for n in range(4):
 for trace in itertools.product(terms,repeat=n):
  rows.append({'name':f'trace{len(rows)}','source':{'rule':'reduce','proof':selfp,'trace':trace},'depth':0,'class':'explicit-trace'})
for n in [90,95,97,98,99,100,101,110]:
 A=BOT
 for _ in range(n):A=('all',A)
 rows.append({'name':f'depth{n}','source':{'rule':'i','A':A},'depth':0,'class':'type-height'})
for n in [8,9,10,11,12]:
 A=BOT
 for _ in range(n):A=('arr',A,A)
 rows.append({'name':f'balanced{n}','source':{'rule':'i','A':A},'depth':0,'class':'intermediate-type-node-bound'})
for n in [3,4,5,6,7]:
 A=V;B=BOT
 for _ in range(n):A=('arr',A,A);B=('arr',B,B)
 rows.append({'name':f'subst{n}','source':{'rule':'all_e','polymorphic':{'rule':'all_i','body':{'rule':'i','A':A}},'type':B},'depth':0,'class':'substitution-output-bound'})
records=[];counts={'accept':0,'refuse':0};env={**os.environ,'LEAN_PATH':os.environ.get('P03_MODEL_BUILD',str(ROOT/'runtime-formal-baseline')+':'+str(ROOT/'constructor-square'))};lean='private-locator:4211d241978f643cb623'
# Small batches keep individual proof expressions independently inspectable.
for start in range(0,len(rows),24):
 batch=rows[start:start+24];name=f'Cross{start//24:03d}';lines=['import SourceResources','set_option maxRecDepth 200000','set_option maxHeartbeats 0','open P03Source OrthemologyV2 OrthemologyV3']
 for row in batch:
  p=row['source'];d=row['depth']
  try:t,A=r.check(p,d);expected=f'some ({term(t)}, {ty(A)})';row['python_outcome']='accept';row['python_output']=[t,A]
  except Rejection as ex:expected='none';row['python_outcome']='refuse';row['python_refusal']=str(ex)
  counts[row['python_outcome']]+=1
  lines.append(f'-- {row["name"]}: {row["class"]}; Python {row["python_outcome"]}')
  lines.append(f'theorem source_{row["name"]}_matches : sourceCheck {d} {proof(p)} = {expected} := by decide')
 path=OUT/(name+'.lean');path.write_text('\n'.join(lines)+'\n')
 proc=subprocess.run([lean,'-o',name+'.olean',path.name],cwd=OUT,env=env,capture_output=True,timeout=300)
 (OUT/(name+'.stdout')).write_bytes(proc.stdout);(OUT/(name+'.stderr')).write_bytes(proc.stderr)
 record={'module':name,'cases':len(batch),'exit_code':proc.returncode,'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'olean_bytes':(OUT/(name+'.olean')).stat().st_size if (OUT/(name+'.olean')).exists() else 0};records.append(record)
 (OUT/'CASES.json').write_text(json.dumps(rows,indent=2)+'\n')
 (OUT/'RESULT.json').write_text(json.dumps({'cases':len(rows),'counts_run':counts,'modules':records,'native_lean':lean,'model_build_path':env['LEAN_PATH'],'source_identities':{x:hashlib.sha256((ROOT/'constructor-square'/x).read_bytes()).hexdigest() for x in ['SourceTypeOps.lean','SourceHeadStep.lean','SourceChecker.lean','SourceCheckerProofs.lean','SourceResources.lean']},'scope':'Kernel-decided modeled source-AST acceptance/output/refusal agrees with separately executed Python on these exact finite cases; does not prove Python interpreter refinement'},indent=2)+'\n')
 print(record,flush=True)
 if proc.returncode:print(proc.stdout.decode());print(proc.stderr.decode());break
