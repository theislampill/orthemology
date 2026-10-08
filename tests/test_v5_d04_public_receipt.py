"""Portable metadata/privacy controls; these fixtures are not science evidence."""
import copy
import ast
import importlib.util
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest
from unittest.mock import patch

spec=importlib.util.spec_from_file_location('public_receipt',Path(__file__).parents[1]/'scripts/v5_d04_public_receipt.py')
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)

def fixture():
    source={'kind':'ORIGINAL_SOURCE','member':'Synthetic.lean','path':'{source}/Synthetic.lean','sha256':'1'*64}
    child_spec={'id':'negative','argv':['{tool:lean}','Synthetic.lean'],'cwd':'{source}','timeout_seconds':10,'capture':'MERGED_TEXT','source_binding':{'kind':'ORIGINAL_SOURCE','sha256':'1'*64},'sources':[source],'outputs':[],'replace_fresh_predecessor':[],'expected_exit_code':1}
    child={'id':'negative','index':0,'probe':False,'argv':['{tool:lean}','Synthetic.lean'],'cwd':'{source}','timeout_seconds':10,'capture':'MERGED_TEXT','stdin':{'mode':'INHERITED_NO_INPUT','data_sha256':None},'environment_sha256':'2'*64,'source_binding':child_spec['source_binding'],'input_bindings':[dict(source,actual_sha256='1'*64)],'source_hashes':{'Synthetic.lean':'1'*64},'replacement_bindings':[],'started_at':'2026-01-01T00:00:01Z','ended_at':'2026-01-01T00:00:02Z','terminal':'COMPLETED','exit_code':1,'log_sha256':'3'*64,'stream_hashes':{},'output_hashes':{},'record_file_sha256':'4'*64,'record_canonical_sha256':'5'*64,'argv_sha256':'6'*64,'cwd_sha256':'7'*64,'assessment':'REJECT'}
    contract={'children':[child_spec],'source_sha256':'8'*64}
    parent={'started_at':'2026-01-01T00:00:00Z','ended_at':'2026-01-01T00:00:03Z'}
    return child,contract,parent,SimpleNamespace(LEAN_SHA='9'*64)

class PublicSummaryControls(unittest.TestCase):
    def check(self,child,complete=True):
        _,contract,parent,api=fixture();p._check_child(child,contract,parent,complete,adapter=api)

    def test_exact_metadata_control_is_admitted(self):self.check(fixture()[0])

    def test_source_substitution_rejects(self):
        child=fixture()[0];child['input_bindings'][0]['actual_sha256']='a'*64
        with self.assertRaises(ValueError):self.check(child)

    def test_foreign_command_rejects(self):
        child=fixture()[0];child['argv']=['{tool:python}','-c','print(1)']
        with self.assertRaises(ValueError):self.check(child)

    def test_boolean_exit_cannot_impersonate_integer_exit(self):
        child=fixture()[0];child['exit_code']=True
        with self.assertRaises(ValueError):self.check(child)

    def test_timeout_keeps_null_exit_and_no_qualification(self):
        child=fixture()[0];child.update(terminal='TIMEOUT',exit_code=None,assessment='NOT_QUALIFIED')
        self.check(child,False)
        with self.assertRaises(ValueError):self.check(child,True)

    def test_unknown_incomplete_exit_is_not_rejection(self):
        child=fixture()[0];child.update(terminal='INTERRUPTED',exit_code=1)
        with self.assertRaises(ValueError):self.check(child,False)

    def test_missing_source_input_rejects(self):
        child=fixture()[0];child['input_bindings']=[]
        with self.assertRaises(ValueError):self.check(child)

    def test_foreign_output_rejects(self):
        child=fixture()[0];child['output_hashes']['{out}/extra.olean']='a'*64
        with self.assertRaises(ValueError):self.check(child)

    def test_log_bytes_cannot_be_added_to_typed_child(self):
        child=fixture()[0];child['log_hex']=b'synthetic text'.hex()
        with self.assertRaises(ValueError):self.check(child)

    def test_raw_transport_keys_reject_even_when_empty(self):
        for key in ['capture_records','log_hex','stream_hex','raw_capture_files','trace_launch']:
            with self.subTest(key=key),self.assertRaises(ValueError):p._public({key:[]})

    def test_mapping_preserves_path_structure(self):
        root='/'+'synthetic-root'
        self.assertEqual(p.symbolic({root+'/a/b':root+'/a/b'},{'out':root}),{'{out}/a/b':'{out}/a/b'})

    def test_prefix_collision_and_unknown_root_reject(self):
        root='/'+'synthetic-root'
        for value in [root+'-neighbor/a','/'+'unknown-root/a',{root+'/a':1,'{out}/a':2}]:
            with self.subTest(value=value),self.assertRaises(ValueError):p.symbolic(value,{'out':root})

    def test_ambiguous_root_aliases_reject(self):
        root='/'+'synthetic-root'
        with self.assertRaises(ValueError):p.symbolic(root,{'out':root,'source':root})

    def test_duplicate_json_keys_reject(self):
        with self.assertRaises(ValueError):p._unique_json(b'{"outcome":"FAILED","outcome":"PASS"}')

    def test_nonfinite_json_rejects(self):
        with self.assertRaises(ValueError):p._unique_json(b'{"value":NaN}')

    def test_projection_preserves_all_source_normalizer_scope_literals(self):
        path=Path(__file__).parents[1]/'scripts/v5_d04_assets/v5_d04_normalizers_translated.py'
        literals=[]
        for node in ast.walk(ast.parse(path.read_text())):
            if isinstance(node,ast.Return)and isinstance(node.value,ast.Dict):
                for key,value in zip(node.value.keys,node.value.values):
                    if isinstance(key,ast.Constant)and key.value=='scope'and isinstance(value,ast.Constant):literals.append(value.value)
        self.assertEqual(len(literals),6)
        self.assertEqual(set(literals),set(p.NORMALIZATION_SCOPES.values()))
        for literal in literals:
            raw={'normalization':{'recipe':'synthetic','normalizer_assets':{},'result':{'summary':{},'scope':literal}}}
            self.assertEqual(p._project_normalization(raw)['result']['scope'],literal)

    def test_missing_rewritten_or_encoded_scope_rejects_before_association(self):
        for scope in [None,'All results qualify.','c3ludGhldGljIGxvZw==']:
            result={'children':[],'summary':{}}
            if scope is not None:result['scope']=scope
            inv={'recipe':'t07-criterion-translated-v1','normalization_sha256':'1'*64,'normalization':{'recipe':'t07-criterion-translated-v1','normalizer_assets':{},'result':result}}
            with self.subTest(scope=scope),self.assertRaisesRegex(ValueError,'Missing/changed original scientific scope'):
                p._check_normalization(inv,adapter=None)

