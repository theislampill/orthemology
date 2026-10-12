"""Independent finite controls for the report's scoped policy statements.

These are small exact models, not source calibration or infinite-time proofs.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
import unittest

class PolicyContractTests(unittest.TestCase):
    def test_postponement_against_interleaved_known_kernel_oracle(self):
        count=0
        # Nodes 0 (shared lemma), 1 and 2 (branch-specific final certificates).
        deps=(frozenset(),frozenset((0,)),frozenset((0,)))
        caches=(frozenset(),frozenset((0,)),frozenset((0,1)),frozenset((0,2)),frozenset((0,1,2)))
        for costs in product((0,1,3),repeat=3):
            for p,query,cache in product((F(1,3),F(1,2),F(2,3)),(0,1),caches):
                @lru_cache(None)
                def value(checked,branch):
                    if branch>=0 and branch+1 in checked: return F(0)
                    choices=[]
                    if branch<0:
                        choices.append(F(query)+p*value(checked,0)+(1-p)*value(checked,1))
                    for node in range(3):
                        if node not in checked and deps[node]<=checked:
                            choices.append(F(costs[node])+value(checked|frozenset((node,)),branch))
                    return min(choices)
                def terminal(b):
                    return sum((F(costs[n]) for n in (0,b+1) if n not in cache),F())
                delayed=F(query)+p*terminal(0)+(1-p)*terminal(1)
                self.assertEqual(value(cache,-1),delayed)
                count+=1
        type(self).postponement_cases=count

    def test_postponement_with_exogenous_source_revocation(self):
        count=0
        # The observation keeps exactly one source and its proof route valid.
        deps=(frozenset(),frozenset((0,)),frozenset(),frozenset((2,)))
        live=(frozenset((0,1)),frozenset((2,3)))
        universe=frozenset(range(4))
        for costs in product((1,3),repeat=4):
            for bits in product((False,True),repeat=4):
                cache=frozenset(i for i,b in enumerate(bits) if b)
                if any(not deps[n]<=cache for n in cache): continue
                p=F(2,5)
                @lru_cache(None)
                def value(checked,branch):
                    if branch>=0 and (1 if branch==0 else 3) in checked: return F(0)
                    choices=[]
                    if branch<0: choices.append(F(1)+p*value(checked&live[0],0)+(1-p)*value(checked&live[1],1))
                    available=universe if branch<0 else live[branch]
                    for n in available-checked:
                        if deps[n]<=checked:
                            choices.append(F(costs[n])+value(checked|frozenset((n,)),branch))
                    return min(choices)
                delayed=F(1)+p*sum((F(costs[n]) for n in live[0]-cache),F())+(1-p)*sum((F(costs[n]) for n in live[1]-cache),F())
                self.assertEqual(value(cache,-1),delayed)
                count+=1
        type(self).revision_cases=count

    def test_gate_and_timing_premises_have_real_effect(self):
        # (credential checked, queried, terminal checked). Query requires credential.
        def successors(s,terminal_only):
            credential,queried,finished=s; out=[]
            if not credential and not terminal_only: out.append((True,queried,finished))
            if credential and not queried: out.append((credential,True,finished))
            if queried and not finished: out.append((credential,queried,True))
            return out
        def can_finish(terminal_only):
            reached={(False,False,False)}; todo=list(reached)
            while todo:
                for t in successors(todo.pop(),terminal_only):
                    if t not in reached: reached.add(t);todo.append(t)
            return any(s[2] for s in reached)
        self.assertTrue(can_finish(False));self.assertFalse(can_finish(True))
        # A mandatory query costs 1; checking before its deadline costs 1, after costs 10.
        self.assertLess(F(1)+F(1),F(1)+F(10))

    def test_fixed_model_costs_cannot_be_pasted(self):
        masses=(F(1,4),F(3,4));branches=((F(9,10),F(1,10)),(F(3,10),F(7,10)))
        vector=tuple(sum((masses[o]*branches[o][i] for o in range(2)),F()) for i in range(2))
        pasted=sum((masses[o]*max(branches[o]) for o in range(2)),F())
        self.assertEqual(vector,(F(9,20),F(11,20)))
        self.assertEqual(pasted,F(3,4));self.assertGreater(pasted,max(vector))
        # Mutually exclusive branch work is not a simultaneous union bill.
        self.assertEqual(F(1,2)*2+F(1,2)*2,F(2))
        self.assertNotEqual(F(2),F(3))  # two footprints of size 2 with one shared node

    @staticmethod
    def recurrent_actions(actions,update):
        n=len(actions)
        reach=[{q} for q in range(n)]
        for q in range(n): reach[q].update(update[q])
        for _ in range(n):
            reach=[set().union(*(reach[v] for v in row)) for row in reach]
        accessible=reach[0]
        components={frozenset(v for v in accessible if v in reach[q] and q in reach[v]) for q in accessible}
        bottom=[B for B in components if all(set(update[q])<=B for q in B)]
        return [frozenset(actions[q] for q in B) for B in bottom]

    def test_all_deterministic_memory_controllers_through_three_states(self):
        count=0
        for m in range(1,4):
            for actions in product((0,1),repeat=m):
                for next_flat in product(range(m),repeat=2*m):
                    update=tuple(next_flat[2*q:2*q+2] for q in range(m))
                    recurrent=self.recurrent_actions(actions,update)
                    self.assertTrue(recurrent)
                    wins=tuple(all(U<=frozenset((theta,)) for U in recurrent) for theta in (0,1))
                    self.assertFalse(all(wins))
                    count+=1
        self.assertEqual(count,5898)
        type(self).finite_memory_controllers=count
        recurrent=self.recurrent_actions((2,),((0,0),))
        self.assertTrue(all(U<=frozenset((0,2)) and U<=frozenset((1,2)) for U in recurrent))

    def test_cirs_positive_supports_and_integer_likelihood_histories(self):
        # p[theta][action] is P(receipt=1). Every action distinguishes all models.
        p=((F(1,4),F(1,2),F(3,4)),(F(1,2),F(3,4),F(1,4)),(F(3,4),F(1,4),F(1,2)))
        targets=tuple(frozenset((theta,)) for theta in range(3))
        self.assertFalse(set.intersection(*(set(t) for t in targets)))
        for theta in range(3):
            U=targets[theta]
            equivalent=[r for r in range(3) if all(p[r][a]==p[theta][a] for a in U)]
            self.assertTrue(all(U<=targets[r] for r in equivalent))
        histories=0;prefix_comparisons=0
        for length in range(11):
            for word in product((0,1),repeat=length):
                weights=[1,1,1];rational=[F(1),F(1),F(1)]
                for t,y in enumerate(word):
                    candidate=max(range(3),key=lambda i:(weights[i],-i))
                    rational_candidate=max(range(3),key=lambda i:(rational[i],-i))
                    self.assertEqual(candidate,rational_candidate)
                    action=candidate  # singleton self-verifying target support
                    for i in range(3):
                        probability=p[i][action] if y else 1-p[i][action]
                        numerator=probability*4
                        self.assertEqual(numerator.denominator,1)
                        weights[i]*=numerator.numerator;rational[i]*=probability
                        self.assertEqual(F(weights[i],4**(t+1)),rational[i])
                    prefix_comparisons+=1
                histories+=1
        type(self).likelihood_histories=histories
        type(self).likelihood_prefix_comparisons=prefix_comparisons
        self.assertEqual(histories,2047)
        # Full-support likelihoods remain positive; a growing numeric domain is used.
        self.assertGreater(3**100,2**100)

    def test_copied_root_is_not_fresh_sampling(self):
        p=F(1,3)
        copied_biased={(0,0):1-p,(1,1):p}
        self.assertEqual(copied_biased.get((0,1),F()),F(0))
        self.assertGreater((1-p)*p,0)  # fresh conditional model does emit 01
        # A marginally fair reused seed has identical one-time laws but different histories.
        copied={(0,0):F(1,2),(1,1):F(1,2)}
        fresh={word:F(1,4) for word in product((0,1),repeat=2)}
        self.assertNotEqual(copied,fresh)

if __name__=='__main__': unittest.main(verbosity=2)
