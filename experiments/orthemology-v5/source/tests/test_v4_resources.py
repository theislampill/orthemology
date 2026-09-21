import unittest
from unittest.mock import patch
import operational as o
import reference as r
from boundaries import Rejection, bound_tree

class OperationResourceTests(unittest.TestCase):
    def test_intermediate_overflow_cannot_be_erased(self):
        e=o.Engine.standard();c=e.admit({'op':'compose','first':{'op':'primitive','name':'succ'},'second':{'op':'primitive','name':'iszero'}})
        with self.assertRaises(Rejection):e.dispatch(c,(1<<256)-1)
    def test_projection_has_bounded_pages(self):
        e=o.Engine.standard()
        for _ in range(4):e.admit({'op':'id','type':'nat'})
        self.assertEqual(len(e.project(limit=2,offset=1)),2)
        for n in [True,-1,0,10000]:
            with self.assertRaises(Rejection):e.project(limit=n)
    def test_refinement_and_requirement_host_inputs(self):
        e=o.Engine.standard()
        for name in [None,{},[],True]:
            with self.assertRaises(Rejection):e.refine_probability_observation(name,{})
            with self.assertRaises(Rejection):e.require_probability('primitive:succ',name,[0,1])
    def test_substitution_stops_before_full_oversized_construction(self):
        body=('v',0);arg=('bottom',)
        for _ in range(8):body=('arr',body,body);arg=('arr',arg,arg)
        with patch.object(r,'shift_type',wraps=r.shift_type) as count:
            with self.assertRaises(Rejection):r.instantiate_type(body,arg)
            self.assertLessEqual(count.call_count,r.MAX_NODES//bound_tree(arg)+1)

if __name__=='__main__':unittest.main()
