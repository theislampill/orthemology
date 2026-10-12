exec(open(__file__.replace('explore_general','explore')).read().split("if __name__")[0])
def law(t):
 return {w: {0:1-3*mu+3*nu-t,1:mu-2*nu+t,2:nu-t,3:t}[sum(w)] for w in product([0,1],repeat=3)}
count=0
for mu in [F(1,4),F(1,3),F(2,5),F(1,2)]:
 for nu in [mu*mu+(mu-mu*mu)*F(k,6) for k in range(1,6)]:
  ti=[nu*nu/mu,nu-(mu-nu)**2/(1-mu)];te=[max(0,2*nu-mu),min(nu,1-3*mu+3*nu)]
  for a in [F(1,3),F(1,2),F(1),F(3,2),F(2),F(3)]:
   for c in [F(0),F(1,100),F(1,24)]:
    r=opt(ti,a,F(1),c);s=opt(te,a,F(1),c)
    if r[0]!=s[0]:
     print(mu,nu,a,c,'iid',r,'exch',s,'ts',ti,te);count+=1
     if count==15:raise SystemExit
print('NONE' if not count else count)
