#!/usr/bin/env python3
"""Independent exact controls, no imports from the author checker.
Finite symbolic/rational checks supplement the all-dimension analytic review.
"""
from pathlib import Path
from functools import lru_cache
import hashlib, json, argparse
import sympy as s
HERE = Path(__file__).resolve().parent
AUTHOR = HERE / 'inputs' / 'author'
checks=[]; details={}
def ck(name, condition):
    if not bool(condition): raise AssertionError(name)
    checks.append(name)
def zmat(a): return all(s.expand(x)==0 for x in a)
def block(rows): return s.BlockMatrix(rows).as_explicit()
def covariance(B,S):
    k=B.cols
    return block([[s.eye(k),B.T],[B,B*B.T+S]])
def precision(B,W):
    k=B.cols
    return block([[s.eye(k)+B.T*W*B,-B.T*W],[-W*B,W]])
def data(B,S,Bt,W):
    k=B.cols; m=B.rows; n=k+m; delta=B-Bt
    N=delta.T*W*delta; M=-Bt.T*W*delta
    P=(N+M+M.T)/3
    Sig=covariance(B,S); Q=precision(Bt,W); Pb=s.diag(P,s.zeros(m))
    # Compared with the advertised field, never imported from it.
    F=2*s.eye(n)+Sig-Q*Sig-Sig*Q-Sig*Q*Sig+Pb*Sig+Sig*Pb+Sig*Pb*Sig
    # Independently derived in conditional coordinates (y,e=z-By).
    Bd=-B-B*P-(s.eye(m)+B*Bt.T)*W*delta+S*W*(2*Bt-B)
    Sd=2*(s.eye(m)+B*B.T)+S-(s.eye(m)+B*Bt.T)*W*S-S*W*(s.eye(m)+Bt*B.T)-S*W*S
    return Sig,Q,M,N,P,Pb,F,Bd,Sd

def symbolic_controls():
    B=s.Matrix(2,2,s.symbols('b0:4')); Bt=s.Matrix(2,2,s.symbols('c0:4'))
    a,b,c,u,v,w=s.symbols('a b c u v w'); S=s.Matrix([[a,b],[b,c]]); W=s.Matrix([[u,v],[v,w]])
    Sig,Q,M,N,P,Pb,F,Bd,Sd=data(B,S,Bt,W)
    ck('symbolic k2 m2 nonsymmetric conditional score M', not zmat(M-M.T))
    ck('symbolic k2 m2 entire observed block cancels', zmat(F[:2,:2]))
    ck('symbolic k2 m2 independent conditional B equation', zmat(F[2:,:2]-Bd))
    ck('symbolic k2 m2 independent conditional S equation', zmat(F[2:,2:]-Bd*B.T-B*Bd.T-Sd))
    J=block([[s.eye(2),s.zeros(2)],[-B,s.eye(2)]])
    ck('symbolic k2 m2 conditional covariance congruence', zmat(J*Sig*J.T-s.diag(s.eye(2),S)))
    Pw=N/3; Pbw=s.diag(Pw,s.zeros(2))
    Fw=2*s.eye(4)+Sig-Q*Sig-Sig*Q-Sig*Q*Sig+Pbw*Sig+Sig*Pbw+Sig*Pbw*Sig
    ck('symbolic omitted-flux error is minus M plus M transpose', zmat(Fw[:2,:2]+M+M.T))
    ck('symbolic omitted-flux error is genuinely nonzero', not zmat(Fw[:2,:2]))


def gaussian_expectation(poly,x,Sig):
    @lru_cache(None)
    def moment(idx):
        if not idx: return s.Integer(1)
        if len(idx)%2: return s.Integer(0)
        i=idx[0]
        return sum(Sig[i,idx[j]]*moment(idx[1:j]+idx[j+1:]) for j in range(1,len(idx)))
    out=s.Integer(0)
    for powers,coeff in s.Poly(s.expand(poly),*x).terms():
        idx=tuple(i for i,p in enumerate(powers) for _ in range(p))
        out+=coeff*moment(idx)
    return s.factor(out)

