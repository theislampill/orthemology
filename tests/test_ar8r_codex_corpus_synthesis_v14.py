import importlib.util
import hashlib
import json
import pathlib
import shutil
import tempfile
import unittest

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/validate_ar8r_codex_corpus_synthesis_v14.py"


def load_validator():
    if not SCRIPT.is_file():
        raise AssertionError("Codex corpus-synthesis V14 validator is missing")
    spec = importlib.util.spec_from_file_location(
        "ar8r_codex_corpus_synthesis_v14", SCRIPT
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Ar8rCodexCorpusSynthesisV14Tests(unittest.TestCase):
    def copy_surface(self, validator, temporary):
        copied = pathlib.Path(temporary) / "codex-corpus-synthesis-v14"
        shutil.copytree(ROOT / validator.SYNTHESIS_REL, copied)
        return copied

    def assert_failed_with(self, receipt, issue_fragment):
        self.assertEqual(receipt["result"], "FAIL", receipt)
        self.assertTrue(
            any(issue_fragment in issue for issue in receipt["issues"]),
            receipt,
        )

    def rewrite_source_manifest(self, copied):
        manifest = copied / "SOURCE_SHA256SUMS"
        rows = []
        for path in sorted(copied.rglob("*")):
            if not path.is_file() or path == manifest:
                continue
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            rows.append(f"{digest}  {path.relative_to(copied).as_posix()}")
        manifest.write_text("\n".join(rows) + "\n", encoding="utf-8", newline="\n")

    def test_current_synthesis_is_bounded_and_complete(self):
        validator = load_validator()
        receipt = validator.validate(ROOT)
        self.assertEqual(
            receipt["result"],
            "PASS_BOUNDED_CODEX_CORPUS_SYNTHESIS_NO_SCIENTIFIC_PROMOTION",
        )
        self.assertEqual(receipt["instance_count"], 12)
        self.assertEqual(receipt["candidate_count"], 5)
        self.assertEqual(receipt["countermodel_count"], 11)
        self.assertEqual(receipt["protocol_count"], 4)
        self.assertEqual(receipt["private_path_findings"], 0)
        self.assertEqual(receipt["source_hash_mismatches"], 0)
        self.assertTrue(receipt["authority_ceiling_exact"])
        self.assertTrue(receipt["theorem_ancestry_bounded"])
        self.assertTrue(receipt["lean_receipt_exact"])
        self.assertTrue(receipt["checker_receipt_exact"])
        self.assertTrue(receipt["audit_chain_complete"])
        self.assertTrue(receipt["protocol_readiness_fail_closed"])

    def test_duplicate_instance_identity_fails_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "AR8R-CODEX-CROSS-LANE-INSTANCE-MAP-V14.yaml"
            data = yaml.safe_load(target.read_text(encoding="utf-8"))
            data["instances"][1]["id"] = data["instances"][0]["id"]
            target.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assert_failed_with(receipt, "typed instance exact identity/order mismatch")

    def test_unknown_relation_class_fails_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "AR8R-CODEX-THEOREM-FAMILY-RELATION-LEDGER-V14.yaml"
            data = yaml.safe_load(target.read_text(encoding="utf-8"))
            data["relations"][0]["relation"] = "SAME_VIBES"
            target.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assert_failed_with(receipt, "unknown theorem-family relation: REL-01")

    def test_historical_identity_or_novelty_promotion_fails_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "AR8R-CODEX-MENISCUS-CANDIDATE-VERDICT-V14.yaml"
            data = yaml.safe_load(target.read_text(encoding="utf-8"))
            data["authority"]["historical_identity"] = "AR8R-T999"
            data["authority"]["general_novelty"] = 1
            target.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assert_failed_with(receipt, "authority ceiling drift or promotion")
        self.assertFalse(receipt["authority_ceiling_exact"])

    def test_meniscus_or_closure_promotion_fails_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "AR8R-CODEX-MENISCUS-CANDIDATE-VERDICT-V14.yaml"
            data = yaml.safe_load(target.read_text(encoding="utf-8"))
            data["program_status"]["meniscus"] = "MENISCUS_REACHED"
            data["program_status"]["natural_closure"] = "REACHED"
            target.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assert_failed_with(receipt, "champion, meniscus, or closure promotion")

    def test_source_world_or_transcendental_bridge_promotion_fails_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "AR8R-CODEX-CROSS-LANE-INSTANCE-MAP-V14.yaml"
            data = yaml.safe_load(target.read_text(encoding="utf-8"))
            row = next(row for row in data["instances"] if row["id"] == "CLIM-12")
            row["source_world_bridge_established"] = True
            row["nonclaims"] = []
            target.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assert_failed_with(receipt, "instance bridge/nonclaim boundary mismatch: CLIM-12")

    def test_candidate_without_nonclaims_or_ancestry_fails_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "AR8R-CODEX-FORMALIZATION-DELTA-V14.yaml"
            data = yaml.safe_load(target.read_text(encoding="utf-8"))
            data["candidates"][0]["nonclaims"] = []
            data["candidates"][0]["earliest_internal_ancestor"] = None
            target.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assert_failed_with(receipt, "candidate ancestry/nonclaim boundary missing: CCS-V14-C1")

    def test_protocols_cannot_be_promoted_to_ready_to_run(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "AR8R-CODEX-FORMALIZATION-DELTA-V14.yaml"
            data = yaml.safe_load(target.read_text(encoding="utf-8"))
            data["empirical_protocols"][0]["status"] = "READY_TO_RUN"
            data["empirical_protocols"][0]["experiment_executed"] = True
            target.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assertEqual(receipt["result"], "FAIL")
        self.assertFalse(receipt["protocol_readiness_fail_closed"])

    def test_private_locator_fails_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            (copied / "PRIVATE-LEAK.txt").write_text(
                "C:" + "\\Users\\owner\\private.txt\n", encoding="utf-8"
            )
            receipt = validator.validate(ROOT, copied)
        self.assertEqual(receipt["result"], "FAIL")
        self.assertGreater(receipt["private_path_findings"], 0)

    def test_checker_or_lean_receipt_drift_fails_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            checker = copied / "checks/codex_fibre_synthesis_check_results.json"
            checker.write_text("{}\n", encoding="utf-8")
            lean = copied / "lean/LEAN_RECEIPT.json"
            lean.write_text("{}\n", encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assertEqual(receipt["result"], "FAIL")
        self.assertFalse(receipt["checker_receipt_exact"])
        self.assertFalse(receipt["lean_receipt_exact"])

    def test_candidate_freeze_manifest_is_independently_pinned(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "audit/CANDIDATE_FREEZE_SHA256SUMS"
            target.write_text(target.read_text(encoding="utf-8") + "0" * 64 + "  ghost.txt\n", encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assert_failed_with(receipt, "candidate freeze manifest or frozen member drift")

    def test_allowed_but_wrong_instance_class_fails_with_specific_issue(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "AR8R-CODEX-CROSS-LANE-INSTANCE-MAP-V14.yaml"
            data = yaml.safe_load(target.read_text(encoding="utf-8"))
            data["instances"][0]["relation_class"] = "FORMAL_ANALOGUE_ONLY"
            target.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assert_failed_with(receipt, "instance relation class drift: CLIM-01")

    def test_relation_truncation_fails_with_exact_coverage_issue(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "AR8R-CODEX-THEOREM-FAMILY-RELATION-LEDGER-V14.yaml"
            data = yaml.safe_load(target.read_text(encoding="utf-8"))
            data["relations"] = data["relations"][:2]
            target.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assert_failed_with(receipt, "theorem-family exact identity/order mismatch")

    def test_candidate_identity_and_verdict_map_are_pinned(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "AR8R-CODEX-FORMALIZATION-DELTA-V14.yaml"
            data = yaml.safe_load(target.read_text(encoding="utf-8"))
            data["candidates"][0]["id"] = "CCS-V14-RENAMED"
            data["candidates"][1]["verdict"] = "COMMON_THEOREM_ESTABLISHED"
            target.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assert_failed_with(receipt, "candidate exact identity/order mismatch")
        self.assert_failed_with(receipt, "candidate verdict drift: CCS-V14-C2")

    def test_countermodel_identity_map_is_pinned(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "AR8R-CODEX-COUNTERMODELS-V14.yaml"
            data = yaml.safe_load(target.read_text(encoding="utf-8"))
            data["countermodels"][0]["id"] = "CM-X"
            target.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assert_failed_with(receipt, "countermodel exact identity/order mismatch")

    def test_b1_b4_exact_status_map_is_pinned(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "AR8R-CODEX-FORMALIZATION-DELTA-V14.yaml"
            data = yaml.safe_load(target.read_text(encoding="utf-8"))
            data["empirical_protocols"][0]["status"] = "PREREGISTRATION_READY_FOR_REVIEW_DRAFT"
            target.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assert_failed_with(receipt, "empirical protocol readiness or execution promoted")

    def test_residual_status_and_authority_are_pinned(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "AR8R-CODEX-RESIDUAL-GUIDED-HYPOTHESIS-LEDGER-V14.yaml"
            data = yaml.safe_load(target.read_text(encoding="utf-8"))
            data["hypotheses"][0]["status"] = "COMMON_THEOREM_ESTABLISHED"
            data["authority_ceiling"]["general_novelty"] = 1
            target.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assert_failed_with(receipt, "residual-hypothesis status drift: RGH-01")
        self.assert_failed_with(receipt, "residual-hypothesis authority drift or promotion")

    def test_all_secondary_authority_surfaces_fail_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            instance = copied / "AR8R-CODEX-CROSS-LANE-INSTANCE-MAP-V14.yaml"
            instance_data = yaml.safe_load(instance.read_text(encoding="utf-8"))
            instance_data["authority"]["owner_adoption"] = "ADOPTED"
            instance.write_text(yaml.safe_dump(instance_data, sort_keys=False), encoding="utf-8")
            counter = copied / "AR8R-CODEX-COUNTERMODELS-V14.yaml"
            counter_data = yaml.safe_load(counter.read_text(encoding="utf-8"))
            counter_data["authority"]["general_novelty"] = 1
            counter.write_text(yaml.safe_dump(counter_data, sort_keys=False), encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assert_failed_with(receipt, "cross-lane instance authority drift or promotion")
        self.assert_failed_with(receipt, "countermodel authority drift or promotion")

    def test_t354_and_tac_sac_controls_are_pinned(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "AR8R-CODEX-MENISCUS-CANDIDATE-VERDICT-V14.yaml"
            data = yaml.safe_load(target.read_text(encoding="utf-8"))
            data["preserved_controls"]["AR8R-T354"] = "REPOSITORY_READY"
            data["preserved_controls"]["TAC_SAC_HISTORICAL_DEFINITIONS"] = "DEFINED_HERE"
            target.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assert_failed_with(receipt, "T354 or TAC/SAC preserved-control drift")

    def test_prose_promotion_is_rejected_independently_of_machine_yaml(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "README.md"
            target.write_text(target.read_text(encoding="utf-8") + "\nMENISCUS_REACHED\n", encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assert_failed_with(receipt, "prose or machine authority promotion: MENISCUS_REACHED")

    def test_semantic_source_contract_is_not_path_existence_only(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "AR8R-CODEX-THEOREM-FAMILY-RELATION-LEDGER-V14.yaml"
            data = yaml.safe_load(target.read_text(encoding="utf-8"))
            row = next(row for row in data["relations"] if row["id"] == "REL-06")
            row["source_refs"] = ["docs/project-closure/ar8r-v11/README.md"]
            target.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assert_failed_with(receipt, "relation semantic source contract drift: REL-06")

    def test_second_fresh_rereview_attempt_cannot_be_removed_and_remanifested(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            (copied / "audit/FRESH_REREVIEW_ATTEMPT_2.json").unlink()
            self.rewrite_source_manifest(copied)
            receipt = validator.validate(ROOT, copied)
        self.assert_failed_with(receipt, "required synthesis member set mismatch")
        self.assert_failed_with(receipt, "second fresh-rereview attempt missing or drifted")

    def test_independent_whole_branch_review_attempt_cannot_be_promoted(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "audit/FRESH_REREVIEW_ATTEMPT_3.json"
            data = json.loads(target.read_text(encoding="utf-8"))
            data["verdict"] = "PASS"
            data["blocking_findings"] = []
            target.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n")
            self.rewrite_source_manifest(copied)
            receipt = validator.validate(ROOT, copied)
        self.assert_failed_with(receipt, "independent whole-branch review attempt missing or drifted")

    def test_final_rereview_false_hash_claim_fails_closed_after_remanifest(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "audit/FRESH_REREVIEW.json"
            data = json.loads(target.read_text(encoding="utf-8"))
            data["reviewed_hashes"]["README.md"] = "0" * 64
            target.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n")
            self.rewrite_source_manifest(copied)
            receipt = validator.validate(ROOT, copied)
        self.assert_failed_with(receipt, "final rereview reviewed-hash claims mismatch")

    def test_final_rereview_cannot_retain_blocking_findings(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "audit/FRESH_REREVIEW.json"
            data = json.loads(target.read_text(encoding="utf-8"))
            data["blocking_findings"] = [{"id": "UNRESOLVED", "summary": "still open"}]
            target.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n")
            self.rewrite_source_manifest(copied)
            receipt = validator.validate(ROOT, copied)
        self.assert_failed_with(receipt, "final rereview retains blocking findings")

    def test_manifested_extra_member_fails_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            (copied / "EXTRA.txt").write_text("bounded but unregistered\n", encoding="utf-8")
            self.rewrite_source_manifest(copied)
            receipt = validator.validate(ROOT, copied)
        self.assert_failed_with(receipt, "required synthesis member set mismatch")

    def test_signed_url_parameter_fails_closed_when_inserted_into_registered_member(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "audit/REPAIR_LOG.md"
            target.write_text(
                target.read_text(encoding="utf-8")
                + "\nhttps://example.invalid/file?X-Amz-Signature=deadbeef\n",
                encoding="utf-8",
                newline="\n",
            )
            self.rewrite_source_manifest(copied)
            receipt = validator.validate(ROOT, copied)
        self.assertGreater(receipt["private_path_findings"], 0, receipt)
        self.assert_failed_with(receipt, "private path, browser locator, signed URL, or token-like text leaked")

    def test_all_transcendental_and_empirical_prose_promotions_fail_closed(self):
        validator = load_validator()
        promotions = {
            "NECESSARY_BEING": "necessary_being_established",
            "ONE_PERSONAL_BEARER": "one_personal_bearer_established",
            "PERSONALITY": "personality_established",
            "WISDOM": "wisdom_established",
            "SPEECH": "speech_established",
            "REVELATION": "revelation_established",
            "ALLAH": "allah_identification_established",
            "EMPIRICAL_RUN": "empirical_program_run",
        }
        for label, key in promotions.items():
            variants = (
                f"{key}: true",
                f'"{key}": true',
                f"{key.replace('_', '-')}: true",
                f"{key.replace('_', ' ')}: true",
            )
            for variant in variants:
                with self.subTest(label=label, variant=variant), tempfile.TemporaryDirectory() as temporary:
                    copied = self.copy_surface(validator, temporary)
                    target = copied / "audit/REPAIR_LOG.md"
                    target.write_text(
                        target.read_text(encoding="utf-8") + "\n" + variant + "\n",
                        encoding="utf-8",
                        newline="\n",
                    )
                    self.rewrite_source_manifest(copied)
                    receipt = validator.validate(ROOT, copied)
                self.assert_failed_with(receipt, f"prose or machine authority promotion: {label}")

    def test_all_authority_boundary_serializations_fail_closed(self):
        validator = load_validator()
        promotions = {
            "HISTORICAL_IDENTITY": ("historical_identity", "AR8R-T999"),
            "GENERAL_NOVELTY": ("general_novelty", "1"),
            "SCIENTIFIC_ADOPTION": ("repository_scientific_adoption", "ADOPTED"),
            "OWNER_ADOPTION": ("owner_adoption", "ADOPTED"),
            "SOURCE_WORLD_TRUE": ("source_world_bridge_established", "true"),
            "EMPIRICAL_RESULT": ("empirical_result", "EXPERIMENT_EXECUTED"),
            "INTEGRATED_CHAMPION": ("integrated_champion", "CANDIDATE_N"),
            "MENISCUS_REACHED": ("meniscus", "REACHED"),
            "NATURAL_CLOSURE_REACHED": ("natural_closure", "REACHED"),
            "T354_PROMOTION": ("T354", "REPOSITORY_READY"),
            "TAC_SAC_DEFINITION": ("TAC_SAC", "DEFINED_HERE"),
        }
        for label, (key, value) in promotions.items():
            variants = (
                f"{key}: {value}",
                f'"{key}": "{value}"',
                f"{key.replace('_', '-')}: {value}",
                f"{key.replace('_', ' ')}: {value}",
            )
            for variant in variants:
                with self.subTest(label=label, variant=variant), tempfile.TemporaryDirectory() as temporary:
                    copied = self.copy_surface(validator, temporary)
                    target = copied / "audit/REPAIR_LOG.md"
                    target.write_text(
                        target.read_text(encoding="utf-8") + "\n" + variant + "\n",
                        encoding="utf-8",
                        newline="\n",
                    )
                    self.rewrite_source_manifest(copied)
                    receipt = validator.validate(ROOT, copied)
                self.assert_failed_with(receipt, f"prose or machine authority promotion: {label}")

    def test_append_only_attempt_2_semantics_are_hash_pinned(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "audit/FRESH_REREVIEW_ATTEMPT_2.json"
            data = json.loads(target.read_text(encoding="utf-8"))
            data["scope_result"] = "PASS_V14_LOCAL_SYNTHESIS"
            data["mutation_controls"]["killed"] = 999
            data["mutation_controls"]["total"] = 999
            data["reviewed_hashes"]["lean_source_sha256"] = "0" * 64
            target.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n")
            self.rewrite_source_manifest(copied)
            receipt = validator.validate(ROOT, copied)
        self.assert_failed_with(
            receipt,
            "append-only audit receipt hash drift: audit/FRESH_REREVIEW_ATTEMPT_2.json",
        )

    def test_append_only_attempt_3_severity_and_summary_are_hash_pinned(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "audit/FRESH_REREVIEW_ATTEMPT_3.json"
            data = json.loads(target.read_text(encoding="utf-8"))
            data["blocking_findings"][0]["severity"] = "LOW"
            data["blocking_findings"][0]["summary"] = ""
            target.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n")
            self.rewrite_source_manifest(copied)
            receipt = validator.validate(ROOT, copied)
        self.assert_failed_with(
            receipt,
            "append-only audit receipt hash drift: audit/FRESH_REREVIEW_ATTEMPT_3.json",
        )

    def test_append_only_attempt_4_repair_findings_are_hash_pinned(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "audit/FRESH_REREVIEW_ATTEMPT_4.json"
            data = json.loads(target.read_text(encoding="utf-8"))
            data["blocking_findings"] = []
            data["verdict"] = "PASS"
            target.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n")
            self.rewrite_source_manifest(copied)
            receipt = validator.validate(ROOT, copied)
        self.assert_failed_with(
            receipt,
            "append-only audit receipt hash drift: audit/FRESH_REREVIEW_ATTEMPT_4.json",
        )

    def test_append_only_attempt_5_authority_matrix_findings_are_hash_pinned(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "audit/FRESH_REREVIEW_ATTEMPT_5.json"
            data = json.loads(target.read_text(encoding="utf-8"))
            data["blocking_findings"] = []
            data["verdict"] = "PASS"
            target.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n")
            self.rewrite_source_manifest(copied)
            receipt = validator.validate(ROOT, copied)
        self.assert_failed_with(
            receipt,
            "append-only audit receipt hash drift: audit/FRESH_REREVIEW_ATTEMPT_5.json",
        )

    def test_final_scope_source_contract_and_repair_closure_are_exact(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "audit/FRESH_REREVIEW.json"
            data = json.loads(target.read_text(encoding="utf-8"))
            data["scope_boundary"] = {
                "qualified_surface": "FULL_REPOSITORY",
                "commit_push_merge_release_publication": "AUTHORIZED",
            }
            data["contracts_verified"].pop("source")
            data["independent_repair_findings_verified"] = ["AR8R-V14-IR01"]
            target.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n")
            self.rewrite_source_manifest(copied)
            receipt = validator.validate(ROOT, copied)
        self.assert_failed_with(receipt, "final rereview scope boundary mismatch")
        self.assert_failed_with(receipt, "final rereview source-contract claims mismatch")
        self.assert_failed_with(receipt, "final rereview independent repair closure mismatch")

    def test_plain_signature_notation_is_not_a_private_locator(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "audit/REPAIR_LOG.md"
            target.write_text(
                target.read_text(encoding="utf-8")
                + "\nsig = the selected sign map\nsignature = a non-secret field name\n",
                encoding="utf-8",
                newline="\n",
            )
            self.rewrite_source_manifest(copied)
            receipt = validator.validate(ROOT, copied)
        self.assertEqual(receipt["private_path_findings"], 0, receipt)


if __name__ == "__main__":
    unittest.main()
