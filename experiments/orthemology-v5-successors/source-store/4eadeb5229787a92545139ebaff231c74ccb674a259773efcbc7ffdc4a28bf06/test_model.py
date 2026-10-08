from copy import deepcopy
from dataclasses import FrozenInstanceError
from fractions import Fraction
from tests.support import BoundaryCase
from tests.fixtures import singleton, bernoulli

class ModelTests(BoundaryCase):
    def setUp(self): self.api=self.module('model')
    def invalid(self, mutate):
        raw=bernoulli(); mutate(raw)
        with self.assertRaises(ValueError): self.api.validate_model(raw)
    def test_exact_immutable_normalization(self):
        raw=bernoulli(); m=self.api.validate_model(raw)
        self.assertEqual(m.rows[0][0][0],(Fraction(2,3),Fraction(1,3)))
        raw['menus'][0].clear(); self.assertEqual(m.menus[0],(0,1))
        with self.assertRaises(FrozenInstanceError): m.initial=1
        self.assertEqual(self.api.validate_model(m),m)
    def test_empty_carriers(self):
        for key in ('n_states','n_actions'):
            with self.subTest(key=key): self.invalid(lambda r:r.__setitem__(key,0))
    def test_boolean_dimensions_indices_priorities(self):
        mutations=[lambda r:r.__setitem__('n_states',True),lambda r:r.__setitem__('n_actions',False),
                   lambda r:r.__setitem__('initial',False),lambda r:r['menus'][0].__setitem__(0,False),
                   lambda r:r['priorities'][0][0].__setitem__(0,True),lambda r:r['rows'][0][0][0].__setitem__(0,True)]
        for mut in mutations:
            with self.subTest(mut=mut): self.invalid(mut)
    def test_reject_floats_and_noncanonical_fractions(self):
        for value in (0.5,'2/6','1/0','nan',' 1/3','+1/3','01/3',Fraction(1,3)):
            with self.subTest(value=value): self.invalid(lambda r:r['rows'][0][0][0].__setitem__(0,value))
    def test_negative_nonunit_and_wrong_dimensions(self):
        for mut in (lambda r:r['rows'][0][0][0].__setitem__(0,-1),lambda r:r['rows'][0][0][0].__setitem__(0,1),
                    lambda r:r['rows'][0][0].pop(),lambda r:r['rows'].pop(),lambda r:r['priorities'][1].pop()):
            with self.subTest(mut=mut): self.invalid(mut)
    def test_menu_and_priority_domains(self):
        for mut in (lambda r:r['menus'].__setitem__(0,[]),lambda r:r['menus'].__setitem__(0,[2]),
                    lambda r:r['menus'].__setitem__(0,[1,0]),lambda r:r['menus'].__setitem__(0,[0,0]),
                    lambda r:r['priorities'][0][0].__setitem__(0,-1),lambda r:r.__setitem__('initial',-1)):
            with self.subTest(mut=mut): self.invalid(mut)
    def test_unknown_and_missing_fields(self):
        self.invalid(lambda r:r.__setitem__('success',True)); self.invalid(lambda r:r.pop('rows'))
    def test_unlawful_action_rows_still_validated(self):
        raw=bernoulli(); raw['menus']=[[0],[0]]; raw['rows'][0][0][1]=[0,0]
        with self.assertRaises(ValueError): self.api.validate_model(raw)
