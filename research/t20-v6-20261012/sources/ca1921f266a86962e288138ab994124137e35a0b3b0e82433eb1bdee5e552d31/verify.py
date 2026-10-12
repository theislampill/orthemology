#!/usr/bin/env python3
"""Exact symbolic controls for finite completion/Bayes commutation."""
from pathlib import Path
from itertools import product
import argparse, hashlib, json
import sympy as s

HERE=Path(__file__).resolve().parent
Q=s.Rational
checks=[]

def check(name, truth, detail=None):
    assert truth,name
    row={'name':name,'passed':True}
    if detail is not None:row['detail']=detail
    checks.append(row)
    print(f'PASS {len(checks):02d}: {name}',flush=True)

def zero(value):
    if isinstance(value,s.MatrixBase):return all(s.simplify(x)==0 for x in value)
    return s.simplify(value)==0

def normalize(p):
    p=s.Matrix(p)
    return p/sum(p)

def bayes(p,L):
    return normalize([a*b for a,b in zip(p,L)])

def square_num(p):
    a,b,c,d=p
    return s.Matrix([(a+b)*(a+c),(a+b)*(b+d),(c+d)*(a+c),(c+d)*(b+d)])

def square_R(p):
    return square_num(p)/(sum(p)**2)

def square_face(indices):
    if len(indices) in (0,1,4):return True
    return indices in ({0,1},{2,3},{0,2},{1,3})

def stabilizes(M,L):
    return M.col_join((M*s.diag(*L))).rank()==M.rank()

def block_R(p):
    return s.Matrix([(p[0]+p[1])/4,3*(p[0]+p[1])/4,(p[2]+p[3])/3,2*(p[2]+p[3])/3])/sum(p)

def duplicate_R(p):
    agg=s.Matrix([p[0]+p[1],p[2],p[3],p[4]])
    q=square_R(agg)
    return s.Matrix([q[0]/3,2*q[0]/3,q[1],q[2],q[3]])

def polynomial_identities_zero(expressions,variables):
    return all(s.Poly(s.expand(e),*variables).is_zero for e in expressions)

