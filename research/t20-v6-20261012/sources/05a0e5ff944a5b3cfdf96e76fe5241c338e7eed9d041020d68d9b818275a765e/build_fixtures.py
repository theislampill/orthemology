from pathlib import Path
import sys,json,hashlib
from fractions import Fraction as Q
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'code'))
from prcodec import *
import flow_solver
OUT=ROOT/'evidence/concrete_fixtures';OUT.mkdir(exist_ok=True)
def serial(x):
 if isinstance(x,Q):return {'numerator':x.numerator,'denominator':x.denominator}
 if isinstance(x,dict):return {str(k):serial(v) for k,v in x.items()}
 if isinstance(x,(list,tuple)):return [serial(y) for y in x]
 return x
s_good=Program(3,3,Set(3,E('le',V(0),V(1))))
s_bad=Program(3,3,Set(3,E('le',V(2),V(1))))
p_rows=Program(4,4,Set(4,E('le',E('add',V(1),C(1)),V(0))))
p=compile_pi3(p_rows,2)
items=[('sigma2_good',compile_sigma2(s_good,2),Q(0)),('sigma2_bad',compile_sigma2(s_bad,0),Q(1)),
       ('pi3_two_good_rows',p,Q(1,4)),('shift_pi3_one_third',compile_shift(p,1,3),Q(1,2)),
       ('q8_halts',compile_q8([('I',0,1),('H',)]),Q(1)),('q8_nonhalts',compile_q8([('I',0,0)]),Q(0))]
rows=[];bits=(1,1,0,1,0,1,1,0,1,0)
for name,prog,defect in items:
 raw=encode_bytes(prog);(OUT/(name+'.p02l')).write_bytes(raw)
 assert decode_bytes(raw)==prog and decode(encode(prog))==prog
 out=output_prefix(prog,bits)
 rows.append({'id':name,'path':'evidence/concrete_fixtures/'+name+'.p02l','bytes':len(raw),
 'sha256':hashlib.sha256(raw).hexdigest(),'natural_code_hex':hex(encode(prog)),
 'input_prefix':bits,'output_prefix':out,'ordinary_theorem_defect':serial(defect),
 'defect_evidence':'Consequence of C2-10/11/12 and M2-06, NOT inferred from the finite prefix.'})
(OUT/'CODEC_FIXTURES.json').write_text(json.dumps(rows,indent=2))
flows=[]
for name,data in [('interval',[[( (Q(0),Q(1)),Q(1,2)),((Q(0),Q(-1)),Q(-1,4))],
 [( (Q(0),Q(1)),Q(3,4)),((Q(0),Q(-1)),Q(-1,2))]]),
 ('swap',[[((Q(1),Q(0)),Q(0))],[((Q(0),Q(1)),Q(0))]])]:
 result=flow_solver.solve(data);assert flow_solver.verify(result,data)
 flows.append({'id':name,'result':serial(result),'verified_against_external_input':True})
(OUT/'FLOW_FIXTURES.json').write_text(json.dumps(flows,indent=2))
print(json.dumps({'codec_roundtrips':len(rows),'finite_prefix_outputs':len(rows),'exact_flow_results':len(flows),'status':'PASS'}))
