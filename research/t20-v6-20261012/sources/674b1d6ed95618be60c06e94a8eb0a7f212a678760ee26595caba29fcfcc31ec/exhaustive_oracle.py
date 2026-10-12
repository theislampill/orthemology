"""Independent literal enumeration oracle. No candidate graph helper is used.
Enumerates every internal state/action component and every local post-fixed
state set, then solves model supports in increasing cardinality.
"""
from itertools import combinations,product

def subsets(items,nonempty=False):
 xs=tuple(sorted(items))
 return [frozenset(c) for r in range(int(nonempty),len(xs)+1) for c in combinations(xs,r)]

def closure(nodes,edges):
 nodes=tuple(nodes);reach={(s,t):s==t or t in edges.get(s,()) for s in nodes for t in nodes}
 for v in nodes:
  for s in nodes:
   for t in nodes:reach[s,t]=reach[s,t] or (reach[s,v] and reach[v,t])
 return reach

def solve(P,G,menus,trace=None):
 m=len(P);n=len(P[0]);k=len(P[0][0]);states=frozenset(range(n));wins={}
 for B in sorted(range(1,1<<m),key=lambda b:(b.bit_count(),b)):
  live=[t for t in range(m) if B>>t&1]
  after={(s,a,y):sum(1<<t for t in live if P[t][s][a][y]>0) for s in states for a in range(k) for y in states}
  internal={(s,a):frozenset(y for y in states if after[s,a,y]==B) for s in states for a in range(k)}
  exitpos={(t,s,a):any(P[t][s][a][y]>0 and after[s,a,y]!=B for y in states) for t in live for s in states for a in range(k)}
  postfixed=[]
  for W in subsets(states):
   allowed={s:[] for s in W}
   for s in W:
    for a in menus(B,s):
     legal=True
     for y in states:
      C=after[s,a,y]
      if C==0:continue
      if C==B:
       if y not in W:legal=False
      elif y not in wins[C]:legal=False
     if legal:allowed[s].append(a)
   edges={s:set().union(*(internal[s,a] for a in allowed[s])) if allowed[s] else set() for s in W}
   reach=closure(W,edges);okay=True
   for theta in live:
    target={s for s in W if any(exitpos[theta,s,a] for a in allowed[s])}
    for C in subsets(W,True):
     locations=tuple(sorted(C));choices=[]
     for s in locations:
      acts=[a for a in allowed[s] if internal[s,a]<=C and (s,a) in G[theta] and not exitpos[theta,s,a]]
      choices.append(subsets(acts,True))
     if any(not us for us in choices):continue
     for selected in product(*choices):
      U=dict(zip(locations,selected));pairs=[(s,a) for s in locations for a in U[s]]
      component_edges={s:set().union(*(internal[s,a] for a in U[s])) for s in locations}
      paths=closure(C,component_edges)
      if not all(paths[s,t] for s in C for t in C):continue
      valid=True
      for eta in live:
       equal=all(P[theta][s][a][y]==P[eta][s][a][y] for s,a in pairs for y in states)
       if equal and not all((s,a) in G[eta] for s,a in pairs):valid=False;break
      if valid:target.update(C)
    if not all(any(reach[s,t] for t in target) for s in W):okay=False;break
   if okay:postfixed.append(W)
  wins[B]=set().union(*postfixed) if postfixed else set()
  if trace is not None:trace[B]=[sorted(W) for W in postfixed]
 return wins
