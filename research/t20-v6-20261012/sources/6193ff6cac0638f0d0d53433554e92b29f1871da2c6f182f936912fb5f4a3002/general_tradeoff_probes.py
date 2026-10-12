"""Finite controls for the displayed common-domain quantifier-duality proof.

None in a table means an inadmissible profile, not a created outcome or an idle
setting. These arbitrary tables do not use the author's Latin law.
"""
from itertools import product
from pathlib import Path
import datetime
import json


def properties(entries, na, nb, targets):
    def entry(a, b):
        return entries[a * nb + b]
    reactive_a = all(any(entry(a, b) == q for a in range(na))
                     for q in targets for b in range(nb))
    reactive_b = all(any(entry(a, b) == q for b in range(nb))
                     for q in targets for a in range(na))
    columns = [{entry(a, b) for a in range(na)} - {None} for b in range(nb)]
    rows = [{entry(a, b) for b in range(nb)} - {None} for a in range(na)]
    uniform_b = any(values == {q} for values in columns for q in targets)
    uniform_a = any(values == {q} for values in rows for q in targets)
    return reactive_a, reactive_b, uniform_a, uniform_b


results = []
for name, na, nb, targets, symbols in (
    ("all_partial_3_by_2_two_target_domains", 3, 2, (0, 1), (None, 0, 1)),
    ("all_total_3_by_3_three_target_tables", 3, 3, (0, 1, 2), (0, 1, 2)),
):
    counts = {"tables": 0, "A_fully_reactive": 0, "B_fully_reactive": 0,
              "both_fully_reactive": 0, "reactive_nonrectangular_domains": 0}
    for entries in product(symbols, repeat=na * nb):
        ra, rb, ua, ub = properties(entries, na, nb, targets)
        assert not (ra and ub)
        assert not (rb and ua)
        counts["tables"] += 1
        counts["A_fully_reactive"] += ra
        counts["B_fully_reactive"] += rb
        counts["both_fully_reactive"] += ra and rb
        counts["reactive_nonrectangular_domains"] += (ra or rb) and None in entries
    results.append({"case": name, **counts})

# The nontrivial-target assumption is necessary.
assert properties((0, 0, 0, 0), 2, 2, (0,)) == (True, True, True, True)

# Different comparison domains do not support the contradiction.
# A's responses see the full column [0,1]; a restricted B claim sees only [0].
assert properties((0, 1), 2, 1, (0, 1))[0]
assert properties((0, None), 2, 1, (0, 1))[3]
assert not properties((0, None), 2, 1, (0, 1))[0]

out = {"at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
       "result": "all independent general-law controls passed",
       "scope": "Finite regression controls for ordinary quantifier duality. No Cartesian admissibility, source transport, or metaphysical possibility is thereby established.",
       "cases": results,
       "negative_controls": ["one exact target permits both properties", "different domains invalidate the combined inference"]}
Path(__file__).with_name("GENERAL_TRADEOFF_PROBES.json").write_text(json.dumps(out, indent=2) + "\n")
print(json.dumps(out, indent=2))
