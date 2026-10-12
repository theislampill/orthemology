# Independent signed-energy continuation review v2, superseding v1

10 October 2026 UTC. Independent ordinary mathematical review; no formal proof, field-priority judgment, protected changes, or T20 closure. Verdict: PASS for the replacement frozen report identified below. No substantive mathematical defect or required correction was found. The prior PASS remains valid for its historical bytes, preserved in signed-energy-independent-review-20261010; this revision reviews the additional null-ideal equivalence and fixed-Gram-rank claim. The participating route checker is not credited as independent review and was not used as proof evidence.

## Exact artifact binding and replay

- Author RESULT.md: SHA-256 2ac90188cc0cb17d3bb80f3ba63d9dfe62742db5919cf86d7001c7e0baf39e55, 31,800 bytes.
- Author FREEZE.json: SHA-256 5bb1f4c25a8e54ba307190814f7fd1d99a68515fb9692a3184e72729d4eb418a.
- Author check_controls.py: SHA-256 2dc4ca568dcff15e1c4d8b5c9817eea049e72e47bfe91c1a7afebb16da69463b.
- Author exact controls replay: PASS, 501 checks; resulting CONTROL_RESULTS.json is byte-identical to the frozen author's result.
- Separately authored controls: PASS, 111 checks.
- All author freeze inventory entries and the retained ancestry inputs were hash-verified. Original files were unchanged across replay. Frozen copies and separately writable replay copies are retained within this review directory.
- ARTIFACT_BINDINGS.json identifies every frozen source and ancestry file. REPLAY_RECEIPT.json binds the executable result. AUTHOR_REPLAY.log contains its output.

This review was independently reconstructed from the mathematical statement and proof, with separate controls and an unmodified author-suite replay. It does not treat the participating signed-energy-proof-check-20261010 route check as independent final review. The author received scope confirmations and the independently checked null-ideal strengthening during review; no reviewer edits were made to author files.

The replacement RESULT.md was compared directly against the v1 frozen copy. Its only substantive mathematical change is the reviewed null-ideal equivalence and fixed finite Gram-kernel/rank corollary; the controls summary is updated accordingly. The rest of the universal argument remains unchanged. Previous review history is preserved, not overwritten.

## Findings

The bounded-energy theorem's argument is sound. The same argument proves the stronger supplied-horizon theorem whenever every finite scalar measure h_*(q² μ) is Hamburger determinate. A single two-sided exponential energy moment is sufficient for this hypothesis; unlike bounded energy it does not give global forward existence.

## Proof reconstructed independently

1. Set a(t)=exp(−∫₀ᵗ L_s(h)ds), A_t=a(t)L_t. The signs give A′_t(p)=−A_t(hp). Iterating this identity across polynomial coordinates is legitimate under coordinatewise C1 and yields interior C∞. Positivity remains since a>0.
2. For fixed q set f=A_t(q²). Its even derivatives equal A_t((qhⁿ)²)≥0. Taylor expansions forward and backward through odd degree have nonnegative even-order remainders. Adding gives m₂ₙ r²ⁿ/(2n)!≤[f(t−r)+f(t+r)]/2. Compact interior intervals supply the uniform constants needed for actual analyticity. Cauchy–Schwarz bounds odd derivatives; (2n)!(2n+2)!/((2n+1)!)²=(2n+2)/(2n+1)≤2.
3. The scalar functional r↦A_t(q²r(h)) is square-positive. One-dimensional Hamburger existence supplies a finite positive representing measure; no multivariate moment-existence claim is made. Even factorial bounds imply ∫e^{b|z|}dσ_t<∞ for b<r. They imply determinacy, either by Carleman or analytic transforms.
4. Taylor's theorem and that exponential margin give f(v)=∫e^{−(v−u)z}dσ_u locally. Differentiating under the integral identifies every moment at v, and determinacy identifies σ_v. A uniform local radius on enlarged compact interior intervals permits a finite chain between arbitrary positive u,v. No globally uniform exponential radius is needed.
5. Fix s>0 and set τ=e^{sz}σ_s. For u↓0, σ_u=e^{(s−u)z}σ_s. On z≥0 apply monotone convergence separately to each even moment. On z<0 use domination by |z|^{2n}, because 0≤s−u≤s. Coordinate continuity at zero identifies the sum. Crucially, n=0 recovers total mass. The resulting even τ-moments then dominate odd moments on the positive half-line; σ_s dominates the negative half-line. Thus τ and h_*(q²μ) share all moments, with no loss of mass or cancellation assumption.
6. Determinacy at zero identifies these measures. Hence A_t(q²)=∫q²e^{−th}dμ and the integral is finite on the whole supplied horizon. Null q is handled by zero mass, without normalizing. The identity p=((p+1)²−(p−1)²)/4 gives every polynomial coordinate and its absolute integrability. The q=1 instance gives a=Z>0.
7. Bounded initial |h| implies compact scalar support for every q-weighted measure, hence determinacy. Even moments first force any competitor onto the same bounded interval; polynomial approximation then identifies it. Bounded energy also directly gives global existence, domination of derivatives, and e^{−Mt}≤Z≤e^{Mt}.
8. If ∫e^{ε|h|}dμ<∞, Cauchy–Schwarz gives ∫q²e^{ε|h|/2}dμ≤(∫q⁴dμ)^{1/2}(∫e^{ε|h|}dμ)^{1/2}. Thus every weighted scalar measure has an exponential moment and is determinate. A smaller time interval allows derivatives of polynomial observables by the same inequality. This is local existence and supplied-horizon uniqueness, not global existence.
9. Compact joint initial support stays compact under the tilt. Any joint competitor with the same moments is confined to a common bounding box by coordinate even moments, then identified by polynomial density. Bounded scalar energy alone cannot identify hidden directions: the signed two-point coordinate times a lognormal Stieltjes-class coordinate is a valid counterexample.
10. Local finiteness of switches permits finite induction on each compact horizon. At switches continuity identifies the new initial moment record with the previous compactly supported tilted law. Fixed-polynomial results apply again, yielding multiplication of densities. Neither global C1 across jumps nor arbitrary continuously varying energies is required or proved.

