#!/usr/bin/env python3
"""Executable theorem controls; run this directory's complete test suite."""
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
import json
import hashlib
import random
import sys
import unittest

from compiler import Rule, Tree, Dag, compile_tree, compile_dag, tree_step, tree_value, dag_value, prune_tree, prune_dag, normalize

METRICS = {}


def R(name, head, premises=(), support=(), cost=0):
    return Rule(name, head, tuple(premises), frozenset(support), Fraction(cost))


def pairs(frontiers):
    return {q: set(f) for q, f in frontiers.items()}


def unpruned_pair_oracle(judgements, rules, rounds):
    """Independent height enumeration: no pair pruning during any round."""
    table = {q: set() for q in judgements}
    for _ in range(rounds):
        nxt = {q: set(table[q]) for q in judgements}
        for rule in rules:
            for children in product(*(table[p] for p in rule.premises)):
                support = set(rule.support)
                cost = rule.cost
                for child_support, child_cost in children:
                    support.update(child_support)
                    cost += child_cost
                nxt[rule.head].add((frozenset(support),cost))
        table = nxt
    # Independent quadratic skyline filter, done only after all height rounds.
    answer = {}
    for q, values in table.items():
        answer[q] = set()
        for s,c in values:
            strictly_dominated = False
            for t,d in values:
                if t.issubset(s) and d <= c and (t != s or d != c):
                    strictly_dominated = True
                    break
            if not strictly_dominated:
                answer[q].add((s,c))
    return answer


