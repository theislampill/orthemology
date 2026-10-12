#!/usr/bin/env python3
"""Exact finite controls for the signed bounded-energy proof.

These controls supplement, and do not replace, the ordinary universal proof.
No network, protected writes, numerical quadrature, or random sampling is used.
"""
from pathlib import Path
from fractions import Fraction
from collections import Counter
import hashlib
import json
import sys
import argparse
import sympy as S

HERE = Path(__file__).resolve().parent
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument("--retained-root",type=Path,default=HERE.parent,
                    help="Directory containing retained original input paths")
parser.add_argument("--output-dir",type=Path,default=HERE,
                    help="Write CONTROL_RESULTS.json here; permits nonmutating review")
args=parser.parse_args()
ROOT = args.retained_root.resolve()
OUT = args.output_dir.resolve()
OUT.mkdir(parents=True,exist_ok=True)
COUNTS = Counter()
CHECKS = []

def check(label, condition, category):
    if not condition:
        raise AssertionError(label)
    COUNTS[category] += 1
    CHECKS.append({"label": label, "category": category, "passed": True})

def eq(label, left, right=0, category="algebra"):
    check(label, S.simplify(S.expand(left-right)) == 0, category)

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

bindings = json.loads((HERE / "INPUT_BINDINGS.json").read_text())
for item in bindings["files"]:
    p = HERE / item["snapshot_path"]
    check(f"snapshot hash {p.name}", digest(p) == item["sha256"], "input_integrity")
    check(f"snapshot length {p.name}", p.stat().st_size == item["bytes"], "input_integrity")
    original = ROOT / item["original_path"]
    check(f"retained original hash {item['original_path']}",
          original.exists() and digest(original) == item["sha256"], "input_integrity")

x,y,t = S.symbols("x y t", real=True)
z,u,v,w = S.symbols("z u v w", positive=True)
qs = S.symbols("q0:3", real=True)
ps = S.symbols("p0:3", real=True)
atoms = [(S.Integer(0),S.Integer(1)), (S.Rational(1,2),S.Rational(1,2)), (S.Integer(1),S.Integer(0))]
weights = [S.Rational(1,2),S.Rational(1,3),S.Rational(1,6)]
energies = [-1,0,1]
eq("initial mass",sum(weights),1,"finite_channel")
for j,(a,b) in enumerate(atoms):
    eq(f"simplex column {j}",a+b,1,"finite_channel")
    eq(f"linear energy {j}",(x-y).subs({x:a,y:b}),energies[j],"finite_channel")

def expectation(values, coeffs):
    return sum(a*b for a,b in zip(values,coeffs))

def tilt(coeffs, factors):
    un = [a*b for a,b in zip(coeffs,factors)]
    total = sum(un)
    return [S.cancel(a/total) for a in un]

un = [weights[j]*z**energies[j] for j in range(3)]
Z = sum(un)
W = [S.cancel(a/Z) for a in un]
D = lambda expr: -z*S.diff(expr,z)
Ap = expectation(ps,un)
Lp = expectation(ps,W)
Lh = expectation(energies,W)
eq("arbitrary unnormalized observable hierarchy",D(Ap),-expectation([a*b for a,b in zip(ps,energies)],un),"finite_channel")
eq("arbitrary normalized observable hierarchy",D(Lp),-expectation([a*b for a,b in zip(ps,energies)],W)+Lh*Lp,"finite_channel")
eq("normalizer differential",D(Z),-expectation(energies,un),"finite_channel")
eq("normalizer logarithmic derivative",-D(Z)/Z,Lh,"finite_channel")
eq("all-time normalized mass",sum(W),1,"finite_channel")

square = expectation([q*q for q in qs],un)
eq("full square form exact",square,qs[0]**2/(2*z)+qs[1]**2/S.Integer(3)+z*qs[2]**2/S.Integer(6),"square_positivity")
check("all square coefficients strictly positive",all(a.is_positive for a in un),"square_positivity")
for i in range(3):
    for j in range(3):
        # Discriminant identity: no finite list of q values replaces this symbolic form.
        eq(f"square Gram entry {i},{j}",S.diff(square,qs[i],qs[j])/2,
           un[i] if i==j else 0,"square_positivity")

mons = [(a,b) for a in range(7) for b in range(7-a)]
for a,b in mons:
    vals = [ax**a*ay**b for ax,ay in atoms]
    obs = expectation(vals,W)
    eq(f"mixed moment hierarchy x^{a}y^{b}",D(obs),
       -expectation([e*p for e,p in zip(energies,vals)],W)+Lh*obs,"mixed_moments")

