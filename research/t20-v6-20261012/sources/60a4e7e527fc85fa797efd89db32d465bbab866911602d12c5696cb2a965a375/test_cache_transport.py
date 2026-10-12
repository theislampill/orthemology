"""Exact diagnostics; unit-test assertions survive python -O."""
from fractions import Fraction as F
from itertools import product
import unittest
import cache_transport as c

class CacheTransportTests(unittest.TestCase):
    def fixture(self):
        R=c.g.Rule
        ea=frozenset({'e'})
        rules=(R('qa','q',(),ea,F(1)),R('qb','q',(),ea,F(2)),
               R('rq','r',('q',),frozenset(),F(10)),
               R('tqr','t',('q','r'),frozenset(),F(1)))
        qa=c.Node(rules[0],()); qb=c.Node(rules[1],())
        rb=c.Node(rules[2],(qb,))
        return ('q','r','t'),('e',),rules,qa,qb,rb

    def test_cached_macro_changes_optimum(self):
        J,E,R,qa,qb,rb=self.fixture(); cache=frozenset((qb,rb))
        value,node=c.cached_optimum(J,E,R,'t',frozenset(E),cache)
        self.assertEqual(value,F(1))
        self.assertEqual(c.incremental_cost(node,cache),F(1))
        self.assertIn(rb,c.footprint(node))

    def test_source_withdrawal_invalidates_descendants(self):
        J,E,R,qa,qb,rb=self.fixture(); cache=frozenset((qb,rb))
        self.assertEqual(c.active_cache(cache,R,frozenset()),frozenset())

    def test_actual_inherited_normalizer_loses_cached_identity(self):
        J,E,R,qa,qb,rb=self.fixture(); cache=frozenset((qb,rb))
        original=c.g.Dag(((R[0],()),(R[1],()),(R[2],(1,)),(R[3],(0,2))),3)
        reduced=c.g.normalize(original,J,E,R)
        self.assertEqual(c.g.dag_value(original,J,E,R)[2],F(14))
        self.assertEqual(c.g.dag_value(reduced,J,E,R)[2],F(12))
        self.assertEqual(c.incremental_cost(c.from_dag(original),cache),F(2))
        self.assertEqual(c.incremental_cost(c.from_dag(reduced),cache),F(12))
        self.assertEqual(c.g.dag_value(original,J,E,R)[:2],c.g.dag_value(reduced,J,E,R)[:2])

    def test_static_optimum_and_remaining_optimum_disagree(self):
        J,E,R,qa,qb,rb=self.fixture(); K=frozenset(E)
        empty_price,empty_node=c.cached_optimum(J,E,R,'t',K,frozenset())
        price,node=c.cached_optimum(J,E,R,'t',K,frozenset((qb,rb)))
        self.assertEqual((empty_price,price),(F(12),F(1)))
        self.assertEqual(c.incremental_cost(empty_node,frozenset((qb,rb))),F(12))
        self.assertEqual(c.incremental_cost(node,frozenset()),F(13))

    def test_no_refund_and_selective_rule_revision(self):
        J,E,R,qa,qb,rb=self.fixture(); ra=c.Node(R[2],(qa,))
        archive=frozenset((qa,qb,ra,rb))
        revised=tuple(r for r in R if r.name!='qb')
        self.assertEqual(c.active_cache(archive,revised,frozenset(E)),frozenset((qa,ra)))
        # Archive is immutable; invalidation changes reuse eligibility, not paid history.
        self.assertEqual(sum((n.rule.cost for n in archive),F()),F(23))
        with self.assertRaisesRegex(ValueError,'stale'):
            c.cached_optimum(J,E,revised,'t',frozenset(E),archive)
        price,node=c.cached_optimum(J,E,revised,'t',frozenset(E),frozenset((qa,ra)))
        self.assertEqual(price,F(1))

    def test_dependency_closed_cache_required(self):
        J,E,R,qa,qb,rb=self.fixture()
        with self.assertRaisesRegex(ValueError,'dependencies'):
            c.cached_optimum(J,E,R,'t',frozenset(E),frozenset((rb,)))

    def test_admission_and_ordered_guard_survive_macro_expansion(self):
        R=c.g.Rule; a=frozenset(('a',)); b=frozenset(('b',)); empty=frozenset()
        rules=(R('a','q',(),a,F(2)),R('b','q',(),b,F(3)),
               R('ordered','t',('q','q'),empty,F(1),frozenset(((a,b),))))
        na,nb=c.Node(rules[0],()),c.Node(rules[1],())
        price,node=c.cached_optimum(('q','t'),('a','b'),rules,'t',a|b,frozenset((nb,)))
        self.assertEqual(price,F(3));self.assertEqual(node.children,(na,nb))
        self.assertFalse(c.valid_node(c.Node(rules[2],(nb,na)),rules,a|b))
        bad=c.Node(R('forged','q',(),a,F(0)),())
        with self.assertRaisesRegex(ValueError,'stale'):
            c.cached_optimum(('q','t'),('a','b'),rules,'t',a|b,frozenset((bad,)))

    def test_unreachable_and_seeded_cycle_controls(self):
        R=c.g.Rule; empty=frozenset()
        cycle=R('loop','q',('q',),empty,F(0))
        self.assertEqual(c.cached_optimum(('q',),(),(cycle,),'q',empty,empty),(None,None))
        seed=R('seed','q',(),empty,F(2))
        self.assertEqual(c.cached_optimum(('q',),(),(seed,cycle),'q',empty,empty)[0],F(2))
        node=c.Node(seed,())
        self.assertEqual(c.cached_optimum(('q',),(),(seed,cycle),'q',empty,frozenset((node,)))[0],F(0))

    def test_exact_support_is_not_terminal_pareto_pruning(self):
        R=c.g.Rule; empty=frozenset(); a=frozenset(('a',))
        rules=(R('empty','q',(),empty,F(0)),R('a','q',(),a,F(1)))
        self.assertEqual(c.cached_optimum(('q',),('a',),rules,'q',a,empty)[0],F(0))
        self.assertEqual(c.cached_optimum(('q',),('a',),rules,'q',a,empty,exact_support=a)[0],F(1))

    def test_full_small_acyclic_oracle(self):
        # Oracle enumerates actual immutable q, r and t proof objects directly.
        # No exact-state refinement or inherited compile_dag is used by the oracle.
        checked=0
        for costs in product((0,2),repeat=4):
            J,E,R,_,_,_=self.fixture()
            R=tuple(c.g.Rule(r.name,r.head,r.premises,r.support,F(w),r.allowed) for r,w in zip(R,costs))
            qs=tuple(c.Node(r,()) for r in R[:2]); rs=tuple(c.Node(R[2],(q,)) for q in qs)
            ts=tuple(c.Node(R[3],(q,r)) for q,r in product(qs,rs))
            universe=qs+rs+ts
            for bits in product((False,True),repeat=len(universe)):
                cache=frozenset(n for n,b in zip(universe,bits) if b)
                if any(not c.footprint(n)<=cache for n in cache): continue
                expected=min(c.incremental_cost(t,cache) for t in ts)
                got,node=c.cached_optimum(J,E,R,'t',frozenset(E),cache)
                self.assertEqual(got,expected)
                self.assertTrue(c.valid_node(node,R,frozenset(E)))
                self.assertLessEqual(len(c.footprint(node)-cache),len(J)*2**len(E))
                checked+=1
        type(self).oracle_cases=checked

    def test_revalidation_profile_retains_alternative_rules(self):
        J,E,R,qa,qb,rb=self.fixture(); ra=c.Node(R[2],(qa,))
        C0=frozenset((qa,ra));C1=frozenset((qb,rb));K=frozenset(E)
        self.assertEqual(c.cached_optimum(J,E,R,'t',K,C0)[0],F(1))
        self.assertEqual(c.cached_optimum(J,E,R,'t',K,C1)[0],F(1))
        revised=tuple(r for r in R if r.name!='qa')
        self.assertEqual(c.cached_optimum(J,E,revised,'t',K,c.active_cache(C0,revised,K))[0],F(13))
        self.assertEqual(c.cached_optimum(J,E,revised,'t',K,c.active_cache(C1,revised,K))[0],F(1))
        local={r.name:frozenset((f'rule:{r.name}',))|r.support for r in R}
        p=c.dependency_frontier(C0|C1,local)
        self.assertEqual(p.get(('q',K),frozenset()),frozenset((frozenset(('rule:qa','e')),frozenset(('rule:qb','e')))))
        self.assertEqual(p.get(('r',K),frozenset()),frozenset((frozenset(('rule:qa','rule:rq','e')),frozenset(('rule:qb','rule:rq','e')))))

    def test_dependency_antichain_against_all_live_sets(self):
        J,E,R,qa,qb,rb=self.fixture();ra=c.Node(R[2],(qa,))
        loop=c.g.Rule('extra','q',('q',),frozenset(),F(0))
        padded=c.Node(loop,(qa,));cache=frozenset((qa,qb,ra,rb,padded))
        local={r.name:frozenset((f'rule:{r.name}',))|r.support for r in R+(loop,)}
        profile=c.dependency_frontier(cache,local)
        self.assertNotIn(frozenset(('e','rule:qa','rule:extra')),profile[('q',frozenset(E))])
        def direct_deps(n): return local[n.rule.name].union(*(direct_deps(ch) for ch in n.children))
        universe=sorted(set().union(*local.values()))
        cases=0
        for bits in product((False,True),repeat=len(universe)):
            live=frozenset(d for d,b in zip(universe,bits) if b)
            for state,antichain in profile.items():
                expected=any((n.rule.head,c.support(n))==state and direct_deps(n)<=live for n in cache)
                got=any(D<=live for D in antichain)
                self.assertEqual(got,expected);cases+=1
        type(self).dependency_profile_cases=cases

if __name__=='__main__': unittest.main(verbosity=2)
