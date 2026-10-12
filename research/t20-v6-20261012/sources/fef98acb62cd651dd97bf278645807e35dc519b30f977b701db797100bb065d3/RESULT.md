# Review of D5 and D6 and a timed kernel repair

11 October 2026 UTC. A separate mathematical review of the supplied synthesis. The original packet is unchanged. This report distinguishes a sound theorem, an underspecified hypothesis, and a narrow local extension. It makes no formal-verification, field-priority, universal hybrid-model, or T20 closure claim.

## Main conclusion

D5 is correct under its stated smoothness, positive-definiteness and full-row-rank assumptions. Its value is a clear operation-relative quotient-cometric criterion and its connection to a retained context. Its core mathematics substantially overlaps the earlier quotient-gradient construction and the currently available full-law coarse-graining report.

D6 is correct under the strongest natural deterministic reading: retained guards come with the same urgent first-hitting rule, entry convention and simultaneous-event resolution, and stochasticity occurs only in the matched post-event kernels. The proof's sentence “Guard values agree throughout, so their specified event times agree” uses this extra timing semantics. The six displayed hypotheses do not state it.

If “event/permission guards” merely determine which jumps are eligible, the displayed conditions alone do not preserve event-time laws. Hidden holding times or rates provide an immediate one-jump countercontrol. This is a scope defect under the broader stochastic/permission-enabled reading, and a specification clarification under the deterministic first-hitting reading. It should not be reported as a refutation of the latter.

A narrow repair is to preserve the complete next-event mechanism. Its most robust expression is equality of the **joint holding-time, event/outcome, next-retained-state kernel**, including the no-event branch. With finite holding-time alphabets, D1–D3 already provide the requisite refinement and sidecar results after time is added to the outcome label. The useful local addition is identifying what the hybrid interface must include and exposing the timing/branch-correlation control.

## Sources and attribution boundary

The following three local sources were inspected, copied without alteration into `inputs/`, and bound by SHA-256 in `INPUT_BINDINGS.json`.

1. `received-cross-front-synthesis-20261011/Orthemology_T20_Whole_Corpus_Synthesis_20261010/documents/CROSS_FRONT_SYNTHESIS.md`. The D1 contract is at lines 26–52; D1–D3 at 62–191; D5 at 274–326; D6 at 330–359. Lines 456–460 explicitly say the supplied tests do not prove the analytic statements D4–D6. That evidence boundary is sound.
2. `noetic-gradient-transport-20261009/RESULT.md`. Lines 78–157 give the all-objectives versus fixed-objective distinction, common-time flow qualification and prescribed canonical cometric comparison. Lines 237–310 give the induced quotient cometric, least-energy lift, local quotient metric and positivity/existence boundary.
3. `full-law-coarse-graining-20261011/RESULT.md`. Lines 67–112 give a law-level pulled-back-gradient criterion and, at line 110, fibre constancy of the induced mobility as the criterion for field closure for all initial laws and test objectives. Lines 128–138 give flow commutation under separately stipulated uniqueness. This is a currently available companion, dated after the supplied synthesis; no claim is made that the synthesis originally inherited from it.

This is a bounded comparison with these passages, not an exhaustive novelty search. All new deductions below are proved in this report; no external authority is needed for their validity.

## D5 is sound with a precise scope

Let Z=L(U). Since L has full row rank and U is open, Z is open. Write A(x)=L G(x)^(-1) L^T. For any x0 in U, a linear right inverse R of L gives a local section s(z)=x0+R(z−Lx0) taking a neighborhood of Lx0 into U. If A is constant on whole fibres, Abar(z)=A(s(z)) is independent of that section and smooth. These local definitions agree on overlaps. For nonzero v, L^T v is nonzero, so v^T A(x)v>0. Thus Abar^(-1) is a genuine smooth positive-definite metric on Z.

For every smooth coarse j, the projected field is −A(x)∇j(Lx). Fibre constancy makes it the coarse negative metric gradient. Conversely the coordinate objectives j(z)=z_i identify every column of A, proving necessity. There is no connected-fibre assumption missing: constancy on each full fibre, as actually stated, is sufficient even when a fibre has disconnected components.

