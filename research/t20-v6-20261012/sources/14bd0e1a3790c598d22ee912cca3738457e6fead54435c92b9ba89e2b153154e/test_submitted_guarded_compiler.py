"""Small deterministic external-to-implementation controls; no DAG claims."""
from fractions import Fraction
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from guarded_compiler import Rule, Tree, compile_exact, prune_exact, tree_value

def rule(name,head,premises=(),support=(),cost=0,allowed=None):
    return Rule(name,head,tuple(premises),frozenset(support),Fraction(cost),allowed)

def allow(*supports):
    return frozenset((frozenset(s),) for s in supports)

class IndependentSubmittedControls(unittest.TestCase):
    def test_sharp_six_round_bound(self):
        rules=(rule('chain','q0',('q1',)),rule('base','q1'),
               rule('add-a','q1',('q0',),'a',allowed=allow('')),
               rule('add-b','q1',('q0',),'b',allowed=allow('a')))
        table,hist=compile_exact(('q0','q1'),('a','b'),rules)
        full=frozenset('ab')
        self.assertNotIn(full,hist[5]['q0'])
        self.assertEqual(hist[6]['q0'][full],0)
        self.assertEqual(tree_value(table['q0'][full][1],rules)[3],6)

    def test_equal_support_keys_are_not_cost_fixed_point(self):
        rules=(rule('expensive','p',cost=10),rule('cheap','q'),rule('route','p',('q',)))
        table,hist=compile_exact(('p','q'),(),rules)
        self.assertEqual({q:set(v) for q,v in hist[1].items()},
                         {q:set(v) for q,v in hist[2].items()})
        self.assertNotEqual(hist[1],hist[2])
        self.assertEqual(hist[1]['p'][frozenset()],10)
        self.assertEqual(hist[2]['p'][frozenset()],0)

    def test_strictly_nonmonotone_terminal_guard(self):
        rules=(rule('empty','p'),rule('full','p',support='ab'),
               rule('enrich','p',('p',),'a'),
               rule('accept-a','t',('p',),allowed=allow('a')))
        table,hist=compile_exact(('p','t'),('a','b'),rules)
        self.assertEqual(hist[2]['t'],{})
        self.assertEqual(hist[3]['t'],{frozenset('a'):0})
        self.assertEqual(set(table['t']),{frozenset('a')})

    def test_pruning_deletes_positive_cost_side_subtree(self):
        base=rule('base','p',support='a',cost=1)
        join=rule('join','p',('p','p'),cost=5,
                  allowed=frozenset({(frozenset('a'),frozenset('a'))}))
        end=rule('end','t',('p',),allowed=allow('a'))
        rules=(base,join,end)
        leaf=Tree(base,())
        witness=Tree(end,(Tree(join,(leaf,leaf)),))
        reduced=prune_exact(witness,rules)
        before,after=tree_value(witness,rules),tree_value(reduced,rules)
        self.assertEqual(before[:2],after[:2])
        self.assertEqual(before[2],7)
        self.assertEqual(after[2],1)
        self.assertEqual(after[3],2)

    def test_mutable_premise_container_rejected(self):
        malformed=Rule('leaf','p',[],frozenset({'e'}),0)
        with self.assertRaises((TypeError,ValueError)):
            compile_exact(('p',),('e',),(malformed,))

if __name__=='__main__':
    unittest.main(verbosity=2)
