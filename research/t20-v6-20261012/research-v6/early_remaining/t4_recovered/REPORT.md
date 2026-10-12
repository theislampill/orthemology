# T4 endpoint: recovered original source and bounded fresh replay

## Result and chronology

The recovery annex now holds the exact original return `d0d3dffa3947bd06b101f267ef9cabeb559bd4e2d2ad4c3df7f80038307efd91` (1,873,244 bytes). This supersedes the former *availability gap for the executable endpoint source*. It does not retroactively expand the frozen v5 census or erase the earlier honest access limitation. `ANNEX_INVENTORY.json` binds every archive member; extraction was into this new v6 branch. The separate recovered-solvers ZIP is not this archive.

The recovered native identity `a77d05474ebd510b30cf52b34828a407dadce962359c678701eba6a9ebda7c7b` contains literal cache bytes and both numeric indices. Actual decoding confirms a 59-byte arity-one cache program and a 105-byte arity-two prefix program. Source trees, codec, both complete checkers, ordinary proof and independent review have now been read. Both original checkers were freshly executed in copied directories: both exit 0, each covers 2,047 words and 18,434 ticks; the independent interpreter additionally covers 578 natural cache frames. `FRESH_TESTS.json` records exact code/log hashes. Reproduced receipts are byte-identical to their archived counterparts. These are bounded Python execution results, not Lean replay.

## Exact semantics and ordinary proof

The initialized cache is `(L,R)=(1,1)`. Each input is an acquired binary bit `b`; the decoded assignments update

`L := L * (b*0 + (1-b)*2)`, `R := R * (b*1 + (1-b)*1)`, then `out := 1[L+1 ≤ R]`.

Subtraction is truncated natural subtraction. Induction on the number `m` of receipts gives `R=1`, with `L=2^m` if all receipts are zero, and `L=0` otherwise. Consequently the output is exactly the seen-one predicate. The prefix program initializes the same products and strips exactly `m=k+1` low bits from a sentinel word encoding those `m` receipts. Its loop excludes the sentinel; the product factors commute, so reversed traversal gives the same seen-one result. This is an ordinary proof over the inspected source trees for every finite valid prefix, rather than an extrapolation of the finite enumeration.

The full policy prepends one false action. Action `n` therefore uses the first `n` receipts, while eager tick `k` supplies action `k+1`. Equality at each finite prefix implies pointwise equality of the infinite output maps. Each output coordinate depends measurably on a finite input prefix, so the maps have equal pushforwards under every supplied input measure.

The adapter is essential. The cache program's arity is one and its returned registers are carried by `run_frame`/`tick`. The old indexed arity-two evaluator defaults to zero on that arity-one code. The prefix code is not a stateful-cache API either. Calling the same numeric code through an incompatible API does not preserve this behavior.

## Literal repair, cost, and output defect

The source-to-score contract is inherited exactly from the already fully read T3 `BernoulliPrefixLaw` and `AuditContractBinding` sources. Here source/scoring weight is either `0` or `1/2`, receipts are iid Bernoulli with that weight, disturbance is `1/4`, and false/true read out the coherent reports `1/2`/`5/8`.

The two all-truth excess losses are respectively `(0,0)` and `(9/64,-7/64)` at weight zero, and `(-5/32,3/32)` and `(-1/64,-1/64)` at weight one half. Thus false is good only in the zero model and true is good only in the half model, within this two-report alphabet. This counts failure of the expected all-truth scoring inequalities, not the outcome of each individual selector draw.

At weight zero there are almost surely no ones and no failed reports. At weight one half, action `n` is bad exactly when its `n` receipts are all zero, with probability `2^-n`. Tonelli and the geometric sum give expected total bad count `2`, including action zero. The finite test's sum through action ten is `2047/1024`. Omitting the initial action would give total `1`, a different convention.

Every output stream is all false forever or a finite run of false followed by true forever. This is a countable image, so its measurable pushforward has zero nonatomic mass under every source law. Countable support and literal repair are separate conclusions. This special two-state quotient does not assert a finite quotient for arbitrary likelihood programs.

## Computation scope and controls

The cache executes two sequence tasks and three assignments, exactly five statement tasks. For `m≥1` the prefix tree executes nine outer tasks, `m+1` repeat tasks and five body tasks per iteration, exactly `6m+10`. Both checkers corroborate the count; the author checker rejects one-less fuel. This meter excludes expression traversal, arithmetic bit cost, input injection, setup, codecs, report readout and elapsed time. The register count is fixed but `L=2^m` grows along all-zero input.

The retained Python codec has an explicit resource-exhaustion exception and does not turn exhausted execution into semantic zero. Its serializer/parser are recursive host implementations and can exhaust host stack. The natural-fuel, natural-register and initialized-frame restrictions matter: the generic helper is not validated on arbitrary Python objects.

The source-bound controls cover cold cache, stale cache, pre-update output, wrong bit, insufficient fuel, API misuse in both directions, an extra sentinel-consuming iteration, omitted initial action, every proper truncation of the 59-byte code and wrong magic. The independent parser and recursive interpreter do not merely call the author's cache adapter.

## Recovered reduction theorem and remaining formal gap

`RepairTestingReduction.lean` (`c86a552e…`, all 113 lines) was also read completely. For `0≤l≤u≤1` and `0≤e≤1/4`, it identifies existence of one coherent report weakly good at both endpoint weights with `robustValue(l,u,e)≤0`. Positive minimax value implies disjoint good-report sets. Its generic report-risk lower bound applies to any report alphabet, provided good-report sets are disjoint and the two finite-word masses are nonnegative; it does not assume a preselected binary report alphabet. It also gives sound own-model reports and an explicit selected common report. The nearby weights `49/100,51/100` at disturbance `1/4` admit a common report, while `1/4,3/4` have positive value. Thus distinct models alone are insufficient for this testing lower bound.

The exact 180-line `RobustBinaryRepair` dependency is recovered and fully read; it imports only Mathlib and proves the endpoint minimax theorem, unique coherent crossing and width certificates. The other direct import, `FiniteLikelihoodRisk.lean`, is absent from this recovered archive and current catalogue. Its `Words`, `mass`, `pairError_eq_min` and summation lemmas cannot receive source-body or fresh kernel credit from the recovered reduction's uses alone. No attempt to compile a fabricated replacement was made.

The historical `EndpointFiniteObserver`, `EndpointActualLaw` and `EndpointLiteralCost` closures and old endpoint-observer archive `e4676218892d81927ea3fdb414d7e5e9093e826dbcd6b2566c9d6d2ce4b18165` remain explicit recovery targets. The original report already labels their proofs unavailable. Its historical JSON's reference to earlier Lean proofs is provenance, not a current seal. These gaps do not block the independently reviewed ordinary source argument and finite execution reproduced here.

## Cross-family consequences

The same exact `prcodec.py` includes `Builder.inline` and `compile_shift`, read in full here. Its sorted source-register renaming, reset-on-every-call rule, fresh range starting at register 12, first-cut scan, copied stopping bit and re-sentinelled tail agree with the separate literal-shift Lean syntax examined in `unjoined_controls`. This source comparison closes the handwritten-AST interpretation at the inspected Python version; it is not a kernel proof of all Python runtime behavior.

For T20 synthesis, this is a concrete example of observable law preservation requiring an explicit state/input/clock adapter; of constant abstract statement count coexisting with growing integer storage; and of zero output-law defect coexisting with a positive expected literal bad-count budget. None supplies normative source authority or truth identification beyond the given source/scoring contract.