def run():
    for row in json.loads((HERE/'INPUT_BINDINGS.json').read_text())['inputs']:
        b=(HERE/row['snapshot_path']).read_bytes()
        check('bound input '+row['snapshot_path'],len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'])
    states=list(product((-1,1),repeat=2))
    phi=s.Matrix([[x for x,y in states],[y for x,y in states]])
    M=s.ones(1,4).col_join(phi)
    a,b,c,d=s.symbols('a b c d',positive=True)
    variables=(a,b,c,d);raw=s.Matrix(variables);T=sum(raw)
    qnum=square_num(raw)
    check('square completion symbolic mass and moment identities',zero(sum(qnum)-T*T) and zero(phi*(qnum/T**2-raw/T)))
    check('square completion is idempotent',zero(square_R(square_R(raw))-square_R(raw)))
    passed=feasible_passed=0;wrong=[]
    for values in product((0,1,2),repeat=4):
        if not any(values):continue
        L=s.Matrix(values);A=sum(L[i]*raw[i] for i in range(4));B=sum(L[i]*qnum[i] for i in range(4));leftnum=square_num([L[i]*raw[i] for i in range(4)])
        identities=[leftnum[i]*B-L[i]*qnum[i]*A*A for i in range(4)]
        exact=polynomial_identities_zero(identities,variables)
        inA=stabilizes(M,L)
        singleton=sum(x>0 for x in values)==1
        assert exact==(inA or singleton),(values,exact,inA,singleton)
        assert inA==(len(set(values))==1)
        passed+=int(exact)
        zeros={i for i,x in enumerate(values) if x==0}
        feasibility=square_face(zeros)
        assert (exact and feasibility)==inA
        feasible_passed+=int(exact and feasibility)
        if not exact:wrong.append(values)
    check('all 80 square likelihood arrays satisfy exact symbolic positive-input classification',passed==10 and len(wrong)==70,{'likelihood_arrays':80,'commuting':passed,'noncommuting':len(wrong),'method':'Polynomial numerator identity over arbitrary positive atom weights'})
    check('feasibility-sensitive square classification collapses to the stabilizer',feasible_passed==2,{'commuting_with_exact_feasibility':feasible_passed})

    rho=Q(1,2);p=s.Matrix([(1+rho*x*y)/4 for x,y in states]);uniform=s.ones(4,1)/4;local=s.Matrix([int(x==1) for x,y in states])
    lhs=square_R(bayes(p,local));rhs=bayes(square_R(p),local)
    check('unary event preserves branch mass but fails completion commutation',sum(p.multiply_elementwise(local))==Q(1,2) and sum(square_R(p).multiply_elementwise(local))==Q(1,2) and lhs==s.Matrix([0,0,Q(1,4),Q(3,4)]) and rhs==s.Matrix([0,0,Q(1,2),Q(1,2)]))
    check('both local-event results are inside the closed product model',zero(square_R(lhs)-lhs) and zero(square_R(rhs)-rhs) and phi*lhs==s.Matrix([1,Q(1,2)]) and phi*rhs==s.Matrix([1,0]))

    vertex=s.Matrix([0,0,0,1]);anti=s.Matrix([0,Q(1,2),Q(1,2),0]);diag=s.Matrix([Q(1,2),0,0,Q(1,2)])
    check('opposite boundary diagonals share a mean and disagree on vertex feasibility',zero(M*(anti-diag)) and sum(vertex.multiply_elementwise(anti))==0 and sum(vertex.multiply_elementwise(diag))==Q(1,2) and square_R(anti)==uniform and square_R(diag)==uniform)
    check('completion invents vertex possibility but does not change a genuine vertex posterior',sum(vertex.multiply_elementwise(square_R(anti)))==Q(1,4) and square_R(bayes(diag,vertex))==bayes(square_R(diag),vertex)==vertex)
    check('positive-input vertex commutation does not preserve branch probability',sum(vertex.multiply_elementwise(p))==Q(3,8) and sum(vertex.multiply_elementwise(square_R(p)))==Q(1,4) and square_R(bayes(p,vertex))==bayes(square_R(p),vertex)==vertex)

    # Exhaustive boundary grid: two-bit independent completion retains every actually supported atom.
    support_cases=0
    for values in product((0,1,2),repeat=4):
        if not any(values):continue
        pgrid=normalize(values);qgrid=square_R(pgrid)
        assert all(qgrid[i]>0 for i in range(4) if pgrid[i]>0)
        for likelihood in product((0,1),repeat=4):
            if not any(likelihood):continue
            A=sum(pgrid[i]*likelihood[i] for i in range(4));B=sum(qgrid[i]*likelihood[i] for i in range(4))
            assert not (A>0 and B==0)
            support_cases+=1
    check('completion cannot destroy actual branch feasibility on the exact finite grid',support_cases==1200,{'input_weights':80,'nonempty_indicator_likelihoods':15,'pairs':support_cases})

    p5=normalize([1,2,3,4,5]);full=s.Matrix([1,1,0,0,0]);unequal=s.Matrix([1,2,0,0,0]);partial=s.Matrix([1,0,0,0,0]);vertex5=s.Matrix([Q(1,3),Q(2,3),0,0,0])
    check('full duplicate-column vertex fibre commutes with constant weights',duplicate_R(bayes(p5,full))==bayes(duplicate_R(p5),full)==vertex5)
    check('unequal duplicate weights break completion commutation',duplicate_R(bayes(p5,unequal))==vertex5 and bayes(duplicate_R(p5),unequal)==s.Matrix([Q(1,5),Q(4,5),0,0,0]))
    check('partial duplicate support breaks completion commutation',duplicate_R(bayes(p5,partial))==vertex5 and bayes(duplicate_R(p5),partial)==s.Matrix([1,0,0,0,0]))
    M5=s.Matrix([[1]*5,[0,0,0,1,1],[0,0,1,0,1]])
    check('duplicate vertex indicator is facial but outside the stabilizing algebra',M5[:,[0,1]].rank()==1 and not stabilizes(M5,full) and not M5.col_join(full.T).rank()==M5.rank())

    # Nonvertex: uniform reference has mean zero, so its selected completion is itself.
    Mmid=s.Matrix([[1,1,1],[-1,0,1]]);mid=s.Matrix([0,1,0]);umid=s.ones(3,1)/3
    check('nonvertex rank-one likelihood cannot be repaired by normalized-record sufficiency',Mmid[:,[1]].rank()==1 and zero(Mmid*(mid-umid)) and bayes(umid,mid)==mid and mid!=umid)

    # Nontrivial stabilizer: one observed bit, duplicate columns are x-blocks.
    Mblock=s.Matrix([[1,1,1,1],[-1,-1,1,1]])
    blocknum=s.Matrix([(a+b)/4,3*(a+b)/4,(c+d)/3,2*(c+d)/3])
    blockaccepted=0
    for values in product((0,1,2),repeat=4):
        if not any(values):continue
        L=s.Matrix(values);A=sum(L[i]*raw[i] for i in range(4));B=sum(L[i]*blocknum[i] for i in range(4));weighted=[L[i]*raw[i] for i in range(4)]
        w,x,y,z=weighted;leftnum=s.Matrix([(w+x)/4,3*(w+x)/4,(y+z)/3,2*(y+z)/3])
        exact=polynomial_identities_zero([leftnum[i]*B-L[i]*blocknum[i]*A for i in range(4)],variables)
        predicted=values[0]==values[1] and values[2]==values[3]
        assert exact==predicted==stabilizes(Mblock,L),(values,exact,predicted)
        blockaccepted+=int(exact)
    check('all 80 one-coordinate likelihood arrays satisfy the exact blockconstant classification',blockaccepted==8,{'likelihood_arrays':80,'commuting':blockaccepted})
    u,v=s.symbols('u v',nonnegative=True);Lblock=s.Matrix([u,u,v,v]);rawmass=sum(Lblock[i]*raw[i] for i in range(4));completionmass=sum(Lblock[i]*blocknum[i] for i in range(4))
    check('nontrivial stabilizer preserves symbolic branch mass, including zero block values',zero(rawmass-completionmass) and zero(rawmass-(u*(a+b)+v*(c+d))))
    # Exposed-vertex/complement-face positive geometry with duplicate apex.
    columns=s.Matrix([[1,1,1,1],[0,0,1,0],[0,0,0,1]])
    apex=s.Matrix([1,1,0,0]);covector=s.Matrix([1,-1,-1])
    check('vertex-complement face yields an affine stabilizing indicator',columns.T*covector==apex and stabilizes(columns,apex) and columns[:,[2,3]].rank()==2 and columns.rank()==3)
    result={'scope':'Exact author symbolic controls; not independent review or a substitute for the ordinary universal proof.','assertion_groups':len(checks),'checks':checks}
    print(f'PASS: {len(checks)} exact assertion groups')
    return result

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path);args=parser.parse_args();result=run()
    if args.output_dir is not None:
        args.output_dir.mkdir(parents=True,exist_ok=True);(args.output_dir/'CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
