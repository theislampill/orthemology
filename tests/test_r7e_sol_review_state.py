#!/usr/bin/env python3
"""Focused contract tests for the R7E Sol review and integration control plane.

Runnable with ``python tests/test_r7e_sol_review_state.py``.  The checks are
deterministic and offline: they validate durable review and merged-main
evidence without self-attesting the containing follow-up commit.
"""
from __future__ import annotations

import hashlib
import contextlib
import copy
import importlib.util
import io
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

import yaml


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAILS: list[str] = []

R7D_BASE = "e34d2cd56057766f8f656a4ff3486eb34dad607e"
R7E_HEAD_AT_OBSERVATION = "cbab14747835855d232448f648eefa1d4e36074e"
REQUIRED_MODEL = "gpt-5.6-sol"
TASK11_APPROVED_COMMIT = "66e148f024359cce380bac47ea3d2fb1750c760a"
TASK12_APPROVED_COMMIT = "fd73f652009f182802b10d547618e7e3b29febd7"
TASK15_REVIEWED_COMMIT = "b22d4351f4d3a76bc3f16b41704a470b4abb1aa5"
TASK16_MAIN_MERGE = "8db1630ab715b0931907c627be97b32399d6f4fc"
TASK16_MERGE_COMMITS = [
    "e12cfbbf880b52c38f4064bb7ec6e4393705e319",
    "4d09fed5f2d2106fd5ecd9a79b1d13e6b9af32fc",
    "f4a4804101202c056a31f3d30f2ef931e1dcca2d",
    "2867f3510c343fea8c7fd6c37b8ad38ce5de83a6",
    "17f6783d5d5a39a90dee7b10573ef6bc3732ae5e",
    TASK16_MAIN_MERGE,
]
TASK16_CASCADE = [
    ("PR #13", TASK16_MERGE_COMMITS[0]),
    ("PR #12", TASK16_MERGE_COMMITS[1]),
    ("PR #11", TASK16_MERGE_COMMITS[2]),
    ("PR #10", TASK16_MERGE_COMMITS[3]),
    ("PR #9", TASK16_MERGE_COMMITS[4]),
    ("PR #8", TASK16_MERGE_COMMITS[5]),
]
TASK16_SUCCESSFUL_RUNS = [
    30317000439, 30317471209, 30317917503, 30317919628,
    30318432384, 30318434266, 30318923898, 30318925662,
    30319389233, 30319391979, 30319878639, 30319880488,
    30320348878,
]

EXPECTED_TOPOLOGY_AT_OBSERVATION = [
    {
        "pr": 8,
        "base_branch": "main",
        "base_head": "43fee0f519e2f6984fb143c1e621c83382e71ec7",
        "head_branch": "closure/r7-noetic-application-experiment-validity",
        "head_at_observation": "b0538601913c8234511a1f1131a58eb23a4a0dc4",
        "state": "OPEN",
        "draft": True,
        "mergeable_at_observation": "MERGEABLE",
        "checks_at_observation": "SUCCESS",
    },
    {
        "pr": 9,
        "base_branch": "closure/r7-noetic-application-experiment-validity",
        "base_head": "b0538601913c8234511a1f1131a58eb23a4a0dc4",
        "head_branch": "candidate/r7b-deep-noetic-latent-math",
        "head_at_observation": "86b8bbdddf35ac1e45748279bac05e5a2d4ed85e",
        "state": "OPEN",
        "draft": True,
        "mergeable_at_observation": "MERGEABLE",
        "checks_at_observation": "SUCCESS",
    },
    {
        "pr": 10,
        "base_branch": "candidate/r7b-deep-noetic-latent-math",
        "base_head": "86b8bbdddf35ac1e45748279bac05e5a2d4ed85e",
        "head_branch": "candidate/r7c-full-math-multitarget-noetic-dynamics",
        "head_at_observation": "3cce235f0e388ba78a093d43c879a2e73262938b",
        "state": "OPEN",
        "draft": True,
        "mergeable_at_observation": "MERGEABLE",
        "checks_at_observation": "SUCCESS",
    },
    {
        "pr": 11,
        "base_branch": "candidate/r7c-full-math-multitarget-noetic-dynamics",
        "base_head": "3cce235f0e388ba78a093d43c879a2e73262938b",
        "head_branch": "candidate/r7d-final-semantic-math-noetic-integration",
        "head_at_observation": "e34d2cd56057766f8f656a4ff3486eb34dad607e",
        "state": "OPEN",
        "draft": True,
        "mergeable_at_observation": "MERGEABLE",
        "checks_at_observation": "SUCCESS",
    },
    {
        "pr": 12,
        "base_branch": "candidate/r7d-final-semantic-math-noetic-integration",
        "base_head": "e34d2cd56057766f8f656a4ff3486eb34dad607e",
        "head_branch": "candidate/r7e-orthing-supplementation",
        "head_at_observation": "cbab14747835855d232448f648eefa1d4e36074e",
        "state": "OPEN",
        "draft": True,
        "mergeable_at_observation": "MERGEABLE",
        "checks_at_observation": "SUCCESS",
    },
]

