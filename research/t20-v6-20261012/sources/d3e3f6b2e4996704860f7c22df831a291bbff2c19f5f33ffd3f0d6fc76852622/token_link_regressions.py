"""Check correspondence of actual acts, proof inputs, and direct graph edges.

This is representation-linkage validation, not a new metaphysical nonreceipt
argument. It does not change any author file.
"""
from copy import deepcopy
from pathlib import Path
import datetime
import json
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "sovereignty-choice-semantics/reactive-context-extension/src"))
from reactive_context import Catalogue, epistemic_model


def validate(world):
    actual = world["actual"]
    expected = {(act.token, event) for act in actual["acts"] for event in actual["events"]}
    proof_edges = {(token, event) for event, proof in actual["proofs"].items()
                   for token in proof["intrinsic_inputs"]}
    graph_edges = set(world["efficient_edges"])
    if proof_edges != expected:
        raise ValueError("Proof inputs are not exactly the represented actual exercise inputs.")
    if graph_edges != proof_edges:
        raise ValueError("Direct graph causes do not exactly match the production proof inputs.")


def rejected(world):
    try:
        validate(world)
    except ValueError:
        return True
    return False


worlds = epistemic_model(Catalogue(("e0", "e1")))["worlds"]
controls = []
for world in worlds:
    validate(world)
    event = sorted(world["actual"]["events"])[0]
    orphan_proof = deepcopy(world)
    orphan_proof["actual"]["proofs"][event]["intrinsic_inputs"] += ("orphan_act",)
    assert rejected(orphan_proof)
    orphan_graph = deepcopy(world)
    orphan_graph["efficient_edges"] += (("orphan_act", event),)
    assert rejected(orphan_graph)
    missing_graph = deepcopy(world)
    missing_graph["efficient_edges"] = tuple(edge for edge in missing_graph["efficient_edges"]
                                              if edge != ("A_act", event))
    assert rejected(missing_graph)
    jointly_wrong = deepcopy(world)
    jointly_wrong["actual"]["proofs"][event]["intrinsic_inputs"] = tuple(
        "orphan_act" if token == "A_act" else token
        for token in jointly_wrong["actual"]["proofs"][event]["intrinsic_inputs"])
    jointly_wrong["efficient_edges"] = tuple(
        ("orphan_act", e) if (token, e) == ("A_act", event) else (token, e)
        for token, e in jointly_wrong["efficient_edges"])
    assert rejected(jointly_wrong)
    controls.append({"context": world["context"], "baseline": "pass",
                     "orphan_proof_input": "rejected", "orphan_graph_cause": "rejected",
                     "missing_graph_cause": "rejected", "matching_but_unowned_proof_and_graph_input": "rejected"})

result = {"at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
          "result": "all token-linkage controls passed",
          "baseline_worlds": len(worlds), "rejected_mutations": 4 * len(worlds),
          "controls": controls,
          "scope": "Actual-act/proof-input/direct-graph correspondence only; no new nonreceipt philosophy or changed operational law."}
(HERE / "TOKEN_LINK_REGRESSIONS.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
