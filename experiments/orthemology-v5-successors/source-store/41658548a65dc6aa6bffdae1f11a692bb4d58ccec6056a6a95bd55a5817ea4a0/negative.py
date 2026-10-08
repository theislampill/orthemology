"""Original negative-body syntax checked through polynomial exact updates.

No exhaustive reference search, reference negative checker, or solve call is
used. Validity is recomputed from full-carrier starts through every step.
"""
from dependencies import validate_model, natural, record, sequence, canonical, Negative
from efficient import known_operator, uncertain_operator


def check_negative(model, raw_body):
    """Return a normalized checked Negative or None; model errors propagate."""
    model = validate_model(model)
    try:
        data = record(raw_body, Negative)
        parse_trace = lambda raw: tuple(canonical(region, lambda s: natural(s, model.n_states))
                                       for region in sequence(raw))
        kt, wt = parse_trace(data['k_trace']), parse_trace(data['w_trace'])
        full = tuple(range(model.n_states))

        def valid(trace, operator):
            if not 2 <= len(trace) <= model.n_states + 2 or trace[0] != full:
                return False
            for index, (before, after) in enumerate(zip(trace, trace[1:])):
                if tuple(sorted(operator(frozenset(before)))) != after:
                    return False
                if index == len(trace) - 2:
                    if before != after:
                        return False
                elif not set(after) < set(before):
                    return False
            return True

        if not valid(kt, lambda K: known_operator(model, K)):
            return None
        if not valid(wt, lambda W: uncertain_operator(model, frozenset(kt[-1]), W)):
            return None
        if model.initial in wt[-1]:
            return None
        return Negative(kt, wt)
    except (ValueError, TypeError, KeyError, IndexError):
        return None
