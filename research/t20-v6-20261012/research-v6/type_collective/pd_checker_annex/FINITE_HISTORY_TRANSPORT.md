# Exact finite-history transport of the actual PD checker lift

Status: separately derived ordinary mathematical corollary and freshly compiled formal companion; independent root ordinary/source review accepted. This is a standard induction instantiated at the newly examined original constructor, not an external novelty claim, and is not part of the original packet's formal theorem credit.

## Fully quantified contract

Let S, X, A and O be finite sets, K(s,a) a probability distribution on O × S, L(x,a) a probability distribution on X, e:X→S an erasure and o:X→O an observation. Let μ and ν be initial probability distributions satisfying e_*ν=μ. Assume the exact **joint** row equality

    (o,e)_* L(x,a) = K(e(x),a)     for every x in X and a in A.

For every shared behavioral policy π mapping a finite history h in (A×O)* to a probability distribution on A, define the two history/state distributions recursively. Initially H^S_0 is the law of ([],s) for s~μ, and H^X_0 is the law of ([],x) for x~ν. At a step, sample a~π(h); in S sample (r,s')~K(s,a), and in X sample x'~L(x,a), setting r=o(x'); append the pair (a,r) to h. Then, for every n≥0,

    (h,x) ↦ (h,e(x)) pushes H^X_n exactly to H^S_n.

The policy is genuinely allowed to use the entire recorded action/receipt history and to randomize. Both runs use the same policy kernel. The statement does not silently replace a policy with a state-only, support-only or memory-bounded controller, and does not cover extra policy state absent from the specified interface.

## Proof

For n=0 the asserted pushforward is exactly e_*ν=μ with the common empty history. Suppose the assertion holds at n. For any history h, action a, receipt r and next state s', the lifted mass of the next history h++[(a,r)] and erased state s' is

    Σ_x H^X_n(h,x) π(h)(a) Σ_{x':o(x')=r,e(x')=s'} L(x,a)(x').

By the joint row identity the inner sum is K(e(x),a)(r,s'). Group the finite outer sum by s=e(x). By the induction hypothesis its coefficient is H^S_n(h,s), leaving

    Σ_s H^S_n(h,s) π(h)(a) K(s,a)(r,s'),

which is exactly the source next mass. A nonempty finite history has a unique prefix/last pair, so this verifies every successor coordinate; histories of the wrong length have zero mass in both constructions. This completes the induction. The same calculation is the PMF map/bind naturality proof; it uses joint receipt/state equality, rather than separate marginals.

It follows by further pushforward that both observable history laws agree at every finite horizon. For each history of positive common probability, the conditional law of the erased current state agrees as well, by dividing the joint probabilities by that common probability. This does not make either posterior a point mass and does not discard the conditioning history.

## Literal source instantiation

Use S=PDChecker.State m Q Γ, X=PDChecker.LiftState m Q Γ, A=Γ×Bool, and O=PDChecker.Receipt with finite Q, Γ, positive m and the original supplied Machine Q Γ. Set K=kernel M, L=liftedKernel M, e=erase and o=observe. The original `lifted_joint_row_exact` in CheckerStateObservation (SHA 71bf2c2dc8ab5adabe54a9e0fa2d393408a5f54cc6cd2907f4cefca85d6babb1, lines 113–124) gives the required row identity for **every** old lifted state and action. This proof uses `kernel_support_valid` before reading the copied receipt; no unconditional equality for malformed copied pairs is substituted.

Use μ=initialBelief tape q0 h0 and ν=initialLiftBelief tape q0 h0. The original `initial_lift_erases` (lines 144–148) supplies the initial erasure. `initial_lift_common_label` (lines 150–155) shows the pre-action initial observation is the deterministic ordinary label. Both policy interfaces here begin with empty action/receipt history: if the interface presents that initial label explicitly, prepend the same single fixed ordinary label to both policy arguments. Do not insert a random boot transition or count the label as a simulated action. The original normalized bad-boot counterkernel proves that such a hidden selecting transition can violate PD.

The original accepting and rejecting sinks are visible and absorbing. Consequently the equality includes every bounded-horizon target-reaching event expressible from receipts (and every terminal-state event through erasure). It supplies no formal alternating-machine language equivalence, positive-probability first-false-claim argument, EXPTIME reduction, runtime cost bound, policy extraction implementation or actual source authority.

## Adversarial initial-label control

Let A={false,true}. A receipt-history policy chooses false with probability one when its receipt list is empty, and true with probability one otherwise. Both the empty list and the singleton [ordinary] are legal inputs. If only the lifted interface presents its common pre-action ordinary label, the very first action distribution changes from delta_false to delta_true. This already falsifies action/history parity for that misaligned comparison, independently of subsequent machine transitions. The repaired convention either omits the deterministic pre-action label on both sides or supplies it identically to both. `misaligned_initial_receipt_changes_action` expresses the concrete PMF inequality in the scratch formal companion.

## Fresh formal qualification

`fresh_lean/FiniteHistoryTransport.lean` proves the generic PMF map/bind induction for arbitrary carriers, then instantiates the actual original checker. All four required original production modules were freshly compiled from hash-checked bytes into the isolated directory. The final corollary and initial-label countercontrol pass Lean 4.19.0 `--trust=0`; all five printed targets use only propext, Classical.choice and Quot.sound. The first proof attempt left the definitional `eraseHistory` projection folded and failed a rewrite; its exact source/log/receipt are retained. Expanding that projection resolves elaboration without changing a theorem statement. Official pinned Mathlib objects remain trusted; no custom original object was reused. Conditional-posterior and bounded-event consequences in the ordinary report are not separately formalized declarations.

Independent review: `../../root_math/pd_history_review/REVIEW.md` and `REVIEW.json` accept the complete ordinary proof and formal candidate against the actual original row/initial source ranges. Their separate five-horizon randomized-policy checks and same-marginals/different-joint countercontrol support the exact joint-law condition; the source compiler receipt above provides fresh kernel assurance. No infinite-path theorem is silently added.
