import json,unittest
from pathlib import Path
import proof_export
class GeneratedExamplesTests(unittest.TestCase):
 def test_generated_target_is_exact_reproducible_output(self):
  root=Path(__file__).resolve().parents[1]
  index=root/'examples'/'EXPORT_INDEX.json'
  self.assertTrue(index.is_file(),'source inputs/index not supplied')
  rows=json.loads(index.read_text())
  generated=proof_export.module([(r['name'],(root/r['path']).read_bytes()) for r in rows])
  self.assertEqual((root/'lean'/'GeneratedExamples.lean').read_text(),generated)
  self.assertGreaterEqual(len(rows),6)
