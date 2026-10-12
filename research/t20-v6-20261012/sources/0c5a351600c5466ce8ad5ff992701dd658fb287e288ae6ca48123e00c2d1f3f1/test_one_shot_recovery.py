"""New adversarial tests for recovered iterator-consumption defect pointers.

These are reconstruction tests written against an unchanged copy of the
provisional synthesis, not claims of recovered interrupted-session source.
"""
import unittest
from fractions import Fraction as F
from contracts import Contract,valid_partition,closure_basis,as_reaches

class IteratorReplay(unittest.TestCase):
    def test_contract_consumes_kernel_row_once(self):
        args=(('x',),('a',),('o',),{'x':'L'},{'x':('a',)},{('x','a'):F(0)})
        row=(('o','x',F(1)),)
        self.assertEqual(Contract(*args,{('x','a'):iter(row)}).kernels['x','a'],row)

    def test_partition_checks_all_blocks_with_one_shot_iterator(self):
        c=Contract(('x','y'),('a',),('o',),{'x':'A','y':'B'},
          {'x':('a',),'y':('a',)}, {('x','a'):F(0),('y','a'):F(0)},
          {('x','a'):(('o','x',F(1)),),('y','a'):(('o','y',F(1)),)})
        self.assertFalse(valid_partition(c,iter((('x','y'),))))

    def test_reachability_keeps_one_shot_target_membership(self):
        c=Contract(('x','done'),('a',),('o',),{'x':'x','done':'done'},
          {'x':('a',),'done':('a',)}, {('x','a'):F(0),('done','a'):F(0)},
          {('x','a'):(('o','done',F(1)),),('done','a'):(('o','done',F(1)),)})
        self.assertTrue(as_reaches(c,'x',iter(('done',)),{'x':'a','done':'a'}))

    def test_closure_processes_generator_of_allowed_updates(self):
        a=((F(1),F(1)),(F(0),F(1)))
        basis=((F(1),F(0)),)
        self.assertEqual(len(closure_basis(basis,iter((a,)))[0]),2)
        self.assertEqual(len(closure_basis(basis,(a,))[0]),2)

if __name__=='__main__': unittest.main()
