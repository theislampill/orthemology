import unittest
from fractions import Fraction as Q
from itertools import product
from research.contracts import tilt, pushforward

class SeparableRepair(unittest.TestCase):
    def test_exact_commuting_current_weight_repair(self):
        p={0:Q(1,4),1:Q(3,4)}; A={0:3,1:5}; R={0:7,1:2}; q={0:10,1:20}
        replay=pushforward(tilt(tilt(p,R),A),q)
        repaired=pushforward(tilt(tilt(p,A),R),q)
        self.assertEqual(replay,repaired)
        self.assertEqual(replay,{10:Q(7,17),20:Q(10,17)})
    def test_normaliser_composition_not_individual_equality(self):
        p={0:Q(1,4),1:Q(3,4)}; A={0:3,1:5}; R={0:7,1:2}
        Z=lambda law,L:sum(law[i]*L[i] for i in law)
        combined=Z(p,{i:A[i]*R[i] for i in p})
        self.assertEqual(Z(p,R)*Z(tilt(p,R),A),combined)
        self.assertEqual(Z(p,A)*Z(tilt(p,A),R),combined)
        self.assertNotEqual(Z(p,R),Z(tilt(p,A),R))
    def test_commutation_grid(self):
        for i,a,b,r,s in product(range(1,5),[1,2],[1,3],[1,4],[1,5]):
            p={0:Q(i,5),1:1-Q(i,5)}; A={0:a,1:b}; R={0:r,1:s}
            self.assertEqual(tilt(tilt(p,A),R),tilt(tilt(p,R),A))
    def test_interaction_changes_first_position_step(self):
        p={0:Q(1,2),1:Q(1,2)}; revised={0:Q(1,4),1:Q(3,4)}; h=Q(1,4)
        m=p[1]; mr=revised[1]
        old_positions={i:Q(i)-h*m for i in p}
        new_positions={i:Q(i)-h*mr for i in p}
        self.assertEqual(old_positions[0]-new_positions[0],Q(1,16))
        self.assertNotEqual(old_positions,new_positions)

if __name__=='__main__':unittest.main(verbosity=2)