The theorem gives projectability of fields and hence equality of projected flows on their common existence interval. It does not by itself give global fine lifts or prevent exit from U. It also constructs an induced coarse metric. If the application instead insists on an independently prescribed coarse metric Gcan, the additional requirement is A(x)=Gcan(Lx)^(-1), rather than mere fibre constancy. The supplied theorem does not claim otherwise.

The all-objectives quantifier is essential. For example, L selects the first two coordinates of (z1,z2,h), and take the fine cometric diag(1,1+h²,1). Then A=diag(1,1+h²). The projected gradient of j=z1 is always (−1,0), although A is not fibre-constant. The objective j=z2 detects the hidden h. This agrees with the source's lines 314–318.

The inherited fixed-reference simplex theorem already owns the induced quotient-cometric construction and the separation between induced and prescribed canonical geometry. D5 packages the smooth state-dependent fibre condition in a general finite-dimensional setting. The law-level companion proves an analogous condition using conditional mobility, in a different state space and tangent geometry. These are mathematically related rather than identical theorem statements. D5 is a useful bridge; it should not receive credit for newly discovering quotient gradient geometry.

## Where D6 needs timing semantics

The original hypothesis 2 says that “event/permission guards are functions of the retained state.” The conclusion includes event times. A Boolean permission, an enabled-action set, a first-entry surface and a stochastic event clock are distinct data. Equal permission values alone do not specify when permission is exercised.

### The charitable deterministic reading

Suppose each guard is a specified retained set G_e, events fire urgently at the first entrance into those sets after mode entry, and fine and coarse models use the same conventions for a guard already true on entry, tangencies and simultaneous events. For example, the next time can be defined by

    τ = inf { t ≥ 0 : z(t) belongs to at least one G_e },

with a fixed shared selection rule for the event type attaining that time. Non-explosion is still needed if zero-duration transitions can repeat. The convention τ=∞ when the set is empty covers no event.

By projected-flow uniqueness, the retained fine path and coarse path are the same up to the next event. Therefore the set of candidate times, its infimum and the shared event selection agree. The source's matched jump-kernel condition then propagates agreement to the next segment. Induction gives D6. This supplies the missing justification for the quoted proof sentence. In this interpretation the issue is making implicit model data explicit, not changing the intended result.

### A stochastic one-jump countercontrol

There are two modes, active and done. In active mode let the fine state be (z,h) in R×(0,∞), let r(z,h)=z, and let all fine and coarse vector fields be zero. The active guard is always enabled. There is a single action, so the policy contains no hidden information. At its jump the observed outcome is always `finish` and the next retained state is the absorbing done mode with z=0. The fine and coarse post-jump kernels are identical after pushforward. Running cost is 1 in active and 0 in done; jump cost is 0; labels identify the current retained mode. There is at most one jump.

Now let the waiting time in the fine model have exponential rate h. The two fine starts (0,1) and (0,2) have the same retained initial state and all the displayed flow, guard, post-jump, cost, label, non-explosion and policy data agree. Nevertheless

    P(T > t | h) = exp(−h t).

At the common physical horizon t=log 2, survival is 1/2 from h=1 and 1/4 from h=2. A reduced model with rate 1 cannot represent both. Even expected accumulated running cost differs: it is (1−2^(−h))/h, hence 1/2 versus 3/8. Retaining the cost function alone does not retain its time integral when occupancy durations differ.

This is a genuine Markov example with smooth zero flow and one stochastic jump; it does not require a missing age coordinate. It falls within a broad permission-enabled stochastic hybrid interpretation. It falls outside an urgent first-hitting interpretation: an always-true urgent guard would trigger at time zero, not at a positive exponential time. The report therefore does not use this example to defeat that stronger interpretation.

For exact finite controls one can instead take deterministic holding times 1 and 2 with the same outcome and absorbing reset. Their deadline success probabilities at 3/2 are 1 and 0. This is a semi-Markov entry-state example. If it is represented as a Markov hybrid flow by adding a residual timer, that timer's decrement and firing rule are additional fine-state data whose retained projection must be checked.

### Why matching a separate timing marginal is insufficient

Use two active information states s+ and s− with a common retained image, one absorbing destination d, and the following joint distributions:

    s+ : (τ=1, o=0, next=d) with mass 1/2;
         (τ=2, o=1, next=d) with mass 1/2.

    s− : (τ=1, o=1, next=d) with mass 1/2;
         (τ=2, o=0, next=d) with mass 1/2.

