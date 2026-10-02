#!/usr/bin/env python3
"""Independent exact replay using nonnegative slack identities, not LP matrices.

Uses no optimizer or author module. Paths are derived from tree edges. All
rejections use explicit checks, remaining active under python -O.
"""
from fractions import Fraction as Q
from math import comb,lcm
from pathlib import Path
import copy
import hashlib
import json
import re


def require(test,reason):
    if not test:
        raise ValueError(reason)


def rational(text):
    require(isinstance(text,str) and re.fullmatch(r"-?\d+(?:/[1-9]\d*)?",text) is not None,"noncanonical rational input")
    return Q(text)


def integer(value,reason):
    require(type(value) is int,reason)
    return value


def scenario(u,rank):
    """Combinatorial unranking, independent of author's combinations list."""
    require(type(rank) is int and 0<=rank<comb(u,4),"scenario out of range")
    out=[];start=0
    for remaining in range(4,0,-1):
        for candidate in range(start,u-remaining+1):
            count=comb(u-candidate-1,remaining-1)
            if rank<count:
                out.append(candidate);start=candidate+1;break
            rank-=count
        else:
            raise ValueError("scenario unranking failed")
    require(rank==0,"unranking residual")
    return tuple(out)


def slack(u,pos,path):
    """Return d-Ax >= 0 as a constant and sparse symbolic coefficients."""
    target=Q(2,u-2)
    if pos<3*u:
        j,i=divmod(pos,u)
        return target,{(j,i):Q(-1)}
    if pos<4*u-1:
        i=pos-3*u
        return Q(0),{(0,i):Q(1),(0,i+1):Q(-1)}
    if pos<6*u-1:
        j,i=divmod(pos-(4*u-1),u)
        return Q(0),{(0,0):Q(1),(j+1,i):Q(-1)}
    if pos==6*u-1:
        return -Q(2,u),{"risk":Q(1)}
    index=pos-6*u
    require(0<=index<len(path),"dual constraint index out of range")
    c,j=path[index]
    coeff={(j,i):Q(-1) for i in scenario(u,c)};coeff["risk"]=Q(1)
    return Q(0),coeff


def verify_data(data):
    u=integer(data["u"],"noninteger universe")
    require(u in (6,8,10,12) and data["b"]==4 and data["M"]==3,"wrong certificate domain")
    target=Q(2,u-2)
    require(rational(data["target"])==target,"wrong claimed target")
    nodes=data["nodes"];require(isinstance(nodes,list) and nodes,"missing root")
    pending=[(0,())];seen={};leaf_bounds=[];max_depth=0;denominator=1;terms_checked=0;coefficient_checks=0
    while pending:
        idx,derived_path=pending.pop()
        integer(idx,"noninteger child")
        require(0<=idx<len(nodes),"child outside tree")
        if idx in seen:
            require(seen[idx]==derived_path,"shared node with different domains")
            continue
        seen[idx]=derived_path;max_depth=max(max_depth,len(derived_path))
        node=nodes[idx]
        expected=[[c,j] for c,j in derived_path]
        require(node["path"]==expected,"stored path differs from edge-derived domain")
        if "certificate" not in node:
            require(set(node)=={"path","branch_scenario","children"},"invalid internal node")
            c=integer(node["branch_scenario"],"noninteger branch scenario")
            scenario(u,c)
            require(c not in {s for s,j in derived_path},"scenario assigned twice")
            children=node["children"]
            require(isinstance(children,list) and len(children)==3,"missing message branch")
            require(all(type(k) is int for k in children) and len(set(children))==3,"duplicate or invalid child")
            for j,child in enumerate(children):
                pending.append((child,tuple(sorted(derived_path+((c,j),)))))
            continue
        require(set(node)=={"path","certificate"},"invalid leaf node")
        cert=node["certificate"]
        require(set(cert)=={"inequality_dual","equality_dual","lower_bound"},"invalid certificate fields")
        total_constant=Q(0)
        coeff={(j,i):Q(0) for j in range(3) for i in range(u)};coeff["risk"]=Q(0)
        used=set();multipliers=[]
        for pair in cert["inequality_dual"]:
            require(isinstance(pair,list) and len(pair)==2,"malformed dual term")
            pos=integer(pair[0],"noninteger dual index")
            require(0<=pos<6*u+len(derived_path) and pos not in used,"duplicate or out-of-range dual index")
            used.add(pos)
            weight=-rational(pair[1]);require(weight>=0,"negative slack weight")
            constant,polynomial=slack(u,pos,derived_path)
            total_constant+=weight*constant
            for variable,value in polynomial.items():
                coeff[variable]+=weight*value
            multipliers.append(weight);terms_checked+=1
        eq=cert["equality_dual"]
        require(isinstance(eq,list) and len(eq)==3,"wrong equality multiplier count")
        eq=[rational(x) for x in eq]
        for j,z in enumerate(eq):
            for i in range(u):
                coeff[(j,i)]+=z
        # In t-B = weighted inequality slacks + z*(row sums-1)
        #          + nonnegative coordinate remainders + constant gap,
        # all non-equality summands must be nonnegative on the node domain.
        remainder={variable:Q(variable=="risk")-value for variable,value in coeff.items()}
        bound=sum(eq)-total_constant
        require(bound==rational(cert["lower_bound"]),"stored bound not derived")
        require(bound>=target,"leaf does not close below-target domain")
        scale=lcm(*(v.denominator for v in [target,bound,total_constant,*coeff.values(),*remainder.values(),*eq]))
        for variable,value in remainder.items():
            scaled=value*scale
            require(scaled.denominator==1 and scaled.numerator>=0,"negative coordinate remainder")
            require((coeff[variable]+value)*scale==int(variable=="risk")*scale,"integer polynomial coefficient identity failed")
            coefficient_checks+=1
        require((total_constant-sum(eq)+(bound-target))*scale==-target*scale,"integer polynomial constant identity failed")
        require((bound-target)*scale>=0,"negative constant gap")
        denominator=max(denominator,*(v.denominator for v in multipliers+eq))
        leaf_bounds.append(bound)
    require(len(seen)==len(nodes),"unreachable nodes")
    require(len(nodes)==data["node_count"] and len(leaf_bounds)==data["leaf_count"],"incorrect payload counts")
    require(leaf_bounds,"no leaves")
    return {"u":u,"target":str(target),"nodes":len(nodes),"leaves":len(leaf_bounds),
            "minimum_leaf_bound":str(min(leaf_bounds)),"maximum_depth":max_depth,
            "max_dual_denominator":denominator,"slack_terms_checked":terms_checked,
            "integer_coordinate_identities":coefficient_checks}


