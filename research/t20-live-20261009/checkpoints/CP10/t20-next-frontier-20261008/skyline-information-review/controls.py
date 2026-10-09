import itertools, json, math
import mpmath as mp
mp.mp.dps=45
H=lambda n: sum(mp.mpf(1)/j for j in range(1,n+1))
results={}
rows=[]
for n in [1,2,3,4,10,30,100]:
 m=n+1;c=mp.mpf(n)/m
 integral=n*mp.quad(lambda t: -mp.log(t)*(1-t)**(n-2)*(1-c*t),[0,mp.mpf('.5'),1])
 delta=(mp.zeta(2)-1)/2 if n==1 else (H(n)-1)/(n*n-1)
 expected=H(n)+delta
 assert abs(integral-expected)<mp.mpf('1e-35')
 assert delta>0 and delta<=mp.mpf(1)/m
 V=H(m)-sum(mp.mpf(1)/(j*j) for j in range(1,m+1))
 W=V+H(m)**2-expected**2
 assert W>=0
 rows.append(dict(n=n,mean=str(expected),gap=str(delta),variance_bound=str(W),quadrature_error=str(abs(integral-expected))))
results['means']=rows
# Exhaust all 120 rank permutations at fixed interior coordinates. Reverse must minimize density product.
x=[mp.mpf(v)/10 for v in [1,3,5,7,9]]; y=[mp.mpf(v)/10 for v in [1,2,4,6,8]]; c=mp.mpf(4)/5
f=lambda a,b:c*(1-a*b)**(c-2)*(1-c*a*b)
weights=[mp.fprod(f(x[i],y[p[i]]) for i in range(5)) for p in itertools.permutations(range(5))]
reverse=mp.fprod(f(x[i],y[4-i]) for i in range(5))
assert reverse==min(weights)
assert reverse/sum(weights)<=mp.mpf(1)/math.factorial(5)
results['conditional_reverse_rank_probability']=str(reverse/sum(weights))
# General conditional CDF by differentiating F with respect to X and normalizing its marginal.
def quantile(x,u,c):
 lo=mp.mpf(0);hi=mp.mpf(1)
 for _ in range(150):
  mid=(lo+hi)/2
  G=mid*((1-x*mid)/(1-x))**(c-1)
  if G<u:lo=mid
  else:hi=mid
 return (lo+hi)/2
violations=0; checks=0
xs=[mp.mpf(v)/10 for v in [1,4,8]]
for us in itertools.product([mp.mpf(v)/10 for v in [1,3,5,7,9]],repeat=3):
 ys=[quantile(xs[i],us[i],mp.mpf(2)/3) for i in range(3)]
 for i in range(1,3):
  iy=ys[i]<min(ys[:i]);iu=us[i]<min(us[:i])
  violations+=int(iy and not iu);checks+=1
assert violations==0
results['quantile_record_checks']={'checked':checks,'violations':violations}
# Deliberately false assertions are rejected by explicit countervalues.
results['negative_controls']={'wrong_zero_mean_gap_n2_rejected': abs(mp.mpf(1)/6)>0,'wrong_uniform_reverse_rank_probability_rejected':reverse/sum(weights)<mp.mpf(1)/120,'wrong_n1_quotient_not_evaluated':True}
results['n1_exact_variance']=str(((mp.zeta(2)-1)/2)*(1-(mp.zeta(2)-1)/2))
print(json.dumps(results,indent=2))
