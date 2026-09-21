import tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import check_mutations as m
class LegacyMutationIntegrity(unittest.TestCase):
 def test_real_named_test_not_import_failure_is_the_detection(self):
  with tempfile.TemporaryDirectory() as td,patch.object(m,'MUTATIONS',m.MUTATIONS[:1]):
   report=m.run(Path(td));row=report['results'][0]
   text=(Path(td)/row['log']).read_text()
   self.assertNotIn('ModuleNotFoundError',text,'dependency failure was counted as a killed mutant')
   self.assertTrue(row.get('positive_ok',False),'normal named regression was not first checked')
   self.assertIn('FAILED (failures=',text)
   self.assertNotIn('Failed to import',text)
