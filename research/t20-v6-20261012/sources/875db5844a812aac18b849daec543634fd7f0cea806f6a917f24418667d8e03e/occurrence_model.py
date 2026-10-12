"""Controlled-language occurrence transport. No natural-language/authentication oracle."""
from dataclasses import dataclass, replace
from itertools import product
import json


@dataclass(frozen=True)
class Context:
    speaker: str
    addressee: str
    time: int
    place: str


@dataclass(frozen=True)
class Occurrence:
    event: str
    context: Context
    force: str  # Assert, Quote, Directive belong to THIS occurrence
    formula: tuple
    domain: str = "service-duty"


@dataclass(frozen=True)
class Carrier:
    event: str
    context: Context
    current_force: str
    reported_event: str
    original_context: Context
    original_force: str
    encoding: str
    payload: str


def freeze(x):
    return tuple(freeze(y) for y in x) if isinstance(x, list) else x


def encode(formula, language):
    if language == "A":
        return json.dumps(formula, separators=(",", ":"))
    if language != "B":
        raise ValueError("unknown controlled encoding")
    def go(f):
        tag, *args = f
        if tag == "and":
            return {"both": [go(args[0]), go(args[1])]}
        if tag == "not":
            return {"negated": go(args[0])}
        if tag == "at":
            return {"located": {"who": args[0], "where": args[1], "when": args[2]}}
        if tag == "duty":
            return {"obligation": dict(zip(("bearer", "act", "start", "duration"), args))}
        raise ValueError(tag)
    return json.dumps(go(formula), sort_keys=True, separators=(",", ":"))


def decode(payload, language):
    x = json.loads(payload)
    if language == "A":
        return freeze(x)
    if language != "B":
        raise ValueError("unknown controlled encoding")
    def go(v):
        if "both" in v:
            return ("and", go(v["both"][0]), go(v["both"][1]))
        if "negated" in v:
            return ("not", go(v["negated"]))
        if "located" in v:
            a = v["located"]
            return ("at", a["who"], a["where"], a["when"])
        a = v["obligation"]
        return ("duty", a["bearer"], a["act"], a["start"], a["duration"])
    return go(x)


def resolve(f, c):
    person = lambda s: c.speaker if s == "I" else c.addressee if s == "you" else s
    instant = lambda t: c.time if t == "now" else t
    if f[0] == "at":
        return ("at", person(f[1]), c.place if f[2] == "here" else f[2], instant(f[3]))
    if f[0] == "duty":
        start = instant(f[3])
        return ("duty", person(f[1]), f[2], start, start + f[4])
    if f[0] == "not":
        return ("not", resolve(f[1], c))
    if f[0] == "and":
        return ("and", resolve(f[1], c), resolve(f[2], c))
    raise ValueError(f[0])


def truth(p, true_atoms):
    if p[0] == "and":
        return truth(p[1], true_atoms) and truth(p[2], true_atoms)
    if p[0] == "not":
        return not truth(p[1], true_atoms)
    return p in true_atoms


def relay(o, language="B"):
    return Carrier("carrier-" + o.event, Context("Relay", "Learner", 10, "archive"),
                   "Quote", o.event, o.context, o.force, language, encode(o.formula, language))


def preservation(o, carrier):
    # Context equality also preserves source-attribution coordinates absent from a formula.
    return (carrier.reported_event == o.event and carrier.original_context == o.context
            and carrier.original_force == o.force
            and resolve(decode(carrier.payload, carrier.encoding), carrier.original_context)
            == resolve(o.formula, o.context))


@dataclass(frozen=True)
class RecipientPremises:
    authenticated_events: frozenset
    veracious_source_domains: frozenset
    semantic_adequacy: bool = True
    testimony_admissible: bool = True
    undefeated: bool = True


@dataclass(frozen=True)
class Attestation:
    rule_event: str
    owner: str
    carrier: str
    domain: str
    start: int
    end: int
    force: str = "Assert"


def prospective_owner(o, rule, grounded_rules, actual_role_occupancy, revoked=False):
    # grounded_rules is supplied independently of the candidate message and its metadata.
    if (rule.rule_event in grounded_rules and not revoked and actual_role_occupancy
            and o.context.speaker == rule.carrier and o.domain == rule.domain
            and o.force == rule.force and rule.start <= o.context.time < rule.end):
        return rule.owner
    return None


def warranted(o, carrier, premises, owner=None):
    source = owner if owner is not None else o.context.speaker
    if (o.force == "Assert" and preservation(o, carrier)
            and o.event in premises.authenticated_events
            and (source, o.domain) in premises.veracious_source_domains
            and premises.semantic_adequacy and premises.testimony_admissible and premises.undefeated):
        return resolve(o.formula, o.context)
    return None


def actionable(proposition, recipient, now, implementation):
    return bool(proposition and proposition[0] == "duty" and proposition[1] == recipient
                and proposition[3] <= now < proposition[4] and implementation)


def directive_duty(o, standing_at_original_occurrence):
    # A constitutive route, explicitly different from testimony about an existing duty.
    if o.force == "Directive" and standing_at_original_occurrence:
        return resolve(o.formula, o.context)
    return None


