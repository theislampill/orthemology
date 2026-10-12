import importlib.util,json
from pathlib import Path
import tempfile,unittest
import os
from unittest.mock import patch

def module(name,file):
    s=importlib.util.spec_from_file_location(name,file);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
HERE=Path(__file__).resolve().parent
v=module('verify_return',HERE/'tooling/verify_return.py')
import sys
sys.modules['verify_return']=v
r=module('replay_python',HERE/'tooling/replay_python.py')

class ReplayTests(unittest.TestCase):
    def source(self,p,bad=False):
        p.mkdir();(p/'script.py').write_text("from pathlib import Path\nPath(__file__).with_name('generated.json').write_text('{\"answer\": "+('8' if bad else '7')+"}')\n")
        (p/'expected.json').write_text('{"answer": 7}')
        (p/'PYTHON_REPLAY.json').write_text(json.dumps({'checks':[{'id':'fixture','script':'script.py','expected':'expected.json','generated':'generated.json'}]}))
        (p/'EVIDENCE_REGISTRY.json').write_text(json.dumps({'subjects':[{'id':'fixture','custody':'new_source','qualification':'fresh_finite_checks','scope':'fixture only','files':[v.identity(p/'script.py','script.py')]}]}));v.seal(p)

    def test_relocated_success_keeps_input_unchanged(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'input';self.source(p);out=Path(t)/'out'
            self.assertEqual(r.replay(p,out)['status'],'PASS_DECLARED_PYTHON_CHECKS')
            self.assertFalse((p/'generated.json').exists());v.verify(p)

    def test_different_result_fails(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'input';self.source(p,True)
            with self.assertRaises(ValueError):r.replay(p,Path(t)/'out')
            result=json.loads((Path(t)/'out/RESULT.json').read_text())
            self.assertEqual(result['status'],'FAIL')
            self.assertEqual(len(result['results']),1)

    def test_output_cannot_be_existing_or_inside_input(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'input';self.source(p)
            for out in [Path(t),p/'inside']:
                with self.assertRaises(ValueError):r.replay(p,out)

    def test_nested_assertions_cannot_be_disabled_by_environment(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'input';self.source(p)
            (p/'script.py').write_text("import subprocess,sys\nfrom pathlib import Path\nr=subprocess.run([sys.executable,'-c','assert False'],capture_output=True)\nPath(__file__).with_name('generated.json').write_text(str(r.returncode))\n")
            (p/'expected.json').write_text('1')
            reg=json.loads((p/'EVIDENCE_REGISTRY.json').read_text());reg['subjects'][0]['files']=[v.identity(p/'script.py','script.py')]
            (p/'EVIDENCE_REGISTRY.json').write_text(json.dumps(reg));v.seal(p)
            with patch.dict(os.environ,{'PYTHONOPTIMIZE':'1'}):
                self.assertEqual(r.replay(p,Path(t)/'out')['status'],'PASS_DECLARED_PYTHON_CHECKS')

if __name__=='__main__':unittest.main()
