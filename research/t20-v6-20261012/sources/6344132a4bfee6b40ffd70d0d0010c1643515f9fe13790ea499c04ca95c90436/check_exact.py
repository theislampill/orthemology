from pathlib import Path
import hashlib,json
import sympy as s
root=Path(__file__).resolve().parent
binding=json.loads((root/'INPUT_BINDING.json').read_text())
p=Path(binding['path'])
assert hashlib.sha256(p.read_bytes()).hexdigest()==binding['sha256']
z=s.symbols('z',positive=True)
a=z*z
correct=(1+a)/(2+a)
wrong=2*z/(1+2*z)
assert s.simplify((correct-wrong)*(2+a)*(1+2*z)-(1-z)**2)==0
weights=[s.Rational(1,3)]*3
factors=[s.Integer(1),s.Integer(1),a]
A=sum(w*f for w,f in zip(weights,factors))
assert s.simplify((weights[1]*factors[1]+weights[2]*factors[2])/A-correct)==0
assert s.simplify(s.Rational(2,3)*(1+a)/2+s.Rational(1,3)-A)==0
# Symbolic log densities at the positive normalised weights; use defining identities.
P=[w*f/A for w,f in zip(weights,factors)]
assert s.simplify(sum(P)-1)==0
# For each label log(P/a_prior)=log(factor)-log(A), I=-log(factor).
KL=sum(p*(s.log(f)-s.log(A)) for p,f in zip(P,factors))
IC=sum(p*(-s.log(f)) for p,f in zip(P,factors))
assert s.simplify(KL+IC+s.log(A))==0
# Finite grouped effective cost retains the exact partition function.
nu=[s.Rational(1,3),s.Rational(2,3)]
r=[s.Integer(1),(1+a)/2]
assert s.simplify(sum(v*f for v,f in zip(nu,r))-A)==0
assert s.simplify(nu[1]*r[1]/A-correct)==0
out={'status':'PASS','exact_algebra_controls':7,'predecessor_hash_controls':1,'scope':'Finite symbolic identities supplement the written measure and entropy proof; no kernel or independent-review claim.'}
(root/'EXACT_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
