#!/usr/bin/env python3
"""Construct explicit proof certificates; the checker is a separate module."""
import json
from pathlib import Path
V=lambda sort,name: ('var',sort,name)
C=lambda sort,name: ('const',sort,name)
At=lambda name,*args: ('atom',name,*args)
All=lambda x,f: ('forall',x,f)
Exi=lambda x,f: ('exists',x,f)
And=lambda a,b: ('and',a,b)
Imp=lambda a,b: ('imp',a,b)
Not=lambda a: Imp(a,('bot',))
x=V('entity','x'); y=V('entity','y'); w=V('world','w')
r=V('entity','r_eigen'); s=V('entity','s_eigen')
actual=lambda t: At('Actual',t)
root=lambda t: At('Root',t)
dep=lambda a,b: At('Dep',a,b)
nec=lambda t: All(w,At('Ex',w,t))
h0=Exi(x,And(actual(x),root(x)))
h1=All(x,Imp(actual(x),Imp(Not(nec(x)),Exi(y,And(actual(y),dep(y,x))))))
h2=All(x,Imp(root(x),All(y,Not(dep(y,x)))))
proof=[]
def add(rule, args=(), premises=()):
    proof.append(dict(rule=rule,args=args,premises=premises)); return len(proof)-1
add('hyp',('root_exists',h0))                         # 0
add('hyp',('contingent_existence_requires_parent',h1))# 1
add('hyp',('root_definition',h2))                    # 2
add('hyp',('hr',And(actual(r),root(r))))             # 3
add('andL',premises=(3,))                           # 4
add('andR',premises=(3,))                           # 5
add('forallE',(r,),(1,))                            # 6
add('impE',premises=(6,4))                          # 7
add('hyp',('hn',Not(nec(r))))                       # 8
add('impE',premises=(7,8))                          # 9
add('hyp',('hs',And(actual(s),dep(s,r))))            # 10
add('andR',premises=(10,))                          # 11
add('forallE',(r,),(2,))                            # 12
add('impE',premises=(12,5))                         # 13
add('forallE',(s,),(13,))                           # 14
add('impE',premises=(14,11))                        # 15
add('existsE',(s,'hs'),(9,15))                      # 16
add('raa',('hn',nec(r)),(16,))                      # 17
add('andI',premises=(4,17))                         # 18
add('existsI',(x,And(actual(x),nec(x)),r),(18,))     # 19
add('existsE',(r,'hr'),(0,19))                      # 20
root_cert=dict(name='Actual root plus contingent-dependence entails a necessary actual entity',
               signature={'Actual':['entity'],'Root':['entity'],'Dep':['entity','entity'],
                          'Ex':['world','entity']},
               assumptions={'root_exists':h0,'contingent_existence_requires_parent':h1,'root_definition':h2},
               proof=proof,conclusion=Exi(x,And(actual(x),nec(x))))

u=V('world','u_eigen'); g=C('entity','fixed_bearer')
proof=[]
hq=All(w,At('Q',w)); hb=All(w,Imp(At('Q',w),At('Ex',w,g)))
add('hyp',('condition_is_necessary',hq))
add('hyp',('same_bearer_is_required',hb))
add('forallE',(u,),(0,))
add('forallE',(u,),(1,))
add('impE',premises=(3,2))
add('forallI',(u,),(4,))
bearer_cert=dict(name='A fixed indispensable bearer of a necessary condition exists necessarily',
                 signature={'Q':['world'],'Ex':['world','entity']},
                 assumptions={'condition_is_necessary':hq,'same_bearer_is_required':hb},
                 proof=proof,conclusion=All(u,At('Ex',u,g)))
# A distinct totality route: no well-foundedness premise occurs.
proof=[]
total=lambda t: At('TotalGround',t)
ground=lambda a,b: At('GroundExistence',a,b)
ht=Exi(x,And(actual(x),total(x)))
hp=All(x,Imp(total(x),All(y,Imp(And(actual(y),Not(nec(y))),ground(x,y)))))
hs=All(x,Not(ground(x,x)))
add('hyp',('total_explanation_exists',ht))              # 0
add('hyp',('explanation_projects_to_contingent_members',hp)) # 1
add('hyp',('no_complete_self_explanation',hs))          # 2
add('hyp',('hr',And(actual(r),total(r))))              # 3
add('andL',premises=(3,))                              # 4
add('andR',premises=(3,))                              # 5
add('hyp',('hn',Not(nec(r))))                          # 6
add('andI',premises=(4,6))                             # 7
add('forallE',(r,),(1,))                               # 8
add('impE',premises=(8,5))                             # 9
add('forallE',(r,),(9,))                               # 10
add('impE',premises=(10,7))                            # 11
add('forallE',(r,),(2,))                               # 12
add('impE',premises=(12,11))                           # 13
add('raa',('hn',nec(r)),(13,))                         # 14
add('andI',premises=(4,14))                            # 15
add('existsI',(x,And(actual(x),nec(x)),r),(15,))        # 16
add('existsE',(r,'hr'),(0,16))                         # 17
total_cert=dict(name='Complete actual explanation of contingent existence is not itself contingent',
                 signature={'Actual':['entity'],'TotalGround':['entity'],
                            'GroundExistence':['entity','entity'],'Ex':['world','entity']},
                 assumptions={'total_explanation_exists':ht,
                              'explanation_projects_to_contingent_members':hp,
                              'no_complete_self_explanation':hs},
                 proof=proof,conclusion=Exi(x,And(actual(x),nec(x))))
p=Path(__file__).resolve().parent/'proof_certificates.json'
p.write_text(json.dumps([root_cert,bearer_cert,total_cert],indent=2)+'\n')
print(p.name)
