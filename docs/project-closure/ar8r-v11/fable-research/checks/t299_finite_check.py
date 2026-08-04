#!/usr/bin/env python3
"""Exhaustive finite check for the T299 fibre-factorization characterization.

Reproduces the exhaustive enumeration recorded in
AR8R-FABLE-R1-LEAN-RECEIPTS.yaml (executable_finite_check.exhaustive_enumeration).

Claim checked, from the definition and without appealing to the theorem:

    Certifiable(P, l)  <=>  FibreConst(P, l)

where Certifiable(P, l) means some c : Prof -> Bool satisfies c(P(b)) = l(b)
for every b (decided by brute force over all 2^|Prof| candidates), and
FibreConst(P, l) means P(b) = P(b') implies l(b) = l(b').

Input domain and enumeration bounds:
    background sets Bg of size 1..6 (elements 0..|Bg|-1);
    profile spaces Prof of size 1..4 (elements 0..|Prof|-1);
    all |Prof|^|Bg| profile maps P, in lexicographic order via
    itertools.product(range(nprof), repeat=nbg);
    all 2^|Bg| labels l, ordered by the integer whose bit i is l(i).

Case-count derivation:
    sum over b in 1..6, p in 1..4 of p^b * 2^b = 361164.

Deterministic ordering: the nested loops above; no randomness anywhere.

Output schema (single JSON object on stdout):
    {"python_version": str, "cases": int, "mismatches": int,
     "expected_cases": 361164, "result_digest": sha256 hex of
     "cases=<cases>;mismatches=<mismatches>", "pass": bool}

Exit status: 0 iff cases == 361164 and mismatches == 0.
"""

import hashlib
import json
import sys
from itertools import product


def main() -> int:
    cases = 0
    mismatches = 0
    for nbg in range(1, 7):
        for nprof in range(1, 5):
            for P in product(range(nprof), repeat=nbg):
                for lbits in range(1 << nbg):
                    l = [(lbits >> i) & 1 for i in range(nbg)]
                    cases += 1
                    certifiable = any(
                        all(((cbits >> P[b]) & 1) == l[b] for b in range(nbg))
                        for cbits in range(1 << nprof)
                    )
                    fibre_const = all(
                        l[b] == l[b2]
                        for b in range(nbg)
                        for b2 in range(b + 1, nbg)
                        if P[b] == P[b2]
                    )
                    if certifiable != fibre_const:
                        mismatches += 1
    digest = hashlib.sha256(
        f"cases={cases};mismatches={mismatches}".encode("ascii")
    ).hexdigest()
    ok = cases == 361164 and mismatches == 0
    json.dump(
        {
            "python_version": sys.version.split()[0],
            "cases": cases,
            "mismatches": mismatches,
            "expected_cases": 361164,
            "result_digest": digest,
            "pass": ok,
        },
        sys.stdout,
        indent=2,
    )
    print()
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
