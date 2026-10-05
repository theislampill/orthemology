"""Test-first contract. Synthetic source roles, never natural-language gold labels."""
import itertools
import math
import unittest
from fractions import Fraction as F
from context_effects import (Origin, Ref, Invalid, MissingBinding, compile_effect,
    compose, apply_effect, rename_outputs, resolve_demands)
from read_cover import (Window, Cover, BadCoverage, active_menu, cover_dp,
    interval_cover, role_decision, minimax_cost, star_locality, coverage_sufficiency)

A,B,C,D,Z = [Origin('s',x) for x in 'abcdz']

def enter(o): return ('enter',o)
def emit(t): return ('emit',t)
def leave(): return ('leave',)
def exit_(o): return ('exit',o)
def w(name,keys,cost=1,**kw): return Window(name,frozenset(keys),F(cost),**kw)
def product_worlds(keys): return tuple(dict(zip(keys,b)) for b in itertools.product((0,1),repeat=len(keys)))
def q(world,keys): return all(world[k] for k in keys)
def response(world,win): return tuple((k,world[k]) for k in sorted(win.coverage))

class EffectContract(unittest.TestCase):
 def test_01_empty(self):
  e=compile_effect([]);self.assertEqual(e.depth,1);self.assertEqual(apply_effect(e,[A]),((A,),()))
 def test_02_pop_bottom_even_before_push(self):
  for events in [[leave()],[leave(),enter(B)]]:
   with self.assertRaises(Invalid):apply_effect(compile_effect(events),[A])
 def test_03_local_return(self):
  e=compile_effect([enter(B),leave(),emit('t')]);self.assertEqual(e.emissions,(('t',Ref(0)),));self.assertEqual(apply_effect(e,[A])[1],(('t',A),))
 def test_04_twice(self):
  e=compile_effect([leave(),leave(),emit('t')]);self.assertEqual((e.depth,e.emissions),(3,(('t',Ref(2)),)))
 def test_05_composed_depth(self):
  e=compose(compile_effect([enter(B)]),compile_effect([leave(),leave(),emit('t')]))
  self.assertEqual((e.depth,e.emissions),(2,(('t',Ref(1)),)))
 def test_06_net_height_insufficient(self):
  e=compile_effect([leave(),enter(B)]);self.assertEqual((e.depth,e.prefix,e.consumed),(2,(B,),1));self.assertEqual(apply_effect(e,[A,C])[0],(B,C))
 def test_07_unselected(self):
  e=compile_effect([enter(B),emit('ignored'),leave(),emit('t')],selected={'t'})
  self.assertEqual(e.emissions,(('t',Ref(0)),))
 def test_08_output_collision_and_rename(self):
  e=compile_effect([emit('t')])
  with self.assertRaises(Invalid):compose(e,e)
  self.assertEqual(len(compose(rename_outputs(e,'one'),rename_outputs(e,'two')).emissions),2)
 def test_09_alias(self):
  e=compile_effect([emit('t'),leave(),emit('u')]);self.assertEqual(resolve_demands(e,{0:A,1:A}),frozenset({A}))
 def test_10_same_text_not_identity(self):
  e=compile_effect([emit('t'),leave(),emit('u')]);self.assertEqual(resolve_demands(e,{0:A,1:B}),frozenset({A,B}))
 def test_11_association_domain(self):
  f,g,h=map(compile_effect,[[enter(B)],[leave(),leave()],[enter(C),emit('t')]])
  self.assertEqual(compose(compose(f,g),h),compose(f,compose(g,h)))
  with self.assertRaises(Invalid):apply_effect(compose(f,compose(g,h)),[A])
 def test_12_missing_identity_map(self):
  e=compile_effect([leave(),leave(),emit('t')])
  with self.assertRaises(MissingBinding):resolve_demands(e,{0:A,1:B})
 def test_13_wrong_snapshot(self):
  e=compile_effect([exit_(A)]);
  with self.assertRaises(Invalid):apply_effect(e,[Origin('other','a'),B])
 def test_43_keyed_exit_mismatch(self):
  with self.assertRaises(Invalid):apply_effect(compile_effect([exit_(C)]),[A,B])
 def test_44_keyed_contradiction(self):
  f=compile_effect([exit_(A),enter(A)]);g=compile_effect([exit_(B)])
  e=compose(f,g);self.assertTrue(e.impossible)
  with self.assertRaises(Invalid):apply_effect(e,[A,B])

