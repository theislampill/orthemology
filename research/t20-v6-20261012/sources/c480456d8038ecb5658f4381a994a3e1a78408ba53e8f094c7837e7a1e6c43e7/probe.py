"""Bounded contract probes, not natural-language interpretation or normative certification."""
import copy
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from dataclasses import replace

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parent
PIN = ROOT / "pinned"
spec = importlib.util.spec_from_file_location("inherited_validator", PIN / "scripts/validate_corrective_transition.py")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)
baseline = json.loads((PIN / "applications/daee-epistemics/CORRECTIVE-TRANSITION.example.json").read_text())

# C = an item is accounted for; P = it is punished. These two finite
# possibilities witness only the non-entailment relevant to the author's
# argument. They are not a complete semantics of the verses or a legal code.
open_punishment = [[True, False], [True, True]]
forced_punishment = [[True, True]]

def entails_punishment(possibilities):
    return all(p for c, p in possibilities if c)

def snapshot(anchor, actual, interpreted, version):
    return {
        "source_anchor": anchor,
        "established_content_possibilities": copy.deepcopy(actual),
        "established_content_version": version,
        "interpreted_possibilities": copy.deepcopy(interpreted),
        "operative_punishment_inference": entails_punishment(interpreted),
    }

source_path = ROOT.parent / "wise-reason-root-20261010/SHIFA_e179_e193.txt"
anchor = {"kind": "received-authorial-reading", "path": str(source_path.relative_to(ROOT.parent)),
          "sha256": hashlib.sha256(source_path.read_bytes()).hexdigest(), "markers": "e192-e193"}
repair_before = snapshot(anchor, open_punishment, forced_punishment, "fixed")
repair_after = snapshot(anchor, open_punishment, open_punishment, "fixed")

# Synthetic control ONLY. This is not the Shifa author's account: here an
# earlier rule really supports P and a later rule removes that support.
synthetic_anchor = {"kind": "synthetic-control", "source_authority": "same-authority"}
change_before = snapshot(synthetic_anchor, forced_punishment, forced_punishment, "v1")
change_after = snapshot(synthetic_anchor, open_punishment, open_punishment, "v2")

def same_source_content_frame(a, b):
    return all(a[k] == b[k] for k in ["source_anchor", "established_content_possibilities", "established_content_version"])

snapshots = {"repair-before": repair_before, "repair-after": repair_after,
             "change-before": change_before, "change-after": change_after}

def document(name, before, after, revision):
    d = copy.deepcopy(baseline)
    t = d["transitions"][0]
    t["transition_id"] = name
    t["state_before"] = before
    t["state_after"] = after
    t["live_burdens"] = ["punishment inference", "external interpretation warrant"]
    t["burden_accounting"] = {"addressed": ["punishment inference"], "carried_forward": ["external interpretation warrant"]}
    t["executor_operation"] = "revise the active interpretation; preserve the source-content frame"
    t["delta"] = "operative punishment inference changes from supported to not supported"
    t["evidence"] = ["DECLARED_SNAPSHOTS.json", "received-Shifa-e192-e193"]
    t["global_revision"] = revision
    t["reread"] = {"performed": True, "outcome": "snapshot interpretation adequacy still requires substantive appraisal"}
    t["non_claims"] = ["No actual-world legal ruling, authentication, or human uptake is certified.",
                        "Structural acceptance does not verify the referenced snapshots or their meaning."]
    return d

no_revision = {"requested": False, "authorized": False, "authorization_ref": None}
declared_revision = {"requested": True, "authorized": True, "authorization_ref": "synthetic-authorization-only"}
documents = {
    "honest-fixed-content-repair": document("honest-fixed-content-repair", "repair-before", "repair-after", no_revision),
    "mislabelled-content-change": document("mislabelled-content-change", "change-before", "change-after", no_revision),
    "declared-content-change": document("declared-content-change", "change-before", "change-after", declared_revision),
}
documents["declared-content-change"]["transitions"][0]["executor_operation"] = "synthetic declared source-content revision"
documents["declared-content-change"]["transitions"][0]["evidence"] = ["DECLARED_SNAPSHOTS.json", "synthetic-authorization-only"]
negative = document("requested-but-unauthorized", "change-before", "change-after", {"requested": True, "authorized": False, "authorization_ref": None})
documents["requested-but-unauthorized"] = negative

