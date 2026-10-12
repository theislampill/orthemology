# Posterior continuation is insufficient for expected inquiry value

10 October 2026 UTC. Additive T20 mathematical interface investigation. This follows the reviewed audit-continuation result but leaves that packet unchanged. Written proof and exact rational controls, not kernel verification or psychological validation.

## The newly exposed interface

The posterior-only continuation contract preserves every answer after every feasible audit. It deliberately discards audit probabilities. Whether this weaker quotient can nevertheless support **optimal inquiry evaluated by expected proper-score improvement** is a further substantive question. The fixed binary-audit result can misleadingly suggest that it can: away from independence its answers reconstruct all audit probabilities. Three audit outcomes already break that inference.

## Exact counterexample, including a reversed inquiry decision

Let the target Θ be binary and D a single fixed three-valued audit. For 0<a<1/2, define the joint law by audit probabilities

    t_a = (a, 1−2a, a)

and conditional target-one probabilities

    q_D = (0, 1/2, 1).

Thus the current target-one probability is 1/2 for every a. Every audit value is possible. Reading the same D twice is idempotent; conflicting readings are impossible. Therefore every a has the same feasible-word language and the same target posterior after **every** future audit word, including the empty word. Adding a do-nothing operation changes nothing.

Use the half-Brier loss L(p,θ)=1/2 Σ_i(p_i−1[i=θ])². Its truthful binary Bayes risk is H(p)=p(1−p). Current risk is 1/4; expected post-audit risk is (1−2a)/4. Expected improvement is a/2.

For a=1/4, improvement is 1/8. For a=1/8, improvement is 1/16. If the audit incurs a fixed cost of 3/32 in the same declared loss units, audit has net value +1/32 in the first model and −1/32 in the second. The optimal audit-versus-skip decision reverses despite exact posterior-only continuation equivalence.

This is a defect only in transporting that equivalence to a stronger policy objective. It does not invalidate the equivalence theorem. It also does not imply that actual epistemic warrant is measured by Brier loss or that the chosen cost has empirical authority.

### Not a zero-cell artefact

Replace the conditional posteriors by (1/4,1/2,3/4), keeping t_a. Every target–audit cell is now positive. Current risk remains 1/4 and improvement is a/8. The same two a values give gains 1/32 and 1/64. Cost 3/128 reverses the optimal choice with net values +1/128 and −1/128.

More generally, take any distinct interior target laws p0,p1 and p*= (p0+p1)/2, using conditional laws (p0,p*,p1) with t_a. For any finite strictly concave proper-score Bayes risk H on these three laws, current law is p* and gain equals

    a [2H(p*) − H(p0) − H(p1)] > 0.

Its magnitude varies with a. This yields the same obstruction without binary targets or quadratic loss, wherever the score's expected risk is finite. Strict propriety and finiteness are substantive score-domain assumptions, not claims about all possible epistemic objectives.

## Why two fixed audit outcomes do not suffice for this obstruction

With at most two possible audit outcomes and a fixed finite Bayes-risk function, posterior-only equivalence preserves the expected information gain. If the two conditional target laws differ, their mixture giving the current target law determines the audit weight uniquely. If they coincide, both equal the current law and gain is zero, regardless of audit frequency. A single feasible outcome also has zero gain. A constant audit cost does not alter this preservation.

Thus three outcomes are minimal for this **one fixed-audit, finite-risk, constant-cost** counterexample. This is not a theorem that every adaptive decision system with binary observations preserves policy values: later fresh experiments, interventions and outcome-dependent costs have additional contracts.

## Exact compatibility criterion for a fixed audit

Let Q be an m×k column-stochastic matrix whose columns are the target posterior laws for k fixed audit values. Consider joint laws parameterised by strictly positive audit weights t, with Qt=q fixed. Since columns sum to one, Qt=q already implies Σt=1 when q is a probability law. Assume this fibre contains a strictly positive t0.

For a declared posterior risk or terminal utility vector h∈R^k, the expected quantity hᵀt is constant on this fibre iff

    h belongs to rowspan(Q).

Proof. If h=bᵀQ, its value is bᵀq. Conversely for every v∈ker Q, t0±εv stay positive for sufficiently small ε. Constancy gives hᵀv=0. In finite real dimension (ker Q)⊥=rowspan(Q). ∎

The positive-fibre assumption supplies all local kernel directions. On a restricted reachable family, the correct criterion instead annihilates the span of differences of admissible weights; imposing the full row-span condition can be too strong. The fixed objects are Q=P(Θ|D) and the projective readout of the already-existing D in the joint-state model. The forward conditional law P(D|Θ) generally varies across these fibres; it is not assumed fixed. This is not a comparison across arbitrary differing target readout matrices.

For a proper-score risk, take h_d=H(Q_d). Current risk H(q) is fixed, so the same criterion governs expected improvement. A fixed cost only subtracts a constant. Outcome-dependent costs require their own expectation vector; they cannot be silently discarded either.

H-Continuation Theorem 2(c) and its proof already preserve bounded adaptive policy branch-weighted values, and its discussion explicitly credits reward-predictive representations. Its contract map already separates answers, risk, incentives and witness predicates. Those general insights are not discoveries here. The general criterion is inherited linear fibre factorization, explicitly already available in H-ICS. Its new use here is to distinguish continuation of conditional answers from continuation of **expected-value inquiry decisions**, with a faithful finite witness and strict-proper-score generalisation. No general field-novelty or new universal linear-algebra mechanism is claimed.

## Research consequence

A proposed noetic state reduction should declare whether it preserves conditional answers, occurrence feasibility, event frequencies, expected epistemic loss, or decision value. The reviewed posterior-only reduction safely answers its own question, but cannot be substituted for the full predictive reduction when the inquiry policy requires the missing expectations. This connects the continuation result to the inherited optimal-inquiry and information-geometry programme without assigning probability or psychological meaning to unrelated theological premises.

For any finite list of expected quantities h_j, retaining their independent linear coordinates in addition to Qt suffices for this one fixed audit. Future interventions require the inherited invariant-observable closure of the expanded readout, rather than assuming a one-step utility fix automatically closes every future decision problem.

## Evidence

`verify.py` constructs the joint laws, compares exact feasible words and posterior answers, checks the two decision reversals, and verifies the kernel/row-span witness using rational arithmetic. Its finite tests corroborate the displayed derivation; they are not a universal theorem proved by enumeration. The separately reviewed audit-continuation packet and H-ICS remain the inherited bases. An independent review is pending when this note is first written.
