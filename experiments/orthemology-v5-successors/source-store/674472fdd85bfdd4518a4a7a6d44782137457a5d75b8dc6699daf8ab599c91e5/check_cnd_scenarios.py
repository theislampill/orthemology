"""Finite formula diagnostics only; no metaphysical possibility assertion."""
import json
from pathlib import Path

W = (0, 1)
G, H = "g", "h"

def audit(name, original, received, participation=()):
    # Tuples are (world, producer, concrete occurrence label, causal respect).
    original = set(original)
    received = set(received)
    participation = set(participation) | original
    cnd = all(a == b for w,a,e,r in original for v,b,f,s in original
              if (w,e,r) == (v,f,s))
    pri = all(any(w == v and a == G for v,a,e,r in original) for w in W)
    sup = all(any((w,H,e,r) == row for row in original)
              for w,a,e,r in original if a == G and (w,G) in received)
    weak = all((w,H,e,r) in participation
               for w,a,e,r in original if a == G and (w,G) in received)
    return {"name":name, "CND":cnd, "PRI":pri, "SUP":sup,
            "weak_participation":weak,
            "actual_nonreceipt":(0,G) not in received,
            "essential_nonreceipt":all((w,G) not in received for w in W),
            "production_in_every_world":all(any(row[0]==w for row in original) for w in W)}

cases = [
    audit("role_switch",[(0,G,"e","r"),(0,H,"f","r"),
                         (1,H,"e","r"),(1,H,"f","r")],[(1,G)]),
    audit("participation_only",[(0,G,"e","r"),(1,G,"e","r")],
          [(1,G)],[(1,H,"e","r")]),
    audit("different_respect",[(0,G,"e","r"),(1,G,"e","r"),
                               (1,H,"e","s")],[(1,G)]),
    audit("different_effect",[(0,G,"e","r"),(1,G,"e","r"),
                              (1,H,"f","r")],[(1,G)]),
    audit("duplicate_same_respect",[(0,G,"e","r"),(1,G,"e","r"),
                                    (1,H,"e","r")],[(1,G)]),
    audit("positive_antecedent",[(0,G,"e","r"),(1,G,"f","s")],[]),
]
expected = [(True,False,True,False),(True,True,False,False),
            (True,True,False,False),(True,True,False,False),
            (False,True,True,False),(True,True,True,True)]
for row, wanted in zip(cases, expected):
    assert tuple(row[k] for k in ("CND","PRI","SUP","essential_nonreceipt")) == wanted
    assert row["production_in_every_world"]
    assert not (row["CND"] and row["PRI"] and row["SUP"]) or row["essential_nonreceipt"]
assert cases[1]["weak_participation"]
result = {"status":"six specified formula diagnostics passed",
          "scope":"These assignments do not certify metaphysical possibility or T17 fidelity.",
          "cases":cases}
Path(__file__).with_name("CND_SCENARIOS_v1.json").write_text(
    json.dumps(result,indent=2)+"\n",encoding="utf-8")
print(result["status"])
