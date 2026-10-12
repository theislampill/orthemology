"""Synthetic metadata preservation checks; no retained research execution."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import build_scope_resolver as b


class ScopeResolverControls(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.a = self.root / 'admission'; self.a.mkdir()
        self.ledger = self.root / 'ledger.json'
        self.ledger.write_bytes(b'{"records":[]}\n')
        self.h = 'a'*64
        self.scope = {'scope': 'full x/y \\forall α; 0.125', 'fresh_execution': False}
        self.assoc = {'source_sha256':self.h, 'ledger':str(self.ledger),
                      'pointer':'$/records/0', 'recorded_scope':self.scope,
                      'ranges':[[1,9]], 'qualification':'scope only'}
        self.physical = {'sha256':self.h, 'bytes':9,
            'artifact_axis':'CURRENT_V6_OUTPUT_ARTIFACT',
            'terminal_scope_kind':'EXACT_COMPLETE_BODY',
            'scope_evidence':[{'kind':'EXACT_COMPLETE_BODY', 'ledger':str(self.ledger),
                              'pointer':'$/records/0', 'role':'authored proof'}]}
    def run_build(self):
        (self.a/'V6_READING_ASSOCIATIONS.jsonl').write_bytes(b.canonical(self.assoc))
        (self.a/'READING_LEDGER_SNAPSHOTS.json').write_bytes(b.canonical([
            {'ledger':str(self.ledger),'sha256':b.sha(self.ledger.read_bytes())}]))
        (self.a/'TERMINAL_PHYSICAL_SCOPE_OVERLAY.jsonl').write_bytes(b.canonical(self.physical))
        target=self.root/'out'
        with patch.object(b,'ROOT',self.root), patch.object(b,'V',self.root), patch.object(b,'A',self.a):
            b.build(target)
        return [json.loads(l)for l in (target/'SOURCE_SCOPE_RESOLVER.jsonl').read_text().splitlines()]
    def test_exact_axis_role_binding_and_scope_values(self):
        r=self.run_build()[0]
        self.assertEqual(r['artifact_axis'],self.physical['artifact_axis'])
        self.assertEqual(r['physical_scope_row_binding']['row_sha256'],b.sha(b.canonical(self.physical)))
        self.assertEqual(r['role_evidence_value_sha256'],b.sha(b.canonical(self.physical['scope_evidence'])))
        self.assertEqual(r['reading_scopes'][0]['recorded_scope'],self.scope)
    def test_formal_sentinel_primrec_is_preserved(self):
        self.scope["declaration"] = "sentinel_primrec"
        r=self.run_build()[0]
        self.assertEqual(r["reading_scopes"][0]["recorded_scope"], self.scope)
    def test_private_qualification_rejected(self):
        self.assoc['qualification']='Sentinel_not_for_delivery'
        with self.assertRaises(ValueError):self.run_build()
    def test_private_ranges_rejected(self):
        self.assoc['ranges']=['libfile_not_for_delivery']
        with self.assertRaises(ValueError):self.run_build()


if __name__=='__main__':unittest.main()
