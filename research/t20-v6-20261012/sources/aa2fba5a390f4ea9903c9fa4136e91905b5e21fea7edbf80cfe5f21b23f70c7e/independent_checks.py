"""Independent bounded oracles; reads author modules without writing them.

This is a reviewer model comparison, not a replay of the historical broad suite.
"""
from pathlib import Path
from itertools import combinations, product
from dataclasses import replace
import importlib.util
import json
import sys

HERE = Path(__file__).resolve().parent
AUTHOR = HERE.parent / 'testimony-continuation'

def load(name):
    spec = importlib.util.spec_from_file_location(name, AUTHOR / (name + '.py'))
    obj = importlib.util.module_from_spec(spec)
    sys.modules[name] = obj
    spec.loader.exec_module(obj)
    return obj

def subsets(items):
    return [frozenset(x) for n in range(len(items)+1) for x in combinations(items, n)]

def independent_resolve(f, c):
    substitutions = {'I': c.speaker, 'you': c.addressee, 'here': c.place, 'now': c.time}
    if f[0] == 'at':
        return ('at',) + tuple(substitutions.get(x, x) for x in f[1:])
    if f[0] == 'duty':
        subject = substitutions.get(f[1], f[1]); start = substitutions.get(f[3], f[3])
        return ('duty', subject, f[2], start, start+f[4])
    return (f[0],) + tuple(independent_resolve(x, c) for x in f[1:])

def atoms(f):
    if f[0] in ('at', 'duty'):
        return {f}
    return set().union(*(atoms(x) for x in f[1:]))

def eval_own(f, valuation):
    if f[0] == 'not': return not eval_own(f[1], valuation)
    if f[0] == 'and': return eval_own(f[1], valuation) and eval_own(f[2], valuation)
    return f in valuation

def occurrence_oracle(m):
    a = [('at','I','here','now'), ('duty','you','inspect','now',2), ('at','Principal','lab',0)]
    first = a + [('not', x) for x in a] + [('and', x,y) for x,y in product(a,repeat=2)]
    formulas = a + [('not', x) for x in first] + [('and', x,y) for x,y in product(first,repeat=2)]
    contexts = [m.Context(s,r,t,p) for s,r,t,p in product(('Principal','Relay'),('Operator','Learner'),(0,1),('lab','archive'))]
    count = truth_count = 0
    for f,c,language in product(formulas, contexts, ('A','B')):
        decoded = m.decode(m.encode(f, language), language)
        assert decoded == f
        target = independent_resolve(f,c)
        assert m.resolve(decoded,c) == target
        for valuation in subsets(tuple(atoms(target))):
            assert m.truth(target, valuation) == eval_own(target, valuation)
            truth_count += 1
        count += 1
    distinctions=[]
    base=m.Context('Principal','Operator',0,'lab')
    for label,f,c in [('speaker',a[0],replace(base,speaker='Relay')),
                      ('place',a[0],replace(base,place='archive')),
                      ('time',a[0],replace(base,time=1)),
                      ('duty addressee',a[1],replace(base,addressee='Learner')),
                      ('duty interval',a[1],replace(base,time=1))]:
        p,q=independent_resolve(f,base),independent_resolve(f,c)
        witnesses=[v for v in subsets(tuple(atoms(p)|atoms(q))) if eval_own(p,v)!=eval_own(q,v)]
        assert witnesses
        distinctions.append(label)
    return {'well_formed_roundtrips':count,'truth_valuation_checks':truth_count,'separated_context_changes':distinctions}

REQUESTS=('read','toggle','intruder-toggle')
WORDS=[w for n in range(3) for w in product(REQUESTS,repeat=n)]
ROOTS=('archive','engine','state','grant','builder','reserve')

def own_capabilities(roots,mode):
    out=set(roots)-{'archive','reserve'}
    if 'reserve' in roots or ('archive' in roots and mode=='atomic_bundles'):
        out.update(('engine','state','grant','builder'))
    return out

def own_execute(initial, enc, first, second, caps):
    # First endpoint is installed before removal, as declared by the author.
    def unpack(data,e): return data if e==0 else 1-data
    def pack(value,e): return value if e==0 else 1-value
    data=pack(initial,enc); expected=initial
    if not {'engine','state'} <= caps: return False
    for phase,word in enumerate((first,second)):
        if phase:
            # Actual next construction reads source and retires its local storage.
            if not {'builder','grant','engine','state'} <= caps: return False
            source=unpack(data,enc); old_data=data; data=None
            enc=1-enc; data=pack(source,enc)
            assert old_data in (0,1)
        for request in word:
            if not {'engine','state','grant'} <= caps: return False
            value=unpack(data,enc)
            if request=='toggle':
                value=1-value; expected=1-expected; data=pack(value,enc)
            if unpack(data,enc)!=expected: return False
    return True

