#!/usr/bin/env python3
"""Independent candidate differential checks; standard-library only.

The three reference mechanisms live in independent_models.py and import no
candidate code. Never assigns alternate worlds to the actual source capture.
"""
import argparse, hashlib, importlib, itertools, json, math, platform, random, sys, time
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
from independent_models import direct_stack, InvalidStack, subset_cover, partition_minimax, star_locality as own_star

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
DEFAULT=ROOT/'research'/'occurrence-continuation'/'checker'
counts=Counter()

def require(value, why):
    if not value: raise AssertionError(why)

def caught(fn, *args, **kwargs):
    try: return ('ok', fn(*args, **kwargs))
    except (ValueError, KeyError, TypeError) as error: return ('invalid', type(error).__name__)

def outcome_equal(a,b):
    return a[0]==b[0] and (a[0]=='invalid' or a[1]==b[1])

def subsets(xs):
    return [frozenset(xs[i] for i in range(len(xs)) if m>>i&1) for m in range(1<<len(xs))]

def run_effects(c):
    A,B,C=[c.Origin('S',x) for x in 'abc']
    keys=[A,B]
    stacks=[tuple(s) for n in range(0,6) for s in itertools.product(keys,repeat=n)]
    stacks += [tuple(c.Origin('S',f'input{i}') for i in range(n)) for n in range(6,9)]
    for n in range(5):
      for word in itertools.product(range(7),repeat=n):
        events=[]; oracle=[]; selected=set()
        for i,op in enumerate(word):
          if op<2: events.append(('enter',keys[op]));oracle.append(events[-1])
          elif op==2: events.append(('leave',));oracle.append(('leave',None))
          elif op<5: events.append(('exit',keys[op-3]));oracle.append(events[-1])
          else:
            t=f't{i}';events.append(('emit',t));oracle.append(('emit',t if op==5 else None))
            if op==5:selected.add(t)
        def compile_local(part):
          local_ids={ev[1] for ev in part if ev[0]=='emit'}
          return c.compile_effect(part,selected=selected & local_ids)
        effect=compile_local(events)
        counts['effect_words']+=1
        if all(op not in (3,4) for op in word):
          level=minimum=0
          for op in word:
            level += 1 if op<2 else (-1 if op==2 else 0)
            minimum=min(minimum,level)
          require(effect.depth==1-minimum,('exact domain',word,effect))
          counts['exact_unkeyed_depths']+=1
        for stack in stacks:
          actual=caught(c.apply_effect,effect,stack)
          expected=caught(direct_stack,oracle,stack)
          require(outcome_equal(actual,expected),('direct stack',word,stack,actual,expected))
          counts['direct_stack_pairs']+=1
        for i in range(n+1):
          left=compile_local(events[:i])
          right=compile_local(events[i:])
          composite=c.compose(left,right)
          for stack in stacks[::5]:
            require(outcome_equal(caught(c.apply_effect,composite,stack),caught(direct_stack,oracle,stack)),('split',word,i,stack))
            counts['split_stack_pairs']+=1
          for j in range(i,n+1):
            f=compile_local(events[:i])
            g=compile_local(events[i:j])
            h=compile_local(events[j:])
            lh=c.compose(c.compose(f,g),h);rh=c.compose(f,c.compose(g,h))
            for stack in stacks[::10]:
              expected=caught(direct_stack,oracle,stack)
              require(outcome_equal(caught(c.apply_effect,lh,stack),expected),('left association',word,i,j,stack))
              require(outcome_equal(caught(c.apply_effect,rh,stack),expected),('right association',word,i,j,stack))
              counts['association_stack_triples']+=1
    # Adversarial boundaries and fork substitutions, independently expected.
    branch=c.compile_effect([('emit','same'),('leave',),('emit','next')])
    require(caught(c.compose,branch,branch)[0]=='invalid','collision overwritten')
    alpha1=c.rename_outputs(branch,'one');alpha2=c.rename_outputs(branch,'two')
    require(len(c.compose(alpha1,alpha2).emissions)==4,'fresh IDs coalesced')
    require(c.resolve_demands(branch,{0:A,1:A})==frozenset({A}),'origin alias not quotiented')
    require(c.resolve_demands(branch,{0:A,1:B})==frozenset({A,B}),'different original keys coalesced')
    require(caught(c.resolve_demands,branch,{0:A})[0]=='invalid','omitted identity invented')
    suff=c.compile_effect([('exit',A),('emit','target')])
    require(caught(c.apply_effect,suff,[c.Origin('S2','a'),B])[0]=='invalid','wrong snapshot accepted')
    # All true role witnesses do not supply the missing identity map.
    held={A:True,B:True,C:True}
    require(caught(c.resolve_demands,branch,{})[0]=='invalid','roles became origin map')
    counts['effect_named_controls']=8


