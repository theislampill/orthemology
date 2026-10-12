import copy
import unittest

from gap_disclosure import analyze, build_certificate, verify_certificate, canonical_hash


def base(profiles=None):
    return {
        'schema': 'profile-base-v1', 'version': 1,
        'profiles': profiles or {'a': ['1','0'], 'b': ['0','1']},
        'coordinate_kinds': ['DESCRIPTIVE', 'DESCRIPTIVE'],
        'extraction_assumptions': [],
    }


def regime(d, lower='1/4', upper='3/4'):
    return {
        'schema': 'two-criterion-weight-interval-v1', 'id': 'bounded-priority',
        'version': 1, 'base_hash': canonical_hash(d), 'lower': lower, 'upper': upper,
        'orientation': [1,1],
        'admissibility_assumptions': [
            {'id':'positive-importance', 'kind':'NORMATIVE',
             'text':'Both declared criteria receive positive priority; their trade-off remains open.'}
        ],
        'authority_status': 'SUPPLIED_NOT_CERTIFIED',
    }


def preference(left='a',right='b',strict=True):
    return {'op': 'gt' if strict else 'ge', 'left': left, 'right': right}


class GapDisclosureTests(unittest.TestCase):
    def test_crossing_profiles_have_admissible_disagreement(self):
        d=base(); r=analyze(d,regime(d),preference())
        self.assertEqual(r['status'],'DISAGREEMENT')
        self.assertEqual(set(w['value'] for w in r['witnesses']),{False,True})

    def test_dominance_is_positive_invariant_control(self):
        d=base({'a':['2','2'],'b':['1','1']})
        self.assertEqual(analyze(d,regime(d),preference())['status'],'INVARIANT_TRUE')

    def test_uniform_failure_is_invariant_false_not_gap(self):
        d=base({'a':['0','0'],'b':['1','1']})
        self.assertEqual(analyze(d,regime(d),preference())['status'],'INVARIANT_FALSE')

    def test_empty_regime_does_not_certify_both_truths(self):
        d=base()
        self.assertEqual(analyze(d,regime(d,'3/4','1/4'),preference())['status'],
                         'NO_ADMISSIBLE_EXTENSION')

    def test_singleton_tie_does_not_entail_strict_preference(self):
        d=base()
        self.assertEqual(analyze(d,regime(d,'1/2','1/2'),preference())['status'],
                         'INVARIANT_FALSE')

    def test_normative_vocabulary_can_occur_in_an_invariant_tautology(self):
        d=base(); p=preference(); t={'op':'or','args':[p,{'op':'not','arg':p}]}
        self.assertEqual(analyze(d,regime(d),t)['status'],'INVARIANT_TRUE')

    def test_interior_cell_cannot_be_missed_by_endpoint_sampling(self):
        d=base({'a':['1','0'],'low':['49/100','49/100'],'high':['51/100','51/100']})
        t={'op':'and','args':[preference('a','low'),preference('high','a')]}
        r=analyze(d,regime(d),t)
        self.assertEqual(r['status'],'DISAGREEMENT')
        self.assertTrue(any(w['value'] for w in r['witnesses']))
        self.assertGreater(r['checked_cells'],2)

    def test_unchanged_tuple_with_mixed_extraction_is_disclosed(self):
        d=base(); d['coordinate_kinds'][0]='MIXED'
        d['extraction_assumptions']=[{'id':'epistemic-quality','kind':'MIXED',
                                     'text':'A calibration theory interprets the recorded quality value.'}]
        r=analyze(d,regime(d),preference())
        self.assertEqual(r['status'],'DISAGREEMENT')
        self.assertFalse(r['base_declared_purely_descriptive'])
        self.assertNotIn('base_is_purely_descriptive',r)

    def test_regime_identifier_is_resource_bounded(self):
        d=base(); b=regime(d); b['id']='x'*129
        self.assertEqual(analyze(d,b,preference())['status'],'INVALID')

    def test_mixed_coordinate_without_extraction_assumption_is_invalid(self):
        d=base(); d['coordinate_kinds'][0]='MIXED'
        self.assertEqual(analyze(d,regime(d),preference())['status'],'INVALID')

    def test_certificate_rechecks_hashes_and_verdict(self):
        d=base(); b=regime(d); t=preference(); c=build_certificate(d,b,t)
        self.assertTrue(verify_certificate(d,b,t,c)['accepted'])
        forged=copy.deepcopy(c); forged['status']='INVARIANT_TRUE'
        self.assertFalse(verify_certificate(d,b,t,forged)['accepted'])

    def test_source_revision_invalidates_old_certificate(self):
        d=base(); b=regime(d); t=preference(); c=build_certificate(d,b,t)
        self.assertTrue(verify_certificate(d,b,t,c)['accepted'])
        d2=copy.deepcopy(d); d2['version']=2
        self.assertFalse(verify_certificate(d2,b,t,c)['accepted'])

    def test_certificate_does_not_coerce_boolean_and_integer_fields(self):
        d=base(); b=regime(d,'1/2','1/2'); t=preference(); c=build_certificate(d,b,t)
        self.assertEqual(c['checked_cells'],1)
        forged=copy.deepcopy(c); forged['checked_cells']=True
        self.assertFalse(verify_certificate(d,b,t,forged)['accepted'])
        forged=copy.deepcopy(c); forged['witnesses'][0]['value']=0
        self.assertFalse(verify_certificate(d,b,t,forged)['accepted'])

    def test_certificate_malformed_values_fail_closed(self):
        d=base(); b=regime(d); t=preference(); c=build_certificate(d,b,t)
        c['witnesses']=object()
        self.assertFalse(verify_certificate(d,b,t,c)['accepted'])

    def test_authority_promotion_is_rejected(self):
        d=base(); b=regime(d); b['authority_status']='CERTIFIED_NORMATIVELY_TRUE'
        self.assertEqual(analyze(d,b,preference())['status'],'INVALID')

    def test_unknown_target_language_is_rejected(self):
        d=base()
        self.assertEqual(analyze(d,regime(d),{'op':'execute','code':'anything'})['status'],'INVALID')

    def test_positive_unit_transport_preserves_the_preference_class(self):
        d=base({'a':['1','0'],'b':['0','2']}); b=regime(d,'1/4','3/4')
        d2=base({'a':['3','0'],'b':['0','2']})
        # w' proportional to (alpha/3, 1-alpha); interval maps monotonically.
        b2=regime(d2,'1/10','1/2')
        self.assertEqual(analyze(d,b,preference())['status'],'DISAGREEMENT')
        self.assertEqual(analyze(d,b,preference())['status'],analyze(d2,b2,preference())['status'])


if __name__ == '__main__':
    unittest.main()
