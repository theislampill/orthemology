import unittest
from solver import classify

# Kernels are support triples (successor, observation); only exact positive support matters.
class QualitativeTests(unittest.TestCase):
    def test_one_sided_reveal_rejects_false_support_cycle(self):
        rows = {'a': [{(0,'yes'),(0,'wait')},{(1,'wait')}]}
        result = classify(rows, [0,1], {0,1})
        self.assertFalse(result['almost_sure'])
        self.assertFalse(result['sure'])
    def test_two_sided_reveal_is_almost_sure_not_sure(self):
        rows = {'a': [{(0,'zero'),(0,'wait')},{(1,'one'),(1,'wait')}]}
        result = classify(rows, [0,1], {0,1})
        self.assertTrue(result['almost_sure'])
        self.assertFalse(result['sure'])
    def test_perfect_reveal_has_rank_one(self):
        rows = {'a': [{(0,'zero')},{(1,'one')}]}
        result = classify(rows, [0,1], {0,1})
        self.assertEqual(result['sure_rank'],1)
    def test_noisy_verifier_never_certifies(self):
        rows = {'a': [{(0,'zero'),(0,'one')},{(1,'zero'),(1,'one')}]}
        self.assertFalse(classify(rows,[0,1],{0,1})['almost_sure'])
    def test_hidden_branching_is_allowed(self):
        rows = {'a': [{(0,'wait'),(1,'wait'),(0,'zero')},
                       {(1,'zero')},
                       {(2,'wait'),(2,'one')}]}
        result=classify(rows,[0,0,1],{0,2})
        self.assertTrue(result['almost_sure'])
        self.assertFalse(result['sure'])
    def test_permission_is_universal_over_support(self):
        rows = {'a': [{(0,'zero')},{(1,'one')}]}
        self.assertFalse(classify(rows,[0,1],{0,1}, [{'a'},set()])['almost_sure'])
    def test_target_label_survives_destructive_merge(self):
        # Labels are immutable target answers; current physical states can coincide.
        # State 2 and 3 represent the same physical sink with opposite old labels.
        rows = {'erase': [{(2,'same')},{(3,'same')},{(2,'same')},{(3,'same')}]}
        self.assertFalse(classify(rows,[0,1,0,1],{0,1})['almost_sure'])

if __name__ == '__main__': unittest.main()
