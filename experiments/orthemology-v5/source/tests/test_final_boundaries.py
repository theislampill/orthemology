import contextlib,io,json,tempfile,tracemalloc,unittest
from pathlib import Path
from unittest.mock import patch
import boundaries as b
import verify

class FinalBoundaries(unittest.TestCase):
 def test_missing_manifest_stops_before_running_code(self):
  with tempfile.TemporaryDirectory() as src,tempfile.TemporaryDirectory() as out:
   with patch.object(verify,'ROOT',Path(src)),patch('sys.argv',['verify.py','--output-dir',out]),patch.object(verify.gate,'run_bounded',side_effect=AssertionError('unverified source was executed')) as run,contextlib.redirect_stdout(io.StringIO()):
    self.assertEqual(verify.main(),1);self.assertEqual(run.call_count,0)
   report=json.loads((Path(out)/'VERIFICATION.json').read_text());self.assertFalse(report['lean']['kernel_verified']);self.assertIn('preflight_error',report)
 def test_output_byte_bound_before_large_aggregate_allocation(self):
  payload=['x'*4096 for _ in range(512)];tracemalloc.start()
  try:
   with self.assertRaises(b.Rejection):b.dump_json(payload)
   peak=tracemalloc.get_traced_memory()[1]
  finally:tracemalloc.stop()
  self.assertLess(peak,4*b.MAX_BYTES,'serializer allocated full oversized output before refusing')

if __name__=='__main__':unittest.main()
