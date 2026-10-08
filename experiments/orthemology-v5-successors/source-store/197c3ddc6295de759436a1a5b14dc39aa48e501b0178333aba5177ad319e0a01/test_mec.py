from itertools import product
from tests.support import BoundaryCase, graph_model, subsets, end_component

class MecTests(BoundaryCase):
    def api(self): return self.module('mec')

    def test_empty_and_singleton_source_totality(self):
        api = self.api(); m = graph_model([[[1], [1]]])
        self.assertEqual(api.maximal_components(m, 0, ()), ())
        self.assertEqual(api.maximal_components(m, 0, ((0,0),)), (((0,0),),))
        self.assertEqual(api.maximal_components(m, 1, ((0,1),(0,0))), (((0,0),(0,1)),))

    def test_disconnected_components_remain_separate(self):
        m=graph_model([[[1,0]], [[0,1]]])
        self.assertEqual(self.api().maximal_components(m, 0, ((0,0),(1,0))), (((0,0),),((1,0),)))

    def test_all_successors_must_stay_inside(self):
        m=graph_model([[[1,0],['1/2','1/2']], [[0,1],[0,1]]])
        self.assertEqual(self.api().maximal_components(m, 0, ((0,0),(0,1))), (((0,0),),))
        self.assertEqual(self.api().maximal_components(m, 0, ((0,1),)), ())

    def test_recursive_split_after_an_unsafe_action_disappears(self):
        # Initial SCC {0,1}; after removing action 0->(1,2), it splits again.
        m=graph_model([[[0,'1/2','1/2'],[1,0,0]], [[1,0,0],[0,1,0]], [[0,0,1],[0,0,1]]])
        pairs=((0,0),(0,1),(1,0),(1,1),(2,0))
        self.assertEqual(self.api().maximal_components(m,0,pairs), (((0,1),),((1,1),),((2,0),)))

    def test_overlapping_end_components_merge_with_all_internal_actions(self):
        m=graph_model([[[1,0],[0,1]], [[1,0],[0,1]]])
        pairs=((0,0),(0,1),(1,0),(1,1))
        self.assertEqual(self.api().maximal_components(m,0,pairs), (pairs,))

    def test_candidate_kernel_is_used(self):
        m=graph_model([[[1,0]], [[0,1]]], rows1=[[[0,1]],[[1,0]]])
        pairs=((0,0),(1,0))
        self.assertEqual(self.api().maximal_components(m,0,pairs), (((0,0),),((1,0),)))
        self.assertEqual(self.api().maximal_components(m,1,pairs), (pairs,))

    def test_iterative_scc_handles_deep_graph(self):
        n=3000; edges={s: {s+1} if s+1<n else {0} for s in range(n)}
        self.assertEqual(self.api()._strongly_connected(frozenset(edges),edges), (frozenset(edges),))

    def test_all_small_end_components_covered_and_outputs_maximal(self):
        api=self.api(); carrier=((0,0),(0,1),(1,0),(1,1))
        row_options=([1,0],[0,1],['1/2','1/2'])
        checked=0
        for choices in product(row_options, repeat=4):
            m=graph_model([[choices[0],choices[1]],[choices[2],choices[3]]])
            for allowed in subsets(carrier):
                valid=tuple(c for c in subsets(allowed) if end_component(m,0,c))
                maximal=tuple(sorted(c for c in valid if not any(set(c)<set(d) for d in valid)))
                actual=api.maximal_components(m,0,allowed)
                self.assertEqual(actual,maximal,(choices,allowed))
                self.assertTrue(all(any(set(c)<=set(d) for d in actual) for c in valid))
                checked+=1
        self.assertEqual(checked,1296)

    def test_malformed_mode_and_pairs_rejected(self):
        api=self.api(); m=graph_model([[[1]]])
        for theta,pairs in ((False,()),(2,()),(0,((0,0),(0,0))),(0,((True,0),)),(0,((0,1),))):
            with self.subTest(theta=theta,pairs=pairs):
                with self.assertRaises(ValueError): api.maximal_components(m,theta,pairs)
