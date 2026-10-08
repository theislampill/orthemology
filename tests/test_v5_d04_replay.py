"""Private executable-path tests; synthetic processes only, no source replay."""
import copy
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

HERE=Path(__file__).resolve().parents[1]
PUBLIC_ROOT=Path(os.environ.get('D04_TEST_PUBLIC_ROOT',str(HERE)))
SCRATCH=Path(tempfile.mkdtemp(prefix='v5-d04-interface-'))
import atexit,shutil
atexit.register(shutil.rmtree,SCRATCH)
ADAPTER=HERE/'scripts/replay_v5_successors.py'
loader=importlib.util.spec_from_file_location('d04_executable_under_test',ADAPTER)
adapter=importlib.util.module_from_spec(loader);loader.loader.exec_module(adapter)

def inputs(family):
    row=adapter.d04_contracts()['families'][family]
    return row['suite'],{'sources':list(row['sources'].values())}

class D04AdmissionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.public=PUBLIC_ROOT

    def admitted(self,family):
        suite,private=inputs(family)
        try:result=adapter.validate_suite(suite,{r['id']:r for r in private['sources']},self.public)
        except ValueError as error:self.fail('Exact D04 executable package refused: '+str(error))
        self.assertEqual(result['d04_family'],family)

    def test_complete_criterion_package_is_admitted(self):self.admitted('criterion')
    def test_complete_covering_package_is_admitted(self):self.admitted('covering')
    def test_complete_composition_package_is_admitted(self):self.admitted('composition')
    def test_complete_dynamic_package_is_admitted(self):self.admitted('dynamic')

