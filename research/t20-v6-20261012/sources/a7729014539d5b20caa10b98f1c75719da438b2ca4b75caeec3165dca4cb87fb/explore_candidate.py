import mpmath as m
m.mp.dps=55
t=m.mpf(1)/10
w=m.nprod(lambda j: 1-m.exp(-j),[1,m.inf])
B=[m.quad(lambda z: m.exp(r*z-t*m.exp(z)-z*z/2)/m.sqrt(2*m.pi),[-15,-5,0,3,6,9,12,15]) for r in range(25)]
print('w',m.nstr(w,30))
for N in range(1,13):
 H=m.matrix([[B[i+j] for j in range(1,N+1)] for i in range(1,N+1)])
 v=m.matrix([B[i] for i in range(1,N+1)])
 c=m.lu_solve(H,-v)
 q=B[0]+(v.T*c)[0]
 print(N,m.nstr(q-w,18),flush=True)
 if q<w:
  print('coeffs',[m.nstr(a,40) for a in c]);break
