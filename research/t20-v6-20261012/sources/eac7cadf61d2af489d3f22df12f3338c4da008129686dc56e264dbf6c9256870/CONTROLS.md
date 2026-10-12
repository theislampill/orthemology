# Supplementary semantic controls

These additions do not change any central-v1 `.lean` byte.

## Positive/kernel countermodel controls

`tests/Regression.lean` applies the general results at (B,c,m)=(1,2,7), rejects
(1,2,6), constructs (1,3,10), rejects (1,3,9), explicitly distinguishes seven
labels from six actual roots, collapses two aliases to one root, and exhibits a
one-root bridge between disjoint label sets. Generic examples retain arbitrary
maximal T and arbitrary root-renaming map ρ.

It proves actual countermodels to deleting B≥1, deleting c≥1, and allowing c>m.
The last control shows why an empty family of maps would make a universal safety
predicate vacuous. The central theorem retains valid cardinal parameters.

`tests/FamilyDeletionControls.lean` uses m=3,k=1 to show:
- availability of only the first family plus full cross safety does not imply
  m≥3k+1 (take all pairs for F and only the universe for G);
- availability plus safety only on diagonal P=R does not imply the lower bound
  (all pairs are self-safe, but distinct pairs can have one common label).

These are kernel-checked finite countermodels, supplementary to generic proofs.
They do not replace or limit the all-parameter quantification in central-v1.

## Proof-source mutation controls

Three copies of the root-image proof source are deliberately invalid:
- remove positive fault-budget hypothesis;
- remove positive class-size hypothesis;
- replace actual root images by injectively named interface labels.

The official compiler rejects all three. The first two fail at cardinal
inequalities; the third fails the root-image membership/decomposition proofs.
Their error logs may contain `sorryAx` because Lean reports dependencies of an
unsuccessful declaration after an error. No such file is imported into the
proved packet, and no mutant object file is used. They are expected-failure
controls, never asserted theorems.

## Additional A/C corollaries

`RootCosts.lean` proves that actual-root image cardinality >B is equivalent to an
untainted shared root for every ≤B fault set contained in the actual image. This
is only a root-level witness: a physical veto still needs the accepted v2 gate
contract. It also proves the arbitrary-family actual-root lower bound
3B+2c−1, attains it generically at m=3(B+c−1)+1, and derives the exact additional
2(c−1) actual-root cost relative to the known-attribution 3B+1 count.

## Reproduction

Run `verify.sh` for isolated central compilation, `test-controls.sh` for positive
controls and expected-failing mutants, and `audit_sources.py` from the original
workspace root to verify all accepted manifest entries, unchanged legacy bytes,
unchanged frozen central sources, and official compiler identity. The pinned
Mathlib tree and its dependencies are read-only; no dependency was edited.
