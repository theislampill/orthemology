from pathlib import Path
from dataclasses import dataclass
import sys,os,json,itertools,subprocess,hashlib
ROOT=Path('private-locator:b161f5e6ec5b32183f0f');OUT=Path(os.environ.get('NATIVE_CROSS_OUT',str(ROOT/'constructor-square/native-cross-language')));OUT.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(ROOT/'python-bases/source'))
import reference as r
from boundaries import Rejection
@dataclass
class Fields:
 rows:list

def dump(value):
 if isinstance(value,Fields):return '{'+','.join(json.dumps(k)+':'+dump(v) for k,v in value.rows)+'}'
 if type(value)is dict:return dump(Fields(list(value.items())))
 if type(value)in(list,tuple):return '['+','.join(dump(v) for v in value)+']'
 return json.dumps(value,ensure_ascii=True,separators=(',',':'))
def wire(v):
 if isinstance(v,Fields):return '(WireValue.object ['+', '.join('('+json.dumps(k)+', '+wire(x)+')' for k,x in v.rows)+'])'
 if type(v)is dict:return wire(Fields(list(v.items())))
 if type(v)in(list,tuple):return '(WireValue.array ['+', '.join(wire(x) for x in v)+'])'
 if type(v)is str:return '(WireValue.text '+json.dumps(v)+')'
 if type(v)is bool:return '(WireValue.boolean '+('true' if v else 'false')+')'
 if v is None:return 'WireValue.null'
 if type(v)is int:return f'(WireValue.natural {v})' if v>=0 else f'(WireValue.negative {-v-1})'
 raise TypeError(type(v))
def ty(A):
 if A[0]=='v':return f'(TypeCode.var {A[1]})'
 if A[0]=='bottom':return 'TypeCode.bottom'
 if A[0]=='arr':return f'(TypeCode.arrow {ty(A[1])} {ty(A[2])})'
 return f'(TypeCode.all {ty(A[1])})'
def term(t):return f'(Term.app {term(t[1])} {term(t[2])})' if t[0]=='app' else f'Term.{t[0]}'
V=('v',0);BOT=('bottom',);ID=('all',('arr',V,V));pid={'rule':'all_i','body':{'rule':'i','A':V}};selfp={'rule':'app','function':{'rule':'all_e','polymorphic':pid,'type':ID},'argument':pid}
base=[{'rule':'i','A':BOT},{'rule':'k','A':BOT,'B':BOT},{'rule':'s','A':BOT,'B':BOT,'C':BOT},selfp,pid,{'rule':'all_e','polymorphic':pid,'type':BOT},{'rule':'reduce','proof':selfp,'trace':[['app',['i'],['i']],['i']]}]
rows=[]
def add(kind,value,duplicates=False,depth=0):rows.append({'name':f'case{len(rows)}','kind':kind,'value':value,'duplicates':duplicates,'depth':depth})
for p in base:
 fields=list(p.items())
 for order in itertools.permutations(fields):add('field-order',Fields(list(order)))
 for pos,(k,v) in enumerate(fields):
  add('missing-field',Fields(fields[:pos]+fields[pos+1:]))
  add('duplicate-same',Fields(fields+[(k,v)]),True)
  add('duplicate-conflicting',Fields(fields+[(k,None)]),True)
 add('extra-field',Fields(fields+[('trusted',True)]))
 for wrong in [None,True,0,'bogus']:
  add('wrong-rule-type-or-name',Fields([(k,wrong if k=='rule' else v) for k,v in fields]))
for A in [None,False,-1,0,'bottom',[],['bottom',0],['v'],['v',-1],['v',True],['v',0,0],['v',2**256],['arr',BOT],['arr',BOT,0],['all'],['all',None],['universe']]:add('malformed-type',{'rule':'i','A':A},depth=1)
for trace in [None,0,{},[],[['k']],[['app',['i'],['i']]],[['app',['i'],['i']],['k']],[['app',['i'],['i']],['i']],[['unknown']],[['i',0]],['i']]:add('trace-shape-or-content',{'rule':'reduce','proof':selfp,'trace':trace})
for root in [None,True,0,[],['i'],'proof'] :add('wrong-root-shape',root)
for child in [None,True,0,{},[],{'rule':'i','A':BOT,'extra':0}]:add('malformed-child',{'rule':'all_i','body':child})
# Nested duplicate fields must not be lost by constructing a Python dictionary.
add('nested-duplicate',{'rule':'all_i','body':Fields([('rule','i'),('A',V),('A',V)])},True)
records=[];outcomes=[];env={**os.environ,'LEAN_PATH':str(ROOT/'constructor-square/fresh-build-3')};lean='private-locator:4211d241978f643cb623'
TAC='''  simp only [nativeCheck, decodeNativeProof, wireShape, wireNodes, wireHeight, wireIntegersFit,
    List.map, List.foldl, List.all]
  decide'''
for start in range(0,len(rows),20):
 batch=rows[start:start+20];name=f'NativeCross{start//20:03d}';lines=['import NativeCheckerBridge','set_option maxRecDepth 200000','set_option maxHeartbeats 0','open P03Source OrthemologyV2 OrthemologyV3']
 for row in batch:
  raw=dump(row['value']).encode();(OUT/(row['name']+'.json')).write_bytes(raw)
  try:t,A=r.check_json(raw,row['depth']);expected=f'some ({term(t)}, {ty(A)})';outcome='accept';extra={'output':[t,A]}
  except Rejection as ex:expected='none';outcome='refuse';extra={'reason':str(ex)}
  if not row['duplicates']:
   try:nt,nA=r.check(json.loads(raw),row['depth']);assert outcome=='accept' and (nt,nA)==(t,A)
   except Rejection:assert outcome=='refuse'
  elif outcome!='refuse':raise AssertionError('Strict JSON accepted a duplicate')
  outcomes.append({'name':row['name'],'kind':row['kind'],'duplicate_field_wire':row['duplicates'],'depth':row['depth'],'outcome':outcome,'raw_sha256':hashlib.sha256(raw).hexdigest(),**extra})
  lines.append(f'theorem {row["name"]}_matches : nativeCheck {row["depth"]} {wire(row["value"])} = {expected} := by\n{TAC}')
 path=OUT/(name+'.lean');path.write_text('\n'.join(lines)+'\n');proc=subprocess.run([lean,'-o',name+'.olean',path.name],cwd=OUT,env=env,capture_output=True,timeout=300);(OUT/(name+'.stdout')).write_bytes(proc.stdout);(OUT/(name+'.stderr')).write_bytes(proc.stderr)
 item={'module':name,'cases':len(batch),'exit_code':proc.returncode,'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'olean_bytes':(OUT/(name+'.olean')).stat().st_size if (OUT/(name+'.olean')).exists() else 0};records.append(item);print(item,flush=True)
 (OUT/'CASES.json').write_text(json.dumps(outcomes,indent=2)+'\n')
 (OUT/'RESULT.json').write_text(json.dumps({'scope':'Finite native-tree modeled decoder/checker comparison with actual reference.py; duplicates compared only to strict raw JSON, never converted to dict first','cases_expected':len(rows),'cases_run':len(outcomes),'modules':records,'model_build':env['LEAN_PATH']},indent=2)+'\n')
 if proc.returncode:print(proc.stdout.decode());print(proc.stderr.decode());break
