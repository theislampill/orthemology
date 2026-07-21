#!/usr/bin/env python3
"""Focused contract tests for the R7E Sol independent-review control plane.

Runnable with ``python tests/test_r7e_sol_review_state.py``.  The checks are
deterministic and offline: they validate durable review evidence, never merge
readiness or independent sign-off.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys

import yaml


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAILS: list[str] = []

R7D_BASE = "e34d2cd56057766f8f656a4ff3486eb34dad607e"
R7E_HEAD_AT_OBSERVATION = "cbab14747835855d232448f648eefa1d4e36074e"
REQUIRED_MODEL = "gpt-5.6-sol"

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


def test_prefix_and_state() -> None:
    index = load_yaml("docs/project-closure/HISTORICAL-STATUS-INDEX.yaml")
    rules = index.get("rules", []) if isinstance(index, dict) else []
    rule = next((row for row in rules
                 if row.get("prefix") == "docs/project-closure/r7e-sol/"), None)
    check("R7E-Sol closure prefix exists", rule is not None)
    check("R7E-Sol closure prefix is current-candidate",
          bool(rule) and rule.get("status") == "current-candidate")

    state = load_json("docs/project-closure/r7e-sol/AUTONOMOUS-R7E-SOL-STATE.json")
    check("R7E-Sol state record exists", bool(state))
    observation = state.get("r7e_observation", {}) if isinstance(state, dict) else {}
    check("state records exact R7D base", observation.get("base") == R7D_BASE,
          repr(observation.get("base")))
    check("state records exact R7E head-at-observation",
          observation.get("head_at_observation") == R7E_HEAD_AT_OBSERVATION,
          repr(observation.get("head_at_observation")))
    model = state.get("model_gate", {}) if isinstance(state, dict) else {}
    check("state records the gpt-5.6-sol model gate",
          model.get("required") == REQUIRED_MODEL
          and model.get("selected") == REQUIRED_MODEL
          and model.get("evidence") == "controller-confirmed-agent-model-selection"
          and model.get("environment_variable_observation") is False)
    check("state does not claim sign-off or merge readiness",
          state.get("independent_signoff") is False
          and state.get("ready_for_merge") is False
          and state.get("merged") is False)

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


def test_decision_boundary_and_validator() -> None:
    registry = load_yaml("docs/decision-status.yaml")
    row = registry.get("decisions", {}).get("0034", {}) if isinstance(registry, dict) else {}
    check("Decision 0034 is proposed-candidate on PR #12",
          row.get("status") == "proposed-candidate" and row.get("pr") == 12)
    decision = read("docs/decisions/0034-r7e-sol-independent-repair-contract.md")
    check("Decision 0034 file carries Sol candidate boundary",
          "SOL CANDIDATE" in decision and "Status:** proposed-candidate" in decision)

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


test_prefix_and_state()
test_findings_and_hunks()
test_decision_boundary_and_validator()

print("TOTAL: %d failures" % len(FAILS))
sys.exit(1 if FAILS else 0)
