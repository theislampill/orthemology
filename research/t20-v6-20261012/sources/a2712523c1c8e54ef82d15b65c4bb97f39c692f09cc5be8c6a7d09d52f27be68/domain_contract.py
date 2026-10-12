"""Read-only domain adapter; no source-level complete-volition predicate.

API-compatible records are NOT thereby wisdom/metaphysics-admissible worlds.
The shifted output function is solely a definition-dependency negative control.
"""
from pathlib import Path
from itertools import product
import importlib.util,sys
path=Path(__file__).resolve().parents[3]/'sovereignty-choice-semantics/reactive-context-extension/src/reactive_context.py'
spec=importlib.util.spec_from_file_location('contract_reactive',path)
model=importlib.util.module_from_spec(spec);sys.modules[spec.name]=model;spec.loader.exec_module(model)


def context(q):
    c=model.Catalogue(('e0','e1'))
    originals={g:model.Original(g) for g in ('A','B')}
    # Defined from supplied intrinsic policies BEFORE evaluating any outcome.
    normal=tuple(model.own_policy(originals[g],q) for g in ('A','B'))
    return {'q':q,'catalogue':c,'target':c.targets[q],'model':model,
            'originals':originals,'normal':normal,'forecast':model.forecast(c,q)}


def ordinary_domain(ctx):
    # This definition neither calls the output function nor tests its value.
    return (ctx['normal'],)


def diagnostic_domain(ctx):
    # Intentions remain q where an act is present. Settings vary over the owned
    # repertoire. None overrides the corresponding policy-required exercise.
    options={g:(None,)+tuple(ctx['originals'][g].issue(ctx['q'],s)
                            for s in ctx['originals'][g].repertoire)
             for g in ('A','B')}
    return tuple(product(options['A'],options['B']))


def policy_conforms(ctx,p):
    # Record/specification agreement, not global numerical act identity.
    return p==ctx['normal']


def success_domain(ctx,domain,f):
    # Deliberately outcome-filtered comparator; not an admissibility warrant.
    return tuple(p for p in domain if f(ctx,p)==ctx['target'])


def outcome(ctx,p):
    return ctx['model'].execute(ctx['catalogue'],*p)['events']


def shifted_outcome(ctx,p):
    # Not a second metaphysical model. Perturb only the observed positive
    # output to expose whether a domain definition secretly filters success.
    events=outcome(ctx,p)
    if not events:return events
    targets=ctx['catalogue'].targets
    return targets[(targets.index(events)+1)%len(targets)]


def profile_key(p):
    return tuple(None if a is None else (a.bearer,int(a.goal),int(a.setting)) for a in p)
