"""Exact-state normalization of a supplied guarded proof DAG.

This is not a minimum-cost DAG optimizer. Guards and rule records are the
unchanged inherited guarded-tree contract; only node accounting differs.
"""
from dataclasses import dataclass
from pathlib import Path
import importlib.util
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent

def load_source(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

guarded = load_source('inherited_guarded', 'source-sensitive-proof-compilation-20261009/guarded_compiler.py')
unguarded = load_source('inherited_unguarded', 'certificate-compilation-boundary-20261009/compiler.py')
Rule = guarded.Rule

@dataclass(frozen=True)
class Dag:
    nodes: tuple
    root: int

def normalize(dag, judgements, evidence, rules):
    judgements,evidence,rules=tuple(judgements),tuple(evidence),tuple(rules)
    original=dag_value(dag,judgements,evidence,rules)
    states=original[5]
    earliest={}
    for i,state in enumerate(states):
        earliest.setdefault(state,i)

    # Every representative remains its original rule occurrence. References
    # target the earliest occurrence of the ORIGINAL child's exact state.
    redirected={i:tuple(earliest[states[j]] for j in dag.nodes[i][1])
                for i in earliest.values()}
    assert all(j<i for i,refs in redirected.items() for j in refs)
    root=earliest[states[dag.root]]
    reachable,stack=set(),[root]
    while stack:
        i=stack.pop()
        if i not in reachable:
            reachable.add(i)
            stack.extend(redirected[i])
    kept=sorted(reachable)
    index={old:new for new,old in enumerate(kept)}
    result=Dag(tuple((dag.nodes[i][0],tuple(index[j] for j in redirected[i]))
                     for i in kept),index[root])
    value=dag_value(result,judgements,evidence,rules)
    assert value[:2]==original[:2]
    assert value[2]<=original[2]
    assert len(set(value[5]))==len(result.nodes)
    assert len(result.nodes)<=len(judgements)*2**len(evidence)
    return result

def dag_value(dag, judgements, evidence, rules):
    """Check admission, ordered supports, acyclicity and full reachability.

    Returns root judgement, exact root support, once-per-node cost, branch
    height, node count, and the exact states of all premise-first nodes.
    This is grammar-internal validation, not source authentication/soundness.
    """
    judgements,evidence,rules=tuple(judgements),tuple(evidence),tuple(rules)
    guarded._validate(judgements,evidence,rules)
    if (not isinstance(dag.nodes,tuple) or type(dag.root) is not int
            or not 0<=dag.root<len(dag.nodes)):
        raise ValueError('Missing root or malformed node catalogue.')
    states,heights=[],[]
    for i,node in enumerate(dag.nodes):
        if not isinstance(node,tuple) or len(node)!=2:
            raise ValueError('Malformed node.')
        rule,refs=node
        if rule not in rules:
            raise ValueError('Rule is not admitted in this grammar.')
        if (not isinstance(refs,tuple) or len(refs)!=len(rule.premises)
                or any(type(j) is not int or not 0<=j<i for j in refs)):
            raise ValueError('Malformed premise references or cyclic indexing.')
        if tuple(states[j][0] for j in refs)!=rule.premises:
            raise ValueError('Wrong scoped premise judgement.')
        ss=tuple(states[j][1] for j in refs)
        if rule.allowed is not None and ss not in rule.allowed:
            raise ValueError('Ordered exact supports fail the rule guard.')
        states.append((rule.head,rule.support.union(*ss)))
        heights.append(1+max((heights[j] for j in refs),default=0))
    reachable,stack=set(),[dag.root]
    while stack:
        i=stack.pop()
        if i not in reachable:
            reachable.add(i)
            stack.extend(dag.nodes[i][1])
    if reachable!=set(range(len(dag.nodes))):
        raise ValueError('Unreachable nodes are not part of a rooted certificate.')
    return (*states[dag.root],sum(r.cost for r,_ in dag.nodes),
            heights[dag.root],len(dag.nodes),tuple(states))
