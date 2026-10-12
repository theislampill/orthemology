from fractions import Fraction as F
import unittest
from stochastic_refinement import Refinement,verify_refinement


def private_fixture():
    # Source observation records its last private virtual action. The destination
    # executes only 'tick'; the controller can remember the virtual action, while
    # a public observer cannot read it from the physical trace.
    return Refinement(source_obs={0:0,1:1},destination_obs={'y':'o'},
        relation={(0,'y',0),(1,'y',1)},
        source_kernels={(x,a):({a:F(1)},) for x in (0,1) for a in (0,1)},
        destination_kernels={('y','tick'):({'y':F(1)},)},
        reconstruct={(q,'o'):q for q in (0,1)},
        abstract_actions={(q,'o'):(0,1) for q in (0,1)},
        translate={(q,'o',a):'tick' for q in (0,1) for a in (0,1)},
        update={(q,'o',a,'tick','o'):a for q in (0,1) for a in (0,1)},
        source_eligible={(x,a) for x in (0,1) for a in (0,1)},
        destination_eligible={('y','tick')},destination_warrant={(0,'o','tick')},
        source_bad=set(),destination_bad=set(),source_safe={0,1},destination_safe={'y'},
        source_initial={0:F(1)},destination_initial={'y':F(1)},initial_mode={'o':0})


class PrivateRefinementTests(unittest.TestCase):
    def test_private_memory_with_separate_public_warrant(self):
        c=private_fixture()
        self.assertFalse(verify_refinement(c)['valid'])
        r=verify_refinement(c,public_projection={0:0,1:0})
        self.assertTrue(r['valid'],r['violations'])
        self.assertEqual(len(r['step_couplings']),4)

    def test_declaring_private_memory_public_is_rejected(self):
        c=private_fixture();c.destination_warrant.add((1,'o','tick'))
        r=verify_refinement(c,public_projection={0:0,1:1})
        self.assertFalse(r['valid'])
        self.assertTrue(any(v[0]=='nonpublic_mode_update' for v in r['violations']))

    def test_public_projection_must_cover_updated_modes(self):
        r=verify_refinement(private_fixture(),public_projection={0:0})
        self.assertFalse(r['valid'])
        self.assertTrue(any(v[0]=='missing_public_projection' for v in r['violations']))

if __name__=='__main__':unittest.main()
