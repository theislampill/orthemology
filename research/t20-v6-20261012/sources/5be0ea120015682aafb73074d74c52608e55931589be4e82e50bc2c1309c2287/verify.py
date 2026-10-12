#!/usr/bin/env python3
"""Exact controls for RESULT.md; general proofs remain ordinary mathematics."""
from pathlib import Path
import hashlib
import json
import sympy as s
Q=s.Rational
count=0

def check(label, condition):
    global count
    assert bool(condition),label
    count+=1
    print('PASS:',label)

def equal(label,a,b):
    if isinstance(a,s.MatrixBase): check(label,a.shape==b.shape and all(s.simplify(x)==0 for x in a-b))
    else: check(label,s.simplify(s.expand_log(a-b,force=True))==0)

def D(p,q,mu): return sum((x-y)**2/w for x,y,w in zip(p,q,mu))/2

def risk(p,q,mu): return sum(p[i]*D(s.eye(len(p))[:,i],q,mu) for i in range(len(p)))

def KL(p,q): return sum(x*s.log(x/y) for x,y in zip(p,q))

def quartic(p,q,mu): return sum(w*((x/w)**4-(y/w)**4-4*(y/w)**3*((x-y)/w)) for x,y,w in zip(p,q,mu))

q=s.Matrix([Q(1,4),Q(1,4),Q(1,2)])
pplus=s.Matrix([Q(3,8),Q(3,8),Q(1,4)])
pminus=s.Matrix([Q(1,8),Q(1,8),Q(3,4)])
Lplus=s.Matrix([Q(3,4),Q(3,4),Q(1,4)])
Lminus=s.ones(3,1)-Lplus
K=s.Matrix([[1,1,0],[0,0,1]])
R=s.Matrix([[Q(1,2),0],[Q(1,2),0],[0,1]])
mu=s.ones(3,1);nu=K*mu
for label,L,p in [('plus',Lplus,pplus),('minus',Lminus,pminus)]:
    check(label+' strictly positive likelihood',all(0<x<1 for x in L))
    raw=q.multiply_elementwise(L);z=sum(raw)
    equal(label+' observation probability',z,Q(1,2))
    equal(label+' exact Bayes posterior',raw/z,p)
    equal(label+' fine Brier regret',D(p,q,mu),Q(3,64))
    equal(label+' reset coarse Brier regret',D(K*p,K*q,s.ones(2,1)),Q(1,16))
    equal(label+' KL equality',KL(K*p,K*q),KL(p,q))
    equal(label+' KL expression',KL(p,q),Q(3,4)*s.log(Q(3,2))+Q(1,4)*s.log(Q(1,2)))
    equal(label+' reference-transported regret',D(K*p,K*q,nu),Q(3,64))
    equal(label+' reverse recovers posterior',R*K*p,p)
    equal(label+' normalization commutes',K*raw/sum(K*raw),K*(raw/z))
    equal(label+' fixed block conditional',p[0]/(p[0]+p[1]),Q(1,2))
