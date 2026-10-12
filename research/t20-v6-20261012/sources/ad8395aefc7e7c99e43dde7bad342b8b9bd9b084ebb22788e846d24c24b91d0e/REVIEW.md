# Independent review of the joined whole-state correction

11 October 2026 UTC. Scope: ordinary mathematical review, source comparison, author-check replay, and a separately implemented nonlinear control. No source edits, publication, integration, formal-kernel verification, exhaustive novelty claim, or programme-closure decision.

## Verdict

Accept the revised theorem within its stated finite-labelled, fixed-group, compact-interior, audit-invariant algorithm contract. This is a genuine second-order result for moving conditional weights, positions, and group masses, not an order claim about frozen-loss selection alone. The implicit method is supplied with a local contraction construction and finite-solve obligations, plus finite exact-rational executable instances. It is not represented as an unconditionally successful black-box solver for arbitrary smooth input.

One substantive scope correction was requested and incorporated: stationary-input preservation requires the certified local root or an explicit verified zero-increment rule. The reviewer supplied the counterexample below, so that repaired boundary is collaborative rather than independent discovery by the author. The core descent identity and order proof were not affected.

Exact reviewed bytes and precise predecessor read scopes are in REVIEW_BINDINGS.json. Acceptance attaches to those bytes, not to later versions.

## Mathematical findings

1. **Endpoint-average coupling.** Expanding each group term gives exactly

   m'v'−mv = (m'−m)(v+v')/2 + (m'+m)(v'−v)/2.

   Every internal loss change is nonpositive. For fixed computed averages c, P₂(αh(c−min c)) is strictly increasing in c, so its reciprocal has nonpositive covariance with c under m. Both terms therefore have the claimed sign. The explicit P₂ pairwise dissipation factor and exponential Jeffreys identity have the correct signs and αh factors. These facts do not require preservation of the ordering of endpoint losses.

2. **Actual grouped dynamics.** The logit Fisher inverse is α[diag(1/r̂)+(1/r_k)11ᵀ], and the position mobility is diag(1/r_i). Group masses cancel out of the internal gradient equation. This is exactly the inherited grouped metric; a change of conditional weights is not being suppressed. The author benchmark has qdot=−κ(q)q, rdot=−q, and moving interacting positions. Its separated-variable reference integrals differentiate correctly: H'(q)=q/κ(q), and F'(q)=1−sigmoid(q).

3. **Order.** On the certified branch the discrete gradient differs from the midpoint ordinary gradient by O(|δ|²), giving the internal expansion hf+h²Df f/2+O(h³). Trapezoidal averaging of the changing group loss then has integral error O(h³). The logarithm of reciprocal P₂ changes mass log-odds by the same increment through order two; the common minimum baseline cancels, without needing differentiability at a tie. The normalized map is locally stable. Uniform O(h³) internal endpoint perturbations can be added as defects in the exact-map recurrence, so discontinuous finite stopping counts do not invalidate the argument. The resulting order statement covers all state coordinates and fixed smooth observables.

4. **Contraction constants.** The midpoint remainder satisfies |e|≤M₃|δ|³/24. Differentiation gives ∇e=∇φ(u+δ)−∇φ(u+δ/2)−(1/2)∇²φ(u+δ/2)δ, bounded by M₃|δ|²/8. The derivative of δ/|δ|² has norm 1/|δ|², hence correction derivative bound M₃|δ|/6. Therefore D₀, L_D and Q_h are valid. The closed increment ball is mapped into itself and is a contraction under (14). The radial-quartic numerical certificate uses valid derivative bounds and a nonzero genuinely multidimensional Gonzalez correction.

5. **Finite solves and descent.** The residual bound |δ−δ*|≤|ρ|/(1−Q_h) is valid on that ball. Substituting the residual into the discrete chain rule gives Δφ=−hDφᵀKDφ+Dφ·ρ, establishing the separate relative-descent obligation. Accuracy alone is insufficient near stationary inputs. The rational quartic bisection terminates with the stated bracket error and descent independent of root accuracy. The radial-quartic Picard control checks both obligations using exact fractions. The transcendental grouped benchmark remains a high-precision diagnostic with fixed numerical tolerances, not a validated all-h real-arithmetic algorithm or an asymptotic guarantee below its tolerance floor. The report explicitly distinguishes those levels.

