from itertools import product
from unittest.mock import patch
from tests.support import BoundaryCase, graph_model, subsets
from finite import all_components, component, used


def targets(components):
    return frozenset(s for c in components for s in used(c))


class ThresholdTests(BoundaryCase):
    def api(self): return self.module('efficient')

    def compare(self,m,pairs):
        api=self.api()
        actual=api.known_components(m,pairs)
        self.assertEqual(targets(actual),targets(all_components(m,1,pairs)))
        self.assertEqual(actual,tuple(sorted(set(actual))))
        self.assertTrue(all(component(m,1,c) for c in actual))
        for theta in (0,1):
            actual=api.uncertain_components(m,theta,pairs)
            self.assertEqual(targets(actual),targets(all_components(m,theta,pairs,True)),(m,pairs,theta))
            self.assertEqual(actual,tuple(sorted(set(actual))))
            self.assertTrue(all(component(m,theta,c,True) for c in actual))

    def test_even_threshold_excludes_lower_odd_action(self):
        m=graph_model([[[1],[1]]],priorities=[[[2,1]],[[2,1]]])
        self.assertEqual(self.api().known_components(m,((0,0),(0,1))), (((0,0),),))
        self.compare(m,((0,0),(0,1)))

    def test_two_separate_even_minimum_witnesses(self):
        m=graph_model([[[1],[1],[1]]],priorities=[[[2,3,1]],[[3,2,1]]])
        for theta in (0,1):
            self.assertEqual(self.api().uncertain_components(m,theta,((0,0),(0,1),(0,2))), (((0,0),(0,1)),))

    def test_distinguishing_pair_and_minimum_pair_may_differ(self):
        rows=[[["1/2","1/2"]],[["1/2","1/2"]]]
        other=[[["1/2","1/2"]],[["1/3","2/3"]]]
        m=graph_model(rows,rows1=other,priorities=[[[2],[3]],[[1],[1]]])
        self.assertEqual(self.api().uncertain_components(m,0,((0,0),(1,0))), (((0,0),(1,0)),))
        self.compare(m,((0,0),(1,0)))

    def test_equal_support_is_not_numerical_row_equality(self):
        rows=[[["2/3","1/3"],["2/3","1/3"]] for _ in (0,1)]
        other=[[["1/3","2/3"],["1/3","2/3"]] for _ in (0,1)]
        priorities=[[[2,1],[2,1]],[[1,2],[1,2]]]
        pairs=((0,0),(0,1),(1,0),(1,1))
        unequal=graph_model(rows,rows1=other,priorities=priorities)
        equal=graph_model(rows,priorities=priorities)
        for theta in (0,1):
            self.assertEqual(targets(self.api().uncertain_components(unequal,theta,pairs)),frozenset({0,1}))
            self.assertEqual(self.api().uncertain_components(equal,theta,pairs),())

    def test_revealing_action_removed_whole_for_candidate_one(self):
        m=graph_model([[[1,0]],[[0,1]]],rows1=[[["1/2","1/2"]],[[1,0]]])
        self.assertEqual(self.api().uncertain_components(m,1,((0,0),(1,0))),())
        self.compare(m,((0,0),(1,0)))

    def test_huge_priorities_only_enumerate_present_values(self):
        api=self.api(); large=1<<8192
        m=graph_model([[[1],[1],[1]]],priorities=[[[large,large+2,1]],[[large+2,large,1]]])
        pairs=((0,0),(0,1),(0,2)); original=api.maximal_components
        with patch.object(api,'maximal_components',wraps=original) as counted:
            api.known_components(m,pairs)
            self.assertEqual(counted.call_count,2)
        with patch.object(api,'maximal_components',wraps=original) as counted:
            result=api.uncertain_components(m,0,pairs)
            self.assertEqual(targets(result),frozenset({0}))
            self.assertLessEqual(counted.call_count,3+3**2)

    def test_every_two_state_one_action_small_support_priority_input(self):
        self.api(); options=([1,0],[0,1],['1/2','1/2']); pairs=((0,0),(1,0)); cases=0
        for row_choices in product(options,repeat=4):
            for labels in product(range(3),repeat=4):
                m=graph_model([[row_choices[0]],[row_choices[1]]],
                    rows1=[[row_choices[2]],[row_choices[3]]],
                    priorities=[[[labels[0]],[labels[1]]],[[labels[2]],[labels[3]]]])
                for allowed in subsets(pairs):
                    self.compare(m,allowed); cases+=1
        self.assertEqual(cases,26244)

    def test_all_single_state_three_action_priority_vectors_and_subsets(self):
        self.api(); pairs=((0,0),(0,1),(0,2)); cases=0
        for labels in product(range(3),repeat=6):
            m=graph_model([[[1],[1],[1]]],priorities=[[list(labels[:3])],[list(labels[3:])]])
            for allowed in subsets(pairs): self.compare(m,allowed); cases+=1
        self.assertEqual(cases,5832)

    def test_malformed_candidate_mode_and_pairs(self):
        api=self.api(); m=graph_model([[[1]]])
        for theta in (False,2,-1):
            with self.assertRaises(ValueError): api.uncertain_components(m,theta,())
        for fn in (api.known_components,lambda m,p:api.uncertain_components(m,0,p)):
            for pairs in (((0,0),(0,0)),((0,1),)):
                with self.assertRaises(ValueError): fn(m,pairs)
