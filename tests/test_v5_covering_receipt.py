"""Synthetic fresh-audit envelopes around exact retained data; no process runs."""
import copy, hashlib, importlib.util, json, os, unittest
from datetime import datetime,timedelta,timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);value=importlib.util.module_from_spec(spec);spec.loader.exec_module(value);return value
def stamp(value):return value.isoformat().replace('+00:00','Z')

class CoveringReceiptTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cc=module('covering_receipt_helper',ROOT/'scripts/v5_covering_continuation.py')
        cls.a=module('covering_receipt_adapter',ROOT/'scripts/replay_v5_successors.py')
        cls.ctx=None

    def fixture(self):
        self.assertTrue(callable(getattr(self.cc,'compose_receipt',None)),'Covering continuation receipt feature has not been implemented')
        path=os.environ.get('V5_COVERING_CONTINUATION_CONTEXT')
        if not path:self.skipTest('Exact private custody context not supplied')
        cls=type(self)
        if cls.ctx is None:
            ctx=json.loads(Path(path).read_text());f=json.loads(Path(ctx['fragment']).read_text());s=json.loads(Path(ctx['suite']).read_text())
            sources={r['id']:r for r in f['sources']};plan=self.a.validate_suite(s,sources,Path(ctx['root']))
            checked=self.cc.read_retained(Path(ctx['prior']),s,sources,Path(ctx['root']),adapter=self.a)
            cls.ctx=(ctx,s,sources,plan,checked)
        ctx,s,sources,plan,checked=cls.ctx
        started=datetime.fromisoformat(checked['collection']['started_at'].replace('Z','+00:00'))-timedelta(seconds=1)
        collected=datetime.fromisoformat(checked['collection']['ended_at'].replace('Z','+00:00'))
        log=''
        for row in plan['targets'].values():
            n=row['name'];log+=f"V5_BEGIN {n}\n{n} : True\n'{n}' does not depend on any axioms\nV5_OWNER {n} {row['module']}\nV5_SAFE {n} 1 []\nV5_END {n}\n"
        raw=log.encode();digest=hashlib.sha256(raw).hexdigest();out='/tmp/COVERING_SYNTHETIC_RECEIPT_FIXTURE_NEVER_EXECUTED'
        pre={'id':'_prerequisites','argv':['{builtin:prerequisites}'],'cwd':'.','budget_seconds':30,'started_at':stamp(started),
             'ended_at':stamp(collected+timedelta(seconds=1)),'terminal':'COMPLETED','exit_code':0,'log_sha256':hashlib.sha256(b'synthetic prerequisites').hexdigest(),'output_hashes':{}}
        audit={'id':'_target_audit','argv':['{tool:lean}','-j1','{out}/generated/V5SuccessorReadback.lean'],'cwd':'.','budget_seconds':300,
               'started_at':stamp(collected+timedelta(seconds=2)),'ended_at':stamp(collected+timedelta(seconds=3)),
               'terminal':'COMPLETED','exit_code':0,'log_sha256':digest,'output_hashes':{}}
        pins=self.cc.data(self.a)
        fresh={'started_at':pre['started_at'],'ended_at':stamp(collected+timedelta(seconds=4)),'stage_results':[pre,audit],
               'audit_log_hex':raw.hex(),'audit_source_hex':self.a._audit_source(list(plan['targets'].values())).encode().hex(),
               'resolved_invocation':{'argv':[ctx['tools']['lean'],'-j1',out+'/generated/V5SuccessorReadback.lean'],'cwd':ctx['prior']+'/project',
                  'timeout_seconds':300,'lean_path':self.cc.expected_lean_path(checked['prior']['receipt'],plan,adapter=self.a),
                  'generated_source_sha256':pins['audit_source_sha256'],'scope':'ONE_COVERING_TARGET_AUDIT_NO_SOURCE_REPLAY'},
               'official_cache_measurements':pins['official_cache_measurements'],'retained_before':checked['inventory'],
               'retained_after':checked['inventory'],'objects_before':checked['all_objects'],'objects_after':checked['all_objects']}
        receipt=self.cc.compose_receipt(checked,s,plan,fresh,adapter=self.a)
        return ctx,s,sources,plan,checked,fresh,receipt

    def check(self,receipt,sources,suite,root):return self.cc.validate_receipt(receipt,suite,sources,Path(root),adapter=self.a)

    def test_complete_synthetic_envelope_preserves_prior_and_has_only_one_new_audit(self):
        ctx,s,sources,plan,checked,fresh,r=self.fixture();self.check(r,sources,s,ctx['root'])
        self.assertEqual(r['proof_scope'],'DECLARED_SUITE');self.assertEqual(len(r['target_readbacks']),4)
        self.assertEqual(len(r['controls']),13);self.assertEqual(r['replay_evidence']['prior'],checked['prior'])
        self.assertEqual([x['id']for x in r['stages']],['_prerequisites','_target_audit'])
        self.assertEqual(r['replay_evidence']['accounting']['new_source_owned_physical_runs'],0)
        self.assertEqual(r['replay_evidence']['accounting']['new_child_compilations'],0)
        self.assertEqual(r['replay_evidence']['accounting']['new_independent_evidence'],0)

    def test_changed_embedded_prior_raw_failure_or_value_is_rejected(self):
        ctx,s,sources,plan,checked,fresh,r=self.fixture()
        for change in [lambda x:x['replay_evidence']['prior']['receipt'].update(outcome='QUALIFIED_DECLARED_SUITE'),
                       lambda x:x['replay_evidence']['prior'].update(receipt_raw_hex='00'),
                       lambda x:x['replay_evidence']['prior'].update(failure_raw_hex='00')]:
            value=copy.deepcopy(r);change(value)
            with self.assertRaises(ValueError):self.check(value,sources,s,ctx['root'])

    def test_unreviewed_executor_helper_or_data_is_rejected(self):
        ctx,s,sources,plan,checked,fresh,r=self.fixture()
        for key in ['runner_sha256','helper_sha256','data_sha256']:
            value=copy.deepcopy(r);value['replay_evidence'][key]='0'*64
            with self.assertRaises(ValueError):self.check(value,sources,s,ctx['root'])

    def test_boolean_exit_cannot_replace_the_actual_integer_terminal(self):
        ctx,s,sources,plan,checked,fresh,r=self.fixture()
        value=copy.deepcopy(r);value['exit_code']=False
        with self.assertRaises(ValueError):self.check(value,sources,s,ctx['root'])
        value=copy.deepcopy(r);value['replay_evidence']['retained_collection']['stage_results'][0]['exit_code']=False
        with self.assertRaises(ValueError):self.check(value,sources,s,ctx['root'])

    def test_foreign_or_missing_cache_and_changed_objects_are_rejected(self):
        ctx,s,sources,plan,checked,fresh,r=self.fixture()
        changes=[lambda x:x['replay_evidence']['retained_input_checks']['official_cache_measurements'].pop(),
                 lambda x:x['replay_evidence']['retained_input_checks']['official_cache_measurements'][0].update(file_count=1),
                 lambda x:x['replay_evidence']['retained_input_checks']['objects_after'].pop(next(iter(x['replay_evidence']['retained_input_checks']['objects_after']))),
                 lambda x:x['replay_evidence']['retained_input_checks']['retained_after'].update(tree_sha256='0'*64)]
        for change in changes:
            value=copy.deepcopy(r);change(value)
            with self.assertRaises(ValueError):self.check(value,sources,s,ctx['root'])

    def test_audit_cwd_import_path_flags_and_source_are_bound(self):
        ctx,s,sources,plan,checked,fresh,r=self.fixture()
        changes=[lambda x:x['replay_evidence']['fresh_audit']['resolved_invocation'].update(cwd='/tmp/foreign'),
                 lambda x:x['replay_evidence']['fresh_audit']['resolved_invocation']['lean_path'].append('/tmp/foreign'),
                 lambda x:x['replay_evidence']['fresh_audit']['resolved_invocation']['argv'].insert(1,'-o'),
                 lambda x:x['replay_evidence']['fresh_audit'].update(audit_source_hex=b'theorem fake : True := by trivial'.hex())]
        for change in changes:
            value=copy.deepcopy(r);change(value)
            with self.assertRaises(ValueError):self.check(value,sources,s,ctx['root'])

    def test_readback_type_axiom_owner_and_terminal_associations_cannot_drift(self):
        ctx,s,sources,plan,checked,fresh,r=self.fixture()
        changes=[lambda x:x['replay_evidence']['target_audits'][0].update(type_sha256='0'*64),
                 lambda x:x['replay_evidence']['target_audits'][0].update(axioms=['sorryAx']),
                 lambda x:x['replay_evidence']['target_audits'][0].update(name='Different.target'),
                 lambda x:x['replay_evidence']['stage_results'][-1].update(exit_code=1)]
        for change in changes:
            value=copy.deepcopy(r);change(value)
            with self.assertRaises(ValueError):self.check(value,sources,s,ctx['root'])

    def test_reused_or_reversed_new_audit_intervals_are_rejected(self):
        ctx,s,sources,plan,checked,fresh,r=self.fixture()
        value=copy.deepcopy(r);value['started_at']=checked['prior']['receipt']['started_at']
        with self.assertRaises(ValueError):self.check(value,sources,s,ctx['root'])
        value=copy.deepcopy(r);value['replay_evidence']['stage_results'][-1]['ended_at']=value['started_at']
        with self.assertRaises(ValueError):self.check(value,sources,s,ctx['root'])

    def test_resource_terminal_preserves_old_controls_without_new_proof_credit(self):
        ctx,s,sources,plan,checked,fresh,r=self.fixture()
        fresh=copy.deepcopy(fresh);fresh['stage_results'][-1].update(terminal='TIMEOUT',exit_code=None,log_sha256=hashlib.sha256(b'').hexdigest());fresh['audit_log_hex']=''
        value=self.cc.compose_receipt(checked,s,plan,fresh,adapter=self.a);self.check(value,sources,s,ctx['root'])
        self.assertEqual(value['outcome'],'RESOURCE_INCONCLUSIVE');self.assertEqual(value['proof_scope'],'NONE')
        self.assertEqual(value['target_readbacks'],[]);self.assertEqual(value['replay_evidence']['target_audits'],[])
        self.assertIsNone(value['stages'][-1]['exit_code']);self.assertEqual(value['replay_evidence']['prior']['receipt']['outcome'],'FAILED')

    def test_failed_new_audit_is_not_a_semantic_rejection_control(self):
        ctx,s,sources,plan,checked,fresh,r=self.fixture();fresh=copy.deepcopy(fresh);raw=b'error: missing target'
        fresh['stage_results'][-1].update(terminal='COMPLETED',exit_code=1,log_sha256=hashlib.sha256(raw).hexdigest());fresh['audit_log_hex']=raw.hex()
        value=self.cc.compose_receipt(checked,s,plan,fresh,adapter=self.a);self.check(value,sources,s,ctx['root'])
        self.assertEqual(value['outcome'],'FAILED');self.assertEqual(value['proof_scope'],'NONE')
        self.assertEqual(len(value['controls']),13);self.assertNotIn('_target_audit',[x['id']for x in value['controls']])

    def test_extra_fresh_stage_or_invented_execution_accounting_is_rejected(self):
        ctx,s,sources,plan,checked,fresh,r=self.fixture()
        value=copy.deepcopy(r);value['replay_evidence']['stage_results'].append(copy.deepcopy(value['replay_evidence']['stage_results'][-1]))
        with self.assertRaises(ValueError):self.check(value,sources,s,ctx['root'])
        value=copy.deepcopy(r);value['replay_evidence']['accounting']['new_source_owned_physical_runs']=1
        with self.assertRaises(ValueError):self.check(value,sources,s,ctx['root'])


    def test_executor_compatibility_admits_only_reviewed_predecessor_without_asset_changes(self):
        from unittest.mock import patch
        ctx,s,sources,plan,checked,fresh,r=self.fixture()
        previous=hashlib.sha256(b'reviewed synthetic covering executor').hexdigest()
        r['replay_evidence']['runner_sha256']=previous
        r['replay_evidence']['retained_collection']['collector_runner_sha256']=previous
        helper=ROOT/'scripts/v5_covering_continuation.py';data=helper.with_suffix('.json')
        before=(helper.read_bytes(),data.read_bytes(),(Path(ctx['prior'])/'RECEIPT.json').read_bytes())
        with patch.object(self.a,'COVERING_REVIEWED_EXECUTOR_HASHES',frozenset({previous}),create=True):
            accepted=self.a.validate_receipt(r,s,sources,Path(ctx['root']))
        self.assertEqual(accepted['proof_scope'],'DECLARED_SUITE')
        self.assertEqual(accepted['replay_evidence']['prior']['receipt']['outcome'],'FAILED')
        self.assertEqual(before,(helper.read_bytes(),data.read_bytes(),(Path(ctx['prior'])/'RECEIPT.json').read_bytes()))

    def test_executor_compatibility_refuses_random_runner_and_random_collector(self):
        from unittest.mock import patch
        ctx,s,sources,plan,checked,fresh,r=self.fixture()
        previous=hashlib.sha256(b'reviewed synthetic covering executor').hexdigest()
        r['replay_evidence']['runner_sha256']=previous
        r['replay_evidence']['retained_collection']['collector_runner_sha256']=previous
        with patch.object(self.a,'COVERING_REVIEWED_EXECUTOR_HASHES',frozenset({previous}),create=True):
            for field in ['runner','collector']:
                value=copy.deepcopy(r)
                if field=='runner':value['replay_evidence']['runner_sha256']='f'*64
                else:value['replay_evidence']['retained_collection']['collector_runner_sha256']='f'*64
                with self.subTest(field=field),self.assertRaises(ValueError):
                    self.a.validate_receipt(value,s,sources,Path(ctx['root']))

    def test_executor_compatibility_never_promotes_original_failed_runner(self):
        from unittest.mock import patch
        ctx,s,sources,plan,checked,fresh,r=self.fixture()
        previous=self.cc.data(self.a)['original_runner_sha256']
        r['replay_evidence']['runner_sha256']=previous
        r['replay_evidence']['retained_collection']['collector_runner_sha256']=previous
        with patch.object(self.a,'COVERING_REVIEWED_EXECUTOR_HASHES',frozenset({previous}),create=True),self.assertRaises(ValueError):
            self.a.validate_receipt(r,s,sources,Path(ctx['root']))

    def test_executor_compatibility_cannot_override_helper_data_or_schema_gates(self):
        from unittest.mock import patch
        ctx,s,sources,plan,checked,fresh,r=self.fixture()
        previous=hashlib.sha256(b'reviewed synthetic covering executor').hexdigest()
        r['replay_evidence']['runner_sha256']=previous
        r['replay_evidence']['retained_collection']['collector_runner_sha256']=previous
        with patch.object(self.a,'COVERING_REVIEWED_EXECUTOR_HASHES',frozenset({previous}),create=True):
            for field in ['helper_sha256','data_sha256','COVERING_REVIEWED_EXECUTOR_HASHES']:
                value=copy.deepcopy(r);value['replay_evidence'][field]='0'*64
                with self.subTest(field=field),self.assertRaises(ValueError):
                    self.a.validate_receipt(value,s,sources,Path(ctx['root']))

if __name__=='__main__':unittest.main(verbosity=2)