The holding-time distributions agree. The untimed joint outcome/next-state distributions agree. But P(τ≤1 and o=0) is 1/2 from s+ and 0 from s−. Thus retained timing and retained branches must be matched jointly, or a generative model must explicitly ensure the equivalent conditional matching. This is the timing counterpart of the source's original insistence on joint outcome/next-block preservation at lines 36–52.

The example uses a timing-dependent outcome kernel. It is not a counterexample to a stronger model that already specifies matching post-jump kernels conditional on the realized time and retained pre-jump state. Under that stronger model, the displayed joint mismatch is already ruled out. It diagnoses what is lost by checking two marginals only.

## A repaired D6 hypothesis and proof

Retain original D6 hypotheses 1 and 4–6, require matching initial retained laws, and replace hypotheses 2–3 by the following complete event contract.

**Timed event contract.** Conditional on any matched retained timed history and a common retained-history control rule, the joint law of the next elapsed time, event type, observed outcome and next retained post-jump state is independent of the fine representative and agrees with the reduced law. Include the possibility of no further event. All guard entry conventions, urgency, timers and resets, competing hazards and simultaneous-event resolution used to generate this law are part of the specified model. Running costs factor through the retained path; jump costs and required labels factor through the corresponding retained event data.

“Retained timed history” includes event timestamps and the retained path observed so far, not just the sequence of untimed modes. If the state representation deliberately excludes clocks, the conditional contract must still hold given the information actually retained. A history-dependent reduced mechanism is allowed by this formulation; a state-Markov quotient requires the stronger factorization through its current retained state and specified controls.

This joint formulation is sufficient and does not demand an unnecessary separate hazard representation. For a model constructed from first-hitting guards and independent hazard clocks, one convenient stronger implementation condition is that the deterministic trigger conventions, hazard intensities and event-selection probabilities are retained, and that post-event kernels have the stated representative-independent pushforward conditional on the realized event and time. Arbitrary hidden timing/output correlation must not be silently excluded without specifying that generative structure.

**Proof.** Starting from a matched retained state, hypothesis 1 and uniqueness identify the retained deterministic trajectory until the next event. The timed event contract gives the same conditional law for its duration and the complete retained event record, including the no-event branch. Conditional on a finite matched event history, the same argument applies to the next segment and record. Integrating the same conditional kernel against the same prefix law gives equality for the next prefix. Induction proves equality of all finite timed event-prefix laws under the common retained policy.

Each finite retained path is reconstructed from its initial state, these event records and the retained flows. Hence every finite-jump truncation has the same retained path law. On a bounded declared horizon, non-explosion implies that the number of jumps is finite almost surely. Restricting to paths with at most n jumps and letting n increase therefore gives equality of the full retained path law. Running-cost integrals, retained jump-cost sums and terminal labels are measurable functions of that path and its retained event data, so their joint laws agree whenever those functionals are defined. For expectations, impose the needed integrability or allow well-defined nonnegative extended values. No independent global existence theorem is imported. QED.

This is a local next-event preservation theorem, not a premise that the entire trajectory law already agrees.

## The finite timed extension of D1 to D3

Here is the smallest executable extension needed for finite waiting-time contracts. Let S, required labels, actions, costs and the fixed summary r be as in D1. At decision epochs choose an action a, held until the next event. Add a finite holding-time alphabet D and a rational probability kernel

    H_a(s, τ, o, t),     τ in D, o in O, t in S.

Use absorbing terminal states to represent termination; a no-further-event symbol can also be included if desired. For accumulating costs over physical time, include retained running rates in the initial record, or stipulate a deterministic retained flow and retained running-cost function between epochs. The controls use positive finite times and absorbing termination, so non-explosion is automatic.

A partition is timing-preserving when the initial retained labels, action menus and costs agree, and, for every action, holding time, outcome and partition block C,

    Σ[t in C] H_a(s, τ, o, t) = Σ[t in C] H_a(s′, τ, o, t)

whenever s and s′ lie in the same block. This is exactly the original D1 condition with enlarged outcome alphabet D×O. Its refinement algorithm, termination bound and coarseness proof therefore transfer without change.

