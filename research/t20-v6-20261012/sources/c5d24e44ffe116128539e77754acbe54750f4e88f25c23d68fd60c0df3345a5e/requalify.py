#!/usr/bin/env python3
"""Fresh recovery-successor qualification, not a recreated pre-loss receipt.
All algorithms are standard-library only; the literal exhaustive oracle is an
exactly recovered source. No finite test is a stochastic existence theorem.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from types import ModuleType
from datetime import datetime,timezone
import sys,random,json,hashlib,time,argparse
BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/'snapshot'))
from support_solver import solve_supports
from common_graph import ModelFamily,solve as solve_common
from exhaustive_oracle import solve as oracle

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def enc(x):
 if isinstance(x,F):return str(x)
 if isinstance(x,dict):return {str(k):enc(v) for k,v in x.items()}
 if isinstance(x,(set,frozenset)):return sorted(enc(v) for v in x)
 if isinstance(x,(tuple,list)):return [enc(v) for v in x]
 return x

def load_pair(folder,label):
 g=ModuleType('review_graph_'+label);g.__file__=str(folder/'common_graph.py');sys.modules[g.__name__]=g
 exec(compile(Path(g.__file__).read_text(),g.__file__,'exec'),g.__dict__)
 sys.modules['common_graph']=g
 s=ModuleType('review_solver_'+label);s.__file__=str(folder/'support_solver.py')
 exec(compile(Path(s.__file__).read_text(),s.__file__,'exec'),s.__dict__)
 return s.solve_supports,g

def generate(r,m,n,k,all_good=False,all_menus=False,common=False):
 shared={(s,a):r.randrange(1,1<<n) for s in range(n) for a in range(k)} if common else None
 P=[]
 for t in range(m):
  states=[]
  for s in range(n):
   actions=[]
   for a in range(k):
    if common:weights=[r.randrange(1,6) if shared[s,a]>>y&1 else 0 for y in range(n)]
    else:
     weights=[r.randrange(5) for _ in range(n)]
     if not sum(weights):weights[r.randrange(n)]=1
    actions.append(tuple(F(w,sum(weights)) for w in weights))
   states.append(tuple(actions))
  P.append(tuple(states))
 G=[{(s,a) for s in range(n) for a in range(k) if all_good or r.randrange(3)} for t in range(m)]
 M={(B,s):{a for a in range(k) if all_menus or r.randrange(4)} for B in range(1,1<<m) for s in range(n)}
 return P,G,M

def mixed_probability(P,tag):
 def view(xs,i):return list(xs) if i%3==0 else tuple(xs) if i%3==1 else iter(tuple(xs))
 models=[]
 for t,states in enumerate(P):
  rows=[]
  for s,actions in enumerate(states):
   rows.append(view([view(row,tag+t+s+a) for a,row in enumerate(actions)],tag+t+s))
  models.append(view(rows,tag+t))
 return view(models,tag)

def named_cases():
 out=[]
 def add(P,G,M,name):out.append((P,G,M,name))
 P=[[[ (F(1),F(0)) ] for _ in range(2)], [[(F(0),F(1))] for _ in range(2)]]
 add(P,[{(0,0),(1,0)}]*2,{(B,s):(set() if B==2 else {0}) for B in range(1,4) for s in range(2)},'dead-proper-successor')
 add([[[ (F(1),F(0)) ],[(F(1),F(0))]]],[{(0,0),(1,0)}],{(1,s):{0} for s in range(2)},'impossible-successor')
 add([[[ (F(0),F(1,2),F(1,2)) ],[(F(0),F(1),F(0))],[(F(0),F(0),F(1))]]],[{(1,0)}],{(1,s):{0} for s in range(3)},'greatest-fixedpoint-trap')
 add([[[ (F(1),),(F(1),) ]]]*2,[{(0,0)},{(0,1)}],{(B,0):{0,1} for B in range(1,4)},'identical-opposite-targets')
 P=[[[ (F(2,3),F(1,3)),(F(2,3),F(1,3)) ] for _ in range(2)],[[ (F(1,3),F(2,3)),(F(1,3),F(2,3)) ] for _ in range(2)]]
 M={(B,s):{0,1} for B in range(1,4) for s in range(2)}
 add(P,[{(s,0) for s in range(2)},{(s,1) for s in range(2)}],M,'informative-opposite-targets')
 add(P,[{(s,0) for s in range(2)},set()],M,'one-model-has-no-target')
 P=[[[ (F(1),F(0)) ],[(F(0),F(1))]], [[(F(1,2),F(1,2))],[(F(0),F(1))]]]
 add(P,[{(0,0)},{(1,0)}],{(B,s):(set() if B==3 and s==1 else {0}) for B in range(1,4) for s in range(2)},'exit-into-newly-lawful-state')
 return out

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();out=a.out.resolve();out.mkdir(parents=True,exist_ok=False)
 result={'status':'RUNNING','recovery_successor':True,'old_receipt_recreated':False,'started_utc':datetime.now(timezone.utc).isoformat(),'source_sha256':{p.name:sha(p) for p in (BASE/'snapshot').glob('*.py')},'oracle_sha256':sha(BASE/'checks/exhaustive_oracle.py'),'driver_sha256':sha(Path(__file__))}
 def save(): (out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
 def check(P,G,M,label):
  exp=oracle(P,G,lambda B,s:M[B,s]);got=solve_supports(P,G,lambda B,s:M[B,s])
  if exp!=got:
   (out/'DISAGREEMENT.json').write_text(json.dumps(enc({'label':label,'P':P,'G':G,'M':M,'expected':exp,'actual':got}),indent=2)+'\n')
   raise AssertionError(label)
  return exp
 save();start=time.monotonic();counts={'grid_cases':0,'random_cases':0,'three_model_stateful_cases':0,'support_regions':0,'nonempty_regions':0,'mixed_general_cases':0}
 specs=[]
 for spec in range(4):
  if spec==0:G=[{(s,t) for s in range(2)} for t in range(2)];M={(B,s):{0,1} for B in range(1,4) for s in range(2)}
  elif spec==1:G=[{(t,a) for a in range(2)} for t in range(2)];M={(B,s):({0,1} if B==3 else {0 if B==1 else 1}) for B in range(1,4) for s in range(2)}
  elif spec==2:G=[{(s,a) for s in range(2) for a in range(2) if (s+a)%2==t} for t in range(2)];M={(B,s):({0,1} if B==3 else (set() if B==1 and s==1 else {1})) for B in range(1,4) for s in range(2)}
  else:G=[{(s,s) for s in range(2)} for _ in range(2)];M={(B,s):({s} if B==3 else {1-s}) for B in range(1,4) for s in range(2)}
  specs.append((G,M))
 for i,rows in enumerate(product([F(0),F(1,2),F(1)],repeat=8)):
  P=[[[ (1-rows[4*t+2*s+a],rows[4*t+2*s+a]) for a in range(2)] for s in range(2)] for t in range(2)]
  for j,(G,M) in enumerate(specs):
   exp=check(P,G,M,f'grid-{i}-{j}');counts['grid_cases']+=1;counts['support_regions']+=len(exp);counts['nonempty_regions']+=sum(bool(v) for v in exp.values())
 print('GRID',counts['grid_cases'],'PASS',flush=True)
 r=random.Random(10011233);dimensions={}
 for i in range(2700):
  if i>=1800:m=n=3;k=2;group='three_model_stateful_cases'
  else:m=2+r.randrange(2);n=1+r.randrange(3);k=0 if i%71==0 else 1+r.randrange(2);group='random_cases'
  P,G,M=generate(r,m,n,k,all_good=i>=1800 and i%5==0,all_menus=i>=1800 and i%5==0)
  exp=check(P,G,M,f'random-{i}');counts[group]+=1;counts['support_regions']+=len(exp);counts['nonempty_regions']+=sum(bool(v) for v in exp.values());dimensions[str((m,n,k))]=dimensions.get(str((m,n,k)),0)+1
  if i<120 or 1800<=i<1920:
   got=solve_supports(mixed_probability(P,i),(iter(g) for g in G),lambda B,s:iter(M[B,s]));assert got==exp;counts['mixed_general_cases']+=1
 result['arbitrary_support_oracle']={**counts,'dimensions':dimensions,'seed':10011233};save();print('ARBITRARY SUPPORT',sum(counts[g] for g in ['grid_cases','random_cases','three_model_stateful_cases']),'PASS',flush=True)
 # Independently exercise the repaired common-support public object boundary.
 r=random.Random(10011234)
 for i in range(1200):
  m=1+i%3;n=1+(i//3)%3;k=0 if i%83==0 else 1+i%2
  P,G,allM=generate(r,m,n,k,common=True);M={s:allM[1,s] for s in range(n)}
  exp=oracle(P,G,lambda B,s:M[s])[(1<<m)-1]
  family=ModelFamily(mixed_probability(P,i),[iter(g) for g in G],{s:iter(v) for s,v in M.items()})
  first=solve_common(family);second=solve_common(family);assert set(first['winning_states'])==exp and first==second
 result['common_public_api']={'cases':1200,'mixed_containers_and_iterators':1200,'repeated_same_object_solve':1200,'seed':10011234};save();print('COMMON API 1200 PASS',flush=True)
 # Reproduce both original defects from exactly recovered predecessor bytes.
 old,old_graph=load_pair(BASE/'defect-snapshot','old')
 p0=[[[F(1)],[F(1)]]];p1=[[(F(1),),(F(1),)]];G=[{(0,0)},{(0,1)}];menus=lambda B,s:{0,1}
 assert old([p0,p1],G,menus)[3]=={0} and solve_supports([p0,p1],G,menus)[3]==set()
 assert old([[[[F(1)]]]],[(x for x in [(0,0)])],lambda B,s:{0})[1]==set()
 assert solve_supports([[[[F(1)]]]],[(x for x in [(0,0)])],lambda B,s:{0})[1]=={0}
 assert old_graph.solve(old_graph.ModelFamily([p0,p1],G,{0:{0,1}}))['winning_states']==[0]
 assert solve_common(ModelFamily([p0,p1],G,{0:{0,1}}))['winning_states']==[]
 result['old_defect_reproduction']={'mixed_rows_false_positive':True,'consumed_good_iterator_false_negative':True,'both_successors_corrected':True};save()
 invalid=[([],[],lambda B,s:set()),([[]],[set()],lambda B,s:set()),([[[(F(1),)]]],[],lambda B,s:{0}),([[[(F(1),)]],[]],[set(),set()],lambda B,s:{0}),([[[(F(1),)]],[[]]],[set(),set()],lambda B,s:{0}),([[[(F(1),F(0))]]],[{(0,0)}],lambda B,s:{0}),([[[(F(-1),F(2))],[(F(0),F(1))]]],[{(0,0)}],lambda B,s:{0}),([[[(F(1,2),)]]],[{(0,0)}],lambda B,s:{0}),([[[(1.0,)]]],[{(0,0)}],lambda B,s:{0}),([[[(1,)]]],[{(0,0)}],lambda B,s:{0}),([[[(True,)]]],[{(0,0)}],lambda B,s:{0}),([[[(F(1),)]]],[{(1,0)}],lambda B,s:{0}),([[[(F(1),)]]],[{(0,0)}],lambda B,s:{-1}),([[[(F(1),)]]],[{(0,0)}],lambda B,s:{1})]
 for P,G,M in invalid:
  try:solve_supports(P,G,M)
  except (ValueError,TypeError,IndexError):pass
  else:raise AssertionError('Invalid instance accepted')
 assert solve_supports([[[]]],[set()],lambda B,s:set())=={1:set()}
 for eps,want in [(F(0),set()),(F(1,10**30),{0,1})]:
  P=[[[ (1-eps,eps) ] for s in range(2)], [[(F(0),F(1))] for s in range(2)]];G=[{(0,0),(1,0)}]*2
  assert solve_supports(P,G,lambda B,s:set() if B==2 else {0})[3]==want
 result['input_boundaries']={'invalid_rejections':len(invalid),'empty_action_type_loses':True,'zero_vs_positive_10_pow_minus_30_changes_verdict':True};save()
 # Semantic mutations are compared to the literal oracle, with a full baseline
 # positive control on the corpus before attempting any mutation.
 cases=named_cases();r=random.Random(10011235)
 for i in range(1400):
  P,G,M=generate(r,2+(i%5==0),2+(i%3==0),2);cases.append((P,G,M,f'random-{i}'))
 enriched=[]
 for P,G,M,label in cases:enriched.append((P,G,M,label,check(P,G,M,label)))
 raw_s=(BASE/'snapshot/support_solver.py').read_text();raw_g=(BASE/'snapshot/common_graph.py').read_text()
 same='same=[j for j in range(family.m) if all(family.probabilities[j][s][a]==family.probabilities[theta][s][a] for s,a in pairs)]'
 mutants=[('ignore-proper-child','s','else y in winning[C]','else True'),('existential-successor','s','if all(C==0 or','if any(C==0 or'),('zero-is-positive','s','if probabilities[t][s][a][y]>0)','if probabilities[t][s][a][y]>=0)'),('union-is-common-stay','s','if updates[s,a,y]==B)','if updates[s,a,y]!=0)'),('one-local-pass','s','if successor==W:break','if True:\n                W=frozenset(successor)\n                break'),('candidate-only-match','g',same,'same=[theta]'),('all-rivals-match','g',same,'same=list(range(family.m))'),('some-model-suffices','s','successor.intersection_update(reachable)','successor.update(reachable)')]
 mr=[]
 for i,(name,target,before,after) in enumerate(mutants):
  s,g=raw_s,raw_g
  if target=='s':assert s.count(before)==1;s=s.replace(before,after)
  else:assert g.count(before)==1;g=g.replace(before,after)
  if name=='some-model-suffices':s=s.replace('successor=set(W)','successor=set()')
  folder=out/'mutations'/name;folder.mkdir(parents=True);(folder/'support_solver.py').write_text(s);(folder/'common_graph.py').write_text(g);fn,_=load_pair(folder,'mutation_'+str(i));record={'name':name,'status':'SURVIVED'}
  for P,G,M,label,expected in enriched:
   try:actual=fn(P,G,lambda B,s:M[B,s])
   except Exception as e:actual={'exception':type(e).__name__,'message':str(e)}
   if actual!=expected:
    record.update(status='REJECTED',counterexample=label)
    (folder/'COUNTEREXAMPLE.json').write_text(json.dumps(enc({'P':P,'G':G,'M':M,'expected':expected,'actual':actual}),indent=2)+'\n');break
  assert record['status']=='REJECTED',record;mr.append(record)
 result['mutations']={'baseline_cases':len(enriched),'baseline_pass':True,'rejected':mr};result.update(status='PASS_SCOPED_FRESH_IMPLEMENTATION_REVIEW',finished_utc=datetime.now(timezone.utc).isoformat(),seconds=time.monotonic()-start);save();print(json.dumps(result,indent=2))
if __name__=='__main__':main()
