"""Controls preventing partial results or backup bodies from becoming success evidence."""
from pathlib import Path
import copy
import json
import tempfile
import unittest

import source_alias_absence_evidence as evidence

PHASES = ['metadata', '824', 'owners', '258-source_objects', '258-legacy_suites',
          '258-preservation', '258-t20_graph', '98', '258-reader', '258-reference',
          'public-references', 'negative-controls', 'post-controls']


class ExecutionEvidenceControls(unittest.TestCase):
    def setUp(self):
        self.state = Path(self.enterContext(tempfile.TemporaryDirectory()))
        self.record = {'status': 'PASS_BOUNDED_EXECUTION_AND_RESTORATION', 'held_denials': 0,
            'phases': [{'phase': phase, 'exit_code': 0, 'terminal': {'sha256': 'a' * 64}} for phase in PHASES],
            'restoration': {'status': 'PASS_EXACT_RESTORATION_ONLY', 'held_denials': 0}}

    def test_complete_terminal_shape(self):
        self.assertTrue(evidence.terminal_complete(self.record, PHASES))

    def test_failure_cancellation_and_partial_phases_cannot_qualify(self):
        cases = []
        failed = copy.deepcopy(self.record); failed['status'] = 'FAIL_OR_INTERRUPTED'; cases.append(failed)
        missing = copy.deepcopy(self.record); missing['phases'].pop(); cases.append(missing)
        duplicate = copy.deepcopy(self.record); duplicate['phases'][-1] = duplicate['phases'][0]; cases.append(duplicate)
        denied = copy.deepcopy(self.record); denied['held_denials'] = 1; cases.append(denied)
        unrestored = copy.deepcopy(self.record); unrestored['restoration']['status'] = 'FAIL_RESTORATION'; cases.append(unrestored)
        nonzero = copy.deepcopy(self.record); nonzero['phases'][0]['exit_code'] = 1; cases.append(nonzero)
        for case in cases:
            with self.subTest(case=case): self.assertFalse(evidence.terminal_complete(case, PHASES))

    def test_missing_terminal_cannot_qualify(self):
        self.assertFalse(evidence.receive_execution(self.state, PHASES)['qualified'])

    def test_unreceived_phase_files_cannot_qualify_a_pass_label(self):
        (self.state / 'EXECUTION-TERMINAL.json').write_text(json.dumps(self.record))
        self.assertFalse(evidence.receive_execution(self.state, PHASES)['qualified'])

    def test_whitelist_excludes_bodies_git_objects_exports_and_unknown_files(self):
        selected = ['PREPARED.json', 'before.json', 'original-index', 'inputs/hold.json',
                    'phases/metadata/TERMINAL.json', 'phases/metadata/stdout.log']
        excluded = ['bodies/012345', '.git/objects/abc', 'phases/258-t20_graph/actual258.export/Proof.lean',
                    'unknown.json', 'inputs/unpublished-body.md', 'phases/metadata/unexpected.txt']
        for name in selected + excluded:
            path = self.state / name; path.parent.mkdir(parents=True, exist_ok=True); path.write_text('{}')
        self.assertEqual({str(path.relative_to(self.state)) for path in evidence.whitelisted_files(self.state, PHASES)}, set(selected))

    def test_symlink_at_whitelisted_path_refuses_export(self):
        (self.state / 'unlisted.txt').write_text('artificial marker')
        (self.state / 'PREPARED.json').symlink_to(self.state / 'unlisted.txt')
        with self.assertRaises(RuntimeError): evidence.whitelisted_files(self.state, PHASES)

    def test_phase_path_traversal_refuses(self):
        phases = PHASES[:-1] + ['../bodies']
        with self.assertRaises(RuntimeError): evidence.whitelisted_files(self.state, phases)