class CompilerTests(unittest.TestCase):
    def test_zero_cycle_with_base_has_actual_finite_witness(self):
        rules = [R('base', 'q', support=['a'], cost=2), R('loop', 'q', ['q'])]
        result, history = compile_tree(('q',), rules)
        self.assertEqual(set(result['q']), {(frozenset('a'), Fraction(2))})
        self.assertEqual(tree_value(next(iter(result['q'].values())))[3], 1)

    def test_unsupported_cycles_are_not_proofs(self):
        rules = [R('pq', 'p', ['q']), R('qp', 'q', ['p'])]
        result, _ = compile_tree(('p', 'q'), rules)
        self.assertEqual(pairs(result), {'p': set(), 'q': set()})
        self.assertEqual(pairs(compile_dag(('p', 'q'), rules)), pairs(result))

    def test_cost_sensitive_support_tradeoff_survives(self):
        rules = [R('a', 'q', support=['a'], cost=10), R('ab', 'q', support=['a','b'], cost=1)]
        result, _ = compile_tree(('q',), rules)
        self.assertEqual(len(result['q']), 2)

    def test_n_rounds_are_needed_for_n_chain(self):
        rules = [R('base','q0',support=['e'])] + [R(str(i), f'q{i}', [f'q{i-1}']) for i in range(1,6)]
        result, history = compile_tree(tuple(f'q{i}' for i in range(6)), rules)
        self.assertFalse(history[5]['q5'])
        self.assertTrue(result['q5'])
        self.assertEqual(tree_value(next(iter(result['q5'].values())))[3], 6)

    def test_exact_support_can_shrink_under_tree_pruning(self):
        base = R('base','q',support=['a'])
        loop = R('loop','q',['q'],support=['b'])
        t = Tree(loop,(Tree(base,()),))
        reduced = prune_tree(t)
        self.assertEqual(tree_value(t)[1], frozenset(['a','b']))
        self.assertEqual(tree_value(reduced)[1], frozenset(['a']))
        self.assertEqual(tree_value(reduced)[3],1)

    def test_dag_sharing_defeats_intermediate_pair_pruning(self):
        rules = [R('p','p',support=['e'],cost=5), R('pa','a',['p']),
                 R('direct_a','a',support=['e'],cost=4), R('pb','b',['p']), R('target','t',['a','b'])]
        tree, _ = compile_tree(('p','a','b','t'),rules)
        dag = compile_dag(('p','a','b','t'),rules)
        self.assertEqual(set(tree['a']),{(frozenset('e'),Fraction(4))})
        self.assertEqual(set(tree['t']),{(frozenset('e'),Fraction(9))})
        self.assertEqual(set(dag['t']),{(frozenset('e'),Fraction(5))})
        selected = {rule.name for rule,_ in next(iter(dag['t'].values())).nodes}
        self.assertIn('pa',selected)
        self.assertNotIn('direct_a',selected)

    def test_repeated_premise_charges_tree_twice_dag_once(self):
        rules = [R('base','p',support=['e'],cost=7),R('twice','t',['p','p'],cost=1)]
        tree, _ = compile_tree(('p','t'),rules)
        dag = compile_dag(('p','t'),rules)
        self.assertEqual(set(tree['t']),{(frozenset('e'),Fraction(15))})
        self.assertEqual(set(dag['t']),{(frozenset('e'),Fraction(8))})

    def test_dag_earliest_representatives_are_acyclic_and_dominate(self):
        rules = [R('p1','p',support=['e'],cost=3),R('a','a',['p'],cost=1),
                 R('p2','p',['a'],support=['f'],cost=2),R('t','t',['p','a'],cost=1)]
        dag = Dag(((rules[0],()),(rules[1],(0,)),(rules[2],(1,)),(rules[3],(2,1))),3)
        before = dag_value(dag)
        reduced = prune_dag(dag)
        after = dag_value(reduced)
        self.assertEqual(before[0],after[0])
        self.assertLessEqual(after[1],before[1])
        self.assertLessEqual(after[2],before[2])
        self.assertEqual(len(reduced.nodes),3)
        self.assertEqual(after[1],frozenset('e'))

    def test_nonnegative_fraction_prices_are_exact(self):
        rules = [R('base','p',support=['e'],cost=Fraction(1,3)), R('loop','p',['p'],cost=Fraction(1,7)),
                 R('target','t',['p'],cost=Fraction(2,5))]
        tree,_ = compile_tree(('p','t'),rules)
        self.assertEqual(set(tree['t']),{(frozenset('e'),Fraction(11,15))})

    def test_negative_costs_and_missing_scopes_are_rejected(self):
        with self.assertRaises(ValueError):
            compile_tree(('q',),[R('bad','q',['q'],cost=-1)])
        with self.assertRaises(ValueError):
            compile_tree(('q',),[R('bad','q',['unscoped'])])
        with self.assertRaises(ValueError):
            compile_dag(('q',),[R('bad','q',cost=-1)])

    def test_exhaustive_small_grammars_against_unpruned_height_oracle(self):
        judgements = ('p','q')
        universe = []
        for q in judgements:
            for e in ('a','b'):
                for c in (0,2):
                    universe.append(R(f'leaf{len(universe)}',q,support=[e],cost=c))
        for q in judgements:
            for p in judgements:
                universe.append(R(f'unary{len(universe)}',q,[p]))
                universe.append(R(f'binary{len(universe)}',q,[p,p],cost=1))
        count = witnesses = 0
        for size in range(5):
            for selected in combinations(universe,size):
                result, history = compile_tree(judgements,selected)
                actual = pairs(result)
                self.assertEqual(actual,unpruned_pair_oracle(judgements,selected,4))
                self.assertEqual(actual,pairs(tree_step(judgements,selected,result)))
                dag = compile_dag(judgements,selected)
                for q in judgements:
                    for pair,witness in result[q].items():
                        head,support,cost,height,_ = tree_value(witness)
                        self.assertEqual((head,support,cost),(q,*pair))
                        self.assertLessEqual(height,len(judgements))
                        self.assertTrue(any(s <= pair[0] and c <= pair[1] for s,c in dag[q]))
                        witnesses += 1
                    for pair,witness in dag[q].items():
                        head,support,cost,nodes = dag_value(witness)
                        self.assertEqual((head,support,cost),(q,*pair))
                        self.assertLessEqual(nodes,len(judgements))
                        witnesses += 1
                count += 1
        self.assertEqual(count,2517)
        METRICS['exhaustive_grammars'] = count
        METRICS['exhaustive_compiled_witnesses_checked'] = witnesses
        METRICS['unpruned_oracle_height'] = 4
        METRICS['compiled_tree_height'] = 2

    def test_seeded_general_tree_and_dag_pruning(self):
        rng = random.Random(20261009)
        comparisons = 0
        for trial in range(250):
            nodes = []
            for i in range(rng.randrange(2,13)):
                refs = () if i == 0 else (i-1,) + tuple(rng.randrange(i) for _ in range(rng.randrange(3)))
                q = rng.choice(('p','q','r','s'))
                premises = [nodes[j][0].head for j in refs]
                support = [e for e in ('a','b','c') if rng.randrange(3) == 0]
                rule = R(f't{trial}n{i}',q,premises,support,rng.randrange(6))
                nodes.append((rule,refs))
            original = Dag(tuple(nodes),len(nodes)-1)
            reduced = prune_dag(original)
            q,s,c,_ = dag_value(original)
            q1,s1,c1,size = dag_value(reduced)
            self.assertEqual(q,q1)
            self.assertLessEqual(s1,s)
            self.assertLessEqual(c1,c)
            self.assertEqual(size,len({r.head for r,_ in reduced.nodes}))
            trees = []
            for rule, refs in nodes:
                trees.append(Tree(rule,tuple(trees[j] for j in refs)))
            original_tree = trees[-1]
            reduced_tree = prune_tree(original_tree)
            tq,ts,tc,_,_ = tree_value(original_tree)
            rq,rs,rc,rh,_ = tree_value(reduced_tree)
            self.assertEqual(tq,rq)
            self.assertLessEqual(rs,ts)
            self.assertLessEqual(rc,tc)
            judgements = tuple(sorted({r.head for r,_ in nodes}))
            self.assertLessEqual(rh,len(judgements))
            rules = tuple(r for r,_ in nodes)
            dag_compiled = compile_dag(judgements,rules)
            tree_compiled,_ = compile_tree(judgements,rules)
            self.assertTrue(any(a <= s and b <= c for a,b in dag_compiled[q]))
            self.assertTrue(any(a <= ts and b <= tc for a,b in tree_compiled[q]))
            comparisons += 1
        METRICS['seeded_root_reachable_dags_and_unfoldings'] = comparisons
        METRICS['seed'] = 20261009


if __name__ == '__main__':
    module = sys.modules[__name__]
    suite = (unittest.defaultTestLoader.loadTestsFromNames(sys.argv[1:],module)
             if len(sys.argv)>1 else unittest.defaultTestLoader.loadTestsFromModule(module))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    here = Path(__file__).resolve().parent
    record = {'status':'PASS' if result.wasSuccessful() else 'FAIL',
              'tests_run':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),
              'metrics':METRICS,
              'source_sha256':{p:hashlib.sha256((here/p).read_bytes()).hexdigest()
                               for p in ('compiler.py','verify.py','RESULT.md')},
              'scope':'Exact finite implementation checks; not a kernel proof of the general theorem.'}
    (here/'CHECK_RESULTS.json').write_text(json.dumps(record,indent=2)+'\n')
    sys.exit(0 if result.wasSuccessful() else 1)