def run(source):
    source=Path(source);results=[]
    for u in (6,8,10,12):
        raw=(source/f"EXACT_SENDER_TREE_u{u}.json").read_bytes()
        data=json.loads(raw);result=verify_data(data);result["certificate_sha256"]=hashlib.sha256(raw).hexdigest();results.append(result)
    base=json.loads((source/"EXACT_SENDER_TREE_u8.json").read_text())
    leaf=next(i for i,n in enumerate(base["nodes"]) if "certificate" in n)
    mutations={}
    def register(name,change):
        mutant=copy.deepcopy(base);change(mutant)
        try:
            verify_data(mutant)
        except (ValueError,KeyError,TypeError,IndexError) as error:
            mutations[name]=str(error)
        else:
            raise ValueError("mutation accepted: "+name)
    register("missing_message_branch",lambda d:d["nodes"][0]["children"].pop())
    register("swapped_child_domains",lambda d:d["nodes"][0]["children"].reverse())
    register("missing_root_domain",lambda d:d["nodes"][0]["path"].append([0,0]))
    register("positive_original_dual",lambda d:d["nodes"][leaf]["certificate"]["inequality_dual"][0].__setitem__(1,"1"))
    register("invented_objective_bound",lambda d:d["nodes"][leaf]["certificate"].__setitem__("lower_bound","1"))
    register("invalid_scenario",lambda d:d["nodes"][0].__setitem__("branch_scenario",comb(8,4)))
    register("wrong_target",lambda d:d.__setitem__("target","1/4"))
    register("unreachable_node",lambda d:d["nodes"].append(copy.deepcopy(d["nodes"][leaf])))
    register("duplicate_dual_index",lambda d:d["nodes"][leaf]["certificate"]["inequality_dual"].append(d["nodes"][leaf]["certificate"]["inequality_dual"][0][:]))
    register("nonrational_dual",lambda d:d["nodes"][leaf]["certificate"]["inequality_dual"][0].__setitem__(1,"nan"))
    register("zero_dual_leaf",lambda d:d["nodes"][leaf].__setitem__("certificate",{"inequality_dual":[],"equality_dual":["0"]*3,"lower_bound":"0"}))
    # Provenance labels and solver flags deliberately do not participate.
    untrusted=copy.deepcopy(base);untrusted["exact_proof_complete"]=False
    untrusted["pending_nodes"]=999;untrusted["base_inequality_keys"]=[["invented"]]
    require(verify_data(untrusted)==verify_data(base),"generator metadata affected mathematical acceptance")
    from itertools import combinations
    scenario_count=0
    for u in (6,8,10,12):
        for rank,expected in enumerate(combinations(range(u),4)):
            require(scenario(u,rank)==expected,"independent unranking differs from lexicographic corruption scenarios")
            scenario_count+=1
    return {"status":"PASS","scope":"Exact independent slack-identity certificate replay, conditional on the inspected model reduction",
            "certificates":results,"mutation_rejections":mutations,"provenance_ignored_control":"PASS",
            "scenario_unranking_checks":scenario_count,"optimizer_imports":False}


if __name__=="__main__":
    print(json.dumps(run(Path(__file__).resolve().parent/"source"),indent=2,sort_keys=True))
