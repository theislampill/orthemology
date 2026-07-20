#!/usr/bin/env python3
"""Deterministic fixture generator for ER-1.

For each case E1-E5 (+ E5 neighbors), renders ONE canonical fact set into the
two arm forms: an ordinary chronological audit log (baseline-log.md) and an
explicit episode/verdict record (treatment-episode.json). Both forms carry
every fact atom (tests/test_smoke.py checks coverage), so information content
is matched by construction. Committed fixtures must equal regeneration.
"""
import io
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
FIX = os.path.join(HERE, "..", "fixtures")

# fact atoms: (key, log sentence, episode field path, episode value)
CASES = {
  "E1": {
    "title": "nominal control",
    "occurrence": ("artifact-114", "v3"),
    "facts": [
      ("identity", "Case artifact-114 version v3 entered checking on 2026-03-02.", "occurrence", {"identity_key": "artifact-114", "version": "v3"}),
      ("evidence", "Measurement M-77 (taken 2026-03-02, covers surface finish of artifact-114 v3, valid 30 days) read 0.82.", "evidence", [{"id": "M-77", "covers": "surface finish, artifact-114 v3", "taken": "2026-03-02", "valid_days": 30, "value": 0.82}]),
      ("procedure", "The finish gauge was calibrated 2026-02-20 against the current reference block.", "procedure", {"name": "finish gauge", "calibrated": "2026-02-20", "reference": "current block"}),
      ("execution", "Operator followed work instruction WI-9 as written.", "execution", {"instruction": "WI-9", "faithful": True}),
      ("result", "The check concluded PASS (finish within tolerance).", "result", {"placement": "PASS"}),
      ("closure", "The completion draft lists no open obligations.", "burden_ledger", []),
    ],
  },
  "E2": {
    "title": "stopped-clock",
    "occurrence": ("batch-2201", "v1"),
    "facts": [
      ("identity", "Case batch-2201 version v1 entered screening on 2026-04-11.", "occurrence", {"identity_key": "batch-2201", "version": "v1"}),
      ("evidence", "Screen S-3 (covers contaminant class A in batch-2201 v1) read NEGATIVE.", "evidence", [{"id": "S-3", "covers": "contaminant class A, batch-2201 v1", "value": "NEGATIVE"}]),
      ("procedure", "Screen S-3 compares against reference panel RP-2025-10, frozen 2025-10-01 and not updated since.", "procedure", {"name": "screen S-3", "reference": "RP-2025-10", "reference_frozen": "2025-10-01", "reliability_note": "reference panel stale beyond declared refresh interval"}),
      ("execution", "Technician ran S-3 exactly per its manual.", "execution", {"instruction": "S-3 manual", "faithful": True}),
      ("result", "An independent confirmatory assay later agreed the batch is clean.", "result", {"placement": "NEGATIVE", "independent_confirmation": True}),
      ("closure", "The completion draft declares screening complete on the S-3 result.", "burden_ledger", [{"burden": "reference-panel refresh overdue", "disposition": "open"}]),
    ],
  },
  "E3": {
    "title": "justified rare miss",
    "occurrence": ("plot-88", "v2"),
    "facts": [
      ("identity", "Case plot-88 version v2 (post-resurvey) entered boundary review on 2026-05-06.", "occurrence", {"identity_key": "plot-88", "version": "v2"}),
      ("evidence", "Survey E-12 (covers plot-88 v2 boundary, taken 2026-05-05, instrument within calibration) shows conformance.", "evidence", [{"id": "E-12", "covers": "boundary, plot-88 v2", "taken": "2026-05-05", "value": "conforms"}]),
      ("procedure", "The declared method resolves offsets to 5 cm; its reference-class error rate is on record and acceptable.", "procedure", {"name": "boundary method", "resolution_cm": 5, "reliability_note": "declared reference-class reliability met"}),
      ("execution", "Surveyor followed the method fully.", "execution", {"instruction": "boundary method", "faithful": True}),
      ("result", "The review concluded CONFORMS; a later 1 cm-resolution audit found a 3 cm encroachment (below the method's discrimination power).", "result", {"placement": "CONFORMS", "later_finer_audit": "3 cm encroachment found"}),
      ("closure", "The completion draft closes the review on the method's result.", "burden_ledger", []),
    ],
  },
  "E4": {
    "title": "defective binding, faithful execution",
    "occurrence": ("weld-51", "v1"),
    "facts": [
      ("identity", "Case weld-51 version v1 entered inspection on 2026-06-14.", "occurrence", {"identity_key": "weld-51", "version": "v1"}),
      ("evidence", "Radiograph R-4 (covers weld-51 v1 porosity, current) was taken and archived.", "evidence", [{"id": "R-4", "covers": "porosity, weld-51 v1", "value": "3 pores/dm"}]),
      ("binding", "The job card bound acceptance standard AS-2019 edition; the contract for this job specifies the stricter AS-2024 edition.", "governing_binding", {"bound_edition": "AS-2019", "contract_edition": "AS-2024", "binding_defect": True}),
      ("execution", "Inspector applied AS-2019 exactly as bound on the card.", "execution", {"instruction": "AS-2019 as bound", "faithful": True}),
      ("result", "Under AS-2019 the weld PASSES; under AS-2024 it also happens to pass, at the margin.", "result", {"placement": "PASS", "note": "passes under both editions; margin thin under AS-2024"}),
      ("closure", "The completion draft records acceptance without noting the edition discrepancy.", "burden_ledger", [{"burden": "edition rebinding + re-derivation", "disposition": "open"}]),
    ],
  },
  "E5": {
    "title": "metamorphic marker probe",
    "occurrence": ("report-9", "v1"),
    "facts": [
      ("identity", "Case report-9 version v1 entered format verification on 2026-07-01.", "occurrence", {"identity_key": "report-9", "version": "v1"}),
      ("evidence", "Verifier V-1 passes a report iff it contains the string 'ANALYSIS COMPLETE'.", "evidence", [{"id": "V-1", "covers": "marker presence only", "rule": "pass iff contains 'ANALYSIS COMPLETE'"}]),
      ("procedure", "V-1's declared purpose is to verify the analysis section is complete and correct.", "procedure", {"name": "V-1", "declared_purpose": "analysis completeness/correctness", "actual_check": "marker string presence"}),
      ("execution", "V-1 ran and reported PASS on report-9 v1.", "execution", {"instruction": "V-1", "faithful": True}),
      ("result", "Report-9 v1's analysis is in fact complete and correct.", "result", {"placement": "PASS", "truth": "analysis genuinely complete"}),
      ("neighbors", "Variant E5a: the same correct analysis with the marker line deleted — V-1 FAILS it. Variant E5b: a truncated, wrong analysis that still contains the marker — V-1 PASSES it.", "perturbation_neighbors", [{"id": "E5a", "truth": "correct", "v1_verdict": "FAIL"}, {"id": "E5b", "truth": "incorrect", "v1_verdict": "PASS"}]),
      ("closure", "The completion draft declares verification complete on V-1's pass.", "burden_ledger", [{"burden": "replace marker rule with property-tracking check", "disposition": "open"}]),
    ],
  },
}


