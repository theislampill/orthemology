"""Exact T08 navigation edition; target bodies are never opened."""
import ast
import hashlib
from pathlib import Path
import subprocess
import unittest

SOURCE=Path(__file__).resolve().parents[1]/'scripts/validate_t20_v6_projection.py'
class T08Tests(unittest.TestCase):
    def setUp(self):
        tree=ast.parse(SOURCE.read_text());self.fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='t08_navigation_edition')
        self.path='experiments/orthemology-v5-successors/groups/t08-history/README.md'
        self.original=subprocess.check_output(['git','show','7efc6217c090b92d65f2c4cb8b011c18eb96bf7c:'+self.path])
        # Use the actual existing administrative adaptation, no copied authority.
        import resolve_t20_v6_source as resolver
        self.earlier=resolver.administrative_guide_adaptation(self.path,self.original)
        self.target='experiments/orthemology-v5-successors/source-store/8d0d5c3934128136fbd69b70b8a0669fe055e5eb005797e25269a69157361657/PUBLIC_ACCEPTANCE.md'
        self.old=('../../source-store/'+self.target.split('/source-store/')[1]).encode()
        self.new=('https://github.com/theislampill/orthemology/blob/27c25b4dc30b1a8b3cb97588aba61482d1d8dcca/'+self.target).encode()
        self.body=self.earlier.replace(self.old,self.new);self.badtarget=False;self.badoriginal=False
        self.index=('100644 30f7b0905c99312d67c5394b0c8c50d767fe1eb4 0\t'+self.path+'\0').encode()
        def git(root,*args):
            if args[:2]==('ls-tree','-z'):
                name=args[-1];blob=('a49fbf2d3e0691495f5884e3a13ec475aafb1293' if name==self.path else '8e998b9d54173e1c38885b1d459e765a57a1bf3e')
                if self.badtarget and name==self.target:blob='0'*40
                return ('100644 blob '+blob+'\t'+name+'\0').encode()
            if args[:2]==('cat-file','blob'):return self.original+(b'X' if self.badoriginal else b'')
            if args[:2]==('ls-files','--stage'):return self.index
            raise AssertionError('unexpected metadata read')
        self.ns=dict(hashlib=hashlib,BASE='7efc6217c090b92d65f2c4cb8b011c18eb96bf7c',T08_NAVIGATION_GUIDE=self.path,_administrative_git=git,_regular_current_bytes=lambda root,path:self.body,administrative_guide_adaptation=resolver.administrative_guide_adaptation)
        exec(compile(ast.Module(body=[self.fn],type_ignores=[]),str(SOURCE),'exec'),self.ns)
    def check(self):return self.ns['t08_navigation_edition'](Path('.'))
    def test_exact(self):self.assertEqual(self.check(),{self.path})
    def test_extra_prose(self):
        self.body+=b'\nextra';self.assertRaises(ValueError,self.check)
    def test_bad_target(self):
        self.badtarget=True;self.assertRaises(ValueError,self.check)
    def test_wrong_index_mode(self):
        self.index=self.index.replace(b'100644',b'100755');self.assertRaises(ValueError,self.check)
    def test_original_identity(self):
        self.badoriginal=True;self.assertRaises(ValueError,self.check)
    def test_wrong_revision(self):
        self.body=self.body.replace(b'27c25b4dc30b1a8b3cb97588aba61482d1d8dcca',b'0'*40);self.assertRaises(ValueError,self.check)
    def test_old_body_cannot_use_new_route(self):
        self.body=self.earlier;self.assertRaises(ValueError,self.check)
    def test_exact_M_only_predicate(self):
        fn=next(n for n in ast.parse(SOURCE.read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='check_preserved_roots')
        expr=next(n.test for n in ast.walk(fn) if isinstance(n,ast.If) and isinstance(n.test,ast.Call) and isinstance(n.test.func,ast.Name) and n.test.func.id=='any' and any(isinstance(x,ast.Name) and x.id=='t08_authenticated' for x in ast.walk(n.test)))
        names={n.id for n in ast.walk(expr) if isinstance(n,ast.Name)};ns={n:set() for n in names-{'any','zip','status','path'}};ns.update(any=any,zip=zip,t08_authenticated={self.path})
        for status,path,reject in [('M',self.path,False),('D',self.path,True),('A',self.path,True),('M',self.path+'x',True)]:
            ns['changes']=[status,path];self.assertEqual(eval(compile(ast.Expression(expr),'actual-predicate','eval'),ns),reject)
        ns.update(t08_authenticated=set(),changes=['M',self.path]);self.assertTrue(eval(compile(ast.Expression(expr),'actual-predicate','eval'),ns))

if __name__=='__main__':unittest.main()