class PublicFixtureEvidenceControls(unittest.TestCase):
    """Receipt grammar controls; a synthetic shape never qualifies execution."""
    def setUp(self):
        self.state = Path(self.enterContext(tempfile.TemporaryDirectory(prefix='public123-evidence-')))
        self.phases = ['fixtures123-present', 'fixtures123-unstaged', 'fixtures123-staged',
                       'fixtures123-controls', 'fixtures123-post-controls']
        self.record = {'profile': 'public-fixtures123', 'status': 'PASS_PUBLIC_FIXTURE_EXECUTION_AND_RESTORATION',
                       'held_denials': 0, 'private_denials': 0,
                       'phases': [{'phase': phase, 'exit_code': 0, 'terminal': {'sha256': 'a' * 64}}
                                  for phase in self.phases],
                       'restoration': {'status': 'PASS_FIXTURE_MEMBERS_AND_INDEX_RESTORATION_ONLY'}}

    def test_shape_does_not_substitute_for_actual_execution_evidence(self):
        self.assertTrue(evidence.public_fixture_terminal_complete(self.record))
        (self.state / 'EXECUTION-TERMINAL.json').write_text(json.dumps(self.record))
        self.assertFalse(evidence.receive_public_fixture_execution(self.state)['qualified'])

    def test_missing_nonzero_duplicate_or_denied_process_cannot_qualify(self):
        variants = []
        for value in (None, 1, True):
            bad = copy.deepcopy(self.record); bad['phases'][0]['exit_code'] = value; variants.append(bad)
        bad = copy.deepcopy(self.record); bad['phases'].pop(); variants.append(bad)
        bad = copy.deepcopy(self.record); bad['phases'][-1] = bad['phases'][0]; variants.append(bad)
        bad = copy.deepcopy(self.record); bad['private_denials'] = 1; variants.append(bad)
        bad = copy.deepcopy(self.record); bad['restoration']['status'] = 'STOPPED_FIRST_NAMESPACE_DIVERGENCE'; variants.append(bad)
        for bad in variants:
            with self.subTest(value=bad):
                self.assertFalse(evidence.public_fixture_terminal_complete(bad))

    def test_previous_and_new_profile_evidence_are_not_interchangeable(self):
        self.assertFalse(evidence.terminal_complete(self.record, PHASES))
        previous = {'status': 'PASS_BOUNDED_EXECUTION_AND_RESTORATION', 'held_denials': 0,
                    'phases': [{'phase': phase, 'exit_code': 0, 'terminal': {'sha256': 'a' * 64}}
                               for phase in PHASES],
                    'restoration': {'status': 'PASS_EXACT_RESTORATION_ONLY', 'held_denials': 0}}
        self.assertTrue(evidence.terminal_complete(previous, PHASES))
        self.assertFalse(evidence.public_fixture_terminal_complete(previous))

    def test_finite_export_excludes_parked_bodies_and_refuses_symlinks(self):
        selected = ['PREPARED.json', 'before.json', 'original-index', 'inputs/hold.json',
                    'phases/fixtures123-staged/TERMINAL.json', 'phases/fixtures123-staged/stdout.log']
        excluded = ['park/original.json', 'bodies/secret', '.git/objects/aa', 'unknown.json',
                    'phases/fixtures123-staged/unexpected.py', 'inputs/unpublished-body.md']
        for name in selected + excluded:
            path = self.state / name; path.parent.mkdir(parents=True, exist_ok=True); path.write_text('{}')
        self.assertEqual({p.relative_to(self.state).as_posix() for p in evidence.public_fixture_whitelisted_files(self.state)},
                         set(selected))
        (self.state / 'PREPARED.json').unlink()
        (self.state / 'PREPARED.json').symlink_to(self.state / 'unknown.json')
        with self.assertRaises(RuntimeError):
            evidence.public_fixture_whitelisted_files(self.state)


import os

class PublicFixtureExportRevisionTests(unittest.TestCase):
    """Finite public-input transport only; never simulated hosted success."""
    def setUp(self):
        self.root = Path(os.environ['PUBLIC123_REVISION_RESOURCES'])/self.id()
        self.state = self.root/'state'
        self.state.mkdir(parents=True)
        self.public = ('258.py', 'boundary.py', 'context.py', 'evidence.py', 'guard.py',
                       'harness.py', 'metadata.py', 'population.py', 'reader_adapter.py')
        self.names = {'inputs/'+name for name in self.public} | {
            'inputs/SOURCE-IDENTITIES.json', 'inputs/hold.json', 'inputs/fixture-sources.json',
            'inputs/fixture-population.json', 'ADMISSION.json', 'index-mode.json',
            'native-stage-before.z', 'before-namespace.json'}
        self.inputs = {}
        for relative in sorted(self.names):
            body = b'# finite public transport contract\n' if relative.endswith('.py') else b'{}\n'
            path = self.state/relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(body)
            self.inputs[relative] = evidence.identity(body)
        (self.state/'PREPARED.json').write_text(json.dumps({'input_files': self.inputs}))

    def test_all_seventeen_prepared_inputs_have_an_exact_export_route(self):
        exported = {p.relative_to(self.state).as_posix() for p in evidence.public_fixture_whitelisted_files(self.state)}
        self.assertEqual(self.names - exported, set())
        self.assertFalse(evidence.receive_public_fixture_execution(self.state)['qualified'])

    def test_missing_or_changed_public_helper_body_is_refused(self):
        exact = evidence.public_fixture_export_inputs(self.state)
        self.assertEqual(set(exact), self.names)
        target = self.state/'inputs/guard.py'
        target.write_bytes(b'# wrong public helper\n')
        with self.assertRaises(RuntimeError):
            evidence.public_fixture_export_inputs(self.state)
        target.unlink()
        with self.assertRaises((RuntimeError, OSError)):
            evidence.public_fixture_export_inputs(self.state)

    def test_transport_does_not_export_unbound_source_or_provider_body(self):
        for relative in ('park/original.json', 'provider-bodies/public', 'inputs/unlisted.py'):
            path = self.state/relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('not exportable')
        evidence.public_fixture_export_inputs(self.state)
        names = {p.relative_to(self.state).as_posix() for p in evidence.public_fixture_whitelisted_files(self.state)}
        self.assertFalse({'park/original.json', 'provider-bodies/public', 'inputs/unlisted.py'} & names)
        (self.state/'inputs/guard.py').unlink()
        (self.state/'inputs/guard.py').symlink_to(self.state/'inputs/unlisted.py')
        with self.assertRaises(RuntimeError):
            evidence.public_fixture_export_inputs(self.state)


