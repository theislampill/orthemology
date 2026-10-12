import hashlib,importlib.util,json,unittest
from pathlib import Path
H=Path(__file__).resolve().parents[1]
if (H/'tools').is_dir():H=H/'tools'
def module(name):
 p=H/(name+'.py')
 if not p.exists():return None
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
L=module('verify_owner_links');N=module('verify_native_integration')
class ScopedLinkTests(unittest.TestCase):
 def setUp(self):
  self.assertIsNotNone(L,'Standard-library owner-link verifier must exist')
  self.files={'t20/context/GUIDE.md':b'guide','t20/cooperation/SOURCE.md':b'source'}
 def receipt(self,href,target):
  sha=lambda b:hashlib.sha256(b).hexdigest()
  return {'schema':'owner-parsed-link-receipt-v1','scope':'Named owner-relative Markdown file targets; no anchor/external availability claim.',
   'source_files':[{'path':'t20/context/GUIDE.md','bytes':5,'sha256':sha(b'guide'),'parsed_link_count':1}],
   'links':[{'source':'t20/context/GUIDE.md','href':href,'kind':'local','target':target,'target_sha256':sha(b'source'),'target_bytes':6}],
   'parser':{'name':'markdown-it-py','version':'4.0.0','performed_during_assembly':True}}
 def test_true_owner_relative_target_passes(self):
  self.assertEqual(L.check_link_receipt(self.receipt('../cooperation/SOURCE.md','t20/cooperation/SOURCE.md'),self.files)['local_targets_verified'],1)
 def test_root_alias_existence_does_not_satisfy_nested_owner_url(self):
  with self.assertRaises(ValueError):L.check_link_receipt(self.receipt('t20/cooperation/SOURCE.md','t20/cooperation/SOURCE.md'),self.files)
 def test_escape_and_source_drift_are_rejected(self):
  with self.assertRaises(ValueError):L.resolve_owner_target('t20/context/GUIDE.md','../../../outside')
  r=self.receipt('../cooperation/SOURCE.md','t20/cooperation/SOURCE.md');self.files['t20/context/GUIDE.md']=b'changed'
  with self.assertRaises(ValueError):L.check_link_receipt(r,self.files)
 def test_target_drift_is_rejected(self):
  r=self.receipt('../cooperation/SOURCE.md','t20/cooperation/SOURCE.md')
  self.files['t20/cooperation/SOURCE.md']=b'changed target'
  with self.assertRaises(ValueError):L.check_link_receipt(r,self.files)
 def test_missing_target_is_rejected(self):
  r=self.receipt('../cooperation/SOURCE.md','t20/cooperation/SOURCE.md')
  del self.files['t20/cooperation/SOURCE.md']
  with self.assertRaises(ValueError):L.check_link_receipt(r,self.files)
 def test_anchor_query_and_encoded_path_are_scoped(self):
  self.assertEqual(L.resolve_owner_target('a/b.md','../c%20d.md?x=1#part'),('local','c d.md'))
  self.assertEqual(L.resolve_owner_target('a/b.md','#part'),('local','a/b.md'))
  self.assertEqual(L.resolve_owner_target('a/b.md','https://example.org/x'),('external',None))

class LayeredReviewTests(unittest.TestCase):
 def setUp(self):
  self.assertTrue(hasattr(N,'check_layered_review'),'Layered native review verifier must exist')
  self.full={'base_commit':'a'*40,'reviewed_tree':'b'*40,'disposition':'PASS_BOUNDED_FULL'}
  self.delta={'base_commit':'a'*40,'from_tree':'b'*40,'reviewed_tree':'c'*40,'disposition':'PASS_BOUNDED_DELTA'}
  self.bodies={'full.json':json.dumps(self.full).encode(),'delta.json':json.dumps(self.delta).encode()}
  h=lambda n:hashlib.sha256(self.bodies[n]).hexdigest()
  self.facts={'base_commit':'a'*40,'candidate_tree':'c'*40,'inherited_review_tree':'b'*40,'inherited_review_sha256':h('full.json'),'delta_review_sha256':h('delta.json')}
  self.binding={'facts':self.facts,'review_chain':{'mode':'INHERITED_FULL_PLUS_FINAL_DELTA','inherited_record':'full.json','delta_record':'delta.json'},'checks':[
   {'id':'review.inherited.base','record':'full.json','pointer':'/base_commit','fact':'base_commit'},
   {'id':'review.inherited.tree','record':'full.json','pointer':'/reviewed_tree','fact':'inherited_review_tree'},
   {'id':'review.inherited.disposition','record':'full.json','pointer':'/disposition','expected':'PASS_BOUNDED_FULL'},
   {'id':'review.delta.base','record':'delta.json','pointer':'/base_commit','fact':'base_commit'},
   {'id':'review.delta.predecessor','record':'delta.json','pointer':'/from_tree','fact':'inherited_review_tree'},
   {'id':'review.delta.tree','record':'delta.json','pointer':'/reviewed_tree','fact':'candidate_tree'},
   {'id':'review.delta.disposition','record':'delta.json','pointer':'/disposition','expected':'PASS_BOUNDED_DELTA'}]}
 def test_separate_full_and_delta_scopes_pass(self):
  self.assertEqual(N.check_layered_review(self.binding,self.bodies)['status'],'PASS_INHERITED_FULL_AND_FINAL_DELTA_BINDINGS')
 def test_same_record_cannot_be_relabelled_as_both_scopes(self):
  self.binding['review_chain']['delta_record']='full.json'
  with self.assertRaises(ValueError):N.check_layered_review(self.binding,self.bodies)
 def test_same_review_body_under_two_paths_is_rejected(self):
  common={'base_commit':'a'*40,'reviewed_tree':'b'*40,'from_tree':'b'*40,'next_tree':'c'*40,
          'disposition':'PASS_BOUNDED_FULL','delta_disposition':'PASS_BOUNDED_DELTA'}
  body=json.dumps(common).encode();self.bodies={'full.json':body,'delta.json':body}
  self.facts['inherited_review_sha256']=hashlib.sha256(body).hexdigest()
  self.facts['delta_review_sha256']=self.facts['inherited_review_sha256']
  for row in self.binding['checks']:
   if row['id']=='review.delta.tree':row['pointer']='/next_tree'
   if row['id']=='review.delta.disposition':row['pointer']='/delta_disposition'
  # Even a summary with both scopes cannot substitute for two distinct receipts.
  with self.assertRaises(ValueError):N.check_layered_review(self.binding,self.bodies)
 def test_full_review_cannot_be_promoted_to_final_tree(self):
  self.binding['checks'][1]['fact']='candidate_tree'
  with self.assertRaises(ValueError):N.check_layered_review(self.binding,self.bodies)
 def test_wrong_delta_predecessor_and_swapped_digest_are_rejected(self):
  self.delta['from_tree']='d'*40;self.bodies['delta.json']=json.dumps(self.delta).encode();self.facts['delta_review_sha256']=hashlib.sha256(self.bodies['delta.json']).hexdigest()
  with self.assertRaises(ValueError):N.check_layered_review(self.binding,self.bodies)
  self.facts['inherited_review_sha256']=self.facts['delta_review_sha256']
  with self.assertRaises(ValueError):N.check_layered_review(self.binding,self.bodies)
if __name__=='__main__':unittest.main()
