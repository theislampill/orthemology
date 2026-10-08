"""Public runner regression contracts, written before implementation."""
import ast
import sys
import subprocess
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

RUNNER = Path(__file__).resolve().parents[1] / 'replay.py'

class PortableRunnerContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = None
        if RUNNER.exists():
            spec = importlib.util.spec_from_file_location('portable_replay', RUNNER)
            cls.module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(cls.module)

    def api(self):
        self.assertIsNotNone(self.module, 'portable replay implementation is missing')
        return self.module

    def test_python_source_import_closure_is_present(self):
        package = RUNNER.parent
        files = list((package / "tranche18").rglob("*.py"))
        local = {p.stem for p in files} | {p.parent.name for p in files if p.name == "__init__.py"}
        missing = set()
        for path in files:
            for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
                names = [x.name for x in node.names] if isinstance(node, ast.Import) else ([node.module] if isinstance(node, ast.ImportFrom) and node.module else [])
                for name in names:
                    base = name.split(".")[0]
                    if base not in sys.stdlib_module_names and base not in local:
                        missing.add((path.relative_to(package).as_posix(), base))
        self.assertEqual(missing, set(), "Python evidence local import closure is incomplete")

    def test_confines_manifest_paths(self):
        m = self.api()
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            self.assertEqual(m.confined(root, 'a/b'), root / 'a/b')
            for bad in ('../outside', '/outside', 'a/../../outside', ''):
                with self.subTest(bad=bad), self.assertRaises(ValueError):
                    m.confined(root, bad)
            (root/'link').symlink_to(root.parent)
            with self.assertRaises(ValueError): m.confined(root, 'link/file')

    def test_manifest_rejects_modified_missing_extra_and_symlink(self):
        m = self.api()
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); p = root/'code.py'; p.write_text('x=1\n')
            manifest = {'files':[{'path':'code.py','bytes':4,'sha256':m.sha(p)}]}
            (root/'MANIFEST.json').write_text(json.dumps(manifest))
            self.assertEqual(m.verify_manifest(root)['files_verified'],1)
            p.write_text('x=2\n')
            with self.assertRaises(ValueError): m.verify_manifest(root)
            p.unlink()
            with self.assertRaises(ValueError): m.verify_manifest(root)
            p.write_text('x=1\n'); (root/'extra').write_text('unlisted')
            with self.assertRaises(ValueError): m.verify_manifest(root)
            (root/'extra').unlink(); (root/'nested').mkdir(); (root/'nested/MANIFEST.json').write_text('{}')
            with self.assertRaises(ValueError): m.verify_manifest(root)
            (root/'nested/MANIFEST.json').unlink(); p.unlink(); p.symlink_to(root/'MANIFEST.json')
            with self.assertRaises(ValueError): m.verify_manifest(root)

    def test_source_order_checks_missing_and_cycles(self):
        m=self.api()
        nodes={'A':{'imports':['B','Mathlib']},'B':{'imports':['Init']}}
        self.assertEqual(m.source_order(nodes), ['B','A'])
        with self.assertRaises(ValueError): m.source_order({'A':{'imports':['Absent']}})
        with self.assertRaises(ValueError): m.source_order({'A':{'imports':['B']},'B':{'imports':['A']}})

    def test_expected_failure_requires_mathematical_marker(self):
        m=self.api()
        rule={'expected_exit':1,'markers':['error: unsolved goals','⊢ False']}
        self.assertTrue(m.qualified_output(1,'error: unsolved goals\n⊢ False',rule))
        for code,text in [(0,'error: unsolved goals\n⊢ False'),(124,'error: unsolved goals\n⊢ False'),(1,'error: unknown identifier X\nerror: unsolved goals\n⊢ False'),(1,'error: unsolved goals'),(1,'error: unsolved goals\n⊢ False\nerror: unrelated failure'),(1,'error: unsolved goals\n⊢ False\nerror: unknown tactic boom')]:
            self.assertFalse(m.qualified_output(code,text,rule))
        self.assertFalse(m.qualified_output(0,"warning: declaration uses 'sorry'",{'expected_exit':0}))
        self.assertFalse(m.qualified_output(0,'sorryAx',{'expected_exit':0}))
        self.assertTrue(m.qualified_output(0,'',{'expected_exit':0}))

    def test_invalid_control_group_writes_nothing_outside_output(self):
        m=self.api()
        with tempfile.TemporaryDirectory() as d:
            base=Path(d);package=base/'package';package.mkdir();out=base/'output';out.mkdir()
            source=package/'Test.lean';source.write_text('example : True := True.intro\n')
            group=str(base/'escaped')
            plan={'modules':{},'controls':[{'group':group,'module':'Test','path':'Test.lean','sha256':m.sha(source),'expected_exit':0}]}
            (package/'lean/test').mkdir(parents=True)
            (package/'lean/test/REPLAY_PLAN.json').write_text(json.dumps(plan))
            writes=[]
            def fake_run(command,cwd,env,log,timeout):
                writes.append(Path(log));Path(log).write_text('stubbed compile\n')
                Path(command[command.index('-o')+1]).write_bytes(b'stub')
                return 0,'',0
            with patch.object(m,'verify_environment',return_value=(Path('/not-executed-lean'),[],{})), patch.object(m,'run_command',side_effect=fake_run):
                with self.assertRaises(ValueError):m.replay_lean(package,{},'test',out)
            self.assertEqual(writes,[], 'invalid identifiers must fail before any compiler or log write')
            self.assertFalse((base/'escaped__Test.log').exists())

    def test_fresh_output_refuses_existing_or_inside_package(self):
        m=self.api()
        with tempfile.TemporaryDirectory() as d:
            base=Path(d); package=base/'pkg';package.mkdir()
            with self.assertRaises(ValueError):m.make_output(package,package/'out')
            existing=base/'old';existing.mkdir()
            with self.assertRaises(ValueError):m.make_output(package,existing)
            out=m.make_output(package,base/'new');self.assertTrue(out.is_dir())

    def test_environment_cannot_inherit_lean_or_python_paths(self):
        m=self.api()
        env=m.clean_environment({'PATH':'/bin','LEAN_PATH':'bad','LEAN_SRC_PATH':'bad','LEAN_SYSROOT':'bad','LEAN_OPTS':'bad','PYTHONPATH':'bad','PYTHONHOME':'bad','PYTHONOPTIMIZE':'2','PYTHONUSERBASE':'bad'})
        self.assertEqual(env['PATH'],'/bin')
        for key in ('LEAN_PATH','LEAN_SRC_PATH','LEAN_SYSROOT','LEAN_OPTS','PYTHONPATH','PYTHONHOME','PYTHONOPTIMIZE','PYTHONUSERBASE'):self.assertNotIn(key,env)
        self.assertEqual(env['PYTHONDONTWRITEBYTECODE'],'1')
        self.assertEqual(env['PYTHONNOUSERSITE'],'1')

    def test_inventory_detects_extra_and_wrong_objects(self):
        m=self.api()
        with tempfile.TemporaryDirectory() as d:
            p=Path(d); cache=p/'dep/.lake/build/lib/lean';cache.mkdir(parents=True)
            f=cache/'A.olean';f.write_bytes(b'abc')
            rows=[{'package':'dep','path':'A.olean','bytes':3,'sha256':m.sha(f)}]
            self.assertEqual(m.verify_objects(p,rows,['dep'])['object_count'],1)
            f.write_bytes(b'bad')
            with self.assertRaises(ValueError):m.verify_objects(p,rows,['dep'])
            f.write_bytes(b'abc');(cache/'X.olean').write_bytes(b'extra')
            with self.assertRaises(ValueError):m.verify_objects(p,rows,['dep'])

    def test_entry_requires_ignored_python_environment(self):
        result=subprocess.run([sys.executable,'-S','-B',str(RUNNER),'verify'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        self.assertNotEqual(result.returncode,0)
        self.assertIn('Run with -E',result.stdout)

    def test_axiom_audit_checks_exact_count_and_whitelist(self):
        m=self.api()
        text="'X' depends on axioms: [propext, Classical.choice, Quot.sound]\n'Y' does not depend on any axioms"
        self.assertEqual(len(m.audit_axioms(text,2)),2)
        with self.assertRaises(ValueError):m.audit_axioms(text,3)
        with self.assertRaises(ValueError):m.audit_axioms("'X' depends on axioms: [sorryAx]",1)

if __name__=='__main__':unittest.main(verbosity=2)
