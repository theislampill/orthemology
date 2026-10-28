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


if __name__ == '__main__': unittest.main()