EXPECTED_CONTROL_PLANE = {
    "reproduction": "docs/project-closure/r7e-sol/R7E-SOL-READONLY-REPRODUCTION.md",
    "clean_clone_verification": "docs/project-closure/r7e-sol/R7E-SOL-CLEAN-CLONE-VERIFICATION.md",
    "finding_matrix": "docs/project-closure/r7e-sol/R7E-INDEPENDENT-FINDING-MATRIX.yaml",
    "hunk_disposition": "docs/project-closure/r7e-sol/R7E-HUNK-DISPOSITION.md",
    "decision": "docs/decisions/0034-r7e-sol-independent-repair-contract.md",
}

EXPECTED_REPRODUCTION_LINK_TARGETS = {
    "AUTONOMOUS-R7E-SOL-STATE.json",
    "R7E-SOL-CLEAN-CLONE-VERIFICATION.md",
    "R7E-INDEPENDENT-FINDING-MATRIX.yaml",
    "R7E-HUNK-DISPOSITION.md",
    "../../decisions/0034-r7e-sol-independent-repair-contract.md",
}

EXPECTED_FINDING_ADJUDICATIONS = {
    "R7E-SOL-F001": ("reproduced", "blocker", 2, "resolved"),
    "R7E-SOL-F002": ("reproduced", "blocker", 3, "resolved"),
    "R7E-SOL-F003": ("reproduced", "blocker", 3, "resolved"),
    "R7E-SOL-F004": ("reproduced", "high", 7, "resolved"),
    "R7E-SOL-F005": ("reproduced", "blocker", 2, "resolved"),
    "R7E-SOL-F006": ("reproduced", "blocker", 8, "resolved"),
    "R7E-SOL-F007": ("reproduced", "blocker", 5, "resolved"),
    "R7E-SOL-F008": ("partially-reproduced", "high", 5, "resolved"),
    "R7E-SOL-F009": ("reproduced", "high", 7, "resolved"),
    "R7E-SOL-F010": ("reproduced", "high", 6, "resolved"),
    "R7E-SOL-F011": ("partially-reproduced", "high", 8, "resolved"),
    "R7E-SOL-F012": ("reproduced", "blocker", 8, "resolved"),
    "R7E-SOL-F013": ("reproduced", "blocker", 8, "resolved"),
    "R7E-SOL-F014": ("reproduced", "blocker", 10, "resolved"),
    "R7E-SOL-F015": ("refuted", "historical-high", 12, "resolved"),
}

EXPECTED_F001_EVIDENCE = [
    "docs/current-candidate-state.yaml stops at a placeholder R7D child and does not name exact PR 11 or PR 12 observations",
    "scripts/validate_candidate_state.py passes the stale natural state",
]

EXPECTED_F011_EVIDENCE = [
    "cbab14747835855d232448f648eefa1d4e36074e:companion/dynamic-orthing-noetic-learning-and-orthability.md:113 and :235 use Pi as the reachability policy/action-sequence argument, while cbab14747835855d232448f648eefa1d4e36074e:docs/notation-registry.yaml:24-26 fixes Pi_A as the complete-profile space; the glyph/role reuse is a notation collision",
    "cbab14747835855d232448f648eefa1d4e36074e:companion/dynamic-orthing-noetic-learning-and-orthability.md:237-238 says correction tracks an objective gradient even though :125-127 disclaims a literal scalar gradient; the objective-gradient formulation overstates the typed contract",
]

EXPECTED_DECISION_BOUNDARY = {
    "schema": "orthemology-decision-candidate-boundary-v1",
    "decision": "0034",
    "status": "proposed-candidate",
    "pr": 12,
    "scope": "review-state-accounting-only",
    "preserves_decisions": ["0001-0022"],
    "reopens": [],
    "independent_signoff": False,
    "ready_for_merge": False,
    "merged": False,
}

EXPECTED_FINDING_IDS = {
    "R7E-SOL-F001",  # stale candidate topology
    "R7E-SOL-F002",  # unreconstructible workflow statistics
    "R7E-SOL-F003",  # duplicate/truncated backlog ledger
    "R7E-SOL-F004",  # absent REBAKE input
    "R7E-SOL-F005",  # stale-topology false pass
    "R7E-SOL-F006",  # argument-map literal-gradient false pass
    "R7E-SOL-F007",  # divergence/curl semantic false pass
    "R7E-SOL-F008",  # DAEE pin/crosswalk adjudication
    "R7E-SOL-F009",  # OSM optimizer precision
    "R7E-SOL-F010",  # epistemology/tawatur boundaries
    "R7E-SOL-F011",  # dynamic companion contradictions
    "R7E-SOL-F012",  # argument-map bridge/status defects
    "R7E-SOL-F013",  # divine-Speech ambiguity
    "R7E-SOL-F014",  # incomplete full math migration
    "R7E-SOL-F015",  # historical glyph defect is closed
}

