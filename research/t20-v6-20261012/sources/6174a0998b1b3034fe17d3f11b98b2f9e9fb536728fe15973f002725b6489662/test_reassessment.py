import hashlib,json,pathlib,subprocess,unittest
P=pathlib.Path(__file__).resolve().parents[1]
class ReassessmentTests(unittest.TestCase):
 def suites(self):
  r=subprocess.run(['python','-B',str(P/'replay_selected.py'),'--list'],capture_output=True,text=True,check=True)
  return json.loads(r.stdout)
 def test_new_successor_is_separate(self):
  s=self.suites();self.assertIn('finite-contracts-reconstructed',s)
  self.assertIn('26 finite contract tests',s['finite-contracts']['scope'])
  self.assertIn('30',s['finite-contracts-reconstructed']['scope'])
 def test_depth_suite_entrypoints(self):
  s=self.suites()
  for name in ['audit-refinement','restricted-controls','depth-independent','foundational-scope','pro-exact-controls','contract-downstream']:
   self.assertIn(name,s)
   self.assertTrue((P/'replay'/s[name]['directory']).is_dir())
 def test_original_bound_code_preserved(self):
  expected='3c42622d5bebb3d07da5f231e7a8b22bc4d174f806f80a92ecf7817d21a29c06'
  for rel in ['replay/finite-contracts/contracts.py','proof-families/rational-hase-j/rational-kernel-additive-preservation-20261011/payload/received-cross-front-synthesis-20261011/Orthemology_T20_Whole_Corpus_Synthesis_20261010/research/contracts.py']:
   self.assertEqual(hashlib.sha256((P/rel).read_bytes()).hexdigest(),expected)
 def test_successor_code_identity(self):
  p=P/'replay/finite-contracts-reconstructed/contracts.py'
  self.assertTrue(p.is_file(),'separately attributed successor bytes are required')
  self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),'852609c327636305d8565549bfb7fbb4aba27076012b4e75861fa97d0460a9c0')
 def test_every_projection_replay_copy(self):
  for row in json.loads((P/'PUBLIC_PROJECTION.json').read_text())['files']:
   for extra in row.get('required_replay_copies',[]):
    raw=(P/extra['path']).read_bytes();self.assertEqual(len(raw),extra['bytes']);self.assertEqual(hashlib.sha256(raw).hexdigest(),extra['sha256'])
 def test_reassessment_local_public_bindings(self):
  def walk(value):
   if isinstance(value,dict):
    target=value.get('public_source')
    if isinstance(target,str) and not target.startswith('https://') and value.get('public_sha256'):
     raw=(P/target).read_bytes();self.assertEqual(hashlib.sha256(raw).hexdigest(),value['public_sha256'],target)
     if 'public_bytes' in value:self.assertEqual(len(raw),value['public_bytes'],target)
    for v in value.values():walk(v)
   elif isinstance(value,list):
    for v in value:walk(v)
  for f in (P/'reassessment').rglob('*.json'):walk(json.loads(f.read_text()))
 def test_current_reader_bindings(self):
  for row in json.loads((P/'READER_PROJECTION.json').read_text())['v3_reader_files']:
   self.assertEqual(hashlib.sha256((P/row['path']).read_bytes()).hexdigest(),row['v3_sha256'],row['path'])
if __name__=='__main__':unittest.main()
