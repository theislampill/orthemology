"""Exact regression controls for the T20 cross-front synthesis.

These test our new finite reference implementation, not the original Lean corpus.
"""
from fractions import Fraction as F
from itertools import product
import unittest
from contracts import (Contract, coarsest_refinement, valid_partition,
                       quotient, sidecar, finite_values, as_reaches,
                       moment_witness, audit_distribution, posterior,
                       pair_marginals, inquiry_values, closure_basis,
                       row_reduce, multiply_row, total_variation,
                       conditioned, geometric_cometric)


def simple():
    return Contract(
        ('x','y','good','bad'), ('withdraw','wait'), ('seen',),
        {'x':'claim accepted','y':'claim accepted','good':'accepted','bad':'withdrawn'},
        {'x':('withdraw','wait'),'y':('withdraw','wait'),
         'good':('wait',),'bad':('wait',)},
        {('x','withdraw'):F(1),('y','withdraw'):F(1),
         ('x','wait'):F(0),('y','wait'):F(0),
         ('good','wait'):F(0),('bad','wait'):F(0)},
        {('x','withdraw'):(('seen','bad',F(1)),),
         ('y','withdraw'):(('seen','good',F(1)),),
         ('x','wait'):(('seen','x',F(1)),),
         ('y','wait'):(('seen','y',F(1)),),
         ('good','wait'):(('seen','good',F(1)),),
         ('bad','wait'):(('seen','bad',F(1)),)})


def partitions(xs):
    if not xs:
        yield []
        return
    first,*rest=xs
    for p in partitions(rest):
        yield [(first,)]+p
        for i in range(len(p)):
            yield p[:i]+[(first,)+p[i]]+p[i+1:]


