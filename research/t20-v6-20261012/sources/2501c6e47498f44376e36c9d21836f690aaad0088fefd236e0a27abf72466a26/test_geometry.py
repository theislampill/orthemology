import unittest
from geometry import run
class GeometryChecks(unittest.TestCase):
 def test_pullback(self):
  r=run();self.assertEqual(r['pullback_failures'],0);self.assertGreater(r['coordinate_checks'],0)
 def test_naive_coordinate_change_is_detected(self): self.assertTrue(run()['naive_euclidean_coordinate_failure'])
 def test_metric_and_feasibility(self):
  r=run();self.assertTrue(r['same_J_metric_changes_direction']);self.assertTrue(r['descent_can_leave_K']);self.assertTrue(r['projected_step_preserves_K_and_decreases_J'])
 def test_criticality(self): self.assertEqual(run()['criticality_failures'],0)
 def test_semantic_fibre(self): self.assertTrue(run()['same_smooth_point_different_authority']);self.assertTrue(run()['exact_record_preserved'])
if __name__=='__main__': unittest.main()