def positive_controls():
    B=s.Matrix([[1,2,-1],[2,-1,3]]); Bt=s.Matrix([[0,1,2],[-1,2,1]])
    S=s.Matrix([[3,1],[1,2]]); T=s.Matrix([[2,-1],[-1,4]]); W=T.inv()
    Sig,Q,M,N,P,Pb,F,Bd,Sd=data(B,S,Bt,W); k=3; m=2; n=5
    ck('positive rational noncommuting conditional covariances', not zmat(S*T-T*S))
    ck('positive rational nonsymmetric observed score', not zmat(M-M.T))
    Sinv=precision(B,S.inv()); C=Q-Sinv-Pb
    ck('positive rational block precision is an actual inverse', zmat(Sinv*Sig-s.eye(n)))
    x=s.Matrix(s.symbols('x0:5')); y=x[:k,0]; z=x[k:,0]
    yy=s.Matrix(y); zz=s.Matrix(z)
    score=((zz-Bt*yy).T*W*(zz-Bt*yy)-(zz-B*yy).T*S.inv()*(zz-B*yy))[0]/2
    phi=(yy.T*P*yy)[0]/2
    f=s.expand(score-phi)
    v=-s.Matrix([s.diff(f,xi) for xi in x]); Ef=gaussian_expectation(f,x,Sig); alpha=-f+Ef
    rho_gradient=-Sinv*x
    pde=s.expand(-sum(s.diff(v[i],x[i])+v[i]*rho_gradient[i] for i in range(n))+alpha)
    density=-s.trace(Sinv*F)/2+(x.T*Sinv*F*Sinv*x)[0]/2
    ck('positive rational full-density polynomial from spatial derivatives', s.expand(pde-density)==0)
    ck('positive rational reaction centered by independent Wick integration', gaussian_expectation(alpha,x,Sig)==0)
    action=gaussian_expectation((v.T*v)[0]+alpha**2,x,Sig)
    trace_action=s.trace(C*Sig*C)+s.trace(C*Sig*C*Sig)/2
    ck('positive rational full action from independent Wick integration', s.factor(action-trace_action)==0)
    Ed=s.trace(W*Sd)/2+s.trace((B-Bt).T*W*Bd)-s.trace(S.inv()*Sd)/2
    ck('positive rational direct conditional KL dissipation', s.factor(Ed+action)==0)
    raw=Q-Sinv
    raw_action=s.trace(raw*Sig*raw)+s.trace(raw*Sig*raw*Sig)/2
    ck('positive rational full orthogonal projection cost identity', s.factor(raw_action-action-s.Rational(3,2)*s.trace(P*P))==0)
    R=Q-Pb
    smooth=s.trace(R*Sig*R)-2*s.trace(R)+s.trace(R*Sig*R*Sig)/2-s.trace(R*Sig)+s.Rational(n,2)
    ck('positive rational direct inverse covariance pole decomposition', s.factor(action-s.trace(Sinv)-smooth)==0)
    ck('positive rational conditional inverse trace decomposition', s.factor(s.trace(Sinv)-k-s.trace((s.eye(m)+B*B.T)*S.inv()))==0)
    # Conditional score at fixed z; differentiating score only after substitution would be wrong.
    ee=s.Matrix(s.symbols('e0:2')); subst=dict(zip(zz,B*yy+ee))
    Egrad=[]
    for i in range(k):
        Egrad.append(gaussian_expectation(s.diff(score,x[i]).subs(subst, simultaneous=True),ee,S))
    ck('positive rational conditional observed spatial score', zmat(s.Matrix(Egrad)-M*yy))
    Escore=gaussian_expectation(score.subs(subst, simultaneous=True),ee,S)
    ck('positive rational conditional score Hessian', zmat(s.hessian(Escore,list(yy))-N))
    details['positive_control']={'k':k,'m':m,'action':str(action),'observed_score_nonsymmetric':True}


