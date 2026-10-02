"""Replay must fail closed before a missing/foreign compiler can earn credit."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from test_research_continuations import fixture, AREA

SCRIPT=Path(__file__).resolve().parents[1]/'scripts/replay_research_continuations.py'


class ReplayTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if SCRIPT.exists():
            sys.path.insert(0,str(SCRIPT.parent))
            spec=importlib.util.spec_from_file_location('continuation_replay',SCRIPT)
            cls.r=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.r)

    def setUp(self):
        self.assertTrue(SCRIPT.is_file(),'Continuation replay is not implemented')
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.base=Path(self.tmp.name);self.root=self.base/'repo';self.root.mkdir();fixture(self.root)

    def transcript(self):
        return "CONTINUATION_BEGIN Demo.ok\nDemo.ok : True\n'Demo.ok' does not depend on any axioms\nCONTINUATION_END Demo.ok\n"

    def test_complete_exact_type_and_axiom_readback(self):
        rows=self.r.parse_readback(self.transcript(),['Demo.ok'])
        self.assertEqual(rows,{'Demo.ok':{'type':'Demo.ok : True','axioms':[]}})

    def test_truncated_missing_and_duplicate_readback_rejected(self):
        for raw in ['',self.transcript().split('CONTINUATION_END')[0],self.transcript()*2]:
            with self.subTest(raw=raw),self.assertRaises(ValueError):self.r.parse_readback(raw,['Demo.ok'])

    def test_wrong_namespace_or_unapproved_axiom_rejected(self):
        for raw in [self.transcript().replace('Demo.ok : True','Wrong.ok : True'),
                    self.transcript().replace('does not depend on any axioms','depends on axioms: [sorryAx]')]:
            with self.assertRaises(ValueError):self.r.parse_readback(raw,['Demo.ok'])

    def test_missing_compiler_is_blocked_and_never_pass(self):
        result=self.r.replay(self.root,'fixture-a',self.base/'missing-bin',self.base/'mathlib',self.base/'out')
        self.assertEqual(result['status'],'BLOCKED')
        self.assertIs(result['kernel_verified'],False)
        self.assertEqual(result['exit_code'],2)
        self.assertEqual(json.loads((self.base/'out/RECEIPT.json').read_text())['status'],'BLOCKED')

    def test_wrong_compiler_identity_is_failure(self):
        bindir=self.base/'bin';bindir.mkdir();(bindir/'lean').write_bytes(b'not the official compiler')
        result=self.r.replay(self.root,'fixture-a',bindir,self.base/'mathlib',self.base/'out')
        self.assertEqual(result['status'],'FAILED');self.assertIs(result['kernel_verified'],False)

    def test_reused_or_internal_output_refused_before_write(self):
        out=self.base/'out';out.mkdir();(out/'keep').write_text('preserve')
        for bad in [out,self.root/'new']:
            with self.assertRaises(ValueError):self.r.replay(self.root,'fixture-a',self.base/'bin',self.base/'math',bad)
        self.assertEqual((out/'keep').read_text(),'preserve')
        self.assertFalse((self.root/'new').exists())

    def test_nonzero_real_process_rejected(self):
        with self.assertRaises(ValueError):
            self.r.run_process([sys.executable,'-c','raise SystemExit(3)'],self.base,{},self.base/'failure.log',10)

    def test_removed_lean_environment_does_not_return_in_child(self):
        with patch.dict(os.environ,{'LEAN_PATH':'poison','LEAN_SRC_PATH':'poison','LEAN_SYSROOT':'poison'}):
            clean={k:v for k,v in os.environ.items() if not k.startswith('LEAN_')}
            raw=self.r.run_process([sys.executable,'-c','import os,json; print(json.dumps({k:v for k,v in os.environ.items() if k.startswith("LEAN_")}))'],self.base,clean,self.base/'environment.log',10)
        self.assertEqual(json.loads(raw),{})

    def test_real_process_timeout_rejected(self):
        with self.assertRaises(ValueError):
            self.r.run_process([sys.executable,'-c','import time; time.sleep(10)'],self.base,{},self.base/'timeout.log',0.1)

    def test_changed_source_prevents_output_creation(self):
        p=next((self.root/AREA/'source-store').glob('*.lean'));p.write_text('bad')
        with self.assertRaises(ValueError):self.r.replay(self.root,'fixture-a',self.base/'bin',self.base/'math',self.base/'out')
        self.assertFalse((self.base/'out').exists())

    def test_stale_object_fingerprint_rejected(self):
        p=self.base/'object.olean';p.write_bytes(b'old')
        with self.assertRaises(ValueError):self.r.verify_object(p,hashlib.sha256(b'new').hexdigest())


if __name__=='__main__':unittest.main(verbosity=2)