point = {z:S.Rational(1,2)}
eq("signed normalizer log2",Z.subs(point),S.Rational(17,12),"exact_values")
for j,answer in enumerate([S.Rational(12,17),S.Rational(4,17),S.Rational(1,17)]):
    eq(f"signed weight log2 {j}",W[j].subs(point),answer,"exact_values")
eq("mean x log2",expectation([a[0] for a in atoms],W).subs(point),S.Rational(3,17),"exact_values")
eq("mean y log2",expectation([a[1] for a in atoms],W).subs(point),S.Rational(14,17),"exact_values")
eq("mean energy log2",Lh.subs(point),-S.Rational(11,17),"exact_values")

c = S.symbols("c",real=True)
eq("no global shift makes signed linear nonnegative",(x-y+c).subs({x:-c-1,y:0}),-1,"signed_scope")
qvals = [(1-a[0]) for a in atoms]
eq("square domination actually fails at zero",D(expectation([a*a for a in qvals],un)).subs(z,1),S.Rational(1,2),"signed_scope")

nonlinear = x**3-3*y
nl = [nonlinear.subs({x:a,y:b}) for a,b in atoms]
check("nonlinear support energies",nl==[-3,-S.Rational(11,8),1],"nonlinear")
unun = [weights[j]*z**(8*nl[j]) for j in range(3)]
N = sum(unun)
NW = [S.cancel(a/N) for a in unun]
ND = lambda expr:-z*S.diff(expr,z)/8
np = expectation(ps,NW)
nh = expectation(nl,NW)
eq("arbitrary nonlinear normalized hierarchy",ND(np),-expectation([p*h for p,h in zip(ps,nl)],NW)+nh*np,"nonlinear")
eq("nonlinear unnormalized hierarchy",ND(expectation(ps,unun)),-expectation([p*h for p,h in zip(ps,nl)],unun),"nonlinear")
check("nonlinear square form has positive coefficients",all(a.is_positive for a in unun),"nonlinear")
eq("nonlinear globally signed witness family",nonlinear.subs({x:0,y:t}),-3*t,"nonlinear")

# Exact finite-support vanishing ideal and weighted scalar records, including zero mass.
ideal = [x+y-1,x*(2*x-1)*(x-1)]
for k,p in enumerate(ideal):
    vals=[p.subs({x:a,y:b}) for a,b in atoms]
    check(f"vanishing ideal generator {k}",vals==[0,0,0],"zero_mass")
    eq(f"zero square mass all time {k}",expectation([a*a for a in vals],un),0,"zero_mass")
    eq(f"null ideal times arbitrary observable {k}",expectation([a*b for a,b in zip(vals,ps)],un),0,"zero_mass")
for n in range(13):
    mn=expectation([qs[j]**2*S.Integer(energies[j])**n for j in range(3)],un)
    eq(f"weighted scalar moment derivative {n}",D(mn),-expectation([qs[j]**2*S.Integer(energies[j])**(n+1) for j in range(3)],un),"weighted_energy")
    eq(f"weighted energy boundary moments {n}",mn.subs(z,1),expectation([qs[j]**2*S.Integer(energies[j])**n for j in range(3)],weights),"weighted_energy")
    eq(f"weighted energy inverse tilt {n}",expectation([qs[j]**2*S.Integer(energies[j])**n*z**(-energies[j]) for j in range(3)],un),mn.subs(z,1),"weighted_energy")

# Local-to-global composition can be checked with arbitrary positive exponential bases.
start = [weights[j]*u**energies[j] for j in range(3)]
middle = [start[j]*(v/u)**energies[j] for j in range(3)]
end = [middle[j]*(w/v)**energies[j] for j in range(3)]
for j in range(3):
    eq(f"energy measure transition composition {j}",end[j],weights[j]*w**energies[j],"composition")
    eq(f"energy measure inverse transition {j}",middle[j]*(u/v)**energies[j],start[j],"composition")

st1=tilt(weights,[S.Rational(1,2)**h for h in energies])
st2=tilt(st1,[S.Integer(3)**h for h in energies])
direct=tilt(weights,[S.Rational(2,3)**(-h) for h in energies])
for j,answer in enumerate([S.Rational(4,11),S.Rational(4,11),S.Rational(3,11)]):
    eq(f"switching endpoint weight {j}",st2[j],answer,"switching")
    eq(f"switching integrated control {j}",st2[j],direct[j],"switching")
