"""Executed finite service/migration model with common-root fault enumeration.

Operational supports are calculated from transitions, never supplied as an input.
External-world fidelity of the chosen semantics remains an application premise.
"""
from dataclasses import dataclass
from itertools import combinations, product
from pathlib import Path
import importlib.util
import json


ROOTS = ("archive", "engine", "state", "grant", "builder", "reserve")
NEEDED = frozenset({"engine", "state", "grant", "builder"})
REQUESTS = ("read", "toggle", "intruder-toggle")
WORDS = [w for n in range(3) for w in product(REQUESTS, repeat=n)]
STEP_COUNT = 0


def powerset(xs):
    return [frozenset(c) for n in range(len(xs) + 1) for c in combinations(xs, n)]


def resources(roots, mode="decoupled"):
    bundles = {r: {r} for r in ROOTS}
    bundles["archive"] = {"evidence"} | (set(NEEDED) if mode == "atomic_bundles" else set())
    bundles["reserve"] = set(NEEDED) | {"evidence"}
    return frozenset().union(*(bundles[r] for r in roots))


def encode(value, encoding):
    return value if encoding == "direct" else 1 - value


def decode(value, encoding):
    return value if encoding == "direct" else 1 - value


@dataclass
class Token:
    identity: int
    encoding: str
    data: int | None
    live: bool = True
    failed: bool = False
    mode: str = "normal"
    copied_lineage_label: str = ""


class Unavailable(Exception):
    pass


class World:
    def __init__(self, initial):
        self.tokens = {0: Token(0, "direct", initial)}
        self.active = 0
        self.events = [dict(kind="genesis", endpoint=0, value=initial)]
        self.initial = initial

    def read_state(self, token, available):
        if self.tokens.get(token.identity) is not token:
            raise Unavailable("supplied token is not this world's registered endpoint")
        if not token.live or token.failed or token.data is None or not {"engine", "state"} <= available:
            raise Unavailable("live encoded state and engine required")
        return decode(token.data, token.encoding)

    def migrate(self, parent, encoding, available):
        if not {"builder", "grant"} <= available or self.active != parent.identity:
            raise Unavailable("constructor and current exclusive transfer authority required")
        actual = self.read_state(parent, available)
        identity = max(self.tokens) + 1
        child = Token(identity, encoding, encode(actual, encoding))
        self.tokens[identity] = child
        # This event is emitted by the executed constructor and bound to its actual endpoint.
        self.events.append(dict(kind="migrate", parent=parent.identity, endpoint=identity,
                                source_value=actual, encoded_value=child.data, encoding=encoding))
        self.active = identity
        parent.live, parent.data = False, None
        return child

    def independent_twin(self, initial, encoding):
        identity = max(self.tokens) + 1
        twin = Token(identity, encoding, encode(initial, encoding), copied_lineage_label="claims-parent-0")
        self.tokens[identity] = twin
        self.events.append(dict(kind="independent-install", endpoint=identity, value=initial))
        # An independent service may have its own lawful appointment. No migration event is emitted.
        self.active = identity
        return twin

    def descends_from(self, endpoint, predecessor):
        parents = {e["endpoint"]: e["parent"] for e in self.events if e["kind"] == "migrate"}
        current = endpoint
        while current in parents:
            current = parents[current]
            if current == predecessor:
                return True
        return False

    def bearer(self, endpoint):
        return "Successor-" + str(endpoint)

    def is_current_successor(self, endpoint):
        # Charter judgement is separate from operation/resource sufficiency.
        return (endpoint in self.tokens and self.active == endpoint
                and self.tokens[endpoint].live and self.descends_from(endpoint, 0))

    def step(self, token, request, available):
        global STEP_COUNT
        STEP_COUNT += 1
        value = self.read_state(token, available)
        if "grant" not in available or self.active != token.identity:
            raise Unavailable("current allocation and exercise capability required")
        if request == "read":
            return ("value", value)
        if request == "intruder-toggle":
            return ("denied", value)
        if request != "toggle":
            raise ValueError(request)
        new = value if token.mode == "stale-write" else 1 - value
        token.data = encode(new, token.encoding)
        self.events.append(dict(kind="toggle", endpoint=token.identity, before=value, after=new))
        if token.mode == "fails-after-write":
            token.failed = True
        return ("value", new)


def specification(value, request):
    if request == "toggle":
        return 1 - value, ("value", 1 - value)
    if request == "intruder-toggle":
        return value, ("denied", value)
    return value, ("value", value)