class PublicFixtureFailureTransportRevisionTests(PublicFixtureExportRevisionTests):
    # Selected explicitly below: inherited passing transport contracts are not rerun.
    def test_failed_corrupt_index_metadata_export_is_nonzero_unqualified_and_read_only(self):
        for relative in ('original-index', 'expected-index'):
            (self.state/relative).write_bytes(b'CORRUPT_SAVED_METADATA')
        before = {str(p.relative_to(self.state)): p.read_bytes() for p in self.state.rglob('*') if p.is_file()}
        with self.assertRaises(SystemExit) as caught:
            evidence.export_public_fixture_evidence(self.state, admission={
                'scope': 'GRAMMAR_AND_FAILURE_TRANSPORT_ONLY', 'actual_hosted_execution': False,
                'live_index': {'exact': False, 'error': 'Declared corrupt-index transport test'}})
        self.assertEqual(caught.exception.code, 1)
        summary = json.loads((self.root/'r0002-public-fixtures123-receipts/EXPORT-SUMMARY.json').read_bytes())
        self.assertFalse(summary['outcome']['qualified'])
        self.assertEqual(len(summary['export_errors']), 2)
        self.assertEqual(before, {str(p.relative_to(self.state)): p.read_bytes() for p in self.state.rglob('*') if p.is_file()})
        self.assertTrue(self.names <= {row['path'] for row in summary['files']})



