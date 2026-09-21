import unittest,threading,itertools
import reference as r
import extensions as e
from test_reference import PID,PT,PF,ID,BOOL,ae

def prim(name):return {'op':'primitive','name':name}
def seq(a,b):return {'op':'compose','first':a,'second':b}
class Operations(unittest.TestCase):
 def setUp(self):
  try:import operational as o
  except ImportError:self.fail('operational construction absent')
  self.o=o;self.eng=o.Engine.standard()
 def runop(self,c,x):return self.eng.dispatch(self.eng.admit(c),x)
 def test_nontrivial(self):
  self.assertEqual(self.runop(prim('succ'),2),3);self.assertIs(self.runop(prim('iszero'),0),True);self.assertIs(self.runop(prim('not'),True),False)
 def test_composition_and_parallel(self):
  self.assertIs(self.runop(seq(prim('succ'),prim('iszero')),0),False)
  self.assertEqual(self.runop({'op':'parallel','left':prim('succ'),'right':prim('not')},[2,True]),[3,False])
 def test_family(self):
  c={'op':'id','type':'nat'}
  for n in range(20):
   self.assertEqual(self.runop(c,0),n);c=seq(c,prim('succ'))
 def test_reject_all(self):
  self.eng.revise_rule('primitive:succ',False);self.assertFalse(self.o.positive_probe(self.eng))
 def test_stale_and_aba(self):
  c=self.eng.admit(prim('succ'));self.eng.revise_rule('primitive:succ',False)
  with self.assertRaises(r.Rejection):self.eng.dispatch(c,1)
  self.eng.revise_rule('primitive:succ',True)
  with self.assertRaises(r.Rejection):self.eng.dispatch(c,1)
  self.assertEqual(self.runop(prim('succ'),1),2)
 def test_unrelated_reuse(self):
  c=self.eng.admit(prim('succ'));self.eng.revise_rule('primitive:not',False);self.assertEqual(self.eng.dispatch(c,1),2)
 def test_dependency_union(self):
  c=self.eng.admit(seq(prim('succ'),prim('iszero')));self.eng.revise_rule('primitive:iszero',False)
  with self.assertRaises(r.Rejection):self.eng.dispatch(c,1)
 def test_projection(self):
  a=self.eng.admit(prim('succ'));b=self.eng.admit(prim('not'));self.eng.revise_rule('primitive:succ',False)
  self.assertEqual([x['ticket'] for x in self.eng.project()],[b.ticket])
 def test_source_immutable(self):
  x=prim('succ');c=self.eng.admit(x);x['name']='not';self.assertEqual(self.eng.dispatch(c,1),2)
 def test_observation_refinement(self):
  self.eng.set_observation('coarse',[0,0,1]);op={'op':'edge','size':3,'source':0,'target':1};c=self.eng.admit(op)
  self.assertEqual(self.eng.dispatch(c,0),1);self.eng.set_observation('fine',[0,1,2])
  with self.assertRaises(r.Rejection):self.eng.dispatch(c,0)
  with self.assertRaises(r.Rejection):self.eng.admit(op)
  self.eng.remove_observation('fine');self.assertEqual(self.runop(op,0),1)
 def test_internal_identity_self(self):
  y=self.runop({'op':'core','proof':ae(PID,ID)},{'proof':PID});t,a=r.check(y['proof'])
  self.assertEqual(a,ID);self.assertEqual(r.normalize(t)[0],e.I)
 def test_internal_selector_self(self):
  a=self.runop({'op':'core','proof':ae(PF,BOOL)},{'proof':PT})
  b=self.runop({'op':'core','proof':a['proof']},{'proof':PF});t,ty=r.check(b['proof'])
  self.assertEqual(ty,BOOL);self.assertEqual(r.normalize(t)[0],e.app(e.K,e.I))
 def test_native_selector_bridge(self):
  for p,n in [(PT,8),(PF,13)]:
   t,_=r.check(p);_,tr=r.normalize(e.app(e.app(t,e.Z),e.O))
   self.assertEqual(self.runop({'op':'selector','type':'nat','proof':p,'trace':tr},[8,13]),n)
 def test_malformed(self):
  for c in [seq(prim('succ'),prim('not')),{'op':'shell','command':'bad'},{'op':'core','proof':PID}]:
   with self.assertRaises(r.Rejection):self.eng.admit(c)
  with self.assertRaises(r.Rejection):self.eng.admit_json(b'{"op":"id","op":"primitive","name":"succ"}')
  with self.assertRaises(r.Rejection):self.eng.dispatch(self.o.Licence('forged'),0)
 def test_values_and_bounds(self):
  c=self.eng.admit(prim('succ'))
  for x in [True,-1,'3',None,(1<<256)-1]:
   with self.assertRaises(r.Rejection):self.eng.dispatch(c,x)
 def test_linearizable_revision(self):
  c=self.eng.admit(prim('succ'));entered=threading.Event();release=threading.Event();done=threading.Event();out=[];real=self.eng._execute
  def slow(o,x):entered.set();release.wait(3);return real(o,x)
  self.eng._execute=slow
  t=threading.Thread(target=lambda:out.append(self.eng.dispatch(c,1)));t.start();self.assertTrue(entered.wait(3))
  u=threading.Thread(target=lambda:(self.eng.revise_rule('primitive:succ',False),done.set()));u.start();self.assertFalse(done.wait(.05));release.set();t.join(3);u.join(3)
  self.assertEqual(out,[2]);self.assertTrue(done.is_set())
 def test_productive_typed_leaves_and_revocation(self):
  c=self.eng.admit({'op':'sampler','left':PT,'right':PF})
  pending=self.eng.dispatch(c,[]);self.assertEqual(pending['status'],'pending')
  done=self.eng.dispatch(c,[0,0]);self.assertEqual(done['status'],'done');self.assertEqual(r.check(done['proof'])[1],BOOL)
  self.eng.revise_rule('sampler',False)
  with self.assertRaises(r.Rejection):self.eng.dispatch(c,[0,0])
 def test_productive_prefix_law(self):
  c=self.eng.admit({'op':'sampler','left':PT,'right':PF})
  for n in range(9):
   counts={'left':0,'right':0,'pending':0}
   for bits in itertools.product((0,1),repeat=n):
    x=self.eng.dispatch(c,list(bits));counts['pending' if x['status']=='pending' else x['branch']]+=1
   m=e.irrational_prefix_mass(n)
   self.assertEqual(counts['pending'],1);self.assertEqual(counts['left'],m['first']*(1<<n))
if __name__=='__main__':unittest.main()
