import sympy as s,json
v=s.symbols('v',positive=True)
m2,m4,m6,m8,m10=s.symbols('m2 m4 m6 m8 m10')
rate2=-2*m4-(m6-m4*m2)/4
rate4=-4*m6-(m8-m4*m4)/4
rate6=-6*m8-(m10-m6*m4)/4
full2=s.diff(rate2,m2)*rate2+s.diff(rate2,m4)*rate4+s.diff(rate2,m6)*rate6
G={m2:v,m4:3*v**2,m6:15*v**3,m8:105*v**4,m10:945*v**5}
f=s.expand(rate2.subs(G)); exact=s.expand(full2.subs(G)); projected=s.expand(s.diff(f,v)*f); gap=s.factor(exact-projected)
checks={'initial_variance_rate':f==-6*v**2-3*v**3,'full_second_derivative':exact==120*v**3+186*v**4+48*v**5,'restricted_second_derivative':projected==72*v**3+90*v**4+27*v**5,'positive_gap_factor':s.expand(gap-3*v**3*(7*v**2+32*v+16))==0,'unit_variance_gap':gap.subs(v,1)==165}
out={'scope':'Root participating exact polynomial calculation; written analytic justification and independent review separate. F=x^4/4, initial centered Gaussian.','values':{'first':str(f),'full_second':str(exact),'restricted_second':str(projected),'difference':str(gap)},'checks':checks,'all_pass':all(checks.values())}
print(json.dumps(out,indent=2));assert out['all_pass']
