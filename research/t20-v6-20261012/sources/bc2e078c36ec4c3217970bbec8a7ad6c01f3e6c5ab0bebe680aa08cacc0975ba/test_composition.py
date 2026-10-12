from fractions import Fraction as Q
from itertools import product,permutations
from pathlib import Path
import hashlib,json,sys,unittest
from composition import *

class CompositionTests(unittest.TestCase):
    def test_inherited_law_is_same_binary_table(self):
        self.assertEqual([[C.combine(a,b) for b in range(3)] for a in range(3)],[[0,2,1],[2,1,0],[1,0,2]])
    def test_inherited_law_is_nonassociative(self):
        self.assertEqual(C.combine(C.combine(0,0),1),2)
        self.assertEqual(C.combine(0,C.combine(0,1)),1)
    def test_original_bilateral_reactivity_and_idempotence(self):
        for a in range(3):
            self.assertEqual(C.combine(a,a),a)
            self.assertEqual({C.combine(a,b) for b in range(3)},set(range(3)))
            self.assertEqual({C.combine(b,a) for b in range(3)},set(range(3)))
    def test_tree_positive_homomorphism_and_failed_flattening(self):
        # Three ACT TOKENS but only TWO bearers; no third original is assumed.
        a,b,c=Leaf('alpha1','A',0),Leaf('beta','B',0),Leaf('alpha2','A',1)
        left,right=Branch(Branch(a,b),c),Branch(a,Branch(b,c))
        self.assertEqual(flatten(left),flatten(right))
        self.assertEqual((evaluate(left),evaluate(right)),(2,1))
        for x,y in product([a,b,c,left,right],repeat=2):
            self.assertEqual(evaluate(Branch(x,y)),C.combine(evaluate(x),evaluate(y)))
    def test_unique_act_union_assoc_comm_idem(self):
        a={'alpha':Act('A',0,0)};b={'beta':Act('B',0,0)};c={'alpha2':Act('A',1,0)}
        self.assertEqual(merge(a,a),a)
        self.assertEqual(merge(a,b),merge(b,a))
        self.assertEqual(merge(merge(a,b),c),merge(a,merge(b,c)))
        self.assertEqual(len(merge(a,a)),1)
        self.assertEqual(len(merge(a,b)),2)
    def test_conflicting_alias_rejected(self):
        with self.assertRaises(ValueError):merge({'alpha':Act('A',0,0)},{'alpha':Act('A',1,0)})
    def test_mean_is_not_future_congruent(self):
        x={'alpha':Act('A',0,0)};y=merge(x,{'beta':Act('B',0,0)})
        c={'alpha2':Act('A',1,1)}
        self.assertEqual(visible(x),visible(y))
        self.assertEqual((visible(merge(x,c)),visible(merge(y,c))),(Q(1,2),Q(1,3)))
    def test_count_changes_needed_reactive_means(self):
        x={'alpha':Act('A',0,0)};y=merge(x,{'beta':Act('B',0,0)})
        a,b=issue_response(x,'A','alpha2',1),issue_response(y,'A','alpha2',1)
        self.assertEqual((a['alpha2'].setting,b['alpha2'].setting),(Q(2),Q(3)))
        self.assertEqual(visible(merge(x,a)),1);self.assertEqual(visible(merge(y,b)),1)
    def test_sum_count_hom_only_disjoint_not_alias_merge(self):
        a={'alpha':Act('A',2,2)};b={'beta':Act('B',4,4)}
        self.assertEqual(summary(merge(a,b)),merge_disjoint_summaries(summary(a),summary(b)))
        self.assertNotEqual(summary(merge(a,a)),merge_disjoint_summaries(summary(a),summary(a)))
    def test_rational_any_fixed_peer_response(self):
        # Finite exact checks instantiate the general response identity in RESULT.
        for values in [(),(0,),(1,),(Q(1,2),Q(-2,3)),(0,0,1)]:
            peer={f'beta{i}':Act('B',v,0) for i,v in enumerate(values)}
            for target in [Q(-7,3),Q(0),Q(2,5),Q(9)]:
                result=merge(peer,issue_response(peer,'A','fresh-alpha',target))
                self.assertEqual(visible(result),target)
                self.assertTrue(own_end(result,'A',target))
                self.assertTrue(peer.items()<=result.items())
    def test_rational_diagonal_suppression_and_provenance(self):
        for q in [Q(-1),Q(0),Q(1,3),Q(4)]:
            a={'alpha':Act('A',q,q)};b={'beta':Act('B',q,q)};joint=merge(a,b)
            self.assertEqual(created_output(joint),created_output(a))
            self.assertTrue(own_end(joint,'A',q));self.assertTrue(own_end(joint,'B',q))
            self.assertTrue(own_end(a,'A',q))
            self.assertEqual(support(joint),frozenset({'A','B'}))
            self.assertEqual(support(a),frozenset({'A'}))
            self.assertNotEqual(joint,a)
    def test_fullstate_translation_is_not_onto(self):
        peer={'beta':Act('B',0,0)};target={'alpha':Act('A',1,1)}
        self.assertNotIn('beta',target)
        for s in [{},{'alpha':Act('A',1,1)},peer]:self.assertIn('beta',merge(s,peer))
    def test_summary_loses_selective_suppression(self):
        a={'alpha':Act('A',0,0),'beta':Act('B',2,0)}
        b={'alpha':Act('A',1,0),'beta':Act('B',1,0)}
        self.assertEqual(summary(a),summary(b));self.assertEqual(support(a),support(b))
        self.assertEqual(visible(a),visible(b))
        self.assertEqual((visible(suppress(a,'alpha')),visible(suppress(b,'alpha'))),(Q(2),Q(1)))
    def test_ternary_Z3_sum_count_cannot_recover_consensus(self):
        summaries={(sum([q]*3)%3,3) for q in range(3)}
        self.assertEqual(len(summaries),1)
        for q in range(3):
            self.assertEqual(mod3_bag_mean([q]),q)
            self.assertEqual(mod3_bag_mean([q,q]),q)
            with self.assertRaises(ValueError):mod3_bag_mean([q,q,q])
    def test_rational_midpoint_not_original_label_map(self):
        # Even the natural integer inclusion disagrees on off-diagonal means.
        self.assertEqual(C.combine(0,1),2)
        self.assertEqual((Q(0)+Q(1))/2,Q(1,2))
    def test_summary_does_not_preserve_fresh_action_menu(self):
        x={'alpha':Act('A',0,0)};y={'alpha2':Act('A',0,0)}
        self.assertEqual(summary(x),summary(y));self.assertEqual(support(x),support(y))
        with self.assertRaises(ValueError):issue_response(x,'A','alpha',1)
        response=issue_response(y,'A','alpha',1)
        self.assertEqual(visible(merge(y,response)),1)
    def test_weighted_merge_commutes_on_disjoint_states(self):
        for u,v,w in product([Q(-1),Q(0),Q(1,2)],repeat=3):
            a={'alpha':Act('A',u,0)}
            b={'beta':Act('B',v,0),'beta2':Act('B',w,0)}
            self.assertEqual(visible(merge(a,b)),(visible(a)*len(a)+visible(b)*len(b))/(len(a)+len(b)))
    def test_midpoint_embedding_equations_force_collapse(self):
        # Exact row reduction of all three off-diagonal midpoint equations.
        matrix=[[Q(-1),Q(-1),Q(2)],[Q(-1),Q(2),Q(-1)],[Q(2),Q(-1),Q(-1)]]
        row=0
        for col in range(3):
            piv=next((r for r in range(row,3) if matrix[r][col]),None)
            if piv is None:continue
            matrix[row],matrix[piv]=matrix[piv],matrix[row]
            a=matrix[row][col];matrix[row]=[x/a for x in matrix[row]]
            for r in range(3):
                if r!=row:
                    a=matrix[r][col];matrix[r]=[x-a*y for x,y in zip(matrix[r],matrix[row])]
            row+=1
        self.assertEqual(matrix,[[Q(1),Q(0),Q(-1)],[Q(0),Q(1),Q(-1)],[Q(0),Q(0),Q(0)]])
    def test_arbitrary_summary_update_fails_with_alias_overlap(self):
        x={'alpha':Act('A',2,0)};y={'beta':Act('A',2,0)}
        z={'alpha':Act('A',2,0),'gamma':Act('B',4,0)}
        self.assertEqual(summary(x),summary(y));self.assertEqual(support(x),support(y))
        self.assertEqual((visible(merge(x,z)),visible(merge(y,z))),(Q(3),Q(8,3)))
        self.assertNotEqual(summary(merge(x,z)),summary(merge(y,z)))
    def test_balanced_Z3_bag_has_no_equivariant_selector(self):
        bag=[0,1,2]
        for p in permutations(range(3)):
            self.assertEqual(sorted(p[x] for x in bag),bag)
        for q in range(3):
            self.assertTrue(any(p[q]!=q for p in permutations(range(3))))
    def test_own_end_respects_stored_intention(self):
        state={'alpha':Act('A',1,0)}
        self.assertFalse(own_end(state,'A',1))
        self.assertFalse(own_end(state,'A',0))
    def test_semantic_extension_preserves_relevant_weaker_symmetries(self):
        event_swap=(1,0,2)  # e0<->e1 fixes the two-event created target.
        for n in range(1,5):
            for values in product(range(3),repeat=n):
                self.assertEqual(semantic_Z3_extension(tuple(event_swap[x] for x in values)),event_swap[semantic_Z3_extension(values)])
                self.assertEqual(semantic_Z3_extension(values),semantic_Z3_extension(tuple(reversed(values))))
            for q in range(3):self.assertEqual(semantic_Z3_extension([q]*n),q)
        for a,b in product(range(3),repeat=2):self.assertEqual(semantic_Z3_extension([a,b]),C.combine(a,b))
        self.assertEqual(semantic_Z3_extension([0,1,2]),2)
    def test_semantic_extension_loses_full_ternary_reactivity(self):
        self.assertEqual({semantic_Z3_extension([0,0,a]) for a in range(3)},{0,2})
        self.assertNotIn(1,{semantic_Z3_extension([0,0,a]) for a in range(3)})
    def test_full_symmetric_ternary_reactivity_census(self):
        self.assertEqual(ternary_symmetric_reactive_census(),{'unordered_keys':10,'fixed_unanimity_keys':3,'free_keys':7,'tested':2187,'survivors':0})
    def test_owner_group_positive_ternary_control(self):
        def make(x,y,z):return {'alpha1':Act('A',x,0),'alpha2':Act('A',y,0),'beta':Act('B',z,0)}
        def f(x,y,z):return owner_group_Z3_mean(make(x,y,z))
        for a,b in product(range(3),repeat=2):
            self.assertEqual(owner_group_Z3_mean({'alpha':Act('A',a,0),'beta':Act('B',b,0)}),C.combine(a,b))
        for x,y,z in product(range(3),repeat=3):
            self.assertEqual(f(x,y,z),(x+y+2*z)%3)
            self.assertEqual(f(x,y,z),f(y,x,z))
            renamed={k:Act('B' if a.bearer=='A' else 'A',a.setting,a.goal) for k,a in make(x,y,z).items()}
            self.assertEqual(owner_group_Z3_mean(renamed),f(x,y,z))
        for q in range(3):self.assertEqual(f(q,q,q),q)
        for a,b in product(range(3),repeat=2):
            self.assertEqual({f(x,a,b) for x in range(3)},set(range(3)))
            self.assertEqual({f(a,x,b) for x in range(3)},set(range(3)))
            self.assertEqual({f(a,b,x) for x in range(3)},set(range(3)))
    def test_owner_group_scope_is_not_anonymous_or_allarity(self):
        x={'alpha1':Act('A',0,0),'alpha2':Act('A',0,0),'beta':Act('B',1,0)}
        y={'alpha1':Act('A',1,0),'alpha2':Act('A',0,0),'beta':Act('B',0,0)}
        self.assertEqual(sorted(a.setting for a in x.values()),sorted(a.setting for a in y.values()))
        self.assertEqual((owner_group_Z3_mean(x),owner_group_Z3_mean(y)),(2,1))
        with self.assertRaises(ValueError):owner_group_Z3_mean({f'alpha{i}':Act('A',0,0) for i in range(3)})
    def test_all_27_triples_record_exact_failure(self):
        failures=[(a,b,c) for a,b,c in product(range(3),repeat=3)
                  if C.combine(C.combine(a,b),c)!=C.combine(a,C.combine(b,c))]
        self.assertEqual(len(failures),18)

if __name__=='__main__':unittest.main(verbosity=2)
