import unittest
from itertools import product
from research.contracts import affected_nodes, replay_dag

class IteratorRegression(unittest.TestCase):
    def test_transitive_one_shot(self):
        self.assertEqual(affected_nodes({'second':iter(['first']), 'first':iter(['source'])}, ['source']), {'first','second'})
    def test_all_four_node_dags_with_one_primitive(self):
        edges=[(i,j) for i in range(4) for j in range(-1,i)]
        for bits in product((False,True),repeat=len(edges)):
            deps={i:[] for i in range(4)}
            for (i,j),b in zip(edges,bits):
                if b: deps[i].append(j)
            expected=affected_nodes(deps,[-1])
            self.assertEqual(affected_nodes({i:iter(v) for i,v in deps.items()},iter([-1])),expected)
    def test_actual_replay_remains_correct(self):
        deps={'second':iter(['first']), 'first':iter(['source'])}
        fs={'first':lambda v:2*v['source'], 'second':lambda v:v['first']+1}
        values,order=replay_dag(deps,fs,{'source':4},{'first':2,'second':3},['source'])
        self.assertEqual((values['first'], values['second']),(8,9))