class ContractTests(unittest.TestCase):
    def test_bad_mass_rejected(self):
        c=simple(); k=dict(c.kernels)
        k[('x','withdraw')]=( ('seen','bad',F(1,2)), )
        with self.assertRaises(ValueError):
            Contract(c.states,c.actions,c.outcomes,c.labels,c.enabled,c.costs,k)

    def test_negative_probability_rejected(self):
        c=simple(); k=dict(c.kernels)
        k[('x','withdraw')]=( ('seen','bad',F(-1)),('seen','good',F(2)) )
        with self.assertRaises(ValueError):
            Contract(c.states,c.actions,c.outcomes,c.labels,c.enabled,c.costs,k)

    def test_unknown_successor_rejected(self):
        c=simple(); k=dict(c.kernels)
        k[('x','withdraw')]=( ('seen','missing',F(1)), )
        with self.assertRaises(ValueError):
            Contract(c.states,c.actions,c.outcomes,c.labels,c.enabled,c.costs,k)

    def test_hidden_source_matters_on_withdrawal(self):
        c=simple(); r={'x':0,'y':0,'good':1,'bad':2}
        self.assertFalse(valid_partition(c,[('x','y'),('good',),('bad',)],r))
        blocks,trace=coarsest_refinement(c,r)
        self.assertEqual(len(blocks),4)
        self.assertTrue(valid_partition(c,blocks,r))
        k,alphabet,bits=sidecar(c,r,blocks)
        self.assertEqual((alphabet,bits),(2,1))
        self.assertNotEqual(k['x'],k['y'])

    def test_partition_is_coarsest_by_exhaustion(self):
        c=simple(); r={s:0 for s in c.states}
        b,_=coarsest_refinement(c,r)
        expected={s:i for i,block in enumerate(b) for s in block}
        count=0
        for p in partitions(list(c.states)):
            if valid_partition(c,p,r):
                count+=1
                for block in p:
                    self.assertEqual(len({expected[s] for s in block}),1)
        self.assertGreater(count,0)

    def test_costs_cannot_disappear(self):
        c=Contract(('x','y'),('a',),('o',),{'x':'same','y':'same'},
                   {'x':('a',),'y':('a',)},
                   {('x','a'):F(3),('y','a'):F(4)},
                   {('x','a'):(('o','x',F(1)),),('y','a'):(('o','y',F(1)),)})
        self.assertFalse(valid_partition(c,[('x','y')]))
        b,_=coarsest_refinement(c,{'x':0,'y':0})
        self.assertEqual(len(b),2)

    def test_outcome_probabilities_cannot_disappear(self):
        c=Contract(('x','y'),('a',),('yes','no'),{'x':'same','y':'same'},
                   {'x':('a',),'y':('a',)},
                   {('x','a'):F(0),('y','a'):F(0)},
                   {('x','a'):(('yes','x',F(1,3)),('no','x',F(2,3))),
                    ('y','a'):(('yes','y',F(2,3)),('no','y',F(1,3)))})
        self.assertFalse(valid_partition(c,[('x','y')]))

    def test_enabled_actions_cannot_disappear(self):
        c=Contract(('x','y'),('a','b'),('o',),{'x':'same','y':'same'},
                   {'x':('a',),'y':('b',)},
                   {('x','a'):F(0),('y','b'):F(0)},
                   {('x','a'):(('o','x',F(1)),),('y','b'):(('o','y',F(1)),)})
        self.assertFalse(valid_partition(c,[('x','y')]))

    def test_safe_merge_and_quotient_values(self):
        c=Contract(('x','y','done'),('a',),('stay','finish'),
            {'x':'working','y':'working','done':'success'},
            {s:('a',) for s in ('x','y','done')},
            {('x','a'):F(1),('y','a'):F(1),('done','a'):F(0)},
            {('x','a'):(('stay','x',F(1,2)),('finish','done',F(1,2))),
             ('y','a'):(('stay','y',F(1,2)),('finish','done',F(1,2))),
             ('done','a'):(('finish','done',F(1)),)})
        r={'x':0,'y':0,'done':1}; b,_=coarsest_refinement(c,r)
        self.assertEqual(len(b),2)
        q,m=quotient(c,b)
        for h in range(7):
            v=finite_values(c,h,{'x':F(5),'y':F(5),'done':F(0)})
            w=finite_values(q,h,{m['x']:F(5),m['done']:F(0)})
            self.assertEqual(v['x'],w[m['x']])
            self.assertEqual(v['y'],w[m['y']])
        self.assertTrue(as_reaches(c,'x',{'done'},{s:'a' for s in c.states}))
        self.assertTrue(as_reaches(q,m['x'],{m['done']},{s:'a' for s in q.states}))

    def test_almost_sure_boundary_is_discontinuous(self):
        def chain(e):
            return Contract(('x','done'),('a',),('wait','done'),
                {'x':'unresolved','done':'resolved'},
                {'x':('a',),'done':('a',)},
                {('x','a'):F(0),('done','a'):F(0)},
                {('x','a'):(('wait','x',1-e),('done','done',e)),
                 ('done','a'):(('done','done',F(1)),)})
        for n in (2,10,1000,10**9):
            self.assertTrue(as_reaches(chain(F(1,n)),'x',{'done'}, {'x':'a','done':'a'}))
        self.assertFalse(as_reaches(chain(F(0)),'x',{'done'},{'x':'a','done':'a'}))

    def test_contract_cannot_be_mutated_after_validation(self):
        c=simple()
        with self.assertRaises(TypeError):
            c.costs['x','withdraw']=F(99)
        with self.assertRaises(TypeError):
            c.labels['x']='pass'

    def test_float_probability_is_not_accepted_as_exact(self):
        c=simple();k=dict(c.kernels)
        k['x','withdraw']=(('seen','bad',1.0),)
        with self.assertRaises(ValueError):
            Contract(c.states,c.actions,c.outcomes,c.labels,c.enabled,c.costs,k)

    def test_execution_status_is_not_conflated_with_verdict(self):
        c=Contract(('x','y'),('a',),('o',),
            {'x':('not-run','undetermined'),'y':('run','fail')},
            {'x':('a',),'y':('a',)},
            {('x','a'):F(0),('y','a'):F(0)},
            {('x','a'):(('o','x',F(1)),),('y','a'):(('o','y',F(1)),)})
        self.assertEqual(len(coarsest_refinement(c,{'x':0,'y':0})[0]),2)

    def test_wrong_partition_cover_rejected(self):
        self.assertFalse(valid_partition(simple(),[('x','y'),('good',)]))
        self.assertFalse(valid_partition(simple(),[('x','y'),('good',),('bad','x')]))

    def test_sidecar_two_bits_for_joint_contract(self):
        starts=('A_low','A_high','B_low','B_high'); states=starts+('good','bad')
        actions=('withdraw','batch','direct','wait')
        enabled={s:('withdraw','batch','direct') for s in starts}
        enabled.update({'good':('wait',),'bad':('wait',)})
        costs={}; kernels={}
        for s in starts:
            for a in enabled[s]:
                costs[s,a]=F(1) if a=='withdraw' else F(3 if s.endswith('low') else 4) if a=='batch' else F(7,2)
                t=('bad' if s.startswith('A') else 'good') if a=='withdraw' else 'good'
                kernels[s,a]=( ('o',t,F(1)), )
        for s in ('good','bad'):
            costs[s,'wait']=F(0); kernels[s,'wait']=( ('o',s,F(1)), )
        c=Contract(states,actions,('o',),{s:('same present claim' if s in starts else s) for s in states},enabled,costs,kernels)
        r={s:('same' if s in starts else s) for s in states}
        b,_=coarsest_refinement(c,r)
        k,a,bits=sidecar(c,r,b)
        self.assertEqual((a,bits),(4,2))
        self.assertEqual(len({k[s] for s in starts}),4)


