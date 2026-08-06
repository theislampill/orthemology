from itertools import product
from pathlib import Path
import json

OUT=Path(__file__).with_name(Path(__file__).stem+'_results.json')

# Boolean deterministic response functions over 4 cells (f,c) in lexicographic order.
functions=[]
for bits in product([0,1],repeat=4):
    functions.append(bits)

def val(fn,f,c): return fn[2*f+c]

def form_invariant(fn):
    return all(val(fn,0,c)==val(fn,1,c) for c in [0,1])

def content_sensitive(fn):
    return any(val(fn,f,0)!=val(fn,f,1) for f in [0,1])

def content_mediated(fn): return form_invariant(fn) and content_sensitive(fn)

def form_mediated(fn):
    return all(val(fn,f,0)==val(fn,f,1) for f in [0,1]) and any(val(fn,0,c)!=val(fn,1,c) for c in [0,1])

classification_counts={'content_mediated':0,'form_mediated':0,'constant':0,'interaction_or_mixed':0}
for fn in functions:
    if content_mediated(fn): classification_counts['content_mediated']+=1
    elif form_mediated(fn): classification_counts['form_mediated']+=1
    elif len(set(fn))==1: classification_counts['constant']+=1
    else: classification_counts['interaction_or_mixed']+=1

# Diagonal observational profiles and collisions across classifications.
profiles={}
for fn in functions:
    p=(val(fn,0,0),val(fn,1,1))
    profiles.setdefault(p,[]).append(fn)
diagonal_collision_pairs=0
semantic_form_collision=False
sem=(0,1,0,1) # y=c: indices 00,01,10,11
frm=(0,0,1,1) # y=f
if (val(sem,0,0),val(sem,1,1))==(val(frm,0,0),val(frm,1,1)) and sem!=frm:
    semantic_form_collision=True
for fs in profiles.values():
    for i in range(len(fs)):
        for j in range(i+1,len(fs)):
            if content_mediated(fs[i]) != content_mediated(fs[j]):
                diagonal_collision_pairs+=1

# Full table uniquely identifies every deterministic function.
full_table_collisions=len(functions)-len(set(functions))

# Deletion of any one cell can create a content-mediation classification collision.
deleted_cell_failures=0; deletion_witnesses=[]
for missing in range(4):
    found=False
    for a in functions:
        for b in functions:
            if content_mediated(a)==content_mediated(b): continue
            if all(a[i]==b[i] for i in range(4) if i!=missing):
                found=True
                deletion_witnesses.append({'missing_cell':missing,'a':a,'b':b})
                break
        if found: break
    if not found: deleted_cell_failures+=1

res={
 'schema':'pmr007-deep-az-crossed-semantic-primary-check-v1-results',
 'boolean_response_functions':len(functions),
 'classification_counts':classification_counts,
 'diagonal_profiles':len(profiles),
 'diagonal_cross_class_collision_pairs':diagonal_collision_pairs,
 'semantic_form_diagonal_collision':semantic_form_collision,
 'full_table_collisions':full_table_collisions,
 'single_cell_deletion_failures':deleted_cell_failures,
 'deletion_witnesses':[{'missing_cell':w['missing_cell'],'a':list(w['a']),'b':list(w['b'])} for w in deletion_witnesses],
 'overall':'PASS' if semantic_form_collision and diagonal_collision_pairs>0 and full_table_collisions==0 and deleted_cell_failures==0 else 'FAIL'
}
OUT.write_text(json.dumps(res,indent=2,sort_keys=True)+'\n')
print(json.dumps(res,indent=2,sort_keys=True))
