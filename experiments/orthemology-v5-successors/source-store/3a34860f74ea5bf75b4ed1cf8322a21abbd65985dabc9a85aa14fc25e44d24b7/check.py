"""Replay the finite calculation on supplied manual source interpretations.

No Arabic parser, source-authentication test, or religious verdict is supplied.
"""
from pathlib import Path
from itertools import product
import hashlib
import json

BASE = Path(__file__).resolve().parent
data = json.loads((BASE / "source_rows.json").read_text())
records = data["records"]
# Exact fixture contracts bind every voice and attributed holder/selector, with
# qualifiers. Hashes avoid duplicating source-derived wording in this test.
# These are drift checks, not source-authentication or interpretation proofs.
FIELDS = ("work_id", "role", "antecedents", "attributed_holder", "attributed_selector", "selector_identity", "report_qualifier")
EXPECTED = {
    "qurtubi-48-9-exposition-split": "7b944327812a9f5f6c11c7f7122c328024f00f55a3e0cb08e68d75c266bda0bc",
    "qurtubi-48-9-reported-unified": "4c8db9a321aad64402e3901949880a394eeb7db9c07c5bdf621cb9c496da99fb",
    "qurtubi-48-9-attributed-split": "d41c9e475db0335e63e590c9c3be6c08d210d8cef5dd8a8b9831f7c479d85eb7",
    "ibn-atiyya-48-9-reported-unified": "6e48051efe523fc23ace246c3fb5e7b56eb69389fbd9ea14977b46ca6bfdbcbd",
    "ibn-atiyya-48-9-reported-split": "fa59de8b917bcc7ecf25b47fbfe863cc4aad3250689155989ea059ff5ecb1dba",
    "ibn-ashur-48-9-exposition-unified": "d68ebba20b2fe751c0323b3e07c912f62d4aa9c9f00e7f418f8d30386a8dee7f",
    "ibn-ashur-48-9-ibn-abbas-report": "0f749c9720831ac0c2097833a4867f587141f7a2aa8d15a14a58c67c4910faac",
}
assert data["schema"] == "source-relative-pronoun-records-v2"
assert data["independent_acquisition_of_attributed_authorities"] is False
ids = [r["claim_id"] for r in records]
assert len(ids) == len(set(ids))
assert set(ids) == set(EXPECTED)
assert len(data["target_occurrences"]) == 3
for r in records:
    assert len(r["antecedents"]) == 3
    assert all(v in ("G", "M", None) for v in r["antecedents"])
    contract = {k: r.get(k) for k in FIELDS}
    digest = hashlib.sha256(json.dumps(contract, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    assert digest == EXPECTED[r["claim_id"]], "voice or attribution contract drift: " + r["claim_id"]


def complete_rows(rs):
    # Missing source content is not a wildcard or permission to fill a value.
    return {tuple(r["antecedents"]) for r in rs if None not in r["antecedents"]}


R = complete_rows(records)
assert R == {("M", "M", "G"), ("G", "G", "G")}
partial = [r for r in records if None in r["antecedents"]]
assert len(partial) == 1 and partial[0]["antecedents"] == ["M", "M", None]
assert complete_rows(partial) == set()
assert ("M", "M", "M") not in R
assert ("M", "M", "G") not in complete_rows(partial)

marginals = [sorted({r[i] for r in R}) for i in range(3)]
J = set(product(*marginals))
assert J - R == {("G", "M", "G"), ("M", "G", "G")}
assert all(r[0] == r[1] for r in R)
assert not all(r[0] == r[1] for r in J)
assert all(r[2] == "G" for r in R)

# A copied statement is not a new statement identity or a new distinct reading.
copied = records + [dict(records[0])]
assert complete_rows(copied) == R
assert {r["claim_id"] for r in copied} == set(ids)

# A work may contain both exposition and a report without making them one claim.
ashur = [r for r in records if r["work_id"] == "IBN_ASHUR_TAHRIR"]
assert len(ashur) == 2
own = [r for r in ashur if r["role"] == "direct_exposition_with_reasons"]
assert complete_rows(own) == {("G", "G", "G")}
reported = [r for r in ashur if r["role"] == "reported_attribution"]
assert complete_rows(reported) == set()

print(json.dumps({
    "status": "PASS",
    "claim_records": len(records),
    "complete_claim_records": len(records) - len(partial),
    "voice_and_attribution_contracts_checked": len(EXPECTED),
    "complete_attested_rows_under_supplied_interpretation": sorted(R),
    "independent_coordinate_product": sorted(J),
    "extra_rows": sorted(J - R),
    "complete_row_count": len(R),
    "partial_record_count": len(partial),
    "interpretation_validation": "not performed by this calculation",
}, indent=2))
