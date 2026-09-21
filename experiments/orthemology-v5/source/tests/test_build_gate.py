"""Verifier policy/real process tests. No test in this file is a Lean build."""
import importlib.util
import json
import hashlib
from pathlib import Path
import tempfile
import sys
import unittest

class BuildGateTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(importlib.util.find_spec('build_gate'), 'strict build gate absent')
        import build_gate
        self.g = build_gate

    def root(self):
        t = tempfile.TemporaryDirectory(); self.addCleanup(t.cleanup); return Path(t.name)

    def manifest(self, root):
        files=[]
        for p in sorted(root.rglob('*')):
            if p.is_file() and p != root/'MANIFEST.json':
                b=p.read_bytes();files.append({'path':p.relative_to(root).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
        (root/'MANIFEST.json').write_text(json.dumps({'files':files}))

    def test_version_exact_not_just_recorded(self):
        self.g.enforce_version('4.19.0','Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit abc, Release)\n')
        for s in ['Lean (version 0.0.0)', 'Lean (version 4.19.0-rc1)', 'other output 4.19.0','Lean (version 4.19.00)']:
            with self.assertRaises(self.g.GateError): self.g.enforce_version('4.19.0',s)

    def test_missing_manifest_fails(self):
        with self.assertRaises(self.g.GateError):self.g.verify_manifest(self.root())

    def test_manifest_exact_including_nested_manifest(self):
        r=self.root();(r/'history').mkdir();(r/'history/MANIFEST.json').write_text('{}');self.manifest(r)
        self.assertEqual(self.g.verify_manifest(r)['members'],1)
        (r/'MANIFEST.json').write_text('{"files":[]}')
        with self.assertRaises(self.g.GateError):self.g.verify_manifest(r)

    def test_manifest_duplicate_and_traversal(self):
        r=self.root();(r/'a').write_text('x');self.manifest(r)
        j=json.loads((r/'MANIFEST.json').read_text());j['files']*=2;(r/'MANIFEST.json').write_text(json.dumps(j))
        with self.assertRaises(self.g.GateError):self.g.verify_manifest(r)
        j['files'][0]['path']='../a';j['files']=j['files'][:1];(r/'MANIFEST.json').write_text(json.dumps(j))
        with self.assertRaises(self.g.GateError):self.g.verify_manifest(r)

    def test_manifest_duplicate_json_keys(self):
        r=self.root();(r/'MANIFEST.json').write_text('{"files":[],"files":[]}')
        with self.assertRaises(self.g.GateError):self.g.verify_manifest(r)

    def test_missing_empty_artifact(self):
        p=self.root()/'A.olean'
        with self.assertRaises(self.g.GateError):self.g.check_artifact(p)
        p.write_bytes(b'')
        with self.assertRaises(self.g.GateError):self.g.check_artifact(p)

    def block(self,name,axioms='[]'):
        return f'AUDIT_BEGIN {name}\n{name} : True\n\'{name}\' depends on axioms: {axioms}\nAUDIT_END {name}\n'

    def test_each_target_requires_type_and_axioms(self):
        s=self.block('A.one')+self.block('A.two','[propext, Quot.sound]')
        d=self.g.parse_audit(s,['A.one','A.two']);self.assertEqual(d['A.two']['axioms'],['Quot.sound','propext'])
        for bad in [self.block('unrelated.trivial'),self.block('A.one'), s.replace('A.two : True','garbage'), s.replace("'A.two' depends on axioms: [propext, Quot.sound]", "'other' depends on axioms: []")]:
            with self.assertRaises(self.g.GateError):self.g.parse_audit(bad,['A.one','A.two'])

    def test_empty_footprint_recognised(self):
        s=self.block('A.one').replace("depends on axioms: []","does not depend on any axioms")
        self.assertEqual(self.g.parse_audit(s,['A.one'])['A.one']['axioms'],[])

    def test_forbidden_and_duplicate_audits(self):
        for bad in [self.block('A.one','[sorryAx]'),self.block('A.one','[Custom.checked]'),self.block('A.one','[Lean.ofReduceBool]'),self.block('A.one')*2]:
            with self.assertRaises(self.g.GateError):self.g.parse_audit(bad,['A.one'])

    def test_process_stdout_stderr_status_real(self):
        r=self.g.run_bounded([sys.executable,'-c','import sys;print("out");print("err",file=sys.stderr);sys.exit(7)'],self.root(),timeout=2)
        self.assertEqual(r['exit_code'],7);self.assertEqual(r['stdout'],'out\n');self.assertEqual(r['stderr'],'err\n')

    def test_timeout_is_structured_real(self):
        r=self.g.run_bounded([sys.executable,'-c','import time;time.sleep(2)'],self.root(),timeout=.05)
        self.assertEqual(r['status'],'TIMEOUT');self.assertFalse(r['ok'])

    def test_os_error_is_structured_real(self):
        r=self.g.run_bounded(['/nonexistent/orth-compiler'],self.root(),timeout=.1)
        self.assertEqual(r['status'],'OS_ERROR');self.assertFalse(r['ok'])

    def test_output_limit_is_fail_closed_real(self):
        r=self.g.run_bounded([sys.executable,'-c','print("x"*100000)'],self.root(),timeout=2,output_limit=1000)
        self.assertEqual(r['status'],'OUTPUT_LIMIT');self.assertFalse(r['ok'])

class ContractGateTests(unittest.TestCase):
    def test_missing_mandatory_target_is_rejected(self):
        import build_gate as g
        self.assertTrue(hasattr(g,'validate_inventory'), 'mandatory inventory gate absent')
        with self.assertRaises(g.GateError):g.validate_inventory({'modules':[]}, {})

    def test_required_role_cannot_be_deleted_with_its_source(self):
        import build_gate as g
        targets=sorted(g.MANDATORY_TARGETS)
        good={'modules':[{'name':'A','targets':targets}]}
        self.assertEqual(len(g.validate_inventory(good,{'A':targets})),1)
        short=[x for x in targets if x!='OrthemologyV4.mainWitnessAt']
        with self.assertRaisesRegex(g.GateError,'acceptance-contract'):
            g.validate_inventory({'modules':[{'name':'A','targets':short}]},{'A':short})

    def test_partial_module_inventory_is_rejected(self):
        import build_gate as g
        self.assertTrue(hasattr(g,'validate_inventory'), 'mandatory inventory gate absent')
        with self.assertRaises(g.GateError):g.validate_inventory({'modules':[{'name':'A','targets':['A.trivial']}]}, {'A':['A.trivial'],'B':['B.omitted']})

if __name__=='__main__':unittest.main()
