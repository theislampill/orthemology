#!/usr/bin/env python3
"""Small first-order natural-deduction certificate checker.

This is a shipped, inspectable checker, not Lean or an independently audited
kernel. Its rules are standard classical natural deduction. It checks formal
inference from the EXACT displayed assumptions, not their metaphysical truth.
All variables and constants have explicit sorts; no function symbols are used.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any
import json
from pathlib import Path

class ProofError(ValueError):
    pass


def freeze(x: Any) -> Any:
    return tuple(map(freeze, x)) if isinstance(x, (list, tuple)) else x


def term_sort(t):
    if not isinstance(t, tuple) or len(t) != 3 or t[0] not in ('var','const'):
        raise ProofError('malformed term')
    return t[1]


def fv(f):
    tag = f[0]
    if tag == 'atom':
        return {t for t in f[2:] if t[0] == 'var'}
    if tag == 'bot':
        return set()
    if tag in ('and','imp'):
        return fv(f[1]) | fv(f[2])
    if tag in ('forall','exists'):
        return fv(f[2]) - {f[1]}
    raise ProofError('unknown formula constructor')


def sub(f, old, new):
    if term_sort(old) != term_sort(new):
        raise ProofError('sort-changing substitution')
    tag = f[0]
    if tag == 'atom':
        return ('atom', f[1], *(new if t == old else t for t in f[2:]))
    if tag == 'bot':
        return f
    if tag in ('and','imp'):
        return (tag, sub(f[1],old,new), sub(f[2],old,new))
    if tag in ('forall','exists'):
        if f[1] == old:
            return f
        if f[1] == new and old in fv(f[2]):
            raise ProofError('capturing substitution')
        return (tag, f[1], sub(f[2],old,new))
    raise ProofError('bad substitution')


def valid_formula(f, sig):
    tag = f[0]
    if tag == 'atom':
        if f[1] not in sig or len(f)-2 != len(sig[f[1]]):
            raise ProofError('predicate signature mismatch')
        if tuple(term_sort(t) for t in f[2:]) != tuple(sig[f[1]]):
            raise ProofError('predicate sort mismatch')
    elif tag == 'bot':
        if len(f) != 1:
            raise ProofError('malformed bottom')
    elif tag in ('and','imp'):
        if len(f) != 3:
            raise ProofError('malformed connective')
        valid_formula(f[1],sig); valid_formula(f[2],sig)
    elif tag in ('forall','exists'):
        if len(f) != 3 or f[1][0] != 'var':
            raise ProofError('malformed quantifier')
        term_sort(f[1]); valid_formula(f[2],sig)
    else:
        raise ProofError('unknown constructor')


@dataclass
class Judgement:
    conclusion: tuple
    assumptions: dict[str, tuple]


def merge(*js):
    out = {}
    for j in js:
        for label, f in j.assumptions.items():
            if label in out and out[label] != f:
                raise ProofError('assumption label changed meaning')
            out[label] = f
    return out


def discharge(j, label, expected):
    if label not in j.assumptions or j.assumptions[label] != expected:
        raise ProofError('invalid discharge')
    return {k:v for k,v in j.assumptions.items() if k != label}


def check(certificate):
    sig = certificate['signature']
    nodes = []
    used_rules = set()
    for ix, raw in enumerate(certificate['proof']):
        rule = raw['rule']; used_rules.add(rule)
        args = freeze(raw.get('args', []))
        refs = raw.get('premises', [])
        if any(not isinstance(i,int) or i < 0 or i >= ix for i in refs):
            raise ProofError('premise must be an earlier node')
        ps = [nodes[i] for i in refs]
        def need(k):
            if len(ps) != k:
                raise ProofError('wrong premise count')
        if rule == 'hyp':
            need(0); label, f = args
            valid_formula(f,sig)
            j = Judgement(f, {label:f})
        elif rule == 'andI':
            need(2); j = Judgement(('and',ps[0].conclusion,ps[1].conclusion),merge(*ps))
        elif rule in ('andL','andR'):
            need(1)
            if ps[0].conclusion[0] != 'and': raise ProofError('not conjunction')
            j = Judgement(ps[0].conclusion[1 if rule=='andL' else 2], merge(*ps))
        elif rule == 'impE':
            need(2)
            f = ps[0].conclusion
            if f[0] != 'imp' or f[1] != ps[1].conclusion: raise ProofError('modus ponens mismatch')
            j = Judgement(f[2],merge(*ps))
        elif rule == 'impI':
            need(1); label, antecedent = args
            j = Judgement(('imp',antecedent,ps[0].conclusion),discharge(ps[0],label,antecedent))
        elif rule == 'forallE':
            need(1); (t,) = args; f = ps[0].conclusion
            if f[0] != 'forall': raise ProofError('not universal')
            j = Judgement(sub(f[2],f[1],t),merge(*ps))
        elif rule == 'forallI':
            need(1); (v,) = args
            if v[0] != 'var': raise ProofError('not eigenvariable')
            if any(v in fv(f) for f in ps[0].assumptions.values()):
                raise ProofError('universal introduction has a dependent assumption')
            j = Judgement(('forall',v,ps[0].conclusion),merge(*ps))
        elif rule == 'existsI':
            need(1); v, body, t = args
            if v[0] != 'var' or sub(body,v,t) != ps[0].conclusion:
                raise ProofError('existential witness mismatch')
            j = Judgement(('exists',v,body),merge(*ps))
        elif rule == 'existsE':
            need(2); fresh, label = args; ex = ps[0].conclusion
            if ex[0] != 'exists' or fresh[0] != 'var': raise ProofError('invalid existential elimination')
            witness = sub(ex[2],ex[1],fresh)
            outer = discharge(ps[1],label,witness)
            combined = merge(ps[0],Judgement(ps[1].conclusion,outer))
            if fresh in fv(ps[1].conclusion) or fresh in fv(ex):
                raise ProofError('existential eigenvariable escaped')
            if any(fresh in fv(f) for f in combined.values()):
                raise ProofError('existential eigenvariable in open context')
            j = Judgement(ps[1].conclusion,combined)
        elif rule == 'raa':
            need(1); label, target = args
            if ps[0].conclusion != ('bot',): raise ProofError('RAA needs contradiction')
            j = Judgement(target,discharge(ps[0],label,('imp',target,('bot',))))
        else:
            raise ProofError('unlicensed proof rule')
        valid_formula(j.conclusion,sig)
        if 'conclusion' in raw and freeze(raw['conclusion']) != j.conclusion:
            raise ProofError('declared conclusion differs from computed conclusion')
        nodes.append(j)
    if not nodes:
        raise ProofError('empty proof')
    final = nodes[-1]
    if final.conclusion != freeze(certificate['conclusion']):
        raise ProofError('wrong final conclusion')
    if final.assumptions != {k:freeze(v) for k,v in certificate['assumptions'].items()}:
        raise ProofError('undischarged or missing premise')
    return {'name':certificate['name'], 'nodes':len(nodes), 'rules':sorted(used_rules),
            'assumption_labels':sorted(final.assumptions), 'status':'PASS'}


def negative_controls(certs):
    """Adversarial examples authored separately from the certificate generator."""
    import copy
    candidates = []
    for c in certs:
        bad = copy.deepcopy(c); bad['conclusion'] = ['bot']
        candidates.append(('altered target: '+c['name'], bad))
    w = ('var','world','w'); x = ('var','entity','x'); a = ('var','entity','a')
    q = ('atom','Q',w); p = ('atom','P',a)
    candidates.append(('illicit universal generalisation',dict(
        name='bad',signature={'Q':['world']},assumptions={'h':q},
        proof=[dict(rule='hyp',args=['h',q]),dict(rule='forallI',args=[w],premises=[0])],
        conclusion=('forall',w,q))))
    ex = ('exists',x,('atom','P',x))
    candidates.append(('existential witness escape',dict(
        name='bad',signature={'P':['entity']},assumptions={'ex':ex},
        proof=[dict(rule='hyp',args=['ex',ex]),dict(rule='hyp',args=['hp',p]),
               dict(rule='existsE',args=[a,'hp'],premises=[0,1])],conclusion=p)))
    universal = ('forall',x,('atom','P',x))
    candidates.append(('world/entity sort substitution',dict(
        name='bad',signature={'P':['entity']},assumptions={'h':universal},
        proof=[dict(rule='hyp',args=['h',universal]),dict(rule='forallE',args=[w],premises=[0])],
        conclusion=('atom','P',w))))
    capture = ('forall',x,('forall',a,('atom','D',x,a)))
    candidates.append(('variable capture',dict(
        name='bad',signature={'D':['entity','entity']},assumptions={'h':capture},
        proof=[dict(rule='hyp',args=['h',capture]),dict(rule='forallE',args=[a],premises=[0])],
        conclusion=('forall',a,('atom','D',a,a)))))
    bad = copy.deepcopy(certs[0]); del bad['assumptions']['root_exists']
    candidates.append(('undisclosed open premise',bad))
    bad = copy.deepcopy(certs[0]); bad['proof'][7]['premises'] = [6,5]
    candidates.append(('modus ponens antecedent mismatch',bad))
    bad = copy.deepcopy(certs[0]); bad['proof'][0]['rule'] = 'oracle'
    candidates.append(('unlicensed oracle rule',bad))
    bad = copy.deepcopy(certs[0]); bad['proof'][6]['conclusion'] = ['bot']
    candidates.append(('dishonest intermediate conclusion',bad))
    rows=[]
    for name,bad in candidates:
        try: check(bad)
        except ProofError as err:
            rows.append({'control':name,'status':'REJECTED','reason':str(err)})
        else: raise AssertionError('accepted invalid proof: '+name)
    return rows


def main():
    here = Path(__file__).resolve().parent
    certs = json.loads((here/'proof_certificates.json').read_text())
    rows = [check(c) for c in certs]
    controls = negative_controls(certs)
    data = {'status':'PASS','certificates':rows,'negative_controls_rejected':len(controls),
            'negative_controls':controls,
            'authority':'local natural-deduction checker; not Lean, independently reviewed, or premise-truth verification'}
    (here/'proof_check_results.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(data,indent=2))

if __name__ == '__main__': main()
