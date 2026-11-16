import importlib.util
import json
import pathlib
import shutil
import tempfile
import unittest

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_pmr007_deep_bw_cj_semantic_reissue.py"


def load_validator():
    if not SCRIPT.is_file():
        raise AssertionError("Deep BW-CJ semantic-reissue validator is missing")
    spec = importlib.util.spec_from_file_location("pmr007_bw_cj_validator", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Pmr007DeepBwCjSemanticReissueTests(unittest.TestCase):
    def copy_surface(self, validator, temporary):
        copied = pathlib.Path(temporary) / "reissue"
        shutil.copytree(ROOT / validator.REISSUE_REL, copied)
        receipt = pathlib.Path(temporary) / "receipt.yaml"
        shutil.copy2(ROOT / validator.PROVENANCE_RECEIPT_REL, receipt)
        return copied, receipt

    def test_reissue_passes_only_at_the_proposal_custody_ceiling(self):
        validator = load_validator()
        receipt = validator.validate(ROOT)

        self.assertEqual(receipt["result"], "PASS_WITH_SEMANTIC_REISSUE_CEILING")
        self.assertEqual(receipt["source_files"], 40)
        self.assertEqual(receipt["source_hash_mismatches"], 0)
        self.assertTrue(receipt["source_manifest_exact"])
        self.assertEqual(receipt["structured_parse_errors"], 0)
        self.assertEqual(receipt["private_path_findings"], 0)
        self.assertEqual(receipt["indexed_results"], 14)
        self.assertTrue(receipt["authority_ceiling_exact"])
        self.assertTrue(receipt["deep_bv_baseline_unchanged"])
        self.assertTrue(receipt["v3_checker_reproduced"])
        self.assertTrue(receipt["v3_result_semantic_match"])
        self.assertTrue(receipt["v3_result_byte_match"])
        self.assertTrue(receipt["v1_false_pass_detected"])

    def test_source_hash_drift_fails_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied, receipt = self.copy_surface(validator, temporary)
            target = copied / "source-files/PROPOSAL/theorems/PMR-007_DEEP_CJ_PMR-007-FSGW-1_REISSUE_V1.md"
            target.write_text(target.read_text(encoding="utf-8") + "\ndrift\n", encoding="utf-8")
            result = validator.validate(ROOT, copied, receipt)

        self.assertEqual(result["result"], "FAIL")
        self.assertGreater(result["source_hash_mismatches"], 0)

    def test_authority_promotion_fails_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied, receipt = self.copy_surface(validator, temporary)
            document = yaml.safe_load(receipt.read_text(encoding="utf-8"))
            document["proposal_boundary"]["owner_adoption"] = "ADOPTED"
            document["proposal_boundary"]["meniscus"] = "MENISCUS_REACHED"
            receipt.write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8")
            result = validator.validate(ROOT, copied, receipt)

        self.assertEqual(result["result"], "FAIL")
        self.assertFalse(result["authority_ceiling_exact"])

    def test_identity_omission_fails_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied, receipt = self.copy_surface(validator, temporary)
            index = copied / "source-files/PROPOSAL/ledgers/RESULT_INDEX.yaml"
            document = yaml.safe_load(index.read_text(encoding="utf-8"))
            document["results"] = document["results"][:-1]
            index.write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8")
            result = validator.validate(ROOT, copied, receipt)

        self.assertEqual(result["result"], "FAIL")
        self.assertNotEqual(result["indexed_results"], 14)

    def test_checker_result_promotion_or_tamper_fails_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied, receipt = self.copy_surface(validator, temporary)
            result_path = copied / "intake-review/checks/post_bv_consolidated_recheck_v3_results.json"
            document = json.loads(result_path.read_text(encoding="utf-8"))
            document["overall_pass"] = False
            result_path.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
            result = validator.validate(ROOT, copied, receipt)

        self.assertEqual(result["result"], "FAIL")
        self.assertFalse(result["v3_result_semantic_match"])

    def test_v3_checker_semantic_mutation_fails_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied, receipt = self.copy_surface(validator, temporary)
            checker = copied / "intake-review/checks/post_bv_consolidated_recheck_v3.py"
            text = checker.read_text(encoding="utf-8")
            text = text.replace(
                'return projection(left) == projection(right) and left["target"] != right["target"]',
                'return projection(left) == projection(right) or left["target"] != right["target"]',
                1,
            )
            checker.write_text(text, encoding="utf-8")
            result = validator.validate(ROOT, copied, receipt)

        self.assertEqual(result["result"], "FAIL")
        self.assertFalse(result["v3_checker_reproduced"])

    def test_unmanifested_private_locator_fails_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied, receipt = self.copy_surface(validator, temporary)
            leaked = copied / "source-files/UNMANIFESTED.txt"
            separator = chr(92)
            leaked.write_text(
                "private: C:%sUsers%sowner%sevidence.txt\n" % (separator, separator, separator),
                encoding="utf-8",
            )
            result = validator.validate(ROOT, copied, receipt)

        self.assertEqual(result["result"], "FAIL")
        self.assertFalse(result["source_coverage_exact"])
        self.assertGreater(result["private_path_findings"], 0)


# Additive consumer controls. These fixtures are synthetic, not custody evidence.
import contextlib as _rc_contextlib
import hashlib as _rc_hashlib
import sys as _rc_sys
import types as _rc_types
import unittest.mock as _rc_mock

_RC_POPULATIONS = {'BV': {'names': ['AR8R_PMR007_CURRENT_CONTINUATION_AFTER_DEEP_BV.yaml',
                  'AR8R_PMR007_CURRENT_CONTINUATION_AFTER_DEEP_BV.yaml.sha256',
                  'AR8R_PMR007_DEEP_BL_BV_BOUNDARY_REPORT.md',
                  'AR8R_PMR007_DEEP_BL_BV_BOUNDARY_REPORT.md.sha256',
                  'CURRENT_STATE_AFTER_DEEP_BV.yaml',
                  'EXTERNAL_PDF_CUSTODY_AND_METHOD_NOTE.md',
                  'EXTERNAL_PDF_CUSTODY_SANITIZED.json',
                  'LIVE_GITHUB_AUTHORITY_AFTER_BU.json',
                  'PMR-007_DEEP_BL_BU_OWNER_REPORT.md',
                  'PMR-007_DEEP_BV_ADMISSION_HASHES.sha256',
                  'PMR-007_DEEP_BV_ADMISSION_OVERLAY.yaml',
                  'PMR-007_DEEP_BV_V1_COLD_AUDIT.md',
                  'PMR-007_DEEP_BV_V2_DISTINCT_FRESH_REREVIEW.md',
                  'PMR-007_DEEP_BV_V2_REPAIR_LOG.md',
                  'PMR-007_DEEP_ROUND_BV_COMMON_INTERVENTION_IDENTIFIABILITY_V2.md',
                  'PMR007_DEEP_BV_COMMON_INTERVENTION_MODELS_V2.yaml',
                  'PMR007_DEEP_MENISCUS_CROSSWALK_A_BV_V4.yaml',
                  'PMR007_POST_BK_BURDEN_DELTA_BL_BV_V4.yaml',
                  'PMR007_POST_BK_FORMALIZATION_QUEUE_THROUGH_BV_V4.yaml',
                  'PMR007_POST_BK_PROPOSED_RESULT_INDEX_THROUGH_BV_V4.json',
                  'PMR007_POST_BK_PROPOSED_RESULT_INDEX_THROUGH_BV_V4.yaml',
                  'pmr007_deep_bv_distinct_partition_experiment_rereview_results.json'],
        'selected': ['AR8R_PMR007_CURRENT_CONTINUATION_AFTER_DEEP_BV.yaml',
                     'CURRENT_STATE_AFTER_DEEP_BV.yaml',
                     'PMR-007_DEEP_BV_ADMISSION_HASHES.sha256',
                     'PMR-007_DEEP_BV_ADMISSION_OVERLAY.yaml',
                     'PMR007_POST_BK_BURDEN_DELTA_BL_BV_V4.yaml',
                     'PMR007_POST_BK_FORMALIZATION_QUEUE_THROUGH_BV_V4.yaml']},
 'BW': {'names': ['MANIFEST.json',
                  'OWNER_ADOPTION_STATUS.yaml',
                  'PRIVATE_DATA_EXCLUSION_REPORT.json',
                  'PRIVATE_DATA_EXCLUSION_REPORT.md',
                  'PROPOSAL/AR8R_PMR007_DEEP_BW_CJ_BOUNDARY_REPORT.md',
                  'PROPOSAL/audits/POST_BV_COLD_AUDIT_AND_REPAIR_SUMMARY.md',
                  'PROPOSAL/AUTHORITY_AND_CUSTODY_RECEIPT.md',
                  'PROPOSAL/checks/post_bv_consolidated_recheck_results.json',
                  'PROPOSAL/checks/post_bv_consolidated_recheck.py',
                  'PROPOSAL/ledgers/BURDEN_DELTA_BW_CJ.yaml',
                  'PROPOSAL/ledgers/CROSSWALK_BV_CJ.yaml',
                  'PROPOSAL/ledgers/CURRENT_STATE.yaml',
                  'PROPOSAL/ledgers/FORMALIZATION_QUEUE.yaml',
                  'PROPOSAL/ledgers/FRONTIER_ROTATION.yaml',
                  'PROPOSAL/ledgers/LIVE_REPOSITORY_AUTHORITY.json',
                  'PROPOSAL/ledgers/RESULT_INDEX.json',
                  'PROPOSAL/ledgers/RESULT_INDEX.yaml',
                  'PROPOSAL/ledgers/SOURCE_USE_REGISTER.yaml',
                  'PROPOSAL/ledgers/TIMING_CUSTODY.yaml',
                  'PROPOSAL/ORIGINAL_EPHEMERAL_BYTES_LOSS_AND_REISSUE_NOTE.md',
                  'PROPOSAL/rereviews/POST_BV_FRESH_REREVIEW_SUMMARY.md',
                  'PROPOSAL/source_notes/PROPER_FUNCTION_AND_ONTOLOGY_ADJUDICATION.md',
                  'PROPOSAL/source_notes/SOURCE_CUSTODY_AND_AUTHORITY.md',
                  'PROPOSAL/theorems/PMR-007_DEEP_BW_PMR-007-TCIS-1_REISSUE_V1.md',
                  'PROPOSAL/theorems/PMR-007_DEEP_BX_PMR-007-MBAC-1_REISSUE_V1.md',
                  'PROPOSAL/theorems/PMR-007_DEEP_BY_PMR-007-SWAC-1_REISSUE_V1.md',
                  'PROPOSAL/theorems/PMR-007_DEEP_BZ_PMR-007-BAXE-1_REISSUE_V1.md',
                  'PROPOSAL/theorems/PMR-007_DEEP_CA_PMR-007-RCIG-1_REISSUE_V1.md',
                  'PROPOSAL/theorems/PMR-007_DEEP_CB_PMR-007-CRFW-1_REISSUE_V1.md',
                  'PROPOSAL/theorems/PMR-007_DEEP_CC_PMR-007-CSQF-1_REISSUE_V1.md',
                  'PROPOSAL/theorems/PMR-007_DEEP_CD_PMR-007-NOPF-1_REISSUE_V1.md',
                  'PROPOSAL/theorems/PMR-007_DEEP_CE_PMR-007-CDPS-1_REISSUE_V1.md',
                  'PROPOSAL/theorems/PMR-007_DEEP_CF_PMR-007-ABIC-1_REISSUE_V1.md',
                  'PROPOSAL/theorems/PMR-007_DEEP_CG_PMR-007-SICM-1_REISSUE_V1.md',
                  'PROPOSAL/theorems/PMR-007_DEEP_CH_PMR-007-OIOT-1_REISSUE_V1.md',
                  'PROPOSAL/theorems/PMR-007_DEEP_CI_PMR-007-SCSI-1_REISSUE_V1.md',
                  'PROPOSAL/theorems/PMR-007_DEEP_CJ_PMR-007-FSGW-1_REISSUE_V1.md',
                  'README.md',
                  'ROLLBACK_AND_NONADOPTION.md',
                  'SHA256SUMS'],
        'selected': ['OWNER_ADOPTION_STATUS.yaml',
                     'PROPOSAL/ledgers/BURDEN_DELTA_BW_CJ.yaml',
                     'PROPOSAL/ledgers/CURRENT_STATE.yaml',
                     'PROPOSAL/ledgers/FORMALIZATION_QUEUE.yaml',
                     'PROPOSAL/ledgers/FRONTIER_ROTATION.yaml',
                     'PROPOSAL/ledgers/SOURCE_USE_REGISTER.yaml',
                     'PROPOSAL/ledgers/TIMING_CUSTODY.yaml']}}
_RC_IDS = [
    "PMR-007-TCIS-1", "PMR-007-MBAC-1", "PMR-007-SWAC-1", "PMR-007-BAXE-1",
    "PMR-007-RCIG-1", "PMR-007-CRFW-1", "PMR-007-CSQF-1", "PMR-007-NOPF-1",
    "PMR-007-CDPS-1", "PMR-007-ABIC-1", "PMR-007-SICM-1", "PMR-007-OIOT-1",
    "PMR-007-SCSI-1", "PMR-007-FSGW-1",
]
_RC_ROUNDS = ["BW", "BX", "BY", "BZ", "CA", "CB", "CC", "CD", "CE", "CF", "CG", "CH", "CI", "CJ"]


def _rc_sha(body):
    return _rc_hashlib.sha256(body).hexdigest()


def _rc_load_validator(kind):
    name = "validate_pmr007_deep_" + ("bv" if kind == "BV" else "bw_cj") + "_semantic_reissue.py"
    script = ROOT / "scripts" / name
    # The historical/native provider layer is an explicitly inert leaf here.
    # Real validator loops and typed receipt/replay predicates are not replaced.
    leaf = _rc_types.ModuleType("resolve_t20_v6_source")
    leaf.digest_record_view_bytes = lambda path: pathlib.Path(path).read_bytes()
    leaf.digest_record_view_text = lambda path, encoding="utf-8": pathlib.Path(path).read_text(encoding=encoding)
    leaf.digest_record_view_is_file = lambda path: pathlib.Path(path).is_file()
    leaf.digest_record_view_paths = lambda root, source: pathlib.Path(source).rglob("*")
    @_rc_contextlib.contextmanager
    def no_supply(root, source, source_rel):
        yield {}
    leaf.reissue_administrative_custody = no_supply
    spec = importlib.util.spec_from_file_location("reissue_consumer_fixture_" + kind, script)
    module = importlib.util.module_from_spec(spec)
    with _rc_mock.patch.dict(_rc_sys.modules, {"resolve_t20_v6_source": leaf}):
        spec.loader.exec_module(module)
    return module


class _ReissueConsumerFixture:
    """Small complete 22/40 synthetic surfaces; never execute a checker file."""
    def __init__(self, case, kind, temporary):
        self.case, self.kind = case, kind
        self.root = pathlib.Path(temporary) / "repo"
        self.module = _rc_load_validator(kind)
        self.reissue = self.root / self.module.REISSUE_REL
        self.source = self.root / self.module.SOURCE_REL
        self.supplied_dir = pathlib.Path(temporary) / "supplied"
        self.supplied = {}
        self.supply_error = False
        self.replay_mode = "exact"
        self.replay_calls = 0
        self.context_calls = 0
        self.child_valid = True
        self.names = tuple(_RC_POPULATIONS[kind]["names"])
        self.selected = tuple(_RC_POPULATIONS[kind]["selected"])
        self.bodies = {
            name: b"{}\n" if name.endswith(".json") else b"fixture: true\n"
            if name.endswith((".yaml", ".yml")) else b"inert fixture\n"
            for name in self.names
        }
        if kind == "BV":
            self.bodies["PMR007_POST_BK_PROPOSED_RESULT_INDEX_THROUGH_BV_V4.yaml"] = yaml.safe_dump({
                "results": [{"round": "Deep " + r, "identity": "PMR-007-CIID-1" if r == "BV" else None}
                            for r in ["BL", "BM", "BN", "BO", "BP", "BQ", "BR", "BS", "BT", "BU", "BV"]],
                "custody_class": "SEMANTIC_REISSUE_OR_REGENERATED_CUSTODY_COPY",
                "original_bytes_proven_preserved": False,
            }).encode()
            self.bodies["pmr007_deep_bv_distinct_partition_experiment_rereview_results.json"] = json.dumps({
                "independently_rerun_in_custody_repair": False,
                "authority_ceiling": "CUSTODY_TRANSCRIPTION_NOT_EXECUTABLE_REPRODUCTION",
            }).encode()
        else:
            self.bodies["PROPOSAL/ledgers/RESULT_INDEX.yaml"] = yaml.safe_dump({
                "custody_class": "SEMANTIC_REISSUE_OR_REGENERATED_CUSTODY_COPY",
                "results": [{"round": r, "identity": i, "historical_identity": "NONE",
                             "general_mathematical_novelty": 0, "owner_adoption": "PENDING",
                             "external_review": "OPEN", "repository_adoption": "NONE",
                             "custody_exact_original_bytes": False}
                            for r, i in zip(_RC_ROUNDS, _RC_IDS)],
            }, sort_keys=False).encode()
            self.bodies["PROPOSAL/checks/post_bv_consolidated_recheck.py"] = (
                b'# inert fixture: "matched_twins":20000\n# "personal_impersonal_twins":20000\n'
            )
            checks = self.reissue / "intake-review/checks"
            self._write(checks / "post_bv_consolidated_recheck_v2.py", b"# inert V2 fixture\n")
            self._write(checks / "post_bv_consolidated_recheck_v3.py", b"# inert V3 fixture\n")
            self.module.EXPECTED_V2_CHECKER_SHA256 = _rc_sha(b"# inert V2 fixture\n")
            self.module.EXPECTED_V2_RESULT_SHA256 = "b" * 64
            self.module.EXPECTED_V3_CHECKER_SHA256 = _rc_sha(b"# inert V3 fixture\n")
            results = {r: {"pass": True} for r in _RC_ROUNDS}
            common = {"witness_failures": 0, "target_leak_false_positives": 0,
                      "profile_change_false_positives": 0, "same_target_false_positives": 0,
                      "predicate_mutation_receipt": {"all_declared_mutants_killed": True}}
            results["CI"].update(json.loads(json.dumps(common)), authority="EXHAUSTIVE_DECLARED_FINITE_SIGNATURE_WITNESS_NOT_ARCHITECTURE_IMPLEMENTATION",
                                 declared_profiles=15625, exhaustive_target_fibre_witnesses=15625)
            results["CJ"].update(json.loads(json.dumps(common)), authority="EXHAUSTIVE_ELIGIBLE_FINITE_SIGNATURE_WITNESS_NOT_ARCHITECTURE_IMPLEMENTATION",
                                 declared_profiles=6561, eligible_profiles=72, eligibility_recheck_failures=0,
                                 exhaustive_personal_impersonal_witnesses=72)
            self.replay_document = {"overall_pass": True, "schema": "pmr007-post-bv-consolidated-recheck-v3",
                "v2_ci_cj_disposition": "REJECTED_TAUTOLOGICAL_REPETITION_NOT_INDEPENDENT_EVIDENCE",
                "authority": "BOUNDED_FINITE_SIGNATURE_WITNESSES_ONLY", "results": results}
            self._write_replay_result()
        for name, body in self.bodies.items():
            self._write(self.source / name, body)
        hashes = {name: _rc_sha(body) for name, body in self.bodies.items()}
        manifest = "".join(f"{hashes[name]}  source-files/{name}\n" for name in self.names).encode()
        self._write(self.reissue / "SOURCE_SHA256SUMS", manifest)
        if kind == "BV":
            self.module.EXPECTED_SOURCE_HASHES = hashes
        else:
            self.module.EXPECTED_SOURCE_MANIFEST_SHA256 = _rc_sha(manifest)
        self.provenance = self._provenance()
        self._write_provenance()

    @staticmethod
    def _write(path, body):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(body)

    def _write_provenance(self):
        self._write(self.root / self.module.PROVENANCE_RECEIPT_REL,
                    yaml.safe_dump(self.provenance, sort_keys=False).encode())

    def _write_replay_result(self):
        body = (json.dumps(self.replay_document, indent=2) + "\n").encode()
        self._write(self.reissue / "intake-review/checks/post_bv_consolidated_recheck_v3_results.json", body)
        self.module.EXPECTED_V3_RESULT_SHA256 = _rc_sha(body)

    def _provenance(self):
        boundary = {"owner_adoption": "PENDING", "external_review": "OPEN",
                    "repository_scientific_adoption": "NONE", "integrated_champion": "NONE",
                    "meniscus": "MENISCUS_NOT_REACHED", "natural_closure": "NOT_REACHED",
                    "historical_duration_effect": "NONE", "theorem_origin_authority_effect": "NONE"}
        integration = {"private_archive_committed": False, "source_pdf_bytes_committed": False,
                       "raw_chat_or_activity_committed": False}
        if self.kind == "BV":
            boundary.update(deep_rounds_summarized=11, range="Deep BL through Deep BV", only_printed_identity="PMR-007-CIID-1",
                deep_bl_through_bu_individual_original_packets="UNAVAILABLE",
                deep_bv_original_theorem_model_checker_audit_repair_rereview_bytes="UNAVAILABLE",
                deep_bv_reported_counts="CUSTODY_TRANSCRIPTION_NOT_EXECUTABLE_REPRODUCTION",
                independently_rerun_from_reissue=False, historical_identity_assigned=False,
                historical_theorem_origin_credit=False, general_novelty_credit="NOT_GRANTED", lean_source_or_kernel_claim="NONE")
            integration["base_sha"] = "ca504400ea7e241d57ddf6db1beadc01d1e77f3b"
            return {"schema": "ar8r-pmr007-deep-bl-bv-custody-reissue-v1",
                "source_reissue": {"filename": "AR8R_PMR007_DEEP_BL_BV_CUSTODY_REISSUE_V1.zip",
                    "sha256": "6ed381f16d2bbd46dd31a987bdc2b9552aa2ae083874dde650e75ff0794f27d3",
                    "bytes": 21618877, "archive_members": 2666, "manifest_members": 2666,
                    "unsafe_paths": 0, "duplicate_paths": 0, "decompression_errors": 0,
                    "manifest_hash_mismatches": 0, "yaml_files_parsed": 574, "json_files_parsed": 368,
                    "structured_parse_errors": 0, "round_trip_restoration": "PASS"},
                "response_linked_custody": {"total": 28, "exact_original_files": 2,
                    "exact_original_filenames": ["EXTERNAL_PDF_CUSTODY_AND_METHOD_NOTE.md", "EXTERNAL_PDF_CUSTODY_SANITIZED.json"],
                    "regenerated_custody_copies": 26, "original_byte_sequences_still_unavailable": 26},
                "repository_copy": {"path": "docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-bl-bv-semantic-reissue/source-files",
                    "source_files": 22, "source_files_copied_byte_exact_from_reissue": True,
                    "original_deep_bl_bv_bytes_claimed_for_all_source_files": False,
                    "role": "PUBLIC_SAFE_SEMANTIC_REISSUE_PROPOSAL_CUSTODY"},
                "exact_baseline_preserved": {"path": "docs/project-closure/ar8r-v11/post-merge-proposals/pmr007-deep-a-bk",
                    "source_archive_sha256": "a7271391bbc7294128597a0798b0dd644bd79bdf4d9d57b3b918b2fa912a32b5",
                    "modified_by_this_import": False}, "proposal_boundary": boundary, "integration": integration}
        boundary.update(result_count=14, range="Deep BW through Deep CJ", identities=list(_RC_IDS),
            original_ephemeral_files="UNAVAILABLE", semantic_reissue_only=True, historical_identity="NONE",
            general_mathematical_novelty=0, lean_parse_elaboration_kernel="NOT_RUN")
        integration["base_sha"] = "a8142c3caf103ee46a2cd759c3d319b1e29b40da"
        return {"schema": "ar8r-pmr007-deep-bw-cj-custody-reissue-v1",
            "source_reissue": {"sha256": "215be89bdca4a33d4272182b2eb21d956290691ac148b1c8df92db9fde96a4af",
                "bytes": 61145, "archive_members": 40, "unsafe_paths": 0, "duplicate_paths": 0,
                "crc_failures": 0, "byte_mismatches": 0, "structured_parse_errors": 0, "round_trip_restoration": "PASS"},
            "repository_copy": {"source_files": 40, "source_files_copied_byte_exact_from_reissue": True,
                "original_ephemeral_deep_bw_cj_bytes_claimed": False}, "proposal_boundary": boundary,
            "independent_intake_recheck": {"v1_parsed_result_reproduced": True, "v1_disposition": "REJECTED_FALSE_PASS_CI_CJ",
                "v1_defects": ["CI_TWIN_COUNTER_PREFILLED_BODY_NOT_EXECUTED", "CJ_TWIN_COUNTER_PREFILLED_BODY_NOT_EXECUTED", "PLATFORM_NATIVE_NEWLINE_OUTPUT_DRIFT"],
                "v2_checker_sha256": self.module.EXPECTED_V2_CHECKER_SHA256,
                "v2_result_sha256": self.module.EXPECTED_V2_RESULT_SHA256,
                "v2_executed_on_intake": True, "v2_parsed_result_reproduces_exactly": True,
                "v2_disposition": "REJECTED_TAUTOLOGICAL_REPETITION_NOT_INDEPENDENT_EVIDENCE",
                "v3_checker_sha256": self.module.EXPECTED_V3_CHECKER_SHA256,
                "v3_result_sha256": self.module.EXPECTED_V3_RESULT_SHA256,
                "v3_executed_on_intake": True, "v3_parsed_result_reproduces_exactly": True,
                "declared_finite_checks": 14, "finite_checks_passed": 14, "ci_exhaustive_signature_witnesses": 15625,
                "ci_negative_controls_executed": 46875, "cj_eligible_signature_witnesses": 72,
                "cj_negative_controls_executed": 216, "predicate_mutant_families_killed_per_round": 3,
                "authority_ceiling": "CONSTRUCTED_FINITE_SIGNATURE_WITNESSES_ONLY",
                "scientific_disposition": {"BW_THROUGH_CH": "GAP_PENDING_PER_RESULT_INDEPENDENT_REVIEW",
                    "CI": "GAP_CONDITIONAL_COUNTERMODEL_ARCHITECTURE_IMPLEMENTATION_UNVERIFIED",
                    "CJ": "GAP_CONDITIONAL_COUNTERMODEL_ARCHITECTURE_IMPLEMENTATION_UNVERIFIED"}},
            "integration": integration}

    def remove_selected(self, names=None):
        for name in self.selected if names is None else names:
            self.case.assertIn(name, self.selected)
            path = self.source / name
            supply = self.supplied_dir / name
            self._write(supply, path.read_bytes())
            path.unlink()  # Synthetic temporary file only.
            self.supplied[name] = supply

    @_rc_contextlib.contextmanager
    def supply(self, root, source, source_rel):
        self.context_calls += 1
        self.case.assertEqual(pathlib.Path(root), self.root)
        self.case.assertEqual(pathlib.Path(source), self.source)
        self.case.assertEqual(pathlib.Path(source_rel), self.module.SOURCE_REL)
        if self.supply_error:
            raise ValueError("inert native supply refused")
        yield dict(self.supplied)

    def replay(self, argv, **kwargs):
        self.replay_calls += 1
        self.case.assertEqual(argv[0], _rc_sys.executable)
        self.case.assertEqual(len(argv), 2)
        checker = pathlib.Path(argv[1])
        self.case.assertEqual(checker.name, "post_bv_consolidated_recheck_v3.py")
        self.case.assertEqual(checker.read_bytes(), b"# inert V3 fixture\n")
        self.case.assertEqual((checker.parent / "post_bv_consolidated_recheck_v2.py").read_bytes(), b"# inert V2 fixture\n")
        self.case.assertEqual(pathlib.Path(kwargs["cwd"]), checker.parent)
        self.case.assertEqual(kwargs["timeout"], 120)
        self.case.assertIs(kwargs["check"], False)
        self.case.assertIs(kwargs["capture_output"], True)
        self.case.assertIs(kwargs["text"], True)
        self.case.assertEqual(kwargs["env"]["PYTHONUTF8"], "1")
        if self.replay_mode == "exit-failure":
            return _rc_types.SimpleNamespace(returncode=1)
        if self.replay_mode != "no-output":
            body = (self.reissue / "intake-review/checks/post_bv_consolidated_recheck_v3_results.json").read_bytes()
            if self.replay_mode == "byte-drift":
                body += b"\n"
            elif self.replay_mode == "semantic-drift":
                document = json.loads(body)
                document["overall_pass"] = False
                body = json.dumps(document).encode()
            self._write(checker.parent / "post_bv_consolidated_recheck_v3_results.json", body)
        return _rc_types.SimpleNamespace(returncode=0)

    def run(self):
        with _rc_contextlib.ExitStack() as stack:
            stack.enter_context(_rc_mock.patch.object(self.module, "reissue_administrative_custody", self.supply, create=True))
            if self.kind == "BV":
                receipt = {"schema": "ar8r-pmr007-public-correction-validation-receipt-v1",
                    "result": "PASS_CURRENT_CORRECTIONS_ONLY", "validation_scope": "CURRENT_CORRECTION_AND_AUTHORITY_BOUNDARIES",
                    "historical_snapshot_validation": "NOT_RUN", "current_public_files_checked": 0,
                    "current_public_non_utf8_files": 0, "private_paths_in_current_public_sources": 0,
                    "repository_source_rows": 12, "repository_source_exact_set": True, "repository_source_unsafe_paths": 0,
                    "repository_source_malformed_rows": 0, "repository_source_hash_mismatches": 0,
                    "crosswalk_values_exact": True, "authority_ceiling_exact": self.child_valid,
                    "private_exclusion_rows": 4, "private_paths_in_public_corrections": 0,
                    "self_contained_public_rereview_reproduction": False, "issues": []}
                stack.enter_context(_rc_mock.patch.object(self.module, "load_bk_validator",
                    return_value=_rc_types.SimpleNamespace(validate=lambda root: receipt)))
            else:
                receipt = {"result": "PASS_WITH_SEMANTIC_REISSUE_CEILING" if self.child_valid else "FAIL",
                           "source_hash_mismatches": 0, "source_manifest_exact": True}
                stack.enter_context(_rc_mock.patch.object(self.module, "load_bv_validator",
                    return_value=_rc_types.SimpleNamespace(validate=lambda root: receipt)))
                stack.enter_context(_rc_mock.patch.object(self.module, "subprocess", _rc_types.SimpleNamespace(run=self.replay)))
            return self.module.validate(self.root)


class _ReissueConsumerControls:
    def fixture(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        return _ReissueConsumerFixture(self, self.KIND, temporary.name)

    def assert_complete(self, receipt):
        self.assertEqual(receipt["result"], "PASS_WITH_SEMANTIC_REISSUE_CEILING", receipt["issues"])
        self.assertEqual(receipt["source_files"], 22 if self.KIND == "BV" else 40)
        self.assertTrue(receipt["source_coverage_exact"])
        self.assertTrue(receipt["source_manifest_exact"])
        self.assertEqual(receipt["source_hash_mismatches"], 0)
        self.assertEqual(receipt["structured_parse_errors"], 0)
        self.assertEqual(receipt["private_path_findings"], 0)
        self.assertTrue(receipt["authority_ceiling_exact"])
        if self.KIND == "BW":
            for name in ("v3_checker_reproduced", "v3_result_semantic_match", "v3_result_byte_match", "v1_false_pass_detected"):
                self.assertTrue(receipt[name], name)
            self.assertEqual(receipt["checker_pass_count"], 14)

    def test_all_present_keeps_complete_acceptance(self):
        fx = self.fixture()
        self.assert_complete(fx.run())
        if self.KIND == "BW":
            self.assertEqual(fx.replay_calls, 1)

    def test_each_selected_absence_still_consumes_original_member(self):
        for name in _RC_POPULATIONS[self.KIND]["selected"]:
            with self.subTest(member=name):
                fx = self.fixture()
                fx.remove_selected([name])
                self.assert_complete(fx.run())

    def test_all_selected_absent_keeps_original_population(self):
        fx = self.fixture()
        baseline = fx.run()
        self.assert_complete(baseline)
        fx.remove_selected()
        supplied = fx.run()
        self.assert_complete(supplied)
        self.assertEqual(
            {key: value for key, value in supplied.items() if key != "administrative_record_custody"},
            {key: value for key, value in baseline.items() if key != "administrative_record_custody"},
        )

    def test_supplied_member_hash_is_still_checked(self):
        fx = self.fixture()
        fx.remove_selected([fx.selected[0]])
        fx.supplied[fx.selected[0]].write_bytes(b"fixture: changed\n")
        result = fx.run()
        self.assertEqual(result["result"], "FAIL")
        self.assertGreater(result["source_hash_mismatches"], 0)

    def test_supplied_yaml_is_still_parsed(self):
        fx = self.fixture()
        name = next(x for x in fx.selected if x.endswith(".yaml"))
        fx.remove_selected([name])
        fx.supplied[name].write_bytes(b"[unterminated\n")
        result = fx.run()
        self.assertEqual(result["result"], "FAIL")
        self.assertGreater(result["structured_parse_errors"], 0)

    def test_supplied_member_still_has_privacy_check(self):
        fx = self.fixture()
        fx.remove_selected([fx.selected[0]])
        fx.supplied[fx.selected[0]].write_bytes(b"private: /home/synthetic/fixture\n")
        result = fx.run()
        self.assertEqual(result["result"], "FAIL")
        self.assertGreater(result["private_path_findings"], 0)

    def test_supplied_non_utf8_cannot_pass(self):
        fx = self.fixture()
        fx.remove_selected([fx.selected[0]])
        fx.supplied[fx.selected[0]].write_bytes(b"\xff")
        self.assertEqual(fx.run()["result"], "FAIL")

    def test_present_corruption_is_not_replaced(self):
        fx = self.fixture()
        (fx.source / fx.selected[0]).write_bytes(b"fixture: corrupt-present\n")
        result = fx.run()
        self.assertEqual(result["result"], "FAIL")
        self.assertGreater(result["source_hash_mismatches"], 0)

    def test_unselected_missing_and_extra_member_remain_errors(self):
        for mode in ("missing", "extra"):
            with self.subTest(mode=mode):
                fx = self.fixture()
                if mode == "missing":
                    name = next(x for x in fx.names if x not in fx.selected and x.endswith(".md"))
                    (fx.source / name).unlink()
                else:
                    (fx.source / "UNEXPECTED.txt").write_text("fixture\n")
                result = fx.run()
                self.assertEqual(result["result"], "FAIL")
                self.assertFalse(result["source_coverage_exact"])
                if self.KIND == "BW":
                    self.assertEqual(fx.replay_calls, 0)

    def test_present_symlink_is_forbidden(self):
        fx = self.fixture()
        path = fx.source / fx.selected[0]
        body = path.read_bytes()
        path.unlink()
        target = fx.supplied_dir / "link-target"
        fx._write(target, body)
        path.symlink_to(target)
        result = fx.run()
        self.assertEqual(result["result"], "FAIL")
        self.assertTrue(any("symlink" in issue for issue in result["issues"]))

    def test_whole_source_absence_returns_fail_without_replay(self):
        fx = self.fixture()
        shutil.rmtree(fx.source)  # Synthetic temporary surface only.
        result = fx.run()
        self.assertEqual(result["result"], "FAIL")
        self.assertFalse(result["source_coverage_exact"])
        self.assertEqual(fx.replay_calls, 0)

    def test_missing_selected_supply_refusal_returns_fail_without_replay(self):
        fx = self.fixture()
        fx.remove_selected()
        fx.supply_error = True
        result = fx.run()
        self.assertEqual(result["result"], "FAIL")
        self.assertEqual(fx.replay_calls, 0)

    def test_manifest_and_required_child_failures_remain_errors(self):
        for mode in ("manifest", "child", "authority"):
            with self.subTest(mode=mode):
                fx = self.fixture()
                if mode == "manifest":
                    path = fx.reissue / "SOURCE_SHA256SUMS"
                    path.write_bytes(path.read_bytes() + path.read_bytes().splitlines(keepends=True)[0])
                elif mode == "child":
                    fx.child_valid = False
                else:
                    fx.provenance["proposal_boundary"]["owner_adoption"] = "ADOPTED"
                    fx._write_provenance()
                self.assertEqual(fx.run()["result"], "FAIL")


class ReissueBvAdministrativeConsumerTests(_ReissueConsumerControls, unittest.TestCase):
    KIND = "BV"


class ReissueBwCjAdministrativeConsumerTests(_ReissueConsumerControls, unittest.TestCase):
    KIND = "BW"

    def test_real_replay_predicates_reject_failed_or_changed_output(self):
        for mode in ("exit-failure", "no-output", "semantic-drift", "byte-drift"):
            with self.subTest(mode=mode):
                fx = self.fixture()
                fx.replay_mode = mode
                result = fx.run()
                self.assertEqual(fx.replay_calls, 1)
                self.assertEqual(result["result"], "FAIL")
                if mode == "byte-drift":
                    self.assertTrue(result["v3_result_semantic_match"])
                    self.assertFalse(result["v3_result_byte_match"])

    def test_replay_is_not_replaced_by_a_cached_receipt(self):
        fx = self.fixture()
        fx.replay_mode = "no-output"
        self.assertEqual(fx.run()["result"], "FAIL")
        self.assertEqual(fx.replay_calls, 1)

    def test_v1_false_pass_detection_is_retained(self):
        fx = self.fixture()
        path = fx.source / "PROPOSAL/checks/post_bv_consolidated_recheck.py"
        path.write_bytes(path.read_bytes() + b'# ci["matched_twins"]+=\n')
        result = fx.run()
        self.assertEqual(result["result"], "FAIL")
        self.assertFalse(result["v1_false_pass_detected"])

    def test_v2_failure_history_cannot_be_promoted(self):
        fx = self.fixture()
        fx.provenance["independent_intake_recheck"]["v2_disposition"] = "ACCEPTED"
        fx._write_provenance()
        result = fx.run()
        self.assertEqual(result["result"], "FAIL")
        self.assertFalse(result["authority_ceiling_exact"])

    def test_v3_semantic_predicates_are_not_only_byte_equality(self):
        for mutate in ("v2", "ci", "cj", "mutant"):
            with self.subTest(predicate=mutate):
                fx = self.fixture()
                if mutate == "v2":
                    fx.replay_document["v2_ci_cj_disposition"] = "ACCEPTED"
                elif mutate == "ci":
                    fx.replay_document["results"]["CI"]["declared_profiles"] = 15624
                elif mutate == "cj":
                    fx.replay_document["results"]["CJ"]["eligible_profiles"] = 71
                else:
                    fx.replay_document["results"]["CJ"]["predicate_mutation_receipt"]["all_declared_mutants_killed"] = False
                fx._write_replay_result()
                fx.provenance["independent_intake_recheck"]["v3_result_sha256"] = fx.module.EXPECTED_V3_RESULT_SHA256
                fx._write_provenance()
                result = fx.run()
                self.assertEqual(result["result"], "FAIL")
                self.assertTrue(result["v3_result_semantic_match"])
                self.assertTrue(result["v3_result_byte_match"])
                self.assertFalse(result["v3_checker_reproduced"])


if __name__ == "__main__":
    unittest.main()