def word_correct(world, token, value, word, available):
    for request in word:
        value, expected = specification(value, request)
        actual = world.step(token, request, available)
        if actual != expected or world.read_state(token, available) != value:
            return False, value
    return True, value


def service_contract(roots, mode="decoupled", mutation="normal", include_renewal=True):
    """Universal finite requests; first migration precedes the damage event.

    Fixed installed state is generated from each real source state. Damage then
    removes resources. Two-request service and an actual second handoff are tested.
    """
    available = resources(roots, mode)
    full = resources(ROOTS)
    for initial, first_encoding, first_word in product((0, 1), ("direct", "inverse"), WORDS):
        next_words = WORDS if include_renewal else [()]
        for next_word in next_words:
            world = World(initial)
            original = world.tokens[0]
            child = world.migrate(original, first_encoding, full)
            child.mode = mutation
            try:
                if world.read_state(child, available) != initial:
                    return False
                ok, value = word_correct(world, child, initial, first_word, available)
                if not ok:
                    return False
                if include_renewal:
                    second_encoding = "inverse" if first_encoding == "direct" else "direct"
                    grandchild = world.migrate(child, second_encoding, available)
                    if child.live or child.data is not None or world.read_state(grandchild, available) != value:
                        return False
                    if not world.descends_from(grandchild.identity, 0):
                        return False
                    ok, _ = word_correct(world, grandchild, value, next_word, available)
                    if not ok:
                        return False
            except Unavailable:
                return False
    return True


