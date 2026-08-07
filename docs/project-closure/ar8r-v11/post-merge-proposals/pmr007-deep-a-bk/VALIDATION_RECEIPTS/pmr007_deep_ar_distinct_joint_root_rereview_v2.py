#!/usr/bin/env python3
"""Preserved first rereview harness. Contains the recorded boundary bug."""
from fractions import Fraction
import json
from pathlib import Path
OUT=Path(__file__).with_name(Path(__file__).stem+"_results.json")
fail=[]
# The intended check: naive independent multiplication should differ from one-root evidence
# whenever the finite root likelihood ratio is informative. This buggy version forgot that L=0
# is idempotent and therefore is not a diagnostic inequality witness.
for j in range(6):
    L=Fraction(0)
    if L**2 == L:
        fail.append({"kind":"common_cause_no_overcount","case":j,"L":str(L),"defect":"harness treated L=0 as requiring L^2 != L"})
result={"identity":"PMR-007-PREC-1","rereview_version":"V2_PRESERVED_FAILED_HARNESS",
        "counts":{"common_cause_cases":6,"failures":len(fail)},"failures":fail,"result":"FAIL"}
OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
print(json.dumps(result,indent=2,sort_keys=True))
raise SystemExit(1)
