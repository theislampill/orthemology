# Unknown-root attribution: accepted kernel closure, version 1

This package deepens verification of the already accepted Seventh
unknown-one-alias-class theorem. It does not change its scientific result or
interface. The exact reviewed proof bytes are preserved.

Independent acceptance covers:
- the sharp robust root-image iff for arbitrary finite label universes;
- actual-root availability equivalence and maximal-taint realization;
- existence of arbitrary fixed path/quorum families iff
  m ≥ 3(B+c−1)+1, with B≥1, c≥1, c≤m and B<m−c+1;
- exact root-renaming and original Bool/Nat representation correspondence;
- the separately bound untainted-root witness and sharp actual-root cost
  n_min=3B+2c−1, with additional cost 2(c−1).

The families are fixed outside map/fault quantifiers. Actual fault sets lie in
the actual root image. Labels are never counted as independent roots.

Start with:
1. `review/REVIEW.md` and its digest-bound `REVIEW_RECEIPT.json`.
2. `sources/central-v1/SPEC.md` and `THEOREM_MAP.md` for exact statements.
3. `REPRODUCING.md` and the additive public `replay.py` for full verification.

The public entrypoint runs central proofs, all three generic targets,
Regression, the controls supplement, reviewer generic/deletion proofs, all
50 central theorem axiom audits and all three expected-failing source mutants.
It does not silently redefine the frozen helpers, which remain byte-identical.

This package excludes covering/search optimality, randomized caps, physical
cancellation behavior, and external temporal/service/authentication/authorization
applicability. The general uniform q/r formula from the ordinary text is not
separately restated as a named kernel equivalence here. No blanket kernel
closure of every sentence of the accepted ordinary paper is claimed.

All successful theorem dependencies are ordinary Lean logical axioms:
propext, Classical.choice and Quot.sound. No custom axiom, sorry, native_decide
or unsafe proof escape is admitted. Finite examples are regression controls,
not substitutes for all-parameter proofs.

`PUBLIC_MANIFEST.json` binds every public file. `ORIGINAL_TO_PUBLIC.json` records
all exact copies; the two original source manifests and independent acceptance
receipt retain their original hashes. Plans, private coordination, object files,
compiled caches and binaries are excluded. Selected accepted-source documents
are included for context; `accepted-source/PACKET_MANIFEST.json` is the original
historical manifest, not a claim that its entire older packet is duplicated.
