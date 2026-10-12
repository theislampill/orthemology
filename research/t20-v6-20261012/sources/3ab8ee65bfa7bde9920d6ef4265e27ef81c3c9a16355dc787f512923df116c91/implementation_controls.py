#!/usr/bin/env python3
"""Independent implementation checks; imports implementation, not author tests."""
import argparse, hashlib, importlib.util, json, math, sys
sys.dont_write_bytecode = True
from pathlib import Path
import numpy as np
from scipy.linalg import expm

p=argparse.ArgumentParser();p.add_argument('--author-dir',required=True);p.add_argument('--output',required=True);args=p.parse_args()
path=Path(args.author_dir)/'gaussian_step.py';spec=importlib.util.spec_from_file_location('review_gaussian_step',path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
step=mod.gaussian_step;checks=[]
def check(name,ok,evidence=None):
    if not bool(ok):raise RuntimeError(f'FAILED: {name}: {evidence}')
    checks.append({'name':name,'passed':True,'evidence':evidence})
for pos,name in enumerate(['mean','covariance','target_mean','target_covariance']):
    values=[np.array([0.]),np.array([[1.]]),np.array([0.]),np.array([[1.]]),.1]
    values[pos]=values[pos].astype(complex)+7j
    try:step(*values)
    except (ValueError,TypeError):rejected=True
    else:rejected=False
    check('reject_complex_'+name,rejected)
for h in [1+1j,np.complex128(1+0j),[.1],np.array([.1]),float('nan'),0.,-1.]:
    try:step([0.],[[1.]],[0.],[[1.]],h)
    except (ValueError,TypeError):rejected=True
    else:rejected=False
    check('reject_invalid_step_'+repr(h),rejected)
# Distinct rank-deficient, noncommuting exact fixture.
r=step([3.,-1.],[[1.,1.],[1.,1.]],[1.,-2.],[[1.,0.],[0.,.5]],math.log(2))
check('independent_rational_covariance',np.allclose(r['covariance'],np.array([[130,8],[8,67]])/131,atol=1e-14))
# Recompute exact mean by matrix arithmetic with rational fixture quantities.
Sd=np.array([[1.,1/8],[1/8,17/32]]);Sr=np.array([[130.,8],[8,67]])/131
mean=np.array([1.,-2.])+.5*Sr@np.linalg.solve(Sd,np.array([1.,.25]))
check('independent_rational_mean',np.allclose(r['mean'],mean,atol=1e-14),mean.tolist())
# Finite positive h close to zero must regularize a zero covariance.
r=step([1.],[[0.]],[0.],[[1.]],1e-12)
check('small_step_singular_regularization',r['covariance'][0,0]>0 and np.isfinite(r['covariance'][0,0]),float(r['covariance'][0,0]))
# Independent matrix exponential oracle on well-conditioned random fixtures.
rng=np.random.default_rng(48723);maxerr=0.
for i in range(24):
    d=2+i%3;W=rng.normal(size=(d,d));T=W@W.T+.6*np.eye(d);V=rng.normal(size=(d,d-1));S=V@V.T+.2*np.eye(d)
    m=rng.normal(size=d);g=rng.normal(size=d);h=.03+.8*rng.random();copies=[v.copy() for v in [m,S,g,T]]
    r=step(m,S,g,T,h);E=expm(-h*np.linalg.inv(T));D=T+E@(S-T)@E
    precision=math.exp(-h)*np.linalg.inv(D)+(1-math.exp(-h))*np.linalg.inv(T)
    C=np.linalg.inv(precision);mm=g+C@(math.exp(-h)*np.linalg.solve(D,E@(m-g)))
    err=max(np.max(abs(r['covariance']-C)),np.max(abs(r['mean']-mm)));maxerr=max(maxerr,float(err))
    if err>2e-11:raise RuntimeError('matrix exponential oracle mismatch')
    if any(not np.array_equal(v,old) for v,old in zip([m,S,g,T],copies)):raise RuntimeError('input mutation')
check('24_independent_expm_oracles_and_input_immutability',True,{'max_abs_error':maxerr})
out={'status':'PASS','count':len(checks),'implementation_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'checks':checks,'limit':'Finite regression/numerical checks, not an error certificate for all inputs.'}
Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(f'PASS {len(checks)} implementation controls')
