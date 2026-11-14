"""Focused current-checkout partition and durable restoration regression controls.

Tiny public fixtures test mechanics, not qualification of the real1180 corpus.
"""
import importlib.util
import pathlib
import tempfile
import unittest
import subprocess
import stat
from unittest.mock import patch

ROOT = pathlib.Path(__file__).resolve().parents[1]
def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / filename)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result
r = module('current_checkout_runner', 'check_source_alias_absence.py')
pop = module('current_checkout_population', 'source_alias_absence_population.py')

class Scope(unittest.TestCase):
 def setUp(self):
  self.classes=[{'alias':'present','canonical':'canonical'},{'alias':'retired','canonical':'canonical'}]
  self.before={'rows':[{'path':'present'},{'path':'canonical'}]}
  self.prepared={'profile':'current-checkout1180-v1','initially_absent_aliases':['retired'],'trial_removed_aliases':['present'],'expected_absent_tracked':1,'preimage_paths':5}
 def test_current_scope(self):
  self.assertEqual(r.trial_partition(self.prepared,self.before,self.classes),{'profile':'current-checkout1180-v1','historical_aliases_observed':2,'planned_trial_removals':1,'previously_absent_aliases':1})
 def test_cannot_relabel_current_as_historical(self):
  self.prepared['profile']='historical-all-present1180-v1';self.assertRaises(RuntimeError,r.trial_partition,self.prepared,self.before,self.classes)
 def test_unknown_profile(self):
  self.prepared['profile']='override';self.assertRaises(RuntimeError,r.trial_partition,self.prepared,self.before,self.classes)
 def test_partition_changed(self):
  self.prepared['trial_removed_aliases']+=['retired'];self.assertRaises(RuntimeError,r.trial_partition,self.prepared,self.before,self.classes)
 def test_denominator_changed(self):
  self.prepared['expected_absent_tracked']=0;self.assertRaises(RuntimeError,r.trial_partition,self.prepared,self.before,self.classes)
 def test_backup_count_changed(self):
  self.prepared['preimage_paths']=6;self.assertRaises(RuntimeError,r.trial_partition,self.prepared,self.before,self.classes)
 def test_historical_packet_compatible(self):
  self.before['rows'].append({'path':'retired'});self.prepared.update(profile='historical-all-present1180-v1',initially_absent_aliases=[],trial_removed_aliases=['present','retired'],preimage_paths=6)
  self.assertEqual(r.trial_partition(self.prepared,self.before,self.classes)['previously_absent_aliases'],0)
 def test_recreated_retired_alias_preserved_and_blocks_restore(self):
  with tempfile.TemporaryDirectory() as d:
   p=pathlib.Path(d)/'retired';r.require_retired_absence(d,self.prepared);p.write_bytes(b'unexpected')
   self.assertRaises(RuntimeError,r.require_retired_absence,d,self.prepared)
   self.assertEqual(p.read_bytes(),b'unexpected')
class Restoration(unittest.TestCase):
 def check_interrupt(self,index_changed):
  with tempfile.TemporaryDirectory() as d:
   root=pathlib.Path(d);repo=root/'repo';repo.mkdir();state=root/'state';state.mkdir()
   def git(*args):return subprocess.check_output(['git','-C',str(repo),*args],stderr=subprocess.DEVNULL)
   git('init');(repo/'present').write_bytes(b'public original');(repo/'canonical').write_bytes(b'public original');(repo/'held').write_bytes(b'sentinel never opened')
   git('add','.');raw=(repo/'.git/index').read_bytes()
   before={'directories':[{'path':'.','mode':stat.S_IMODE(repo.stat().st_mode)}],'index_mode':stat.S_IMODE((repo/'.git/index').stat().st_mode)}
   read=pathlib.Path.read_bytes
   def guarded(path):
    if path==repo/'held':raise AssertionError('protected read')
    return read(path)
   with patch.object(pathlib.Path,'read_bytes',guarded):
    r.save_preimages(repo,state,{'present','canonical'},{'held'})
    prepared={'preimages':r.identity((state/'preimages.json').read_bytes()),'raw_index':r.identity(raw),'initially_absent_aliases':['retired']}
    (repo/'present').unlink()
    if index_changed:git('update-index','--force-remove','--','present')
    r.require_retired_absence(repo,prepared)
    r.restore_preimages(repo,state,prepared,before,{'held'})
    self.assertEqual((repo/'present').read_bytes(),b'public original');self.assertEqual((repo/'.git/index').read_bytes(),raw);self.assertFalse((repo/'retired').exists())
    r.restore_preimages(repo,state,prepared,before,{'held'})
    self.assertEqual((repo/'.git/index').read_bytes(),raw)
 def test_interruption_after_unlink(self):self.check_interrupt(False)
 def test_interruption_after_index_update(self):self.check_interrupt(True)

class Presence(unittest.TestCase):
 def test_index_partition_and_negative_controls(self):
  with tempfile.TemporaryDirectory() as d:
   root=pathlib.Path(d);identity={'mode':'100644','blob':'a'*40};stage={'alias':('100644','a'*40),'canonical':('100644','a'*40)}
   self.assertTrue(pop.current_alias_present(root,'alias','canonical',identity,stage))
   stage.pop('alias');self.assertFalse(pop.current_alias_present(root,'alias','canonical',identity,stage))
   for wrong in ({}, {'canonical':('100755','a'*40)}, {'canonical':('100644','b'*40)}, dict(stage,alias=('100755','a'*40))):
    self.assertRaises(ValueError,pop.current_alias_present,root,'alias','canonical',identity,wrong)
   (root/'alias').write_bytes(b'untracked');self.assertRaises(ValueError,pop.current_alias_present,root,'alias','canonical',identity,stage)
   (root/'alias').unlink();(root/'alias').symlink_to('absent');self.assertRaises(ValueError,pop.current_alias_present,root,'alias','canonical',identity,stage)

if __name__ == '__main__':
 unittest.main()
