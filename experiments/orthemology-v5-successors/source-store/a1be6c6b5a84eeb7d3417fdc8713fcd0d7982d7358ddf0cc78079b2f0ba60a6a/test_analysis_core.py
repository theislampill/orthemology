import unittest, math
import numpy as np
import pandas as pd
import analysis_core as core

class CoreTests(unittest.TestCase):
    def test_batch_per_size_leave_one_out_ranges(self):
        mixed=np.column_stack([np.arange(1,7)/10,np.full(6,.2)])
        r=core.block_contrast(mixed,np.array([0.,.4]),replicates=200,seed=4)
        np.testing.assert_allclose(r['size_specific_leave_one_block_out_ranges'],[[.3,.4],[.2,.2],[0.,.4]],atol=1e-14)
    def test_batch_bootstrap_preserves_cross_size_pairing(self):
        mixed=np.array([[.1,-.1],[-.1,.1],[.2,-.2],[-.2,.2],[.3,-.3],[-.3,.3]])
        r=core.block_contrast(mixed,np.array([0.,0.]),replicates=1000,seed=4)
        self.assertAlmostEqual(r['estimate'],0.)
        np.testing.assert_allclose(r['ci95'],[0.,0.],atol=1e-16)
    def test_batch_constant_contrast(self):
        r=core.block_contrast(np.tile([.1,.2],(6,1)),np.array([.3,.3]),replicates=1000,seed=4)
        self.assertAlmostEqual(r['estimate'],.2)
        np.testing.assert_allclose(r['ci95'],[.2,.2],atol=1e-15)
    def test_recorded_flag_support_boundaries(self):
        r=core.score_flags([True,None],assigned=3)
        self.assertTrue(math.isnan(r['R_reconstructed']))
        self.assertEqual(r['A_E0'],1.)
        self.assertEqual(r['B_E0'],0.)
        self.assertEqual(r['Q_E0'],0.)
        self.assertEqual(r['E'],1)
    def test_recorded_flag_empty_is_failure_not_tie(self):
        r=core.score_flags([None,None],assigned=3)
        self.assertEqual(r['R_reconstructed'],0.)
        self.assertTrue(math.isnan(r['A_E']))
        self.assertEqual(r['A_E0'],0.)
    def test_recorded_flag_majority_three_boundaries(self):
        r=core.score_flags([True,True,False],assigned=7)
        self.assertEqual(r['R_reconstructed'],1.)
        self.assertEqual(r['A_E0'],1.)
        self.assertEqual(r['B_E0'],1.)
        self.assertEqual(r['Q_E0'],0.)
    def test_extract_only_literal_fields(self):
        s="{'willHappen': True, 'globalAccurate': False, 'irrelevant': datetime.datetime(2018,1,1)}"
        self.assertEqual(core.event_bits(s),(True,False))
        with self.assertRaises(ValueError): core.event_bits("{'willHappen': evil(), 'globalAccurate': True}")
        with self.assertRaises(ValueError): core.event_bits("{'willHappen': 1, 'globalAccurate': True}")
    def test_truth_reversal_symmetry(self):
        a=core.score_votes([True,True,False],True,3)
        b=core.score_votes([False,False,True],False,3)
        self.assertEqual(a,b)
        self.assertEqual(a['Q0'],1)
        self.assertEqual(a['A0'],1)
    def test_missing_capacity_changes_support(self):
        r=core.score_votes([True,True,False],True,7)
        self.assertEqual(r['A0'],1)
        self.assertEqual(r['Q0'],0)
        self.assertTrue(r['q_unresolved'])
        self.assertTrue(r['correct_active_fails_quorum'])
    def test_incorrect_majority_is_not_missing(self):
        r=core.score_votes([True,True,False],False,3)
        self.assertEqual(r['Q0'],0)
        self.assertFalse(r['q_unresolved'])
        self.assertEqual(r['A0'],0)
    def test_tie_is_expected_half(self):
        r=core.score_votes([True,False],True,3)
        self.assertEqual(r['A0'],.5)
        self.assertTrue(r['tie'])
        self.assertTrue(math.isnan(r['Q']))
    def test_no_response_unresolved(self):
        r=core.score_votes([],False,3)
        self.assertTrue(math.isnan(r['A']))
        self.assertEqual(r['A0'],0)
        self.assertEqual(r['Q0'],0)
        self.assertTrue(r['empty'])
        self.assertFalse(r['tie'])
    def test_capacity_and_boolean_validation(self):
        with self.assertRaises(ValueError): core.score_votes([True]*4,True,3)
        with self.assertRaises(ValueError): core.score_votes([None],True,3)
        with self.assertRaises(ValueError): core.score_votes([True],True,0)
    def test_logistic_intercept_and_cluster_duplication(self):
        x=np.ones((8,1));y=np.array([1,1,1,0,1,1,1,0.]);g=np.repeat([0,1],4)
        a=core.logistic_cluster(x,y,g);b=core.logistic_cluster(np.repeat(x,2,0),np.repeat(y,2),np.repeat(g,2))
        self.assertAlmostEqual(a['beta'][0],math.log(3),places=7)
        np.testing.assert_allclose(a['beta'],b['beta'],atol=1e-8)
        np.testing.assert_allclose(a['cluster_cov_cr0'],b['cluster_cov_cr0'],atol=1e-10)
    def test_stratified_contrast_and_deterministic_bootstrap(self):
        d=pd.DataFrame({'size':[3,3,3,3,7,7,7,7,15,15,15,15],
          'incentive':[0,0,1,1]*3,'metric':[0,.2,.4,.6,.1,.3,.4,.6,.2,.4,.6,.8]})
        r=core.stratified_contrast(d,'metric',replicates=1000,seed=5)
        self.assertAlmostEqual(r['estimate'],(.4+.3+.4)/3)
        self.assertEqual(r,core.stratified_contrast(d,'metric',replicates=1000,seed=5))
        z=core.stratified_contrast(d.assign(metric=1.),'metric',replicates=200,seed=5)
        self.assertEqual(z['ci95'],[0.,0.])
    def test_pair_correlation_selected_overlap(self):
        a=np.tile([0.,1.],6);b=1-a
        self.assertAlmostEqual(core.pair_correlation(a,b,12),-1)
        self.assertTrue(math.isnan(core.pair_correlation(a,np.ones(12),12)))
        self.assertTrue(math.isnan(core.pair_correlation(a[:11],b[:11],12)))
    def test_fail_closed_duplicate_keys(self):
        d=pd.DataFrame({'game':['a','a'],'player':['p','p'],'round':[0,0]})
        with self.assertRaises(ValueError):core.require_unique(d,['game','player','round'])

if __name__=='__main__':unittest.main()
