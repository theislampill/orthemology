"""Reason-dependent necessary-choice restriction over the existing action menu.

The participation rule uses end syntax, never evaluated outcome success.
It is not a sufficient-reason derivation, a universal rationality norm, a
source-level CompleteWill predicate, or a proof of metaphysical admissibility.
"""
from itertools import product
from joint_end import Model


def participation_options(ctx,subject,content):
    """Local action options; never choose or guarantee the peer's action.

    Product-only makes no own-activity demand. Both old own-activity and richer
    joint-activity contain that demand. Rich content earns no additional local
    restriction over own-activity. Every standing active setting is retained.
    """
    if content not in {'product','own','joint'}:raise ValueError(content)
    original=ctx['originals'][subject]
    active=tuple(original.issue(ctx['q'],setting) for setting in original.repertoire)
    return (None,)+active if content=='product' else active


def policy_domain(ctx,content,use_inherited_means):
    """Compose two declared local policies, not all metaphysically possible choices.

    The optional means stage reuses the old q-setting recipe. It is an extra
    selection premise, not derived from the richer relation or the source.
    """
    menus=[]
    for subject in ('A','B'):
        menu=participation_options(ctx,subject,content)
        if use_inherited_means:
            inherited=Model.own_policy(ctx['originals'][subject],ctx['q'])
            menu=tuple(a for a in menu if a is None or a==inherited)
        menus.append(menu)
    return tuple(product(*menus))


def evaluate_profile(ctx,profile,content):
    """Evaluate only AFTER policy-domain construction; diagnostic cuts are allowed."""
    a,b=profile; base=Model.execute(ctx['catalogue'],a,b)
    q=ctx['q']; expected=ctx['catalogue'].targets[q]
    product_ok=base['events']==expected
    active={x.bearer:x for x in base['acts']}
    own={g:g in active and active[g].goal==q and bool(base['events']) and
         all(g in roots for roots in base['supports'].values()) for g in ('A','B')}
    joint=all(own.values())
    if content=='product':ends={g:product_ok for g in ('A','B')}
    elif content=='own':ends={g:product_ok and own[g] for g in ('A','B')}
    elif content=='joint':ends={g:product_ok and joint for g in ('A','B')}
    else:raise ValueError(content)
    return {'base':base,'product_satisfied':product_ok,'goal_directed_coproduction':joint,
            'individual_ends':ends,'stated_end_satisfied':all(ends.values())}
