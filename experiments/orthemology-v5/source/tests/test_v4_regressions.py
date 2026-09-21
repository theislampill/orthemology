import json,subprocess,sys,unittest,tempfile,pathlib
import reference as r
import extensions as e

class InputRepairs(unittest.TestCase):
 def test_bytes_duplicate_and_bad_encoding(self):
  for b in [b'{"rule":"bad","rule":"i","A":["bottom"]}',b'{} {}',b'\xff',b'{"x":NaN}',b'{"x":1.1}',b'{"x":'+b'9'*200+b'}']:
   with self.assertRaises(r.Rejection):r.check_json(b)
 def test_bytes_success(self):self.assertEqual(r.check_json(b'{"rule":"i","A":["bottom"]}'),r.check({'rule':'i','A':['bottom']}))
 def test_accepted_output_validates(self):
  p={'rule':'i','A':['v',0]}
  for _ in range(100):p={'rule':'all_i','body':p}
  try:t,a=r.check(p)
  except r.Rejection:return
  r._freeze(a);r._freeze(t)
 def test_selector_objects_fail_declared(self):
  for x in [None,{},e.SelectorCertificate(e.K,(),0)]:
   with self.assertRaises(r.Rejection):e.replay_selector(x,e.I,e.K)
 def test_integer_cap(self):
  with self.assertRaises(r.Rejection):r.shift_type(('v',1<<2048),1)
  with self.assertRaises(r.Rejection):e._weight([1,1<<2048])
 def test_cyclic_ast(self):
  p={'rule':'all_i'};p['body']=p
  with self.assertRaises(r.Rejection):r.check(p)
 def test_optimisation_negative_control(self):
  p=subprocess.run([sys.executable,'-O','-c','import census;census.e.named_instantiate=lambda b,a:("bottom",);census.run()'],capture_output=True,text=True,timeout=30)
  self.assertNotEqual(p.returncode,0,'mutated substitution wrongly passed under -O')

if __name__=='__main__':unittest.main()
