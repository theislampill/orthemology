"""Small deterministic discriminators, not a sampling/optimization campaign."""
from dataclasses import replace
from fractions import Fraction as F
from itertools import combinations, product
import unittest

from guarded_dag import Dag, Rule, dag_value, normalize, guarded, unguarded

def R(name, head, premises=(), support=(), cost=0, allowed=None):
    return Rule(name, head, tuple(premises), frozenset(support), F(cost), allowed)

def guard(*tuples):
    return frozenset(tuple(frozenset(s) for s in ss) for ss in tuples)

def powerset(items):
    return tuple(frozenset(c) for n in range(len(items)+1) for c in combinations(items,n))

def refine(J, E, rules):
    """Literal finite-state transport, used only on tiny declared fixtures."""
    states = tuple((q,s) for q in J for s in powerset(E))
    lifted, decode = [], {}
    for r in rules:
        for ss in product(powerset(E), repeat=len(r.premises)):
            if r.allowed is not None and ss not in r.allowed:
                continue
            x = unguarded.Rule((r.name,ss), (r.head,r.support.union(*ss)),
                               tuple(zip(r.premises,ss)), r.support, r.cost)
            lifted.append(x)
            decode[x] = r
    return states, tuple(lifted), decode

def catalogue(J, E, rules):
    states, lifted, decode = refine(J,E,rules)
    result = unguarded.compile_dag(states,lifted)
    out = {}
    for state, rows in result.items():
        out[state] = []
        for pair, d in rows.items():
            original = Dag(tuple((decode[r],refs) for r,refs in d.nodes),d.root)
            value = dag_value(original,J,E,rules)
            assert value[:3] == (state[0],state[1],pair[1])
            out[state].append((pair[1],original))
    return out


