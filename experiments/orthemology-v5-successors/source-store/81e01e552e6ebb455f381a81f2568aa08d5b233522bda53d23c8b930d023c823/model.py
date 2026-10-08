"""Strict finite input normalization. No numerical approximations."""
from dataclasses import dataclass, fields
from fractions import Fraction


def natural(value, bound=None):
    if type(value) is not int or value < 0 or (bound is not None and value >= bound):
        raise ValueError('expected a natural integer within its bound')
    return value


def array(value, size=None):
    if type(value) not in (tuple, list) or (size is not None and len(value) != size):
        raise ValueError('wrong array type or dimension')
    return value


@dataclass(frozen=True)
class Model:
    n_states: int
    n_actions: int
    initial: int
    menus: tuple
    rows: tuple
    priorities: tuple


def validate_model(raw):
    normalized = type(raw) is Model
    if normalized:
        raw = {f.name: getattr(raw, f.name) for f in fields(Model)}
    if type(raw) is not dict or set(raw) != {f.name for f in fields(Model)}:
        raise ValueError('model fields must match the schema exactly')
    n, a = natural(raw['n_states']), natural(raw['n_actions'])
    if not n or not a:
        raise ValueError('carriers must be nonempty')
    initial = natural(raw['initial'], n)
    menus = []
    for menu in array(raw['menus'], n):
        values = tuple(natural(x, a) for x in array(menu))
        if not values or tuple(sorted(set(values))) != values:
            raise ValueError('menus must be nonempty canonical sets')
        menus.append(values)

    def rational(value):
        if normalized and type(value) is Fraction:
            result = value
        elif type(value) is int:
            result = Fraction(value)
        elif type(value) is str:
            try:
                result = Fraction(value)
            except (ValueError, ZeroDivisionError):
                raise ValueError('invalid rational') from None
            if str(result) != value:
                raise ValueError('rational string is not canonical')
        else:
            raise ValueError('probabilities must be integers or canonical rational strings')
        if result < 0:
            raise ValueError('negative probability')
        return result

    rows = []
    for mode in array(raw['rows'], 2):
        states = []
        for state in array(mode, n):
            actions = []
            for row in array(state, a):
                row = tuple(rational(x) for x in array(row, n))
                if sum(row) != 1:
                    raise ValueError('row is not stochastic')
                actions.append(row)
            states.append(tuple(actions))
        rows.append(tuple(states))
    priorities = tuple(tuple(tuple(natural(x) for x in array(state, a))
                             for state in array(mode, n))
                       for mode in array(raw['priorities'], 2))
    return Model(n, a, initial, tuple(menus), tuple(rows), priorities)
