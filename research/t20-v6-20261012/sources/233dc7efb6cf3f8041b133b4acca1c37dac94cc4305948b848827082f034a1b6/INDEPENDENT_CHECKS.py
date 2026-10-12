"""Independent exact controls. No imports from candidate control code."""
from fractions import Fraction as Q
from itertools import product
import json
n = 0
def require(cond, name):
    global n
    if not cond: raise RuntimeError(name)
    n += 1

# Integrate the actual binary flip channel against the inherited exact angular law.
base = {(0,0):Q(5,12),(0,1):Q(1,12),(1,0):Q(1,12),(1,1):Q(5,12)}
values = {}
for j in range(61):
    e=Q(j,60); d=(1-2*e)/6
    lp={z:Q(1,4) for z in base}
    pp={z:(1-e)*base[z]+e*base[(1-z[0],z[1])] for z in base}
    require(pp=={z:Q(1,4)+(d if z[0]==z[1] else -d) for z in base},'flip convolution')
    for prior in [Q(1,7),Q(1,3),Q(1,2),Q(4,5)]:
        mix={z:prior*pp[z]+(1-prior)*lp[z] for z in base}
        post={z:prior*pp[z]/mix[z] for z in base}
        # Compute risk from both underlying truth states, not posterior variance.
        risk=sum((1-prior)*lp[z]*post[z]**2+prior*pp[z]*(1-post[z])**2 for z in base)
        gain=prior*(1-prior)-risk
        independent_identity=prior**2*(1-prior)**2*sum((pp[z]-lp[z])**2/mix[z] for z in base)
        require(gain==independent_identity,'general prior squared loss identity')
        if prior==Q(1,2):
            require(gain==d*d/(1-4*d*d),'equal prior value')
            values[str(e)]=str(gain)
    require(sum(pp[z] for z in base if z[0]==0)==Q(1,2),'Q marginal')
    require(sum(pp[z] for z in base if z[1]==0)==Q(1,2),'Y marginal')
require(values['0']=='1/32' and values['1/4']=='1/140' and values['1/2']=='0','reported gains')
# At price 1/64, strict inquiry preference is |delta| > 1/sqrt(68).
for j in range(61):
    d=(1-2*Q(j,60))/6
    require((d*d/(1-4*d*d)>Q(1,64))==(68*d*d>1),'exact cost boundary')
old=base[(1,1)]/Q(1,4)
new=(Q(3,4)*base[(1,1)]+Q(1,4)*base[(0,1)])/Q(1,4)
require(new/(1+new)==Q(4,7),'replace calibration')
require(old*new/(1+old*new)==Q(20,29),'duplicate calibration')
# Linked trials versus disjoint-trial Cartesian product.
for z in base:
    require(sum(base[x] for x in base if x[0]==z[0])*sum(base[x] for x in base if x[1]==z[1])==Q(1,4),'unlinked independent trial')
# Abstract finite adaptive-kernel check. Rational kernels stand in for the
# proved common Gaussian response kernels; this does not enumerate Gaussian laws.
def transcript(model):
    out={}
    def visit(history,mass):
        stop=Q(1) if len(history)==5 else (Q(1,3) if history and history[-1][1] else Q(0))
        if stop: out[history]=out.get(history,Q(0))+mass*stop
        if stop==1: return
        design=(sum(y for a,y in history)+len(history))%3
        # Deliberately distinct expressions of the same common kernel.
        p=[Q(1,5),Q(1,2),Q(4,5)][design]
        if model=='P': p=1-(1-p)
        for y in (0,1): visit(history+((design,y),),mass*(1-stop)*(p if y else 1-p))
    visit((),Q(1)); return out
l=transcript('L'); p=transcript('P')
require(l==p and sum(l.values())==1,'adaptive stop/design common kernels')
# Finite illustrative late diagonal discovery, not a computability proof.
def admissible(s): return len(s)<3 or s[0]==1
def plan(k): return tuple([int(k>=3)]+[0]*(k-1)) if k else ()
for k in range(7):
    h=plan(k); require(admissible(h),'finite stage plan')
    require(all(admissible(h[:j]) for j in range(k+1)),'finite prefix closure')
require(plan(2)!=(plan(3)[:2]) and admissible(plan(2)),'valid past need not extend')
# Direct truth-state enumeration of migration, semantic readout and arbitrary
# length-4 input traces on both encodings (different control coverage).
def encode(q,parity): return tuple(x^parity for x in q)
for state in product((0,1),repeat=2):
  for par in (0,1):
    for inputs in product((0,1),repeat=4):
      q=state; stored=encode(q,par)
      for bit in inputs:
        require(encode(stored,par)[0]==q[0],'readout')
        stored=encode(encode(stored,par),1-par); par=1-par
        require(encode(stored,par)==q,'migration semantic identity')
        q=(q[1],bit)
        decoded=encode(stored,par); stored=encode((decoded[1],bit),par)
        require(encode(stored,par)==q,'execution semantic identity')
print(json.dumps({'status':'PASS','exact_checks':n,'adaptive_terminal_transcripts':len(l),'values':{x:values[x] for x in ['0','1/4','1/2','3/4','1']},'limitations':['finite exact controls do not prove infinite transcript equality','finite stage illustration does not prove diagonal uncomputability','no empirical, formal kernel, or sequential classifier execution']},indent=2))
