from pathlib import Path
import re,unittest
ROOT=Path('private-locator:b161f5e6ec5b32183f0f')
class ReadbackRegression(unittest.TestCase):
 def test_native_check_readback_is_recognised(self):
  runner=(ROOT/'shadow/tools/run_formal419.py').read_text()
  expression=re.search(r"if not re\.search\((r'.*'),audit\):raise RuntimeError\('Missing type readback",runner).group(1)
  target='P03Q1f.Chain.mapEdge'; pattern=eval(expression,{'re':re,'target':target})
  native=(ROOT/'repaired-formal-1/build-P03Audit.stdout.bin').read_text()
  self.assertIsNotNone(re.search(pattern,native))
  self.assertIsNone(re.search(pattern,"'P03Q1f.Chain.mapEdge' does not depend on any axioms"))
  self.assertIsNone(re.search(pattern,'@P03Q1f.Chain.mapEdgeForged : True'))
if __name__=='__main__':unittest.main()
