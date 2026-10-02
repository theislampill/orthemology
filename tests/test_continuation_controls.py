"""The native control runner executes exact sources in separate fresh directories."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))


class ControlReplayTests(unittest.TestCase):
    def setUp(self):
        import replay_continuation_controls as r
        self.r=r
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)/'repo';self.root.mkdir()
        self.out=Path(self.tmp.name)/'out'
        data=b'import json\nfrom pathlib import Path\nif not __debug__: raise ValueError("assertions disabled")\nPath("result.json").write_text(json.dumps({"status":"PASS"}))\n'
        (self.root/'check.py').write_bytes(data)
        self.sources={'s':{'path':'check.py','sha256':hashlib.sha256(data).hexdigest(),'projection':'EXACT'}}
        self.suite={'schema':'orthemology-native-controls-v1','id':'example',
                    'steps':[{'id':'one','files':[{'path':'check.py','source_id':'s'}],
                              'entry':'check.py','outputs':['result.json'],'args':[]}]}

    def test_executes_original_control_with_assertions_enabled(self):
        result=self.r.replay(self.root,self.suite,self.sources,self.out)
        self.assertEqual(result['status'],'PASS_NATIVE_CONTROLS')
        self.assertEqual(result['steps'][0]['exit_code'],0)

    def test_existing_or_repository_output_is_rejected(self):
        self.out.mkdir()
        for out in [self.out,self.root/'outputs']:
            with self.subTest(out=out),self.assertRaises(ValueError):
                self.r.replay(self.root,self.suite,self.sources,out)

    def test_changed_source_cannot_execute(self):
        (self.root/'check.py').write_text('raise RuntimeError("tampered")\n')
        with self.assertRaises(ValueError):self.r.replay(self.root,self.suite,self.sources,self.out)

    def test_duplicate_or_escaping_module_path_is_rejected(self):
        for rel in ['../check.py','/check.py','check.py']:
            original=list(self.suite['steps'][0]['files'])
            self.suite['steps'][0]['files'].append({'path':rel,'source_id':'s'})
            with self.subTest(rel=rel),self.assertRaises(ValueError):
                self.r.validate_suite(self.suite,self.sources,self.root)
            self.suite['steps'][0]['files']=original

    def test_unexpected_written_file_is_failure(self):
        data=b'from pathlib import Path\nPath("undeclared.txt").write_text("x")\n'
        (self.root/'check.py').write_bytes(data);self.sources['s']['sha256']=hashlib.sha256(data).hexdigest()
        with self.assertRaises(ValueError):self.r.replay(self.root,self.suite,self.sources,self.out)
        self.assertEqual(json.loads((self.out/'RECEIPT.json').read_text())['status'],'FAILED')


if __name__=='__main__':unittest.main()
