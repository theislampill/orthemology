import pathlib,subprocess,unittest
P=pathlib.Path(__file__).resolve().parents[1]
class ReplayTests(unittest.TestCase):
 def test_list(self):
  self.assertTrue((P/'replay_selected.py').is_file(),'portable selected replay runner required')
  r=subprocess.run(['python','-B',str(P/'replay_selected.py'),'--list'],capture_output=True,text=True)
  self.assertEqual(r.returncode,0,r.stderr);self.assertIn('finite-contracts',r.stdout)
 def test_unknown_fails(self):
  self.assertTrue((P/'replay_selected.py').is_file(),'portable selected replay runner required')
  r=subprocess.run(['python','-B',str(P/'replay_selected.py'),'--suite','unknown'],capture_output=True,text=True)
  self.assertNotEqual(r.returncode,0)
if __name__=='__main__':unittest.main()
