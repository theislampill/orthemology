import unittest
from copy import deepcopy
from itertools import product, permutations
from reactive_context import Catalogue, Exercise, Original, execute, own_policy, forecast, response_pairs, has_foreign_donor, epistemic_model, TargetCode, SettingCode

def records_correspond(world):
    """Test utility: correspondence of declared records, not proof of causality."""
    actual=world['actual']; events=set(actual['events']); acts=actual['acts']
    tokens={act.token:act.bearer for act in acts}
    if len(tokens)!=len(acts): return False
    if set(actual['proofs'])!=events or set(actual['supports'])!=events: return False
    expected={(token,e) for token in tokens for e in events}
    proof_edges=set()
    for event,proof in actual['proofs'].items():
        inputs=proof['intrinsic_inputs']
        if len(inputs)!=len(set(inputs)) or set(inputs)!=set(tokens): return False
        if proof['created_inputs']: return False
        roots=frozenset(tokens.values())
        if proof['positive_roots']!=roots or actual['supports'][event]!=roots: return False
        proof_edges.update((token,event) for token in inputs)
    return proof_edges==expected==set(world['efficient_edges'])


class ReactiveContextTests(unittest.TestCase):
    def setUp(self):
        self.c = Catalogue(('e0','e1'))

    def test_positive_catalogue_and_idle_are_different_types(self):
        self.assertEqual(self.c.targets, (frozenset(('e0',)),frozenset(('e1',)),frozenset(('e0','e1'))))
        self.assertTrue(execute(self.c, Exercise('A',0,0), None)['events'])
        self.assertEqual(execute(self.c,None,None)['events'],frozenset())

    def test_idempotent_commutative_latin_operation(self):
        self.assertEqual([[self.c.combine(a,b) for b in range(3)] for a in range(3)],
                         [[0,2,1],[2,1,0],[1,0,2]])
        for a in range(3):
            self.assertEqual(self.c.combine(a,a),a)
            self.assertEqual({self.c.combine(a,b) for b in range(3)},set(range(3)))
            self.assertEqual({self.c.combine(b,a) for b in range(3)},set(range(3)))
            for b in range(3): self.assertEqual(self.c.combine(a,b),self.c.combine(b,a))

    def test_every_positive_target_has_an_actual_means_in_each_peer_context(self):
        for q,b in product(range(3),(None,0,1,2)):
            a=self.c.respond(q,b)
            self.assertIn(a,range(3))
            self.assertEqual(self.c.combine(a,b),q)
            self.assertEqual(self.c.combine(b,a),q)

    def test_no_fixed_exercise_controls_any_target_against_all_active_peers(self):
        for q,a in product(range(3),repeat=2):
            self.assertTrue(any(self.c.combine(a,b)!=q for b in range(3)))

    def test_one_actual_joined_interpretation_for_every_target(self):
        originals={g:Original(g) for g in ('A','B')}
        for q in range(3):
            expected=forecast(self.c,q)
            acts={g:own_policy(originals[g],q) for g in originals}
            self.assertEqual([acts[g].setting for g in originals],[q,q])
            actual=execute(self.c,acts['A'],acts['B'])
            self.assertEqual(actual['events'],self.c.targets[q])
            self.assertEqual(actual,expected)
            self.assertEqual(actual['intentions'],{'A':True,'B':True})
            self.assertEqual(actual['own_activity_ends'],{'A':True,'B':True})
            self.assertTrue(all(roots==frozenset(('A','B')) for roots in actual['supports'].values()))
            self.assertTrue(all(not roots for roots in actual['entire'].values()))

    def test_unchanged_actual_exercise_survives_peer_suppression(self):
        for q in range(3):
            a=own_policy(Original('A'),q); b=own_policy(Original('B'),q)
            joint=execute(self.c,a,b); solo=execute(self.c,a,None)
            self.assertIs(solo['acts'][0],a)
            self.assertEqual(solo['events'],joint['events'])
            self.assertTrue(solo['intentions']['A'])
            self.assertTrue(solo['own_activity_ends']['A'])
            self.assertTrue(all(s==frozenset(('A',)) for s in solo['supports'].values()))
            self.assertNotEqual(forecast(self.c,q),solo)

    def test_active_replacement_sensitivity_is_not_idle_removal_necessity(self):
        for a,b in product(range(3),repeat=2):
            q=self.c.combine(a,b)
            self.assertTrue(all(self.c.combine(c,b)!=q for c in range(3) if c!=a))
            self.assertTrue(all(self.c.combine(a,c)!=q for c in range(3) if c!=b))
        for q in range(3):
            for event in self.c.targets[q]:
                self.assertTrue(any(event not in self.c.targets[self.c.combine(c,q)] for c in range(3)))
            self.assertEqual(self.c.combine(q,None),self.c.combine(q,q))

    def test_mutual_response_equations_are_solved_not_assumed(self):
        for qa,qb in product(range(3),repeat=2):
            solutions=response_pairs(self.c,qa,qb)
            expected=tuple((a,b) for a,b in product(range(3),repeat=2) if (a+b)%3==(2*qa)%3 and qa==qb)
            self.assertEqual(solutions,expected)
            self.assertEqual(len(solutions),3 if qa==qb else 0)
            for a,b in solutions:
                run=execute(self.c,Exercise('A',qa,a),Exercise('B',qb,b))
                self.assertTrue(all(run['intentions'].values()))
                if a!=qa:
                    self.assertFalse(execute(self.c,Exercise('A',qa,a),None)['intentions']['A'])
            if qa==qb:
                self.assertEqual(tuple(p for p in solutions if p[0]==p[1]),((qa,qa),))

    def test_adaptation_restores_goal_and_really_changes_own_exercise(self):
        q=0; a=own_policy(Original('A'),q)
        changed_peer=Exercise('B',1,1)
        frozen=execute(self.c,a,changed_peer)
        self.assertFalse(frozen['intentions']['A'])
        adapted=Exercise('A',q,self.c.respond(q,changed_peer.setting))
        self.assertNotEqual(adapted.setting,a.setting)
        self.assertTrue(execute(self.c,adapted,changed_peer)['intentions']['A'])
        self.assertFalse(execute(self.c,adapted,None)['intentions']['A'])

    def test_nonreceipt_has_typed_efficient_edges_and_detects_foreign_donor(self):
        edges=(('A_act','e0'),('B_act','e0'))
        for g in ('A','B'):
            for attribute in ('K','P'):
                self.assertFalse(has_foreign_donor(g+'_'+attribute,g,edges))
        self.assertTrue(has_foreign_donor('A_K','A',edges+(('B_act','A_K'),)))

    def test_contextwise_success_with_active_peer_does_not_become_sole_provenance(self):
        for q,b in product(range(3),repeat=2):
            a=Exercise('A',q,self.c.respond(q,b))
            result=execute(self.c,a,Exercise('B',b,b))
            self.assertTrue(result['intentions']['A'])
            self.assertTrue(all(not s for s in result['entire'].values()))

    def test_minimality_two_labels_fail_three_label_fixture_succeeds(self):
        candidates=[]
        for entries in product(range(2),repeat=4):
            rows=(entries[:2],entries[2:])
            if rows[0][0]!=0 or rows[1][1]!=1: continue
            if any(set(row)!={0,1} for row in rows): continue
            if any({rows[a][b] for a in range(2)}!={0,1} for b in range(2)): continue
            candidates.append(entries)
        self.assertEqual(candidates,[])
        self.assertEqual({self.c.combine(0,b) for b in range(3)},{0,1,2})
        self.assertTrue(all(self.c.combine(q,q)==q for q in range(3)))

    def test_three_alternative_law_is_label_equivariant(self):
        for p in permutations(range(3)):
            for a,b in product(range(3),repeat=2):
                self.assertEqual(p[self.c.combine(a,b)],self.c.combine(p[a],p[b]))

    def test_generic_nonempty_catalogue_family_preserves_conditional_power(self):
        c=Catalogue(('e0','e1','e2'))
        self.assertEqual(len(c.targets),7)
        for q,b in product(range(7),repeat=2):
            self.assertEqual(c.combine(c.respond(q,b),b),q)
            self.assertEqual(c.combine(q,q),q)

    def test_standing_cognition_and_reason_derived_full_factivity_share_one_model(self):
        model=epistemic_model(self.c)
        self.assertIsInstance(model,dict)
        self.assertEqual(len(model['worlds']),3)
        for w in model['worlds']:
            self.assertTrue(records_correspond(w))
            proof_edges={(token,e) for e,proof in w['actual']['proofs'].items() for token in proof['intrinsic_inputs']}
            self.assertEqual(proof_edges,set(w['efficient_edges']))
            self.assertEqual(set(w['efficient_edges']),
                             {(act.token,e) for act in w['actual']['acts'] for e in w['actual']['events']})
            for g in ('A','B'):
                self.assertIs(w['originals'][g],model['originals'][g])
                self.assertEqual(w['forecasts'][g],w['actual'])
                self.assertEqual(w['accessible'],(w['context'],))
                self.assertFalse(has_foreign_donor(w['originals'][g].knowledge_token,g,w['efficient_edges']))
                self.assertFalse(has_foreign_donor(w['originals'][g].power_token,g,w['efficient_edges']))
            for mask in range(8):
                p={i for i in range(3) if mask>>i&1}
                self.assertEqual(all(i in p for i in w['accessible']),w['context'] in p)

    def test_standing_power_repertoire_is_owned_and_actually_executable(self):
        for g in ('A','B'):
            original=Original(g)
            self.assertEqual(getattr(original,'repertoire',None),(0,1,2))
            for q,b in product(range(3),(None,0,1,2)):
                act=original.issue(q,self.c.respond(q,b))
                self.assertEqual(act.bearer,g)
                self.assertEqual(self.c.combine(act.setting,b),q)
            with self.assertRaises(ValueError): original.issue(0,7)

    def test_target_and_setting_are_distinct_types_even_when_codes_match(self):
        act=own_policy(Original('A'),0)
        self.assertIs(type(act.goal),TargetCode)
        self.assertIs(type(act.setting),SettingCode)
        adapted=Original('A').issue(0,self.c.respond(0,1))
        self.assertEqual(adapted.goal,0)
        self.assertEqual(adapted.setting,2)

    def test_full_contextual_control_requires_nonmonotonic_solo_manifestation(self):
        for q,b in product(range(3),repeat=2):
            if self.c.targets[b] <= self.c.targets[q]: continue
            peer=Exercise('B',b,b)
            a=Original('A').issue(q,self.c.respond(q,b))
            solo=execute(self.c,None,peer)
            joint=execute(self.c,a,peer)
            missing=solo['events']-joint['events']
            self.assertTrue(missing)
            self.assertEqual(joint['events'],self.c.targets[q])
            self.assertIs(joint['acts'][1],peer)
            self.assertFalse(joint['intentions']['B'])
            self.assertTrue(all(not proof['created_inputs'] for proof in joint['proofs'].values()))

    def test_classwide_retention_obstruction_without_empty_targets(self):
        targets=self.c.targets
        checked=0
        # Arbitrary fixed-peer rows, not only the quasigroup or union law.
        for solo,target in product(targets,repeat=2):
            for row in product(targets,repeat=2):
                checked+=1
                if all(solo <= out for out in row):
                    if any(out==target for out in row): self.assertLessEqual(solo,target)
                    if not solo <= target: self.assertNotIn(target,row)
        self.assertEqual(checked,81)
        # Inclusion is necessary, not sufficient for an arbitrary law.
        solo=targets[0]; target=targets[2]; row=(solo,solo)
        self.assertLess(solo,target)
        self.assertTrue(all(solo<=out for out in row))
        self.assertNotIn(target,row)

    def test_orphan_proof_input_is_rejected_by_correspondence_check(self):
        w=deepcopy(epistemic_model(self.c)['worlds'][0])
        event=next(iter(w['actual']['events']))
        w['actual']['proofs'][event]['intrinsic_inputs']+=('orphan_act',)
        self.assertFalse(records_correspond(w))

    def test_extra_orphan_graph_cause_is_rejected_by_correspondence_check(self):
        w=deepcopy(epistemic_model(self.c)['worlds'][0])
        event=next(iter(w['actual']['events']))
        w['efficient_edges']+=(('orphan_act',event),)
        self.assertFalse(records_correspond(w))

if __name__=='__main__': unittest.main()
