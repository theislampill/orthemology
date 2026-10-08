"""Finite graph predicates. Row equality always means the complete exact row."""
from model import natural

Pair = tuple[int, int]


def checked_pairs(model, pairs):
    result = tuple(pairs)
    for pair in result:
        if type(pair) is not tuple or len(pair) != 2:
            raise ValueError('invalid pair')
        s, a = pair
        natural(s, model.n_states); natural(a, model.n_actions)
        if a not in model.menus[s]:
            raise ValueError('unlawful pair')
    if len(set(result)) != len(result):
        raise ValueError('duplicate pair')
    return result


def used(pairs):
    return frozenset(s for s, _ in pairs)


def reachable(model, source, pairs, theta, compatible_only=False):
    natural(source, model.n_states); natural(theta, 2)
    pairs = checked_pairs(model, pairs)
    reached = {source}
    pending = [source]
    while pending:
        s = pending.pop()
        for x, a in pairs:
            if x != s:
                continue
            for y, p in enumerate(model.rows[theta][s][a]):
                if p and (not compatible_only or model.rows[0][s][a][y]) and y not in reached:
                    reached.add(y); pending.append(y)
    return frozenset(reached)


def component(model, theta, pairs, uncertain=False):
    try:
        natural(theta, 2)
        pairs = checked_pairs(model, pairs)
    except (ValueError, TypeError):
        return False
    if not pairs:
        return False
    sources = used(pairs)
    for s, a in pairs:
        for y, p in enumerate(model.rows[theta][s][a]):
            if p and (y not in sources or (uncertain and not model.rows[0][s][a][y])):
                return False
    if any(not sources <= reachable(model, s, pairs, theta) for s in sources):
        return False
    if not uncertain:
        return theta == 1 and min(model.priorities[1][s][a] for s, a in pairs) % 2 == 0
    for rival in (0, 1):
        if all(model.rows[rival][s][a] == model.rows[theta][s][a] for s, a in pairs):
            if min(model.priorities[rival][s][a] for s, a in pairs) % 2:
                return False
    return True


def all_components(model, theta, pairs, uncertain=False):
    """Exhaustive subset search; exponential, with no resource-failure fallback."""
    from itertools import combinations
    pairs = tuple(sorted(checked_pairs(model, pairs)))
    return tuple(sorted(subset for size in range(1, len(pairs) + 1)
                        for subset in combinations(pairs, size)
                        if component(model, theta, subset, uncertain)))


def checked_region(model, region):
    return frozenset(natural(s, model.n_states) for s in region)


def safe_known(model, region):
    region = checked_region(model, region)
    return tuple((s, a) for s in sorted(region) for a in model.menus[s]
                 if all(not p or y in region for y, p in enumerate(model.rows[1][s][a])))


def safe_uncertain(model, known, region):
    known, region = checked_region(model, known), checked_region(model, region)
    return tuple((s, a) for s in sorted(region) for a in model.menus[s]
                 if all((not p0 or y in region) and (not p1 or p0 or y in known)
                        for y, (p0, p1) in enumerate(zip(model.rows[0][s][a], model.rows[1][s][a]))))
