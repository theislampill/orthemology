import unittest
from fractions import Fraction as Q
from itertools import product
from research.contracts import tilt, tv, replicator, audit_tangent, rational_weight_step

class AuditCovariantDiscretisation(unittest.TestCase):
    def test_replicator_vector_field_equivariance(self):
        for a,b in product(range(1,5),repeat=2):
            w={0:Q(a,a+b+2),1:Q(b,a+b+2),2:Q(2,a+b+2)}
            r={0:Q(2),1:Q(1,3),2:Q(7,4)}; c={0:Q(-3),1:Q(1),2:Q(5)}
            self.assertEqual(audit_tangent(w,r,replicator(w,c)),replicator(tilt(w,r),c))
    def test_euler_positive_descent_still_fails_audit_covariance(self):
        w={0:Q(1,2),1:Q(1,2)}; r={0:1,1:2}; c={0:0,1:1}; h=Q(1,2)
        def euler(p):
            f=replicator(p,c)
            return {i:p[i]+h*f[i] for i in p}
        left=tilt(euler(w),r); right=euler(tilt(w,r))
        self.assertEqual(left,{0:Q(3,13),1:Q(10,13)})
        self.assertEqual(right,{0:Q(2,9),1:Q(7,9)})
        self.assertEqual(tv(left,right),Q(1,117))
        self.assertTrue(all(x>0 for x in left.values()))
        self.assertTrue(all(x>0 for x in right.values()))
        # Energy is w_0: it falls under either Euler step.
        self.assertLess(euler(w)[0],w[0])
        self.assertLess(euler(tilt(w,r))[0],tilt(w,r)[0])
    def test_rational_step_restores_exact_covariance(self):
        w={0:Q(1,2),1:Q(1,2)}; r={0:1,1:2}; V={0:1,1:0}; h=Q(1,2)
        left=tilt(rational_weight_step(w,V,h),r)
        right=rational_weight_step(tilt(w,r),V,h)
        self.assertEqual(left,right)
        self.assertEqual(left,{0:Q(1,4),1:Q(3,4)})
    def test_rational_step_positive_descent_and_covariance_grid(self):
        count=0
        for a,b,c,h in product(range(1,4),range(1,4),range(1,4),[Q(0),Q(1,10),Q(1),Q(100)]):
            w={0:Q(a,a+b+c),1:Q(b,a+b+c),2:Q(c,a+b+c)}
            V={0:Q(-2),1:Q(3),2:Q(1)}; r={0:Q(2),1:Q(1,3),2:Q(5)}
            out=rational_weight_step(w,V,h)
            self.assertEqual(sum(out.values()),1)
            self.assertTrue(all(v>0 for v in out.values()))
            self.assertLessEqual(sum(out[i]*V[i] for i in out),sum(w[i]*V[i] for i in w))
            self.assertEqual(tilt(out,r),rational_weight_step(tilt(w,r),V,h))
            count+=1
        self.assertEqual(count,108)
    def test_common_potential_shift_does_not_change_weight_step(self):
        w={0:Q(1,3),1:Q(2,3)}; V={0:-3,1:2}; shifted={i:v+101 for i,v in V.items()}
        self.assertEqual(rational_weight_step(w,V,Q(7,2)),rational_weight_step(w,shifted,Q(7,2)))
    def test_first_order_consistency_control(self):
        w={0:Q(1,3),1:Q(2,3)}; V={0:0,1:3}
        f=replicator(w,{i:-v for i,v in V.items()})
        for h in [Q(1,10),Q(1,100),Q(1,1000)]:
            out=rational_weight_step(w,V,h)
            err=max(abs((out[i]-w[i])/h-f[i]) for i in w)
            self.assertLessEqual(err,9*h)
    def test_joint_separable_repair_multiple_steps(self):
        initial={0:Q(1,4),1:Q(3,4)}; x0={0:Q(1),1:Q(3)}; r={0:2,1:Q(1,3)}
        def advance(w,x):
            old_energy=sum(w[i]*x[i]*x[i] for i in w)
            x={i:v/2 for i,v in x.items()}  # each V_i(x_i)=x_i² decreases independently of weights
            V={i:v*v for i,v in x.items()}
            w=rational_weight_step(w,V,Q(1,3))
            self.assertLessEqual(sum(w[i]*V[i] for i in w),old_energy)
            return w,x
        w,x=initial.copy(),x0.copy(); wr,xr=tilt(initial,r),x0.copy()
        for _ in range(5):w,x=advance(w,x);wr,xr=advance(wr,xr)
        self.assertEqual(x,xr)
        self.assertEqual(tilt(w,r),wr)
    def test_invalid_weight_step_is_rejected(self):
        with self.assertRaises(ValueError):rational_weight_step({0:1},{0:2},-1)
        with self.assertRaises(ValueError):rational_weight_step({0:0,1:1},{0:1,1:2},1)

if __name__=='__main__':unittest.main(verbosity=2)
