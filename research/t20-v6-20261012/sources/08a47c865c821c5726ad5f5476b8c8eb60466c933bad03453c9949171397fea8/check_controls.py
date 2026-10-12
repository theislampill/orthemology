from fractions import Fraction as F
import json
from pathlib import Path
rows=[]
for n in range(25):
    no_a=F(1,2)**n
    no_mix=(1+no_a)/2
    a_given_zeros=no_a/(1+no_a)
    next_reveal=a_given_zeros/2
    assert no_mix==F(1,2)+F(1,2)**(n+1)
    assert next_reveal==F(1,2*(2**n+1))
    assert no_mix>F(1,2) and F(1,2)**n>0
    rows.append({'n':n,'one_sided_no_reveal':str(no_mix),'conditional_next_reveal':str(next_reveal),'two_sided_no_reveal':str(F(1,2)**n)})
r={'status':'PASS','scope':'25 exact prefix-probability controls, not proof of universal POMDP strategy criterion','rows':rows}
p=Path(__file__).with_name('CONTROL_RESULTS.json');p.write_text(json.dumps(r,indent=2)+'\n')
print(r['status'],len(rows))
