"""Exact public-guide link edition; research target bodies are never read."""
import ast
import hashlib
from pathlib import Path
import subprocess
import unittest

SOURCE = Path(__file__).resolve().parents[1] / 'scripts/validate_t20_v6_projection.py'

class FoundationsEditionTests(unittest.TestCase):
    def setUp(self):
        tree = ast.parse(SOURCE.read_text())
        assignment = next(n for n in tree.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'FOUNDATIONS_LINK_EDITION' for t in n.targets))
        self.binding = ast.literal_eval(assignment.value)
        fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'foundations_navigation_edition')
        self.originals = {row['original'][0]: subprocess.check_output(['git', 'show', self.binding['revision']+':'+path]) for path,row in self.binding['guides'].items()}
        self.bodies={};self.indices={};self.bad_target=False
        for path,row in self.binding['guides'].items():
            body=self.originals[row['original'][0]]
            for old,new,count in row['replacements']: body=body.replace(old.encode(),new.encode())
            self.bodies[path]=body
            self.indices[path]=('100644 '+row['adapted'][0]+' 0\t'+path+'\0').encode()
        self.path=next(iter(self.bodies))
        def git(root,*args):
            path=args[-1]
            if args[:2]==('ls-tree','-z'):
                blob=(self.binding['guides'][path]['original'][0] if path in self.binding['guides'] else self.binding['targets'][path])
                if self.bad_target and path in self.binding['targets']:blob='0'*40
                return ('100644 blob '+blob+'\t'+path+'\0').encode()
            if args[:2]==('cat-file','blob'):return self.originals[args[-1]]
            if args[:2]==('ls-files','--stage'):return self.indices[path]
            raise AssertionError(args)
        self.ns={'hashlib':hashlib,'FOUNDATIONS_LINK_EDITION':self.binding,'_administrative_git':git,'_regular_current_bytes':lambda root,path:self.bodies[path]}
        exec(compile(ast.Module(body=[fn],type_ignores=[]),str(SOURCE),'exec'),self.ns)
    def run_edition(self):return self.ns['foundations_navigation_edition'](Path('.'))
    def test_exact_edition(self):self.assertEqual(self.run_edition(),set(self.binding['guides']))
    def test_extra_prose_rejected(self):
        self.bodies[self.path]+=b'\nextra\n'
        with self.assertRaises(ValueError):self.run_edition()
    def test_wrong_target_pin_rejected(self):
        self.bad_target=True
        with self.assertRaises(ValueError):self.run_edition()
    def test_wrong_index_rejected(self):
        self.indices[self.path]=self.indices[self.path].replace(b'100644',b'100755')
        with self.assertRaises(ValueError):self.run_edition()
    def test_original_worktree_rejected(self):
        self.bodies[self.path]=self.originals[self.binding['guides'][self.path]['original'][0]]
        with self.assertRaises(ValueError):self.run_edition()
    def test_literal_target_change_rejected(self):
        self.binding['guides'][self.path]['replacements'][0][1]+='?changed'
        with self.assertRaises(ValueError):self.run_edition()
    def test_actual_admission_predicate(self):
        fn=next(n for n in ast.parse(SOURCE.read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='check_preserved_roots')
        predicate=next(n.test for n in ast.walk(fn) if isinstance(n,ast.If) and isinstance(n.test,ast.Call) and isinstance(n.test.func,ast.Name) and n.test.func.id=='any' and any(isinstance(x,ast.Name) and x.id=='foundations_authenticated' for x in ast.walk(n.test)))
        names={n.id for n in ast.walk(predicate) if isinstance(n,ast.Name)}
        ns={n:set() for n in names-{'any','zip','status','path'}};ns.update(any=any,zip=zip,foundations_authenticated=set(self.binding['guides']))
        code=compile(ast.Expression(predicate),'actual-predicate','eval')
        for status,path,expect_reject in [('M',self.path,False),('D',self.path,True),('M',self.path+'.other',True)]:
            ns['changes']=[status,path];self.assertEqual(eval(code,ns),expect_reject)
        ns.update(changes=['M',self.path],foundations_authenticated=set());self.assertTrue(eval(code,ns))

if __name__=='__main__':unittest.main()
