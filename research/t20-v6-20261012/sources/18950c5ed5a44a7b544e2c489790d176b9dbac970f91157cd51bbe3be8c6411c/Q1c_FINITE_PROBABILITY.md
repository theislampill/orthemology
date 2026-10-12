# Q1c — finite probability prerequisites and the two T300 witnesses

Status: PARTIAL formalisation queue obligation. Ordinary all-n proofs and concrete candidate code are supplied. The existing T300 source status and historical payload-hash claims are preserved. No missing historical proof, declaration or mixture weights are asserted to have been recovered.

## 1. Exact target and prerequisites

The queue assigns finite probability/counting first, then two concrete T300 statements. Its named predecessor is AR8R-T300 and its prerequisite is Q0, whose accepted evidence is only its recorded scope. Neither the queue nor that evidence is a fresh build receipt for this run. Optional downstream Q1a use of T300 is a wrapper dependency; pure factorisation work is not made conditional on a P02 PASS.

The exact public theorem file is included and hash-bound. It says that for n≥3 uniform even and odd laws on {0,1}^n agree on every proper-subset marginal but differ on the parity target. It separately says that a finite mixture can move the complete pairwise profile while the parity target remains true. The second target is an existential statement; the file does not specify numerical mixture weights. The following explicit witness is a **new scoped construction**, not historical custody recovery.

## 2. Proposed finite probability interface

For a nonempty finite carrier X, use a mass table w:X→ℚ≥0 or X→ℝ≥0, together with the proof Σ_xw_x=1. Probabilities of events are finite sums. A deterministic map f:X→Y pushes the law forward by summing each finite fibre. A stochastic kernel K(x,y) has nonnegative rows summing to one; the transported law is Σ_xw_x K(x,y). State table identities before interpreting them as probability measures or PMFs.

For the parity examples every probability is dyadic, so exact rational counting suffices. Normalisation and nonnegativity are mandatory, not inferred from an arbitrary list of weights. The finite Python implementation refuses non-Fraction data, negative weights and non-unit totals. The Lean candidate's explicit rational tables carry separate normalisation and nonnegativity targets; a general PMF bridge is still pending.

## 3. P02-QC01 — parity count and identical proper marginals

Let C_n={0,1}^n for n≥1. Define π(x)=Σ_i x_i mod 2 and E_b={x:π(x)=b}. Flipping any one coordinate is an involutive bijection E_0↔E_1, so both sets have 2^(n−1) elements. Let P_b be uniform on E_b.

Fix a proper subset J of coordinates, |J|=k<n, and a pattern u∈{0,1}^J. Choose one omitted coordinate j0. Assign the remaining n−k−1 omitted coordinates arbitrarily; there are 2^(n−k−1) assignments. Exactly one value for coordinate j0 completes the required parity b. Therefore

    P_b(x↾J=u)=2^(n−k−1)/2^(n−1)=2^(-k),

independent of b. The proof includes J=∅ and requires J to be proper. It does not extend to J equal to all coordinates.

Define the declared target Q(P) by P(E_0)=1. Then Q(P_1) is false and Q(P_0) is true. A fixed-coordinate bit flip pushes P_1 exactly to P_0, so this is a specified deterministic intervention, not only a comparison between unrelated distributions. For n≥3, each one- or two-coordinate set is proper; thus every such marginal, and indeed the entire proper-subset profile, is unchanged while Q is restored. Pairwise-profile movement is not necessary for this declared restoration.

## 4. P02-QC02 — a concrete finite mixture moving every pair

For n≥3 put

    P=P_0,        P'=(1/2)P_0+(1/2)δ_(0,...,0).

Both laws are supported on E_0, so Q is true both before and after. For any two distinct coordinates i,j the P-profile is uniform: each pair has probability 1/4. The P'-profile is

    00: 5/8,       01: 1/8,       10: 1/8,       11: 1/8.

Thus every pairwise marginal changes, while there is no false-to-true target restoration. The kernel K(x,·)=(1/2)δ_x+(1/2)δ_0 realises the specified change: toss an independent fair bit, keep x in one branch and overwrite with zero in the other. It is a fully stated finite stochastic intervention.

This is sufficient for the source's target-relative converse. It is not a statement about any learned embedding, arbitrary metric, human interpretation, empirical causal attribution or general restoration diagnostic. The two directions together show non-necessity and non-sufficiency, not probabilistic independence of arbitrary random variables bearing those names.

## 5. Boundary and countermodel checks

For n=2 the pair is the full coordinate set, so the first pairwise-blind statement does not apply. Full parity marginals distinguish P_0 from P_1 for every n. A no-op intervention would not restore Q. A criterion calling any pairwise movement a restoration wrongly accepts QC02. Conversely, a criterion demanding pairwise movement wrongly rejects QC01. These limits are part of the theorem, not caveats to be dropped in a wrapper.

The new exact census checks n=3,...,8, all 498 proper coordinate subsets, 9,324 projected cells, 83 mixture pair profiles and the specified flip transport. These are finite checks of the code and examples, not a proof of all n. The ordinary counting bijection above is the all-n argument.

## 6. Lean candidate scope, not a disguised completion

`P02/T300ThreeBit.lean` is an unexecuted n=3 candidate with seven theorem targets: normalisation, nonnegative weights, all proper marginals equal, changed parity target, declared involutive flip/weight transport, retained mixture target and changed profile for all three pairs. It uses exact finite rational computation and ordinary `decide`, not an assumed probability theorem or native evaluator acceptance.

No Lean executable ran, so no declaration is reported as elaborated, compiled, kernel-checked, or axiom-audited. The all-n finite counting theorem, arbitrary finite PMF pushforward/kernel bridge and T300 wrapper integration remain later work. The handoff must not promote the concrete three-bit module into a proof of the general n≥3 theorem.

The exact source file preimage is in the portable input packet. Its internal historical repaired/pre-repair payload hashes are not its current file SHA-256; `OBLIGATION_RESULTS.json` records the actual file identity separately. Historical absent material remains absent and no additional recovery credit is awarded.
