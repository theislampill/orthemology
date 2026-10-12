import sympy as s, json
from pathlib import Path
x,y,u,z,t=s.symbols('x y u z t', real=True)
checks=[]
def check(name,expr):
    assert s.expand(expr)==0,(name,expr)
    checks.append(name)
for m in (3,4,5):
    h=x*x+(y-t*x**m)**2
    check(f'pullback_energy_{m}',h.subs({x:u,y:z+t*u**m},simultaneous=True)-u*u-z*z)
    check(f'inverse_first_{m}',(y-t*x**m).subs({x:u,y:z+t*u**m},simultaneous=True)-z)
    for i,j in ((0,0),(1,0),(0,1),(1,1),(2,1),(0,3)):
        q=x**i*(y-t*x**m)**j
        check(f'characteristic_{m}_{i}_{j}',s.diff(q,t)+x**m*s.diff(q,y))
    # Gaussian initial density: tilted base has precision 1+t in each coordinate.
    def gauss(k):
        return 0 if k%2 else s.factorial2(k-1)/(2*(1+t))**(k//2) if k else s.Integer(1)
    def avg(p):
        return s.expand(sum(c*gauss(a)*gauss(b) for (a,b),c in s.Poly(s.expand(p),u,z).terms()))
    def L(p): return avg(p.subs({x:u,y:z+t*u**m},simultaneous=True))
    for i,j in ((1,0),(0,1),(0,2),(1,1)):
        p=x**i*y**j
        expr=s.diff(L(p),t)-L(x**m*s.diff(p,y))+L(h*p)-L(h)*L(p)
        assert s.cancel(expr)==0,(m,i,j,expr)
        checks.append(f'normalised_hierarchy_{m}_{i}_{j}')
result={'algebraic_checks':len(checks),'checks':checks,'scope':'finite symbolic controls, not universal proof or kernel verification'}
Path(__file__).with_name('EXACT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