## Exact-horizon converse and null-ideal corollary

The final expanded converse is valid: if every ∫q²e^{−th}dμ is finite on [0,H), then |p||h|ⁿe^{−vh} is dominated on each small time interval by the sum of its two endpoint-weighted values. Those absolute polynomial factors are bounded by sums of polynomial squares. This also works one-sided at zero using endpoints 0 and δ. Consequently the path is coordinatewise C∞, including one-sided boundary derivatives. The stated supremal open forward horizon follows, without assuming endpoint inclusion.

The added null-ideal persistence statement is valid in its stronger stated scope, without an initial joint law or initial determinacy. The n=0 boundary identity forces τ_q=0 whenever L₀(q²)=0. The positive density linking τ_q to σ_s forces σ_s=0 at every positive time. Cauchy–Schwarz gives L_t(qr)=0 for arbitrary r. The initial null space is indeed an ideal: its linearity follows from Cauchy–Schwarz, and L₀(q·qr²)=L₀((qr)²)=0 establishes multiplicative closure. This preserves polynomial equations only; it creates neither a joint measure nor general support inequalities.

## Narrow v2 amendment: exact null-ideal and fixed-Gram invariance

The reverse implication is valid without an initial joint law or initial determinacy. If L_t(q²)=0 at one positive time t, the corresponding finite positive scalar σ_t has zero mass and hence is zero. For every positive u, σ_u=e^{−(u−t)z}σ_t=0; the density is strictly positive and the transition is invertible. Thus L_u(q²)=0 for all positive u, and continuity gives L₀(q²)=0. Together with the previously reviewed forward implication, I_t=I₀ throughout the supplied horizon.

For any fixed finite list p₁,…,p_k, the matrix G_t=(L_t(p_i p_j)) is positive semidefinite. A coefficient vector c belongs to ker G_t exactly when cᵀG_tc=L_t((Σ_i c_i p_i)²)=0. That square-null condition is invariant, including at zero. Hence the actual subspace ker G_t in R^k is constant, and rank is constant by rank-nullity. This is stronger than equal nullity alone and does not require the p_i to be linearly independent. It does not assert fixed numerical matrix entries, uniform spectral bounds, or joint representability.

Eight extra independently authored exact controls check a redundant-feature Gram matrix with arbitrary positive diagonal weights and several exact substitutions. As with all finite controls, the universal conclusion rests on the argument above.

## Independent discriminating controls

The separately authored independent_controls.py checks 111 exact identities/inequalities. They include direct t-parameterized signed atomic hierarchy identities, normalized weights at log 2, factorial interpolation constants, nonlinear signed energy values, null support polynomial, polarization, reverse switching, Gaussian negative-quadratic moments, Gaussian signed-linear moments, the flat negative-square value, geometric energy mean, and lognormal sine cancellation.

For μ=N(0,1), h=−x², a small positive exponential energy moment exists, Z=(1−2t)^{−1/2}, and L_t(x²)=(1−2t)^{−1}. Every supplied full-positive path must agree for t<1/2. If its horizon included t=1/2, continuity would contradict divergence. This validates the distinction between determinacy and global existence.

Finite tests do not establish the universal theorem; the reconstruction above supplies the mathematical review.

## Classical source checked

Konrad Schmüdgen, Ten Lectures on the Moment Problem, https://arxiv.org/pdf/2008.12698, Theorem 1.12 and Corollaries 2.3–2.4, were checked directly. They support scalar Hamburger existence and factorial/exponential determinacy, respectively. The multivariate conclusion here is obtained through weighted scalar observables, not an unsupported general square-positive multivariate representation theorem.