for a,b in mons:
    vals=[ax**a*ay**b for ax,ay in atoms]
    eq(f"switching moment x^{a}y^{b}",expectation(vals,st2),expectation(vals,direct),"switching")
shift = S.symbols("shift",positive=True)
for j in range(3):
    eq(f"normalized scalar shift cancellation {j}",(un[j]*shift)/(Z*shift),W[j],"composition")

# Generic parity cancellation and exact Taylor remainder kernels.
r,s = S.symbols("r s",positive=True)
for n in range(9):
    coeff=S.symbols(f"d0:{2*n+2}",real=True)
    forward=sum(coeff[k]*r**k/S.factorial(k) for k in range(2*n+2))
    backward=sum(coeff[k]*(-r)**k/S.factorial(k) for k in range(2*n+2))
    even=2*sum(coeff[2*k]*r**(2*k)/S.factorial(2*k) for k in range(n+1))
    eq(f"symmetric Taylor odd cancellation {n}",forward+backward,even,"taylor")
    # Reversal v=t-s makes backward remainder kernel (r-s)^(2n+1) on [0,r].
    eq(f"backward integral remainder sign {n}",-(-(r-s))**(2*n+1),(r-s)**(2*n+1),"taylor")
    eq(f"odd factorial ratio {n}",S.factorial(2*n)*S.factorial(2*n+2)/S.factorial(2*n+1)**2,S.Rational(2*n+2,2*n+1),"taylor")
    check(f"odd factorial ratio <=2 {n}",S.Rational(2*n+2,2*n+1)<=2,"taylor")

# Signed energy with bounded observed coordinate and an indeterminate hidden law.
Pminus = 1/(1+z**2) # z=exp(-t)
Pplus = z**2/(1+z**2)
meanx = S.cancel(Pplus-Pminus)
eq("two-point normalized mass",Pminus+Pplus,1,"hidden_law")
eq("two-point signed mean",meanx,-(1-z**2)/(1+z**2),"hidden_law")
eq("two-point mean hierarchy",D(meanx),-(1-meanx**2),"hidden_law")
eq("two-point normalizer",(1/z+z)/2,(z*z+1)/(2*z),"hidden_law")
for a in range(7):
    for b in range(7):
        y_moment=S.exp(S.Rational(b*b,2))
        m=y_moment*((-1)**a*Pminus+Pplus)
        nxt=y_moment*((-1)**(a+1)*Pminus+Pplus)
        eq(f"hidden mixed hierarchy {a},{b}",D(m),-nxt+meanx*m,"hidden_law")
        expected=y_moment*(1 if a%2==0 else meanx)
        eq(f"hidden common mixed formula {a},{b}",m,expected,"hidden_law")
for b in range(21):
    eq(f"lognormal sine cancellation integer {b}",S.exp(S.Rational(b*b,2)-2*S.pi**2)*S.sin(2*S.pi*b),0,"hidden_law")
eq("hidden densities differ at log y=1/4",S.Rational(1,2)*S.sin(2*S.pi*S.Rational(1,4))-(-S.Rational(1,2))*S.sin(2*S.pi*S.Rational(1,4)),1,"hidden_law")
check("hidden density perturbations remain nonnegative",S.Rational(1,2)>0,"hidden_law")

# Flat initial perturbation: exact recurrence, compact initial record, failed square.
positive_t=S.symbols("positive_t",positive=True)
flat=S.exp(-1/positive_t)
mass=1-flat/2
for n in range(7):
    An=(-1)**n*S.diff(mass,positive_t,n)
    nextAn=(-1)**(n+1)*S.diff(mass,positive_t,n+1)
    eq(f"flat unnormalized recurrence {n}",S.diff(An,positive_t),-nextAn,"flat_failure")
    eq(f"flat initial moment {n}",S.limit(An,positive_t,0,dir="+"),1 if n==0 else 0,"flat_failure")
    Ln=An/mass
    L1=-S.diff(mass,positive_t)/mass
    eq(f"flat normalized hierarchy {n}",S.diff(Ln,positive_t),-nextAn/mass+L1*Ln,"flat_failure")
eq("flat negative square formula",S.diff(mass,positive_t,2),flat*(2*positive_t-1)/(2*positive_t**4),"flat_failure")
eq("flat negative square at quarter",S.diff(mass,positive_t,2).subs(positive_t,S.Rational(1,4)),-64*S.exp(-4),"flat_failure")
check("flat square is strictly negative at quarter",(-64*S.exp(-4)).is_negative,"flat_failure")

