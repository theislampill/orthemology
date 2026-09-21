"""Integration negatives. Compiler fixtures never receive kernel credit."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location('repository_adapter', ROOT / 'verify_repository.py')
adapter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adapter)

class IntegrationNegatives(unittest.TestCase):
    def fixture(self, root):
        p = root/'owned/a.py'; p.parent.mkdir(); p.write_text('value = 1\n')
        return {'base_commit':adapter.BASE,'files':[{'path':'owned/a.py','bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}],'managed_roots':['owned'],'standalone_files':[]}

    def rejection(self, change):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);m=self.fixture(root)
            self.assertEqual(adapter.validate_manifest(root,m),1)
            change(root,m)
            with self.assertRaises(adapter.gate.GateError):adapter.validate_manifest(root,m)

    def test_source_tamper(self):self.rejection(lambda r,m:(r/'owned/a.py').write_text('value = 2\n'))
    def test_missing_source(self):self.rejection(lambda r,m:(r/'owned/a.py').unlink())
    def test_renamed_source(self):self.rejection(lambda r,m:(r/'owned/a.py').rename(r/'owned/b.py'))
    def test_omitted_manifest_member(self):self.rejection(lambda r,m:m['files'].clear())
    def test_moved_import_collision(self):self.rejection(lambda r,m:(r/'owned/build_gate.py').write_text('fake = True\n'))
    def test_stale_base(self):self.rejection(lambda r,m:m.update(base_commit='0'*40))
    def test_duplicate_ids(self):
        rows=[{'qualified_id':'V4::T01'}];adapter.validate_ids(rows,['V4::T01'])
        with self.assertRaises(adapter.gate.GateError):adapter.validate_ids(rows+rows,['V4::T01'])
    def test_dropped_ids(self):
        with self.assertRaises(adapter.gate.GateError):adapter.validate_ids([],['V4::T01'])
    def test_stale_evidence(self):
        current={'digest':'current'}
        result={'scope':'REPOSITORY_NATIVE_REFERENCE_AND_REQUIRED_FORMAL','preflight':current,'postflight':current,'exit_code':2}
        adapter.verify_result_binding(result,current)
        with self.assertRaises(adapter.gate.GateError):adapter.verify_result_binding(result,{'digest':'old'})
    def test_missing_compiler_is_open_not_success(self):
        r={'exit_code':2,'status':'KERNEL_UNAVAILABLE','kernel_verified':False,'tools':{'lean':None,'lake':None}}
        self.assertFalse(adapter.accept_formal(r,2))
        r['kernel_verified']=True
        with self.assertRaises(adapter.gate.GateError):adapter.accept_formal(r,2)
    def test_wrong_compiler_real_process_identity(self):
        p=subprocess.run([sys.executable,'-c','print("Lean (version 9.99.0)")'],capture_output=True,text=True)
        self.assertEqual(p.returncode,0)
        with self.assertRaises(adapter.gate.GateError):adapter.gate.enforce_version('4.19.0',p.stdout)
    def test_failed_compiler_real_process_exit(self):
        p=subprocess.run([sys.executable,'-c','raise SystemExit(1)'],capture_output=True)
        with self.assertRaises(adapter.gate.GateError):adapter.accept_formal({'exit_code':1,'status':'FORMAL_GATE_FAIL','kernel_verified':False},p.returncode)
    def test_fake_all_green_wrapper(self):
        p=subprocess.run([sys.executable,'-c','print("all green")'],capture_output=True)
        self.assertEqual(p.returncode,0)
        with self.assertRaises(adapter.gate.GateError):adapter.accept_formal({'exit_code':0,'status':'KERNEL_AND_INVENTORY_PASS','kernel_verified':True},p.returncode)
        with self.assertRaises((adapter.gate.GateError,KeyError)):adapter.baseline_summary({'scope':'REFERENCE_AND_REQUIRED_FORMAL_TARGETS','exit_code':0},0)
    def test_privacy_leak(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'source.md';p.write_text('Ordinary source\n');adapter.privacy_check([p])
            p.write_text('/mnt/'+'data/private-chat.json')
            with self.assertRaises(adapter.gate.GateError):adapter.privacy_check([p])

if __name__=='__main__':unittest.main()
