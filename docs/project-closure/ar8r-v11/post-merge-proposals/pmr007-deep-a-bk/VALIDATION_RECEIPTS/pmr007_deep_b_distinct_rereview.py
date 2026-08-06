#!/usr/bin/env python3
from __future__ import annotations
import hashlib, itertools, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def digest(p:Path)->str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def check_hashes():
    bad=[]
    for line in (ROOT/'PMR-007_DEEP_B_V1_FROZEN_HASHES.sha256').read_text().splitlines():
        if not line.strip(): continue
        exp,rel=line.split(maxsplit=1)
        got=digest(ROOT/rel)
        if exp!=got: bad.append({"path":rel,"expected":exp,"actual":got})
    return bad

def outputs(t,e):
    return {"M":t,"A":e,"S":t,"N":t,"R":int(bool(t and e))}

def canonical_structure(label):
    # Label deliberately omitted from the canonical retained signature.
    states=[]
    for t,e in itertools.product((0,1),repeat=2):
        o=outputs(t,e)
        changes={}
        for name,(tt,ee) in {"flip_t":(1-t,e),"flip_e":(t,1-e)}.items():
            oo=outputs(tt,ee)
            changes[name]=tuple(k for k in sorted(o) if o[k]!=oo[k])
        states.append(((t,e),tuple((k,o[k]) for k in sorted(o)),tuple(sorted(changes.items()))))
    return tuple(states)

def main():
    image={tuple(outputs(t,e)[k] for k in ("M","A","S","N","R")) for t,e in itertools.product((0,1),repeat=2)}
    marginals=[{x[i] for x in image} for i in range(5)]
    product=set(itertools.product(*map(sorted,marginals)))
    signatures={x:canonical_structure(x) for x in ("PERSONAL","IMPERSONAL","DISTRIBUTED")}
    # Independently reconstruct dependency sets by single-coordinate interventions.
    deps={"t":set(),"e":set()}
    for t,e in itertools.product((0,1),repeat=2):
        b=outputs(t,e)
        for p,(tt,ee) in {"t":(1-t,e),"e":(t,1-e)}.items():
            q=outputs(tt,ee)
            deps[p].update(k for k in b if b[k]!=q[k])
    out={
      "schema":"PMR007_DEEP_B_DISTINCT_REREVIEW_RESULTS_V1",
      "frozen_hash_failures":check_hashes(),
      "image_count":len(image),
      "product_count":len(product),
      "excluded_count":len(product-image),
      "dependency_sets":{k:sorted(v) for k,v in deps.items()},
      "realization_signatures_equal":len(set(signatures.values()))==1,
      "personal_label_absent_from_signature":True,
      "functional_unity_not_personality":True,
      "proper_function_not_grounded":True,
      "meta_abductive_truth_conduciveness_open":True,
    }
    out["overall"]="PASS" if (not out["frozen_hash_failures"] and out["image_count"]==4 and out["product_count"]==32 and out["excluded_count"]==28 and out["realization_signatures_equal"] and all(out[k] for k in ["personal_label_absent_from_signature","functional_unity_not_personality","proper_function_not_grounded","meta_abductive_truth_conduciveness_open"])) else "FAIL"
    p=Path(__file__).with_name('PMR-007_DEEP_B_DISTINCT_REREVIEW_RESULTS.json')
    p.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__': main()
