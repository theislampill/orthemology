#!/usr/bin/env python3
"""Exact deterministic research controls. No sampling or certified asymptotic cutoff."""
from fractions import Fraction as F
import argparse
from itertools import combinations_with_replacement, product
from math import comb
from pathlib import Path
import hashlib
import json

BASE = Path(__file__).resolve().parent

def harmonic(n, order=1):
    return sum((F(1, j**order) for j in range(1, n+1)), F(0))

def ceil_fraction(x):
    return -(-x.numerator // x.denominator)

def baseline_mean(n):
    m=n+1; a=harmonic(m); g=harmonic(m,2)
    return -2*a/m+F(2,m*m)-(a*a-g-4)/(m+1)-2*(a+1)/(m+1)**2

def exact_root_resolution(n, R, eta):
    m=n+1; A=F(m*(m-1)*R)/eta
    target=A.numerator**m; factor=A.denominator**m
    def valid(L):
        return L**n*factor >= target
    hi=1
    while not valid(hi):
        hi*=2
    lo=1
    while lo<hi:
        mid=(lo+hi)//2
        if valid(mid):
            hi=mid
        else:
            lo=mid+1
    return lo

def plan(n, alpha, eta):
    assert isinstance(n,int) and n>=2
    assert isinstance(alpha,F) and isinstance(eta,F)
    assert alpha>0 and eta>0 and alpha+eta<1
    m=n+1; h=harmonic(n); b=baseline_mean(n)
    R=ceil_fraction(F(192*m**4)/(alpha*h*h))
    La=ceil_fraction(F(32*m**5)/(h*h))
    Lc=exact_root_resolution(n,R,eta)
    return dict(n=n,m=m,h=h,b=b,R=R,L=max(La,Lc),L_area=La,L_collision=Lc,
                threshold=b+h*h/(4*m*m),score_tolerance=h*h/(8*m*m),
                alpha=alpha,eta=eta,
                guarantee='eventual in n; no certified n0')

def direct_minima(points):
    unique=set(points)
    return sorted(p for p in unique if not any(q!=p and q[0]<=p[0] and q[1]<=p[1] for q in unique))

def extract(L, bit):
    """bit accepts integer indices: its physical query is (a/L,b/L)."""
    calls=0
    def query(a,b):
        nonlocal calls
        assert 0<=a<=L and 0<=b<=L
        calls+=1
        return bool(bit(a,b))
    def first_true(hi,predicate):
        lo=0
        while lo<hi:
            mid=(lo+hi)//2
            if predicate(mid):
                hi=mid
            else:
                lo=mid+1
        return lo
    corners=[]; b=L
    while b>=0:
        if not query(L,b):
            break
        a=first_true(L,lambda x:query(x,b))
        y=first_true(b,lambda z:query(a,z))
        corners.append((a,y)); b=y-1
    return corners,calls

def area(corners,L):
    if not corners:
        return F(1)
    numerator=corners[0][0]*L
    for i,(a,b) in enumerate(corners):
        next_a=corners[i+1][0] if i+1<len(corners) else L
        numerator+=(next_a-a)*b
    return F(numerator,L*L)

def score(corners,L,m):
    K=len(corners); U=area(corners,L)
    return (K-m*U)**2-K

def decide(scores,threshold):
    assert scores
    return int(sum(scores,F(0))>=len(scores)*threshold)

def observed_score(L,m,bit):
    corners,calls=extract(L,bit)
    return score(corners,L,m),calls

def run_plan(configuration,fresh_oracle):
    """Exact finite test; fresh_oracle creates the next independent retained oracle.
    The caller must supply the stipulated experiment. No finite-n guarantee is inferred.
    """
    total=F(0); calls=0
    for _ in range(configuration['R']):
        value,used=observed_score(configuration['L'],configuration['m'],fresh_oracle())
        total+=value; calls+=used
    return int(total>=configuration['R']*configuration['threshold']),calls

# Independent finite-polynomial integration of the two-query uncovered event.
def polynomial_U2(n):
    J=sum((F((-1)**j*comb(n,j),(j+2)**2) for j in range(n+1)),F(0))
    I=sum((F((-1)**j*comb(n,j),(j+2)**2)*
           sum((F((-1)**r*comb(j,r),(r+1)**2) for r in range(j+1)),F(0))
           for j in range(n+1)),F(0))
    return 2*(J+I)

def geometry_center(n):
    m=n+1; h=harmonic(n); g=harmonic(n,2)
    Jprevious=sum((F((-1)**j*comb(n-1,j),(j+2)**2) for j in range(n)),F(0))
    KU=n*(polynomial_U2(n-1)-Jprevious)
    return h*h-g-2*m*KU+m*m*polynomial_U2(n)

def oracle(points):
    return lambda a,b:any(x<=a and y<=b for x,y in points)

def qceil(value,denominator,L):
    return (L*value+denominator-1)//denominator

centering=[]
for n in range(1,33):
    b=baseline_mean(n)
    assert b==geometry_center(n),(n,b,geometry_center(n))
    assert abs(b)<=11*harmonic(n+1)**2/(n+1)
    centering.append({'n':n,'b':str(b)})
assert baseline_mean(1)==F(-5,9)

extraction_counts={}; max_queries={}
for L in range(1,5):
    atoms=list(product(range(L+1),repeat=2)); count=0; biggest=0
    for N in range(5):
        for points in combinations_with_replacement(atoms,N):
            corners,calls=extract(L,oracle(points)); want=direct_minima(points)
            assert corners==want
            # Separate midpoint-cell integration of the binary oracle, with boundaries null.
            hit_cells=sum(any(2*x<=2*a+1 and 2*y<=2*b+1 for x,y in points)
                          for a in range(L) for b in range(L))
            U=F(L*L-hit_cells,L*L)
            assert area(corners,L)==U
            assert calls<=1+len(want)*(1+2*L.bit_length())
            assert score(corners,L,max(2,N))==(len(want)-max(2,N)*U)**2-len(want)
            count+=1; biggest=max(biggest,calls)
    extraction_counts[str(L)]=count; max_queries[str(L)]=biggest

quantization_count=0; collision_free_count=0; signs={}; count_loss=None
D=4; L=2
for N in range(5):
    atoms=list(product(range(D+1),repeat=2))
    for points in combinations_with_replacement(atoms,N):
        rounded=[(qceil(x,D,L),qceil(y,D,L)) for x,y in points]
        original=direct_minima(points); grid=direct_minima(rounded); m=max(2,N)
        U=area(original,D); UL=area(grid,L); delta=score(grid,L,m)-score(original,D,m)
        assert 0<=UL-U<=F(2*m,L)
        assert len(grid)<=len(original)
        no_collision=all(len({p[coordinate] for p in rounded})==N for coordinate in (0,1))
        if no_collision:
            assert len(grid)==len(original)
            assert abs(delta)<=F(4*m**3,L)
            collision_free_count+=1
        if len(grid)<len(original) and count_loss is None:
            count_loss={'points_denominator':D,'points':points,'L':L,'K':len(original),'K_L':len(grid)}
        quantization_count+=1

# Exact admissible parameter controls: validate every inequality, including root minimality.
parameter_results=[]
for n,(alpha,eta) in product([2,3,5,10,20,50,100],[(F(1,10),F(1,10)),(F(1,7),F(1,13)),(F(1,3),F(1,4))]):
    p=plan(n,alpha,eta); m=p['m']; h=p['h']; R=p['R']; L=p['L']; e=p['score_tolerance']
    assert F(4*m**3,L)<=e
    assert F(32*m**5,p['L_area'])<=h*h
    assert p['L_area']==1 or F(32*m**5,p['L_area']-1)>h*h
    A=F(m*(m-1)*R)/eta; Lc=p['L_collision']
    assert F(Lc**n)>=A**m
    assert Lc==1 or F((Lc-1)**n)<A**m
    assert F(L**n)>=A**m
    assert F(3)*h*h/(R*e*e)<=alpha
    assert R==1 or F(3)*h*h/((R-1)*e*e)>alpha
    assert p['threshold']-e-p['b']==e
    assert (p['b']+h*h/(2*m*m))-(p['threshold']+e)==e
    # High-resolution antichain with rational coordinates; score budget checked exactly.
    points=[(i,m+1-i) for i in range(1,m+1)]
    rounded=[(qceil(x,m+1,L),qceil(y,m+1,L)) for x,y in points]
    assert all(len({z[c] for z in rounded})==m for c in (0,1))
    got,calls=extract(L,oracle(rounded))
    assert len(got)==m
    assert abs(score(got,L,m)-score(points,m+1,m))<=e
    assert calls<=1+m*(1+2*L.bit_length())
    parameter_results.append({'n':n,'alpha':str(alpha),'eta':str(eta),'R':R,'L':L,
                              'L_bits':L.bit_length(),'guarantee':p['guarantee']})

# Finite comparator ties and full loop behavior on small synthetic configurations.
assert decide([F(1),F(3)],F(2))==1
assert decide([F(1),F(3)],F(201,100))==0
small_configuration={'R':3,'L':4,'m':3,'threshold':F(-1)}
created=[0]
def fresh():
    created[0]+=1
    return oracle([(1,1)])
outcome,used=run_plan(small_configuration,fresh)
assert created[0]==3
expected=score([(1,1)],4,3)
assert outcome==int(expected>=F(-1))
assert used<=3*(1+3*(1+2*(4).bit_length()))

# Deliberately false claims must be rejected; these are not failures of the theorem.
negative={}
for D,L,points in [(16,8,[(1,1)]),(4,2,[(1,1)])]:
    rounded=[(qceil(x,D,L),qceil(y,D,L)) for x,y in points]
    difference=score(direct_minima(rounded),L,3)-score(direct_minima(points),D,3)
    sign='positive' if difference>0 else 'negative'
    assert difference!=0
    signs[sign]={'D':D,'L':L,'points':points,'score_difference':str(difference)}
assert set(signs)=={'positive','negative'}
negative['one_sided_score_bias']={'rejected':True,'witnesses':signs}
# One route means C automatically holds; a coarse grid still overwhelms the planned margin.
coarse_error=abs(score([(1,1)],2,3)-score([(1,1)],4,3))
assert coarse_error>harmonic(2)**2/(8*9)
negative['ignore_area_resolution']={'rejected':True,'n':2,'L':2,'score_error':str(coarse_error),'allowed':str(harmonic(2)**2/72)}
# Collision qualification cannot be deleted from the 4m^3/L score bound.
L=1000; D=4*L; points=[(2,1000),(3,500)]
rounded=[(qceil(x,D,L),qceil(y,D,L)) for x,y in points]
original=direct_minima(points); grid=direct_minima(rounded)
collision_error=abs(score(grid,L,3)-score(original,D,3))
assert len(original)==2 and len(grid)==1
assert collision_error>F(4*3**3,L)
negative['delete_collision_qualification']={'rejected':True,'D':D,'L':L,'points':points,
   'K':len(original),'K_L':len(grid),'score_error':str(collision_error),'claimed_bound':str(F(108,L))}
# Moment-certificate negative control: uncentered threshold need not lie below the lower alternative mean.
n=20; m=n+1; h=harmonic(n); b=baseline_mean(n); gap=h*h/(2*m*m); d=h*h/(4*m*m)
assert b+gap<d
negative['omit_baseline_centering']={'rejected':True,'n':n,'b':str(b),
    'alternative_mean_lower_certificate':str(b+gap),'wrong_threshold':str(d),
    'scope':'Rejects the claimed moment-based guarantee; not a constructed skyline distribution.'}
assert F(3)*64/48==4
negative['reuse_ideal_midpoint_constant_48']={'rejected':True,'chebyshev_bound_multiple_of_alpha':4,
    'scope':'Rejects this sufficient-bound calculation; does not claim 192 is optimal.'}

# Verify the exact source bytes and the sharp accepted digest, without writing predecessor files.
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def check(path,wanted,size=None):
    assert path.is_file(),str(path)
    assert sha(path)==wanted,(str(path),sha(path),wanted)
    if size is not None:
        assert path.stat().st_size==size
bindings=json.loads((BASE/'SOURCE_BINDINGS.json').read_text())
for item in bindings['sources']:
    check(BASE/item['path'],item['sha256'],item['bytes'])
sharp=BASE.parent/'sharp-skyline-information'
review=BASE.parent/'sharp-skyline-information-review'
receipt=json.loads((review/'REVIEW_RECEIPT.json').read_text())
assert receipt['result']=='PASS' and receipt['blocking_findings']==[]
assert receipt['historical_floor']=='UNVERIFIED'
check(sharp/'RESULT.md',receipt['accepted_author_result_sha256'])
check(sharp/'MANIFEST.json',receipt['author_manifest_sha256'])
check(review/'REVIEW.md',receipt['review_sha256'])
check(review/'SOURCE_BINDINGS.json',receipt['source_bindings_sha256'])
source_checks=0
for directory,filename,field in [(sharp,'MANIFEST.json','files'),(sharp,'SOURCE_BINDINGS.json','sources'),
                                 (review,'MANIFEST.json','files'),(review,'SOURCE_BINDINGS.json','sources')]:
    for item in json.loads((directory/filename).read_text())[field]:
        check(directory/item['path'],item['sha256'],item.get('bytes')); source_checks+=1

result={'status':'PASS','kind':'exact deterministic mathematical controls; not a statistical simulation or a formal proof kernel',
        'baseline_centering_cases':len(centering),'centering_boundary_n1':centering[0],
        'extraction_and_cell_area_cases_by_L':extraction_counts,'max_actual_queries_by_L':max_queries,
        'quantization_cases':quantization_count,'collision_free_cases':collision_free_count,'count_loss_witness':count_loss,
        'exact_parameter_cases':len(parameter_results),'parameter_results':parameter_results,
        'full_loop_and_tie_controls':'PASS','negative_controls':negative,
        'direct_source_bindings_checked':len(bindings['sources']),'sharp_transitive_bound_files_checked':source_checks,
        'sharp_review_status':'PASS for exactly bound predecessor; current packet unreviewed',
        'sharp_result_sha256':receipt['accepted_author_result_sha256'],
        'explicit_cutoff_certified':False,'historical_floor':'UNVERIFIED'}
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output-dir',type=Path,default=BASE,help='Write the deterministic result outside the author packet for review replay.')
args=parser.parse_args()
args.output_dir.mkdir(parents=True,exist_ok=True)
(args.output_dir/'CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','baseline_centering_cases':len(centering),
                  'extraction_and_cell_area_cases':sum(extraction_counts.values()),
                  'quantization_cases':quantization_count,'exact_parameter_cases':len(parameter_results),
                  'negative_controls':list(negative),'explicit_cutoff_certified':False,
                  'direct_source_bindings_checked':len(bindings['sources']),
                  'sharp_transitive_bound_files_checked':source_checks},indent=2))
