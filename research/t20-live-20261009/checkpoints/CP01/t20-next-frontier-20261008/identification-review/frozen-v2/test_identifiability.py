import unittest,random,sys
from pathlib import Path
from itertools import product
from identifiability import *
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[3]
CP=ROOT/'recovery-t20/checkpoint/Orthemology_T20_Continuation_Owner_Review_Checkpoint_20261008/tranche20/research-frontier-continuation'
sys.path.insert(0,str(CP/'provision-identity/src'))
import provision_semantics as old
sys.path.insert(0,str(CP/'sovereignty-choice-semantics/reactive-context-extension/src'))
import reactive_context as reactive

class IdentificationTests(unittest.TestCase):
    def test_all_1024_five_type_models_reconstruct(self):
        for counts in product(range(4),repeat=5):
            model={(*kind,1):n for kind,n in zip(TYPES,counts) if n}
            self.assertEqual(recover_model(endpoint_panel(model,1),1),model)

    def test_factor_product_matches_independent_gate_enumeration(self):
        models=[one_effect_fixture(k) for k in ('coalescence','redundant','priority_A')]
        models += [{(A,0,1):1,(B,0,2):1,(AB,0,3):1},
                   {(A,B,3):1,(B,A,2):1,(AB,0,1):1}]
        for model in models:
            m=max(t.bit_length() for p,n,t in model)
            for profile in (0,A,B,AB):
                distribution=exact_distribution(occurrences(model),profile)
                self.assertEqual(sum(distribution.values()),1)
                for query in subsets((1<<m)-1,True):
                    self.assertEqual(query_absence(distribution,query),absence_probability(model,profile,query))

    def test_guarded_fixtures_match_actual_preserved_rules(self):
        for kind in ('coalescence','redundant','priority_A'):
            model=one_effect_fixture(kind)
            for profile in (0,A,B,AB):
                active=''.join(g for bit,g in ((A,'A'),(B,'B')) if profile&bit)
                run=old.run(old.direct_rules(kind),active)
                eligible=[(p,n) for (p,n,t),count in model.items() for _ in range(count) if enabled(p,n,profile)]
                self.assertEqual(bool(run.events),bool(eligible))
                self.assertEqual(sorted(len(p.roots) for p in run.proofs.get('e',())),sorted(p.bit_count() for p,n in eligible))

    def test_current_reactive_contexts_embed_without_new_gate_claim(self):
        catalogue=reactive.Catalogue(('e0','e1'))
        model=reactive.epistemic_model(catalogue)
        for world in model['worlds']:
            actual=world['actual'];acts={act.bearer:act for act in actual['acts']}
            for profile in (0,A,B,AB):
                outcome=reactive.execute(catalogue,acts['A'] if profile&A else None,acts['B'] if profile&B else None)
                self.assertEqual(outcome['events'],actual['events'] if profile else frozenset())
                for event in outcome['events']:
                    self.assertEqual(outcome['supports'][event],frozenset(g for bit,g in ((A,'A'),(B,'B')) if profile&bit))
            self.assertTrue(all(actual['intentions'].values()))
            self.assertTrue(all(actual['own_activity_ends'].values()))
        # Only the pre-intervention typed route law is transported above.

    def test_uniform_route_thinning_does_not_identify_root_support(self):
        joint=occurrences(one_effect_fixture('coalescence'))
        priority=occurrences(one_effect_fixture('priority_A'))
        for profile,z in product((0,A,B,AB),(Q(1,5),Q(1,2),Q(4,5))):
            self.assertEqual(exact_distribution(joint,profile,'route',route_rate=z),exact_distribution(priority,profile,'route',route_rate=z))
        self.assertNotEqual(exact_distribution(joint,AB,'route'),exact_distribution(occurrences(one_effect_fixture('redundant')),AB,'route'))

    def test_shared_gates_with_and_without_guard_reevaluation_are_distinct(self):
        records=[occurrences(one_effect_fixture(k)) for k in ('coalescence','redundant','priority_A')]
        for profile in (0,A,B,AB):
            outputs=[exact_distribution(r,profile,'source_deletion') for r in records]
            self.assertEqual(outputs[0],outputs[1]);self.assertEqual(outputs[1],outputs[2])
        self.assertNotEqual(exact_distribution(records[0],AB,'shared_frozen'),exact_distribution(records[2],AB,'shared_frozen'))

    def test_shared_frozen_gates_hide_duplicates_and_absorbed_routes(self):
        models=[{(A,0,1):1},{(A,0,1):2},{(A,0,1):1,(AB,0,1):1}]
        for rates in ({A:Q(1,2),B:Q(1,3)},{A:Q(2,5),B:Q(3,7)}):
            shared=[exact_distribution(occurrences(m),AB,'shared_frozen',rates) for m in models]
            self.assertEqual(shared[0],shared[1]);self.assertEqual(shared[1],shared[2])
        self.assertEqual(len({absence_probability(m,AB,1) for m in models}),3)

    def test_aliases_share_gates_but_distinct_actual_occurrences_do_not(self):
        one=Occurrence('r',A,0,1);clone=Occurrence('r',A,0,1);other=Occurrence('s',A,0,1)
        self.assertEqual(exact_distribution((one,),A),exact_distribution((one,clone),A))
        self.assertNotEqual(exact_distribution((one,),A),exact_distribution((one,other),A))
        with self.assertRaises(ValueError):exact_distribution((one,Occurrence('r',B,0,1)),AB)

    def test_each_nonempty_issued_profile_is_required(self):
        # An exclusive guard or joint support hides a route at every other profile,
        # even if every incidence rate there can be varied freely.
        additions={A:(A,B,1),B:(B,A,1),AB:(AB,0,1)}
        base={(A,0,1):1,(B,0,1):1}
        for omitted,key in additions.items():
            changed=dict(base);changed[key]=changed.get(key,0)+1
            for profile in (A,B,AB):
                for x,y in product((Q(0),Q(1,4),Q(1,2),Q(1)),repeat=2):
                    if profile!=omitted:self.assertEqual(absence_probability(base,profile,1,{A:x,B:y}),absence_probability(changed,profile,1,{A:x,B:y}))
            self.assertNotEqual(absence_probability(base,omitted,1),absence_probability(changed,omitted,1))

    def test_joint_effect_absence_recovers_bundling_lost_in_marginals(self):
        bundled={(AB,0,3):1};separate={(AB,0,1):1,(AB,0,2):1}
        for query in (1,2):self.assertEqual(absence_probability(bundled,AB,query),absence_probability(separate,AB,query))
        self.assertEqual(absence_probability(bundled,AB,3),Q(5,6))
        self.assertEqual(absence_probability(separate,AB,3),Q(25,36))
        self.assertEqual(recover_model(endpoint_panel(bundled,2),2),bundled)
        self.assertEqual(recover_model(endpoint_panel(separate,2),2),separate)

    def test_general_multi_effect_reconstruction(self):
        rng=random.Random(20261008)
        for effect_count in range(1,5):
            for _ in range(20):
                model={(*kind,t):rng.randrange(3) for kind in TYPES for t in subsets((1<<effect_count)-1,True)}
                model={k:v for k,v in model.items() if v}
                self.assertEqual(recover_model(endpoint_panel(model,effect_count),effect_count),model)

    def test_every_absence_coordinate_has_a_separating_omission_witness(self):
        for effect_count in range(1,5):
            universe=(1<<effect_count)-1
            for omitted in subsets(universe,True):
                left,right=omitted_query_witness(effect_count,omitted)
                for query in subsets(universe,True):
                    lp=absence_probability(left,A,query);rp=absence_probability(right,A,query)
                    self.assertEqual(lp==rp,query!=omitted)
                # Same entire unattenuated output catalogue.
                self.assertEqual(absence_probability(left,A,universe,{A:Q(1),B:Q(1)}),0)
                self.assertEqual(absence_probability(right,A,universe,{A:Q(1),B:Q(1)}),0)

    def test_fixed_rate_sampling_separation_and_bounded_grid(self):
        for k in range(1,11):
            p0=Q(1,2)**k;p1=Q(1,2)**(k+1)
            self.assertEqual(abs(p0-p1),Q(1,2)**(k+1))
        # For at most K active routes all AB probabilities share denominator 6^K.
        for bound in range(6):
            values=[]
            for a,b,c in product(range(bound+1),repeat=3):
                if a+b+c<=bound:
                    value=Q(1,2)**a*Q(2,3)**b*Q(5,6)**c
                    self.assertEqual((value*6**bound).denominator,1);values.append(value)
            self.assertEqual(len(values),len(set(values)))
            ordered=sorted(values)
            if len(ordered)>1:self.assertGreaterEqual(min(y-x for x,y in zip(ordered,ordered[1:])),Q(1,6**bound))

    def test_invalid_exact_panels_rejected(self):
        with self.assertRaises(ValueError):decode_ab(Q(7,11))
        with self.assertRaises(ValueError):decode_ab(Q(0))
        panel=endpoint_panel({(A,0,1):1},1);panel[A,1]=Q(1)
        with self.assertRaises(ValueError):recover_model(panel,1)

    def test_uncalibrated_rates_can_mask_different_actual_multiplicities(self):
        single={(A,0,1):1};double={(A,0,1):2}
        for profile in (0,A,B,AB):
            self.assertEqual(absence_probability(single,profile,1,{A:Q(3,4),B:Q(1,3)}),
                             absence_probability(double,profile,1,{A:Q(1,2),B:Q(1,3)}))

    def test_exact_finite_sample_distance_respects_saturation_bound(self):
        from math import comb
        n,k=20,8
        p,q=Q(1,2)**k,Q(1,2)**(k+1)
        tv=sum(abs(comb(n,j)*p**j*(1-p)**(n-j)-comb(n,j)*q**j*(1-q)**(n-j)) for j in range(n+1))/2
        self.assertLessEqual(tv,n*abs(p-q))
        self.assertLess((1+tv)/2,Q(2,3))

    def test_uniform_route_count_fibre_formula_is_complete(self):
        all_vectors=tuple(product(range(4),repeat=5))
        for na,nb,nab in product(range(4),repeat=3):
            enumerated={v for v in all_vectors if (v[0]+v[3],v[1]+v[4],v[0]+v[1]+v[2])==(na,nb,nab)}
            formula={(a,b,nab-a-b,na-a,nb-b) for a in range(na+1) for b in range(nb+1) if a+b<=nab}
            self.assertEqual(enumerated,formula)

    def test_finite_full_support_samples_cannot_certify_zero_error(self):
        for observations in product((False,True),repeat=4):
            likelihoods=[]
            for k in (1,2):
                absence=Q(1,2)**k
                likelihood=Q(1)
                for observed_effect in observations:likelihood*=1-absence if observed_effect else absence
                likelihoods.append(likelihood)
            self.assertTrue(all(v>0 for v in likelihoods))

    def test_endpoint_law_does_not_identify_physical_gate_architecture(self):
        models=[one_effect_fixture(k) for k in ('coalescence','redundant','priority_A')]
        models.append({(A,0,1):1,(AB,0,3):1,(B,A,2):1})
        for model in models:
            for profile in (0,A,B,AB):
                for rates in (RATES,{A:Q(2,5),B:Q(3,7)}):
                    self.assertEqual(exact_distribution(occurrences(model),profile,'incidence',rates),
                                     exact_distribution(occurrences(model),profile,'support_route',rates))

    def test_distinct_stochastic_extensions_commute_with_unattenuated_slice(self):
        catalogue=reactive.Catalogue(('e0','e1'))
        world=reactive.epistemic_model(catalogue)['worlds'][2]
        self.assertEqual(world['actual']['events'],frozenset(('e0','e1')))
        bundled={(*kind,3):1 for kind in ((AB,0),(A,B),(B,A))}
        separate={(*kind,t):1 for kind in ((AB,0),(A,B),(B,A)) for t in (1,2)}
        for profile in (0,A,B,AB):
            for model in (bundled,separate):
                self.assertEqual(exact_distribution(occurrences(model),profile,rates={A:Q(1),B:Q(1)}),{3 if profile else 0:Q(1)})
                for effect in (1,2):
                    declared_roots=0
                    for (p,n,t),count in model.items():
                        if t&effect and enabled(p,n,profile):declared_roots|=p
                    self.assertEqual(declared_roots,profile)
        self.assertNotEqual(exact_distribution(occurrences(bundled),AB),exact_distribution(occurrences(separate),AB))

if __name__=='__main__':unittest.main(verbosity=2)
