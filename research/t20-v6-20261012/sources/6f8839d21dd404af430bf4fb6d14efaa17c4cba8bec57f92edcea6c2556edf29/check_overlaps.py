#!/usr/bin/env python3
"""Exact finite left-linearity/critical-overlap check for proposed extended SKI TRS.
This checks orthogonality hypotheses, not a whole-source model or semantic soundness.
"""
from collections import Counter
from pathlib import Path
import json

A = lambda f,x: ('@',f,x)
V = lambda name: ('?',name)
def apps(f,*xs):
    for x in xs: f=A(f,x)
    return f
x,y,f,g=map(V,['x','y','f','g'])
values = [('I','I'),('K','K'),('Kx',A('K',x)),('S','S'),
          ('Sx',A('S',x)),('Sxy',apps('S',x,y)),('nu','nu'),('nux',A('nu',x))]
rules=[('I',A('I',x),x),('K',apps('K',x,y),x),
       ('S',apps('S',f,g,x),A(A(f,x),A(g,x))),
       ('nu_a0',apps('nu',f,'a0'),'a0'),('nu_a1',apps('nu',f,'a1'),'a1')]
rules += [('nu_'+name,apps('nu',f,v),A(f,v)) for name,v in values]

def variable(t): return isinstance(t,tuple) and t[0]=='?'
def variables(t):
    if variable(t): return [t[1]]
    if isinstance(t,tuple): return variables(t[1])+variables(t[2])
    return []
def rename(t,prefix):
    if variable(t): return V(prefix+t[1])
    if isinstance(t,tuple): return A(rename(t[1],prefix),rename(t[2],prefix))
    return t
def subterms(t,path=()):
    if variable(t): return
    yield path,t
    if isinstance(t,tuple):
        yield from subterms(t[1],path+(0,))
        yield from subterms(t[2],path+(1,))
def deref(t,subst):
    while variable(t) and t[1] in subst: t=subst[t[1]]
    return t
def occurs(name,t,subst):
    t=deref(t,subst)
    if variable(t): return t[1]==name
    return isinstance(t,tuple) and (occurs(name,t[1],subst) or occurs(name,t[2],subst))
def unify(a,b):
    subst={}; todo=[(a,b)]
    while todo:
        a,b=map(lambda t:deref(t,subst),todo.pop())
        if a==b: continue
        if variable(b) and not variable(a): a,b=b,a
        if variable(a):
            if occurs(a[1],b,subst): return None
            subst[a[1]]=b
        elif isinstance(a,tuple) and isinstance(b,tuple) and a[0]==b[0]:
            todo.extend([(a[1],b[1]),(a[2],b[2])])
        else: return None
    return subst

overlaps=[]; self_root=[]; trials=0
for i,(n,l,r) in enumerate(rules):
    assert max(Counter(variables(l)).values(),default=0)<=1
    assert set(variables(r))<=set(variables(l))
    for j,(m,k,s) in enumerate(rules):
        for path,t in subterms(rename(l,'outer_')):
            trials+=1
            unifier=unify(t,rename(k,'inner_'))
            if unifier is not None:
                match={'outer':n,'inner':m,'position':list(path)}
                if i==j and not path: self_root.append(match)
                else: overlaps.append(match)
assert not overlaps, overlaps
result={'status':'PASS','rule_count':len(rules),'left_linear':True,
        'nonvariable_overlap_trials':trials,'trivial_root_self_overlaps':len(self_root),
        'nontrivial_overlaps':overlaps,'rules':rules,
        'scope':'Exact orthogonality hypotheses only; not a confluence formalization or whole-source model.'}
Path(__file__).with_name('overlap-results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='rules'},indent=2))
