from fractions import Fraction as F
from copy import deepcopy
import unittest
from stochastic_refinement import Refinement, verify_refinement


def fixture():
    src={('b','step'):({'b':F(1,2),'g0':F(1,4),'g1':F(1,4)},),
         ('g0','step'):({'g0':F(1)},),('g1','step'):({'g1':F(1)},),
         ('b','hold'):({'b':F(1)},),('g0','hold'):({'g0':F(1)},),('g1','hold'):({'g1':F(1)},)}
    dst={('B','do'):({'B':F(1,2),'G':F(1,2)},),('G','do'):({'G':F(1)},),
         ('B','wait'):({'B':F(1)},),('G','wait'):({'G':F(1)},)}
    obsA={'b':'bad','g0':'good','g1':'good'};obsB={'B':'unclear','G':'landed'}
    return Refinement(source_obs=obsA,destination_obs=obsB,
        relation={('b','B',0),('g0','G',0),('g1','G',0)},
        source_kernels=src,destination_kernels=dst,
        reconstruct={(0,'unclear'):'bad',(0,'landed'):'good'},
        abstract_actions={(0,o):('step','hold') for o in obsB.values()},
        translate={(0,o,a):('do' if a=='step' else 'wait') for o in obsB.values() for a in ('step','hold')},
        update={(0,o,a,b,no):0 for o in obsB.values() for a,b in (('step','do'),('hold','wait')) for no in obsB.values()},
        source_eligible=set(src),destination_eligible=set(dst),
        destination_warrant={(0,o,b) for o in obsB.values() for b in ('do','wait')},
        source_bad={'b'},destination_bad={'B'},source_safe=set(obsA),destination_safe=set(obsB),
        source_initial={'b':F(1)},destination_initial={'B':F(1)},initial_mode={'unclear':0,'landed':0})


class StochasticRefinementTests(unittest.TestCase):
    def test_many_to_one_observation_compatible_contract(self):
        result=verify_refinement(fixture())
        self.assertTrue(result['valid'],result['violations'])
        self.assertEqual(len(result['step_couplings']),6)

    def test_full_destination_mass_cannot_be_conditioned_away(self):
        c=fixture();c.destination_kernels['B','do']=({'B':F(1)},)
        result=verify_refinement(c)
        self.assertFalse(result['valid'])
        self.assertTrue(any(v[0]=='no_full_kernel_coupling' for v in result['violations']))

    def test_hidden_source_observation_cannot_be_reconstructed_by_oracle(self):
        c=fixture();c.source_obs['g1']='different_good'
        result=verify_refinement(c)
        self.assertFalse(result['valid'])
        self.assertIn(('observation_incompatibility','g1','G',0),result['violations'])

    def test_destination_permission_is_separate_from_coupling(self):
        c=fixture();c.destination_warrant.remove((0,'unclear','do'))
        result=verify_refinement(c)
        self.assertFalse(result['valid'])
        self.assertIn(('destination_warrant',0,'unclear','do'),result['violations'])

    def test_every_adversarial_destination_kernel_needs_a_match(self):
        c=fixture();c.destination_kernels['B','do']+=({'B':F(2,3),'G':F(1,3)},)
        result=verify_refinement(c)
        self.assertFalse(result['valid'])
        c.source_kernels['b','step']+=({'b':F(2,3),'g0':F(1,6),'g1':F(1,6)},)
        self.assertTrue(verify_refinement(c)['valid'])

    def test_initial_coupling_covers_all_destination_mass(self):
        c=fixture();c.destination_initial={'B':F(1,2),'G':F(1,2)}
        result=verify_refinement(c)
        self.assertFalse(result['valid'])
        self.assertIn(('initial_coupling_absent',),result['violations'])

    def test_transducer_mode_must_be_publicly_reconstructible(self):
        c=fixture()
        # Add a second source action with exactly the same plant kernel and the
        # same executed destination action. Its virtual identity is private.
        for x in c.source_obs:
            c.source_kernels[x,'alias']=c.source_kernels[x,'step']
            c.source_eligible.add((x,'alias'))
        c.relation |= {(x,y,1) for x,y,z in c.relation}
        for z in (0,1):
            for o in c.destination_obs.values():
                c.reconstruct[z,o]=c.reconstruct[0,o]
                c.abstract_actions[z,o]=('step','alias','hold')
                for a,b in (('step','do'),('alias','do'),('hold','wait')):
                    c.translate[z,o,a]=b
                    c.destination_warrant.add((z,o,b))
                    for no in c.destination_obs.values():
                        c.update[z,o,a,b,no]=int(a=='alias')
        result=verify_refinement(c)
        self.assertFalse(result['valid'])
        self.assertTrue(any(v[0]=='nonpublic_mode_update' for v in result['violations']))
        for key in c.update:c.update[key]=0
        self.assertTrue(verify_refinement(c)['valid'])

    def test_probability_inputs_are_exact_and_not_boolean(self):
        for value in (1.0, True):
            c=fixture();c.source_initial={'b':value}
            self.assertFalse(verify_refinement(c)['valid'])

if __name__=='__main__':unittest.main()
