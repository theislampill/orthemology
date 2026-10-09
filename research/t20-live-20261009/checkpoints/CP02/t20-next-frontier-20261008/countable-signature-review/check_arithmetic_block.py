from fractions import Fraction
from pathlib import Path
from math import isqrt
import json

def valuation(n,p):
    result=0
    while n%p==0:
        n//=p
        result+=1
    return result

rows=[]
for k in range(2,10):
    a=2**k-1
    p=next(p for p in range(3,a+1,2) if a%p==0 and all(p%d for d in range(2,isqrt(p)+1)))
    h=valuation(a,p)
    actual=(valuation(a-1,2),valuation(a*a-1,2),-h,-2*h)
    assert actual==(1,k+1,-h,-2*h)
    determinant=actual[0]*actual[3]-actual[1]*actual[2]
    assert determinant==(k-1)*h>0
    values={Fraction(a-1,a)**n1*Fraction(a*a-1,a*a)**n2 for n1 in range(4) for n2 in range(4)}
    assert len(values)==16
    rows.append({'base':a,'k':k,'denominator_prime':p,'denominator_valuation':h,'determinant':determinant})
receipt={'exceptional_base_blocks':rows,'checked_models_per_base':16}
path=Path(__file__).resolve().parent/'ARITHMETIC_CONTROL.json'
path.write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
