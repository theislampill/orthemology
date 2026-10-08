"""Validate the submitted body itself, independently of witness synthesis."""
from dataclasses import dataclass, fields
from model import natural, validate_model
from finite import component, used


@dataclass(frozen=True)
class Route:
    source: int
    steps: tuple
    component: int | None
    reveal: tuple | None


@dataclass(frozen=True)
class Positive:
    K: tuple
    W: tuple
    D1: tuple
    D: tuple
    known_components: tuple
    uncertain_components: tuple
    known_routes: tuple
    uncertain_routes: tuple


def record(raw, cls):
    names = {f.name for f in fields(cls)}
    if type(raw) is cls:
        return {name: getattr(raw, name) for name in names}
    if type(raw) is not dict or set(raw) != names:
        raise ValueError('body fields do not match schema')
    return raw


def sequence(raw, size=None):
    if type(raw) is not tuple or (size is not None and len(raw) != size):
        raise ValueError('certificate sequence must be a tuple of the right size')
    return raw


def canonical(raw, parser):
    result = tuple(parser(item) for item in sequence(raw))
    if result != tuple(sorted(set(result))):
        raise ValueError('finite set is not canonical')
    return result


def pair(raw, n, a):
    s, act = sequence(raw, 2)
    return natural(s, n), natural(act, a)


def parse_route(raw, model):
    data = record(raw, Route)
    source = natural(data['source'], model.n_states)
    steps = tuple(pair(step, model.n_actions, model.n_states) for step in sequence(data['steps']))
    target = data['component']
    if target is not None:
        natural(target)
    reveal = None if data['reveal'] is None else pair(data['reveal'], model.n_actions, model.n_states)
    if (target is None) == (reveal is None):
        raise ValueError('route needs exactly one target kind')
    return Route(source, steps, target, reveal)


def valid_route(model, route, theta, pairs, components, known, uncertain):
    current = route.source
    visited = {current}
    if len(route.steps) >= model.n_states:
        return False
    for a, y in route.steps:
        if (current, a) not in pairs or not model.rows[theta][current][a][y]:
            return False
        if uncertain and not model.rows[0][current][a][y]:
            return False
        if y in visited:
            return False
        visited.add(y); current = y
    if route.component is not None:
        return route.component < len(components) and current in used(components[route.component])
    if not uncertain:
        return False
    a, y = route.reveal
    return ((current, a) in pairs and bool(model.rows[theta][current][a][y])
            and not model.rows[0][current][a][y] and y in known)


def check_positive(model, raw_body):
    """Return a normalized checked body, or None. Never calls solve/search."""
    model = validate_model(model)
    try:
        body = record(raw_body, Positive)
        state_parser = lambda s: natural(s, model.n_states)
        pair_parser = lambda p: pair(p, model.n_states, model.n_actions)
        regions = {name: canonical(body[name], state_parser) for name in ('K', 'W')}
        pairs = {name: canonical(body[name], pair_parser) for name in ('D1', 'D')}
        parse_components = lambda value: canonical(value, lambda c: canonical(c, pair_parser))
        known_components = parse_components(body['known_components'])
        uncertain_components = tuple(parse_components(value) for value in sequence(body['uncertain_components'], 2))
        known_routes = tuple(parse_route(r, model) for r in sequence(body['known_routes']))
        uncertain_routes = tuple(tuple(parse_route(r, model) for r in sequence(value))
                                 for value in sequence(body['uncertain_routes'], 2))
        K, W, D1, D = regions['K'], regions['W'], pairs['D1'], pairs['D']
        if model.initial not in W:
            return None
        for s, a in D1:
            if s not in K or a not in model.menus[s]:
                return None
            if any(p and y not in K for y, p in enumerate(model.rows[1][s][a])):
                return None
        for s, a in D:
            if s not in W or a not in model.menus[s]:
                return None
            for y, (p0, p1) in enumerate(zip(model.rows[0][s][a], model.rows[1][s][a])):
                if (p0 and y not in W) or (p1 and not p0 and y not in K):
                    return None
        if any(not set(c) <= set(D1) or not component(model, 1, c) for c in known_components):
            return None
        for theta in (0, 1):
            if any(not set(c) <= set(D) or not component(model, theta, c, True)
                   for c in uncertain_components[theta]):
                return None
        if tuple(r.source for r in known_routes) != K:
            return None
        if any(not valid_route(model, r, 1, D1, known_components, K, False) for r in known_routes):
            return None
        for theta in (0, 1):
            if tuple(r.source for r in uncertain_routes[theta]) != W:
                return None
            if any(not valid_route(model, r, theta, D, uncertain_components[theta], K, True)
                   for r in uncertain_routes[theta]):
                return None
        return Positive(K, W, D1, D, known_components, uncertain_components, known_routes, uncertain_routes)
    except (ValueError, TypeError, KeyError, IndexError):
        return None


@dataclass(frozen=True)
class Negative:
    k_trace: tuple
    w_trace: tuple


def check_negative(model, raw_body):
    """Recompute every exact update from the full carrier, not just fixedness."""
    from synthesis import known_operator, uncertain_operator
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