results = []
for name, d in documents.items():
    ok, reason = validator.document_ok(d)
    expected = name != "requested-but-unauthorized"
    assert ok == expected, (name, ok, reason)
    if not expected:
        assert reason == "unauthorized-global-revision"
    t = d["transitions"][0]
    a, b = snapshots[t["state_before"]], snapshots[t["state_after"]]
    results.append({"name": name, "inherited_document_ok": ok, "reason": reason,
                    "external_declared_frame_preserved": same_source_content_frame(a, b),
                    "operative_output_before": a["operative_punishment_inference"],
                    "operative_output_after": b["operative_punishment_inference"]})

assert same_source_content_frame(repair_before, repair_after)
assert not same_source_content_frame(change_before, change_after)
assert repair_after["interpreted_possibilities"] == repair_after["established_content_possibilities"]
assert repair_before["operative_punishment_inference"] and not repair_after["operative_punishment_inference"]
assert change_before["operative_punishment_inference"] and not change_after["operative_punishment_inference"]
assert [True, True] in open_punishment and [True, False] in open_punishment

(ROOT / "DECLARED_SNAPSHOTS.json").write_text(json.dumps(snapshots, indent=2) + "\n")
(ROOT / "PROBE_DOCUMENTS.json").write_text(json.dumps(documents, indent=2) + "\n")
out = {"contract": "inherited v2 document_ok; external snapshots are not dereferenced by that validator",
       "results": results,
       "non_entailment": {"C_true_P_false": [True, False], "C_true_P_true_still_allowed": [True, True]},
       "status": "PASS at bounded declared-record scope; not a semantic validator bug or a new theorem"}

# Separate native controlled-language probe. This is a service-duty fixture,
# NOT a translation of the Shifa passages into the native location/duty grammar.
occurrence_dir = ROOT.parent / "recovery-t20/checkpoint/Orthemology_T20_Continuation_Owner_Review_Checkpoint_20261008/tranche20/research-resumption/testimony-continuation"
sys.path.insert(0, str(occurrence_dir))
import occurrence_model as om
inherited = om.run_cases()
assert all(r["actual"] == r["expected"] for r in inherited["cases"])
c = om.Context("Principal", "Operator", 0, "lab")
f = ("duty", "you", "inspect", "now", 2)
o = om.Occurrence("unchanged-source-event", c, "Assert", f)
good = om.relay(o)
wrong = ("and", f, ("duty", "you", "penalize", "now", 2))
bad_carrier = replace(good, event="mistaken-derived-carrier", payload=om.encode(wrong, "B"))
premises = om.RecipientPremises({o.event: o}, frozenset({("Principal", "service-duty")}))
assert not om.preservation(o, bad_carrier)
assert om.warranted(o, bad_carrier, premises) is None
assert om.preservation(o, good)
assert om.warranted(o, good, premises) == om.resolve(f, c)
counterfeit_source = replace(o, formula=wrong)
assert om.warranted(counterfeit_source, om.relay(counterfeit_source), premises) is None
out["occurrence_probe"] = {
    "inherited_cases_passed": len(inherited["cases"]),
    "inherited_roundtrips_passed": inherited["roundtrip_cases"],
    "mistaken_derived_content_rejected": True,
    "corrected_derivation_with_fixed_original_accepted": True,
    "same_id_content_substitution_rejected_by_full_anchor": True,
    "new_native_assertions": 5,
    "limit": "native service-duty grammar, not a parsing or semantic formalization of the Shifa source"
}
(ROOT / "PROBE_RESULTS.json").write_text(json.dumps(out, indent=2) + "\n")
print(json.dumps(out, indent=2))