def singular_controls():
    B=s.Matrix([[1,-2],[2,1],[-1,3]]); Bt=s.Matrix([[2,1],[0,-1],[1,2]])
    T=s.Matrix([[4,1,0],[1,3,1],[0,1,2]]); W=T.inv(); k=2; m=3
    # Rational Householder rotation: both range and nullspace are non-coordinate.
    h=s.Matrix([1,2,3]); O=s.eye(3)-2*h*h.T/(h.T*h)[0]
    ck('rotated controls use an exact orthogonal noncoordinate basis', zmat(O.T*O-s.eye(3)) and all(O[i,j]!=0 for i in range(3) for j in range(3)))
    t=s.symbols('t')
    for rank in [0,1,2]:
        E=s.diag(*([2,5][:rank]+[0]*(3-rank))); S0=O*E*O.T
        U=O[:,:rank]; V=O[:,rank:]; r=3-rank
        Sig,Q,M,N,P,Pb,F,Bd,Sd=data(B,S0,Bt,W)
        AK=2*V.T*(s.eye(m)+B*B.T)*V
        ck(f'rotated rank{rank} kernel basis', zmat(S0*V))
        ck(f'rotated rank{rank} full observed tangent', zmat(F[:k,:k]))
        ck(f'rotated rank{rank} independent Schur tangent', zmat(Sd-(F[k:,k:]-Bd*B.T-B*Bd.T)))
        ck(f'rotated rank{rank} strict nullspace inflow', zmat(V.T*Sd*V-AK) and all(AK[:j,:j].det()>0 for j in range(1,r+1)))
        d0=(U.T*S0*U).det()*AK.det() if rank else AK.det()
        detpoly=s.Poly((S0+t*Sd).det(),t)
        ck(f'rotated rank{rank} determinant leading coefficient', all(detpoly.nth(j)==0 for j in range(r)) and detpoly.nth(r)==d0)
        # Exact inverse Laurent coefficient of a first-order covariance jet.
        invjet=(S0+t*Sd).inv()
        residue=invjet.applyfunc(lambda a:s.limit(t*a,t,0))
        ck(f'rotated rank{rank} inverse Laurent residue', zmat(residue-V*AK.inv()*V.T))
        pole=s.trace((s.eye(m)+B*B.T)*residue)
        ck(f'rotated rank{rank} target independent dissipation pole', pole==s.Rational(r,2))
        d=details.setdefault('singular_controls',[])
        d.append({'rank':rank,'nullity':r,'determinant_leading_coefficient':str(d0),'dissipation_pole':str(pole)})
    Sig,Q,M,N,P,Pb,F,Bd,Sd=data(Bt,T,Bt,W)
    ck('target stationary in independent coordinate equations', zmat(P) and zmat(Bd) and zmat(Sd) and zmat(F))


def source_controls():
    freeze=json.loads((AUTHOR/'AUTHOR_FREEZE.json').read_text())
    for name,digest in freeze['files'].items():
        ck('author freeze '+name,hashlib.sha256((AUTHOR/name).read_bytes()).hexdigest()==digest)
    bindings=json.loads((AUTHOR/'INPUT_BINDINGS.json').read_text())
    for binding in bindings:
        ck('predecessor snapshot '+binding['original'],hashlib.sha256((AUTHOR/binding['snapshot']).read_bytes()).hexdigest()==binding['sha256'])
    details['author_result_sha256']=hashlib.sha256((AUTHOR/'RESULT.md').read_bytes()).hexdigest()
    details['author_checker_sha256']=hashlib.sha256((AUTHOR/'verify.py').read_bytes()).hexdigest()

if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--output',default=str(HERE/'INDEPENDENT_CHECKS.json')); args=parser.parse_args()
    symbolic_controls(); positive_controls(); singular_controls(); source_controls()
    result={'status':'pass','count':len(checks),'controls':checks,'details':details,'scope':'Finite exact controls supplement the source-bound ordinary mathematical proof review; no formal proof, novelty certification, or programme closure.'}
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'pass','count':len(checks)}))