def old_grounded_module():
    path = Path(__file__).resolve().parents[2] / "testimony-continuation/grounded-attestation/grounded_support.py"
    spec = importlib.util.spec_from_file_location("retained_t20_grounded", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def epistemic_supports():
    # Historical q: the registrar's witnessed genesis recorded state 0 or 1.
    # Each root is an already adequate authenticated record route; reliability
    # and interpretation are fixed background premises, not measured here.
    ground = old_grounded_module()
    base = [("archive", "authentic-archive-record"), ("reserve", "authentic-live-record")]
    rules = [(("authentic-archive-record",), "historical-q"),
             (("authentic-live-record",), "historical-q")]
    return ground.minimal_supports(base, rules)["historical-q"]


def minimal_true(table):
    return frozenset(s for s, v in table.items() if v and not any(t < s and tv for t, tv in table.items()))


def serial(family):
    return sorted((sorted(s) for s in family), key=lambda s: (len(s), s))


def profile(mode):
    subsets = powerset(ROOTS)
    e = epistemic_supports()
    direct = {a: service_contract(a, mode) for a in subsets}
    operational = minimal_true(direct)
    surviving = lambda a: any(s <= a for s in e)
    implication = all(not surviving(a) or direct[a] for a in subsets)
    cover = all(any(c <= s for c in operational) for s in e)
    violations = [a for a in subsets if surviving(a) and not direct[a]]
    monotone = all(not direct[a] or direct[b] for a in subsets for b in subsets if a <= b)
    assert all(direct[a] == any(c <= a for c in operational) for a in subsets)
    assert implication == cover
    return dict(name=mode, retained_sets_checked=len(subsets), epistemic_supports=serial(e),
                operational_supports=serial(operational), direct_implication=implication,
                support_cover=cover, operational_monotonicity=monotone,
                failing_retained_sets=serial(violations),
                rows=[dict(available=sorted(a), evidence=surviving(a), operation=direct[a]) for a in subsets])


def run_cases():
    global STEP_COUNT
    STEP_COUNT = 0
    rows = []
    def check(name, actual, expected):
        rows.append(dict(name=name, actual=bool(actual), expected=expected))
    profiles = [profile("decoupled"), profile("atomic_bundles")]
    full = resources(ROOTS)
    world = World(1)
    predecessor = world.tokens[0]
    child = world.migrate(predecessor, "inverse", full)
    check("ordinary_positive_migration_executes_service_and_next_migration", service_contract(ROOTS), True)
    check("retired_parent_is_not_operative_support", predecessor.data is None and not predecessor.live, True)
    check("lineage_bound_to_executed_constructor_endpoint", world.descends_from(child.identity, predecessor.identity), True)
    check("lawful_temporarily_unavailable_successor_keeps_office", world.is_current_successor(child.identity) and not service_contract({"archive"}), True)
    twin_world = World(1)
    twin = twin_world.independent_twin(1, "inverse")
    check("twin_matches_current_output", twin_world.read_state(twin, full) == world.read_state(child, full), True)
    for word in WORDS:
        w1, w2 = World(1), World(1)
        c1 = w1.migrate(w1.tokens[0], "inverse", full)
        c2 = w2.independent_twin(1, "inverse")
        out1 = [w1.step(c1, x, full) for x in word]
        out2 = [w2.step(c2, x, full) for x in word]
        assert out1 == out2
    check("twin_matches_every_declared_behavioral_word", True, True)
    check("copied_lineage_label_does_not_create_transfer_event", twin_world.descends_from(twin.identity, 0), False)
    migration_outputs, twin_outputs = [], []
    for initial in (0, 1):
        w = World(initial)
        c = w.migrate(w.tokens[0], "inverse", full)
        migration_outputs.append(w.read_state(c, full))
        tw = World(initial)
        t = tw.independent_twin(1, "inverse")
        twin_outputs.append(tw.read_state(t, full))
    intervention = dict(source_states=[0, 1], migrated_outputs=migration_outputs,
                        fixed_twin_outputs=twin_outputs, migrated_tracks_parent=migration_outputs == [0, 1],
                        fixed_twin_tracks_parent=twin_outputs == [0, 1])
    check("preserved_archive_cannot_supply_operation", service_contract({"archive"}), False)
    check("lost_constructor_blocks_next_handoff", service_contract({"archive", "engine", "state", "grant"}), False)
    check("same_profile_retains_two_request_service_without_renewal", service_contract({"archive", "engine", "state", "grant"}, include_renewal=False), True)
    check("copied_grant_without_live_exercise_capability_is_insufficient", service_contract({"archive", "engine", "state", "builder"}), False)
    check("same_readout_delayed_failure_is_detected", service_contract(ROOTS, mutation="fails-after-write"), False)
    delayed_world = World(0)
    delayed = delayed_world.migrate(delayed_world.tokens[0], "inverse", full)
    delayed.mode = "fails-after-write"
    first_ok = delayed_world.step(delayed, "toggle", full) == ("value", 1)
    try:
        delayed_world.step(delayed, "read", full)
        second_available = True
    except Unavailable:
        second_available = False
    check("first_mutation_succeeds_but_next_request_fails", first_ok and not second_available, True)
    check("stale_write_realiser_is_detected", service_contract(ROOTS, mutation="stale-write"), False)
    try:
        world.migrate(predecessor, "direct", full)
        duplicate_allowed = True
    except Unavailable:
        duplicate_allowed = False
    check("retired_parent_cannot_allocate_second_exclusive_successor", duplicate_allowed, False)
    # Equal minimum cut size, different identities: neither scalar decides implication.
    e, op = [frozenset({"a"})], [frozenset({"b"})]
    ecut = min(len(d) for d in powerset(("a", "b")) if all(d & s for s in e))
    ocut = min(len(d) for d in powerset(("a", "b")) if all(d & s for s in op))
    check("equal_cut_size_does_not_imply_support_cover", ecut == ocut and not all(any(c <= s for c in op) for s in e), True)
    # Outside fail-stop optional resources: presence of a malicious mandatory
    # controller can break monotonicity. Minimal successes then overpredict.
    nonmonotone = {a: service_contract(ROOTS if "engine" in a else (),
                                       mutation="stale-write" if "hostile-controller" in a else "normal")
                   for a in powerset(("engine", "hostile-controller"))}
    minima = minimal_true(nonmonotone)
    bad_superset = frozenset({"engine", "hostile-controller"})
    check("nonmonotone_mandatory_controller_defeats_minimal_support_representation",
          any(c <= bad_superset for c in minima) and not nonmonotone[bad_superset], True)
    return dict(cases=rows, profiles=profiles, parent_intervention=intervention,
                executed_request_steps=STEP_COUNT, words_per_service_phase=len(WORDS), initial_states=2,
                realiser_encodings=["direct", "inverse"], horizons=dict(requests_per_phase=2, actual_migrations=2),
                example_causal_trace=world.events,
                limitations=["Transitions are executed in a finite reference model, not an empirical deployment.",
                             "Trusted constructor/registrar semantics and external-world authentication are distinct premises.",
                             "Atomic bundle availability is an optional co-survival assumption, not a warranted present-readiness claim.",
                             "The constitutional office-continuity judgement is separate from the operational predicate."])


if __name__ == "__main__":
    print(json.dumps(run_cases(), indent=2))
