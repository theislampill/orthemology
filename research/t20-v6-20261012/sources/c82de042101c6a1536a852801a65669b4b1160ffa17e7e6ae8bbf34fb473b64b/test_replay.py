"""Lightweight wrapper-boundary controls; no Lean proof mutation or build."""
from pathlib import Path
import importlib.util, json, os, shutil, sys, tempfile, unittest

HERE=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('checkpoint_replay',HERE/'replay.py')
replay=importlib.util.module_from_spec(spec);spec.loader.exec_module(replay)

class BoundaryControls(unittest.TestCase):
    def test_absent_output_rejects_existing_without_touching(self):
        with tempfile.TemporaryDirectory() as temp:
            output=Path(temp)/'existing';output.mkdir();sentinel=output/'keep';sentinel.write_text('preserve')
            with self.assertRaises(RuntimeError): replay.require_fresh_output(output,[])
            self.assertEqual(sentinel.read_text(),'preserve')
            self.assertEqual(list(output.iterdir()),[sentinel])
    def test_output_protected_trees(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)/'source';root.mkdir()
            for name in ('root','mathlib','lean'):
                tree=root/name;tree.mkdir()
                output=tree/'new-replay'
                with self.assertRaises(RuntimeError): replay.require_fresh_output(output,[tree])
                self.assertFalse(output.exists())
    def test_safe_manifest_paths(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);(root/'ok').write_text('content')
            for bad in ('../ok','/absolute','a/../ok','./ok'):
                with self.assertRaises(RuntimeError): replay.regular_path(root,bad)
            (root/'link').symlink_to(root/'ok')
            with self.assertRaises(RuntimeError): replay.regular_path(root,'link')
    def test_extra_inventory_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);(root/'PUBLIC_MANIFEST.json').write_text('{}');(root/'extra').write_text('x')
            with self.assertRaises(RuntimeError): replay.exact_inventory(root,[],'PUBLIC_MANIFEST.json')
    def test_corrupted_source_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);path=root/'source.lean';path.write_text('original')
            record={'path':'source.lean','bytes':path.stat().st_size,'sha256':replay.digest(path)}
            path.write_text('modified')
            with self.assertRaises(RuntimeError): replay.verify_record(root,record)
    def test_nested_comment_and_string_token_scan(self):
        clean=replay.proof_tokens('/- admit /- sorry -/ unsafe -/\ndef s := "axiom"\n-- admit\ntheorem x : True := by trivial')
        self.assertNotRegex(clean,r'\b(sorry|admit|axiom|unsafe)\b')
        self.assertIn('theorem x',clean)
        self.assertIn('sorry',replay.proof_tokens('theorem x : False := by sorry'))
    def test_timeout_preserves_partial_diagnostics(self):
        with tempfile.TemporaryDirectory() as temp:
            log=Path(temp)/'timeout.log'
            with self.assertRaises(RuntimeError):
                replay.run_stage([sys.executable,'-u','-c','import time; print("before timeout",flush=True); time.sleep(2)'],dict(os.environ),log,0.15)
            text=log.read_text();self.assertIn('before timeout',text);self.assertIn('REPLAY_TIMEOUT',text)
            self.assertFalse((Path(temp)/'RECEIPT.json').exists())
    def test_mathlib_pin_is_independent(self):
        with tempfile.TemporaryDirectory() as temp:
            copy=Path(temp)/'checkpoint';shutil.copytree(HERE,copy)
            old=replay.ROOT
            try:
                replay.ROOT=copy
                (copy/'MATHLIB_SOURCE_PIN.json').write_text('{"commit":"c44e0c8ee63ca166450922a373c7409c5d26b00b","files":[]}')
                # Rewriting the public manifest cannot replace the independent dependency pin.
                public=json.loads((copy/'PUBLIC_MANIFEST.json').read_text())
                for item in public['files']:
                    if item['path']=='MATHLIB_SOURCE_PIN.json':
                        item['bytes']=(copy/item['path']).stat().st_size;item['sha256']=replay.digest(copy/item['path'])
                (copy/'PUBLIC_MANIFEST.json').write_text(json.dumps(public))
                with self.assertRaisesRegex(RuntimeError,'Mathlib source manifest changed'): replay.verify_checkpoint()
            finally: replay.ROOT=old

if __name__=='__main__': unittest.main()