class PublicFixtureProcessGraphRevisionTests(unittest.TestCase):
    """In-memory grammar only, intentionally lacking any complete hosted/source packet."""
    def setUp(self):
        self.root = Path(os.environ['PUBLIC123_REVISION_RESOURCES'])/self.id()
        self.root.mkdir(parents=True)
        self.cases = 0

    def tearDown(self):
        (self.root/'GRAMMAR-ONLY.json').write_text(json.dumps({'scope': 'PROCESS_SERIALIZATION_ONLY',
            'negative_cases': self.cases, 'actual_hosted_execution': False, 'complete_execution_packet_created': False}))

    def graph(self):
        def process(pid): return {'pid': pid, 'proc_pid': pid, 'start_ticks': str(pid*100), 'pid_namespace': 'pid:[1]'}
        def group(pid): return dict(process=process(pid), pgid=pid, sid=pid, proc_pgid=pid, proc_sid=pid)
        zero = dict(held_denials=0, private_denials=0, held_events=[], private_events=[])
        parent = process(100); parent_group = group(100)
        operation = {'operation': 'prepare-public-fixtures123', 'process': parent, 'group': parent_group, 'token': '1'*32}
        execute = dict(operation, operation='execute-public-fixtures123', token='2'*32)
        prepared = dict(zero, operation=operation, repo='/grammar/repo', state='/grammar/state', runtime={'executable': '/grammar/python'})
        start = {'operation': execute, 'process': parent}
        terminal = copy.deepcopy(zero); preparation = dict(copy.deepcopy(zero), operation=copy.deepcopy(operation))
        frames, children = {}, {}
        groups = {'groups/'+op['token']+'.json': copy.deepcopy(parent_group) for op in (operation, execute)}
        for i, phase in enumerate(evidence.PUBLIC_FIXTURE_PHASES, 3):
            token = str(i)*32; child_group = group(200+i); child_process = child_group['process']
            prefix = ['/grammar/python', '-B', '/grammar/repo/scripts/check_source_alias_absence.py', '_fixture-phase',
                      '--repo', '/grammar/repo', '--state', '/grammar/state', '--phase', phase, '--token', token]
            command = prefix+['--identity-fd', '7']; child_ref = 'children/'+token+'.json'; stdout = evidence.identity(b'grammar')
            custody = {'profile': 'public-fixtures123', 'phase': phase, 'token': token, 'parent': parent,
                'command_prefix': prefix, 'command': command, 'pid': child_process['pid'], 'group': child_group,
                'group_record_persisted': True, 'lease_sent': True, 'status': 'TERMINAL_RECEIVED',
                'quiescent': True, 'exit_code': 0, 'stdout': stdout}
            children[child_ref] = copy.deepcopy(custody); groups['groups/'+token+'.json'] = copy.deepcopy(child_group)
            frames[phase] = {'START': {'token': token, 'profile': 'public-fixtures123', 'phase': phase, 'process': parent},
                'child': {'process': child_process, 'group': child_group, 'token': token, 'command': command, 'custody_record': child_ref},
                'LEASE': {'token': token, 'phase': phase, 'child': child_process, 'command': command, 'status': 'SENT_TO_CHILD'},
                'CHILD-RESULT': copy.deepcopy(custody),
                'PROCESS': {'phase': phase, 'token': token, 'exit_code': 0, 'stdout': stdout, 'custody_record': child_ref},
                'TERMINAL': dict(copy.deepcopy(zero), lease_token=token, process=child_process, group=child_group),
                'QUIESCENCE': {'group': child_group, 'token': token, 'custody_record': child_ref,
                               'quiescent': True, 'observed_members': []}}
        parent_member = dict(parent, state='R', pgid=100, sid=100, proc_pgid=100, proc_sid=100)
        quiet = {'quiescent': True, 'groups': [{'record': '/grammar/state/'+ref, 'group': copy.deepcopy(g),
            'observed_members': [copy.deepcopy(parent_member)] if g['process']==parent else [], 'active_members': []}
            for ref,g in groups.items()], 'children': [{'record':ref, 'child':copy.deepcopy(child), 'exact_quiescent': True}
            for ref,child in children.items()]}
        return [prepared, start, terminal, preparation, frames, groups, children, quiet]

    def reject(self, graph):
        with self.assertRaises((RuntimeError, KeyError, ValueError, TypeError, IndexError)):
            evidence.public_fixture_process_graph(*graph)
        self.cases += 1

    def test_process_grammar_requires_all_start_child_lease_group_and_terminal_links(self):
        graph = self.graph()
        self.assertEqual(evidence.public_fixture_process_graph(*graph)['scope'], 'CONSISTENT_PROCESS_SERIALIZATION_ONLY')
        phase = evidence.PUBLIC_FIXTURE_PHASES[0]
        for name in ('START', 'child', 'LEASE', 'CHILD-RESULT', 'PROCESS', 'TERMINAL', 'QUIESCENCE'):
            bad = self.graph(); del bad[4][phase][name]; self.reject(bad)
        bad = self.graph(); bad[5].pop('groups/'+'3'*32+'.json'); self.reject(bad)
        bad = self.graph(); bad[6].pop('children/'+'3'*32+'.json'); self.reject(bad)
        bad = self.graph(); bad[4][phase]['LEASE']['status']='DURABLE_INTENT_BEFORE_SEND'; self.reject(bad)
        bad = self.graph(); bad[4][phase]['TERMINAL']['lease_token']='9'*32; self.reject(bad)
        bad = self.graph(); bad[4][phase]['PROCESS']['exit_code']=False; self.reject(bad)
        bad = self.graph(); bad[4][phase]['child']['command'][3]='_unadmitted'; self.reject(bad)

    def test_quiescence_boolean_cannot_hide_missing_parent_live_member_or_missing_child(self):
        phase = evidence.PUBLIC_FIXTURE_PHASES[0]
        bad = self.graph(); bad[7]['groups'][0]['observed_members']=[]; self.reject(bad)
        bad = self.graph(); bad[7]['children'].pop(); self.reject(bad)
        bad = self.graph(); bad[7]['groups'].pop(); self.reject(bad)
        bad = self.graph(); child = bad[4][phase]['child']['group']; proc = child['process']
        bad[4][phase]['QUIESCENCE']['observed_members'] = [dict(proc, state='R', pgid=proc['pid'], sid=proc['pid'],
            proc_pgid=proc['proc_pid'], proc_sid=proc['proc_pid'])]; self.reject(bad)
        bad = self.graph(); extra = dict(bad[7]['groups'][0]['observed_members'][0], pid=999, proc_pid=999)
        bad[7]['groups'][0]['observed_members'].append(extra); self.reject(bad)

    def test_parent_preparation_and_phase_denial_arrays_must_match_zero_counts(self):
        for index in (0, 2, 3):
            for key in ('held_events', 'private_events'):
                bad = self.graph(); bad[index][key] = [{'event': 'GRAMMAR_ONLY_CONTRADICTION'}]; self.reject(bad)
        bad = self.graph(); bad[4][evidence.PUBLIC_FIXTURE_PHASES[0]]['TERMINAL']['held_events']=[{}]; self.reject(bad)
        bad = self.graph(); bad[2]['held_denials']=False; self.reject(bad)


