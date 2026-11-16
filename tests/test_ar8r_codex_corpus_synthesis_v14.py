import importlib.util
import hashlib
import json
import pathlib
import shutil
import tempfile
import unittest
from unittest import mock
import urllib.parse

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


CURRENT_INPUTS = ('AR8R-CODEX-CROSS-LANE-INSTANCE-MAP-V14.yaml', 'AR8R-CODEX-THEOREM-FAMILY-RELATION-LEDGER-V14.yaml', 'AR8R-CODEX-FORMALIZATION-DELTA-V14.yaml', 'AR8R-CODEX-COUNTERMODELS-V14.yaml', 'AR8R-CODEX-MENISCUS-CANDIDATE-VERDICT-V14.yaml', 'AR8R-CODEX-RESIDUAL-GUIDED-HYPOTHESIS-LEDGER-V14.yaml', 'lean/CodexFibreSynthesis.lean', 'lean/LEAN_RECEIPT.json', 'checks/codex_fibre_synthesis_check.py', 'checks/codex_fibre_synthesis_check_results.json')


class Ar8rCodexCorpusSynthesisV14Tests(unittest.TestCase):
    def copy_surface(self, validator, temporary):
        copied = pathlib.Path(temporary) / "codex-corpus-synthesis-v14"
        copied.mkdir()
        for relative in CURRENT_INPUTS:
            destination = copied / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / validator.SYNTHESIS_REL / relative, destination)
        (copied / "PUBLIC-CONTROL.md").write_text("Synthetic live guard carrier.\n", encoding="utf-8")
        return copied

    def assert_failed_with(self, receipt, issue_fragment):
        self.assertEqual(receipt["result"], "FAIL", receipt)
        self.assertTrue(
            any(issue_fragment in issue for issue in receipt["issues"]),
            receipt,
        )


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
            target = copied / "PUBLIC-CONTROL.md"
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


    def test_signed_url_parameter_fails_closed_when_inserted_into_registered_member(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "PUBLIC-CONTROL.md"
            target.write_text(
                target.read_text(encoding="utf-8")
                + "\nhttps://example.invalid/file?X-Amz-Signature=deadbeef\n",
                encoding="utf-8",
                newline="\n",
            )
            receipt = validator.validate(ROOT, copied)
        self.assertGreater(receipt["private_path_findings"], 0, receipt)
        self.assert_failed_with(receipt, "private path, browser locator, signed URL, or token-like text leaked")


    def test_percent_encoded_signed_url_parameter_fails_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "PUBLIC-CONTROL.md"
            target.write_text(
                target.read_text(encoding="utf-8")
                + "\nhttps://example.invalid/file?X-Amz-Signature%3Ddeadbeef\n",
                encoding="utf-8",
                newline="\n",
            )
            receipt = validator.validate(ROOT, copied)
        self.assertGreater(receipt["private_path_findings"], 0, receipt)
        self.assert_failed_with(receipt, "private path, browser locator, signed URL, or token-like text leaked")


    def test_browser_session_identifier_fails_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "PUBLIC-CONTROL.md"
            target.write_text(
                target.read_text(encoding="utf-8")
                + "\nbrowser_session_id: private-browser-session-123\n",
                encoding="utf-8",
                newline="\n",
            )
            receipt = validator.validate(ROOT, copied)
        self.assertGreater(receipt["private_path_findings"], 0, receipt)
        self.assert_failed_with(receipt, "private path, browser locator, signed URL, or token-like text leaked")


    def test_nested_encoded_and_quoted_private_locators_fail_closed(self):
        validator = load_validator()
        payloads = (
            "https://example.invalid/file?X-Amz-Signature%25253Ddeadbeef",
            '"browser_session_id": "private-browser-session-123"',
            "'browser-session-identifier' = 'private-browser-session-123'",
            r"https:\/\/example.invalid\/file?signature=deadbeef",
            "browser%255Fsession%255Fid%253Aprivate-browser-session-123",
        )
        for payload in payloads:
            with self.subTest(payload=payload), tempfile.TemporaryDirectory() as temporary:
                copied = self.copy_surface(validator, temporary)
                target = copied / "PUBLIC-CONTROL.md"
                target.write_text(
                    target.read_text(encoding="utf-8") + "\n" + payload + "\n",
                    encoding="utf-8",
                    newline="\n",
                )
                receipt = validator.validate(ROOT, copied)
            self.assertGreater(receipt["private_path_findings"], 0, receipt)
            self.assert_failed_with(receipt, "private path, browser locator, signed URL, or token-like text leaked")


    def test_json_unicode_escaped_private_locators_fail_closed(self):
        validator = load_validator()
        payloads = (
            r'{"browser\u005fsession\u005fid": "opaque"}',
            r"https://example.invalid/?\u0058-Amz-Signature=opaque",
        )
        for payload in payloads:
            with self.subTest(payload=payload), tempfile.TemporaryDirectory() as temporary:
                copied = self.copy_surface(validator, temporary)
                target = copied / "PUBLIC-CONTROL.md"
                target.write_text(
                    target.read_text(encoding="utf-8") + "\n" + payload + "\n",
                    encoding="utf-8",
                    newline="\n",
                )
                receipt = validator.validate(ROOT, copied)
            self.assertGreater(receipt["private_path_findings"], 0, receipt)
            self.assert_failed_with(
                receipt,
                "private path, browser locator, signed URL, or token-like text leaked",
            )


    def test_percent_decoding_scans_the_final_bounded_iteration(self):
        validator = load_validator()
        encoded = "X-Amz-Signature=opaque"
        for _ in range(8):
            encoded = urllib.parse.quote(encoded, safe="")
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "PUBLIC-CONTROL.md"
            target.write_text(
                target.read_text(encoding="utf-8")
                + "\nhttps://example.invalid/?"
                + encoded
                + "\n",
                encoding="utf-8",
                newline="\n",
            )
            receipt = validator.validate(ROOT, copied)
        self.assertGreater(receipt["private_path_findings"], 0, receipt)
        self.assert_failed_with(
            receipt,
            "private path, browser locator, signed URL, or token-like text leaked",
        )


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
                    target = copied / "PUBLIC-CONTROL.md"
                    target.write_text(
                        target.read_text(encoding="utf-8") + "\n" + variant + "\n",
                        encoding="utf-8",
                        newline="\n",
                    )
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
                    target = copied / "PUBLIC-CONTROL.md"
                    target.write_text(
                        target.read_text(encoding="utf-8") + "\n" + variant + "\n",
                        encoding="utf-8",
                        newline="\n",
                    )
                    receipt = validator.validate(ROOT, copied)
                self.assert_failed_with(receipt, f"prose or machine authority promotion: {label}")


    def test_non_token_and_compact_authority_promotions_fail_closed(self):
        validator = load_validator()
        promotions = {
            "GENERAL_NOVELTY": "general_novelty: 0.5",
            "HISTORICAL_IDENTITY": '{"historical_identity":"AR8R-T999","note":"compact"}',
        }
        for label, payload in promotions.items():
            with self.subTest(label=label), tempfile.TemporaryDirectory() as temporary:
                copied = self.copy_surface(validator, temporary)
                target = copied / "PUBLIC-CONTROL.md"
                target.write_text(
                    target.read_text(encoding="utf-8") + "\n" + payload + "\n",
                    encoding="utf-8",
                    newline="\n",
                )
                receipt = validator.validate(ROOT, copied)
            self.assert_failed_with(receipt, f"prose or machine authority promotion: {label}")


    def test_json_unicode_escaped_authority_key_fails_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "PUBLIC-CONTROL.md"
            target.write_text(
                target.read_text(encoding="utf-8")
                + '\n{"\\u0067eneral_novelty": 1}\n',
                encoding="utf-8",
                newline="\n",
            )
            receipt = validator.validate(ROOT, copied)
        self.assert_failed_with(
            receipt,
            "prose or machine authority promotion: GENERAL_NOVELTY",
        )


    def test_bounded_authority_value_with_yaml_comment_is_accepted(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "PUBLIC-CONTROL.md"
            target.write_text(
                target.read_text(encoding="utf-8")
                + "\ngeneral_novelty: 0 # bounded control\n",
                encoding="utf-8",
                newline="\n",
            )
            receipt = validator.validate(ROOT, copied)
        self.assertNotIn(
            "prose or machine authority promotion: GENERAL_NOVELTY",
            receipt["issues"],
            receipt,
        )


    def test_authority_boundary_separator_and_quoting_bypasses_fail_closed(self):
        validator = load_validator()
        payloads = {
            "GENERAL_NOVELTY": (
                "general\u00a0novelty: 0.5",
                "general\u2003novelty: 0.5",
                "general\tnovelty: 0.5",
                "general_novelty /* promoted */: 0.5",
                "`general_novelty`: 0.5",
                "general_novelty = 0.5",
            ),
            "HISTORICAL_IDENTITY": (
                "historical\u00a0identity: AR8R-T999",
                "historical_identity <!-- promoted -->: AR8R-T999",
                "`historical-identity` = AR8R-T999",
            ),
        }
        for label, variants in payloads.items():
            for payload in variants:
                with self.subTest(label=label, payload=payload), tempfile.TemporaryDirectory() as temporary:
                    copied = self.copy_surface(validator, temporary)
                    target = copied / "PUBLIC-CONTROL.md"
                    target.write_text(
                        target.read_text(encoding="utf-8") + "\n" + payload + "\n",
                        encoding="utf-8",
                        newline="\n",
                    )
                    receipt = validator.validate(ROOT, copied)
                self.assert_failed_with(receipt, f"prose or machine authority promotion: {label}")


    def test_backtick_wrapped_bounded_authority_value_is_accepted(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "PUBLIC-CONTROL.md"
            target.write_text(
                target.read_text(encoding="utf-8")
                + "\nrepository_scientific_adoption: `NONE`\n",
                encoding="utf-8",
                newline="\n",
            )
            receipt = validator.validate(ROOT, copied)
        self.assertNotIn(
            "prose or machine authority promotion: SCIENTIFIC_ADOPTION",
            receipt["issues"],
            receipt,
        )


    def test_plain_signature_notation_is_not_a_private_locator(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "PUBLIC-CONTROL.md"
            target.write_text(
                target.read_text(encoding="utf-8")
                + "\nsig = the selected sign map\nsignature = a non-secret field name\n",
                encoding="utf-8",
                newline="\n",
            )
            receipt = validator.validate(ROOT, copied)
        self.assertEqual(receipt["private_path_findings"], 0, receipt)


    def test_current_inputs_pass_without_historical_package(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            self.assertFalse((copied / "audit").exists())
            self.assertFalse((copied / "SOURCE_SHA256SUMS").exists())
            receipt = validator.validate(ROOT, copied)
        self.assertEqual(receipt["result"], "PASS_CURRENT_SYNTHESIS_CONTRACTS", receipt)
        self.assertEqual(receipt["instance_count"], 12)
        self.assertEqual(receipt["candidate_count"], 5)
        self.assertEqual(receipt["countermodel_count"], 11)
        self.assertEqual(receipt["protocol_count"], 4)
        self.assertEqual(receipt["private_path_findings"], 0)
        for key in ("authority_ceiling_exact", "theorem_ancestry_bounded",
                    "lean_receipt_exact", "checker_receipt_exact", "protocol_readiness_fail_closed"):
            self.assertTrue(receipt[key], key)
        self.assertEqual(receipt["historical_audit_chain"], "NOT_RUN")
        self.assertEqual(receipt["historical_package_authentication"], "NOT_RUN")

    def test_optional_current_text_needs_no_historical_registration(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            (copied / "additional-context.md").write_text("A bounded current note.\n", encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assertEqual(receipt["result"], "PASS_CURRENT_SYNTHESIS_CONTRACTS", receipt)

    def test_present_historical_named_text_is_still_scanned(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            (copied / "audit").mkdir()
            (copied / "audit/FRESH_REREVIEW.json").write_text('{"general_novelty":1}\n', encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assert_failed_with(receipt, "prose or machine authority promotion: GENERAL_NOVELTY")

    def test_non_utf8_current_extra_fails_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            (copied / "extra.bin").write_bytes(b"\xff\xfe")
            receipt = validator.validate(ROOT, copied)
        self.assert_failed_with(receipt, "non-UTF-8 synthesis member")

    def test_unreadable_current_extra_fails_closed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "blocked.txt"
            target.write_text("Ordinary synthetic text.\n", encoding="utf-8")
            original = pathlib.Path.read_text
            def read_text(path, *args, **kwargs):
                if path == target:
                    raise PermissionError("synthetic refusal")
                return original(path, *args, **kwargs)
            with mock.patch.object(pathlib.Path, "read_text", read_text):
                receipt = validator.validate(ROOT, copied)
        self.assert_failed_with(receipt, "unreadable synthesis member")

    def test_symlink_current_member_is_not_followed(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = pathlib.Path(temporary) / "outside.txt"
            target.write_text("Synthetic outside text.\n", encoding="utf-8")
            (copied / "linked.txt").symlink_to(target)
            receipt = validator.validate(ROOT, copied)
        self.assert_failed_with(receipt, "unsafe current synthesis member")

    def test_symlink_source_root_is_rejected(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            linked = pathlib.Path(temporary) / "linked"
            linked.symlink_to(copied, target_is_directory=True)
            receipt = validator.validate(ROOT, linked)
        self.assert_failed_with(receipt, "unsafe current synthesis root")

    def test_unresolved_normalized_source_reference_is_rejected(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            target = copied / "AR8R-CODEX-CROSS-LANE-INSTANCE-MAP-V14.yaml"
            data = yaml.safe_load(target.read_text(encoding="utf-8"))
            data["instances"][0]["source_refs"] = ["missing-current-reference.txt"]
            target.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assert_failed_with(receipt, "unresolved instance source reference: CLIM-01")

    def test_normalization_exhaustion_is_rejected(self):
        validator = load_validator()
        payload = "%25"
        for _ in range(70):
            payload = urllib.parse.quote(payload, safe="")
        with tempfile.TemporaryDirectory() as temporary:
            copied = self.copy_surface(validator, temporary)
            (copied / "extra.txt").write_text(payload, encoding="utf-8")
            receipt = validator.validate(ROOT, copied)
        self.assertGreater(receipt["private_path_findings"], 0, receipt)
        self.assert_failed_with(receipt, "private path, browser locator, signed URL, or token-like text leaked")

    def test_required_input_absence_is_not_retired_with_history(self):
        validator = load_validator()
        for relative in CURRENT_INPUTS:
            with self.subTest(relative=relative), tempfile.TemporaryDirectory() as temporary:
                copied = self.copy_surface(validator, temporary)
                (copied / relative).unlink()
                receipt = validator.validate(ROOT, copied)
            self.assertEqual(receipt["result"], "FAIL", receipt)


if __name__ == "__main__":
    unittest.main()
