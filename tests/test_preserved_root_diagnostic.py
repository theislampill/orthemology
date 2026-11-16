"""Bounded diagnostic controls: no source bodies or Git checkout needed."""
import ast
import json
from pathlib import Path
import subprocess
from types import SimpleNamespace
import unittest

SOURCE=Path(__file__).resolve().parents[1]/'scripts/validate_t20_v6_projection.py'

def load(source, changes, fail=False):
    fn=next(n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name=='check_preserved_roots')
    names={n.id for n in ast.walk(fn) if isinstance(n,ast.Name)}
    ns={n:set() for n in names if n.isupper()}
    ns.update(HISTORICAL_PROSE={},BASE='baseline',CONTINUATION_COPY_ROOT='unrelated/',subprocess=subprocess)
    calls=[]
    def receiver(name):
        def f(*args,**kwargs):
            calls.append(name)
            if name.endswith('_candidate'):return False
            if fail:raise ValueError('SECRET/path/body/command')
            return set()
        return f
    for n in ast.walk(fn):
        if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id not in {'set','any','zip','str','list','note','len','sorted','dict'}:
            if n.func.id not in {'ValueError'}:ns[n.func.id]=receiver(n.func.id)
    ns['readonly_git_diff']=lambda *a:SimpleNamespace(returncode=0,stdout='\0'.join(sum(([s,p] for s,p in changes),[])).encode()+ (b'\0' if changes else b''))
    ns['continuation_owners']=SimpleNamespace(PRESERVATION_OWNER_PATHS=set())
    exec(compile(ast.Module(body=[fn],type_ignores=[]),'<actual-validator>','exec'),ns)
    return ns['check_preserved_roots'],calls

class DiagnosticTests(unittest.TestCase):
    def test_clean(self):
        fn,calls=load(SOURCE.read_text(),[]);d={}
        self.assertEqual(fn(None,{},d),[]);self.assertEqual(d,{})
    def test_status_counts_no_leak(self):
        changes=[('D','SECRET/a'),('D','SECRET/b'),('M','SECRET/c'),('SECRET/status','SECRET/d')]
        fn,calls=load(SOURCE.read_text(),changes);d={}; result=fn(None,{},d)
        self.assertEqual(result,['preserved v5 or prior T20 baseline changed'])
        self.assertEqual(d,{'cached:D':2,'cached:M':1,'cached:other':1,'worktree:D':2,'worktree:M':1,'worktree:other':1})
        self.assertNotIn('SECRET',json.dumps(d))
    def test_failure_is_not_admitted_or_leaked(self):
        fn,calls=load(SOURCE.read_text(),[('D','SECRET/a')],True);d={}
        self.assertEqual(fn(None,{},d),['preserved v5 or prior T20 baseline changed'])
        self.assertEqual(d['receiver:mediator_guide_source_bytes'],1)
        self.assertEqual(d['receiver:t10_navigation_edition'],1)
        self.assertEqual(d['receiver:foundations_navigation_edition'],1)
        self.assertNotIn('SECRET',json.dumps(d))
    def test_optional_diagnostic_no_result_change(self):
        for changes in [[],[('D','SECRET/a')],[('M','SECRET/a'),('T','SECRET/b')]]:
            for fail in [False,True]:
                fn,a=load(SOURCE.read_text(),changes,fail);x=fn(None,{})
                fn,b=load(SOURCE.read_text(),changes,fail);y=fn(None,{}, {})
                self.assertEqual(x,y);self.assertEqual(a,b)

    def test_actual_transport_retains_strict_assertion(self):
        path=SOURCE.with_name('source_alias_absence_continuations.py')
        tree=ast.parse(path.read_text())
        branch=next(n for n in ast.walk(tree) if isinstance(n,ast.If) and ast.unparse(n.test)=="args.phase == 't20_graph'")
        start=next(i for i,n in enumerate(branch.body) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='preserved_diagnostic' for t in n.targets))
        end=next(i for i,n in enumerate(branch.body[start:],start) if isinstance(n,ast.Assert))
        statements=branch.body[start:end+1]
        # Exact last statements of actual graph phase, not a copy of its checks.
        for errors in [[],['SECRET/path']]:
            record={}
            def check(root,objects,diagnostic):
                diagnostic['cached:D']=2
                return errors
            ns=dict(record=record,repo=None,objects={},projection=SimpleNamespace(check_preserved_roots=check))
            code=compile(ast.Module(body=statements,type_ignores=[]),'<actual-transport>','exec')
            if errors:
                with self.assertRaises(AssertionError):exec(code,ns)
            else:exec(code,ns)
            self.assertEqual(record['preserved_root_summary'],{'total':len(errors),'categories':{'cached:D':2}})
            self.assertNotIn('SECRET',json.dumps(record))

if __name__=='__main__':unittest.main()