EXPECTED_R7E_PATHS = {
    "applications/daee-epistemics/SOUND-DESCENT-MODEL-COMPARISON.md",
    "artifacts/dynamic-orthing-noetic-learning-orthability-draft.pdf",
    "artifacts/dynamic-orthing-noetic-learning-orthability-draft.sources.json",
    "companion/DYNAMIC-ORTHABILITY-ARGUMENT-MAP.yaml",
    "companion/dynamic-orthing-noetic-learning-and-orthability.md",
    "docs/current-state.yaml",
    "docs/project-closure/HISTORICAL-STATUS-INDEX.yaml",
    "docs/project-closure/r7e/AUTONOMOUS-R7E-STATE.json",
    "docs/project-closure/r7e/ORTHING-CANDIDATE-BACKLOG.md",
    "docs/provenance/RELEASE-MANIFEST.sha256",
}

DECISION_0001_0022_SHA256 = {
    "0001-analysis-relative-ground-truth.md": "f014c45f78df78b6de99ff3e968c45332a7d18aedd4085fb36c6a57c65b536e4",
    "0002-metaorthemma-configuration-token.md": "d819e97e623fa8e20447ec9496cb2e932071b3fc54604df77c4c24396ecafe07",
    "0003-result-free-pathway-adequacy.md": "25a529b4ed76125f2a10acc824ead56a76ff3d35814457b00b59e07a944fedb4",
    "0004-verdict-registry-normalization.md": "de44e24dcfba515bdef4cc2d62975ffa4ce1b2e18e0c211b707c04ef013acc86",
    "0005-symbol-table-normalization.md": "03237a1f79069913b5978a3ff1c64a876cc3bba1d2b6dfe07100035247e216be",
    "0006-compaction-stale-steer-placement.md": "59206678711c1f7a9c6070669ca6e493efcede731fd5f38a98aa849842992d85",
    "0007-profile-space-definition.md": "1b1e82cdc11f79f21581a338ba1808d60f85a4ccae12b202d6751cca730bca9c",
    "0008-thesis-c-disposition.md": "ebb85a236f5df3ebfa7f7b85c9f74dc16e85ac97e13167abb15b26006c74a111",
    "0009-type-token-soundness-and-concrete-reason.md": "ae9e06caada8f30cbf66a2492dd907f4185af9b960439c668f51d6e292c1d4c6",
    "0010-orthability-sense-and-argument-boundary.md": "4da3849144d33d0df00dc55d7eb66afe60529a59869f04c564c1ea6923454a45",
    "0011-claim-relative-reasoning-path-and-strict-soundness.md": "1bf717823b340e716a0651223b19ec732232581af01a48462d458fab5c291102",
    "0012-reference-model-semantic-contract.md": "cc9d4913a8c69406822a084314548f6315a481887668e66ad4a2a90a4372805f",
    "0013-source-attribution-and-status-normalization.md": "5b164a4ac61104713014916cfdc6bcd9a3a5c748079115da049d02151f958506",
    "0014-generated-project-state-and-whole-state-reread.md": "857ce85efb0865e39385e703a8c67a17321eb1540e1ddbf0b447414ab100e850",
    "0015-latent-state-observation-and-representation-boundary.md": "b769e622706bf510f0f800c19664010b7ec54a19eafdec67b1fa12d97c322c4d",
    "0016-current-review-state-and-historical-supersession.md": "3608ff56c99a33c0577c5af5028481f2904c6bea033ce36619fd0f5f6bfc5cec",
    "0017-private-design-records-and-public-evidence-boundary.md": "f102d2664ef684f1bccd7d1d205342797e49dc0c4de9e79088979a2727108171",
    "0018-experiment-packet-readiness-and-registration-status.md": "60bb1ad891fda3a07640a54d67ea99103336c0228371e679f23de58b59b63ce2",
    "0019-current-sourcing-ledger-and-historical-overlays.md": "529ce916e37e850a62f2198a7ed9593f7188b42924715f5a53782a08069eab83",
    "0020-experiment-inferential-readiness-and-packet-versioning.md": "fc8df4302197b61f9933053980ed803331542a9f3a3c004040176d1a9f5f2f94",
    "0021-daee-epistemics-as-noetic-orthing-application.md": "7a983667afe89f30bbfd783f203b78c6aa71e891690d56de26319e3961e71a77",
    "0022-experiment-methods-and-ready-to-run-gate.md": "739a6bbca2a4804ec5c9d14c2b91798bd76ee1e56344775e0d6ad2a3cc4ed5b7",
}


