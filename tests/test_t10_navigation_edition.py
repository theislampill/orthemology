import ast
import hashlib
from pathlib import Path
import subprocess
import types
import unittest

SOURCE = Path(__file__).resolve().parents[1] / 'scripts/validate_t20_v6_projection.py'
GUIDE = 'experiments/orthemology-v5-successors/groups/t10-technical/README.md'
BASE = '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'
OLD = b'../../source-store/cdff07e133a38347c1a0f5b31787af914c50f3023e6690a42a356ec97ab4e74e/VERIFICATION_NOTE.md'
NEW = b'https://github.com/theislampill/orthemology/blob/27c25b4dc30b1a8b3cb97588aba61482d1d8dcca/experiments/orthemology-v5-successors/source-store/cdff07e133a38347c1a0f5b31787af914c50f3023e6690a42a356ec97ab4e74e/VERIFICATION_NOTE.md'

class NavigationEditionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original = subprocess.check_output(['git', 'show', BASE + ':' + GUIDE])
        cls.adapted = cls.original.replace(OLD, NEW)

    def setUp(self):
        tree = ast.parse(SOURCE.read_text())
        selected = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 't10_navigation_edition']
        self.assertEqual(len(selected), 1)
        self.body = self.adapted
        self.index = b'100644 c7b04b22bcfe5f3e9f3872fb7c6a9daae1fa5e90 0\t' + GUIDE.encode() + b'\0'
        self.bad_target = False
        self.calls = []
        def git(root, *args):
            self.calls.append(args)
            if args[:2] == ('ls-tree', '-z'):
                oid = ('662300a336a3d462c78e512ae7ea66babb72ea91' if args[2] == BASE else
                       ('0' * 40 if self.bad_target else '0b70eebb1bce10f70bdc955e7f1e3284e1f99058'))
                return ('100644 blob ' + oid + '\t' + args[-1] + '\0').encode()
            if args[:2] == ('cat-file', 'blob'):return self.original
            if args[:2] == ('ls-files', '--stage'):return self.index
            raise AssertionError(args)
        self.ns = {'hashlib': hashlib, 'BASE': BASE, 'T10_NAVIGATION_GUIDE': GUIDE,
                   '_administrative_git': git, '_regular_current_bytes': lambda root, path: self.body}
        exec(compile(ast.Module(body=selected, type_ignores=[]), str(SOURCE), 'exec'), self.ns)

    def test_actual_admission_predicate_is_narrow(self):
        function = next(n for n in ast.parse(SOURCE.read_text()).body if isinstance(n, ast.FunctionDef) and n.name == 'check_preserved_roots')
        predicate = next(n.test for n in ast.walk(function) if isinstance(n, ast.If) and isinstance(n.test, ast.Call) and isinstance(n.test.func, ast.Name) and n.test.func.id == 'any' and any(isinstance(x, ast.Name) and x.id == 'navigation_authenticated' for x in ast.walk(n.test)))
        names = {n.id for n in ast.walk(predicate) if isinstance(n, ast.Name)}
        context = {name: set() for name in names - {'any', 'zip', 'status', 'path'}}
        context.update(any=any, zip=zip, changes=['M', GUIDE], navigation_authenticated={GUIDE})
        code = compile(ast.Expression(predicate), '<actual-final-predicate>', 'eval')
        self.assertFalse(eval(code, context))
        context['navigation_authenticated'] = set()
        self.assertTrue(eval(code, context))
        context.update(changes=['M', GUIDE + '.other'], navigation_authenticated={GUIDE})
        self.assertTrue(eval(code, context))
        context.update(changes=['D', GUIDE], navigation_authenticated={GUIDE})
        self.assertTrue(eval(code, context))

    def test_exact_two_link_edition(self):
        self.assertEqual(self.ns['t10_navigation_edition'](Path('.')), {GUIDE})
        self.assertEqual(sum(c[:2] == ('cat-file', 'blob') for c in self.calls), 1)

    def test_extra_prose_rejected(self):
        self.body += b'\nextra prose\n'
        with self.assertRaises(ValueError): self.ns['t10_navigation_edition'](Path('.'))

    def test_bad_target_rejected(self):
        self.bad_target = True
        with self.assertRaises(ValueError): self.ns['t10_navigation_edition'](Path('.'))

    def test_wrong_staged_body_rejected(self):
        self.index = self.index.replace(b'c7b04b22bcfe5f3e9f3872fb7c6a9daae1fa5e90', b'0' * 40)
        with self.assertRaises(ValueError): self.ns['t10_navigation_edition'](Path('.'))

    def test_wrong_staged_mode_rejected(self):
        self.index = self.index.replace(b'100644', b'100755')
        with self.assertRaises(ValueError): self.ns['t10_navigation_edition'](Path('.'))

    def test_original_worktree_not_excused_by_adapted_index(self):
        self.body = self.original
        with self.assertRaises(ValueError): self.ns['t10_navigation_edition'](Path('.'))

if __name__ == '__main__': unittest.main()
