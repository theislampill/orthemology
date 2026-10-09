"""Separate primitive joint-law rival, NOT the inherited union interpreter.

Goal is exact intended CREATED target; setting identifies the intrinsic exercise
whose SOLO output is that target code. Goal and setting may differ in contextual
means selection. Codes index nonempty event sets; zero is an active setting.
None is absence of exercise, not an outcome label or a created object.
"""
from dataclasses import dataclass, field
from itertools import product

class TargetCode(int):
    """Names an exact intended created-event set in a Catalogue."""

class SettingCode(int):
    """Names an intrinsic exercise by its solo-output code, not its intention."""

@dataclass(frozen=True)
class Exercise:
    bearer: str
    goal: TargetCode
    setting: SettingCode

    def __post_init__(self):
        object.__setattr__(self, 'goal', TargetCode(self.goal))
        object.__setattr__(self, 'setting', SettingCode(self.setting))

    @property
    def token(self):
        return self.bearer + '_act'

@dataclass(frozen=True)
class Original:
    bearer: str
    repertoire: tuple[int, ...] = (0, 1, 2)
    power_token: str = field(init=False)
    knowledge_token: str = field(init=False)

    def __post_init__(self):
        object.__setattr__(self, 'power_token', self.bearer + '_P')
        object.__setattr__(self, 'knowledge_token', self.bearer + '_K')

    def issue(self, goal, setting):
        if setting not in self.repertoire:
            raise ValueError('Exercise is outside this bearer’s standing repertoire.')
        return Exercise(self.bearer, goal, setting)

class Catalogue:
    def __init__(self, events):
        events = tuple(events)
        if not events or len(set(events)) != len(events):
            raise ValueError('Expected a nonempty, duplicate-free event catalogue.')
        self.targets = tuple(frozenset(e for i,e in enumerate(events) if mask >> i & 1)
                             for mask in range(1, 1 << len(events)))
        self.n = len(self.targets)
        self.half = (self.n + 1) // 2  # inverse of 2 mod odd n

    def valid(self, setting):
        return isinstance(setting, int) and 0 <= setting < self.n

    def combine(self, a, b):
        if any(x is not None and not self.valid(x) for x in (a,b)):
            raise ValueError('Setting outside the operational catalogue.')
        if a is None: return b
        if b is None: return a
        return (self.half * (a + b)) % self.n

    def respond(self, q, b):
        if not self.valid(q) or (b is not None and not self.valid(b)):
            raise ValueError('Goal or peer setting outside the catalogue.')
        return q if b is None else (2*q - b) % self.n


def execute(c, a, b):
    if a is not None and a.bearer != 'A': raise ValueError('A-slot mismatch.')
    if b is not None and b.bearer != 'B': raise ValueError('B-slot mismatch.')
    acts = tuple(x for x in (a,b) if x is not None)
    if any(not c.valid(x.goal) for x in acts): raise ValueError('Invalid goal.')
    out = c.combine(None if a is None else a.setting, None if b is None else b.setting)
    events = frozenset() if out is None else c.targets[out]
    # Each event has ONE direct production from the actual positive intrinsic
    # inputs. No earlier created emissions, mixer, or cancellation events exist
    # in this declared ontology. That is a substantive interpretation, not a
    # claim about the completeness of a physical causal history.
    roots = frozenset(x.bearer for x in acts)
    proofs = {e: {'schema':'direct-from-active-exercises',
                   'intrinsic_inputs':tuple(x.token for x in acts),
                   'created_inputs':(), 'positive_roots':roots}
              for e in events}
    supports = {e:p['positive_roots'] for e,p in proofs.items()}
    intentions = {x.bearer: events == c.targets[x.goal] for x in acts}
    own_ends = {x.bearer: intentions[x.bearer] and bool(events)
                and all(x.bearer in supports[e] for e in events) for x in acts}
    return {'events':events, 'acts':acts, 'proofs':proofs, 'supports':supports,
            'created_history':tuple(sorted(events)), 'intentions':intentions,
            'own_activity_ends':own_ends,
            'entire':{e:frozenset(g for g in ('A','B') if s == frozenset((g,)))
                      for e,s in supports.items()}}


def own_policy(original, q):
    # Same disclosed own-full-target selection premise as the earlier rival.
    # The peer's ACTUAL exercise is not an input. Its normative warrant remains
    # open; mere optimality of the output does not derive this policy uniquely.
    return original.issue(goal=q, setting=q)


def forecast(c, q):
    # Compute from assumed known intrinsic policies and the law BEFORE receiving
    # actual execution. This is primitive reason-based knowledge representation,
    # not an efficient donation from a peer action or created product.
    return execute(c, own_policy(Original('A',tuple(range(c.n))),q), own_policy(Original('B',tuple(range(c.n))),q))


def response_pairs(c, qa, qb):
    # Solve simultaneously. Neither player is silently ordered after the other.
    return tuple((a,b) for a,b in product(range(c.n),repeat=2)
                 if a == c.respond(qa,b) and b == c.respond(qb,a))


def has_foreign_donor(attribute, bearer, efficient_edges):
    backwards = {}
    for a,b in efficient_edges: backwards.setdefault(b,set()).add(a)
    pending = [attribute]; ancestors = set()
    while pending:
        for parent in backwards.get(pending.pop(),set()):
            if parent not in ancestors:
                ancestors.add(parent); pending.append(parent)
    foreign = 'B_' if bearer == 'A' else 'A_'
    return any(x.startswith(foreign) for x in ancestors)


def epistemic_model(c):
    originals = {g:Original(g,tuple(range(c.n))) for g in ('A','B')}
    worlds = []
    for q in range(c.n):
        forecasts = {g:forecast(c,q) for g in originals}
        actual = execute(c, own_policy(originals['A'],q), own_policy(originals['B'],q))
        efficient_edges = tuple((g+'_act',e) for e,roots in actual['supports'].items() for g in sorted(roots))
        worlds.append({'context':q, 'originals':originals, 'forecasts':forecasts,
                       'actual':actual, 'efficient_edges':efficient_edges,
                       'accessible':tuple(j for j in range(c.n) if j==q)})
    return {'originals':originals, 'worlds':worlds,
            'inherence':tuple((token,g) for g,o in originals.items()
                              for token in (o.power_token,o.knowledge_token)),
            'scope':'Reason-context alternatives, not alternatives under a fully fixed necessary nature. Inherence, intrinsic reasons and factive truth-relations are not efficient donation edges.'}