def run_cases():
    rows = []
    def check(name, actual, expected):
        rows.append(dict(name=name, actual=bool(actual), expected=expected))
    c = Context("Principal", "Operator", 0, "lab")
    duty = ("duty", "you", "inspect", "now", 2)
    o = Occurrence("source-duty-0", c, "Assert", duty)
    packet = relay(o)
    p = RecipientPremises(frozenset({o.event}), frozenset({("Principal", "service-duty")}))
    q = warranted(o, packet, p)
    check("different_encoding_same_contextual_proposition", encode(duty, "A") != packet.payload and q == resolve(duty, c), True)
    check("carrier_quote_retains_original_assertion", packet.current_force == "Quote" and q is not None, True)
    check("new_carrier_occurrence_is_not_original", packet.event == o.event, False)
    check("historical_duty_needs_no_current_grant_or_duplicate_jurisdiction", q is not None, True)
    check("old_duty_still_applicable_within_interval", actionable(q, "Operator", 1, True), True)
    check("old_duty_does_not_rebind_to_later_now", actionable(q, "Operator", 10, True), False)
    check("old_duty_does_not_rebind_to_new_recipient", actionable(q, "Learner", 1, True), False)
    check("warrant_does_not_supply_actuator", actionable(q, "Operator", 1, False), False)
    for name, changed in [("now", replace(c, time=10)), ("you", replace(c, addressee="Learner"))]:
        copied = replace(packet, original_context=changed)
        check("unchanged_words_changed_" + name + "_reject_transport", preservation(o, copied), False)
        check("changed_" + name + "_has_different_proposition", resolve(duty, c) != resolve(duty, changed), True)
    at = ("at", "I", "here", "now")
    at_o = Occurrence("location-0", c, "Assert", at)
    for name, changed in [("I", replace(c, speaker="Relay")), ("here", replace(c, place="archive")), ("now", replace(c, time=1))]:
        original, rebound = resolve(at, c), resolve(at, changed)
        check("discriminating_valuation_" + name, truth(original, {original}) and not truth(rebound, {original}), True)
    quote = replace(o, event="quoted-duty", force="Quote")
    quote_p = replace(p, authenticated_events=frozenset({quote.event}))
    check("source_quote_is_not_its_assertoric_endorsement", warranted(quote, relay(quote), quote_p) is not None, False)
    directive = replace(o, event="directive-0", force="Directive")
    dp = replace(p, authenticated_events=frozenset({directive.event}))
    check("bare_directive_is_not_truthful_duty_assertion", warranted(directive, relay(directive), dp) is not None, False)
    check("directive_with_original_standing_can_institute_duty", directive_duty(directive, True) is not None, True)
    check("directive_without_original_standing_does_not_institute_duty", directive_duty(directive, False) is not None, False)
    check("quoted_directive_does_not_become_assertion", preservation(directive, replace(relay(directive), original_force="Assert")), False)
    check("internally_matching_fabrication_lacks_independent_anchor", warranted(o, packet, replace(p, authenticated_events=frozenset())) is not None, False)
    check("semantic_adequacy_is_application_premise", warranted(o, packet, replace(p, semantic_adequacy=False)) is not None, False)
    check("veracity_scope_is_application_premise", warranted(o, packet, replace(p, veracious_source_domains=frozenset())) is not None, False)
    check("defeater_blocks_special_route", warranted(o, packet, replace(p, undefeated=False)) is not None, False)
    new = Occurrence("new-attested-1", Context("Successor", "Operator", 1, "lab"), "Assert", duty)
    rule = Attestation("independently-established-rule", "Principal", "Successor", "service-duty", 1, 3)
    grounded = frozenset({rule.rule_event})
    owner = prospective_owner(new, rule, grounded, True)
    np = replace(p, authenticated_events=frozenset({new.event}))
    check("bounded_prospective_attestation_owns_new_proposition", owner == "Principal" and warranted(new, relay(new), np, owner) is not None, True)
    check("new_attestation_is_not_alias_of_old_assertion", new.event != o.event and resolve(new.formula, new.context) != q, True)
    check("general_employee_without_adoption_rule", prospective_owner(new, rule, frozenset(), True) is not None, False)
    check("self_asserted_rule_does_not_anchor_itself", prospective_owner(new, rule, frozenset({new.event}), True) is not None, False)
    check("out_of_domain_report_not_adopted", prospective_owner(replace(new, domain="finance"), rule, grounded, True) is not None, False)
    check("out_of_interval_report_not_adopted", prospective_owner(replace(new, context=replace(new.context, time=3)), rule, grounded, True) is not None, False)
    check("quote_not_adopted_by_assertion_rule", prospective_owner(replace(new, force="Quote"), rule, grounded, True) is not None, False)
    check("office_label_without_actual_occupancy_insufficient", prospective_owner(new, rule, grounded, False) is not None, False)
    check("revocation_blocks_future_adoption", prospective_owner(new, rule, grounded, True, True) is not None, False)
    check("revocation_does_not_retroactively_erase_old_testimony", warranted(o, packet, p) == q, True)
    atoms = [at, duty, ("at", "Principal", "lab", 0), ("duty", "Operator", "inspect", 0, 2)]
    formulas = atoms + [("not", a) for a in atoms] + [("and", a, b) for a, b in product(atoms, repeat=2)]
    contexts = [Context(s, a, t, place) for s, a, t, place in product(("Principal", "Relay"), ("Operator", "Learner"), (0, 1), ("lab", "archive"))]
    total = 0
    for f, context, language in product(formulas, contexts, ("A", "B")):
        assert decode(encode(f, language), language) == f
        assert resolve(decode(encode(f, language), language), context) == resolve(f, context)
        total += 1
    return dict(cases=rows, roundtrip_cases=total, discriminating_valuation=all(r["actual"] for r in rows if r["name"].startswith("discriminating_valuation")),
                historical_proposition=q, adopted_new_proposition=resolve(new.formula, new.context),
                limits=["Controlled formal languages, not natural-language translation certification.",
                        "Authentication, epistemic adequacy, veracity, and actual office occupancy are application premises.",
                        "Failure of the special-source route does not deny ordinary defeasible testimony."])


if __name__ == "__main__":
    print(json.dumps(run_cases(), indent=2))
