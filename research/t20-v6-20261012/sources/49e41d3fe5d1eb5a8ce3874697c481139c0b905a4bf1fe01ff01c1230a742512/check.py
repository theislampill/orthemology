import sympy as S,json,pathlib
s,x=S.symbols('s x', positive=True)
v=1-5*s**5; a=s-s**6; V=(x**4-a*x**5)**2/2; b=-S.diff(V,x); X=1/s
checks=[]
def ck(name,e):
 assert S.factor(e)==0,(name,S.factor(e))
 checks.append(name)
ck('exact gradient characteristic',b.subs(x,X)-v/s**2)
ck('initial state',X.subs(s,S.Rational(1,2))-2)
ck('trajectory loss',V.subs(x,X)-s**2/2)
ck('total energy derivative',-v*S.diff(V.subs(x,X),s)+s*v)
ck('partial-time energy term',(-v*S.diff(V,s)).subs(x,X)-v*(1-6*s**5)/s**4)
ck('gradient-square term',S.diff(V,x).subs(x,X)**2-v**2/s**4)
ck('energy chain rule',(-v*S.diff(V,s)).subs(x,X)-S.diff(V,x).subs(x,X)**2+s*v)
ck('endpoint coercive potential',V.subs(s,0)-x**8/2)
ck('initial loss',V.subs({s:S.Rational(1,2),x:2})-S.Rational(1,8))
ck('schedule speed minimum value',v.subs(s,S.Rational(1,2))-S.Rational(27,32))
ck('finite time upper bound',S.Rational(1,2)/S.Rational(27,32)-S.Rational(16,27))
# Arbitrary differentiable observable verifies the Dirac hierarchy chain rule.
p=S.Function('p')
ck('arbitrary Dirac observable chain rule',-v*S.diff(p(1/s),s)-v/s**2*S.Subs(S.diff(p(x),x),x,1/s))
out={'status':'PASS','count':len(checks),'checks':checks,'level':'Exact SymPy algebra, not kernel verification or independent review'}
pathlib.Path(__file__).with_name('CHECK_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