def check(name: str, condition: bool, detail: str = "") -> None:
    print("[%s] %s%s" % ("PASS" if condition else "FAIL", name,
                         "" if condition or not detail else " — " + detail))
    if not condition:
        FAILS.append(name)


def read(rel: str) -> str:
    path = os.path.join(ROOT, *rel.split("/"))
    if not os.path.exists(path):
        return ""
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def load_yaml(rel: str) -> object:
    text = read(rel)
    return yaml.safe_load(text) if text else {}


def load_json(rel: str) -> object:
    text = read(rel)
    return json.loads(text) if text else {}


def valid_utc_timestamp(value: object) -> bool:
    if not isinstance(value, str) or not re.fullmatch(
            r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", value):
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None and parsed.utcoffset() == timezone.utc.utcoffset(parsed)


def decision_candidate_boundary(text: str) -> object:
    match = re.search(
        r"<!-- decision-candidate-boundary:start -->\s*```yaml\s*(.*?)\s*```\s*"
        r"<!-- decision-candidate-boundary:end -->",
        text,
        flags=re.DOTALL,
    )
    return yaml.safe_load(match.group(1)) if match else {}


def production_validator_exit(overrides: dict[str, str]) -> tuple[int, str]:
    path = os.path.join(ROOT, "scripts", "validate_review_state.py")
    spec = importlib.util.spec_from_file_location("r7e_review_state_probe", path)
    if spec is None or spec.loader is None:
        return 2, "could not import production validator"
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    real_read = module.read
    module.read = lambda rel: overrides.get(rel, real_read(rel))
    module.FAILS.clear()
    output = io.StringIO()
    exit_code = 0
    with contextlib.redirect_stdout(output):
        try:
            module.main()
        except SystemExit as exc:
            exit_code = int(exc.code or 0)
    return exit_code, output.getvalue()


def test_prefix_and_state() -> None:
    index = load_yaml("docs/project-closure/HISTORICAL-STATUS-INDEX.yaml")
    rules = index.get("rules", []) if isinstance(index, dict) else []
    rule = next((row for row in rules
                 if row.get("prefix") == "docs/project-closure/r7e-sol/"), None)
    check("R7E-Sol closure prefix exists", rule is not None)
    check("R7E-Sol closure prefix is current after protected integration",
          bool(rule) and rule.get("status") == "current")
    candidate_prefixes = {
        row.get("prefix"): row for row in rules
        if row.get("prefix") in {
            "docs/project-closure/r7e/",
            "docs/project-closure/r7d/",
            "docs/project-closure/r7c/",
            "docs/project-closure/r7b/",
            "docs/project-closure/r7/",
        }
    }
    check("integrated candidate-era closure records are historical snapshots",
          len(candidate_prefixes) == 5
          and all(row.get("status") == "historical-snapshot"
                  for row in candidate_prefixes.values()))
    check("integrated candidate-era notes contain no false live topology",
          all("unmerged" not in str(row.get("note", "")).lower()
              and "never merged" not in str(row.get("note", "")).lower()
              and "protected-main" in str(row.get("note", "")).lower()
              for row in candidate_prefixes.values()))

    state = load_json("docs/project-closure/r7e-sol/AUTONOMOUS-R7E-SOL-STATE.json")
    check("R7E-Sol state record exists", bool(state))
    check("state records a valid UTC observation timestamp",
          valid_utc_timestamp(state.get("observed_at_utc")),
          repr(state.get("observed_at_utc")))
    observation = state.get("r7e_observation", {}) if isinstance(state, dict) else {}
    check("state records exact R7D base", observation.get("base") == R7D_BASE,
          repr(observation.get("base")))
    check("state records exact R7E head-at-observation",
          observation.get("head_at_observation") == R7E_HEAD_AT_OBSERVATION,
          repr(observation.get("head_at_observation")))
    check("state marks the R7E observation as non-timeless",
          observation.get("timeless_state") is False,
          repr(observation.get("timeless_state")))
    check("state records the exact PR 8-12 topology observation",
          state.get("topology_at_observation") == EXPECTED_TOPOLOGY_AT_OBSERVATION,
          repr(state.get("topology_at_observation")))
    model = state.get("model_gate", {}) if isinstance(state, dict) else {}
    check("state records the gpt-5.6-sol model gate",
          model.get("required") == REQUIRED_MODEL
          and model.get("selected") == REQUIRED_MODEL
          and model.get("evidence") == "controller-confirmed-agent-model-selection"
          and model.get("environment_variable_observation") is False)
    check("state records completed protected integration without follow-up self-attestation",
          state.get("independent_signoff") is True
          and state.get("ready_for_merge") is False
          and state.get("merged") is True)
    task15 = state.get("task15_verification", {})
    check("Task 15 state binds the exact approved remote candidate",
          task15.get("candidate_commit")
          == "ad57371b8ef88c313f9b92c43c7618500337e0ed"
          and task15.get("remote_head")
          == "ad57371b8ef88c313f9b92c43c7618500337e0ed"
          and task15.get("independent_review_verdict") == "APPROVED")
    check("Task 15 state binds exact-SHA CI and clean-clone validation",
          task15.get("github_actions_run") == 30313374447
          and task15.get("github_actions_conclusion") == "SUCCESS"
          and task15.get("workflow_command_count") == 71
          and task15.get("supplemental_command_count") == 8
          and task15.get("clean_clone_head")
          == "ad57371b8ef88c313f9b92c43c7618500337e0ed"
          and task15.get("clean_clone_status_porcelain") == "")
    check("Task 15 state accounts for deterministic all-page PDF QA",
          task15.get("pdf_artifacts") == 6
          and task15.get("pdf_pages") == 61
          and task15.get("raster_passes") == 2
          and task15.get("raster_hash_lists_identical") is True
          and task15.get("visually_inspected_pages") == 61
          and task15.get("prohibited_semantic_hits") == 0)

    baseline = state.get("baseline", {}) if isinstance(state, dict) else {}
    check("baseline accounts for all 56 logical workflow validations",
          baseline.get("logical_validations") == 56
          and baseline.get("passing") == 56)
    check("baseline separates 53 direct passes from three UTF-8 reruns",
          baseline.get("direct_passes") == 53
          and baseline.get("utf8_unchanged_reruns") == 3
          and baseline.get("validator_logic_failures") == 0)
    reruns = baseline.get("utf8_rerun_commands", [])
    check("baseline names the three unchanged UTF-8 reruns", set(reruns) == {
        "python scripts/validate_source_status.py",
        "python scripts/validate_notation.py",
        "python scripts/validate_quran_loci.py",
    })
    pdfs = baseline.get("pdf_rebuild", {})
    check("baseline records six byte-identical PDF rebuilds",
          pdfs.get("artifacts") == 6 and pdfs.get("byte_identical") == 6)
    check("baseline records clean-tree evidence",
          baseline.get("clean_tree", {}).get("porcelain") == "")

    control_plane = state.get("control_plane", {}) if isinstance(state, dict) else {}
    check("state records the exact control-plane links",
          control_plane == EXPECTED_CONTROL_PLANE, repr(control_plane))
    check("every state control-plane link resolves",
          all(bool(read(path)) for path in EXPECTED_CONTROL_PLANE.values()))
    reproduction = read(EXPECTED_CONTROL_PLANE["reproduction"])
    reproduction_links = set(re.findall(r"\]\(([^)]+)\)", reproduction))
    check("reproduction links every control-plane artifact",
          EXPECTED_REPRODUCTION_LINK_TARGETS <= reproduction_links,
          repr(sorted(reproduction_links)))


def test_findings_and_hunks() -> None:
    matrix = load_yaml("docs/project-closure/r7e-sol/R7E-INDEPENDENT-FINDING-MATRIX.yaml")
    findings = matrix.get("findings", []) if isinstance(matrix, dict) else []
    ids = [row.get("id") for row in findings]
    check("finding matrix contains every independent finding ID",
          set(ids) == EXPECTED_FINDING_IDS,
          "missing=%r extra=%r" % (sorted(EXPECTED_FINDING_IDS - set(ids)),
                                   sorted(set(ids) - EXPECTED_FINDING_IDS)))
    check("finding IDs are unique", len(ids) == len(set(ids)))
    allowed_dispositions = {"reproduced", "refuted", "partially-reproduced", "unverified"}
    allowed_terminal = {"open", "resolved", "deferred", "blocked"}
    for row in findings:
        fid = str(row.get("id", "<missing>"))
        check(fid + " has an allowed disposition",
              row.get("disposition") in allowed_dispositions,
              repr(row.get("disposition")))
        check(fid + " has evidence", bool(row.get("evidence")))
        check(fid + " has severity", bool(str(row.get("severity", "")).strip()))
        check(fid + " has a repair task",
              isinstance(row.get("repair_task"), int) and row.get("repair_task") >= 1)
        check(fid + " has terminal status",
              row.get("terminal_status") in allowed_terminal,
              repr(row.get("terminal_status")))

    actual_adjudications = {
        str(row.get("id")): (
            row.get("disposition"),
            row.get("severity"),
            row.get("repair_task"),
            row.get("terminal_status"),
        )
        for row in findings
    }
    check("finding adjudications exactly match the Task 15 boundary",
          actual_adjudications == EXPECTED_FINDING_ADJUDICATIONS,
          repr(actual_adjudications))
    by_id = {str(row.get("id")): row for row in findings}
    check("F001 retains exact review evidence before resolution evidence",
          by_id.get("R7E-SOL-F001", {}).get("evidence", [])[:2]
          == EXPECTED_F001_EVIDENCE,
          repr(by_id.get("R7E-SOL-F001", {}).get("evidence")))
    check("F011 retains exact source evidence before resolution evidence",
          by_id.get("R7E-SOL-F011", {}).get("evidence", [])[:2]
          == EXPECTED_F011_EVIDENCE,
          repr(by_id.get("R7E-SOL-F011", {}).get("evidence")))
    resolved = {fid for fid, values in actual_adjudications.items()
                if values[3] == "resolved"}
    check("all fifteen R7E-Sol findings are terminally resolved",
          resolved == EXPECTED_FINDING_IDS,
          repr(sorted(resolved)))
    todo = read("TODO.md")
    f014_evidence = "\n".join(
        str(item) for item in by_id.get("R7E-SOL-F014", {}).get("evidence", []))
    for task, commit, surfaces in (
        ("Task 11", TASK11_APPROVED_COMMIT, [todo]),
        ("Task 12", TASK12_APPROVED_COMMIT, [todo, f014_evidence]),
    ):
        commit_probe = subprocess.run(
            ["git", "cat-file", "-e", commit + "^{commit}"],
            cwd=ROOT, text=True, encoding="utf-8", capture_output=True, check=False)
        ancestry_probe = subprocess.run(
            ["git", "merge-base", "--is-ancestor", commit, "HEAD"],
            cwd=ROOT, text=True, encoding="utf-8", capture_output=True, check=False)
        check(task + " closure evidence binds the approved repository commit",
              all(commit in surface for surface in surfaces),
              commit)
        check(task + " approved repository commit resolves in current ancestry",
              commit_probe.returncode == 0 and ancestry_probe.returncode == 0,
              (commit_probe.stderr + ancestry_probe.stderr).strip())

    hunk_text = read("docs/project-closure/r7e-sol/R7E-HUNK-DISPOSITION.md")
    rows = re.findall(
        r"^\|\s*`([^`]+)`\s*\|\s*`?(keep|revise|drop|provenance-only)`?\s*\|",
        hunk_text, flags=re.MULTILINE)
    paths = [path for path, _disposition in rows]
    check("all ten PR #12 paths have a disposition",
          set(paths) == EXPECTED_R7E_PATHS and len(paths) == 10,
          "paths=%r" % paths)
    check("each PR #12 path is reviewed exactly once", len(paths) == len(set(paths)))
    check("binary PDF is provenance-only",
          ("artifacts/dynamic-orthing-noetic-learning-orthability-draft.pdf",
           "provenance-only") in rows)
    check("release manifest is provenance-only",
          ("docs/provenance/RELEASE-MANIFEST.sha256", "provenance-only") in rows)
    check("preserved R7E provenance inputs are kept byte-identical",
          ("docs/project-closure/r7e/AUTONOMOUS-R7E-STATE.json", "keep") in rows
          and ("docs/project-closure/r7e/ORTHING-CANDIDATE-BACKLOG.md", "keep") in rows)
    check("hunk disposition records Task 16 integration and follow-up boundary",
          "TASK 16 PROTECTED CASCADE AND FRESH-MAIN PROOF COMPLETE" in hunk_text
          and "FOLLOW-UP PROTECTED READBACK PENDING" in hunk_text)


def test_decision_boundary_and_validator() -> None:
    registry = load_yaml("docs/decision-status.yaml")
    row = registry.get("decisions", {}).get("0034", {}) if isinstance(registry, dict) else {}
    check("Decision 0034 is proposed-candidate on PR #12",
          row.get("status") == "proposed-candidate" and row.get("pr") == 12)
    decision = read("docs/decisions/0034-r7e-sol-independent-repair-contract.md")
    boundary = decision_candidate_boundary(decision)
    check("Decision 0034 carries the exact structured candidate boundary",
          boundary == EXPECTED_DECISION_BOUNDARY, repr(boundary))

    for filename, expected in DECISION_0001_0022_SHA256.items():
        path = os.path.join(ROOT, "docs", "decisions", filename)
        actual = ""
        if os.path.exists(path):
            with open(path, "rb") as handle:
                actual = hashlib.sha256(handle.read()).hexdigest()
        check("historical decision remains byte-identical: " + filename,
              actual == expected, actual)

    proc = subprocess.run(
        [sys.executable, os.path.join(ROOT, "scripts", "validate_review_state.py")],
        cwd=ROOT, text=True, encoding="utf-8", capture_output=True, check=False)
    check("review-state validator enforces the R7E-Sol contract",
          proc.returncode == 0, (proc.stdout + proc.stderr)[-1000:])


def test_task16_merged_main_followup_record() -> None:
    record_path = (
        "docs/project-closure/r7e-sol/R7E-SOL-MERGED-MAIN-VERIFICATION.md")
    record = read(record_path)
    state = load_json(
        "docs/project-closure/r7e-sol/AUTONOMOUS-R7E-SOL-STATE.json")
    task16 = state.get("task16_verification", {}) if isinstance(state, dict) else {}
    todo = read("TODO.md")
    readme = read("README.md")
    status = read("STATUS.md")
    hunk = read("docs/project-closure/r7e-sol/R7E-HUNK-DISPOSITION.md")

    check("Task 16 merged-main verification record exists", bool(record))
    check("Task 16 record binds the exact independently reviewed commit",
          TASK15_REVIEWED_COMMIT in record)
    check("Task 16 record binds every protected cascade merge commit",
          task16.get("merge_commits") == TASK16_MERGE_COMMITS
          and all(
              re.search(
                  r"\|\s*" + re.escape(pr)
                  + r"[^|]*\|\s*`" + re.escape(commit) + r"`\s*\|",
                  record)
              for pr, commit in TASK16_CASCADE))
    check("Task 16 record binds every successful exact-SHA CI run",
          all(str(run) in record for run in TASK16_SUCCESSFUL_RUNS))
    check("Task 16 record states the non-self-referential follow-up rule",
          "never self-hashed" in record
          and "protected readback" in record
          and "Git history" in record)
    check("Task 16 state binds merged main and the complete fresh-main proof",
          task16.get("reviewed_commit") == TASK15_REVIEWED_COMMIT
          and task16.get("main_merge_commit") == TASK16_MAIN_MERGE
          and task16.get("github_actions_runs") == TASK16_SUCCESSFUL_RUNS
          and task16.get("workflow_command_count") == 71
          and task16.get("supplemental_command_count") == 8
          and task16.get("pdf_pages") == 61
          and task16.get("visually_inspected_pages") == 61
          and task16.get("visual_defects") == 0
          and task16.get("tracked_paths") == 707
          and task16.get("release_manifest_entries") == 706
          and task16.get("prohibited_semantic_hits") == 0
          and task16.get("ar6_records") == 1329
          and task16.get("ar6_unclassified_counters") == 0)
    check("Task 16 state records the completed cascade without self-attestation",
          state.get("merged") is True
          and state.get("ready_for_merge") is False
          and task16.get("followup_record_self_hashed") is False
          and task16.get("followup_protected_readback") == "pending")
    check("TODO records Tasks 1-16 complete through merged-main verification",
          "### Task 16 — Perform the authorized protected integration cascade"
          in todo
          and "Status: completed through protected-main merge and fresh-main verification"
          in todo
          and "- [ ] Execute and verify the protected PR cascade" not in todo)
    for task in range(1, 11):
        match = re.search(
            r"^### Task %d\b(?P<body>.*?)(?=^### Task \d+\b|\Z)" % task,
            todo, flags=re.MULTILINE | re.DOTALL)
        body = match.group("body") if match else ""
        check("TODO Task %d records protected-main integration" % task,
              bool(body)
              and "integrated to protected `main`" in body
              and "not merged to `main`" not in body
              and "inherits Tasks 15–16 integration gates" not in body)
    check("README records the verified protected-main integration",
          TASK16_MAIN_MERGE in readme
          and "R7E-SOL-MERGED-MAIN-VERIFICATION.md" in readme
          and "Decisions 0020–0036 are `proposed-candidate` in the unmerged PR chain"
          not in readme
          and "No PR is merged" not in readme)
    check("STATUS points to the current R7E merged-main verification",
          "docs/project-closure/r7e-sol/R7E-SOL-MERGED-MAIN-VERIFICATION.md"
          in status)
    check("hunk disposition contains no stale Task 16 future tense",
          "must be regenerated after each Task 16 merge" not in hunk
          and "Task 16 must regenerate it last" not in hunk
          and "Correctly classifies R7E as current-candidate" not in hunk)
    check("AR6 remains interrupted and unapplied",
          task16.get("ar6_status") == "INTERRUPTED_IN_PROGRESS"
          and task16.get("ar6_integration_status") == "NOT_APPLIED_NOT_APPROVED")


def test_production_validator_rejects_adversarial_mutations() -> None:
    state_path = "docs/project-closure/r7e-sol/AUTONOMOUS-R7E-SOL-STATE.json"
    matrix_path = "docs/project-closure/r7e-sol/R7E-INDEPENDENT-FINDING-MATRIX.yaml"
    decision_path = "docs/decisions/0034-r7e-sol-independent-repair-contract.md"

    state = load_json(state_path)
    matrix = load_yaml(matrix_path)
    decision = read(decision_path)

    reviewer_state = copy.deepcopy(state)
    reviewer_state.pop("observed_at_utc", None)
    reviewer_state.pop("topology_at_observation", None)
    reviewer_matrix = copy.deepcopy(matrix)
    reviewer_f001 = next(row for row in reviewer_matrix["findings"]
                         if row["id"] == "R7E-SOL-F001")
    reviewer_f001.update(
        disposition="refuted",
        evidence=["fabricated"],
        severity="none",
        repair_task=99,
        terminal_status="resolved",
    )

    invalid_timestamp = copy.deepcopy(state)
    invalid_timestamp["observed_at_utc"] = "2026-07-21T19:10:22+01:00"

    mutated_topology = copy.deepcopy(state)
    mutated_topology["topology_at_observation"][2]["head_branch"] = "fabricated"

    mutated_control_plane = copy.deepcopy(state)
    mutated_control_plane["control_plane"]["reproduction"] = "fabricated.md"

    reopened_f014 = copy.deepcopy(matrix)
    f014 = next(row for row in reopened_f014["findings"]
                if row["id"] == "R7E-SOL-F014")
    f014["terminal_status"] = "open"

    open_f015 = copy.deepcopy(matrix)
    f015 = next(row for row in open_f015["findings"]
                if row["id"] == "R7E-SOL-F015")
    f015["terminal_status"] = "open"

    mutated_decision = decision.replace(
        "status: proposed-candidate", "status: adopted-merged", 1)

    wrong_intermediate = copy.deepcopy(state)
    wrong_intermediate["task16_verification"]["merge_commits"][2] = "0" * 40

    missing_intermediate = copy.deepcopy(state)
    missing_intermediate["task16_verification"]["merge_commits"].pop(3)

    false_self_attestation = copy.deepcopy(state)
    false_self_attestation["task16_verification"]["followup_record_self_hashed"] = True

    reopened_task16 = copy.deepcopy(state)
    reopened_task16["merged"] = False

    promoted_ar6 = copy.deepcopy(state)
    promoted_ar6["task16_verification"]["ar6_status"] = "COMPLETED"
    promoted_ar6["task16_verification"]["ar6_integration_status"] = "APPLIED"

    verification_path = (
        "docs/project-closure/r7e-sol/R7E-SOL-MERGED-MAIN-VERIFICATION.md")
    verification = read(verification_path)
    false_containing_commit = verification.replace(
        "they are never self-hashed or named by a\ntracked equality contract.",
        "containing commit: " + ("1" * 40))
    prohibited_public_term = verification + "\n" + ("Tachi" + "koma") + "\n"

    cases = [
        ("reviewer's missing-observation and fabricated-F001 mutation", {
            state_path: json.dumps(reviewer_state),
            matrix_path: yaml.safe_dump(reviewer_matrix, sort_keys=False),
        }),
        ("non-UTC observation timestamp", {state_path: json.dumps(invalid_timestamp)}),
        ("mutated PR topology branch", {state_path: json.dumps(mutated_topology)}),
        ("mutated control-plane link", {state_path: json.dumps(mutated_control_plane)}),
        ("F014 improperly reopened", {matrix_path: yaml.safe_dump(reopened_f014, sort_keys=False)}),
        ("F015 no longer resolved", {matrix_path: yaml.safe_dump(open_f015, sort_keys=False)}),
        ("Decision 0034 candidate self-promotion", {decision_path: mutated_decision}),
        ("wrong intermediate cascade merge identity", {
            state_path: json.dumps(wrong_intermediate),
        }),
        ("missing intermediate cascade merge identity", {
            state_path: json.dumps(missing_intermediate),
        }),
        ("false follow-up self-attestation", {
            state_path: json.dumps(false_self_attestation),
        }),
        ("Task 16 reopened after protected integration", {
            state_path: json.dumps(reopened_task16),
        }),
        ("interrupted AR6 research promoted", {
            state_path: json.dumps(promoted_ar6),
        }),
        ("containing commit falsely attested in tracked record", {
            verification_path: false_containing_commit,
        }),
        ("prohibited public terminology introduced", {
            verification_path: prohibited_public_term,
        }),
    ]
    for name, overrides in cases:
        exit_code, output = production_validator_exit(overrides)
        check("production validator rejects " + name,
              exit_code != 0, output[-800:])


test_prefix_and_state()
test_findings_and_hunks()
test_decision_boundary_and_validator()
test_task16_merged_main_followup_record()
test_production_validator_rejects_adversarial_mutations()

print("TOTAL: %d failures" % len(FAILS))
sys.exit(1 if FAILS else 0)
