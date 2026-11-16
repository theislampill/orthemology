import importlib.util
import json
import pathlib
import shutil
import tempfile
import unittest

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/validate_ar8r_six_lane_v14_intake.py"


def load_validator():
    if not SCRIPT.is_file():
        raise AssertionError("six-lane V14 intake validator is missing")
    spec = importlib.util.spec_from_file_location("ar8r_six_lane_v14_intake", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Ar8rSixLaneV14IntakeTests(unittest.TestCase):
    def copy_surface(self, validator, temporary):
        copied = pathlib.Path(temporary) / "six-lane-v14-intake"
        shutil.copytree(ROOT / validator.INTAKE_REL, copied)
        return copied

    def test_all_six_lanes_validate_without_scientific_promotion(self):
        validator = load_validator()
        receipt = validator.validate(ROOT)
        self.assertEqual(receipt["result"], "PASS_CURRENT_INTAKE_AND_SPECIALIST_CUSTODY")
        self.assertEqual(receipt["lane_count"], 6)
        self.assertEqual(receipt["source_file_counts"], {
            "specialist-a": 77,
            "specialist-b": 29,
        })
        self.assertEqual(receipt["source_hash_mismatches"], 0)
        self.assertEqual(receipt["private_path_findings"], 0)
        self.assertTrue(receipt["specialist_a_checks_reproduced"])
        self.assertTrue(receipt["specialist_a_original_lean_failures_recorded"])
        self.assertTrue(receipt["specialist_a_repaired_lean_receipts_exact"])
        self.assertTrue(receipt["specialist_b_original_lean_failure_recorded"])
        self.assertTrue(receipt["specialist_b_repaired_lean_receipt_exact"])
        self.assertTrue(receipt["deep_research_locator_corrections_exact"])
        self.assertTrue(receipt["tensor_arm_specification_blocked"])
        self.assertTrue(receipt["deep_research_22_readiness_fail_closed"])
        self.assertTrue(receipt["deep_research_22_b1_b4_gap_explicit"])

    def test_source_drift_fails_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "specialist-a/source-files/README.md"
            target.write_text(target.read_text(encoding="utf-8") + "\ndrift\n", encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assertEqual(receipt["result"], "FAIL")
        self.assertGreater(receipt["source_hash_mismatches"], 0)

    def test_private_locator_fails_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            leaked = copied / "LEAK.txt"
            private_locator = "C:" + "\\Users\\owner\\private.txt\n"
            leaked.write_text(private_locator, encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assertEqual(receipt["result"], "FAIL")
        self.assertGreater(receipt["private_path_findings"], 0)

    def test_owner_adoption_promotion_fails_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "AR8R-SIX-LANE-V14-INTEGRATION-LEDGER.yaml"
            text = target.read_text(encoding="utf-8").replace(
                "owner_adoption: PENDING", "owner_adoption: ADOPTED", 1
            )
            target.write_text(text, encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assertEqual(receipt["result"], "FAIL")

    def test_bad_classical_locator_fails_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "external-evidence/AR8R-DEEP-RESEARCH-20-22-INTAKE-V14.yaml"
            text = target.read_text(encoding="utf-8").replace("volume 12, pages 98 and 409", "volume 12, pages 98 and 173")
            target.write_text(text, encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assertEqual(receipt["result"], "FAIL")
        self.assertFalse(receipt["deep_research_locator_corrections_exact"])

    def test_tensor_arm_ambiguity_cannot_be_silently_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "external-evidence/AR8R-DEEP-RESEARCH-20-22-INTAKE-V14.yaml"
            text = target.read_text(encoding="utf-8").replace(
                "status: BLOCKED_SPECIFICATION_AMBIGUITY", "status: READY_TO_RUN", 1
            )
            target.write_text(text, encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assertEqual(receipt["result"], "FAIL")
        self.assertFalse(receipt["tensor_arm_specification_blocked"])

    def test_deep_research_22_protocols_cannot_be_promoted_or_credited(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "external-evidence/AR8R-DEEP-RESEARCH-20-22-INTAKE-V14.yaml"
            text = target.read_text(encoding="utf-8").replace(
                "ready_to_run_count: 0", "ready_to_run_count: 1", 1
            ).replace(
                "status: NOT_ANSWERED_BY_CURRENT_REPORT", "status: ANSWERED", 1
            )
            target.write_text(text, encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assertEqual(receipt["result"], "FAIL")
        self.assertFalse(receipt["deep_research_22_readiness_fail_closed"])
        self.assertFalse(receipt["deep_research_22_b1_b4_gap_explicit"])

    def test_empty_specialist_a_repair_receipt_fails_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "specialist-a/intake-review/LEAN_INTAKE_RECEIPT.json"
            data = json.loads(target.read_text(encoding="utf-8"))
            data["repairs"] = []
            target.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assertEqual(receipt["result"], "FAIL")
        self.assertFalse(receipt["specialist_a_repaired_lean_receipts_exact"])

    def test_duplicate_specialist_a_repair_receipt_fails_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "specialist-a/intake-review/LEAN_INTAKE_RECEIPT.json"
            data = json.loads(target.read_text(encoding="utf-8"))
            data["repairs"].append(dict(data["repairs"][0]))
            target.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assertEqual(receipt["result"], "FAIL")
        self.assertFalse(receipt["specialist_a_repaired_lean_receipts_exact"])

    def test_historical_identity_promotion_fails_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "external-evidence/AR8R-DEEP-RESEARCH-20-22-INTAKE-V14.yaml"
            data = yaml.safe_load(target.read_text(encoding="utf-8"))
            data["authority_ceiling"]["historical_identity"] = "AR8R-T999"
            target.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assertEqual(receipt["result"], "FAIL")
        self.assertFalse(receipt["authority_ceiling_exact"])

    def test_ledger_champion_promotion_fails_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "AR8R-SIX-LANE-V14-INTEGRATION-LEDGER.yaml"
            data = yaml.safe_load(target.read_text(encoding="utf-8"))
            data["program_status"]["integrated_champion"] = "PROMOTED"
            target.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assertEqual(receipt["result"], "FAIL")

    def test_private_report_copy_flag_fails_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "external-evidence/AR8R-DEEP-RESEARCH-20-22-INTAKE-V14.yaml"
            data = yaml.safe_load(target.read_text(encoding="utf-8"))
            data["reports"][0]["public_bytes_copied"] = True
            target.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assertEqual(receipt["result"], "FAIL")
        self.assertFalse(receipt["private_reports_excluded"])

    def test_private_report_file_insertion_fails_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            (copied / "external-evidence/deep-research-report-20.md").write_text(
                "unreviewed report bytes\n", encoding="utf-8"
            )
            receipt = validator.validate(ROOT, copied)
        self.assertEqual(receipt["result"], "FAIL")
        self.assertFalse(receipt["private_reports_excluded"])

    def test_b1_b4_protocol_identity_drift_fails_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "external-evidence/AR8R-DEEP-RESEARCH-20-22-INTAKE-V14.yaml"
            data = yaml.safe_load(target.read_text(encoding="utf-8"))
            for row in data["empirical_and_protocol_intake"]:
                if row.get("id") == "DR22-B1-B4-COVERAGE-GAP":
                    row["required_protocols"] = ["X1", "X2", "X3", "X4"]
            target.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assertEqual(receipt["result"], "FAIL")
        self.assertFalse(receipt["deep_research_22_b1_b4_gap_explicit"])

    def test_nested_ready_to_run_status_fails_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "external-evidence/AR8R-DEEP-RESEARCH-20-22-INTAKE-V14.yaml"
            data = yaml.safe_load(target.read_text(encoding="utf-8"))
            data["empirical_and_protocol_intake"][1]["nested_disposition"] = {
                "status": "READY_TO_RUN"
            }
            target.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assertEqual(receipt["result"], "FAIL")
        self.assertFalse(receipt["deep_research_22_readiness_fail_closed"])


class CurrentCentralIntakeTests(unittest.TestCase):
    """Current intake guards with finite fixtures; no original checker execution."""
    LEAN_FILES = (
        'specialist-a/source-files/lean/DeletionCriterion.lean',
        'specialist-a/source-files/lean/ObservationUniformity.lean',
        'specialist-a/intake-review/lean/DeletionCriterion.repaired.lean',
        'specialist-a/intake-review/lean/ObservationUniformity.repaired.lean',
        'specialist-b/source-files/SpecialistBBridgeSignatures.lean',
        'specialist-b/intake-review/lean/SpecialistBBridgeSignatures.repaired.lean',
    )

    def setUp(self):
        from copy import deepcopy
        import hashlib
        from unittest import mock
        self.validator = load_validator()
        v = self.validator
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = pathlib.Path(temporary.name)
        self.intake = self.root / v.INTAKE_REL
        self.intake.mkdir(parents=True)
        self.original_packages = deepcopy(v.PACKAGES)
        for relative in self.LEAN_FILES:
            source = ROOT / v.INTAKE_REL / relative
            target = self.intake / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(source.read_bytes())
        # Only specialist fixture manifests are substituted. The original
        # central contract, if still present, is deliberately not overridden.
        packages = deepcopy(v.PACKAGES)
        for lane in ('specialist-a', 'specialist-b'):
            source = self.intake / lane / 'source-files'
            (source / 'README.md').write_text('Synthetic current specialist fixture.\n', encoding='utf-8')
            rows = []
            for path in sorted(source.rglob('*')):
                if path.is_file():
                    rows.append(hashlib.sha256(path.read_bytes()).hexdigest() + '  ' + path.relative_to(source).as_posix())
            manifest = source / packages[lane]['manifest']
            manifest.write_text('\n'.join(rows) + '\n', encoding='utf-8')
            packages[lane] = dict(packages[lane], files=len(rows) + 1,
                                  manifest_sha256=hashlib.sha256(manifest.read_bytes()).hexdigest())
        patcher = mock.patch.object(v, 'PACKAGES', packages)
        patcher.start()
        self.addCleanup(patcher.stop)
        # This fixture's ordinary view is direct. No historical/native transport.
        for name, fn in {
            'digest_record_view_bytes': lambda p: p.read_bytes(),
            'digest_record_view_text': lambda p, encoding='utf-8': p.read_text(encoding=encoding),
            'digest_record_view_is_file': lambda p: p.is_file(),
            'digest_record_view_paths': lambda root, p: list(p.rglob('*')) if p.exists() else [],
        }.items():
            patcher = mock.patch.object(v, name, fn)
            patcher.start()
            self.addCleanup(patcher.stop)
        self.documents = {
            'AR8R-SIX-LANE-V14-INTEGRATION-LEDGER.yaml': {
                'lanes': [{'id': 'lane-' + str(i), 'owner_adoption': 'PENDING'} for i in range(6)],
                'program_status': {'repository_scientific_adoption': 'NONE', 'owner_adoption': 'PENDING',
                                   'integrated_champion': 'NONE', 'meniscus': 'MENISCUS_NOT_REACHED',
                                   'natural_closure': 'NOT_REACHED'},
            },
            'specialist-a/intake-review/LEAN_INTAKE_RECEIPT.json': {
                'originals': [{'status': 'PARSE_FAILED'}, {'status': 'PARSE_FAILED'}],
                'repairs': [
                    {'path': 'intake-review/lean/DeletionCriterion.repaired.lean',
                     'sha256': '8825df59e9ba945d61ec5db752087bf677f1d0fdd1f82cdb556b84732c8b2873',
                     'standalone_parse_elaboration_kernel': 'PASS'},
                    {'path': 'intake-review/lean/ObservationUniformity.repaired.lean',
                     'sha256': 'b46453b7f11f4593e3caf4e96cd2f48ad02af9df345586b720a7e9cf70f73324',
                     'standalone_parse_elaboration_kernel': 'PASS'},
                ],
                'repository_scientific_adoption': 'NONE', 'owner_adoption': 'PENDING',
            },
            'specialist-b/intake-review/LEAN_INTAKE_RECEIPT.json': {
                'original': {'status': 'PARSE_ELABORATION_FAILED'},
                'repair': {'standalone_parse_elaboration_kernel': 'PASS'},
                'repository_scientific_adoption': 'NONE', 'owner_adoption': 'PENDING',
            },
            'external-evidence/AR8R-DEEP-RESEARCH-20-22-INTAKE-V14.yaml': {
                'reports': [{'lane': 'DEEP_RESEARCH_' + str(i), 'public_bytes_copied': False}
                            for i in (20, 21, 22)],
                'authority_ceiling': deepcopy(v.EXPECTED_AUTHORITY_CEILING),
                'theological_and_metaphysical_sources': [
                    {'id': 'DR21-SPEECH-VOICE',
                     'locator': 'volume 12, pages 98 and 409 in the checked Islamweb digital rendering',
                     'prior_locator_12_98': 'CONFIRMED_PARALLEL_LOCUS'},
                    {'id': 'DR21-QIYAS-AL-AWLA', 'locator': 'volume 7 pages 362-363 in the checked digital rendering'},
                ],
                'empirical_and_protocol_intake': [
                    {'id': 'DR22-TENSOR-ARM-ONTOLOGY', 'representation_candidates_in_current_charter': 6,
                     'legacy_gate_description': '120 observations and five arms',
                     'status': 'BLOCKED_SPECIFICATION_AMBIGUITY'},
                    {'id': 'DR22-B1-B4-COVERAGE-GAP', 'status': 'NOT_ANSWERED_BY_CURRENT_REPORT',
                     'required_protocols': list(v.EXPECTED_B1_B4_PROTOCOLS)},
                ],
                'protocol_readiness': {'ready_to_run_count': 0, 'empirical_validation_claimed': False},
            },
        }
        for relative, value in self.documents.items():
            self.write_document(relative, value)
        self.write('external-evidence/AR8R-SIX-LANE-V14-SOURCING-CORRECTION.md', 'Synthetic correction fixture.\n')
        target = self.root / 'docs/project-closure/ar8r-v11/programs/tensor-and-bitter-lesson.md'
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text('BLOCKED_SPECIFICATION_AMBIGUITY\n', encoding='utf-8')

    def write(self, relative, text):
        target = self.intake / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding='utf-8')
        return target

    def write_document(self, relative, value):
        self.write(relative, json.dumps(value, indent=2) + '\n' if relative.endswith('.json')
                   else yaml.safe_dump(value, sort_keys=False))

    def validate(self):
        return self.validator.validate(self.root, self.intake)

    def forbid_central_history(self):
        from unittest import mock
        central = self.intake / 'central'
        for name in ('digest_record_view_bytes', 'digest_record_view_text', 'digest_record_view_is_file'):
            original = getattr(self.validator, name)
            def bounded(path, *args, original=original, **kwargs):
                self.assertFalse(pathlib.Path(path).is_relative_to(central), 'central history requested')
                return original(path, *args, **kwargs)
            patcher = mock.patch.object(self.validator, name, bounded)
            patcher.start()
            self.addCleanup(patcher.stop)
        original_paths = self.validator.digest_record_view_paths
        def bounded_paths(root, path):
            self.assertNotEqual(pathlib.Path(path), self.intake, 'whole-intake history requested')
            self.assertFalse(pathlib.Path(path).is_relative_to(central), 'central history requested')
            return original_paths(root, path)
        patcher = mock.patch.object(self.validator, 'digest_record_view_paths', bounded_paths)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_current_boundaries_pass_without_historical_central_package(self):
        receipt = self.validate()
        self.assertEqual(receipt['result'], 'PASS_CURRENT_INTAKE_AND_SPECIALIST_CUSTODY')
        self.assertEqual(receipt['historical_central_snapshot_validation'], 'NOT_RUN')
        self.assertEqual(receipt['source_file_counts'], {'specialist-a': 4, 'specialist-b': 3})
        self.assertEqual(receipt['issues'], [])
        self.assertFalse(receipt['specialist_a_checks_reproduced'])
        self.assertFalse((self.intake / 'central').exists())

    def test_original_specialist_contracts_remain_exact(self):
        self.assertEqual(self.original_packages, {
            'specialist-a': {'manifest': 'SHA256SUMS', 'manifest_sha256': 'f19fb30506f0d91cd0ababbe48c2f39ab0d075d5ae9b683fdf87717e26cf371f', 'files': 77},
            'specialist-b': {'manifest': 'MANIFEST.sha256', 'manifest_sha256': 'a3e32a6f8986fb9196c21e4ed9bb7d1be05b80050a063c201d9e71bbcbbd78dd', 'files': 29},
        })

    def test_unmanifested_current_central_file_is_not_a_count_requirement(self):
        self.write('central/source-files/current-note.txt', 'Current public note.\n')
        self.assertEqual(self.validate()['result'], 'PASS_CURRENT_INTAKE_AND_SPECIALIST_CUSTODY')

    def test_absent_central_never_requests_historical_bytes(self):
        self.forbid_central_history()
        self.assertEqual(self.validate()['result'], 'PASS_CURRENT_INTAKE_AND_SPECIALIST_CUSTODY')

    def test_current_central_privacy_uses_physical_bytes(self):
        self.write('central/source-files/current-note.txt', 'private: C:' + chr(92) + 'Users' + chr(92) + 'owner\n')
        self.forbid_central_history()
        receipt = self.validate()
        self.assertEqual(receipt['result'], 'FAIL')
        self.assertGreater(receipt['private_path_findings'], 0)

    def test_current_central_non_utf8_is_rejected(self):
        p = self.write('central/source-files/binary.txt', '')
        p.write_bytes(b'\xff')
        receipt = self.validate()
        self.assertEqual(receipt['result'], 'FAIL')
        self.assertTrue(any('non-UTF-8' in issue for issue in receipt['issues']))

    def test_current_central_structured_parse_failure_is_retained(self):
        self.write('central/source-files/bad.json', '{broken')
        receipt = self.validate()
        self.assertEqual(receipt['result'], 'FAIL')
        self.assertTrue(any('structured parse failure' in issue for issue in receipt['issues']))

    def test_current_central_symlink_is_rejected(self):
        target = self.write('ordinary.txt', 'Current ordinary file.\n')
        link = self.intake / 'central/source-files/link.txt'
        link.parent.mkdir(parents=True)
        link.symlink_to(target)
        receipt = self.validate()
        self.assertEqual(receipt['result'], 'FAIL')
        self.assertTrue(any('symlink' in issue for issue in receipt['issues']))

    def test_both_specialist_source_hash_guards_still_apply(self):
        for lane in ('specialist-a', 'specialist-b'):
            with self.subTest(lane=lane):
                p = self.intake / lane / 'source-files/README.md'
                original = p.read_bytes()
                p.write_bytes(original + b'drift\n')
                receipt = self.validate()
                self.assertEqual(receipt['result'], 'FAIL')
                self.assertGreater(receipt['source_hash_mismatches'], 0)
                p.write_bytes(original)

    def test_both_specialist_manifest_identity_guards_still_apply(self):
        for lane in ('specialist-a', 'specialist-b'):
            with self.subTest(lane=lane):
                p = self.intake / lane / 'source-files' / self.validator.PACKAGES[lane]['manifest']
                original = p.read_bytes()
                p.write_bytes(original + b'drift\n')
                receipt = self.validate()
                self.assertEqual(receipt['result'], 'FAIL')
                self.assertTrue(any('source manifest mismatch' in issue for issue in receipt['issues']))
                p.write_bytes(original)

    def test_default_replay_call_and_override_boundary_remain(self):
        from unittest import mock
        calls = []
        def inert(source, issues):
            calls.append(source)
            return True
        with mock.patch.object(self.validator, 'rerun_specialist_a', inert):
            receipt = self.validator.validate(self.root)
            self.assertEqual(receipt['result'], 'PASS_CURRENT_INTAKE_AND_SPECIALIST_CUSTODY')
            self.assertTrue(receipt['specialist_a_checks_reproduced'])
            self.assertEqual(calls, [self.intake / 'specialist-a/source-files'])
            calls.clear()
            receipt = self.validate()
            self.assertFalse(receipt['specialist_a_checks_reproduced'])
            self.assertEqual(calls, [])

    def test_default_source_hash_failure_still_prevents_replay(self):
        from unittest import mock
        p = self.intake / 'specialist-a/source-files/README.md'
        p.write_bytes(p.read_bytes() + b'drift\n')
        with mock.patch.object(self.validator, 'rerun_specialist_a', side_effect=AssertionError('unexpected replay')):
            receipt = self.validator.validate(self.root)
        self.assertEqual(receipt['result'], 'FAIL')
        self.assertGreater(receipt['source_hash_mismatches'], 0)
        self.assertFalse(receipt['specialist_a_checks_reproduced'])



class SpecialistBOriginalCustodyTests(unittest.TestCase):
    """Owner-local transport controls; actual original inputs are qualified separately."""
    def setUp(self):
        import hashlib
        from unittest import mock
        self.mock = mock
        self.v = load_validator()
        self.assertTrue(callable(getattr(self.v, 'specialist_b_source_custody', None)),
                        'mandatory Specialist B ordinary supplier is absent')
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = pathlib.Path(temporary.name)
        self.intake = self.root / self.v.INTAKE_REL
        self.intake.mkdir(parents=True)
        self.source = self.intake / 'specialist-b/source-files'
        self.prefix = (self.v.INTAKE_REL / 'specialist-b/source-files').as_posix()
        self.data = b'Ordinary synthetic source.\n'
        self.manifest = hashlib.sha256(self.data).hexdigest().encode() + b'  evidence.txt\n'
        self.expected = {'evidence.txt': hashlib.sha256(self.data).hexdigest()}
        self.contract = {'manifest': 'MANIFEST.sha256', 'files': 2,
                         'manifest_sha256': hashlib.sha256(self.manifest).hexdigest()}
        self.bodies = {'evidence.txt': self.data, 'MANIFEST.sha256': self.manifest}
        self.blobs = {name: hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest()
                      for name, body in self.bodies.items()}
        self.raw = b''.join(('100644 blob ' + self.blobs[name] + '\t' + self.prefix + '/' + name + '\0').encode()
                            for name in sorted(self.bodies))
        self.calls = []
        def parse(path, expected_digest, issues):
            self.calls.append(('manifest', path, expected_digest))
            self.assertEqual(path, self.source / 'MANIFEST.sha256')
            self.assertEqual(expected_digest, self.contract['manifest_sha256'])
            return dict(self.expected)
        def tree(root, *args):
            self.calls.append(('tree', args))
            self.assertEqual(args, ('ls-tree', '-rz', '--full-tree', self.v.DIGEST_RECORD_BASE,
                                    '--', self.prefix))
            return self.raw
        def bound(root, path, blob, initial):
            name = pathlib.PurePosixPath(path).relative_to(self.prefix).as_posix()
            self.assertIsNone(initial)
            self.assertEqual(blob, self.blobs[name])
            self.calls.append(('body', name))
            return self.bodies[name]
        self.parse = parse
        self.bound = bound
        for name, value in {'PACKAGES': dict(self.v.PACKAGES, **{'specialist-b': self.contract}),
                            'parse_manifest': parse, '_administrative_git': tree,
                            '_digest_record_bound_bytes': bound}.items():
            patch = mock.patch.object(self.v, name, value); patch.start(); self.addCleanup(patch.stop)

    def custody(self):
        return self.v.specialist_b_source_custody(self.root, self.intake)

    def test_absent_exact_input_is_materialized_once_and_removed(self):
        with self.custody() as source:
            self.assertNotEqual(source, self.source)
            self.assertEqual({p.name: p.read_bytes() for p in source.iterdir()}, self.bodies)
            self.assertFalse(any(p.is_symlink() for p in source.iterdir()))
            self.assertEqual([x[0] for x in self.calls], ['manifest', 'tree', 'body', 'body'])
        self.assertFalse(source.exists())
        self.assertFalse(self.source.exists())

    def test_present_partial_or_corrupt_source_is_not_replaced(self):
        self.source.mkdir(parents=True)
        (self.source / 'unexpected.txt').write_text('corrupt current source')
        with self.custody() as source:
            self.assertEqual(source, self.source)
            self.assertEqual(self.calls, [])
            self.assertEqual((source / 'unexpected.txt').read_text(), 'corrupt current source')

    def test_required_native_manifest_refusal_propagates(self):
        with self.mock.patch.object(self.v, 'parse_manifest', side_effect=OSError('native176 unavailable')):
            with self.assertRaises(OSError):
                with self.custody(): pass
        self.assertEqual(self.calls, [])

    def test_original_manifest_error_or_count_cannot_be_skipped(self):
        def failed(path, expected, issues):
            issues.append('manifest mismatch')
            return self.expected
        with self.mock.patch.object(self.v, 'parse_manifest', failed):
            with self.assertRaises(ValueError):
                with self.custody(): pass
        self.expected.clear()
        with self.assertRaises(ValueError):
            with self.custody(): pass
        self.assertFalse(any(c[0] == 'body' for c in self.calls))

    def test_tree_mode_membership_and_duplicate_are_checked(self):
        original = self.raw
        for raw in (original.replace(b'100644', b'100755', 1), original + original.split(b'\0')[0] + b'\0',
                    original.replace(b'evidence.txt', b'other.txt'), b''):
            with self.subTest(raw=raw):
                self.raw = raw
                with self.assertRaises(ValueError):
                    with self.custody(): pass
        self.assertFalse(any(c[0] == 'body' for c in self.calls))

    def test_native_body_or_index_failure_cannot_be_skipped(self):
        with self.mock.patch.object(self.v, '_digest_record_bound_bytes', side_effect=ValueError('index changed')):
            with self.assertRaises(ValueError):
                with self.custody(): pass
        self.assertFalse(self.source.exists())

    def test_every_original_body_hash_is_required_before_yield(self):
        for name in self.bodies:
            with self.subTest(name=name):
                def wrong(root, path, blob, initial):
                    body = self.bound(root, path, blob, initial)
                    return body + b'drift' if path.endswith('/' + name) else body
                with self.mock.patch.object(self.v, '_digest_record_bound_bytes', wrong):
                    with self.assertRaises(ValueError):
                        with self.custody(): pass
        self.assertFalse(self.source.exists())

    def test_missing_source_cannot_use_an_unrelated_intake_root(self):
        unrelated = self.root / 'other-intake'; unrelated.mkdir()
        with self.assertRaises(ValueError):
            with self.v.specialist_b_source_custody(self.root, unrelated): pass
        self.assertEqual(self.calls, [])

    def test_current_source_appearing_during_authentication_refuses(self):
        def appearing(root, path, blob, initial):
            value = self.bound(root, path, blob, initial)
            self.source.mkdir(parents=True, exist_ok=True)
            return value
        with self.mock.patch.object(self.v, '_digest_record_bound_bytes', appearing):
            with self.assertRaises(ValueError):
                with self.custody(): pass
        self.assertTrue(self.source.is_dir())

    def test_current_source_appearing_during_validation_refuses(self):
        with self.assertRaises(ValueError):
            with self.custody() as supplied:
                self.source.mkdir(parents=True)
        self.assertFalse(supplied.exists())
        self.assertTrue(self.source.is_dir())

    def test_lexical_and_symlink_repository_aliases_refuse(self):
        link = self.root / 'linked'; link.symlink_to(self.root, target_is_directory=True)
        with self.assertRaises(ValueError):
            with self.v.specialist_b_source_custody(link, link / self.v.INTAKE_REL): pass
        lexical = self.root / 'missing' / '..'
        with self.assertRaises(ValueError):
            with self.v.specialist_b_source_custody(lexical, lexical / self.v.INTAKE_REL): pass
        self.assertEqual(self.calls, [])

    def test_existing_source_symlink_is_not_followed(self):
        outside = self.root / 'outside'; outside.mkdir()
        self.source.parent.mkdir(parents=True)
        self.source.symlink_to(outside, target_is_directory=True)
        with self.assertRaises(ValueError):
            with self.custody(): pass
        self.assertEqual(self.calls, [])


if __name__ == "__main__":
    unittest.main()