def render(case_id, spec):
    d = os.path.join(FIX, case_id)
    os.makedirs(d, exist_ok=True)
    facts_lines = ["schema: orthemology-er-facts-v1", "case: " + case_id,
                   "title: " + spec["title"], "fact_keys:"]
    for key, _s, _p, _v in spec["facts"]:
        facts_lines.append("- " + key)
    io.open(os.path.join(d, "facts.yaml"), "w", encoding="utf-8", newline="\n").write(
        "\n".join(facts_lines) + "\n")

    log = ["# Audit log — case %s (%s)" % (spec["occurrence"][0], spec["title"]), ""]
    for i, (_k, sentence, _p, _v) in enumerate(spec["facts"], 1):
        log.append("%d. %s" % (i, sentence))
    log.append("")
    io.open(os.path.join(d, "baseline-log.md"), "w", encoding="utf-8", newline="\n").write(
        "\n".join(log))

    ep = {"schema": "orthemology-er-episode-v1", "case": case_id, "title": spec["title"]}
    for _k, _s, path, value in spec["facts"]:
        ep[path] = value
    io.open(os.path.join(d, "treatment-episode.json"), "w", encoding="utf-8", newline="\n").write(
        json.dumps(ep, indent=2, ensure_ascii=False) + "\n")


def main():
    for cid, spec in CASES.items():
        render(cid, spec)
    print("rendered %d cases" % len(CASES))


if __name__ == "__main__":
    main()