def run_covers(c,r):
    keys=[c.Origin('synthetic',str(i)) for i in range(4)]
    def menu_from(actions):return [r.Window(name,cov,F(cost)) for name,cov,cost in actions]
    rng=random.Random(67103)
    for n in range(5):
      k=keys[:n];ss=subsets(k)
      menus=[]
      if n<=3:
        # Every set family, including empty coverage and impossible families.
        for mask in range(1<<len(ss)):
          menus.append([(f'w{i}',ss[i],F(1+(i%3),1+(i%2))) for i in range(len(ss)) if mask>>i&1])
      else:
        for case in range(180):
          picks=rng.sample(range(len(ss)),rng.randrange(0,9))
          menus.append([(f'w{i}',ss[i],F(rng.randrange(1,9),rng.randrange(1,5))) for i in picks])
      for actions in menus:
        menu=menu_from(actions)
        for demand in ss:
          expected,witness=subset_cover(demand,actions)
          got=r.cover_dp(demand,menu)
          require(got.cost==expected,('cover',demand,actions,got,expected))
          # Verify returned certificate once representation becomes known.
          counts['cover_subfamily_instances']+=1
          convex=all(not [i for i,x in enumerate(k) if x in cov&demand] or
            max(i for i,x in enumerate(k) if x in cov&demand)-min(i for i,x in enumerate(k) if x in cov&demand)+1
            ==len([x for x in k if x in cov&demand])
            for _,cov,_ in actions)
          # Geometry must be convex over demanded order, not full source order.
          demand_order=[x for x in k if x in demand]
          convex=all(not [i for i,x in enumerate(demand_order) if x in cov] or
            max(i for i,x in enumerate(demand_order) if x in cov)-min(i for i,x in enumerate(demand_order) if x in cov)+1
            ==len(cov&demand) for _,cov,_ in actions)
          result=caught(r.interval_cover,list(reversed(demand_order))+demand_order,k,menu)
          if convex:
            require(result[0]=='ok' and result[1].cost==expected,('interval',demand,actions,result,expected))
            counts['convex_interval_instances']+=1
          else:
            require(result[0]=='invalid',('nonconvex accepted',demand,actions,result))
            counts['nonconvex_rejections']+=1
    for cost in [0,-1,F(-1,3)]:
      require(caught(r.Window,'bad',frozenset(keys),F(cost))[0]=='invalid','nonpositive Window accepted')
      counts['positive_cost_rejections']+=1


