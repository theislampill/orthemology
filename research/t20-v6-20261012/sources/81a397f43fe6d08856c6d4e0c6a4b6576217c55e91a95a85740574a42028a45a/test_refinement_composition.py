from copy import deepcopy
from fractions import Fraction as F
import unittest
from stochastic_refinement import verify_refinement
from test_private_refinement import private_fixture
from refinement_composition import compose_refinements,glue_couplings


def chain():
    second=private_fixture()
    # Second interface only needs the constant middle observation, so its mode
    # does not change. Both hidden middle states relate to the singleton target.
    second.source_obs={0:'o',1:'o'}
    second.relation={(0,'y',0),(1,'y',0)}
    second.reconstruct={(0,'o'):'o'}
    second.abstract_actions={(0,'o'):(0,1)}
    second.translate={(0,'o',a):'tick' for a in (0,1)}
    second.update={(0,'o',a,'tick','o'):0 for a in (0,1)}
    first=deepcopy(second)
    first.source_obs={0:0,1:1};first.destination_obs={0:'o',1:'o'}
    first.relation={(0,0,0),(1,1,1)}
    first.destination_kernels=deepcopy(second.source_kernels)
    first.reconstruct={(q,'o'):q for q in (0,1)}
    first.abstract_actions={(q,'o'):(0,1) for q in (0,1)}
    first.translate={(q,'o',a):a for q in (0,1) for a in (0,1)}
    first.update={(q,'o',a,a,'o'):a for q in (0,1) for a in (0,1)}
    first.destination_eligible=set(second.source_eligible)
    first.destination_warrant={(q,'o',a) for q in (0,1) for a in (0,1)}
    first.destination_safe={0,1};first.destination_initial={0:F(1)}
    return first,second


class RefinementCompositionTests(unittest.TestCase):
    def test_private_product_composes_two_public_interfaces(self):
        first,second=chain()
        self.assertTrue(verify_refinement(first)['valid'])
        self.assertTrue(verify_refinement(second)['valid'])
        composite,projection=compose_refinements(first,second)
        self.assertFalse(verify_refinement(composite)['valid'])
        self.assertTrue(verify_refinement(composite,projection)['valid'])

    def test_middle_plant_identity_is_checked(self):
        first,second=chain();second.source_initial={1:F(1)}
        with self.assertRaises(ValueError):compose_refinements(first,second)

    def test_exact_three_way_gluing(self):
        left={('a','m'):F(1,3),('b','m'):F(1,6),('b','n'):F(1,2)}
        right={('m','x'):F(1,4),('m','y'):F(1,4),('n','y'):F(1,2)}
        joint=glue_couplings(left,right)
        self.assertEqual(joint,{('a','x'):F(1,6),('a','y'):F(1,6),
                                ('b','x'):F(1,12),('b','y'):F(7,12)})
        right[('m','x')]=F(1,3)
        with self.assertRaises(ValueError):glue_couplings(left,right)

if __name__=='__main__':unittest.main()