class CrossFrontControls(unittest.TestCase):
    def test_random_report_survives_as_relational_evidence(self):
        d=audit_distribution(F(4,5))
        self.assertEqual(posterior(d,{'R':0,'A':0}),F(1,5))
        self.assertEqual(posterior(d,{'A':0}),F(1,2))
        self.assertEqual(posterior(d,{'R':0}),F(1,2))
        for tab in pair_marginals(d).values():
            self.assertEqual(set(tab.values()),{F(1,4)})
        self.assertEqual(sum(p*((-1)**(h+r+a)) for (h,r,a),p in d.items()),F(3,5))

    def test_same_posteriors_reverse_inquiry_decision(self):
        good,bad=inquiry_values()
        self.assertEqual(good,F(1,32)); self.assertEqual(bad,F(-1,32))

    def test_rare_event_amplification(self):
        for n in (2,10,100,1000):
            e=F(1,n); p=(1-e,e,F(0)); q=(1-e,F(0),e); l=(F(0),F(1),F(1))
            self.assertEqual(total_variation(p,q),e)
            self.assertEqual(total_variation(conditioned(p,l),conditioned(q,l)),F(1))

    def test_zero_event_is_not_a_posterior(self):
        with self.assertRaises(ValueError):
            conditioned((F(1),F(0)),(F(0),F(1)))

    def test_positive_moments_fail_at_any_monitor_depth(self):
        for d in range(1,13):
            r=moment_witness(d)
            self.assertTrue(all(x>0 for x in r['moments']))
            self.assertEqual(r['square_expectation'],F(-1,2))
            self.assertEqual(r['original_square_expectation'],F(0))
            self.assertEqual(r['moments'][:-1],r['original_moments'][:-1])

    def test_future_linear_observation_needs_hidden_coordinate(self):
        a=((F(1),F(1)),(F(0),F(1)))
        b,trace=closure_basis(((F(1),F(0)),),(a,))
        self.assertEqual(len(b),2)
        self.assertEqual(row_reduce(b),((F(1),F(0)),(F(0),F(1))))

    def test_closed_linear_observation_needs_no_extra_coordinate(self):
        a=((F(2),F(0)),(F(0),F(3)))
        b,_=closure_basis(((F(1),F(0)),),(a,))
        self.assertEqual(len(b),1)

    def test_finite_linear_closure_terminates_and_is_invariant(self):
        c=((F(1),F(0),F(0)),)
        for entries in product((F(0),F(1)),repeat=4):
            a=((entries[0],entries[1],F(0)),(entries[2],entries[3],F(1)),(F(0),F(0),F(1)))
            b,tr=closure_basis(c,(a,))
            self.assertLessEqual(len(b),3)
            for v in b:
                self.assertEqual(row_reduce(b+(multiply_row(v,a),)),row_reduce(b))

    def test_induced_cometric_must_keep_leaf_information(self):
        l=((F(1),F(0)),)
        self.assertEqual(geometric_cometric(l,((F(1),F(0)),(F(0),F(1)))),((F(1),),))
        self.assertEqual(geometric_cometric(l,((F(1,2),F(0)),(F(0),F(1)))),((F(2),),))

    def test_bad_hessian_rejected(self):
        with self.assertRaises(ValueError):
            geometric_cometric(((F(1),F(0)),),((F(1),F(0)),(F(0),F(-1))))

    def test_triple_overlap_cost_obstruction(self):
        low=({1,2},{2,3},{1,3}); high=({0,1},{0,2},{0,3})
        self.assertEqual([len(x) for x in low],[len(x) for x in high])
        self.assertEqual([len(low[i]&low[j]) for i in range(3) for j in range(i)],
                         [len(high[i]&high[j]) for i in range(3) for j in range(i)])
        self.assertEqual(len(set.union(*low)),3); self.assertEqual(len(set.union(*high)),4)
        self.assertLess(F(3),F(7,2)); self.assertLess(F(7,2),F(4))

if __name__=='__main__':
    unittest.main(verbosity=2)