def run_adaptive(c,r):
    A,B,C,Z=[c.Origin('synthetic',x) for x in 'abcz']
    for n in range(4):
      keys=[A,B,C][:n]
      worlds=tuple(dict(zip(keys,bits)) for bits in itertools.product([0,1],repeat=n))
      verdicts=[all(w.values()) for w in worlds]
      ss=subsets(keys)
      # All menus on n<=3, exact weighted observations, compared to independent
      # bottom-up all-knowledge-state solver rather than candidate cover oracle.
      for mask in range(1<<len(ss)):
        menu=[r.Window(f'w{i}',ss[i],F(i%3+1,2)) for i in range(len(ss)) if mask>>i&1]
        def response(w,win):return tuple(w[k] for k in sorted(win.coverage))
        cols=[tuple(response(w,win) for w in worlds) for win in menu]
        expected=partition_minimax(verdicts,cols,[w.cost for w in menu])
        got=r.minimax_cost(worlds,menu,lambda w:all(w.values()),response)
        require(got==expected,('adaptive',n,mask,got,expected))
        require(got==subset_cover(keys,[(w.name,w.coverage,w.cost) for w in menu])[0],('adaptive-cover',n,mask))
        require(r.star_locality(worlds,keys,menu,response),'local product rejected')
        require(own_star(worlds,keys,[(w.coverage,col) for w,col in zip(menu,cols)]),'independent product rejected')
        counts['adaptive_product_menus']+=1
    worlds=tuple(dict(zip([A,B],bits)) for bits in itertools.product([0,1],repeat=2))
    both=frozenset({A,B}); verdicts=[all(w.values()) for w in worlds]
    menu=[r.Window('a',frozenset({A}),F(4)),r.Window('b',frozenset({B}),F(4)),r.Window('outside',frozenset(),F(1))]
    for field in ['outside-conjunction','rich-label','status','length','timing','authentication-payload']:
      def resp(w,win):
        if win.name=='outside':return (field,all(w.values()))
        return tuple(w[k] for k in sorted(win.coverage))
      cols=[tuple(resp(w,win) for w in worlds) for win in menu]
      require(not r.star_locality(worlds,both,menu,resp),(field,'star accepted leak'))
      require(not own_star(worlds,both,[(w.coverage,col) for w,col in zip(menu,cols)]),(field,'own star'))
      require(r.minimax_cost(worlds,menu,lambda w:all(w.values()),resp)==1,(field,'missed cheaper decision'))
      require(partition_minimax(verdicts,cols,[w.cost for w in menu])==1,(field,'reference'))
      counts['complete_response_leaks']=counts['complete_response_leaks']+1
    def plain(w,win):return tuple(w[k] for k in sorted(win.coverage))
    require(not r.star_locality(worlds,both,menu,plain,metadata=lambda w:tuple(w[k] for k in [A,B])),'informative public metadata ignored')
    counts['public_metadata_leaks']=1
    require(r.minimax_cost(worlds,menu,lambda w:all(w.values()),plain,metadata=lambda w:tuple(w[k] for k in [A,B]))==0,'public evidence not free')
    counts['public_evidence_cost_zero']=1
    constant_menu=[r.Window('constant-all',both,F(1))]
    constant=lambda w,win:None
    require(r.star_locality(worlds,both,constant_menu,constant),'locality should be vacuous here')
    require(not r.coverage_sufficiency(worlds,constant_menu,constant),'false adequate-coverage certification')
    require(r.minimax_cost(worlds,constant_menu,lambda w:all(w.values()),constant)==math.inf,'constant response decides')
    require(r.coverage_sufficiency(worlds,menu[:2],plain),'honest covered-bit response rejected')
    counts['locality_adequacy_separation']=4
    # Available whole-source and task verdict are real menu alternatives in this
    # synthetic model; no contradictory assignments to the actual source.
    whole=menu[:2]+[r.Window('whole',both,F(1,2))]
    require(r.minimax_cost(worlds,whole,lambda w:all(w.values()),plain)==F(1,2),'whole source alternative omitted')
    counts['whole_source_competitor']=1
    # Positive-star sufficiency need not require a full product model.
    star=(worlds[-1],worlds[1],worlds[2])
    require(r.star_locality(star,both,whole,plain),'n+1 star refused')
    require(r.minimax_cost(star,whole,lambda w:all(w.values()),plain)==F(1,2),'star minimax')
    counts['star_only_family']=1
    # Known negative has zero remaining decision cost, despite unavailable key.
    negatives=tuple(w for w in worlds if w[A]==0)
    require(r.minimax_cost(negatives,[],lambda w:all(w.values()),plain)==0,'known false not immediate')
    require(r.role_decision(both,{A:False}) is False,'known false role decision')
    require(r.role_decision([], {}) is True,'empty selected query')
    counts['known_false_empty_query']=2
    unavailable=[r.Window('retired',both,F(1),eligible=False)]
    require(r.cover_dp(both,unavailable).cost==math.inf,'retired service treated available')
    require(r.minimax_cost(worlds,unavailable,lambda w:all(w.values()),plain)==math.inf,'adaptive retired service')
    counts['retirement_controls']=2
    require(caught(r.active_menu,[r.Window('dup',both,F(1)),r.Window('dup',frozenset({A}),F(2))])[0]=='invalid','duplicate window ID')
    require(caught(r.interval_cover,both,[A,B,A],whole)[0]=='invalid','duplicate original coordinate')
    require(caught(r.role_decision,both,{A:'False'})[0]=='invalid','truthy pseudo-evidence')
    counts['malformed_contract_rejections']=3


def run_general_tables(c,r):
    rng=random.Random(67003)
    for case in range(360):
        n=rng.randrange(2,9);m=rng.randrange(0,5)
        worlds=tuple({'index':i} for i in range(n))
        targets=tuple(bool(rng.randrange(2)) for _ in range(n))
        columns=[tuple(rng.randrange(3) for _ in range(n)) for _ in range(m)]
        costs=[F(rng.randrange(1,8),rng.randrange(1,5)) for _ in range(m)]
        public=tuple(rng.randrange(2) if case%3==0 else 0 for _ in range(n))
        blocks={}
        for i,v in enumerate(public):blocks[v]=blocks.get(v,0)|(1<<i)
        expected=partition_minimax(targets,columns,costs,tuple(blocks.values()))
        windows=[r.Window(str(j),frozenset(),costs[j]) for j in range(m)]
        got=r.minimax_cost(worlds,windows,lambda w:targets[w['index']],lambda w,win:columns[int(win.name)][w['index']],metadata=lambda w:public[w['index']])
        require(got==expected,('general-table',case,got,expected))
        counts['general_observation_tables']+=1


def main():
    p=argparse.ArgumentParser();p.add_argument('--candidate',type=Path,default=DEFAULT);p.add_argument('--output',type=Path,default=HERE/'INDEPENDENT_RESULTS.json');args=p.parse_args()
    sys.path.insert(0,str(args.candidate.resolve()))
    c=importlib.import_module('context_effects');r=importlib.import_module('read_cover')
    started=time.time()
    run_effects(c);run_covers(c,r);run_adaptive(c,r);run_general_tables(c,r)
    result={'status':'PASS','scope':'finite executable checks only; source interpretation and ordinary proofs separate','python':sys.version,'platform':platform.platform(),'optimized':not __debug__,'seconds':round(time.time()-started,4),'counts':dict(counts),'candidate':str(args.candidate.resolve()),'candidate_hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(args.candidate.glob('*.py'))},'review_hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [HERE/'independent_models.py',Path(__file__).resolve()]}}
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