class GuardedDagTests(unittest.TestCase):
    def test_normalizer_removes_duplicate_exact_states(self):
        a=R('a','q',support='a',cost=2)
        t=R('t','t',('q','q'),allowed=guard(('a','a')))
        d=Dag(((a,()),(a,()),(t,(0,1))),2)
        n=normalize(d,('q','t'),'a',(a,t))
        self.assertEqual(len(n.nodes),2)
        self.assertEqual(n.nodes[n.root][1],(0,0))

    def test_false_nullary_guard_rejected(self):
        a=R('false','q',allowed=frozenset())
        with self.assertRaises(ValueError):
            dag_value(Dag(((a,()),),0),('q',),(),(a,))

    def test_ordered_repeated_supports_and_nonmonotone_guard_preserved(self):
        a=R('a','q',support='a',cost=F(1,3))
        b=R('b','q',support='b',cost=F(2,5))
        wrap=R('wrap','q',('q',),cost=3)
        t=R('t','t',('q','q','q'),cost=F(1,7),allowed=guard(('a','b','a')))
        rules=(a,b,wrap,t); J=('q','t'); E='ab'
        d=Dag(((a,()),(wrap,(0,)),(b,()),(t,(1,2,1))),3)
        n=normalize(d,J,E,rules)
        before,after=dag_value(d,J,E,rules),dag_value(n,J,E,rules)
        self.assertEqual(after[:2],before[:2])
        self.assertEqual(after[2],F(1,3)+F(2,5)+F(1,7))
        self.assertEqual(before[2]-after[2],3)
        self.assertEqual(n.nodes[n.root][1],(0,1,0))
        # Same root union but reversed ordered premise supports is invalid.
        with self.assertRaises(ValueError):
            dag_value(Dag(n.nodes[:-1]+((t,(1,0,0)),),n.root),J,E,rules)
        # Superset replacement also fails this genuinely nonmonotone guard.
        ab=R('ab','q',support='ab')
        with self.assertRaises(ValueError):
            dag_value(Dag(((ab,()),(b,()),(t,(0,1,0))),2),J,E,rules+(ab,))

    def test_judgement_only_redirection_is_invalid(self):
        a=R('a','q',support='a'); b=R('b','q',support='b')
        t=R('t','t',('q','q'),allowed=guard(('a','b')))
        d=Dag(((a,()),(b,()),(t,(0,1))),2)
        self.assertEqual(len(normalize(d,('q','t'),'ab',(a,b,t)).nodes),3)
        with self.assertRaises(ValueError):
            dag_value(Dag(((a,()),(t,(0,0))),1),('q','t'),'ab',(a,b,t))

    def test_admission_is_checked_even_for_same_named_rule(self):
        a=R('a','q',support='a',cost=2)
        for fake in (R('invented','q'),replace(a,cost=F(0))):
            with self.assertRaises(ValueError):
                dag_value(Dag(((fake,()),),0),('q',),'a',(a,))

    def test_cycles_missing_refs_and_unreachable_nodes_rejected(self):
        a=R('a','q'); loop=R('loop','q',('q',))
        bad=(Dag(((loop,(0,)),),0),Dag(((loop,(1,)),),0),
             Dag(((a,()),(a,())),0),Dag(((loop,()),),0))
        for d in bad:
            with self.assertRaises(ValueError):
                dag_value(d,('q',),(),(a,loop))

    def test_cyclic_grammar_seeded_and_unseeded_catalogue(self):
        loop=R('loop','q',('q',))
        self.assertEqual(catalogue(('q',),(),(loop,))[('q',frozenset())],[])
        seed=R('seed','q',cost=F(1,3))
        cat=catalogue(('q',),(),(loop,seed))
        self.assertEqual([c for c,_ in cat[('q',frozenset())]],[F(1,3)])
        false=R('false','q',allowed=frozenset())
        self.assertEqual(catalogue(('q',),(),(loop,false))[('q',frozenset())],[])

    def test_exact_support_growth_uses_two_states_of_one_judgement(self):
        seed=R('seed','q'); add=R('add','q',('q',),'a',cost=2,allowed=guard(('',)))
        rules=(seed,add)
        cat=catalogue(('q',),'a',rules)
        self.assertEqual([c for c,_ in cat[('q',frozenset('a'))]],[F(2)])
        d=cat[('q',frozenset('a'))][0][1]
        self.assertEqual(len(d.nodes),2)
        self.assertEqual(normalize(d,('q',),'a',rules),d)

    def test_zero_cost_tie_terminates_by_node_removal(self):
        seed=R('seed','q'); loop=R('loop','q',('q',))
        d=Dag(((seed,()),(loop,(0,)),(loop,(1,))),2)
        n=normalize(d,('q',),(),(seed,loop))
        self.assertEqual(len(n.nodes),1)
        self.assertEqual(d.nodes[d.root][0],loop)
        self.assertEqual(n.nodes[n.root][0],seed) # root rule identity may change
        self.assertEqual(dag_value(d,('q',),(),(seed,loop))[2],0)
        self.assertEqual(dag_value(n,('q',),(),(seed,loop))[2],0)
        # Keeping the latest same-state loop and redirecting to that chosen
        # representative creates a self-edge, despite the original valid DAG.
        with self.assertRaises(ValueError):
            dag_value(Dag(((loop,(0,)),),0),('q',),(),(seed,loop))

    def test_negative_cycle_breaks_cost_nonincrease_and_attainment(self):
        seed=R('seed','q'); loop=R('negative','q',('q',),cost=-1)
        costs=[]
        for count in range(4):
            d=Dag(((seed,()),)+tuple((loop,(i,)) for i in range(count)),count)
            costs.append(sum(r.cost for r,_ in d.nodes))
            with self.assertRaises(ValueError):
                normalize(d,('q',),(),(seed,loop))
        self.assertEqual(costs,[0,-1,-2,-3])
        self.assertGreater(costs[0],costs[-1])

    def test_branch_bound_is_not_total_node_bound(self):
        E='abc'; supports=powerset(E); proper=supports[:-1]
        leaves=tuple(R('leaf'+str(i),'q',support=s) for i,s in enumerate(proper))
        root=R('root','q',('q',)*len(proper),allowed=frozenset((proper,)))
        d=Dag(tuple((r,()) for r in leaves)+((root,tuple(range(len(leaves)))),),len(leaves))
        n=normalize(d,('q',),E,leaves+(root,))
        v=dag_value(n,('q',),E,leaves+(root,))
        self.assertEqual(len(n.nodes),8) # n*2^m with n=1, m=3
        self.assertGreater(len(n.nodes),1*(len(E)+1))
        self.assertEqual(v[3],2)
        self.assertEqual(len(set(v[5])),len(n.nodes))

    def test_earliest_is_not_cheapest_and_scalar_dag_dp_still_fails(self):
        dear=R('dear','q',cost=5); cheap=R('cheap','q',cost=1)
        t=R('t','t',('q','q')); rules=(dear,cheap,t)
        d=Dag(((dear,()),(cheap,()),(t,(0,1))),2)
        n=normalize(d,('q','t'),(),rules)
        self.assertEqual(dag_value(n,('q','t'),(),rules)[2],5)
        self.assertEqual(catalogue(('q','t'),(),rules)[('t',frozenset())][0][0],1)
        # Inherited strict standalone-pruning counterexample, all exact supports equal.
        p=R('p','p',support='e',cost=5); pa=R('pa','a',('p',))
        direct=R('direct','a',support='e',cost=4); pb=R('pb','b',('p',))
        top=R('top','t',('a','b')); rr=(p,pa,direct,pb,top); J=('p','a','b','t')
        table,_=guarded.compile_exact(J,'e',rr)
        self.assertEqual(table['t'][frozenset('e')][0],9)
        d=Dag(((p,()),(pa,(0,)),(pb,(0,)),(top,(1,2))),3)
        self.assertEqual(dag_value(normalize(d,J,'e',rr),J,'e',rr)[2],5)

    def test_undeclared_node_identity_guard_is_outside_contract(self):
        q=R('q','q'); t=R('t','t',('q','q'))
        d=Dag(((q,()),(q,()),(t,(0,1))),2)
        n=normalize(d,('q','t'),(),(q,t))
        self.assertEqual(len(set(d.nodes[d.root][1])),2)
        self.assertEqual(len(set(n.nodes[n.root][1])),1)
        # A hypothetical distinct-node predicate changes; actual support guard does not.
        self.assertEqual(dag_value(d,('q','t'),(),(q,t))[:2],
                         dag_value(n,('q','t'),(),(q,t))[:2])


if __name__=='__main__':
    unittest.main(verbosity=2)
