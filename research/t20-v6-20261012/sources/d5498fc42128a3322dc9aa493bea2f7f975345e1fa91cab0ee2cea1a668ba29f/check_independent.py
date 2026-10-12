from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import argparse,hashlib,json
N=0
def check(ok,msg):
 global N
 N+=1
 if not ok:raise RuntimeError('ACTIVE_MOMENT_REVIEW_FAILURE: '+msg)
def run(fail=False):
 if fail:check(False,'deliberate guard')
 # Independently enumerate finite two-point calibration laws, then rebuild them
 # through the proposed (0,nu/mu) canonical representative.
 for p,q,w in product((Q(0),Q(1,4),Q(1,3),Q(1,2),Q(2,3),Q(3,4),Q(1)),repeat=3):
  mu=w*p+(1-w)*q;nu=w*p*p+(1-w)*q*q
  check(0<=mu<=1 and mu*mu<=nu<=mu,'moment body necessity')
  atoms=((Q(0),Q(1)),) if mu==0 else ((nu/mu,mu*mu/nu),(Q(0),1-mu*mu/nu))
  check(sum(v for u,v in atoms)==1 and all(0<=u<=1 and v>=0 for u,v in atoms),'constructive representative valid')
  m=lambda k:sum((v*u**k for u,v in atoms),Q(0))
  check((m(1),m(2))==(mu,nu),'constructive representative exact')
  original=(w*(1-p)**2+(1-w)*(1-q)**2,w*(1-p)*p+(1-w)*(1-q)*q,w*p*(1-p)+(1-w)*q*(1-q),nu)
  encoded=(1-2*mu+nu,mu-nu,mu-nu,nu)
  check(original==encoded and min(encoded)>=0 and sum(encoded)==1,'ordered path law exact')
  # Independent signed loss row tests the full affine objective, not just mismatch.
  loss=(Q(-2),Q(3),Q(5),Q(7))
  check(sum(a*b for a,b in zip(loss,original))==loss[0]+(-2*loss[0]+loss[1]+loss[2])*mu+(loss[0]-loss[1]-loss[2]+loss[3])*nu,'affine path loss')
 # Explicit distinction from arbitrary exchangeability: anticorrelated fair trials.
 check(Q(0)<Q(1,2)**2,'exchangeable anticorrelation lies outside fixed-p mixture body')
 a=((Q(1,3),Q(3,4)),(Q(1),Q(1,4)));b=((Q(0),Q(1,4)),(Q(2,3),Q(3,4)))
 m=lambda rho,k:sum((w*p**k for p,w in rho),Q(0))
 check(tuple(m(a,k) for k in (1,2))==tuple(m(b,k) for k in (1,2))==(Q(1,2),Q(1,3)),'same two moments')
 check((m(a,3),m(b,3))==(Q(5,18),Q(2,9)),'distinct third moments')
 check((m(a,3)/m(a,2),m(b,3)/m(b,2))==(Q(5,6),Q(2,3)),'positive-event third prediction')
 # Exact posterior mixing, independently of the third-moment ratio code.
 for rho,expected in ((a,Q(5,6)),(b,Q(2,3))):
  weights=tuple(w*p*p for p,w in rho);total=sum(weights)
  check(total==Q(1,3)>0,'two successes have equal positive probability')
  check(sum(p*z/total for (p,w),z in zip(rho,weights))==expected,'posterior calibration averaging')
 for item in json.loads((Path(__file__).parent/'BINDINGS.json').read_text())['inputs']:
  data=(Path(__file__).resolve().parent.parent/item['path']).read_bytes()
  check(hashlib.sha256(data).hexdigest()==item['sha256'] and len(data)==item['bytes'],'input binding '+item['path'])
 return {'status':'PASS','active_checks':N,'scope':'Independent exact controls, with universal argument reviewed in REVIEW.md.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--negative',action='store_true');args=p.parse_args()
 print(json.dumps(run(args.negative),indent=2))
