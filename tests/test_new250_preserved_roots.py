"""Check finite authenticated NEW250 wiring, not a replacement source proof."""
import ast
import pathlib
import types
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]


def probe(source, status='D', authenticated=True, declared=True):
    tree = ast.parse(source)
    fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'check_preserved_roots')
    path = 'experiments/orthemology-v5-continuations/source-store/test.lean'
    ns = {name.id: set() for name in ast.walk(fn) if isinstance(name, ast.Name) and name.id.isupper()}
    ns.update(BASE='baseline', MEDIATOR_GUIDE='other', SUCCESSOR_INPUT_REGISTRY='other',
              SUCCESSOR_CALCULUS_MAP='other', CONTINUATION_COPY_ROOT='not-this/',
              HISTORICAL_PROSE={}, NEW250_PATHS={path} if declared else set(),
              continuation_owners=types.SimpleNamespace(PRESERVATION_OWNER_PATHS=set()),
              readonly_git_diff=lambda *a: types.SimpleNamespace(returncode=0, stdout=(status+'\0'+path+'\0').encode()),
              status_record_candidate=lambda p: False, binding_record_candidate=lambda p: False,
              mediator_guide_source_bytes=lambda *a, **k: None,
              t10_navigation_edition=lambda *a: set(), foundations_navigation_edition=lambda *a: set(),
              t08_navigation_edition=lambda *a: set())
    calls=[]
    def authenticate(root):
        calls.append(True)
        if not authenticated:
            raise ValueError('invalid exact receiver')
        return {path}
    ns['new250_absences']=authenticate
    exec(compile(ast.Module(body=[fn],type_ignores=[]),'preserved-roots','exec'),ns)
    return ns['check_preserved_roots'](ROOT,{}),calls


class New250AdmissionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source=(ROOT/'scripts/validate_t20_v6_projection.py').read_text()
    def test_authenticated_deletion(self):
        errors,calls=probe(self.source)
        self.assertEqual(errors,[])
        self.assertEqual(len(calls),1)
    def test_failed_authentication_rejects(self):
        errors,calls=probe(self.source,authenticated=False)
        self.assertTrue(errors)
        self.assertEqual(len(calls),1)
    def test_undeclared_deletion_rejects_without_call(self):
        errors,calls=probe(self.source,declared=False)
        self.assertTrue(errors)
        self.assertEqual(calls,[])
    def test_modification_rejects_without_call(self):
        errors,calls=probe(self.source,status='M')
        self.assertTrue(errors)
        self.assertEqual(calls,[])
    def test_type_change_rejects_without_call(self):
        errors,calls=probe(self.source,status='T')
        self.assertTrue(errors)
        self.assertEqual(calls,[])

if __name__=='__main__': unittest.main()
