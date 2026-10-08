from copy import deepcopy
from unittest.mock import patch
from tests.support import BoundaryCase
from tests.fixtures import bernoulli, bernoulli_body, recovery, recovery_body, stale, stale_body, route

class PositiveTests(BoundaryCase):
    def setUp(self):
        self.model=self.module('model'); self.api=self.module('certificates')
    def checked(self, raw, body): return self.api.check_positive(self.model.validate_model(raw),body)
    def test_k_empty_positive_and_zero_length_routes(self):
        result=self.checked(bernoulli(),bernoulli_body())
        self.assertIsInstance(result,self.api.Positive); self.assertEqual(result.K,())
        self.assertEqual(self.checked(bernoulli(),result),result)
    def test_known_recovery_and_final_reveal(self):
        self.assertIsNotNone(self.checked(recovery(),recovery_body()))
    def test_nonempty_internal_route(self):
        self.assertIsNotNone(self.checked(stale(),stale_body()))
    def test_missing_duplicate_extra_and_unsorted_route_keys(self):
        for routes in ((),(route(0,0),route(0,0)),(route(0,0),route(1,0),route(2,0)),(route(1,0),route(0,0))):
            body=bernoulli_body(); body['uncertain_routes']=(routes,body['uncertain_routes'][1])
            with self.subTest(routes=routes): self.assertIsNone(self.checked(bernoulli(),body))
    def test_canonical_sets_required(self):
        for field,value in (('W',(1,0)),('W',(0,0,1)),('W',[0,1]),('D',((1,1),(0,0))),
                            ('D',((0,0),(0,0),(1,0),(1,1))),('K',(False,))):
            body=bernoulli_body();body[field]=value
            with self.subTest(field=field,value=value): self.assertIsNone(self.checked(bernoulli(),body))
    def test_pair_source_and_action_domains(self):
        for pairs in (((2,0),),((0,2),),((False,0),),((0,-1),)):
            body=bernoulli_body();body['D']=pairs
            with self.subTest(pairs=pairs): self.assertIsNone(self.checked(bernoulli(),body))
    def test_omitted_positive_successor_rejected(self):
        body=bernoulli_body();body['W']=(0,)
        body['D']=((0,0),(0,1));body['uncertain_components']=((((0,0),),),(((0,1),),))
        body['uncertain_routes']=((route(0,0),),(route(0,0),))
        self.assertIsNone(self.checked(bernoulli(),body))
    def test_reveal_outside_k_rejected(self):
        body=recovery_body();body['K']=();body['D1']=();body['known_routes']=();body['known_components']=()
        self.assertIsNone(self.checked(recovery(),body))
    def test_wrong_equal_row_rival_and_invalid_component_rejected(self):
        self.assertIsNone(self.checked(bernoulli(equal=True),bernoulli_body()))
        body=bernoulli_body();body['uncertain_components']=((((0,0),),),body['uncertain_components'][1])
        self.assertIsNone(self.checked(bernoulli(),body))
    def test_non_simple_bad_endpoint_and_bad_index_paths(self):
        for changed in (route(0,0,((0,1),(0,0))),route(0,1),route(0,False),route(0,0,((0,2),)),
                        route(0,0,((False,1),)),route(0,0,reveal=(0,1)),route(0)):
            body=stale_body(); body['uncertain_routes']=((changed,route(1,0),route(2,0)),body['uncertain_routes'][1])
            with self.subTest(changed=changed):self.assertIsNone(self.checked(stale(),body))
    def test_zero_probability_internal_edge_and_reveal_rejected(self):
        body=recovery_body();body['uncertain_routes']=((route(0,0,((0,1),)),),body['uncertain_routes'][1])
        self.assertIsNone(self.checked(recovery(),body))
        body=recovery_body();body['uncertain_routes']=(body['uncertain_routes'][0],(route(0,reveal=(0,0)),))
        self.assertIsNone(self.checked(recovery(),body))
    def test_known_components_paths_and_safety_checked(self):
        for mutate in (lambda b:b.__setitem__('known_routes',()),
                       lambda b:b.__setitem__('known_components',()),
                       lambda b:b.__setitem__('D1',((0,0),(1,0))),
                       lambda b:b.__setitem__('known_routes',(route(1,reveal=(0,1)),))):
            body=recovery_body();mutate(body)
            with self.subTest(mutate=mutate):self.assertIsNone(self.checked(recovery(),body))
    def test_exact_fields_and_wrong_types_fail_closed(self):
        for body in (None,[],True,{'success':True},dict(bernoulli_body(),success=True)):
            with self.subTest(body=body):self.assertIsNone(self.checked(bernoulli(),body))
        body=bernoulli_body();body['uncertain_routes'][0][0]['success']=True
        self.assertIsNone(self.checked(bernoulli(),body))
    def test_initial_must_belong_to_w(self):
        body=recovery_body();body['W']=();body['D']=();body['uncertain_components']=((),());body['uncertain_routes']=((),())
        self.assertIsNone(self.checked(recovery(),body))
