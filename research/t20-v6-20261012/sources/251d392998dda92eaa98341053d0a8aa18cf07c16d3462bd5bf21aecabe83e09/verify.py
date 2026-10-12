#!/usr/bin/env python3
"""Exact bounded controls; RESULT.md contains the universal ordinary proofs."""
from pathlib import Path
from itertools import product
import argparse
import hashlib
import json
import sympy as sp

HERE = Path(__file__).resolve().parent
Q = sp.Rational
checks = []


def check(name, truth, detail=None):
    assert truth, name
    item = {"name": name, "passed": True}
    if detail is not None:
        item["detail"] = detail
    checks.append(item)
    print(f"PASS {len(checks):02d}: {name}", flush=True)


def zero(a):
    if isinstance(a, sp.MatrixBase):
        return all(sp.simplify(x) == 0 for x in a)
    return sp.simplify(a) == 0


def normalize(v):
    v = sp.Matrix(v)
    assert all(x >= 0 for x in v) and sum(v) > 0
    return v / sum(v)


def posterior(p, L):
    v = sp.Matrix([a*b for a, b in zip(p, L)])
    return normalize(v)


def cov(phi, p):
    z = phi*p
    return phi*sp.diag(*p)*phi.T - z*z.T


def supp(v):
    return frozenset(i for i, x in enumerate(v) if x > 0)


def log_retained(M, L, indices):
    """Exact log-row-space check for strictly positive rational values on indices.
    Each rational kernel relation is integer-scaled and verified multiplicatively.
    """
    indices = sorted(indices)
    if not indices:
        raise ValueError("Empty support has no posterior")
    N = M[:, indices]
    for h in N.nullspace():
        denominator = sp.ilcm(*[a.q for a in h]) if len(h) > 1 else h[0].q
        h = [int(denominator*a) for a in h]
        ratio = sp.prod(L[i]**a for i, a in zip(indices, h))
        if ratio != 1:
            return False
    return True


def square_face(indices, states):
    if len(indices) in (1, 4):
        return True
    if len(indices) != 2:
        return False
    return any(len({states[i][j] for i in indices}) == 1 for j in (0, 1))


def square_closure(p, r):
    return p[0]*p[3]*r[1]*r[2] == p[1]*p[2]*r[0]*r[3]


def H(p, r):
    return sum(px*sp.log(px/rx) for px, rx in zip(p, r) if px > 0)


def kl(p, q):
    assert all(qx > 0 for px, qx in zip(p, q) if px > 0)
    return sum(px*sp.log(px/qx) for px, qx in zip(p, q) if px > 0)


