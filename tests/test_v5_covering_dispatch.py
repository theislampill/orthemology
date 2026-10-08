"""Narrow adapter seams: loader custody and dispatch, with no process calls."""
import contextlib,hashlib,importlib.util,io,sys,tempfile,unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
def load():
    spec=importlib.util.spec_from_file_location('covering_dispatch_adapter',ROOT/'scripts/replay_v5_successors.py')
    a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a);return a

class CoveringDispatchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.a=load()

    def loader(self):
        self.assertTrue(callable(getattr(self.a,'covering_continuation_load',None)),'Reviewed covering helper loader is absent')
        return self.a.covering_continuation_load

    def test_loader_reads_exact_helper_and_data_without_process(self):
        loader=self.loader()
        with patch.object(self.a,'run_process',side_effect=AssertionError('ANY_PROCESS_FORBIDDEN')):
            cc=loader();self.assertEqual(cc.SCHEMA,'orthemology-v5-covering-audit-continuation-v1')
            self.assertEqual(cc.data(self.a)['prior_receipt_sha256'],'e8e4c419c4926761c4677fba9dce6f24a8188e53681cba9703a1e2018efc4e48')

    def test_loader_rejects_changed_helper_and_changed_data(self):
        loader=self.loader();source=ROOT/'scripts/v5_covering_continuation.py';data=source.with_suffix('.json')
        for changed in ['helper','data']:
            with self.subTest(changed=changed),tempfile.TemporaryDirectory()as d:
                dst=Path(d);(dst/source.name).write_bytes(source.read_bytes()+(b'\n# mutation'if changed=='helper'else b''))
                (dst/data.name).write_bytes(data.read_bytes()+(b' 'if changed=='data'else b''))
                with patch.object(self.a,'__file__',str(dst/'replay_v5_successors.py')):
                    with self.assertRaises(ValueError):loader()

    def test_execution_wrapper_passes_exact_arguments_and_adapter(self):
        self.loader();self.assertTrue(callable(getattr(self.a,'execute_covering_audit_continuation',None)))
        calls=[];marker=object()
        def execute(*args,**kwargs):calls.append((args,kwargs));return marker
        inputs=({}, {}, Path('/root'),Path('/prior'),Path('/fresh'),{},{});reviews={}
        with patch.object(self.a,'covering_continuation_load',return_value=SimpleNamespace(execute=execute)):
            self.assertIs(self.a.execute_covering_audit_continuation(*inputs,reviews=reviews),marker)
        self.assertEqual(calls[0][0],inputs);self.assertIs(calls[0][1]['reviews'],reviews)
        self.assertEqual(calls[0][1]['adapter'].__file__,self.a.__file__)

    def test_receipt_dispatch_preserves_receipt_and_sources(self):
        self.loader();calls=[];marker=object();receipt={'replay_evidence':{'schema':'orthemology-v5-covering-audit-continuation-v1'}}
        def validate(*args,**kwargs):calls.append((args,kwargs));return marker
        suite={};sources={};root=Path('/root')
        with patch.object(self.a,'covering_continuation_load',return_value=SimpleNamespace(validate_receipt=validate)):
            self.assertIs(self.a.validate_receipt(receipt,suite,sources,root),marker)
        self.assertEqual(calls[0][0],(receipt,suite,sources,root))

    def test_cli_admits_only_covering_audit_continuation_mode(self):
        self.loader();suite={'id':'covering-fixture'};bundle={'suites':[suite],'sources':[],'reviews':[]};calls=[]
        def execute(*args,**kwargs):calls.append((args,kwargs));return {'suite_id':suite['id'],'outcome':'RESOURCE_INCONCLUSIVE','proof_scope':'NONE','exit_code':1}
        argv=['replay_v5_successors.py','--covering-audit-continuation','--suite',suite['id'],'--root','/root','--prior','/prior','--out','/fresh']
        with patch.object(sys,'argv',argv),patch.dict(sys.modules,{'validate_v5_successors':SimpleNamespace(load_bundle=lambda root:bundle)}),patch.object(self.a,'execute_covering_audit_continuation',side_effect=execute),contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(self.a.main(),1)
        self.assertEqual(len(calls),1);self.assertEqual(calls[0][0][3:5],(Path('/prior'),Path('/fresh')))

if __name__=='__main__':unittest.main(verbosity=2)
