from fractions import Fraction as F
from pathlib import Path
import json

root=Path(__file__).resolve().parent

def log_interval(x,width):
    z=(x-1)/(x+1)
    if not z:
        return F(0),F(0)
    term=z
    total=F(0)
    count=0
    while True:
        total+=2*term/(2*count+1)
        count+=1
        term*=z*z
        tail=2*abs(term)/((2*count+1)*(1-z*z))
        if tail<=width:
            return (total,total+tail) if z>0 else (total-tail,total)

cases=0
for k in range(2,41):
    p=F(1,2*k)
    for r in range(1,7):
        q0=(1-p)**(k-1)
        q1=q0*(1-p**r)
        assert F(1,2)<=q1<=q0<=F(4,5)
        assert q1*(1-q1)>=F(1,10)
        separation=q0-q1
        chi=separation**2/(q1*(1-q1))
        assert chi<=10*p**(2*r)
        width=p**(2*r)/10000
        a=log_interval(q0/q1,width)
        b=log_interval((1-q0)/(1-q1),width)
        kl_upper=q0*a[1]+(1-q0)*b[1]
        assert kl_upper<10*p**(2*r)
        cases+=1
receipt={'exact_parameter_pairs':cases,'K_range':[2,40],'root_range':[1,6],
         'checked':'Probability bounds, chi-square upper bound and certified rational-log KL upper enclosures.',
         'not_checked_by_enumeration':'The adaptive chain-rule/Pinsker argument is a written general proof, not a finite simulation.'}
(root/'LOWER_BOUND_CONTROL.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