class RoleContract(unittest.TestCase):
 def test_14_local_author_inside_quote(self):
  self.assertFalse(role_decision({A},{A:False})) # local speaker 'author' is not this field
 def test_15_return_into_report(self):
  keys=resolve_demands(compile_effect([leave(),emit('t')]),{0:A,1:B})
  self.assertFalse(role_decision(keys,{B:False}))
 def test_16_return_to_argument(self):
  keys=resolve_demands(compile_effect([leave(),leave(),emit('t')]),{0:C,1:B,2:A})
  self.assertTrue(role_decision(keys,{A:True}))
 def test_17_reply_target_separate(self):
  self.assertTrue(role_decision({A},{A:True})) # no reply-target API is supplied
 def test_18_current_carrier_force_separate(self):
  packet={'source_roles':{A:True},'current_force':'quotation'}
  self.assertTrue(role_decision({A},packet['source_roles']));self.assertEqual(packet['current_force'],'quotation')
 def test_19_known_heading(self):
  self.assertTrue(role_decision({A},{A:True}));self.assertFalse(role_decision({A},{A:False}))
 def test_23_known_false(self):self.assertFalse(role_decision({A,B},{A:False}))
 def test_29_abstention_not_total(self):self.assertIsNone(role_decision({A,B},{}))
 def test_39_preloaded(self):self.assertTrue(role_decision({A,B},{A:True,B:True}))