equal('posterior martingale',(pplus+pminus)/2,q)
equal('reverse recovers prior',R*K*q,q)
equal('reverse recovers reference',R*K*mu,mu)
a=s.symbols('a');p=s.Matrix([a,a,1-2*a])
equal('reverse recovers whole stated submodel',R*K*p,p)
v=pplus-q
equal('fine Hessian energy',sum(x*x for x in v),Q(3,32))
equal('reset coarse Hessian energy',sum(x*x for x in K*v),Q(1,8))
check('Hessian contraction fails',sum(x*x for x in K*v)>sum(x*x for x in v))
equal('fine prior Bayes risk',risk(q,q,mu),Q(5,16))
equal('fine expected posterior risk',(risk(pplus,pplus,mu)+risk(pminus,pminus,mu))/2,Q(17,64))
equal('transported prior Bayes risk',risk(K*q,K*q,nu),Q(3,16))
equal('transported expected posterior risk',(risk(K*pplus,K*pplus,nu)+risk(K*pminus,K*pminus,nu))/2,Q(9,64))
equal('absolute risk discrepancy persists',risk(q,q,mu)-risk(K*q,K*q,nu),Q(1,8))
# Genuine observation garbling: keep truth coordinates, flip Y with probability 1/4.
rplus=Q(3,4)*pplus+Q(1,4)*pminus
rminus=Q(1,4)*pplus+Q(3,4)*pminus
Ifine=(D(pplus,q,mu)+D(pminus,q,mu))/2
Igarbled=(D(rplus,q,mu)+D(rminus,q,mu))/2
conditional_gap=(Q(3,4)*D(pplus,rplus,mu)+Q(1,4)*D(pminus,rplus,mu)+Q(1,4)*D(pplus,rminus,mu)+Q(3,4)*D(pminus,rminus,mu))/2
equal('fixed-truth noisy-signal information',Igarbled,Q(3,256))
equal('fixed-truth exact conditional Bregman gap',Ifine-Igarbled,conditional_gap)
check('fixed-truth noisy-signal monotonicity',Igarbled<Ifine)
equal('fixed-truth constant-signal information',D((pplus+pminus)/2,q,mu),0)
# Three-object recovery guard.
mu_bad=s.Matrix([1,2,1]);nu_bad=K*mu_bad
equal('pair-only recovery fine divergence',D(pplus,q,mu_bad),Q(11,256))
equal('pair-only recovery coarse divergence',D(K*pplus,K*q,nu_bad),Q(1,24))
equal('pair-only recovery strict gap',D(pplus,q,mu_bad)-D(K*pplus,K*q,nu_bad),Q(1,768))
check('pair-only reverse does not recover reference',R*K*mu_bad!=mu_bad)
# Arbitrary weighted Bregman guard.
u=s.Matrix([Q(19,100),Q(1,100),Q(4,5)])
w=s.Matrix([Q(31,100),Q(29,100),Q(2,5)])
equal('quartic positive coherent p mass',sum(u),1)
equal('quartic positive coherent q mass',sum(w),1)
equal('quartic weighted Bregman increase',quartic(K*u,K*w,nu)-quartic(u,w,mu),Q(921,1562500))
# Genuine stochastic contraction and exact variance accounting.
J=s.Matrix([[Q(3,4),Q(1,4)],[Q(1,4),Q(3,4)]])
P=K*pplus;Qp=K*q;M=s.Matrix([2,1]);N=J*M;delta=P-Qp
variance=sum(N[j]*(sum(J[j,i]*M[i]/N[j]*(delta[i]/M[i])**2 for i in range(2))-(sum(J[j,i]*delta[i] for i in range(2))/N[j])**2) for j in range(2))
equal('stochastic exact weighted variance gap',2*(D(P,Qp,M)-D(J*P,J*Qp,N)),variance)
check('stochastic weighted contraction',D(J*P,J*Qp,N)<D(P,Qp,M))
# Ambient perspective split and equal radial cancellation, with s != t.
def ambient_D(x,y,ref):
    def F(v): return sum(v[i]**2/ref[i] for i in range(len(v)))/(2*sum(v))+sum(v)**2/2
    sy=sum(y);fy=sum(y[i]**2/ref[i] for i in range(len(y)))
    grad=s.Matrix([y[i]/(ref[i]*sy)-fy/(2*sy**2)+sy for i in range(len(y))])
    return F(x)-F(y)-grad.dot(x-y)
x=Q(2,3)*pplus;y=Q(4,5)*q
equal('ambient divergence split',ambient_D(x,y,mu),Q(2,3)*D(pplus,q,mu)+(Q(2,3)-Q(4,5))**2/2)
equal('ambient sufficient weighted equality',ambient_D(K*x,K*y,nu),ambient_D(x,y,mu))
# Exact source-byte bindings, including reviewer-origin guards.
ledger=json.loads(Path(__file__).with_name('SOURCE_LEDGER.json').read_text())
root=Path(__file__).resolve().parents[1]
for src in ledger['local_sources']:
    data=(root/src['path']).read_bytes()
    check('source SHA-256 '+src['path'],hashlib.sha256(data).hexdigest()==src['sha256'])
    if src.get('git_blob_sha'):
        blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        check('pinned Git blob '+src['path'],blob==src['git_blob_sha'])
print('PASS:',count,'exact controls; general proofs in RESULT.md')
