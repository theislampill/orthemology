import unittest
from itertools import combinations
from grounded_support import minimal_supports,available_claims,cuts,minimum_cuts,quotient_supports

def subsets(xs):
 xs=tuple(xs)
 return [frozenset(c) for k in range(len(xs)+1) for c in combinations(xs,k)]
def direct_closure(base,rules,alive):
 out={c for r,c in base if r in alive}
 while True:
  nxt=out|{h for b,h in rules if set(b)<=out}
  if nxt==out:return out
  out=nxt
def exact_supports(base,rules,roots,c):
 ss=[s for s in subsets(roots) if c in direct_closure(base,rules,s)]
 return frozenset(s for s in ss if not any(t<s for t in ss))
class GroundedSupportTests(unittest.TestCase):
 def test_unanchored_cycle_empty_anchor_propagates(self):
  rules=[(frozenset({'b'}),'a'),(frozenset({'a'}),'b')]
  self.assertEqual(minimal_supports([],rules).get('a',frozenset()),frozenset())
  self.assertEqual(minimal_supports([('r','a')],rules).get('b',frozenset()),frozenset({frozenset({'r'})}))
 def test_testimony_and_prospective_authority_are_different(self):
  base=[('source','owns-duty-0'),('truth','veracious'),('past-order','issued-at-0'),('past-standing','standing-at-0'),('grant-now','live-standing'),('scope-now','within-scope-now'),('occasion','applicable-now-0'),('implementation','ready')]
  rules=[(frozenset({'owns-duty-0','veracious'}),'duty-0'),(frozenset({'issued-at-0','standing-at-0'}),'duty-0'),(frozenset({'live-standing','within-scope-now'}),'may-issue-next'),(frozenset({'duty-0','applicable-now-0','ready'}),'act-now')]
  got=minimal_supports(base,rules);roots={r for r,c in base}
  self.assertEqual(got.get('duty-0'),frozenset({frozenset({'source','truth'}),frozenset({'past-order','past-standing'})}))
  after=available_claims(got,roots-{'grant-now'})
  self.assertIn('duty-0',after);self.assertIn('act-now',after);self.assertNotIn('may-issue-next',after)
  self.assertIn('duty-0',available_claims(got,roots-{'occasion'}))
  self.assertNotIn('act-now',available_claims(got,roots-{'occasion'}))
  self.assertNotIn('duty-0',available_claims(got,roots-{'source','past-standing'}))
 def test_axiom_and_underivable(self):
  got=minimal_supports([],[(frozenset(),'axiom')])
  self.assertEqual(got.get('axiom'),frozenset({frozenset()}))
  self.assertNotIn('missing',got)
  self.assertEqual(cuts(got['axiom'],set()),frozenset())
  self.assertEqual(cuts(frozenset(),set()),frozenset({frozenset()}))
 def test_k32_cut_order(self):
  ss=frozenset(frozenset({a,b}) for a in ('a1','a2','a3') for b in ('b','c'))
  pi={'a1':'a','a2':'a','a3':'a','b':'b','c':'c'}
  self.assertEqual(minimum_cuts(ss,set(pi)),frozenset({frozenset({'b','c'})}))
  self.assertEqual(minimum_cuts(quotient_supports(ss,pi),set(pi.values())),frozenset({frozenset({'a'})}))
 def test_four_label_cut_order(self):
  ss=frozenset({frozenset({'a1'}),frozenset({'a2','b'}),frozenset({'a3','b'})});pi={'a1':'a','a2':'a','a3':'a','b':'b'}
  self.assertEqual(minimum_cuts(ss,set(pi)),frozenset({frozenset({'a1','b'})}))
  self.assertEqual(quotient_supports(ss,pi),frozenset({frozenset({'a'})}))
 def test_all_small_positive_systems(self):
  claims=(0,1,2);roots=(0,1);base=[(0,0),(1,1)];candidates=[(s,c) for s in subsets(claims) for c in claims];systems=profiles=0
  for k in range(4):
   for rules in combinations(candidates,k):
    systems+=1;got=minimal_supports(base,rules)
    for c in claims:self.assertEqual(got.get(c,frozenset()),exact_supports(base,rules,roots,c))
    for alive in subsets(roots):
     profiles+=1;self.assertEqual(available_claims(got,alive),direct_closure(base,rules,alive))
  self.assertEqual(systems,2325);self.assertEqual(profiles,9300)

class CutSearchTests(unittest.TestCase):
 def test_four_label_fixture_is_cheaper_after_root_identification(self):
  ss=frozenset({frozenset({0}),frozenset({1,3}),frozenset({2,3})});pi={0:0,1:0,2:0,3:1}
  old=minimum_cuts(ss,set(pi));wrong=min(len({pi[x] for x in c}) for c in old)
  true=min(len(c) for c in minimum_cuts(quotient_supports(ss,pi),set(pi.values())))
  self.assertEqual((wrong,true),(2,1))

if __name__=='__main__':unittest.main()