# Unbounded Gaussian linear energy: exact ordinary moment formulas and hierarchy.
def normal_shifted_moment(n):
    return sum(S.factorial(n)*(-t)**(n-2*k)/(2**k*S.factorial(k)*S.factorial(n-2*k))
               for k in range(n//2+1))

gaussZ=S.exp(t*t/2)
eq("Gaussian linear normalizer logarithmic derivative",-S.diff(gaussZ,t)/gaussZ,-t,"gaussian_linear")
eq("Gaussian linear completion of square",-x*x/2-t*x,-(x+t)**2/2+t*t/2,"gaussian_linear")
for n in range(19):
    mn=normal_shifted_moment(n)
    nxt=normal_shifted_moment(n+1)
    eq(f"Gaussian linear hierarchy {n}",S.diff(mn,t),-nxt-t*mn,"gaussian_linear")
    initial=0 if n%2 else S.factorial2(n-1)
    eq(f"Gaussian initial moment {n}",mn.subs(t,0),initial,"gaussian_linear")
    An=gaussZ*mn
    eq(f"Gaussian linear unnormalized hierarchy {n}",S.diff(An,t),-gaussZ*nxt,"gaussian_linear")

# Gaussian negative quadratic energy has the sharp half-time boundary.
negZ=(1-2*t)**(-S.Rational(1,2))
neq=lambda n:S.factorial2(2*n-1)/(1-2*t)**n
eq("Gaussian negative quadratic normalizer",S.diff(negZ,t),negZ/(1-2*t),"gaussian_maximal_horizon")
eq("Gaussian negative quadratic density exponent",-x*x/2+t*x*x,-(S.Rational(1,2)-t)*x*x,"gaussian_maximal_horizon")
eq("Gaussian boundary density exponent is zero",(-x*x/2+t*x*x).subs(t,S.Rational(1,2)),0,"gaussian_maximal_horizon")
for n in range(13):
    mn=neq(n)
    nxt=neq(n+1)
    eq(f"Gaussian negative quadratic even hierarchy {n}",S.diff(mn,t),nxt-neq(1)*mn,"gaussian_maximal_horizon")
    eq(f"Gaussian negative quadratic unnormalized {n}",S.diff(negZ*mn,t),negZ*nxt,"gaussian_maximal_horizon")
    eq(f"Gaussian negative quadratic initial {n}",mn.subs(t,0),S.factorial2(2*n-1),"gaussian_maximal_horizon")
check("Gaussian second moment diverges at half",S.limit(neq(1),t,S.Rational(1,2),dir="-")==S.oo,"gaussian_maximal_horizon")
check("Gaussian partition diverges at half",S.limit(negZ,t,S.Rational(1,2),dir="-")==S.oo,"gaussian_maximal_horizon")

# Unbounded signed energy: inherited geometric finite-horizon control.
et=S.symbols("et",positive=True)
geoZ=1/(2-et)
geoMean=-et/(2-et)
GD=lambda f:et*S.diff(f,et)
eq("geometric negative logarithmic derivative",-GD(geoZ)/geoZ,geoMean,"unbounded_horizon")
eq("geometric initial normalization",geoZ.subs(et,1),1,"unbounded_horizon")
eq("geometric initial mean",geoMean.subs(et,1),-1,"unbounded_horizon")
check("geometric mean diverges at boundary",S.limit(geoMean,et,2,dir="-")==-S.oo,"unbounded_horizon")

result={
    "status":"PASS",
    "check_count":len(CHECKS),
    "categories":dict(sorted(COUNTS.items())),
    "python":sys.version.split()[0],
    "sympy":S.__version__,
    "scope":"Exact finite controls supplement an ordinary universal proof. They do not establish infinite-dimensional validity by sampling.",
    "result_sha256":digest(HERE/"RESULT.md"),
    "script_sha256":digest(Path(__file__).resolve()),
    "input_bindings_sha256":digest(HERE/"INPUT_BINDINGS.json"),
    "checks":CHECKS,
}
(OUT/"CONTROL_RESULTS.json").write_text(json.dumps(result,indent=2)+"\n")
print(f"PASS: {len(CHECKS)} exact checks")
for k,n in sorted(COUNTS.items()):
    print(f"  {k}: {n}")
print(f"RESULT.md sha256 {result['result_sha256']}")