class D04CaptureTests(unittest.TestCase):
    def setUp(self):
        (SCRATCH).mkdir(exist_ok=True)
        self.temp=tempfile.TemporaryDirectory(dir=SCRATCH);self.addCleanup(self.temp.cleanup)
        self.work=Path(self.temp.name);self.trace=self.work/'trace';self.trace.mkdir()

    def session(self,code,*,capture='MERGED_BYTES',timeout=10,outputs=()):
        self.assertTrue(hasattr(adapter,'D04CaptureSession'),'Missing actual D04 subprocess capture interface')
        source=self.work/'synthetic-source.txt';source.write_bytes(b'explicit synthetic fixture input')
        row={'id':'synthetic-child','argv':[sys.executable,'-I','-B','-c',code], 'cwd':str(self.work),
             'timeout_seconds':timeout,'capture':capture,'stdin':'INHERITED_NO_INPUT','log':str(self.work/'source.log'),
             'sources':[{'kind':'ORIGINAL_SOURCE','member':'synthetic-source.txt','path':str(source),'sha256':adapter.sha(source.read_bytes())}],
             'outputs':[str(self.work/name)for name in outputs],'replace_fresh_predecessor':[],
             'expected_exit_code':0,'required_diagnostics':[],'forbidden_diagnostics':[],
             'source_binding':{'kind':'ORIGINAL_SOURCE','source_id':'synthetic-fixture','source_sha256':adapter.sha(source.read_bytes())},
             'source_environment_overrides':{},'environment_policy':'SYNTHETIC_TEST_ONLY'}
        context={'recipe':'synthetic-fixture','parent_stage_id':'synthetic-parent','source_root':str(self.work),'output':str(self.work),
                 'trace':str(self.trace),'bindings':{},'replay_id':'synthetic-run','launch_cwd':str(self.work)}
        contract={'children':[row],'tool_probes':[],'family':'synthetic-test'}
        session=adapter.D04CaptureSession(context,contract,dict(os.environ),{})
        return session,row

    def test_real_synthetic_child_records_actual_output_and_source_hash(self):
        session,spec=self.session("from pathlib import Path; Path('result.txt').write_text('fresh'); print('SYNTHETIC')",outputs=['result.txt'])
        with patch.object(subprocess,'Popen',session.popen_type()):
            result=subprocess.run(spec['argv'],cwd=spec['cwd'],env=dict(os.environ),stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=10)
        self.assertEqual(result.stdout,b'SYNTHETIC\n');self.assertEqual(result.returncode,0)
        row=json.loads((self.trace/'0000.json').read_bytes())
        self.assertEqual(row['terminal'],'COMPLETED');self.assertEqual(row['exit_code'],0)
        self.assertEqual(row['output_hashes'],{str(self.work/'result.txt'):adapter.sha(b'fresh')})
        self.assertEqual(row['source_hashes'],{'synthetic-source.txt':spec['sources'][0]['sha256']})
        self.assertEqual((self.trace/'0000.log').read_bytes(),b'SYNTHETIC\n')

    def test_separate_byte_streams_keep_original_result_and_journal_order(self):
        session,spec=self.session("import sys;sys.stdout.buffer.write(b'out');sys.stderr.buffer.write(b'err')",capture='SEPARATE_BYTES')
        with patch.object(subprocess,'Popen',session.popen_type()):
            result=subprocess.run(spec['argv'],cwd=spec['cwd'],env=dict(os.environ),capture_output=True,timeout=10)
        self.assertEqual((result.stdout,result.stderr),(b'out',b'err'))
        self.assertEqual((self.trace/'0000.log').read_bytes(),b'outerr')
        row=json.loads((self.trace/'0000.json').read_bytes())
        self.assertEqual(row['stream_hashes'],{'stdout':adapter.sha(b'out'),'stderr':adapter.sha(b'err')})

    def test_wrong_argv_cwd_env_and_stdin_are_refused_before_launch(self):
        session,spec=self.session("print('synthetic')")
        for changes in [{'args':spec['argv']+['injected']},{'cwd':str(self.work.parent)},{'env':dict(os.environ,LEAN_PATH='attacker')},{'stdin':subprocess.PIPE}]:
            kwargs={'args':spec['argv'],'cwd':spec['cwd'],'env':dict(os.environ),'stdout':subprocess.PIPE,'stderr':subprocess.STDOUT,**changes}
            argv=kwargs.pop('args')
            with self.subTest(changes=list(changes)),patch.object(subprocess,'Popen',session.popen_type()),self.assertRaises(ValueError):subprocess.run(argv,timeout=10,**kwargs)
        self.assertFalse((self.trace/'0000.json').exists())

    def test_actual_file_stream_capture_preserves_source_log_and_exit(self):
        session,spec=self.session("print('FILE SYNTHETIC')",capture='FILE_MERGED_BYTES')
        with (self.work/'source.log').open('wb') as log,patch.object(subprocess,'Popen',session.popen_type()):
            child=subprocess.Popen(spec['argv'],cwd=spec['cwd'],env=dict(os.environ),stdout=log,stderr=subprocess.STDOUT,shell=False)
            self.assertEqual(child.wait(timeout=10),0)
        self.assertEqual((self.trace/'0000.log').read_bytes(),b'FILE SYNTHETIC\n')

    def test_actual_merged_text_and_nonzero_exit_are_recorded_exactly(self):
        session,spec=self.session("import sys;print('explicit negative');sys.exit(3)",capture='MERGED_TEXT')
        with patch.object(subprocess,'Popen',session.popen_type()):
            result=subprocess.run(spec['argv'],cwd=spec['cwd'],env=dict(os.environ),stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=10)
        row=json.loads((self.trace/'0000.json').read_bytes())
        self.assertEqual((result.stdout,row['terminal'],row['exit_code']),('explicit negative\n','COMPLETED',3))

    def test_source_change_during_child_keeps_terminal_then_refuses_qualification(self):
        session,spec=self.session("from pathlib import Path;Path('synthetic-source.txt').write_text('changed');print('changed')")
        with patch.object(subprocess,'Popen',session.popen_type()),self.assertRaises(ValueError):
            subprocess.run(spec['argv'],cwd=spec['cwd'],env=dict(os.environ),stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=10)
        row=json.loads((self.trace/'0000.json').read_bytes())
        self.assertEqual((row['terminal'],row['exit_code']),('COMPLETED',0));self.assertEqual(session.producers,{})

    def test_cleanup_retains_available_partial_pipe_log_without_invented_exit(self):
        session,spec=self.session("from pathlib import Path;import time;print('available partial',flush=True);Path('ready').touch();time.sleep(10)")
        with patch.object(subprocess,'Popen',session.popen_type()):
            child=subprocess.Popen(spec['argv'],cwd=spec['cwd'],env=dict(os.environ),stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            try:
                for _ in range(100):
                    if (self.work/'ready').exists():break
                    time.sleep(.01)
                self.assertTrue((self.work/'ready').exists());session.stop()
            finally:
                if child.poll()is None:child.kill();session.original_popen.wait(child)
        row=json.loads((self.trace/'0000.json').read_bytes())
        self.assertEqual(row['terminal'],'INTERRUPTED');self.assertIsNone(row['exit_code'])
        self.assertEqual((self.trace/'0000.log').read_bytes(),b'available partial\n')

    def test_stdout_text_capture_preserves_check_output_interface(self):
        session,spec=self.session("print('text probe interface')",capture='STDOUT_TEXT',timeout=None)
        with patch.object(subprocess,'Popen',session.popen_type()):
            value=subprocess.check_output(spec['argv'],cwd=spec['cwd'],text=True)
        self.assertEqual(value,'text probe interface\n')
        self.assertEqual((self.trace/'0000.log').read_bytes(),value.encode())

    def test_timeout_preserves_unknown_exit_and_actual_partial_log(self):
        session,spec=self.session("import time;print('partial',flush=True);time.sleep(10)",timeout=1)
        with patch.object(subprocess,'Popen',session.popen_type()),self.assertRaises(subprocess.TimeoutExpired):
            subprocess.run(spec['argv'],cwd=spec['cwd'],env=dict(os.environ),stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=1)
        row=json.loads((self.trace/'0000.json').read_bytes())
        self.assertEqual(row['terminal'],'TIMEOUT');self.assertIsNone(row['exit_code'])
        self.assertEqual((self.trace/'0000.log').read_bytes(),b'partial\n')

from v5_d04_fixture_capture import make_capture,refresh,qualify,family_evidence

class D04EvidenceTests(unittest.TestCase):
    def plan(self,family):
        suite,private=inputs(family)
        return adapter.validate_suite(suite,{r['id']:r for r in private['sources']},PUBLIC_ROOT)

    def test_all_ten_exact_recipe_captures_validate_without_source_execution(self):
        producers={}
        for recipe in adapter.d04_contracts()['recipes']:
            with self.subTest(recipe=recipe):
                invocation,parent=make_capture(adapter,recipe,producers=producers)
                adapter.d04_validate_captured_invocation(invocation,self.plan(adapter.d04_contracts()['recipes'][recipe]['family']),parent,True)

    def test_unreviewed_record_metadata_is_rejected_even_with_updated_hash(self):
        invocation,parent=make_capture(adapter,'t07-criterion-translated-v1')
        invocation['capture_records'][0]['record']['scientific_credit']='FORGED';refresh(adapter,invocation)
        with self.assertRaises(ValueError):adapter.d04_validate_captured_invocation(invocation,self.plan('criterion'),parent,True)

    def test_failed_collector_does_not_erase_real_parent_terminal(self):
        plan=self.plan('criterion');driver=next(iter(plan['drivers'].values()));stage=plan['stages']['original-driver']
        with tempfile.TemporaryDirectory(dir=SCRATCH)as folder:
            out=Path(folder);log=out/'parent.log';log.write_bytes(b'ACTUAL FAILURE')
            mappings={'out':out,'project':out/'project','build':out/'build','adapter':ADAPTER,'tool:python':sys.executable,
                'tool:python312':sys.executable,'tool:lean':out/'lean','archive:source-archive':out/'archive'}
            actual={'terminal':'COMPLETED','exit_code':7,'started_at':'2026-10-05T12:00:00Z','ended_at':'2026-10-05T12:00:01Z','log_sha256':adapter.sha(log.read_bytes())}
            with patch.object(adapter,'run_process',return_value=actual),patch.object(adapter,'d04_collect_capture',side_effect=ValueError('Malformed partial journal')):
                run,invocation=adapter.d04_run_parent(stage,driver,plan,out,mappings,{},log,'f'*64,{})
            self.assertEqual(run,actual);self.assertEqual(invocation['capture_error'],'ValueError: Malformed partial journal')

    def test_qualified_objects_are_rederived_from_captured_physical_producers(self):
        self.assertTrue(hasattr(adapter,'d04_expected_objects'),'Missing independent producer/object receipt binding')
        recipe='t07-covering-translated-v1';invocation,parent=make_capture(adapter,recipe)
        plan=self.plan('covering');expected=adapter.d04_expected_objects(plan,invocation)
        self.assertEqual(set(expected),{r['path'].removeprefix('{out}/')for r in adapter.d04_contracts()['families']['covering']['object_producers'].values()if r.get('recipe')==recipe})
        row=next(r['record']for r in invocation['capture_records']if r['record']['id']=='RootImage')
        row['input_bindings'][0]['actual_sha256']='0'*64
        with self.assertRaises(ValueError):adapter.d04_expected_objects(plan,invocation)

    def test_serial_import_objects_bind_all_three_copied_fresh_predecessors(self):
        row=adapter.d04_contracts()['recipes']['t07-composition-serial-mutations-v1']['children'][0]
        inherited=[r for r in row['sources']if r.get('producer_recipe')=='t07-composition-original-v1']
        self.assertEqual({Path(r['path']).name for r in inherited},{'TypedCriterionGuard.olean','CriterionInstallation.olean','DynamicInterlock.olean'})

    def test_finite_dynamic_summary_is_bound_to_exact_source_owned_counts(self):
        self.assertTrue(hasattr(adapter,'d04_fixed_summary'),'Missing exact source-owned dynamic summary contract')
        expected=adapter.d04_fixed_summary('t07-dynamic-base-v1')
        self.assertEqual(expected['finite_matched_trace_count'],expected['finite_counts']['deletion_and_matched_control_traces'])

    def test_four_complete_synthetic_family_ledgers_validate(self):
        for family in ['criterion','covering','composition','dynamic']:
            with self.subTest(family=family):
                plan=self.plan(family);evidence,stages=family_evidence(adapter,plan)
                adapter.d04_validate_child_evidence(evidence,plan,stages,True)

    def test_mandatory_packaging_and_projection_cannot_be_omitted(self):
        plan=self.plan('composition');evidence,stages=family_evidence(adapter,plan)
        for recipe in ['t07-composition-projection-v1','t07-composition-packaging-translated-v1','t07-composition-review-translated-v1','t07-composition-serial-mutations-v1']:
            changed=copy.deepcopy(evidence);changed['driver_invocations']=[r for r in changed['driver_invocations']if r['recipe']!=recipe]
            with self.subTest(recipe=recipe),self.assertRaises(ValueError):adapter.d04_validate_child_evidence(changed,plan,stages,True)

    def test_actual_source_cwd_and_child_ledger_tampering_are_rejected(self):
        plan=self.plan('criterion');invocation,parent=make_capture(adapter,'t07-criterion-translated-v1')
        changes=[lambda i:i['capture_records'][0]['record'].update(cwd='/wrong/project'),
            lambda i:i['capture_records'][0]['record']['argv'].append('--root=/undocumented'),
            lambda i:i['capture_records'][0]['record']['input_bindings'][0].update(actual_sha256='0'*64),
            lambda i:i['capture_records'][0]['record'].update(ended_at='2026-10-05T13:00:00Z'),
            lambda i:i['capture_records'][0]['record']['source_binding'].update(source_id='invented'),
            lambda i:i['capture_records'].pop()]
        for index,change in enumerate(changes):
            changed=copy.deepcopy(invocation);change(changed);refresh(adapter,changed)
            with self.subTest(mutation=index),self.assertRaises(ValueError):adapter.d04_validate_captured_invocation(changed,plan,parent,True)

    def test_wrong_dynamic_counts_are_rejected_after_rehash(self):
        plan=self.plan('dynamic');invocation,parent=make_capture(adapter,'t07-dynamic-base-v1');qualify(adapter,invocation,plan)
        adapter.d04_bind_normalization(invocation)
        invocation['normalization']['result']['summary']['finite_counts']['deletion_and_matched_control_traces']=0
        invocation['normalization_sha256']=adapter.canonical(invocation['normalization'])
        with self.assertRaises(ValueError):adapter.d04_bind_normalization(invocation)

    def test_timeout_prefix_is_retained_without_normalization_or_rejection_credit(self):
        plan=self.plan('criterion');invocation,parent=make_capture(adapter,'t07-criterion-translated-v1')
        invocation['capture_records']=invocation['capture_records'][:1];invocation['child_count']=1
        row=invocation['capture_records'][0]['record'];row.update(terminal='TIMEOUT',exit_code=None,output_hashes={})
        refresh(adapter,invocation);parent.update(terminal='TIMEOUT',exit_code=None)
        adapter.d04_validate_captured_invocation(invocation,plan,parent,False)
        with self.assertRaises(ValueError):adapter.d04_validate_captured_invocation(invocation,plan,parent,True)

    def test_forged_qualified_object_digest_cannot_substitute_for_real_capture(self):
        plan=self.plan('criterion');evidence,stages=family_evidence(adapter,plan)
        invocation=evidence['driver_invocations'][0];path=next(iter(invocation['qualified_objects']))
        invocation['qualified_objects'][path]='0'*64;evidence['output_hashes'][path]='0'*64
        with self.assertRaises(ValueError):adapter.d04_validate_child_evidence(evidence,plan,stages,True)

    def test_replacement_prior_producer_record_cannot_be_forged(self):
        plan=self.plan('composition');evidence,stages=family_evidence(adapter,plan)
        invocation=next(r for r in evidence['driver_invocations']if r['recipe']=='t07-composition-serial-mutations-v1')
        invocation['capture_records'][0]['record']['replacement_bindings'][0]['producer_capture_sha256']='0'*64
        refresh(adapter,invocation)
        with self.assertRaises(ValueError):adapter.d04_validate_child_evidence(evidence,plan,stages,True)

    def test_historical_receipt_uses_its_recorded_adapter_asset_path(self):
        plan=self.plan('criterion');invocation,parent=make_capture(adapter,'t07-criterion-translated-v1')
        invocation['bindings']['adapter']='/historical-install/scripts/replay_v5_successors.py'
        invocation['actual_launch_argv']=adapter.d04_expand(invocation['launch_argv'],invocation['bindings'])
        invocation['helper_argv'][0]='/historical-install/scripts/v5_d04_assets/criterion_recipe.py'
        invocation['trace_launch']['helper_argv']=invocation['helper_argv'];refresh(adapter,invocation)
        adapter.d04_validate_captured_invocation(invocation,plan,parent,True)

    def test_serial_child_intervals_cannot_overlap_after_rehash(self):
        plan=self.plan('criterion');invocation,parent=make_capture(adapter,'t07-criterion-translated-v1')
        first,second=[item['record']for item in invocation['capture_records'][:2]]
        second.update(started_at=first['started_at'],ended_at=first['ended_at']);refresh(adapter,invocation)
        with self.assertRaises(ValueError):adapter.d04_validate_captured_invocation(invocation,plan,parent,True)

    def test_covering_package_library_glob_cannot_admit_undeclared_cache(self):
        plan=self.plan('covering')
        with tempfile.TemporaryDirectory(dir=SCRATCH)as folder:
            root=Path(folder)
            for row in plan['packages'].values():
                if row['path'].startswith('.lake/packages/'):(root/row['path']/'.lake/build/lib/lean').mkdir(parents=True)
            adapter.d04_runtime_bindings(plan,{'dependency:mathlib':root})
            (root/'.lake/packages/UNDECLARED/.lake/build/lib/lean').mkdir(parents=True)
            with self.assertRaises(ValueError):adapter.d04_runtime_bindings(plan,{'dependency:mathlib':root})

    def test_covering_source_pinned_unimported_cli_needs_no_library_directory(self):
        plan=self.plan('covering')
        self.assertIn('Cli',plan['packages'])
        self.assertFalse(any(row['package']=='Cli'for row in plan['official'].values()))
        with tempfile.TemporaryDirectory(dir=SCRATCH)as folder:
            root=Path(folder)
            for name,row in plan['packages'].items():
                if name!='Cli'and row['path'].startswith('.lake/packages/'):(root/row['path']/'.lake/build/lib/lean').mkdir(parents=True)
            bindings=adapter.d04_runtime_bindings(plan,{'dependency:mathlib':root})
            self.assertNotIn('/Cli/',bindings['locked:mathlib-package-libraries'])
            self.assertFalse((root/'.lake/packages/Cli/.lake/build/lib/lean').exists())

    def test_covering_required_imported_package_cache_is_still_required(self):
        plan=self.plan('covering')
        # Synthetic imported-package boundary for the shared package_library gate.
        plan['official']['Synthetic.Required']={'package':'batteries'}
        with tempfile.TemporaryDirectory(dir=SCRATCH)as folder:
            root=Path(folder)
            for name,row in plan['packages'].items():
                if name not in {'Cli','batteries'}and row['path'].startswith('.lake/packages/'):(root/row['path']/'.lake/build/lib/lean').mkdir(parents=True)
            with self.assertRaisesRegex(adapter.MissingTool,'Required imported package cache is unavailable: batteries'):
                adapter.d04_runtime_bindings(plan,{'dependency:mathlib':root})

    @unittest.skipUnless(os.environ.get('D04_TEST_MATHLIB'),'Explicit operational Mathlib cache binding required')
    def test_covering_actual_operational_cache_matches_original_existing_library_glob(self):
        plan=self.plan('covering');root=Path(os.environ['D04_TEST_MATHLIB'])
        self.assertTrue((root/'.lake/packages/Cli').is_dir())
        self.assertFalse((root/'.lake/packages/Cli/.lake/build/lib/lean').exists())
        expected=sorted((root/'.lake/packages').glob('*/.lake/build/lib/lean'))
        self.assertEqual(len(expected),7)
        bindings=adapter.d04_runtime_bindings(plan,{'dependency:mathlib':root})
        self.assertEqual(bindings['locked:mathlib-package-libraries'],os.pathsep.join(map(str,expected)))

class D04ExecutionFailureTests(unittest.TestCase):
    # Direct helper invocation, with the sole process boundary mocked. No driver,
    # theorem, compiler, tool probe or original target is executed by these tests.
    def test_failed_parent_terminal_survives_execute_and_full_receipt_validator(self):
        suite,private=inputs('criterion');sources={r['id']:r for r in private['sources']}
        reviews={rid:{'review_sha256':'a'*64}for rid in suite['review_ids']}
        with tempfile.TemporaryDirectory(dir=SCRATCH)as folder:
            out=Path(folder)/'replay'
            def fake_run(argv,cwd,env,log,timeout):
                log.write_bytes(b'SYNTHETIC physical parent failure\n')
                return {'terminal':'COMPLETED','exit_code':7,'started_at':adapter.utc(),'ended_at':adapter.utc(),'log_sha256':adapter.sha(log.read_bytes())}
            with patch.object(adapter,'_verify_environment',return_value=({'python':Path(sys.executable),'python312':Path(sys.executable),'lean':Path('/synthetic/lean')},{},{},{},{})),\
                 patch.object(adapter,'extract_source_zip',return_value={}),patch.object(adapter,'d04_source_inventory',return_value={}),patch.object(adapter,'run_process',side_effect=fake_run):
                receipt=adapter.execute_suite(suite,sources,PUBLIC_ROOT,out,{}, {'source-archive':Path('/synthetic/archive.zip')},reviews=reviews)
            stage=next(r for r in receipt['replay_evidence']['stage_results']if r['id']=='original-driver')
            self.assertEqual((receipt['outcome'],receipt['proof_scope']),('FAILED','NONE'))
            self.assertEqual((stage['terminal'],stage['exit_code']),('COMPLETED',7))
            self.assertEqual(len(receipt['replay_evidence']['driver_invocations']),1)
            self.assertEqual(receipt['replay_evidence']['child_observations'],[])

if __name__=='__main__':unittest.main(verbosity=2)
