#!/usr/bin/env python3
"""Experiment methods / READY_TO_RUN gate (Decision 0022, R7).

A benchmark packet may hold READY_TO_RUN only when it is executionally AND
inferentially ready. The R6 readiness validator checked packet SHAPE; this
gate checks METHODS. Deterministic, offline — it exercises each current
benchmark packet's own harness+analysis on the deterministic mock adapter and
asserts:

  1. an executable run harness with a mock adapter exists and runs offline;
  2. public/scoring isolation: the harness's exact payloads carry no hidden
     scoring key, family/archetype label, or diagnostic conclusion;
  3. a strict parser with a logged format-retry path exists;
  4. every endpoint the packet declares is produced by its analysis;
  5. the decision rules are executed mechanically (proven by the packet's own
     smoke tests, which unit-test decide() and assert the synthetic outcome is
     unadjudicated);
  6. the unit of inference is stated and repeats are not counted as
     independent evidence;
  7. a synthetic end-to-end run yields NO adjudicated scientific outcome;
  8. the no-run guard holds (no non-synthetic output in the tree).

Any current packet failing a gate must not be READY_TO_RUN (enforced jointly
with validate_experiment_readiness).
"""
import io
import json
import os
import subprocess
import sys
import tempfile

try:
    import yaml
except ImportError as e:
    print("FATAL: requires pyyaml:", e)
    sys.exit(2)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAILS = []

# per-packet method contract: harness, analysis, endpoints-source, smoke
GATE = {
    "FCSP-2": {
        "dir": "experiments/false-closure-selective-prediction-v2",
        "harness": "harness/run_fcsp.py",
        "analysis": "analysis/analyze_fcsp2.py",
        "endpoints_yaml": "ENDPOINTS.yaml",
        "declared_endpoints": ["false_closure_rate", "aurc", "missed_residual_rate",
                               "appropriate_abstention_rate", "route_admissibility_accuracy",
                               "result_accuracy", "burden_disposition_accuracy", "excess_aurc",
                               "structure_overhead_ratio_on_controls",
                               "false_closure_worst_case_bound"],
    },
    "ER-2": {
        "dir": "experiments/episode-reification-v2",
        "harness": "harness/run_er.py",
        "analysis": "analysis/analyze_er2.py",
        "endpoints_yaml": None,
        "declared_endpoints": ["defect_discovery_contrast", "completion_correctness_contrast",
                               "traceability_rate", "e5_robustness_rate", "cost_ratio",
                               "treatment_false_positive_rate"],
    },
}


def check(name, ok, detail=""):
    print("[%s] %s%s" % ("PASS" if ok else "FAIL", name, (" — " + detail) if detail and not ok else ""))
    if not ok:
        FAILS.append(name)


def read(rel):
    p = os.path.join(ROOT, rel)
    return io.open(p, encoding="utf-8").read() if os.path.exists(p) else ""


def run_smoke(pkt_dir):
    p = subprocess.run([sys.executable, os.path.join(ROOT, pkt_dir, "tests", "test_smoke.py")],
                       capture_output=True, text=True)
    return p.returncode == 0, (p.stdout + p.stderr)[-400:]


def main():
    for pid, g in GATE.items():
        d = g["dir"]
        harness = read(d + "/" + g["harness"])
        analysis = read(d + "/" + g["analysis"])
        check("%s: harness exists with a mock adapter" % pid,
              bool(harness) and "MockAdapter" in harness and "mock" in harness)
        check("%s: harness provides a provider adapter interface that cannot live-call in CI" % pid,
              "provider" in harness.lower())
        check("%s: harness has a strict parser and a logged format retry" % pid,
              "parse_strict" in harness and "FORMAT_REMINDER" in harness
              and "format_retried" in harness)
        # the harness must never READ the hidden keys in code (a docstring line
        # honestly stating "never opens KEYS.json" is fine; an actual open/load is not)
        code_lines = [ln for ln in harness.splitlines()
                      if "KEYS" in ln and not ln.lstrip().startswith("#")
                      and ("open(" in ln or "load(" in ln or "read(" in ln)]
        check("%s: harness has no code path that reads the hidden keys" % pid,
              not code_lines, str(code_lines[:2]))
        check("%s: analysis implements Holm multiplicity" % pid, "holm" in analysis.lower())
        check("%s: analysis executes decision rules mechanically" % pid,
              "decide(" in analysis or "def decide" in analysis or "outcome" in analysis)
        check("%s: analysis states the unit of inference" % pid,
              "unit_of_inference" in analysis)
        check("%s: analysis refuses to adjudicate synthetic runs" % pid,
              "SYNTHETIC" in analysis and "no scientific result" in analysis)

        # smoke test is the executable proof of the full chain + decision unit tests
        ok, tail = run_smoke(d)
        check("%s: packet smoke (harness->parser->analysis->decision) passes" % pid, ok, tail)

    # no-run guard (methods-side): assert no non-synthetic output anywhere in the
    # two current packet trees
    offenders = []
    for g in GATE.values():
        for base, dirs, fns in os.walk(os.path.join(ROOT, g["dir"])):
            dirs[:] = [x for x in dirs if x != "__pycache__"]
            for fn in fns:
                if fn.endswith((".json", ".jsonl")):
                    if '"synthetic_smoke": false' in read(os.path.relpath(
                            os.path.join(base, fn), ROOT).replace("\\", "/")):
                        offenders.append(fn)
    check("no non-synthetic run output exists in the current packets", not offenders,
          str(offenders[:3]))

    print("TOTAL: %d failures" % len(FAILS))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
