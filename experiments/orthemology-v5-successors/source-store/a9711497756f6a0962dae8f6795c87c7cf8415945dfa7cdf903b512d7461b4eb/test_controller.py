from dataclasses import replace
from fractions import Fraction
from itertools import product
from tests.support import BoundaryCase
from tests.fixtures import bernoulli, bernoulli_body, recovery, recovery_body, stale, stale_body, singleton

class ControllerTests(BoundaryCase):
    def setUp(self):
        self.model=self.module('model');self.cert=self.module('certificates');self.api=self.module('controller')
        self.m=self.model.validate_model(bernoulli());self.p=self.cert.check_positive(self.m,bernoulli_body())
    def initial(self):return self.api.initial_memory(self.m,self.p)
    def count_memory(self,phase,count,zeros,known1=False):
        m=self.initial()
        return replace(m,phase=phase,known1=known1,departures=(count,0),uses=((count,0),(0,0)),receipts=(((zeros,count-zeros),(0,0)),((0,0),(0,0))))
    def test_initial_phase_and_first_component_selection(self):
        m=self.initial();self.assertEqual((m.phase,m.known1,m.retained),(0,False,None))
        a,prepared=self.api.choose(self.m,self.p,m,0)
        self.assertEqual(a,0);self.assertEqual(prepared.retained,0);self.assertEqual(m.retained,None)
    def test_threshold_and_exact_gate_at_r_and_r_plus_one(self):
        self.assertEqual(self.api.threshold(self.m),Fraction(1,6))
        at_gate=self.count_memory(6,6,3)
        self.assertFalse(self.api.rejection(self.m,at_gate))
        self.assertTrue(self.api.rejection(self.m,self.count_memory(5,6,3)))
        self.assertFalse(self.api.rejection(self.m,self.count_memory(0,12,7)))
        self.assertTrue(self.api.rejection(self.m,self.count_memory(0,12,6)))
        self.assertEqual(self.api.threshold(self.model.validate_model(singleton())),1)
    def test_stale_row_guard_and_later_candidate_reentry(self):
        m=self.model.validate_model(stale());p=self.cert.check_positive(m,stale_body());memory=self.api.initial_memory(m,p)
        a,prepared=self.api.choose(m,p,memory,0);memory=self.api.observe(m,p,prepared,0,a,1)
        self.assertEqual(memory.phase,0);self.assertEqual(memory.uses[0][0],1)
        true_candidate=replace(memory,phase=1,retained=None)
        self.assertFalse(self.api.rejection(m,true_candidate))
        a,prepared=self.api.choose(m,p,true_candidate,1);self.assertEqual(a,1)
        # Global stale row remains stored; it is gated, never reset or forgotten.
        self.assertEqual(prepared.receipts[0][0],(0,1,0))
    def test_p1_zero_receipt_keeps_future_candidate_one(self):
        m=self.model.validate_model(recovery());p=self.cert.check_positive(m,recovery_body());mem=self.api.initial_memory(m,p)
        a,pre=self.api.choose(m,p,mem,0);mem=self.api.observe(m,p,pre,0,a,0)
        self.assertFalse(mem.known1);self.assertFalse(mem.fallback)
        mem=replace(mem,phase=1,retained=None)
        a,pre=self.api.choose(m,p,mem,0);mem=self.api.observe(m,p,pre,0,a,1)
        self.assertTrue(mem.known1);self.assertFalse(mem.fallback)
    def test_revelation_precedes_empirical_rejection_and_exit(self):
        m=self.model.validate_model(recovery());p=self.cert.check_positive(m,recovery_body());mem=self.api.initial_memory(m,p)
        a,pre=self.api.choose(m,p,mem,0);self.assertEqual(pre.retained,0)
        mem=self.api.observe(m,p,pre,0,a,1)
        self.assertEqual((mem.known1,mem.phase,mem.retained),(True,0,None))
        self.assertEqual(mem.uses[0][0],1)
        a,pre=self.api.choose(m,p,mem,1);mem=self.api.observe(m,p,pre,1,a,1)
        self.assertTrue(mem.known1);self.assertEqual(mem.phase,0);self.assertEqual(mem.retained,0)
    def test_known1_impossible_p1_zero_even_when_p0_positive(self):
        raw=recovery();raw['rows'][0][1][0]=[1,0]
        m=self.model.validate_model(raw);p=self.cert.check_positive(m,recovery_body());self.assertIsNotNone(p)
        mem=self.api.initial_memory(m,p);a,pre=self.api.choose(m,p,mem,0);mem=self.api.observe(m,p,pre,0,a,1)
        a,pre=self.api.choose(m,p,mem,1);mem=self.api.observe(m,p,pre,1,a,0)
        self.assertTrue(mem.known1);self.assertTrue(mem.fallback)
    def test_global_count_action_cycling_and_known1_no_rejection(self):
        raw=singleton();raw['n_actions']=2;raw['menus']=[[0,1]]
        raw['rows']=[[[[1],[1]]],[[[1],[1]]]];raw['priorities']=[[[0,0]],[[0,0]]]
        m=self.model.validate_model(raw);body=dict(K=(0,),W=(0,),D1=((0,0),(0,1)),D=((0,0),(0,1)),
          known_components=(((0,0),(0,1)),),uncertain_components=((((0,0),(0,1)),),(((0,0),(0,1)),)),
          known_routes=({'source':0,'steps':(),'component':0,'reveal':None},),
          uncertain_routes=tuple(({'source':0,'steps':(),'component':0,'reveal':None},) for _ in (0,1)))
        p=self.cert.check_positive(m,body);mem=replace(self.api.initial_memory(m,p),known1=True)
        actions=[]
        for _ in range(5):
            a,pre=self.api.choose(m,p,mem,0);actions.append(a);mem=self.api.observe(m,p,pre,0,a,0)
        self.assertEqual(actions,[0,1,0,1,0]);self.assertEqual(mem.departures,(5,));self.assertEqual(mem.phase,0)
    def test_exit_and_rejection_increment_phase_only_once(self):
        # All priorities even; candidate0 component at0; candidate1 may move to1 without revelation.
        raw=dict(n_states=2,n_actions=1,initial=0,menus=[[0],[0]],
                 rows=[[[['1/2','1/2']],[[0,1]]],[[[1,0]],[[0,1]]]],priorities=[[[0],[0]],[[0],[0]]])
        m=self.model.validate_model(raw);p=self.module('synthesis').solve(m)
        mem=replace(self.api.initial_memory(m,p),phase=1,departures=(1,0),uses=((1,),(0,)),receipts=(((1,0),),((0,0),)))
        a,pre=self.api.choose(m,p,mem,0)
        self.assertIsNotNone(pre.retained)
        mem=self.api.observe(m,p,pre,0,a,1)
        self.assertEqual(mem.phase,2);self.assertIsNone(mem.retained);self.assertFalse(mem.known1)
    def test_history_malformed_before_indexing(self):
        for history in ((),(0,0),(False,),(-1,),(2,),(0,True,0),(0,2,0),(0,0,-1),(0,0,'0'),None):
            with self.subTest(history=history):
                with self.assertRaises(ValueError):self.api.action_for_history(self.m,self.p,history)
        m=self.model.validate_model(stale());p=self.cert.check_positive(m,stale_body())
        with self.assertRaises(ValueError):self.api.action_for_history(m,p,(0,1,1))
    def test_off_policy_fallback_persists(self):
        # Initial emitted action is0; action1 is lawful but off-policy.
        mem=self.initial();a,pre=self.api.choose(self.m,self.p,mem,0);mem=self.api.observe(self.m,self.p,pre,0,1,1)
        self.assertTrue(mem.fallback)
        a,pre=self.api.choose(self.m,self.p,mem,1);self.assertEqual(a,0)
        mem=self.api.observe(self.m,self.p,pre,1,a,0);self.assertTrue(mem.fallback)
        self.assertEqual(self.api.action_for_history(self.m,self.p,(0,1,1,0,0)),0)
    def test_all_bounded_well_formed_histories_are_lawful(self):
        count=0
        for length in range(4):
            for values in product(range(2),repeat=2*length+1):
                action=self.api.action_for_history(self.m,self.p,values)
                self.assertIn(action,self.m.menus[values[-1]]);count+=1
        self.assertEqual(count,170)
    def test_replay_matches_incremental_on_supported_branches(self):
        frontier=[((self.m.initial,),self.initial())]
        for _ in range(5):
            following=[]
            for h,mem in frontier:
                a,pre=self.api.choose(self.m,self.p,mem,h[-1])
                self.assertEqual(self.api.action_for_history(self.m,self.p,h),a)
                for y in range(2):following.append((h+(a,y),self.api.observe(self.m,self.p,pre,h[-1],a,y)))
            frontier=following
        self.assertEqual(len(frontier),32)
    def test_runtime_does_not_read_priorities(self):
        class Forbidden:
            def __getitem__(self,key):raise AssertionError('runtime priority read')
        mem=self.initial();runtime=replace(self.m,priorities=Forbidden())
        a,pre=self.api.choose(runtime,self.p,mem,0);self.api.observe(runtime,self.p,pre,0,a,1)
    def test_initial_memory_rejects_unchecked_invalid_body(self):
        with self.assertRaises(ValueError):self.api.initial_memory(self.m,replace(self.p,W=()))
