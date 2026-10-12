from itertools import combinations
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import csc_matrix
import numpy as np,json,time
rows=[]
for v,k,t in [(8,3,2),(9,4,2),(10,5,2)]:
 points=list(combinations(range(v),t));blocks=list(combinations(range(v),k))
 A=np.array([[set(p).issubset(b) for b in blocks] for p in points],dtype=float)
 s=time.time();res=milp(np.ones(len(blocks)),integrality=np.ones(len(blocks)),bounds=Bounds(0,1),constraints=LinearConstraint(csc_matrix(A),np.ones(len(points)),np.full(len(points),np.inf)),options={'time_limit':90,'mip_rel_gap':0})
 selected=[list(blocks[i]) for i,x in enumerate(res.x) if x>.5] if res.x is not None else []
 row={'v':v,'k':k,'t':t,'status':int(res.status),'message':res.message,'objective':float(res.fun) if res.fun is not None else None,'dual_bound':float(res.mip_dual_bound) if res.x is not None else None,'elapsed':time.time()-s,'blocks':selected}
 rows.append(row);print(json.dumps(row),flush=True)
open(__import__('pathlib').Path(__file__).resolve().parent/'solver_covering_candidates.json','w').write(json.dumps(rows,indent=2)+'\n')
