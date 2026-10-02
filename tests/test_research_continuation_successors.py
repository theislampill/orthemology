"""Successor intake must preserve predecessor evidence and scoped claim limits."""
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import validate_research_continuations as v
from test_research_continuations import fixture, AREA, PROV, put


class SuccessorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.data = fixture(self.root)

    def fixture(self):
        import validate_continuation_successor as s
        self.s = s
        old = self.data[AREA+'/registry.json']['results'][0]
        old_status = self.data[PROV+'/RESULT_STATUS.json']['results'][0]
        results = {old['id']:old}
        statuses = {old['id']:old_status}
        for name in s.NEW_RESULT_IDS:
            results[name] = dict(old, id=name)
            statuses[name] = dict(old_status, id=name)
        sources = v.indexed(self.data[PROV+'/SOURCE_MAP.json']['sources'], 'id')
        self.results, self.statuses, self.sources = results, statuses, sources
        self.overlay = {
            'schema':'orthemology-v5-sixth-final-overlay-v1',
            'predecessor':{'commit':'1'*40, 'tree':'2'*40, 'registry_sha256':'a'*64,
                           'verification_sha256':'b'*64},
            'inputs':[{'name':n, 'sha256':'c'*64, 'bytes':1} for n in s.INPUT_NAMES],
            'report_bindings':[{'id':n, 'source_id':'source-a',
                               'sha256':sources['source-a']['original_sha256'],
                               'role':'SUPPORT' if n.startswith('support-') else 'REPORT'}
                              for n in s.REPORT_IDS],
            'prior_results':[{'id':old['id'], 'statement_sha256':v.statement_digest(old),
                              'status_sha256':s.record_digest(old_status), 'successors':['S6F-19']}],
            'new_results':list(s.NEW_RESULT_IDS),
            'claim_contracts':[{'id':n, 'contract':deepcopy(c), 'review_source_ids':['source-a']}
                               for n,c in s.CLAIM_CONTRACTS.items()],
            'current_selections':[{'prior_result':old['id'], 'successor':'S6F-19',
                                   'scope':'The actual chronological count only.',
                                   'relation':'SCOPED_SUCCESSOR', 'review_source_ids':['source-a']}],
            'checks':[], 'check_bindings':[],
            'result_checks':[{'id':n,'check_ids':[]} for n in s.NEW_RESULT_IDS],
            'research_avenues':[{'id':n,'result_ids':['S6F-26'],
                                'disposition':'PRESERVED_WITH_SCOPED_CONTINUATION',
                                'residual':'No global closure.'} for n in range(1,13)]}

    def validate(self):
        self.s.validate_overlay(self.overlay,self.results,self.statuses,self.sources,self.root)

    def test_valid_overlay_does_not_promote_previous_status(self):
        self.fixture(); before=deepcopy(self.statuses);self.validate()
        self.assertEqual(before,self.statuses)

    def test_cannot_delete_prior_result(self):
        self.fixture();del self.results['T5-EXAMPLE']
        with self.assertRaises(ValueError):self.validate()

    def test_cannot_rewrite_historical_conditional_claim(self):
        self.fixture();self.results['T5-EXAMPLE']['claim']='An unconditional result.'
        with self.assertRaises(ValueError):self.validate()

    def test_cannot_rewrite_prior_evidence_status(self):
        self.fixture();self.statuses['T5-EXAMPLE']['fresh']='QUALIFIED'
        with self.assertRaises(ValueError):self.validate()

    def test_missing_or_duplicate_report_binding_is_rejected(self):
        self.fixture();self.overlay['report_bindings'].pop()
        with self.assertRaises(ValueError):self.validate()
        self.fixture();self.overlay['report_bindings'].append(deepcopy(self.overlay['report_bindings'][0]))
        with self.assertRaises(ValueError):self.validate()

    def test_report_binding_needs_exact_original_source(self):
        self.fixture();self.overlay['report_bindings'][0]['sha256']='0'*64
        with self.assertRaises(ValueError):self.validate()

    def test_scoped_successor_requires_matching_prior_crosswalk(self):
        self.fixture();self.overlay['current_selections'][0]['successor']='S6F-22'
        with self.assertRaises(ValueError):self.validate()

    def test_contracts_reject_foundation_and_runtime_overclaims(self):
        self.fixture()
        for row in self.overlay['claim_contracts']:
            for key,value in list(row['contract'].items()):
                row['contract'][key]=not value if isinstance(value,bool) else 'UNRESTRICTED'
                with self.subTest(scope=row['id'],field=key),self.assertRaises(ValueError):self.validate()
                row['contract'][key]=value

    def test_seventh_is_not_a_completed_research_avenue(self):
        self.fixture();self.overlay['research_avenues'].append({'id':13,'result_ids':['S6F-26'],
            'disposition':'COMPLETE','residual':'None'})
        with self.assertRaises(ValueError):self.validate()

    def test_native_terminal_cannot_be_boolean_or_timeout(self):
        self.fixture();h=self.sources['source-a']['original_sha256']
        check={'id':'finite-control','kind':'FINITE_CONTROL','source_ids':['source-a'],
               'source_hashes':{'source-a':h},'driver_source_ids':['source-a'],
               'driver_hashes':{'source-a':h},'command_sha256':'d'*64,
               'receipt_sha256':'e'*64,'log_sha256':'f'*64,
               'terminal':'EXIT','exit_code':0,'status':'PASS',
               'scope':'Finite controls only.','outcomes':[], 'result_ids':['S6F-01'],
               'kernel_receipts':{}, 'execution':'PUBLIC_EXACT_FINITE_DRIVER',
               'execution_driver_sha256':'1'*64}
        self.overlay['checks']=[check]
        self.overlay['check_bindings']=[{'id':check['id'],'subject_sha256':self.s.check_subject_digest(check),
                                        'outcomes_sha256':self.s.record_digest(check['outcomes'])}]
        self.overlay['result_checks'][0]['check_ids']=['finite-control']
        self.validate()
        for field,value in [('exit_code',False),('terminal','TIMEOUT'),('exit_code',2),('source_hashes',{})]:
            original=check[field];check[field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):self.validate()
            check[field]=original

    def test_control_association_cannot_be_reassigned_or_lose_its_binding(self):
        self.test_native_terminal_cannot_be_boolean_or_timeout()
        check=self.overlay['checks'][0]
        check['result_ids']=['S6F-22']
        self.overlay['result_checks'][0]['check_ids']=[]
        self.overlay['result_checks'][21]['check_ids']=[check['id']]
        with self.assertRaises(ValueError):self.validate()
        check['result_ids']=['S6F-01']
        self.overlay['result_checks'][0]['check_ids']=[check['id']]
        self.overlay['result_checks'][21]['check_ids']=[]
        self.overlay['check_bindings']=[]
        with self.assertRaises(ValueError):self.validate()

    def test_semantic_control_needs_qualified_kernel_dependency(self):
        self.test_native_terminal_cannot_be_boolean_or_timeout()
        check=self.overlay['checks'][0];check['kind']='SOURCE_MUTATION'
        check['outcomes']=[{'id':'positive','status':'PASS','exit_code':0,'diagnostic_sha256':'d'*64}]
        self.overlay['check_bindings'][0]['subject_sha256']=self.s.check_subject_digest(check)
        self.overlay['check_bindings'][0]['outcomes_sha256']=self.s.record_digest(check['outcomes'])
        with self.assertRaisesRegex(ValueError,'[Kk]ernel'):self.validate()

    def test_timeout_mutation_is_never_concrete_rejection(self):
        self.fixture()
        for code in [None, False, True, 0, 2, 124, 137, 143, -9, -15]:
            with self.subTest(exit_code=code),self.assertRaises(ValueError):
                self.s.validate_outcome({'id':'mutation','status':'REJECTED_CONCRETE',
                    'exit_code':code,'diagnostic_sha256':'d'*64})
        self.s.validate_outcome({'id':'mutation','status':'REJECTED_CONCRETE',
            'exit_code':1,'diagnostic_sha256':'d'*64})
        self.s.validate_outcome({'id':'mutation','status':'INCONCLUSIVE',
            'exit_code':None,'diagnostic_sha256':'d'*64})
        self.s.validate_outcome({'id':'heartbeat','status':'INCONCLUSIVE',
            'exit_code':1,'diagnostic_sha256':'d'*64})

    def test_overlay_is_required_for_the_final_cutoff(self):
        self.data[AREA+'/registry.json']['cutoff']='sixth-tranche-final'
        for name,value in self.data.items():put(self.root,name,value)
        with self.assertRaises(ValueError):v.validate(self.root)