class PublicFixtureControlReaderGraphRevisionTests(unittest.TestCase):
    """Exact path and reader-event grammar; no synthetic full hosted result."""
    def setUp(self):
        self.root=Path(os.environ['PUBLIC123_REVISION_RESOURCES'])/self.id(); self.root.mkdir(parents=True)

    def test_exact_ten_control_paths_reject_duplicate_provider_wrong_row_and_changed_key_target(self):
        providers=[{'path':'public/provider'+str(i)+'.py'} for i in range(3)]
        records=[{'path':'public/original.json'}]
        targets=([(kind,row['path']) for kind in ('provider-body','provider-index-mode') for row in providers]
                 +[(kind,records[0]['path']) for kind in ('public-row-role','public-row-public_sha256')]
                 +[('nonmember-request',p) for p in ('not-an-admitted-public-fixture.json',
                    'experiments/episode-reification-v2/fixtures/KEYS.json')])
        controls=[dict(kind=kind,path=path,errors=['GRAMMAR_ONLY_REFUSAL'],exact_restoration=True) for kind,path in targets]
        self.assertEqual(evidence.public_fixture_control_targets(controls, providers, records)['scope'], 'CONSISTENT_TEN_CONTROL_TARGETS_ONLY')
        variants=[]
        for index,path in ((2,providers[0]['path']),(5,providers[0]['path']),(6,'public/wrong.json'),(9,'public/not-the-key.json')):
            bad=copy.deepcopy(controls); bad[index]['path']=path; variants.append(bad)
        bad=copy.deepcopy(controls); bad[0]['errors']=[]; variants.append(bad)
        for bad in variants:
            with self.assertRaises(RuntimeError): evidence.public_fixture_control_targets(bad,providers,records)
        (self.root/'GRAMMAR-ONLY.json').write_text(json.dumps({'negative_cases':len(variants),'actual_hosted_execution':False}))

    def test_reader_boundary_requires_exact_private_exclusions_and_actual_native_links(self):
        from source_alias_absence_boundary import PROTECTED_PATHS
        from source_alias_absence_reader import BASELINE
        held=set(PROTECTED_PATHS); events=[]; native=[]
        suffix=['--no-ext-diff','--no-textconv','--no-renames','--name-status','-z',BASELINE,'--']
        for surface in ('index','public_worktree'):
            original=['git','diff']+(['--cached'] if surface=='index' else [])+suffix
            executed=['git','--no-replace-objects',*original[1:]]
            if surface=='public_worktree': executed+=['.',*(':(top,literal,exclude)'+p for p in sorted(held))]
            events.append({'surface':surface,'original_command':original,'executed_command':executed,'returncode':0,
                'held_worktree_exclusions':0 if surface=='index' else 5,'held_stage_tree_metadata':'EXACT',
                'held_worktree_body_integrity':'UNKNOWN'})
            native.append({'observed_argv':executed,'exit_code':0})
        boundary={'scope':'Actual public reader with exact held metadata gate and explicit native worktree exclusions',
            'full_protected_local_reader_cli':'NOT_RUN','held_worktree_body_integrity':'UNKNOWN','baseline':BASELINE,
            'root':'/grammar/repo','held_paths':sorted(held),'known_held_links_per_body':1,'events':events}
        self.assertEqual(evidence.public_fixture_reader_graph(boundary,'/grammar/repo',held,BASELINE,native)['scope'],
                         'CONSISTENT_READER_BOUNDARY_ONLY')
        variants=[]
        bad=copy.deepcopy(boundary); bad['events'].pop(); variants.append((bad,native))
        bad=copy.deepcopy(boundary); bad['events'][1]['executed_command'].pop(); variants.append((bad,native))
        bad=copy.deepcopy(boundary); bad['held_worktree_body_integrity']='VERIFIED'; variants.append((bad,native))
        bad=copy.deepcopy(boundary); bad['events'][1]['held_worktree_exclusions']=4; variants.append((bad,native))
        variants.append((boundary,[]))
        for bad,outcomes in variants:
            with self.assertRaises(RuntimeError): evidence.public_fixture_reader_graph(bad,'/grammar/repo',held,BASELINE,outcomes)
        (self.root/'GRAMMAR-ONLY.json').write_text(json.dumps({'negative_cases':len(variants),'actual_hosted_execution':False}))


