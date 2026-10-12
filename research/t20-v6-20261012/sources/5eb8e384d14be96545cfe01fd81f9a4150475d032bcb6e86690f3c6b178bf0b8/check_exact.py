import sympy as S
import json
from pathlib import Path
checks=[]
def zero(name,z):
    z=S.factor(z)
    assert z==0,(name,z)
    checks.append(name)
w,x,y,a,b,c=S.symbols('w x y a b c',real=True)
D=b-a*a; s=(c-a*b)/D; p=(a*c-b*b)/D
zero('discriminant',s*s-4*p-((c-3*a*b+2*a**3)**2/D**2+4*D))
zero('mean_between_roots',a*a-s*a+p+D)
zero('second_recovery',s*a-p-b)
zero('third_recovery',s*b-p*a-c)
m=[w*x**i+(1-w)*y**i for i in range(7)]
M=S.Matrix(m[1:4]); J=M.jacobian([w,x,y]); Ginv=S.diag(w*(1-w),1/w,1/(1-w))
B=J*Ginv*J.T
zero('jacobian',J.det()-w*(1-w)*(x-y)**4)
for i in range(1,4):
 for j in range(1,4):
  zero(f'cometric_{i}_{j}', B[i-1,j-1]-(i*j*m[i+j-2]+m[i+j]-m[i]*m[j]))
zero('cometric_determinant',B.det()-w*w*(1-w)**2*(x-y)**8)
sub={a:m[1],b:m[2],c:m[3]}
zero('support_sum',s.subs(sub)-(x+y))
zero('support_product',p.subs(sub)-x*y)
for n in range(5): zero(f'recurrence_{n}',m[n+2]-(x+y)*m[n+1]+x*y*m[n])
wdot=-w*(x*x/2-m[2]/2)
v=S.Matrix([wdot,-x,-y]); dm=J*v
for i in range(1,4): zero(f'quadratic_ode_{i}',dm[i-1]+i*m[i]+(m[i+2]-m[2]*m[i])/2)
zero('dissipation',dm[1]/2+m[2]+(m[4]-m[2]**2)/4)
for n,expected in [(0,0),(1,0),(2,0),(3,S.Rational(3,2))]:
 mu=(S.Integer(-1)**n+1)/2; nu=S.Rational(1,5)*S.Integer(-2)**n+S.Rational(4,5)*S.Rational(1,2)**n
 zero(f'omission_control_{n}',mu-nu-expected)
report={'status':'PASS','exact_checks':len(checks),'checks':checks,'verification':'SymPy exact identities; no kernel or empirical certification'}
Path(__file__).with_name('EXACT_CHECKS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
