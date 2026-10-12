"""Finite controls for independently specified, necessarily concordant outputs."""
import unittest
from itertools import product
import diagnostics as d

class CompatibilityTests(unittest.TestCase):
    def test_full_cartesian_connected(self):
        self.assertTrue(hasattr(d,'compatibility_components'))
        components=d.compatibility_components(2,2,[(0,0),(0,1),(1,0),(1,1)])
        self.assertEqual(len(components),1)
    def test_diagonal_two_components(self):
        self.assertTrue(hasattr(d,'compatibility_components'))
        self.assertEqual(len(d.compatibility_components(2,2,[(0,0),(1,1)])),2)
    def test_three_edges_already_suffice(self):
        self.assertTrue(hasattr(d,'compatibility_components'))
        self.assertEqual(len(d.compatibility_components(2,2,[(0,0),(0,1),(1,1)])),1)
    def test_all_sixteen_relations_against_enumeration(self):
        self.assertTrue(hasattr(d,'compatibility_components'))
        for mask in range(16):
            edges=[(a,b) for a,b in product(range(2),repeat=2) if mask&(1<<(2*a+b))]
            c=d.compatibility_components(2,2,edges)
            count=sum(all(f[a]==g[b] for a,b in edges)
                      for f in product(range(2),repeat=2) for g in product(range(2),repeat=2))
            self.assertEqual(count,2**len(c))
    def test_three_labels_all_relations(self):
        self.assertTrue(hasattr(d,'compatibility_components'))
        for mask in range(16):
            edges=[(a,b) for a,b in product(range(2),repeat=2) if mask&(1<<(2*a+b))]
            c=d.compatibility_components(2,2,edges)
            count=sum(all(f[a]==g[b] for a,b in edges)
                      for f in product(range(3),repeat=2) for g in product(range(3),repeat=2))
            self.assertEqual(count,3**len(c))
    def test_isolates_not_silently_dropped(self):
        self.assertTrue(hasattr(d,'compatibility_components'))
        self.assertEqual(len(d.compatibility_components(2,2,[(0,0)])),3)
    def test_invalid_endpoint(self):
        self.assertTrue(hasattr(d,'compatibility_components'))
        with self.assertRaises(ValueError): d.compatibility_components(2,2,[(2,0)])
    def test_empty_factor(self):
        self.assertTrue(hasattr(d,'compatibility_components'))
        with self.assertRaises(ValueError): d.compatibility_components(0,2,[])

if __name__=='__main__': unittest.main()
