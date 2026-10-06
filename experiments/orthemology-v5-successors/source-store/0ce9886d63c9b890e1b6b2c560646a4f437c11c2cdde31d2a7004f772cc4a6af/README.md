# Explicit two-orientation literal counterexamples

This is an additive result. The separately frozen core counterexample is unchanged and remains a separate theorem.

## The upgrade

Two concrete selector records are supplied:

- false-first orientation: cycleTable 44812, targetTable 428783445879334172098560, stageTable 64080
- true-first orientation: cycleTable 24332, the same targetTable and stageTable

Both Config records and their old/computed P02 policy encodings are executable. The theorem explicit_two_literal_counterexamples proves an exhaustive disjunction: at least one of these two exact literal records has the retained finite Certificate and positive-measure failure of the exact mixed runtime target, with every original hypothesis.

This is not an evaluated selection of the opaque retained orientation. The accepted cycleAction uses Fintype.equivFin; the proof does not replace that enumeration or arbitrarily assume false comes first. Instead it proves the two possible Boolean orientations and handles both cases.

The all-action-menu fixture also had genuinely nonunique off-path singleton-support targets. The addendum restricts only singleton-support menus, making those targets unique and binding all certificate cells, including off-path cells. sparse_generated_full proves that this change preserves the complete generated decision on every finite acquired history from full support, for every rejection predicate. literal_computed_decoder_exact then identifies the computed decoder used in the original counterexample. The actual kernel is definitionally equal to the accepted fixture kernel.

## Source and proof boundary

SOURCE_MANIFEST.json binds three additional proof modules, selected readbacks and the pinned parsed-code evaluator. It requires core SOURCE_MANIFEST SHA256 8981fe18fb0d182dfbab01142f250354846dfb691c873d8d1ced71d3f1df3f4c.

The Lean theorem proves positive-measure failure. Native checks only corroborate finite execution and serialized source identity. They do not prove an infinite-horizon probability claim or determine which opaque retained orientation is selected.

The parsed-code check covers all 340 combinations of four old/computed policy encodings and acquired histories of lengths zero through three. A zero-step resource test must raise ResourceLimit rather than return a semantic value. Each policy encoding contains 48,389 bytes. Exact hashes are recorded in the native receipt.

## Replay

Validate the addendum and its separately extracted core packet:

    python3 replay.py --core-packet /path/to/core --verify-only

The default proof replay builds the core from source first, then the three additional modules, selected axiom readbacks, literal numeral and code readbacks, and bounded parsed-code checks:

    python3 replay.py --core-packet /path/to/core \
      --lean-bin /path/to/lean-4.19.0-linux/bin \
      --mathlib /path/to/mathlib4 \
      --mathlib-archive /path/to/pinned-mathlib.tar.gz \
      --out /path/to/new-absent-output

Omit --mathlib-archive for a clean exact pinned Git checkout. --existing-core-output is an explicit optional reuse route: every one of the 167 source-bound core object hashes and its successful receipt are verified. The author used this route with the fresh Eighth core replay, then built all three addendum modules into a new empty object directory. No historical Sixth/Seventh objects receive fresh proof credit.

No Lean compiled objects are distributed. No heartbeat settings are changed. Proof compilation has a 180-second wall-clock bound per module; code emission 120 seconds; numeral readback 30 seconds; parsed execution 90 seconds overall plus its per-case step bound. Failure is fail-closed.

## Retained exploratory limitation

An earlier combined probe containing direct Lean denotation calls was manually interrupted after slow evaluation, with exit 130 and no semantic result. It is resource-inconclusive, not a rejection. Isolated literal/code emission and the pinned parsed evaluator completed successfully. The interrupted probe is preserved separately and does not supply acceptance evidence.

The separately bound independent review passed all 56 new declarations, including 47 theorems, exact inherited-endpoint correspondence and the 340 parsed execution cases. See INDEPENDENT_REVIEW_BINDING.json. The finite checks do not claim direct Lean denotation evaluation, universal Python-to-Lean evaluator refinement, or emission/execution of a full physical runtime wrapper.
