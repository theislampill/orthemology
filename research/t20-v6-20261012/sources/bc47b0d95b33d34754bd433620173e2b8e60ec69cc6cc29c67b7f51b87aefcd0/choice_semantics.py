"""Choice quantifiers over an explicit profile domain; no ontology is inferred.

On a Cartesian domain, uniform is ordinary one-step alpha-effectivity. On a
restricted domain it is only slice-relative success, not independently selectable
STIT ability unless the choice-independence condition is separately satisfied.
"""
from itertools import product
from pathlib import Path
import sys

PROVISION = Path(__file__).resolve().parents[2] / 'provision-identity' / 'src'
sys.path.insert(0, str(PROVISION))
from provision_semantics import IntendedAct, execute_intentions


def powerset(values):
    values = tuple(values)
    return tuple(frozenset(x for i, x in enumerate(values) if mask >> i & 1)
                 for mask in range(1 << len(values)))


def rectangle(domain):
    domain = frozenset(domain)
    return bool(domain) and domain == frozenset(product(
        {a for a, _ in domain}, {b for _, b in domain}))


def ability(outcome, a_moves, b_moves, target, domain=None, agent=0):
    if agent not in (0, 1):
        raise ValueError('Expected one of the two agents.')
    full = frozenset(product(a_moves, b_moves))
    domain = full if domain is None else frozenset(domain)
    if not domain <= full:
        raise ValueError('An admissible profile is outside the supplied moves.')
    own = {p[agent] for p in domain}
    peer = {p[1-agent] for p in domain}
    witness = tuple(s for s in own if all(outcome(*p) == target
                                        for p in domain if p[agent] == s))
    return {
        'joint': any(outcome(*p) == target for p in domain),
        'reactive': bool(peer) and all(any(p[1-agent] == t and outcome(*p) == target
                                         for p in domain) for t in peer),
        'uniform': bool(witness),
        'uniform_witnesses': witness,
        'independent_domain': rectangle(domain),
        'settled_target': bool(domain) and all(outcome(*p) == target for p in domain),
    }


def inherited_run(a, b):
    acts = (IntendedAct('A', 'fixed-A', frozenset(a)),
            IntendedAct('B', 'fixed-B', frozenset(b)))
    events, support, rules, satisfaction = execute_intentions(acts)
    return {
        'output': frozenset(key for key, state in events),
        'support': support,
        'entire': {e: frozenset(g for g in ('A', 'B') if roots == frozenset((g,)))
                   for e, roots in support.items()},
        'rules': rules,
        'intentions': satisfaction,
    }


def inherited_output(a, b):
    return inherited_run(a, b)['output']


def exact_guaranteeing_commands(commands, peer_domain, target):
    peer_domain = tuple(peer_domain)
    if not peer_domain:
        return ()
    return tuple(s for s in commands
                 if all(inherited_output(s, t) == target for t in peer_domain))
