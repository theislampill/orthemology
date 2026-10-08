"""Independent bounded controls; counts describe exactly what was executed."""
from itertools import product,combinations
from fractions import Fraction as F
from math import inf
import json,platform,time
from pathlib import Path
from context_effects import Origin,Invalid,compile_effect,compose,apply_effect
from read_cover import Window,cover_dp,interval_cover,minimax_cost,star_locality,coverage_sufficiency

A,B,C,D=[Origin('synthetic',s) for s in 'abcd']

def direct(events,entry):
    # Bottom-first conventional stack, intentionally independent of normal form.
    stack=list(reversed(entry));out=[];seen=set()
    if not stack:return None
    for ev in events:
        op=ev[0]
        if op=='enter':stack.append(ev[1])
        elif op in ('leave','exit'):
            if len(stack)==1:return None
            if op=='exit' and stack[-1]!=ev[1]:return None
            stack.pop()
        elif op=='emit':
            if ev[1] in seen:return None
            seen.add(ev[1]);out.append((ev[1],stack[-1]))
        else:raise AssertionError('generator emitted unsupported opcode')
    return tuple(reversed(stack)),tuple(out)

def candidate_result(effect,stack):
    try:return apply_effect(effect,stack)
    except Invalid:return None

def events(word):
    table={'a':('enter',A),'b':('enter',B),'p':('leave',),'x':('exit',A),'y':('exit',B)}
    return tuple(('emit',f't{i}') if t=='e' else table[t] for i,t in enumerate(word))

def brute_cover(keys,windows):
    # Enumerates subfamilies; never calls the subset-DP or interval algorithm.
    keys=set(keys);eligible=[w for w in windows if w.eligible and w.adequate];best=inf
    for mask in range(1<<len(eligible)):
        covered=set();cost=F(0)
        for j,w in enumerate(eligible):
            if mask>>j&1:covered.update(w.coverage);cost+=w.cost
        if keys<=covered and cost<best:best=cost
    return best

def check_plan(keys,windows,answer):
    if answer.cost==inf:return
    byname={w.name:w for w in windows};covered=set();cost=F(0)
    assert len(set(answer.plan))==len(answer.plan)
    for name in answer.plan:
        w=byname[name];assert w.eligible and w.adequate;covered.update(w.coverage);cost+=w.cost
    assert set(keys)<=covered and cost==answer.cost

def run():
    start=time.monotonic();counts={}
    direct_count=composition_count=association_count=0
    for n in range(8):
        for word in product('abpe',repeat=n):
            ev=events(word);e=compile_effect(ev)
            for depth in range(1,10):
                stack=tuple([A,B,C,D][i%4] for i in range(depth))
                assert candidate_result(e,stack)==direct(ev,stack),(word,stack,e)
                direct_count+=1
            for cut in range(n+1):
                got=compose(compile_effect(ev[:cut]),compile_effect(ev[cut:]))
                assert got==e,(word,cut,got,e)
                composition_count+=1
            if n<=5:
                for i in range(n+1):
                    for j in range(i,n+1):
                        f,g,h=compile_effect(ev[:i]),compile_effect(ev[i:j]),compile_effect(ev[j:])
                        assert compose(compose(f,g),h)==compose(f,compose(g,h))==e
                        association_count+=1
    counts.update(unkeyed_words=sum(4**n for n in range(8)),unkeyed_direct_cases=direct_count,
                  unkeyed_binary_splits=composition_count,unkeyed_triple_parenthesisations=association_count)
    kd=kc=0;stacks=[(A,),(B,),(A,B),(B,A),(A,A),(B,B),(A,B,A),(A,A,A),(A,B,C,D)]
    for n in range(6):
        for word in product('abpexy',repeat=n):
            ev=events(word);e=compile_effect(ev)
            for stack in stacks:
                assert candidate_result(e,stack)==direct(ev,stack),(word,stack,e)
                kd+=1
            for cut in range(n+1):
                got=compose(compile_effect(ev[:cut]),compile_effect(ev[cut:]))
                assert got==e,(word,cut,got,e)
                kc+=1
    counts.update(keyed_words=sum(6**n for n in range(6)),keyed_direct_cases=kd,keyed_binary_splits=kc)
    ic=0
    for n in range(1,5):
        order=[A,B,C,D][:n];intervals=[(i,j) for i in range(n) for j in range(i,n)]
        for mask in range(1<<len(intervals)):
            for pattern in range(3):
                menu=[]
                for k,(i,j) in enumerate(intervals):
                    if mask>>k&1:
                        cost=F(1) if pattern==0 else F(j-i+1) if pattern==1 else F(k%3+1,k%2+1)
                        menu.append(Window(str(k),frozenset(order[i:j+1]),cost))
                # All target subsets: deletions must preserve interval geometry.
                for demand_mask in range(1<<n):
                    keys=[o for i,o in enumerate(order) if demand_mask>>i&1]
                    expected=brute_cover(keys,menu);ans=interval_cover(keys,order,menu)
                    assert ans.cost==expected,(n,mask,pattern,demand_mask,ans,expected)
                    assert cover_dp(keys,menu).cost==expected
                    check_plan(keys,menu,ans);ic+=1
    counts['interval_menu_cost_demand_cases']=ic
    ac=0
    for n in range(1,4):
        keys=[A,B,C][:n];subsets=[frozenset(k for i,k in enumerate(keys) if mask>>i&1) for mask in range(1,1<<n)]
        worlds=tuple(dict(zip(keys,v)) for v in product((0,1),repeat=n))
        target=lambda x:all(x[k] for k in keys)
        response=lambda x,w:tuple((k,x[k]) for k in sorted(w.coverage))
        for choice in range(1<<len(subsets)):
            for pattern in range(3):
                menu=[Window(str(i),s,F(1) if pattern==0 else F(len(s)) if pattern==1 else F(i%3+1,i%2+1)) for i,s in enumerate(subsets) if choice>>i&1]
                assert star_locality(worlds,keys,menu,response)
                assert coverage_sufficiency(worlds,menu,response)
                expected=brute_cover(keys,menu)
                assert cover_dp(keys,menu).cost==expected
                assert minimax_cost(worlds,menu,target,response)==expected,(n,choice,pattern)
                ac+=1
    counts['all_boolean_menu_adaptive_cover_cases']=ac
    return {'status':'PASS','runtime':platform.python_version(),'seconds':round(time.monotonic()-start,4),'counts':counts,
        'limits':{'unkeyed_max_word_length':7,'unkeyed_entry_depths':[1,9],'keyed_max_word_length':5,'keyed_entry_stacks':len(stacks),'interval_max_origins':4,'adaptive_max_origins':3},
        'scope':'Bounded synthetic exhaustive controls, not a universal proof or source-world validation.'}

if __name__=='__main__':
    result=run();Path('logs/exhaustive_results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
