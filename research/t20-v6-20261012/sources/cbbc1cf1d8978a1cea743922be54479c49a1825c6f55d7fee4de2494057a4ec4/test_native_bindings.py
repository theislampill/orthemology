import importlib.util,json,hashlib,unittest
from pathlib import Path
H=Path(__file__).resolve().parents[1]
M=None
if (H/'verify_native_integration.py').exists():
 s=importlib.util.spec_from_file_location('native',H/'verify_native_integration.py');M=importlib.util.module_from_spec(s);s.loader.exec_module(M)

class NativeBindingsTests(unittest.TestCase):
 def setUp(self):
  self.assertIsNotNone(M,'Native receipt verifier must exist')
  self.patch=b'actual patch bytes\n';self.sha=hashlib.sha256(self.patch).hexdigest()
  self.facts={'base_commit':'a'*40,'base_tree':'b'*40,'candidate_tree':'c'*40,'patch_sha256':self.sha,'patch_bytes':len(self.patch),'results':262,'sources':3806,'suites':37,'receipts':44}
  self.record={'base':'a'*40,'base_tree':'b'*40,'tree':'c'*40,'patch':{'sha256':self.sha,'bytes':len(self.patch)},'status':'PASS','results':262,'sources':3806,'suites':37,'receipts':44}
  self.bodies={'integration/repository.patch':self.patch,'integration/receipt.json':json.dumps(self.record).encode()}
  self.binding={'schema':'owner-native-receipt-bindings-v1','patch_path':'integration/repository.patch','facts':self.facts,
   'required_check_ids':['patch.digest','base','tree','results'],'checks':[
    {'id':'patch.digest','record':'integration/receipt.json','pointer':'/patch/sha256','fact':'patch_sha256'},
    {'id':'base','record':'integration/receipt.json','pointer':'/base','fact':'base_commit'},
    {'id':'tree','record':'integration/receipt.json','pointer':'/tree','fact':'candidate_tree'},
    {'id':'results','record':'integration/receipt.json','pointer':'/results','fact':'results'},
    {'id':'disposition','record':'integration/receipt.json','pointer':'/status','expected':'PASS'}]}
 def test_native_json_fields_bind_actual_patch_and_candidate(self):
  self.assertEqual(M.check_bindings(self.binding,self.bodies)['checks_passed'],5)
 def test_declared_patch_hash_cannot_replace_actual_patch_bytes(self):
  self.bodies['integration/repository.patch']=b'different patch'
  with self.assertRaises(ValueError):M.check_bindings(self.binding,self.bodies)
 def test_receipt_field_mismatch_and_absence_are_rejected(self):
  self.record['tree']='d'*40;self.bodies['integration/receipt.json']=json.dumps(self.record).encode()
  with self.assertRaises(ValueError):M.check_bindings(self.binding,self.bodies)
  self.record['tree']='c'*40;del self.record['results'];self.bodies['integration/receipt.json']=json.dumps(self.record).encode()
  with self.assertRaises(ValueError):M.check_bindings(self.binding,self.bodies)
 def test_missing_duplicate_or_type_confused_checks_are_rejected(self):
  self.binding['checks']=self.binding['checks'][1:]
  with self.assertRaises(ValueError):M.check_bindings(self.binding,self.bodies)
  self.binding['required_check_ids']=[];self.binding['checks'].append(dict(self.binding['checks'][0]))
  with self.assertRaises(ValueError):M.check_bindings(self.binding,self.bodies)
 def test_json_pointer_escapes_and_strict_types(self):
  self.assertEqual(M.json_pointer({'a/b':{'~name':[7]}},'/a~1b/~0name/0'),7)
  self.record['results']=True;self.facts['results']=1;self.bodies['integration/receipt.json']=json.dumps(self.record).encode()
  with self.assertRaises(ValueError):M.check_bindings(self.binding,self.bodies)

if __name__=='__main__':unittest.main()
