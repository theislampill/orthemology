"""Covering continuation gates; no Lean, original driver, or audit is executed."""
import copy, hashlib, importlib.util, json, os, tempfile, unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
CONTEXT = os.environ.get('V5_COVERING_CONTINUATION_CONTEXT')

def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module); return module

def hash_bytes(raw): return hashlib.sha256(raw).hexdigest()

class CoveringContinuationTests(unittest.TestCase):
    def setUp(self):
        helper = ROOT/'scripts/v5_covering_continuation.py'
        self.assertTrue(helper.is_file(), 'Covering-only continuation feature has not been implemented')
        self.cc = load_module('covering_continuation_under_test', helper)
        self.a = load_module('covering_adapter_under_test', ROOT/'scripts/replay_v5_successors.py')

    def context(self):
        if not CONTEXT: self.skipTest('Exact private retained-run context was not supplied; no scientific run is implied')
        data = json.loads(Path(CONTEXT).read_text())
        fragment = json.loads(Path(data['fragment']).read_text()); suite = json.loads(Path(data['suite']).read_text())
        sources = {r['id']:r for r in fragment['sources']}; reviews = {r['id']:r for r in fragment['reviews']}
        return {'suite':suite, 'sources':sources, 'reviews':reviews, 'root':Path(data['root']), 'prior':Path(data['prior']),
                'tools':data['tools'], 'inputs':data['inputs'], 'plan':self.a.validate_suite(suite,sources,Path(data['root']))}

    def retained(self):
        ctx = self.context()
        checked = self.cc.read_retained(ctx['prior'], ctx['suite'], ctx['sources'], ctx['root'], adapter=self.a)
        return ctx, checked

    def test_exact_inventory_is_read_only(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name); (root/'one').write_bytes(b'one')
            expected = {'one':{'sha256':hash_bytes(b'one'),'bytes':3}}
            self.assertEqual(self.cc.verify_inventory(root,expected,adapter=self.a)['file_count'],1)
            self.assertEqual((root/'one').read_bytes(),b'one')

    def test_changed_missing_extra_and_symlink_inventory_are_rejected(self):
        expected = {'one':{'sha256':hash_bytes(b'one'),'bytes':3}}
        for damage in ['changed','missing','extra','symlink']:
            with self.subTest(damage=damage), tempfile.TemporaryDirectory() as name:
                root=Path(name); (root/'one').write_bytes(b'one')
                if damage=='changed': (root/'one').write_bytes(b'two')
                elif damage=='missing': (root/'one').unlink()
                elif damage=='extra': (root/'extra').write_bytes(b'extra')
                else: (root/'alias').symlink_to(root/'one')
                with self.assertRaises(ValueError): self.cc.verify_inventory(root,expected,adapter=self.a)

    def test_old_receipt_bytes_cannot_be_reserialized_or_relabelled(self):
        ctx=self.context(); raw=(ctx['prior']/'RECEIPT.json').read_bytes(); failure=(ctx['prior']/'FAILURE.json').read_bytes()
        self.assertEqual(self.cc.prior_value(raw,failure,ctx['suite'],ctx['sources'],ctx['root'],adapter=self.a)['receipt']['outcome'],'FAILED')
        for altered in [raw+b' ', json.dumps(json.loads(raw),separators=(',',':')).encode(),raw.replace(b'FAILED',b'PASSED',1)]:
            with self.subTest(bytes=len(altered)),self.assertRaises(ValueError):
                self.cc.prior_value(altered,failure,ctx['suite'],ctx['sources'],ctx['root'],adapter=self.a)
        with self.assertRaises(ValueError): self.cc.prior_value(raw,failure+b' ',ctx['suite'],ctx['sources'],ctx['root'],adapter=self.a)

    def test_only_the_exact_covering_descriptor_is_admitted(self):
        ctx=self.context(); raw=(ctx['prior']/'RECEIPT.json').read_bytes(); fail=(ctx['prior']/'FAILURE.json').read_bytes()
        for mutate in [lambda s:s.update(id='D04-T07-HISTORY-ORIGINAL'),lambda s:s['targets'].pop(),lambda s:s['replay']['stages'].reverse()]:
            suite=copy.deepcopy(ctx['suite']);mutate(suite)
            with self.assertRaises(ValueError):self.cc.prior_value(raw,fail,suite,ctx['sources'],ctx['root'],adapter=self.a)

    def test_collection_preserves_38_original_intervals_and_18_objects(self):
        ctx,checked=self.retained(); collection=checked['collection']
        self.assertEqual(checked['inventory']['file_count'],356)
        self.assertEqual(len(checked['all_objects']),18)
        self.assertEqual(len(checked['qualified_objects']),7)
        self.assertEqual(len(collection['child_observations']),38)
        self.assertEqual(len(collection['controls']),13)
        self.assertEqual(sum(r['actual_outcome']=='REJECT' for r in collection['child_observations']),12)
        old=checked['prior']['receipt']['replay_evidence']['driver_invocations'][0]
        self.assertEqual(collection['driver_invocation']['capture_records'],old['capture_records'])
        self.assertGreater(collection['started_at'],checked['prior']['receipt']['ended_at'])
        self.cc.validate_collection(collection,checked['prior']['receipt'],ctx['plan'],ctx['suite'],adapter=self.a)

    def test_collection_rejects_omitted_reordered_or_invented_physical_events(self):
        ctx,checked=self.retained()
        changes=[lambda c:c['driver_invocation']['capture_records'].pop(),
                 lambda c:c['driver_invocation']['capture_records'].reverse(),
                 lambda c:c['driver_invocation']['capture_records'][0]['record'].update(exit_code=1),
                 lambda c:c['driver_invocation']['capture_records'][0]['record'].update(started_at='2099-01-01T00:00:00Z')]
        for mutate in changes:
            candidate=copy.deepcopy(checked['collection']);mutate(candidate)
            with self.assertRaises(ValueError):self.cc.validate_collection(candidate,checked['prior']['receipt'],ctx['plan'],ctx['suite'],adapter=self.a)

    def test_collection_rejects_log_source_object_control_and_parser_drift(self):
        ctx,checked=self.retained()
        changes=[lambda c:c['driver_invocation']['capture_records'][21].update(log_hex=b'error: sorryAx different'.hex()),
                 lambda c:c['driver_invocation']['capture_records'][21]['record']['source_binding'].update(generated_sha256='0'*64),
                 lambda c:c['driver_invocation']['qualified_objects'].update({'original/kernel/CoveringPortfolio.olean':'0'*64}),
                 lambda c:c['controls'].pop(),
                 lambda c:c.update(parser_revision='producer-chosen')]
        for mutate in changes:
            candidate=copy.deepcopy(checked['collection']);mutate(candidate)
            with self.assertRaises(ValueError):self.cc.validate_collection(candidate,checked['prior']['receipt'],ctx['plan'],ctx['suite'],adapter=self.a)

    def test_collection_does_not_relabel_old_events_as_new_execution(self):
        ctx,checked=self.retained()
        candidate=copy.deepcopy(checked['collection']);candidate['started_at']=checked['prior']['receipt']['started_at']
        with self.assertRaises(ValueError):self.cc.validate_collection(candidate,checked['prior']['receipt'],ctx['plan'],ctx['suite'],adapter=self.a)
        candidate=copy.deepcopy(checked['collection']);candidate['child_observations'][0]['started_at']=candidate['started_at']
        with self.assertRaises(ValueError):self.cc.validate_collection(candidate,checked['prior']['receipt'],ctx['plan'],ctx['suite'],adapter=self.a)

    def test_negative_resource_infrastructure_and_zero_exit_have_no_credit(self):
        ctx,checked=self.retained(); old=checked['prior']['receipt']; invocation=old['replay_evidence']['driver_invocations'][0]
        contract,bindings=self.a.d04_capture_specs(invocation); item=invocation['capture_records'][21]
        spec=self.a.d04_expand(contract['children'][21],bindings); parent=next(r for r in old['replay_evidence']['stage_results']if r['id']=='original-driver')
        self.assertTrue(self.a.d04_assess_captured_child(spec,item['record'],bytes.fromhex(item['log_hex']),parent)['rejection_credit'])
        for text in ['error: unknown identifier missing sorryAx','error: must be contained in root directory sorryAx','maximum number of heartbeats sorryAx']:
            row=copy.deepcopy(item['record']);log=text.encode();row['log_sha256']=hash_bytes(log)
            try: value=self.a.d04_assess_captured_child(spec,row,log,parent)
            except ValueError:continue
            self.assertFalse(value['rejection_credit'])
        row=copy.deepcopy(item['record']);row['exit_code']=0
        with self.assertRaises(ValueError):self.a.d04_assess_captured_child(spec,row,bytes.fromhex(item['log_hex']),parent)

    def test_positive_sorryAx_stays_rejected(self):
        ctx,checked=self.retained();old=checked['prior']['receipt'];iv=old['replay_evidence']['driver_invocations'][0]
        contract,bindings=self.a.d04_capture_specs(iv);row=copy.deepcopy(iv['capture_records'][4]['record']);log=b'sorryAx'
        row['log_sha256']=hash_bytes(log);parent=next(r for r in old['replay_evidence']['stage_results']if r['id']=='original-driver')
        with self.assertRaises(ValueError):self.a.d04_assess_captured_child(self.a.d04_expand(contract['children'][4],bindings),row,log,parent)

    def test_audit_resource_and_failure_are_not_proof_or_rejection(self):
        for terminal,code,log,expected in [('TIMEOUT',None,b'', 'RESOURCE_INCONCLUSIVE'),('INTERRUPTED',None,b'', 'RESOURCE_INCONCLUSIVE'),('COMPLETED',1,b'error: bad theorem','FAILED'),('COMPLETED',0,b'maximum number of heartbeats','RESOURCE_INCONCLUSIVE')]:
            with self.subTest(terminal=terminal,code=code):
                outcome,rows=self.cc.audit_result({'terminal':terminal,'exit_code':code},log,[],adapter=self.a)
                self.assertEqual((outcome,rows),(expected,{}))
        with self.assertRaises(ValueError):self.cc.audit_result({'terminal':'TIMEOUT','exit_code':1},b'',[],adapter=self.a)
        with self.assertRaises(ValueError):self.cc.audit_result({'terminal':'RUNNING','exit_code':None},b'',[],adapter=self.a)

    def test_audit_requires_exact_owner_axioms_complete_closure_and_no_proof_hole(self):
        target={'target_id':'one','name':'Synthetic.p','module':'Synthetic'}
        valid=b"V5_BEGIN Synthetic.p\nSynthetic.p : True\n'Synthetic.p' does not depend on any axioms\nV5_OWNER Synthetic.p Synthetic\nV5_SAFE Synthetic.p 1 []\nV5_END Synthetic.p\n"
        run={'terminal':'COMPLETED','exit_code':0}
        outcome,rows=self.cc.audit_result(run,valid,[target],adapter=self.a)
        self.assertEqual(outcome,'QUALIFIED_DECLARED_SUITE');self.assertEqual(rows['one']['checked_declarations'],1)
        for raw in [valid.replace(b'Synthetic\nV5_SAFE',b'Other\nV5_SAFE'),valid.replace(b'1 []',b'0 []'),valid.replace(b'1 []',b'1 [sorryAx]'),valid+b'warning: sorryAx\n',valid.replace(b'V5_END',b'MISSING_END')]:
            with self.assertRaises(ValueError):self.cc.audit_result(run,raw,[target],adapter=self.a)

    def test_output_must_be_absent_and_outside_retained_inputs(self):
        with tempfile.TemporaryDirectory() as name:
            root=Path(name);old=root/'old';old.mkdir();new=root/'fresh'
            self.assertEqual(self.cc.output_path(new,[old],adapter=self.a),new)
            for target in [old,old/'nested',root]:
                with self.assertRaises(ValueError):self.cc.output_path(target,[old],adapter=self.a)

    def test_one_audit_boundary_cannot_launch_a_producer_or_write_old_output(self):
        ctx,checked=self.retained();calls=[]
        with tempfile.TemporaryDirectory() as name:
            out=Path(name);(out/'logs').mkdir()
            def forbidden_process(argv,cwd,env,log,seconds):
                calls.append(([str(x)for x in argv],str(cwd),seconds,dict(env)))
                raise RuntimeError('TEST_STOP_BEFORE_ANY_PROCESS')
            before=(ctx['prior']/'RECEIPT.json').read_bytes()
            with patch.object(self.a,'run_process',side_effect=forbidden_process),self.assertRaisesRegex(RuntimeError,'TEST_STOP'):
                self.cc.audit_once(out,ctx['prior'],ctx['plan'],{'lean':Path(ctx['tools']['lean'])},{'LEAN_PATH':'TEST_BOUND_PATH'},adapter=self.a)
            self.assertEqual(len(calls),1)
            self.assertEqual(calls[0][0],[ctx['tools']['lean'],'-j1',str(out/'generated/V5SuccessorReadback.lean')])
            self.assertEqual(calls[0][1],str(ctx['prior']/'project'));self.assertEqual(calls[0][2],300)
            self.assertEqual((ctx['prior']/'RECEIPT.json').read_bytes(),before)

if __name__=='__main__':unittest.main(verbosity=2)
