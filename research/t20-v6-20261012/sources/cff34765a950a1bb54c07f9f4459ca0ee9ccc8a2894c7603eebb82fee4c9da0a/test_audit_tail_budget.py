import unittest
from fractions import Fraction as Q
from research.contracts import normalise,tilt

class AuditTailBudget(unittest.TestCase):
    def test_finite_heavy_tail_source_and_exact_withdrawal(self):
        for N in range(2,15):
            prior=normalise({n:Q(1,(n+1)**2) for n in range(N)})
            L={n:Q((n+1)**2,4**n) for n in range(N)}
            self.assertTrue(all(0<v<=1 for v in L.values()))
            post=tilt(prior,L)
            geometric=normalise({n:Q(1,4**n) for n in range(N)})
            self.assertEqual(post,geometric)
            self.assertEqual(tilt(post,{n:1/L[n] for n in L}),prior)
    def test_exact_envelope_transfer_at_budget_boundary(self):
        mu=normalise({0:1,1:2,2:3,3:1})
        # Psi(n)=log(2)*n, beta=3, gamma=1, q(n)=n+1, eta=2.
        R={n:Q(2**n) for n in mu}; post=tilt(mu,R)
        M=sum(mu[n]*2**(3*n) for n in mu); Z=sum(mu[n]*R[n] for n in mu)
        lhs=sum(post[n]*2**(2*(n+1)) for n in mu)
        rhs=Q(4)*M/Z
        self.assertEqual(lhs,rhs)
    def test_envelope_transfer_with_strict_upper_bound(self):
        mu=normalise({0:1,1:2,2:3,3:1})
        R={n:Q(2**n,n+1) for n in mu};post=tilt(mu,R)
        M=sum(mu[n]*2**(3*n) for n in mu);Z=sum(mu[n]*R[n] for n in mu)
        lhs=sum(post[n]*2**(2*(n+1)) for n in mu)
        self.assertLessEqual(lhs,Q(4)*M/Z)

if __name__=='__main__':unittest.main(verbosity=2)