class PublicHelperLoaderControls(unittest.TestCase):
    def loader(self,directory,expected):
        source=Path(__file__).parents[1]/'scripts/replay_v5_successors.py'
        names={'d04_public_receipt_load','no_symlinks'}
        nodes=[node for node in ast.parse(source.read_text()).body if isinstance(node,ast.FunctionDef) and node.name in names]
        self.assertEqual(len(nodes),2)
        namespace={'Path':Path,'__file__':str(directory/'replay_v5_successors.py'),'require':p.require,'sha':p.sha,'SimpleNamespace':SimpleNamespace,'D04_PUBLIC_HELPER_SHA256':expected}
        exec(compile(ast.Module(body=nodes,type_ignores=[]),str(source),'exec'),namespace)
        return namespace['d04_public_receipt_load']

    def test_hash_bound_helper_loads_only_verified_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory=Path(tmp);raw=b'VALUE = 1\n';helper=directory/'v5_d04_public_receipt.py';helper.write_bytes(raw)
            self.assertEqual(self.loader(directory,p.sha(raw))().VALUE,1)
            helper.write_bytes(b'VALUE = 2\n')
            with self.assertRaises(ValueError):self.loader(directory,p.sha(raw))()

    def test_same_byte_covering_data_symlink_rejects(self):
        raw=(Path(__file__).parents[1]/'scripts/v5_covering_continuation.json').read_bytes()
        with tempfile.TemporaryDirectory() as tmp:
            directory=Path(tmp);target=directory/'data.json';target.write_bytes(raw)
            (directory/'v5_covering_continuation.json').symlink_to(target)
            with patch.object(p,'__file__',str(directory/'v5_d04_public_receipt.py')):
                with self.assertRaises(ValueError):p.covering_pins()

    def test_symlink_helper_rejects_even_with_matching_digest(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory=Path(tmp);raw=b'VALUE = 1\n';target=directory/'target.py';target.write_bytes(raw)
            (directory/'v5_d04_public_receipt.py').symlink_to(target)
            with self.assertRaises(ValueError):self.loader(directory,p.sha(raw))()

class PublicDispatchControls(unittest.TestCase):
    def test_unhashable_schema_reaches_the_original_validation_gate(self):
        source=Path(__file__).parents[1]/'scripts/replay_v5_successors.py'
        function=next(node for node in ast.parse(source.read_text()).body if isinstance(node,ast.FunctionDef)and node.name=='validate_receipt')
        branch=next(node for node in function.body if isinstance(node,ast.If)and any(isinstance(n,ast.Name)and n.id=='d04_public_receipt_load'for n in ast.walk(node)))
        # Keep the exact proposed branch; a malformed schema must fall through
        # to the existing validator, not escape with Python's hashing TypeError.
        function.body=[branch,ast.Raise(exc=ast.Call(func=ast.Name(id='ValueError',ctx=ast.Load()),args=[ast.Constant(value='Original validation gate')],keywords=[]),cause=None)]
        tree=ast.fix_missing_locations(ast.Module(body=[function],type_ignores=[]));namespace={}
        exec(compile(tree,str(source),'exec'),namespace)
        for schema in [[],{},None,1]:
            with self.subTest(schema=schema),self.assertRaisesRegex(ValueError,'Original validation gate'):
                namespace['validate_receipt']({'replay_evidence':{'schema':schema}},None,None,None)

if __name__=='__main__':unittest.main(verbosity=2)