def support_oracle(m):
    records=[]; comparisons=0; histories=0; upward_pairs=0
    for mode in ('decoupled','atomic_bundles'):
        author=m.profile(mode)
        own={}
        for roots in subsets(ROOTS):
            caps=own_capabilities(roots,mode)
            passed=True
            for initial,enc,first,second in product((0,1),(0,1),WORDS,WORDS):
                histories+=1
                if not own_execute(initial,enc,first,second,caps):
                    passed=False
            own[roots]=passed
        for row in author['rows']:
            roots=frozenset(row['available'])
            assert row['operation']==own[roots]
            assert row['evidence']==bool({'archive','reserve'} & roots)
            comparisons+=1
        for a,b in product(own,repeat=2):
            if a<=b:
                assert not own[a] or own[b]
                upward_pairs+=1
        minima={a for a,v in own.items() if v and not any(b<a and w for b,w in own.items())}
        assert minima=={frozenset(c) for c in author['operational_supports']}
        records.append({'mode':mode,'operational_supports':sorted(map(sorted,minima)),'implication':author['direct_implication']})
    return {'retained_set_comparisons':comparisons,'oracle_histories_executed':histories,'upward_closure_pairs':upward_pairs,'profiles':records}

def actual_endpoint_checks(m):
    caps=m.resources(m.ROOTS); checks=0
    for initial,encoding in product((0,1),('direct','inverse')):
        world=m.World(initial); parent=world.tokens[0]
        child=world.migrate(parent,encoding,caps)
        assert not parent.live and parent.data is None
        assert world.active==child.identity and world.descends_from(child.identity,0)
        # Intervention on retired parent's state cannot alter successor service.
        parent.data=1-initial; parent.live=True
        assert world.read_state(child,caps)==initial
        assert world.step(child,'toggle',caps)==('value',1-initial)
        assert world.read_state(parent,caps)==1-initial
        assert world.read_state(child,caps)==1-initial
        second=world.migrate(child,'direct' if encoding=='inverse' else 'inverse',caps)
        assert world.descends_from(second.identity,0)
        assert not child.live and child.data is None
        for retired in (parent,child):
            try: world.migrate(retired,'direct',caps)
            except m.Unavailable: pass
            else: raise AssertionError('retired endpoint allocated second child')
        checks+=1
    return {'executed_two_handoff_intervention_cases':checks}

def nonmonotone_control():
    # A conflicting live grant makes a strictly larger retained profile fail.
    u=('engine','conflicting-grant')
    direct={a: 'engine' in a and 'conflicting-grant' not in a for a in subsets(u)}
    minimal={a for a,v in direct.items() if v and not any(b<a and w for b,w in direct.items())}
    bad=[a for a in direct if direct[a] != any(s<=a for s in minimal)]
    assert bad==[frozenset(u)]
    return {'nonmonotone_minimisation_rejected':True,'failed_larger_profile':sorted(bad[0])}

def support_theorem_oracle():
    # Every pair of monotone Boolean predicates on a three-element universe.
    universe=(0,1,2); avail=subsets(universe)
    monotone=[]
    for bits in product((False,True),repeat=len(avail)):
        f=dict(zip(avail,bits))
        if all(not f[a] or f[b] for a in avail for b in avail if a<=b):
            mins={a for a in avail if f[a] and not any(f[b] and b<a for b in avail)}
            monotone.append((f,mins))
    count=0
    for (e,em),(c,cm) in product(monotone,repeat=2):
        all_damage=all(not e[a] or c[a] for a in avail)
        cover=all(any(s<=t for s in cm) for t in em)
        assert all_damage==cover
        count+=1
    return {'monotone_predicates':len(monotone),'predicate_pairs':count,'retained_sets_per_pair':len(avail)}

if __name__=='__main__':
    occ=load('occurrence_model');cont=load('continuation_model')
    result={'occurrence':occurrence_oracle(occ),'service':support_oracle(cont),
            'endpoint':actual_endpoint_checks(cont),'support_characterisation':support_theorem_oracle(),
            'nonmonotone_control':nonmonotone_control()}
    print(json.dumps(result,indent=2))