6. **Audit covariance and law preservation.** All internal solver choices, branches, baseline, tolerances and step choices must be independent of audited group masses. Under that contract the two positive diagonal mass changes commute exactly. Reconstruction gives a positive normalized represented law, including after collisions. This proves all polynomial square tests simultaneously; sampled square tests are only controls. The common-carrier qualification now covers the law and Wasserstein claims when abstract position slots have different types or dimensions.

7. **Topology and continuation.** The W₁ transport bound is valid by coupling common label mass and moving unmatched mass over diameter D. Moving distinct Diracs have TV distance 1 even when their coordinates differ by O(h³), and the repeated-step quadratic example also defeats terminal-time TV convergence. Variable mass errors of order h² on separated fixed support give only order h in W₂; the new fixed-support control has the stated leading coefficient. Compact internal sublevels plus uniform local solver bounds justify finite-horizon continuation and the mass lower bound. None of these arguments establishes collision avoidance, rank preservation, unlabelled-law gradient structure, infinite-support recovery, or nonautonomous global continuation.

## Correction found during review

For φ(x)=−x²/2, K=1, initial u=0 and h=2, the discrete-gradient equation is v=v. Every v is a solution. A nonzero endpoint strictly lowers energy from the stationary input. Thus equality implies stationarity for arbitrary exact roots, but the converse requires branch selection. The revised §2 explicitly includes the local-branch or stationary-input zero-step rule, and §3 records this counterexample. This resolves the issue.

## Independent executable evidence

The original 90-check author suite replay passed before the author completed additional controls. That receipt is retained as REPLAY_NORMAL.json but is not used as the final exact-byte execution certificate. The final replay is REPLAY_FINAL.json: all 98 checks passed, and its recorded program digest equals the reviewed digest 424bfa0aa2eefa0cb1f8867cd54315a8fb4f7cb57f6e5aeadf5f1a3f2052d5ff. Report and script hashes were unchanged after execution.

The separate file independent_checks.py imports no author code. It uses the actual two-label mobility and a different nonquadratic chart energy

   φ(q,x₁,x₂)=q²/2+(x₂−x₁)²/2+0.1(q⁴+x₁⁴+x₂⁴),

joined to a singleton quadratic group. Its nonzero Gonzalez correction is evaluated as an exact polynomial formula in the midpoint and increment, avoiding cancellation in the difference quotient. A finite Picard solve is compared with a separately integrated DOP853 ODE reference. From n=32 to 256 the whole-state rates are 2.0001118, 2.0000279, 2.0000070. Group-mass errors also decrease by about four. Replacing endpoint-average loss by final loss produces rates 0.9912176, 0.9956202, 0.9978130. Audit residual is zero in this floating-point fixture; maximum nonlinear residual is below 1.8e−16. These are diagnostics, not exact universal proofs or interval certification.

## Ancestry and limits of inspection

The substantive predecessors verify the claimed gap: grouped classification supplied arbitrary internal descent plus first-order consistency; the reciprocal-Taylor theorem expressly excluded moving-position order; Pro I–L supplied the audit interface but left convergence order open. The present joined theorem fills that narrower interface. It does not own the metric, group classification, positive reweighting/covariance mechanism, reciprocal P₂ approximation, or the Gonzalez discrete gradient.

Primary-paper inspection independently verified Gonzalez formula (3.7) and its second-order ancestry (paper pp. 453–455), and the dissipative Riemannian discrete-gradient identity in the 2018 paper, Proposition 1 and neighboring §3. Those attributions are correct. This review did not conduct an exhaustive literature search or independently certify the complete 44-source substring scan. No unavailable R3 proof or implementation is imported.

Remaining limits are explicit assumptions, not unresolved objections to this statement: supplied derivative bounds/effective evaluations for a general solver; validated arithmetic when exact numerical descent/positivity is required; fixed retained labels and group action; sufficiently small steps for the general local branch; compact finite-horizon control for convergence; no arbitrary cross-group interaction or broad source-warrant theorem.

## Final provenance-only revision qualification

At 2026-10-11T14:08:42.465414+00:00, the report was rebound to SHA-256 b2fa75f865fac44cef1ccee03705002cceca0810bd51b77c35f55bcc64ca0cd1. The opening now limits its gap claim to inspected bodies; a new paragraph records reported but unrecovered R3 overlap and unknown within-T20 priority. Reversing exactly these two edits reproduces the prior reviewed report hash, proving that the mathematics was unchanged. This clarification is accepted. The previous 98-check reviewer receipt is reused after verifying the unchanged program digest; no new execution is claimed. No first-T20 priority conclusion is supported. PROVENANCE_REVISION_REVIEW.json records the check.
