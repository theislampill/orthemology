#!/usr/bin/env python3
"""Exact controls for a bounded M2 source application, not a cognitive model."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent
RESULTS = []

def check(name, condition, detail=None):
    assert condition, name
    RESULTS.append({'name': name, 'passed': True, 'detail': detail})

def posterior(p, a, b):
    z = p*a + (1-p)*b
    return None if z == 0 else p*a/z

def phi(p, r):
    return p*r/(1-p+p*r)

def channel_for_ratio(r):
    return (r/2, F(1,2)) if r <= 1 else (F(1,2), 1/(2*r))

def run():
    priors = sorted({F(i,j) for j in range(2,18) for i in range(1,j)})
    ratios = sorted({F(i,j) for i in range(1,13) for j in range(1,13)})
    thresholds = sorted({F(i,j) for j in range(2,11) for i in range(1,j)})
    n = 0
    for p in priors:
        for r in ratios:
            q = phi(p,r)
            a,b = channel_for_ratio(r)
            assert 0<a<1 and 0<b<1 and a/b == r
            assert posterior(p,a,b) == q
            assert (q>p)-(q<p) == (r>1)-(r<1)
            assert q-p == p*(1-p)*(r-1)/(1-p+p*r)
            z=p*a+(1-p)*b
            assert 0<z<1
            assert z*q+(1-z)*posterior(p,1-a,1-b) == p
            for t in thresholds:
                rb=t*(1-p)/((1-t)*p)
                pb=t/(t+r*(1-t))
                assert (q<t)==(r<rb)==(p<pb)
                assert (q<=t)==(r<=rb)==(p<=pb)
                n += 1
    check('direction_threshold_and_valid_channel_grid', True,
          {'priors':len(priors),'ratios':len(ratios),'thresholds':len(thresholds),'triples':n})

    p=F(99,100); a=F(1,2000); b=F(1,2)
    check('high_prior_low_posterior', posterior(p,a,b)==F(99,1099)<F(1,10),
          {'prior':str(p),'a':str(a),'b':str(b),'posterior':'99/1099'})
    check('high_prior_event_probability', p*a+(1-p)*b==F(1099,200000))
    check('adverse_evidence_high_posterior', phi(p,F(1,2))==F(99,101)>F(9,10))
    check('supporting_evidence_low_posterior', phi(F(1,100),F(2))==F(2,101)>F(1,100))
    check('fixed_ratio_range_low_threshold',
          phi(F(9,10),F(1,1000))==F(9,1009) and
          phi(F(99,100),F(1,1000))==F(99,1099)<F(1,10))
    check('fixed_ratio_range_high_threshold',
          phi(F(9,10),F(1,2))==F(9,11)>F(4,5) and
          phi(F(99,100),F(1,2))==F(99,101))
    check('unresolved_range',
          phi(F(1,10),F(1,2))==F(1,19)<F(1,2)<
          phi(F(9,10),F(1,2))==F(9,11))

    # Every strict boundary must stay open; equality is not strict defeat.
    equality_cases=0
    for p in priors:
        for t in thresholds:
            r=t*(1-p)/((1-t)*p)
            assert phi(p,r)==t
            equality_cases+=1
    check('threshold_equality_boundary', True, {'cases':equality_cases})

    # A fixed finite positive multiplier has no universal interior-prior bound.
    # Invert phi at t/2 and (1+t)/2 to produce exact priors on either side.
    crossing_cases=0
    for r in ratios:
        for t in thresholds:
            qlo=t/2; qhi=(1+t)/2
            plo=qlo/(qlo+r*(1-qlo))
            phi_=qhi/(qhi+r*(1-qhi))
            assert 0<plo<phi_<1
            assert phi(plo,r)==qlo<t<qhi==phi(phi_,r)
            crossing_cases+=1
    check('no_unrestricted_prior_threshold', True, {'cases':crossing_cases})

    l,u,r,s=F(1,4),F(3,4),F(1,3),F(3)
    corners=[phi(p,k) for p in (l,u) for k in (r,s)]
    check('rectangle_extrema',min(corners)==phi(l,r) and max(corners)==phi(u,s))
    # Coupled odds and LR cancel: marginal ranges still form this rectangle,
    # but its corners are impossible and the actual posterior is constant.
    family=[(F(1,4),F(3)),(F(1,2),F(1)),(F(3,4),F(1,3))]
    check('coupled_parameters_make_rectangle_nontight',
          {phi(p,k) for p,k in family}=={F(1,2)} and
          phi(l,r)<F(1,2)<phi(u,s),
          {'actual_posterior':'1/2','rectangle_lower':str(phi(l,r)),
           'rectangle_upper':str(phi(u,s))})

    check('support_cases',
          posterior(F(0),F(1,3),F(1,2))==0 and
          posterior(F(1),F(1,3),F(1,2))==1 and
          posterior(F(1,2),F(0),F(1,2))==0 and
          posterior(F(1,2),F(1,2),F(0))==1 and
          posterior(F(1,2),F(0),F(0)) is None and
          posterior(F(1),F(0),F(1,2)) is None)

    # The same label for a topic does not decide whether an observation is new.
    # Here E is literally already in B; its conditional LR is one, not 1/2.
    old_p=F(3,4); old_q=phi(old_p,F(1,2))
    check('explicit_duplicate_control', phi(old_q,F(1))==old_q and
          phi(old_q,F(1,2))!=old_q)

    bindings=json.loads((ROOT/'INPUT_BINDINGS.json').read_text())
    for item in bindings:
        data=(ROOT/item['packet_path']).read_bytes()
        assert len(data)==item['size']
        assert hashlib.sha256(data).hexdigest()==item['sha256']
        original=ROOT.parent/item['source_path']
        assert original.read_bytes()==data
        if 'git_blob' in item:
            assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==item['git_blob']
    check('input_copy_and_original_custody', True, {'files':len(bindings)})

    out={'status':'PASS','assertion_groups':len(RESULTS),'controls':RESULTS,
         'scope':'Exact rational examples and finite controls; not a proof assistant, actual likelihood validation, or warrant verdict.'}
    (ROOT/'CHECK_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':
    run()
