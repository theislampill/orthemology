"""Synthetic failure controls; no study input is required."""
import pathlib,subprocess,sys,tempfile,unittest

SCRIPT=pathlib.Path(__file__).with_name('replay.py')

class CliTests(unittest.TestCase):
    def test_explicit_arguments_required(self):
        r=subprocess.run([sys.executable,str(SCRIPT)],capture_output=True,text=True)
        self.assertEqual(r.returncode,2)
        self.assertIn('--raw-export',r.stderr)
    def test_nonempty_destination_preserved(self):
        with tempfile.TemporaryDirectory() as t:
            p=pathlib.Path(t);a=p/'a';b=p/'b';a.write_text('synthetic');b.write_text('synthetic')
            out=p/'out';out.mkdir();marker=out/'keep';marker.write_text('unchanged')
            r=subprocess.run([sys.executable,str(SCRIPT),'--raw-export',str(a),'--author-responses',str(b),'--output-root',str(out)],capture_output=True,text=True)
            self.assertEqual(r.returncode,2);self.assertEqual(marker.read_text(),'unchanged')
            self.assertEqual(sorted(x.name for x in out.iterdir()),['keep'])
    def test_wrong_digest_stops_estimation(self):
        with tempfile.TemporaryDirectory() as t:
            p=pathlib.Path(t);a=p/'a';b=p/'b';a.write_text('synthetic');b.write_text('synthetic');out=p/'out'
            r=subprocess.run([sys.executable,str(SCRIPT),'--raw-export',str(a),'--author-responses',str(b),'--output-root',str(out)],capture_output=True,text=True)
            self.assertNotEqual(r.returncode,0);self.assertIn('input digest mismatch',r.stderr)
            self.assertFalse(list(out.rglob('*.json')))

if __name__=='__main__':unittest.main()
