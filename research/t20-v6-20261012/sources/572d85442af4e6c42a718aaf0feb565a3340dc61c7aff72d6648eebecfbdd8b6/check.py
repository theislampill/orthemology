import sympy as s,json
u,v=s.symbols('u v'); L=s.Matrix([[u,v,1-u-v]])
B=s.Matrix(3,3,s.symbols('b0:9'));C=s.Matrix(3,3,s.symbols('c0:9'));one=s.ones(3,1)
def field(A):
 row=L*A-(L*A*one)[0]*L
 return s.Matrix([row[0],row[1]])
VB,VC=field(B),field(C)
res=VC.jacobian([u,v])*VB-VB.jacobian([u,v])*VC-field(B*C-C*B)
checks={'normalized_commutator_coordinate_1':s.expand(res[0])==0,'normalized_commutator_coordinate_2':s.expand(res[1])==0,'scalar_identity_vanishes':field(s.eye(3))==s.zeros(2,1)}
# A diagonal scalar-on-each-output map is not generally a global normalization gauge.
D=s.diag(1,2,3)
checks['nonconstant_diagonal_survives']=any(s.expand(z)!=0 for z in field(D))
# Removing the unit cannot give a nontrivial unital associative quotient.
checks['identity_left_product_recovers_arbitrary_operator']=s.eye(3)*B==B
out={'scope':'Root participating symbolic control, finite-dimensional arbitrary real operators. No positivity, realizability or global-flow theorem asserted.','checks':checks,'all_pass':all(checks.values())}
print(json.dumps(out,indent=2)); assert out['all_pass']