class ActualOutcomeBindingTests(unittest.TestCase):
    """Keep the reviewed semantic inventory and classifications in real data."""
    @classmethod
    def setUpClass(cls):
        cls.root=Path(__file__).resolve().parents[1]
        cls.path=cls.root/PROV/'SIXTH_FINAL_OVERLAY.json'
        cls.overlay=v.read_json(cls.path)

    def validate_override(self, overlay):
        original=v.read_json
        def read(path):
            return deepcopy(overlay) if Path(path)==self.path else original(path)
        with patch.object(v,'read_json',side_effect=read):v.validate(self.root)

    def test_current_reviewed_outcomes_are_valid(self):
        self.validate_override(self.overlay)

    def test_resource_diagnostics_cannot_be_relabeled_as_rejection(self):
        overlay=deepcopy(self.overlay);changed=0
        for check in overlay['checks']:
            if check['kind']!='SOURCE_MUTATION':continue
            for outcome in check['outcomes']:
                if outcome['status']=='INCONCLUSIVE':
                    outcome['status']='REJECTED_CONCRETE';changed+=1
            check['status']='PASS'
        self.assertGreater(changed,0)
        with self.assertRaisesRegex(ValueError,'[Oo]utcome'):
            self.validate_override(overlay)

    def test_all_semantic_outcomes_cannot_disappear(self):
        overlay=deepcopy(self.overlay)
        for check in overlay['checks']:
            if check['kind']=='SOURCE_MUTATION':
                self.assertTrue(check['outcomes'])
                check['outcomes']=[];check['status']='PASS'
        with self.assertRaisesRegex(ValueError,'[Oo]utcome'):
            self.validate_override(overlay)

    def test_a_single_attempt_cannot_disappear(self):
        overlay=deepcopy(self.overlay)
        check=next(c for c in overlay['checks'] if c['id']=='semantic-cost')
        check['outcomes'].pop()
        with self.assertRaisesRegex(ValueError,'[Oo]utcome'):
            self.validate_override(overlay)

    def test_diagnostic_identity_cannot_be_substituted(self):
        overlay=deepcopy(self.overlay)
        check=next(c for c in overlay['checks'] if c['id']=='semantic-runtime')
        check['outcomes'][0]['diagnostic_sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'[Oo]utcome'):
            self.validate_override(overlay)


if __name__=='__main__':unittest.main()
