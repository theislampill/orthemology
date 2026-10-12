from fractions import Fraction as F
from itertools import product
checks=0
def check(x,msg):
 global checks
 if not x:raise RuntimeError(msg)
 checks+=1
def sum_children(children):
 return {tuple(sum(v[i] for v in combo) for i in range(2)) for combo in product(*children)}
def child_choices(masses,legal_values):
 if all(x==0 for x in masses): return {(F(0),F(0))}
 return set(legal_values)
left={(F(1,5),F(2,5))};no_terminal=set()
check(sum_children([left,no_terminal])==set(),'unconditional emptyproduct destroysaction')
right=child_choices((F(0),F(0)),no_terminal)
check(sum_children([left,right])==left,'globally impossible branch zero neutral')
check(child_choices((F(0),F(1)),no_terminal)==set(),'one live model stillinfeasible')
check(child_choices((F(1),F(1)),no_terminal)==set(),'all live models infeasible')
values={tuple(x+F(1,10) for x in z) for z in sum_children([left,right])}
check(values=={(F(3,10),F(1,2))},'cost includedonce')
check(min(max(z) for z in values)==F(1,2),'correct feasible minimax')
print({'status':'PASS','explicit_checks':checks,'scope':'Zero-history legal-menu control; no external implementationmodified'})