def run():
    bindings = json.loads((HERE/'INPUT_BINDINGS.json').read_text())
    for item in bindings['inputs']:
        b = (HERE/item['snapshot_path']).read_bytes()
        check('bound snapshot '+item['snapshot_path'], len(b) == item['bytes'] and hashlib.sha256(b).hexdigest() == item['sha256'])

    states = list(product((-1, 1), repeat=2))
    phi = sp.Matrix([[x for x,y in states], [y for x,y in states]])
    M = sp.ones(1, 4).col_join(phi)
    r = sp.ones(4, 1)/4
    check('minimal square observable rank and circuit', M.rank() == 3 and M.nullspace() == [sp.Matrix([1,-1,-1,1])])
    diagonal = sp.Matrix([int(x == y) for x,y in states])
    antidiagonal = sp.ones(4,1)-diagonal
    qplus, qminus = posterior(r, diagonal), posterior(r, antidiagonal)
    check('opposite diagonal posteriors share the global interior mean', zero(phi*qplus) and zero(phi*qminus) and qplus == diagonal/2 and qminus == antidiagonal/2)
    check('diagonal supports violate product closure polynomial', not square_face(supp(qplus), states) and not square_face(supp(qminus), states) and not square_closure(qplus,r) and not square_closure(qminus,r))
    check('actual diagonal covariances differ from entropy-completion covariance', cov(phi,qplus)==sp.Matrix([[1,1],[1,1]]) and cov(phi,qminus)==sp.Matrix([[1,-1],[-1,1]]) and cov(phi,r)==sp.eye(2))
    check('restricted diagonal charts have positive one-dimensional covariance', cov(phi[:1,:],qplus)==sp.ones(1,1) and cov(phi[:1,:],qminus)==sp.ones(1,1))

    tilted = normalize([Q(2)**x * Q(3)**y for x,y in states])
    n_accept = 0
    for raw in product((0,1,2), repeat=4):
        if not any(raw):
            continue
        L=sp.Matrix(raw); S=supp(L)
        predicted = square_face(S,states) and log_retained(M,L,S)
        observed = [square_closure(posterior(p,L),r) for p in (r,tilted)]
        assert observed == [predicted,predicted], (raw,predicted,observed)
        n_accept += int(predicted)
    check('all 80 nonzero ternary likelihoods obey one-parameter/all-parameter criterion at two controls', True, {'likelihoods':80,'priors_per_likelihood':2,'accepted_likelihoods':n_accept})
    counts={'both':0,'closure_only':0,'feasibility_only':0,'neither':0}
    allindices=frozenset(range(4))
    for mask in range(1,16):
        S=frozenset(i for i in range(4) if mask & (1<<i)); Z=allindices-S
        closed=square_face(S,states)
        feasible=not Z or square_face(Z,states)
        name='both' if closed and feasible else 'closure_only' if closed else 'feasibility_only' if feasible else 'neither'
        counts[name]+=1
        assert square_closure(normalize([int(i in S) for i in range(4)]),r)==closed
    check('positive-support and zero-set face contracts are independent', counts=={'both':5,'closure_only':4,'feasibility_only':4,'neither':2},counts)

    # Exact edge limit: t=exp(-2 theta_x) > 0, y tilt gives mean 1/3.
    t=sp.symbols('t',positive=True)
    p_t=sp.Matrix([(t if x==-1 else 1)*(1+Q(y,3)) for x,y in states])/(2*(1+t))
    qedge=sp.Matrix([sp.limit(px,t,0,dir='+') for px in p_t])
    check('normal exponential ray reaches the entire saturated edge', qedge==sp.Matrix([0,0,Q(1,3),Q(2,3)]) and phi*qedge==sp.Matrix([1,Q(1,3)]))
    check('ambient edge covariance is singular with correct positive reduction', cov(phi,qedge)==sp.diag(0,Q(8,9)) and cov(phi[1:2,:],qedge).inv()==sp.Matrix([[Q(9,8)]]))
    u=sp.symbols('u',real=True)
    q_u=sp.Matrix([(1-u)/2,(1+u)/2])
    fisher=sum(sp.diff(qx,u)**2/qx for qx in q_u)
    check('intrinsic edge Fisher metric equals inverse covariance', zero(fisher-1/(1-u*u)) and sp.limit(1/(1-u*u),u,1,dir='-')==sp.oo)

    cube=list(product((-1,1),repeat=3))
    pcube=sp.ones(8,1)/8
    phicube=sp.Matrix([[s[i] for s in cube] for i in range(3)])
    Mcube=sp.ones(1,8).col_join(phicube)
    Lbad=sp.Matrix([int(x==1)*(1+Q(y*z,2)) for x,y,z in cube])
    pbad=posterior(pcube,Lbad); faceidx=sorted(supp(Lbad))
    check('facial support without restricted log membership fails', all(cube[i][0]==1 for i in faceidx) and len(faceidx)==4 and not log_retained(Mcube,Lbad,faceidx) and phicube*pbad==sp.Matrix([1,0,0]))
    yztable=[pbad[i] for i in faceidx]
    check('facial nonaffine likelihood creates exact odds ratio nine', yztable==[Q(3,8),Q(1,8),Q(1,8),Q(3,8)] and yztable[0]*yztable[3]/(yztable[1]*yztable[2])==9)
    Lgood=sp.Matrix([int(x==1)*Q(2)**y*Q(3)**z for x,y,z in cube])
    pgood=posterior(pcube,Lgood)
    vals=[pgood[i] for i in faceidx]
    check('facial affine-log likelihood passes the same support control', log_retained(Mcube,Lgood,faceidx) and vals[0]*vals[3]==vals[1]*vals[2])

    points=[(0,0),(1,0),(1,0),(2,0),(0,1),(2,1)]
    phid=sp.Matrix([[x for x,y in points],[y for x,y in points]])
    Md=sp.ones(1,6).col_join(phid)
    rd=sp.Matrix([1,2,3,1,2,4])/13
    bottom=range(4)
    qb=normalize([rd[i] if i<4 else 0 for i in range(6)])
    endpoints=sp.Matrix([Q(1,2),0,0,Q(1,2),0,0])
    check('bottom face is saturated over duplicate and nonvertex supplied columns', Md.rank()==3 and Md[:,list(bottom)].rank()==2 and all(phid[1,i]==0 for i in bottom) and all(phid[1,i]>0 for i in (4,5)))
    check('mean does not identify unknown support even on a proper face', qb==sp.Matrix([1,2,3,1,0,0])/7 and phid*qb==sp.Matrix([1,0]) and zero(phid*(qb-endpoints)) and supp(qb)!=supp(endpoints))
    Lduplicate=sp.Matrix([1,1,2,1,0,0])
    Lmiddle=sp.Matrix([1,2,2,1,0,0])
    Laffine=sp.Matrix([1,2,2,4,0,0])
    check('duplicate splitting and nonaffine interior weights both violate restricted log condition', not log_retained(Md,Lduplicate,bottom) and not log_retained(Md,Lmiddle,bottom) and log_retained(Md,Laffine,bottom))
    qtilt=posterior(rd,Laffine)
    pendpoint=sp.Matrix([Q(2,5),0,0,Q(3,5),0,0])
    check('finite relative parameter realizes an exact nonzero boundary mean', qtilt==sp.Matrix([1,4,6,4,0,0])/15 and phid*qtilt==sp.Matrix([Q(6,5),0]) and zero(phid*(qtilt-pendpoint)) and qtilt[1]/qtilt[2]==Q(2,3))
    dual=Q(6,5)*sp.log(2)-sp.log(Q(15,13))
    check('boundary entropy identity and exposed-ray dual value', sp.expand_log(H(qtilt,rd)-dual,force=True).simplify()==0 and sp.expand_log(H(pendpoint,rd)-kl(pendpoint,qtilt)-dual,force=True).simplify()==0 and kl(pendpoint,qtilt)==Q(2,5)*sp.log(6)+Q(3,5)*sp.log(Q(9,4)))

    phipair=sp.Matrix([[s[i] for s in cube] for i in range(3)]+[[s[i]*s[j] for s in cube] for i,j in ((0,1),(0,2),(1,2))])
    Mpair=sp.ones(1,8).col_join(phipair)
    a=sp.Matrix([Q(1+x*y+x*z+y*z,4) for x,y,z in cube])
    facet=[i for i in range(8) if a[i]==0]
    pfacet=normalize([1-a[i] for i in range(8)])
    fullcov=cov(phipair,pfacet)
    psi=phipair[:5,:]
    reduced=cov(psi,pfacet)
    unary=sp.Matrix(3,3,lambda i,j:1 if i==j else -Q(1,3))
    pairs=sp.Matrix([[Q(8,9),-Q(4,9)],[-Q(4,9),Q(8,9)]])
    check('pairwise global facet has six saturated atoms and dimension five', len(facet)==6 and Mpair.rank()==7 and Mpair[:,facet].rank()==6 and phipair*pfacet==sp.Matrix([0,0,0,-Q(1,3),-Q(1,3),-Q(1,3)]))
    normal=sp.Matrix([0,0,0,1,1,1])
    check('ambient covariance loses exactly the global face normal', fullcov.rank()==5 and fullcov.nullspace()==[normal] and zero(fullcov*normal))
    check('reduced pairwise-facet covariance has exact positive blocks and eigenvalues', reduced==sp.diag(unary,pairs) and reduced.eigenvals()=={Q(1,3):1,Q(4,3):3,Q(4,9):1} and all(reduced[:k,:k].det()>0 for k in range(1,6)))
    eps=sp.symbols('epsilon',positive=True)
    peps=sp.Matrix([eps if a[i]==1 else 1 for i in range(8)])/(6+2*eps)
    check('observable normal-ray limit realizes the inherited global facet', sp.Matrix([sp.limit(px,eps,0,dir='+') for px in peps])==pfacet and zero(sum(peps)-1))
    # The explicit affine relation removes one pair moment, rather than a local table cell.
    check('minimal facet coordinates remove the true affine redundancy', all(phipair[5,i]==-1-phipair[3,i]-phipair[4,i] for i in facet) and sp.ones(1,6).col_join(psi[:,facet]).rank()==6)

    check('six-atom face has full projection onto every pair', all({(cube[i][j],cube[i][k]) for i in facet}==set(product((-1,1),repeat=2)) for j,k in ((0,1),(0,2),(1,2))))
    soft=sp.symbols('soft',positive=True)
    factors=[[soft if state[j]==state[k] else 1 for state in cube] for j,k in ((0,1),(0,2),(1,2))]
    combined=sp.Matrix([sp.prod(factor[i] for factor in factors) for i in range(8)])
    branch=sum(combined)/8
    normalised=combined/sum(combined)
    check('pair-local soft limit has vanishing event mass but the stated posterior limit', all(combined[i]==(soft if i in facet else soft**3) for i in range(8)) and branch==(6*soft+2*soft**3)/8 and sp.limit(branch,soft,0,dir='+')==0 and sp.Matrix([sp.limit(px,soft,0,dir='+') for px in normalised])==pfacet)
    check('simultaneous hard pair anti-alignment is impossible while the global six-atom event is positive', not any(x*y==-1 and x*z==-1 and y*z==-1 for x,y,z in cube) and sum((1-a[i])*pcube[i] for i in range(8))==Q(3,4))

    # Every unary likelihood preserves the entire closed fixed-r square family.
    # Use a nonproduct reference: this verifies a fixed residual class, not independence.
    rnon=normalize([1,2,3,4])
    faces=[frozenset(i for i in range(4) if mask&(1<<i)) for mask in range(1,16)]
    faces=[S for S in faces if square_face(S,states)]
    passed=impossible=0
    for face in faces:
        prior=normalize([rnon[i]*Q(2)**states[i][0]*Q(3)**states[i][1] if i in face else 0 for i in range(4)])
        assert square_closure(prior,rnon)
        for coord in (0,1):
            for values in product((0,1,2),repeat=2):
                if not any(values):
                    continue
                L=sp.Matrix([values[0 if s[coord]==-1 else 1] for s in states])
                eventmass=sum(a*b for a,b in zip(prior,L))
                if eventmass==0:
                    impossible+=1
                    continue
                out=posterior(prior,L)
                assert square_closure(out,rnon)
                assert square_face(supp(out),states)
                passed+=1
    check('all local unary ternary likelihoods preserve every selected closed stratum of a nonproduct reference', passed+impossible==144 and passed>0 and impossible>0, {'face_states':len(faces),'positive_branches':passed,'impossible_branches':impossible})
    rrplus=sp.Matrix([(1+Q(x*y,2))/4 for x,y in states])
    rrminus=sp.Matrix([(1-Q(x*y,2))/4 for x,y in states])
    local=sp.Matrix([int(x==1) for x,y in states])
    check('fixed-reference local closure does not imply all-prior marginal sufficiency', zero(phi*(rrplus-rrminus)) and phi*posterior(rrplus,local)==sp.Matrix([1,Q(1,2)]) and phi*posterior(rrminus,local)==sp.Matrix([1,-Q(1,2)]))
    # A zero-dimensional face with repeated columns has fixed r proportions.
    vertex_points=sp.Matrix([[0,0,1]])
    vertex_r=sp.Matrix([2,3,5])/10
    vertex_q=normalize([2,3,0])
    check('duplicate vertex stratum retains reference proportions without fake positive dimension', vertex_points*vertex_q==sp.zeros(1,1) and vertex_q==sp.Matrix([Q(2,5),Q(3,5),0]) and cov(vertex_points,vertex_q)==sp.zeros(1,1))

    result={'scope':'Exact author controls for selected finite cases; not a universal numerical proof or independent review.','assertion_groups':len(checks),'checks':checks}
    print(f"PASS: {len(checks)} exact assertion groups")
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output-dir',type=Path)
    args=parser.parse_args()
    result=run()
    if args.output_dir is not None:
        args.output_dir.mkdir(parents=True,exist_ok=True)
        (args.output_dir/'CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