For completeness, start from the initial record partition and repeatedly split by the displayed vector. Every strict split increases the block count. Any admissible competing partition refines the initial partition. If it refines the current one, each current block is a union of its blocks, so its equality of joint masses implies equality into each current block. It consequently refines the next split. Induction proves that it refines the final fixed point, which is itself timing-preserving. Thus the final partition is coarsest.

If N_z^time counts the final timed blocks in r^(-1)(z), the minimum deterministic common sidecar alphabet is max_z N_z^time and the fixed-length bit count is ceil(log2 max_z N_z^time). Every admissible representation must distinguish those blocks within a fibre; enumerating them separately inside each fibre attains the bound. This is D2's original proof, not a new coding theorem.

The original D3 induction now preserves timed event histories. Non-explosion and retained interpolation then preserve physical-time trajectories, deadline events and the corresponding running and jump costs. One must not identify the original h-step Bellman horizon with a physical-time deadline without this added timing model.

The timed partition refines the untimed one because summing the timed equalities over τ gives the original joint branch equality. Thus adding timing cannot reduce the sidecar requirement. In the deterministic two-wait example, the untimed active states need zero sidecar bits but the timed contract needs one. The timing/outcome-correlation example also changes the minimum from zero to one bit, despite equal separate marginals.

For general Borel holding times, the condition is equality of the finite measures

    Σ[t in C] H_a(s, B, o, t)

for every measurable B⊆[0,∞] and every o,C. The same finite-state partition and minimality arguments remain mathematical statements because they compare equal measures. **Computability does not follow for arbitrary measure descriptions.** An effective equality procedure is additional input. The executable controls claim only finite rational timing alphabets.

## Exact controls and what they establish

`checks.py` uses standard-library rational arithmetic and explicit exceptions, so checks remain active under Python optimization. It does not import or modify the supplied implementation. Its eight control groups verify:

1. The three inspected source snapshots, and optionally their original counterparts, match their recorded SHA-256 hashes.
2. D5 permits variation in a hidden metric direction when the retained cometric is unchanged.
3. The two-leaf velocity/event-time control and the fixed-objective versus all-objective distinction have the stated exact values.
4. Hidden deterministic holding times merge under the untimed contract, split under the timed contract, and change the minimum sidecar from zero to one bit.
5. Rates 1 and 2 give the exact unequal exponential survival values at log 2, using exp(−h log 2)=2^(−h); this is an algebraic evaluation of the stated law, not a simulation or a probabilistic theorem proof.
6. Equal separate time and untimed-branch marginals conceal the displayed timing/outcome correlation.
7. Future timing distinctions propagate back through two refinement rounds in a five-state model. All 52 partitions of that model are enumerated to verify the coarsest stable result independently of the refinement iteration.
8. A positive timed quotient merges genuinely equivalent hidden states and gives the same physical-deadline running-plus-jump cost, 13/3 in the declared example.

Both normal and optimized runs returned PASS with original source hashes checked. Receipts are `CHECKS.json` and `CHECKS_OPTIMISED.json`. Reproduce from the parent workspace with:

    python3 synthesis-hybrid-timing-review-20261011/checks.py --original-root .
    python3 -O synthesis-hybrid-timing-review-20261011/checks.py --original-root .

These controls corroborate examples and the finite timed construction. The general D5 result, the repaired hybrid theorem and the general finite-state refinement argument rest on the ordinary proofs given above. The original packet's independent integrity and 26-test replays were supplied by the parent and were not duplicated here.

## What to carry forward

Keep D5, with credit to the inherited quotient-gradient line and its state-dependent formulation. Keep D6 as a conditional interface, but explicitly fix its event semantics. If the intended scope is urgent deterministic guards, a short hypothesis clarification is sufficient. If stochastic waiting, delayed exercise of permissions or clock-driven actions are in scope, use the complete joint timed event contract.

The bounded additive result is that **timing itself can be an operation-relative retained distinction, and timing/branch correlation can require an extra sidecar even when both marginals are preserved**. The one-bit controls make that requirement concrete. The finite algorithm is an application of the synthesis's own D1–D3, not a new research programme or a claim that arbitrary hybrid abstractions are now solved.
