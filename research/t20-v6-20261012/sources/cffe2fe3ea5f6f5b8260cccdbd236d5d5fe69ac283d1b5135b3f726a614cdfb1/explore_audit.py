from fractions import Fraction as F
from itertools import product
from scipy.optimize import linprog
# cells y,a = (0,0),(0,1),(1,0),(1,1)
def bsc(q,r=F(4,5)):return ((1-q)*r,(1-q)*(1-r),q*(1-r),q*r)
def rect(m,p1,p0):return ((1-m)*(1-p0),m*(1-p1),(1-m)*p0,m*p1)
ps=[('skip',0),('skip',1)]+[('query',a,b) for a,b in product([0,1],repeat=2)]
def value(pol,j,c):
 return sum(j[y*2+a]*(c+(pol[a+1]!=y) if pol[0]=='query' else (pol[1]!=y)) for y,a in product([0,1],repeat=2))
def lp(models,c):
 vals=[[value(pol,m,c) for pol in ps] for m in models]
 import numpy as np
 res=linprog([0]*6+[1],A_ub=[[float(x) for x in v]+[-1] for v in vals],b_ub=[0]*len(vals),A_eq=[[1]*6+[0]],b_eq=[1],bounds=[(0,None)]*6+[(None,None)],method='highs')
 print('value',F(float(res.fun)).limit_denominator(),[(ps[i],F(float(x)).limit_denominator()) for i,x in enumerate(res.x[:-1]) if x>1e-8], 'dual', [(i,F(float(-x)).limit_denominator()) for i,x in enumerate(res.ineqlin.marginals) if -x>1e-8])
 print('models',models)
for c in [F(1,10),F(1,5)]:
 print('\nc',c,'iid');lp([bsc(F(2,3)),bsc(F(5,6))],c)
 print('exchangeable');lp([bsc(F(1,2)),bsc(F(1))],c)
 print('rect');lp([rect(m,p1,p0) for m,p1,p0 in product([F(3,5),F(7,10)],[F(8,9),F(20,21)],[F(1,3),F(5,9)])],c)
