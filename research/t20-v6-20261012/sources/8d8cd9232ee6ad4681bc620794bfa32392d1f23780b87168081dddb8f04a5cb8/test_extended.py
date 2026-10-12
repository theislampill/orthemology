import unittest
import extended_histories as e

class ExtendedHistoryControls(unittest.TestCase):
    def test_complete_old_menu_misses_proposal_and_cross_record_order(self):
        cases=e.institution_history_cases()
        base=cases['base']
        for key in ['missing_proposal','publication_before_votes']:
            w=cases[key]
            self.assertEqual(base['old_observations'],w['old_observations'])
            self.assertEqual(base['holder'],'N')
            self.assertEqual(w['holder'],'P')
            self.assertNotEqual(base['ordered_minutes'],w['ordered_minutes'])

    def test_ordered_minutes_reconstruct_the_observed_finite_history(self):
        answer=e.enumerate_event_orders()
        self.assertEqual(answer['permutations_checked'],120)
        self.assertTrue(answer['old_menu_collision'])
        self.assertTrue(answer['ordered_minutes_sufficient'])

    def test_lawful_remit_change_does_not_enlarge_fixed_source_adoption(self):
        a=e.adoption_after_amendment('fixed')
        b=e.adoption_after_amendment('dynamic')
        self.assertEqual(a['holder'],'N')
        self.assertEqual(b['holder'],'N')
        self.assertEqual(a['new_domain'],'safety')
        self.assertEqual(a['received_rule'],b['received_rule'])
        self.assertFalse(a['source_owned'])
        self.assertTrue(b['source_owned'])
        self.assertNotEqual(a['independent_source_statement'],b['independent_source_statement'])

    def test_dynamic_adoption_does_not_guarantee_report_truth(self):
        w=e.adoption_after_amendment('dynamic',hazard=True)
        self.assertTrue(w['source_owned'])
        self.assertFalse(w['report_true'])

if __name__=='__main__':unittest.main(verbosity=2)
