from pathlib import Path
from fractions import Fraction
import hashlib,json
from countable_support import *
from gcd_decoder import decode_gcd,histograms_of_weight
from oracle_boundaries import inside_value_gap,one_effect_absence
BASE=Path(__file__).resolve().parents[1]

def serial(x):
    if isinstance(x,Fraction):return {'numerator':x.numerator,'denominator':x.denominator}
    if isinstance(x,dict):return {str(k):serial(v) for k,v in x.items()}
    if isinstance(x,(tuple,list,frozenset)):return [serial(v) for v in x]
    return x

def main():
    finite=[]
    for model in ({4:1},{6:2,3:1,1:4},{32:1}):
        q=probability(model);decoded,trace=decode(q)
        finite.append({'model':model,'probability':q,'decoded':decoded,'trace':trace})
    gcd_examples=[]
    for model in ({11:2},{256:1},{1:5000}):
        q=probability(model);decoded,trace=decode_gcd(q)
        gcd_examples.append({'model':model,'decoded':decoded,'input_numerator_bits':q.numerator.bit_length(),
                             'input_denominator_bits':q.denominator.bit_length(),
                             'readout_sha256':hashlib.sha256(f'{q.numerator}/{q.denominator}'.encode()).hexdigest(),
                             'trace':trace})
    prefix,qprefix,records=greedy_infinite_prefix(1,16)
    left=({1:1},{2:1});right=({1:1,2:1},{3:1});rates=(Q(1,2),Q(1,2))
    mixture={'rates':rates,'left_first':sum(one_effect_absence(m,3,rates) for m in left)/2,
             'right_first':sum(one_effect_absence(m,3,rates) for m in right)/2,
             'left_grouped_second':sum(one_effect_absence(m,3,rates)**2 for m in left)/2,
             'right_grouped_second':sum(one_effect_absence(m,3,rates)**2 for m in right)/2}
    result={'scope':'Exact finite controls and proved infinite-limit targets; no finite prefix is represented as an executed infinite process.',
            'primitive_order_witnesses':[{'exponent':e,'prime':primitive_prime_witness(e)} for e in range(1,25)],
            'finite_decodings':finite,'gcd_examples':gcd_examples,
            'greedy_tail':{'target':failure(1),'prefix_counts':prefix,'prefix_probability':qprefix,'records':records,
                           'exact_infinite_limit_status':'The written convergence proof establishes 3/4; no finite prefix equals it.',
                           'conditional_second_query':compare_scope_queries(failure(1),Q(1))},
            'candidate_specific_gap':inside_value_gap(probability({1:2}),max_inside_count=10),
            'mixture_grouping':mixture,'test_groups':[15,6,8],
            'weighted_cross_decoder_cases':sum(1 for w in range(13) for _ in histograms_of_weight(w))}
    (BASE/'results/RESULTS.json').write_text(json.dumps(serial(result),indent=2)+'\n')
    print(json.dumps({'test_groups':result['test_groups'],'weighted_cross_decoder_cases':result['weighted_cross_decoder_cases'],
                      'gcd_largest_generators':[x['trace']['largest_generator'] for x in gcd_examples]}))
if __name__=='__main__':main()
