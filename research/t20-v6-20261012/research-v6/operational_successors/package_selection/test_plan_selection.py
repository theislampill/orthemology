import copy,hashlib,json,tempfile,unittest
from pathlib import Path
import plan_selection as p

class PlannerControls(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);self.addCleanup(self.tmp.cleanup)
  self.data=b'authored exact proof\n';self.h=p.digest(self.data);(self.root/'source').write_bytes(self.data)
  self.rec={'sha256':self.h,'bytes':len(self.data),'source_path':'source','source_hash_verified':True,'reviewed_digest':self.h,'current_path_digest':self.h,'prior_exclusion_reasons':[],'distribution_disposition':'authored_code_annex_candidate_requires_final_selection','sensitive_screen_flags':[]}
  self.v5={'zip_sha256':'a'*64,'members':[]}
  self.row={'sha256':self.h,'action':'include','scope_status':'full-source-read-only','eligibility':{'basis':'reviewed_owner_authored','decision_reference':'parent-approved-v6-design','content_reviewed_for_distribution':True,'resolved_historical_role_filters':[]},'role':'authored_proof','views':[{'packet':'packet','path':'Proof.lean'}],'required_dependencies':[]}
  self.s={'schema':p.SCHEMA,'assembly_authorized':False,'audience':'public_repository','decision_reference':'parent-approved-v6-design','destination':'research/t20-v6','baseline_policy':'separate_unchanged_owner_checkpoint','lookup_sha256':'b'*64,'v5_index_sha256':'c'*64,'exclusions_sha256':'d'*64,'v5_archive_sha256':'a'*64,'objects':[self.row]}
 def build(self):return p.build_plan(self.s,{self.h:self.rec},self.v5,{},self.root)
 def test_exact_positive_determinism(self):
  x=self.build();self.assertEqual(x,self.build());self.assertFalse(x['public_plan']['source_execution_selected']);self.assertEqual(x['public_plan']['objects'][0]['provider']['kind'],'authored_annex_object')
 def test_private_v5_reuse_rejected(self):
  self.v5['members']=[{'sha256':self.h,'member':'package/Proof.lean'}];self.rec['prior_exclusion_reasons']=['private_machine_locators']
  with self.assertRaises(ValueError):self.build()
 def test_primary_bulk_rejected(self):
  self.rec['distribution_disposition']='exclude_primary_or_binary_bulk_use_scoped_receipt_and_locator'
  with self.assertRaises(ValueError):self.build()
 def test_explicit_v5_reuse_eligible(self):
  self.v5['members']=[{'sha256':self.h,'member':'package/Proof.lean'}];x=self.build()['public_plan'];self.assertEqual(x['objects'][0]['provider']['kind'],'separate_v5_member');self.assertFalse(x['baseline']['whole_archive_publication_selected'])
 def test_casefold_parent_collision_rejected(self):
  self.row['views']=[{'packet':'packet','path':'A'},{'packet':'packet','path':'a/Proof.lean'}]
  with self.assertRaises(ValueError):self.build()
 def test_parent_collision_with_intervening_sibling_rejected(self):
  self.row['views']=[{'packet':'packet','path':'A'},{'packet':'packet','path':'A-other'},{'packet':'packet','path':'A/Proof.lean'}]
  with self.assertRaises(ValueError):self.build()
 def test_casefold_deep_parent_with_intervening_sibling_rejected(self):
  self.row['views']=[{'packet':'packet','path':'a/b'},{'packet':'packet','path':'a/b-other'},{'packet':'packet','path':'A/B/deep/Proof.lean'}]
  with self.assertRaises(ValueError):self.build()
 def test_windows_forbidden_path_characters_rejected(self):
  for c in '<>|?*\"':
   with self.subTest(character=c),self.assertRaises(ValueError):p.relative('folder/a'+c+'b')
 def test_symlink_source_ancestor(self):
  (self.root/'alias').symlink_to(self.root,target_is_directory=True);self.rec['source_path']='alias/source'
  with self.assertRaises(ValueError):self.build()
 def test_drift_rejected(self):
  (self.root/'source').write_bytes(b'changed')
  with self.assertRaises(ValueError):self.build()
 def test_missing_disposition_rejected(self):
  self.row['required_dependencies']=['e'*64]
  with self.assertRaises(ValueError):self.build()
 def test_nonfinite_json_rejected(self):
  with self.assertRaises(ValueError):p.parse('{"x":NaN}')
 def test_duplicate_json_rejected(self):
  with self.assertRaises(ValueError):p.parse('{"x":1,"x":2}')
 def test_unsafe_views(self):
  for bad in ['../a','a//b','a\\b','/a','a/CON','a./b','a:drive','libfile_bad','a\x01b']:
   with self.subTest(bad=bad),self.assertRaises(ValueError):p.relative(bad)
 def test_projection_requires_receipt(self):
  self.row['eligibility']['basis']='reviewed_public_projection';self.row['original_sha256']='e'*64;self.row['transformation_receipt_sha256']='f'*64
  with self.assertRaises(ValueError):self.build()
 def test_role_filter_needs_exact_resolution(self):
  self.rec['prior_exclusion_reasons']=['nonselected_text_or_log_extension']
  with self.assertRaises(ValueError):self.build()
  self.row['eligibility']['resolved_historical_role_filters']=['nonselected_text_or_log_extension'];self.build()
 def test_no_materializing_omitted_views(self):
  self.row['action']='omit'
  with self.assertRaises(ValueError):self.build()
 def test_nonplanner_authority_refused(self):
  self.s['assembly_authorized']=True
  with self.assertRaises(ValueError):self.build()

class WindowsDeviceAliasControls(unittest.TestCase):
 def test_superscript_device_names_rejected(self):
  for stem in ('COM¹','COM²','COM³','LPT¹','LPT²','LPT³'):
   for suffix in ('','.txt','/source.py'):
    with self.subTest(stem=stem,suffix=suffix),self.assertRaises(ValueError):
     p.relative('packet/'+stem+suffix)
 def test_similar_nondevice_names_remain_allowed(self):
  for name in ('COM4extra','LPT0','COM¹extra','ordinary¹.txt'):
   self.assertEqual(p.relative('packet/'+name),'packet/'+name)

if __name__=='__main__':unittest.main()