class CurrentEvidence(unittest.TestCase):
 def setUp(self):
  self.classes=[{'alias':f'a{i}','canonical':f'c{i%1082}'} for i in range(1180)]
  self.before={'rows':[{'path':f'a{i}'} for i in range(114,1180)]+[{'path':f'c{i}'} for i in range(1082)]+[{'path':f'g{i}'} for i in range(3)]}
  self.prepared={'profile':'current-checkout1180-v1','initially_absent_aliases':[f'a{i}' for i in range(114)],'trial_removed_aliases':[f'a{i}' for i in range(114,1180)],'preimage_paths':2151,'expected_absent_tracked':1085}
  for k in ('initially_absent_aliases','trial_removed_aliases'):self.prepared[k].sort()
 def test_current(self):self.assertEqual(evidence.prepared_alias_scope(self.prepared,self.before,self.classes)['planned_trial_removals'],1066)
 def test_legacy(self):
  self.before['rows'] += [{'path':f'a{i}'} for i in range(114)];self.prepared={'preimage_paths':2265,'expected_absent_tracked':1085};self.assertEqual(evidence.prepared_alias_scope(self.prepared,self.before,self.classes)['previously_absent_aliases'],0)
 def test_relabelled_current_fails(self):
  self.prepared['profile']='historical-all-present1180-v1';self.assertRaises(RuntimeError,evidence.prepared_alias_scope,self.prepared,self.before,self.classes)
 def test_wrong_backup_count(self):
  self.prepared['preimage_paths']=2265;self.assertRaises(RuntimeError,evidence.prepared_alias_scope,self.prepared,self.before,self.classes)
 def test_wrong_partition(self):
  self.prepared['initially_absent_aliases'].pop();self.assertRaises(RuntimeError,evidence.prepared_alias_scope,self.prepared,self.before,self.classes)
 def test_missing_canonical(self):
  self.before['rows']=[r for r in self.before['rows'] if r['path']!='c0'];self.assertRaises(RuntimeError,evidence.prepared_alias_scope,self.prepared,self.before,self.classes)

class CurrentReceiverEarlyRejection(unittest.TestCase):
    setUp = CurrentEvidence.setUp
    def check_receiver(self, wrong_scope):
        from unittest.mock import patch
        before_body = json.dumps(self.before).encode()
        self.prepared.update(held_denials=0, originals=1180, unique_canonicals=1082,
            original_census_paths=16103, input_files={}, before=evidence.identity(before_body),
            preimages=evidence.identity(b'[]'))
        scope = evidence.prepared_alias_scope(self.prepared, self.before, self.classes)
        terminal = {'trial_scope': {} if wrong_scope else scope}
        data = {'EXECUTION-TERMINAL.json': terminal, 'PREPARED.json': self.prepared,
                'classes.json': self.classes}
        # Isolate receiving checks after the unchanged terminal gate. This does
        # not construct or claim a successful hosted thirteen-phase packet.
        with patch.object(evidence, 'terminal_complete', return_value=True), \
             patch.object(evidence, 'read_json', side_effect=lambda state, name: data[name]), \
             patch.object(evidence, 'read', side_effect=lambda state, name: before_body if name=='before.json' else b'[]'):
            result = evidence.receive_execution(Path('/unused'), PHASES)
        self.assertFalse(result['qualified'])
        self.assertIn('Current terminal trial scope differs' if wrong_scope else 'Current preimage membership differs', result['error'])
    def test_receiver_rejects_wrong_scope(self): self.check_receiver(True)
    def test_receiver_rejects_wrong_preimage_membership(self): self.check_receiver(False)


if __name__ == '__main__': unittest.main()

