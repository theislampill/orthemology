"""Hash-pinned reuse of approved helpers from the unchanged sibling reference.

Only the exported helpers below are used by the polynomial production path.
Loading synthesis defines its exhaustive functions; it does not execute them.
Conflicting already-imported generic module names are rejected, never replaced.
"""
import hashlib
import importlib
from pathlib import Path
import sys

REFERENCE = Path(__file__).resolve().parent.parent / 'reference-v1'
PINNED_SHA256 = {
    'model': '81e01e552e6ebb455f381a81f2568aa08d5b233522bda53d23c8b930d023c823',
    'finite': '50c7a6dbb1f72b9907886eacd2ad04941ff803e01703b8968ef699cfa1e8fae1',
    'certificates': 'a75e325dd879bab3ab392b4a467e12b93716ee33eebec61d30ba668fbdd1e41c',
    'synthesis': '94c0445a5979171ed5eba929ac75a88f02e1685f41701ee21d809f4b628bde09',
    'controller': '777a95bf89caa09b4c0c4c9274e4b5aa3b7371d63ea9a92c313e7bffba8be003',
}


def verify_dependencies():
    """Verify full files before importing any frozen helper; raise on mismatch."""
    actual = {}
    for name, expected in PINNED_SHA256.items():
        path = REFERENCE / (name + '.py')
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != expected:
            raise ImportError('frozen reference hash mismatch: ' + path.name)
        actual[name] = digest
        module = sys.modules.get(name)
        if module is not None and Path(getattr(module, '__file__', '')).resolve() != path:
            raise ImportError('conflicting imported module: ' + name)
    return actual


verify_dependencies()
sys.path.insert(0, str(REFERENCE))
_model = importlib.import_module('model')
_finite = importlib.import_module('finite')
_certificates = importlib.import_module('certificates')
_synthesis = importlib.import_module('synthesis')

Model, validate_model, natural = _model.Model, _model.validate_model, _model.natural
checked_pairs, checked_region = _finite.checked_pairs, _finite.checked_region
safe_known, safe_uncertain, used = _finite.safe_known, _finite.safe_uncertain, _finite.used
Positive, Negative, Route = _certificates.Positive, _certificates.Negative, _certificates.Route
check_positive = _certificates.check_positive
record, sequence, canonical = _certificates.record, _certificates.sequence, _certificates.canonical
shortest_route = _synthesis.shortest_route
