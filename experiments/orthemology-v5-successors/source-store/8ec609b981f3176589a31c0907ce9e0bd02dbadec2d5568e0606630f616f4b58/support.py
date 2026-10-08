"""Test-only independent graph helpers and controlled module loading."""
from importlib import import_module
from itertools import combinations
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT.parent / 'reference-v1'
sys.path.insert(0, str(ROOT))
sys.path.append(str(REFERENCE))
from model import validate_model

class BoundaryCase(unittest.TestCase):
    def module(self, name):
        self.assertTrue((ROOT / (name + '.py')).is_file(),
                        f'missing planned implementation: {name}.py')
        return import_module(name)


def graph_model(rows, priorities=None, rows1=None):
    n, a = len(rows), len(rows[0])
    raw = dict(n_states=n, n_actions=a, initial=0, menus=[list(range(a)) for _ in rows],
               rows=[rows, rows if rows1 is None else rows1],
               priorities=priorities or [[[0] * a for _ in rows] for _ in (0,1)])
    return validate_model(raw)


def subsets(items):
    return tuple(c for k in range(len(items)+1) for c in combinations(items, k))


def end_component(model, theta, pairs):
    """Brute test oracle, independent of finite.component and MEC code."""
    states = {s for s, _ in pairs}
    if not states:
        return False
    edges = {s: set() for s in states}
    for s, a in pairs:
        nexts = {t for t,p in enumerate(model.rows[theta][s][a]) if p > 0}
        if not nexts <= states:
            return False
        edges[s].update(nexts)
    for source in states:
        reached, pending = {source}, [source]
        while pending:
            for target in edges[pending.pop()]:
                if target not in reached:
                    reached.add(target); pending.append(target)
        if reached != states:
            return False
    return True
