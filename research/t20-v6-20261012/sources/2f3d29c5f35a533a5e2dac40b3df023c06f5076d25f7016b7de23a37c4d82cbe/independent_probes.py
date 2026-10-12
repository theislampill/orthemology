"""Independent diagnostic probes; no author source is modified."""
import datetime
import itertools
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "sovereignty-choice-semantics/reactive-context-extension/src"
sys.path.insert(0, str(SOURCE))
import reactive_context as r

c = r.Catalogue(("e0", "e1"))
rows = []
for q, b in itertools.product(range(3), repeat=2):
    a = c.respond(q, b)
    result = r.execute(c, r.Original("A").issue(q, a), r.Original("B").issue(b, b))
    rows.append({
        "A_goal": q, "A_setting": a, "B_goal": b, "B_setting": b,
        "created": sorted(result["events"]), "intentions": result["intentions"],
        "A_same_full_target_setting": a == q,
    })
assert sum(not x["intentions"]["B"] for x in rows) == 6
assert all(len({c.respond(q, b) for b in range(3)}) == 3 for q in range(3))
envelopes = []
for q, a in itertools.product(range(3), repeat=2):
    peers = [b for b in (None, 0, 1, 2) if c.combine(a, b) == q]
    expected = ([None] if a == q else []) + [(2 * q - a) % 3]
    assert peers == expected
    envelopes.append({"goal": q, "own_setting": a, "maximal_exact_target_peer_domain": peers})

model = r.epistemic_model(c)
represented = {
    (w["context"], w["actual"]["acts"][0].setting, w["actual"]["acts"][1].setting)
    for w in model["worlds"]
}
solved = {(q, a, b) for q in range(3) for a, b in r.response_pairs(c, q, q)}
assert len(represented) == 3 and len(solved) == 9 and represented < solved

fixed = r.Original("A").issue(0, 0)
peer = r.Original("B").issue(1, 1)
frozen = r.execute(c, fixed, peer)
adapted_act = r.Original("A").issue(0, c.respond(0, 1))
adapted = r.execute(c, adapted_act, peer)
solo = r.execute(c, adapted_act, None)
assert frozen["events"] == frozenset(("e0", "e1"))
assert adapted["events"] == frozenset(("e0",))
assert solo["events"] == frozenset(("e0", "e1"))

result = {
    "at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "result": "independent finite checks passed",
    "limitations": "Finite semantic checks only. No physical causal completeness, metaphysical admissibility, all-premise countermodel, or proof-kernel certification.",
    "contexts": {
        "epistemic_diagonal": sorted(represented),
        "equal_goal_solved_operational": sorted(solved),
    },
    "response_rows": rows,
    "uniform_control_envelopes": envelopes,
    "concrete_counterexample": {
        "frozen_A_goal0_setting0_B_goal1_setting1": sorted(frozen["events"]),
        "adapted_A_goal0_setting2_B_goal1_setting1": sorted(adapted["events"]),
        "adapted_A_alone": sorted(solo["events"]),
    },
}
(HERE / "INDEPENDENT_PROBES.json").write_text(json.dumps(result, indent=2) + "\n")
print("Independent probes passed: frozen/adapted/solo outputs; six peer-intention failures; nine solved profiles versus three ordinary epistemic worlds; all nine maximal fixed-setting control envelopes.")
