from pathlib import Path
from itertools import product
from collections import defaultdict
import hashlib,json,yaml
ROOT=Path(__file__).resolve().parents[1]
# verify frozen hashes independently
hash_file=ROOT/'PMR-007_DEEP_F_V3_FROZEN_HASHES.sha256'
mis=[]
for line in hash_file.read_text().splitlines():
    if not line.strip(): continue
    exp, rel=line.split(None,1); rel=rel.strip()
    p=ROOT/rel
    got=hashlib.sha256(p.read_bytes()).hexdigest()
    if got!=exp: mis.append({'path':rel,'expected':exp,'observed':got})

# Independent relation representation: each world is a frozenset of true atoms.
atoms=['Src','Des','Aim','Fit','Op','Env','Acc','Und','Rel','Corr','Coh']
worlds=[]
for bits in product([False,True], repeat=len(atoms)):
    w=frozenset(a for a,b in zip(atoms,bits) if b)
    q=tuple(a in w for a in ['Acc','Rel','Corr','Coh'])
    nfunc=all(a in w for a in ['Src','Des','Aim','Fit','Op','Env'])
    nacc=nfunc and 'Acc' in w
    nwarr=nacc and 'Und' in w
    worlds.append((w,q,(nfunc,nacc,nwarr)))

fibres=defaultdict(lambda:[set(),set(),set()])
for _,q,v in worlds:
    for i,x in enumerate(v): fibres[q][i].add(x)
collisions=[sum(1 for q in fibres if len(fibres[q][i])>1) for i in range(3)]

# Rich profile exact factorization check.
rich={}
rich_mismatch=0
for w,q,v in worlds:
    key=tuple(a in w for a in atoms)
    if key in rich and rich[key]!=v: rich_mismatch+=1
    rich[key]=v

# Independence witnesses.
def evalw(true_atoms):
    w=set(true_atoms)
    nf=all(a in w for a in ['Src','Des','Aim','Fit','Op','Env'])
    na=nf and 'Acc' in w
    nw=na and 'Und' in w
    return (nf,na,nw)
witnesses={
 'proper_function_without_accuracy':evalw(['Src','Des','Aim','Fit','Op','Env']),
 'accuracy_without_proper_function':evalw(['Acc','Rel','Corr','Coh']),
 'accurate_proper_but_defeated':evalw(['Src','Des','Aim','Fit','Op','Env','Acc']),
 'full_source_package':evalw(['Src','Des','Aim','Fit','Op','Env','Acc','Und']),
}
# Same q twin.
twin1=frozenset(['Src','Des','Aim','Fit','Op','Env','Acc','Und','Rel','Corr','Coh'])
twin2=frozenset(['Aim','Fit','Op','Env','Acc','Und','Rel','Corr','Coh'])
q1=tuple(a in twin1 for a in ['Acc','Rel','Corr','Coh']);q2=tuple(a in twin2 for a in ['Acc','Rel','Corr','Coh'])

source=json.loads((ROOT/'checks/pmr007_deep_f_source_custody_check_v3_results.json').read_text())
model=yaml.safe_load((ROOT/'models/PMR007_DEEP_F_FITRAH_PROPER_FUNCTION_MODELS_V3.yaml').read_text())

out={
 'schema':'PMR007_DEEP_F_V3_DISTINCT_REREVIEW_RESULTS',
 'frozen_hash_mismatches':mis,
 'worlds_checked':len(worlds),
 'neutral_profile_collision_counts':{'NFunc_T':collisions[0],'NAcc_T':collisions[1],'NWarr_T':collisions[2]},
 'rich_profile_mismatches':rich_mismatch,
 'independence_witnesses':witnesses,
 'same_profile_twin':{'same_q':q1==q2,'track_n_values':evalw(twin1),'impersonal_values':evalw(twin2)},
 'source_custody_pass':source['pass'],
 'source_locator_count':source['locator_count'],
 'source_truth_established':source['source_truth_established'],
 'arabic_primary_verified':source['arabic_primary_verified'],
 'model_neutral_transfer_false':model['authority']['neutral_transfer'] is False,
 'pass':not mis and all(x>0 for x in collisions) and rich_mismatch==0 and witnesses['proper_function_without_accuracy']==(True,False,False) and witnesses['accuracy_without_proper_function']==(False,False,False) and witnesses['accurate_proper_but_defeated']==(True,True,False) and witnesses['full_source_package']==(True,True,True) and q1==q2 and evalw(twin1)==(True,True,True) and evalw(twin2)==(False,False,False) and source['pass'] and not source['source_truth_established'] and not source['arabic_primary_verified'] and model['authority']['neutral_transfer'] is False
}
Path(__file__).with_name('PMR-007_DEEP_F_V3_DISTINCT_REREVIEW_RESULTS.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out,indent=2,sort_keys=True))
