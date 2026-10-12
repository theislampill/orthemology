"""Bounded differential experiment. No Lean execution or universal credit.
The abstract side uses simultaneous substitution and application spines, not
reference.py's cutoff traversal / recursive head-context implementation.
"""
from pathlib import Path
import hashlib,json,os,sys
sys.path.insert(0,os.environ['P03_SOURCE'])
import reference as r


def rename(t,rho):
    if t[0]=='v':return ('v',rho(t[1]))
    if t[0]=='bottom':return t
    if t[0]=='arr':return ('arr',rename(t[1],rho),rename(t[2],rho))
    if t[0]=='all':return ('all',rename(t[1],lambda n:0 if n==0 else rho(n-1)+1))
    raise ValueError(t)


def substitute(t,sigma):
    if t[0]=='v':return sigma(t[1])
    if t[0]=='bottom':return t
    if t[0]=='arr':return ('arr',substitute(t[1],sigma),substitute(t[2],sigma))
    if t[0]=='all':
        return ('all',substitute(t[1],lambda n:('v',0) if n==0 else rename(sigma(n-1),lambda k:k+1)))
    raise ValueError(t)


def spine_step(t):
    args=[];head=t
    while head[0]=='app':args.append(head[2]);head=head[1]
    args.reverse()
    if head==('i',) and len(args)>=1:out=args[0];rest=args[1:]
    elif head==('k',) and len(args)>=2:out=args[0];rest=args[2:]
    elif head==('s',) and len(args)>=3:
        a,b,x=args[:3];out=('app',('app',a,x),('app',b,x));rest=args[3:]
    else:return None
    for arg in rest:out=('app',out,arg)
    return out


def ensure(ok,detail):
    if not ok:raise RuntimeError(json.dumps(detail,ensure_ascii=False))


def main():
    bysize={1:[('bottom',),('v',0),('v',1),('v',2)]}
    for n in range(2,6):
        vals=[('all',t) for t in bysize[n-1]]
        for i in range(1,n-1):
            for a in bysize[i]:
                for b in bysize[n-1-i]:vals.append(('arr',a,b))
        bysize[n]=vals
    types=[t for n in range(1,6) for t in bysize[n]]
    shift_cases=sub_cases=0
    for t in types:
        for amount in range(4):
            for cutoff in range(4):
                actual=r.shift_type(t,amount,cutoff)
                expected=rename(t,lambda n:n if n<cutoff else n+amount)
                ensure(actual==expected,{'shift_failure':[t,amount,cutoff,actual,expected]});shift_cases+=1
        for arg in types:
            expected=substitute(t,lambda n:arg if n==0 else ('v',n-1))
            actual=r.instantiate_type(t,arg)
            ensure(actual==expected,{'substitution_failure':[t,arg,actual,expected]});sub_cases+=1
    terms_by_size={1:[(tag,) for tag in ('i','k','s','zero','one')]}
    for n in range(2,8):
        terms_by_size[n]=[('app',f,x) for i in range(1,n-1)
                         for f in terms_by_size[i] for x in terms_by_size[n-1-i]]
    terms=[t for n in range(1,8) for t in terms_by_size[n]]
    for t in terms:ensure(r.head_step(t)==spine_step(t),{'step_failure':t})
    # Independent mutation-sensitivity witness: omitting the under-binder lift
    # would capture var0 here. This is NOT a production-source mutation.
    witness={'body':('all',('v',1)),'argument':('v',0)}
    expected=substitute(witness['body'],lambda n:witness['argument'] if n==0 else ('v',n-1))
    ensure(expected==('all',('v',1)) and expected!=('all',('v',0)),{'lift_witness':expected})
    corpus=json.dumps({'types':types,'terms':terms},separators=(',',':'),sort_keys=True).encode()
    root=Path(__file__).resolve().parents[1]
    target=root/'evidence/FINITE_CORRESPONDENCE_CORPUS.json'
    if target.exists():ensure(target.read_bytes()==corpus,{'corpus_drift':True})
    else:target.write_bytes(corpus)
    print(json.dumps({'status':'PASS_FINITE_ONLY','types':len(types),'types_ast_nodes_max':5,
      'variable_indices':[0,1,2],'shift_cases':shift_cases,'shift_amounts':[0,1,2,3],'cutoffs':[0,1,2,3],
      'substitution_pairs':sub_cases,'head_step_terms':len(terms),'term_ast_nodes_max':7,
      'failures':0,'corpus_bytes':len(corpus),'corpus_sha256':hashlib.sha256(corpus).hexdigest(),
      'reference_sha256':hashlib.sha256(Path(r.__file__).read_bytes()).hexdigest(),
      'binder_lift_sensitivity_witness':{**witness,'correct':expected,'uncaptured_lift_mutant':('all',('v',0))},
      'kernel_credit':False,'universal_python_refinement_credit':False},indent=2))
if __name__=='__main__':main()
