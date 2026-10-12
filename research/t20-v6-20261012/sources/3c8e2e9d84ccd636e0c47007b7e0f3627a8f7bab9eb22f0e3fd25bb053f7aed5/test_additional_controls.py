import unittest
from fractions import Fraction as Q
from itertools import product
from research.contracts import tilt, tv, kernel_likelihood, kernel_pushforward

class AdditionalControls(unittest.TestCase):
    def test_zero_likelihood_loses_reversible_prior_information(self):
        p={'a':Q(1,3),'b':Q(2,3)}; q={'a':Q(2,3),'b':Q(1,3)}
        L={'a':1,'b':0}
        self.assertEqual(tilt(p,L),tilt(q,L))
        self.assertNotEqual(p,q)
    def test_unreachable_kernel_output_gets_arbitrary_factor(self):
        K={'a':{0:1,1:0},'b':{0:1,1:0}}
        ell=kernel_likelihood(K,{'a':3,'b':3})
        p={'a':Q(1,3),'b':Q(2,3)}
        self.assertEqual(tilt(kernel_pushforward(p,K),ell),
                         kernel_pushforward(tilt(p,{'a':3,'b':3}),K))
    def test_kernel_operator_criterion_exhaustive_two_by_two(self):
        for u,v in product([Q(0),Q(1,2),Q(1)],repeat=2):
            K={'a':{0:u,1:1-u},'b':{0:v,1:1-v}}
            for la,lb in product([Q(1),Q(2)],repeat=2):
                L={'a':la,'b':lb}
                expected=all(len({L[a] for a in K if K[a][y]>0})<=1 for y in [0,1])
                try:ell=kernel_likelihood(K,L)
                except ValueError:
                    self.assertFalse(expected)
                    continue
                self.assertTrue(expected)
                for j in range(5):
                    p={'a':Q(j,4),'b':1-Q(j,4)}
                    self.assertEqual(kernel_pushforward(tilt(p,L),K),tilt(kernel_pushforward(p,K),ell))
    def test_posterior_equality_does_not_preserve_normaliser(self):
        p={'a':Q(1,3),'b':Q(2,3)}; L={'a':Q(1,4),'b':Q(1,2)}
        Lhat={k:7*v for k,v in L.items()}
        self.assertEqual(tilt(p,L),tilt(p,Lhat))
        self.assertEqual(sum(p[k]*Lhat[k] for k in p),7*sum(p[k]*L[k] for k in p))
    def test_small_coordinate_distance_not_small_total_variation(self):
        e=Q(1,10**12)
        self.assertEqual(tv({Q(0):1},{e:1}),1)
        self.assertEqual(abs(e-Q(0)),e)
    def test_joined_observable_bound_rational_grid(self):
        # x=(0,1), xhat=(e,1+e), f(x)=x on [0,2]; range bound 2, Lipschitz bound 1.
        for i,j,k in product(range(9),range(9),range(5)):
            p={0:Q(i,8),1:1-Q(i,8)}; q={0:Q(j,8),1:1-Q(j,8)}; e=Q(k,20)
            exact=p[1]; approx=q[0]*e+q[1]*(1+e)
            self.assertLessEqual(abs(exact-approx),2*tv(p,q)+e)
    def test_pairwise_source_overlap_is_not_global_adequacy(self):
        sets=[{'a','b'},{'b','c'},{'a','c'}]
        self.assertTrue(all(sets[i]&sets[j] for i in range(3) for j in range(i+1,3)))
        self.assertEqual(set.intersection(*sets),set())

if __name__=='__main__':unittest.main(verbosity=2)
