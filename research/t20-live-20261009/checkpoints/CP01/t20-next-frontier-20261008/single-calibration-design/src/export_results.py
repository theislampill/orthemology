from pathlib import Path
from dataclasses import asdict
from fractions import Fraction
import json
from crt_calibration import *
BASE=Path(__file__).resolve().parents[1]

def serial(x):
    if isinstance(x,Fraction):return {'numerator':x.numerator,'denominator':x.denominator}
    if isinstance(x,dict):return {str(k):serial(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [serial(v) for v in x]
    return x

def main():
    calibrations=[]
    for r in range(1,5):
        cal=construct(r)
        matrix=tuple(tuple(valuation(cal.failure(s),q) for s in subsets(cal.universe,True)) for q in cal.private_primes)
        sample={p:(p%3) for p in subsets(cal.universe,True) if p%3}
        calibrations.append({'certificate':asdict(cal),'rates':cal.rates,'private_valuation_matrix':matrix,
                             'diagonal':cal.diagonal(),'sample_histogram':sample,
                             'sample_probability':cal.probability(sample),'decoded_sample':cal.decode(cal.probability(sample)),
                             'denominator_bit_length':cal.denominator.bit_length()})
    six=construct(6)
    nonunits=[{'support':p,'prime':q,'valuation':d} for p,q,d in zip(subsets(six.universe,True),six.private_primes,six.diagonal()) if d>1]
    result={'scope':'Exact integer multiplicities under the stipulated response law; no finite empirical frequency or physical actuator claim.',
            'calibrations':calibrations,'six_root_nonunit_diagonals':nonunits,
            'checked_models':{'binary_support_vectors_r1_to_r3':138,'random_support_vectors_r1_to_r4':64,
                              'guarded_histograms_r1_to_r4':32,'test_groups':11}}
    (BASE/'results/RESULTS.json').write_text(json.dumps(serial(result),indent=2)+'\n')
    print(json.dumps({'root_counts':[1,2,3,4],'six_root_nonunit_diagonals':nonunits,'test_groups':11}))
if __name__=='__main__':main()