class ReadContract(unittest.TestCase):
 def test_20_total_all_positive(self):
  keys=[A,B,C];menu=[w('ab',[A,B]),w('bc',[B,C])];worlds=product_worlds(keys)
  self.assertTrue(star_locality(worlds,keys,menu,response))
  self.assertEqual(minimax_cost(worlds,menu,lambda x:q(x,keys),response),F(2));self.assertEqual(cover_dp(keys,menu).cost,F(2))
 def test_21_negative_early(self):
  keys=[A,B,C];menu=[w('a',[A]),w('bc',[B,C],10)]
  self.assertEqual(cover_dp(keys,menu).cost,F(11));self.assertFalse(role_decision(keys,{A:False}))
 def test_22_missing_coverage(self):
  menu=[w('a',[A])];worlds=product_worlds([A,B])
  self.assertEqual(cover_dp([A,B],menu).cost,math.inf)
  self.assertEqual(minimax_cost(worlds,menu,lambda x:q(x,[A,B]),response),math.inf)
 def test_24_correlated_keys(self):
  worlds=({A:0,B:0},{A:1,B:1});menu=[w('a',[A])]
  self.assertFalse(star_locality(worlds,[A,B],menu,response));self.assertEqual(minimax_cost(worlds,menu,lambda x:q(x,[A,B]),response),F(1))
 def test_25_outside_summary_leak(self):
  worlds=tuple(dict(x,**{})|{Z:int(q(x,[A,B]))} for x in product_worlds([A,B]));menu=[w('z',[Z]),w('ab',[A,B],10)]
  self.assertFalse(star_locality(worlds,[A,B],menu,response));self.assertEqual(minimax_cost(worlds,menu,lambda x:q(x,[A,B]),response),F(1));self.assertEqual(cover_dp([A,B],menu).cost,F(10))
 def test_26_rich_response_leak(self):
  worlds=product_worlds([A,B]);menu=[w('a',[A])];rich=lambda x,_:(x[A],x[B])
  self.assertFalse(star_locality(worlds,[A,B],menu,rich));self.assertEqual(minimax_cost(worlds,menu,lambda x:q(x,[A,B]),rich),F(1))
 def test_27_public_metadata_leak(self):
  worlds=product_worlds([A,B]);menu=[w('ab',[A,B])]
  self.assertFalse(star_locality(worlds,[A,B],menu,response,metadata=lambda x:x[B]))
 def test_28_status_size_timing_leak(self):
  worlds=product_worlds([A,B]);menu=[w('a',[A])]
  for field in ['status','size','timing']:
   resp=lambda x,win:(response(x,win),(field,x[B]))
   self.assertFalse(star_locality(worlds,[A,B],menu,resp))
 def test_30_quotient_scrambled(self):
  targets=[C,A,B,A,C];menu=[w('ab',[A,B]),w('c',[C])]
  self.assertEqual(interval_cover(targets,[A,B,C],menu).cost,F(2))
 def test_31_weighted_greedy_trap(self):
  menu=[w('all',[A,B],100),w('a',[A]),w('b',[B])]
  self.assertEqual(interval_cover([A,B],[A,B],menu).cost,F(2))
 def test_32_overlap(self):
  menu=[w('ac',[A,B,C],3),w('bd',[B,C,D],3),w('a',[A]),w('d',[D])]
  self.assertEqual(interval_cover([A,B,C,D],[A,B,C,D],menu).cost,F(4))
 def test_33_empty_uncovered(self):
  self.assertEqual(interval_cover([A],[A,B],[w('b',[B])]).cost,math.inf)
  self.assertEqual(interval_cover([],[],[]).cost,F(0))
 def test_34_inadequate_raw_text(self):
  menu=[w('raw',[A,B],adequate=False)]
  self.assertEqual(active_menu(menu),());self.assertEqual(cover_dp([A,B],menu).cost,math.inf)
 def test_35_nonconvex_cards(self):
  menu=[w('ac',[A,C]),w('b',[B])]
  with self.assertRaises(BadCoverage):interval_cover([A,B,C],[A,B,C],menu)
  self.assertEqual(cover_dp([A,B,C],menu).cost,F(2))
 def test_36_whole_source(self):
  menu=[w('ab',[A,B]),w('bc',[B,C]),w('whole',[A,B,C])]
  self.assertEqual(cover_dp([A,B,C],menu).cost,F(1))
 def test_37_singletons(self):
  menu=[w('ac',[A,C]),w('a',[A]),w('b',[B]),w('c',[C])]
  self.assertEqual(cover_dp([A,B,C],menu).cost,F(2))
 def test_38_spanning_read(self):
  self.assertEqual(cover_dp([A,B,C],[w('a',[A]),w('bc',[B,C]),w('span',[A,B,C])]).cost,F(1))
 def test_40_preparation_separate(self):
  read=cover_dp([A],[w('a',[A])]).cost;preparation=F(7)
  self.assertEqual(preparation+read,F(8));self.assertNotEqual(read,preparation+read)
 def test_41_padding(self):
  self.assertEqual(cover_dp([A,B],[w('az',[A,Z]),w('bz',[B,Z])]).cost,F(2))
 def test_42_matched_baseline(self):
  keys=[A,B,C];menu=[w('ab',[A,B],F(1,2)),w('bc',[B,C],F(3,2))]
  self.assertEqual(cover_dp(keys,menu).cost,interval_cover(keys,keys,menu).cost)
  self.assertEqual(cover_dp(keys,menu).cost,minimax_cost(product_worlds(keys),menu,lambda x:q(x,keys),response))
 def test_45_service_retirement_and_targeted_retention(self):
  cards=[w('ab',[A,B]),w('bc',[B,C])]
  self.assertEqual(cover_dp([C,A,B,A],cards+[w('source',[A,B,C])]).cost,F(1))
  self.assertEqual(cover_dp([C,A,B,A],cards).cost,F(2))
  self.assertEqual(cover_dp([B,C],cards).cost,F(1)) # carry a
  self.assertEqual(cover_dp([A,B],cards).cost,F(1)) # carry c
  self.assertEqual(cover_dp([A,C],cards).cost,F(2)) # carry b
 def test_46_valid_fixed_query_verdict(self):
  # A valid already-held verdict changes holdings, so zero further read cost.
  worlds=tuple(x for x in product_worlds([A,B,C]) if q(x,[A,B,C]))
  self.assertEqual(minimax_cost(worlds,[],lambda x:q(x,[A,B,C]),response),F(0))
 def test_48_retention_selection_channel(self):
  keys=[A,B,C];worlds=product_worlds(keys)
  selection=lambda x:A if q(x,keys) else B
  self.assertFalse(star_locality(worlds,keys,[],response,metadata=selection))
  self.assertEqual(minimax_cost(worlds,[],lambda x:q(x,keys),response,metadata=selection),F(0))
  # The retention comparison uses fixed selectors, not the above verdict code.
  self.assertTrue(star_locality(worlds,keys,[],response,metadata=lambda _:B))
 def test_49_locality_is_not_adequacy(self):
  worlds=product_worlds([A,B]);menu=[w('all',[A,B])];constant=lambda _x,_w:'constant'
  self.assertTrue(star_locality(worlds,[A,B],menu,constant))
  self.assertFalse(coverage_sufficiency(worlds,menu,constant))
  self.assertEqual(minimax_cost(worlds,menu,lambda x:q(x,[A,B]),constant),math.inf)
  self.assertTrue(coverage_sufficiency(worlds,menu,response))
 def test_47_unavailable_right(self):
  self.assertEqual(cover_dp([A],[w('a',[A],eligible=False)]).cost,math.inf)

if __name__=='__main__':unittest.main()
