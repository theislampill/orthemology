from fractions import Fraction
from itertools import product
from pathlib import Path
import json
R=Path(__file__).resolve().parent
binary=0;prefix=0
for b in range(1,41):
 for a in range(b+1):
  for n in range(21):
   ds=[True if a==b else (a*2**(i+1)//b)%2==1 for i in range(n)]
   s=sum((Fraction(1,2**(i+1)) for i,d in enumerate(ds) if d),Fraction())
   q=Fraction(a,b)
   assert 0<=q-s<=Fraction(1,2**n)
   if a<b: assert s==Fraction(a*2**n//b,2**n)
   binary+=1

def sentinel(bs):
 v=1
 for b in bs:v=2*v+b
 return v

def F(a,n,w):return a+3*n+5*w
for length in range(1,11):
 for bits in product(range(2),repeat=length):
  for n in range(length):
   bs=bits[:n+1];word=sentinel(bs)
   scanned=[(word//2**(n-j))%2 for j in range(n+1)]
   i=next((j for j,b in enumerate(scanned) if not b),len(scanned))
   for mode in range(3):
    d=lambda i: mode==1 or (mode==2 and i%2==0)
    for a in range(3):
     value=word%2 if n<=i or d(i) else F(a,n-i-1,sentinel(scanned[i+1:]))
     whole_i=next((j for j,b in enumerate(bits) if not b),len(bits))
     expected=(bits[n] if n<=whole_i or d(whole_i) else F(a,n-whole_i-1,sentinel(bits[whole_i+1:n+1])))%2
     assert value%2==expected
     prefix+=1
(R/'EXACT_CONTROLS.json').write_text(json.dumps({'binary_exact_fraction_cases':binary,'finite_prefix_cases':prefix,'result':'PASS','scope':'Finite executable guard only; Lean supplies universal theorems.'},indent=2)+'\n')
print(binary,prefix,'PASS')
