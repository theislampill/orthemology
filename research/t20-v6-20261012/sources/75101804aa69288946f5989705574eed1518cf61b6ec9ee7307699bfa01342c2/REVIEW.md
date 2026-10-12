# Independent review: ordered control tensors and projective continuation

11 October 2026 UTC. Internal independent mathematical review of the completed author packet. This is ordinary proof review plus exact symbolic checking, not external peer review, a proof-assistant certificate, source authentication, protected integration, or T20 closure.

## Disposition and immutable target

**ACCEPT within the explicit finite-jet, full-law and local-flow scope of the frozen report. No blocking mathematical correction is required.**

The accepted target is `ordered-control-projective-transport-20261011/RESULT.md`, SHA-256 `8feef686238981aae90112805a6478b3693476f5b08ae90b28cd0a0b08b22a30`, bound by author `MANIFEST.json`, SHA-256 `33f5ee1809d2f5674b009798d12e413fd597c70d68281d5d78746ec3470d7663`. Acceptance does not extend automatically to later edits. The final machine-readable acceptance records the reviewer artifacts and these same pins.

The result correctly supplies four things: a declared ordered-control representation into polynomial operators; exact scalar-projective faithfulness of finite operator jets when every finite-support law and polynomial readout is tested; the Lie-versus-associative normalization boundary; and a positive-stage, coercive example whose degree-two control data agree but whose degree-three normalized outputs differ.

## Review independence and executed evidence

The parent supplied the candidate statements and signs. Before inspecting the author's derivation, this reviewer independently derived the scalar-kernel induction, the Lie commutator, the free-word cubic discrepancy, and the translated-quadratic mean coefficient. This is independent checking of proposed claims, not independent discovery of their conjectures.

`independent_checks.py` imports neither the author script nor the root's finite-matrix control. Its nine exact check groups passed with SymPy 1.14.0. The central normalized-output checks use independently composed exact characteristics and symbolic initial moments, rather than the author's represented-word numerator route. The finite tests corroborate the written universal arguments; their finite polynomial list does not prove a universal statement by sampling.

The frozen author packet was also copied, unmodified, into a temporary reviewer-owned replay tree. Its inherited inputs were read through symlinks to the bound originals. Its 41 exact controls passed, including the two Fliess source-byte checks, and the regenerated `CHECKS.json` exactly matched the frozen hash. The original nine-file author manifest was verified before and after replay; no author file was changed. `AUTHOR_REPLAY_RECEIPT.json` and `AUTHOR_REPLAY.log` record this separate replay.

## 1. The ordered representation is correctly typed

For the fixed polynomial algebra P and fixed objectives F_i, B_i p = −∇F_i·∇p − F_i p is a real-linear polynomial endomorphism. It need not be a derivation: B_i1 = −F_i. Assigning a control letter e_i to B_i therefore invokes the free associative tensor algebra's universal property with an explicitly supplied map. It does not identify the control alphabet with the inherited semantic roles or with the state-coordinate vector space.

For finite N, the ideal of grades greater than N is two-sided. Sending a length-r word to ε^r B_w consequently defines a genuine algebra map from the truncated tensor quotient into A⊗R[ε]/(ε^(N+1)). Truncation is essential: the finite vector-space sum of the first N grades is not usually a subalgebra under untruncated concatenation. The source and target grading is control/ε degree, not polynomial degree or differential order.

The added weight-coordinate construction is sound. On P[z], the vector field −∇F_i·∇_x − F_i z∂_z sends zp to zB_i p and preserves homogeneous z-degree one. Iterating proves the word intertwiner. The inclusion p↦zp is linear and injective, but not multiplicative. Thus the actual killing term is retained when comparing with ordinary vector-field expansions.

There can be additional word kernel. Equal generators or commuting represented operators already give examples. Neither this representation nor its normalized version recovers raw words or control paths in general. The report states that restriction correctly.

## 2. Actual finite jets and their analytic boundary

For the stated piecewise-constant finite control and compact initial support, sufficiently small positive and negative ε keep all characteristic trajectories in a common compact set. This follows from ordinary uniform local existence for finitely many smooth fields, or directly from a bound on their velocities in a compact neighborhood and the fixed finite control duration. The weighted coordinate remains positive and bounded there.

The weighted observable pullback satisfies U'_s = ε U_s B_{u(s)}. Iterating the integral equation orders the earliest operator on the left. Hence physical F then G acts as U_F U_G on observables, matching both the control words and the inherited convention. Splitting the integration simplex at a concatenation time proves the stated product of signatures.

After N substitutions, the remainder involves only finitely many length-(N+1) polynomial operator words evaluated along the controlled characteristics, with bounded weights and finite control L1 norm. This gives the claimed uniform O(|ε|^(N+1)) bound for each fixed polynomial observable and compact initial support. Integrating preserves the bound. Since the mass denominator tends to one, normalization has precisely the formal quotient jet near zero.

This proves neither convergence of an unrestricted infinite operator series nor exact finite-degree continuation at nonzero duration. Constants in the remainder may depend on N, the observable, control and support. No total-variation differentiability of moving atomic laws is needed. The report's distinction between formal operator jets and actual positive flows is adequate.

The polynomial-degree bound is also valid: if D is the maximum objective degree, each B_i increases polynomial degree by at most D. Consequently initial moments through r+ND and ND suffice for the numerator and denominator of a degree-r observable's N-jet. This does not create one fixed finite moment closure for every time and output.

## 3. Full-law scalar projective faithfulness

Here is the independent proof of the key separating step. Suppose D is a real-linear map P→P and every finite-support probability μ satisfies μ(Dp)−μ(D1)μ(p)=0 for every polynomial p. Set a=D1. On a Dirac law at x, the equality reads (Dp)(x)=a(x)p(x). Since it holds for every x, polynomial equality gives Dp=ap. For the half-and-half law at distinct x,y, the same expression is

    (a(x)−a(y))(p(x)−p(y))/4.

A linear polynomial separates x and y, so a(x)=a(y). Hence a is constant and D is scalar. Conversely scalar D plainly vanishes under this normalized infinitesimal readout. This proof applies to all polynomial endomorphisms; it does not depend on a differential-operator representation.

Now let U,V have identity constant term modulo ε^(N+1). If scalar coefficients have already made U−cV vanish below order k, its leading difference ε^kD changes the degree-k normalized readout by exactly μ(Dp)−μ(D1)μ(p). The lemma makes D=d_kI. Adding d_k ε^k to c removes this coefficient because V_0=I. Induction through N constructs the common scalar jet. Its uniqueness follows from the formal inverse of V. The converse is exact scalar cancellation.

The assumptions doing substantive work are the identity constant term, the complete polynomial output family, and the all-laws test. Diracs alone cannot detect a nonconstant multiplier: M_x is invisible at every singleton, but at the equal mixture of −1 and 1 its normalized infinitesimal x-output is one. Restricted laws or outputs can therefore have larger equivalence classes. The finite-jet theorem is not a theorem about arbitrary finite positive kernels away from identity, where rank collapse and impossible branches introduce other behavior.

The formal near-identity quotient G_N/Z_N and chronological right-action formula are correct. Extension to formal normalized functionals keeps every mass denominator a unit. This is an algebraic action, not an assertion that each formal jet preserves an actual positive cone.

## 4. Lie commutator and associative obstruction

Work on the affine algebraic dual L(1)=1 and its algebra of polynomial cylindrical functions. With l_p(L)=L(p), define D_B l_p=l_(Bp)−l_(B1)l_p and extend by the Leibniz rule. The relations among evaluation functions are respected, including l_1=1. Direct calculation gives

    D_BD_C l_p = l_(BCp) − l_(B1)l_(Cp) − l_(BC1)l_p
                 − l_(C1)l_(Bp) + 2l_(B1)l_(C1)l_p.

Antisymmetrizing leaves D_[B,C]l_p. Thus [D_B,D_C]=D_[B,C] with the standard commutator of derivations. Equivalently, using vector-field coordinates X_B(L), the bracket is D X_C(L)[X_B(L)]−D X_B(L)[X_C(L)]. This sign matches the author's convention.

The preceding scalar-kernel lemma makes the kernel exactly R I when all finite-support laws and polynomial outputs are admitted. The resulting quotient is a Lie quotient by scalar operators. It is not a claim that a possibly larger center of a particular generated algebra is entirely invisible.

There is no corresponding nonzero associative quotient that kills I: every B=BI would vanish. If the algebra contains a nonscalar B, the scalar span is not a two-sided associative ideal. Scalar shifts of generators are therefore different from scalar multiplication of full propagators. The report correctly retains multiplicative projective composition for positive weighted flows with common domains and explicitly warns that products of nonzero general positive kernels can be zero.

## 5. The positive-stage discriminator and both effects

Expanding e^(tA/2)e^(tB)e^(tA/2) and its A/B interchange in the free associative algebra gives the same grades zero, one and two. Their cubic difference has coefficients −1/8 on AAB and BAA, +1/4 on ABA, +1/8 on ABB and BBA, and −1/4 on BAB. This is exactly −[A+B,[A,B]]/8.

For F=x²/2 and G=(x−a)²/2, a≠0, independent differential calculation gives

    [A,B]=a∂x,
    [A+B,[A,B]]=2a∂x+(2ax−a²)I.

The cubic difference operator is therefore D=−a∂x/4−axI/4+a²I/8. Since the lower operator coefficients coincide, its normalized effect is

    μ(Dp)−μ(D1)μ(p) = −a[μ(p′)+Cov_μ(x,p)]/4.

For p=x this is −a(1+Var_μ x)/4, nonzero for every compact probability law when a≠0. The singleton coefficient is −a/4; the equal ±1 mixture has coefficient −a/2. The covariance contribution is genuinely the nonconstant relative-weight effect.

The exact-flow verification is independent of the operator-word calculation. A stage with center c and contraction r sends y to c+r(y−c) and subtracts (y−c)²(1−r²)/4 from the log weight. Composing the three positive stages, with q=e^(−t/2), gives

    y_P−y_Q = a(q−1)³(q+1),
    log(w_P/w_Q) = a(2x−a)(q−1)³(q+1)(q⁴+1)/4.

Both formulas and their cubic coefficients agree with the frozen report. The log-odds difference for initial labels +1 and −1 is a(q−1)³(q+1)(q⁴+1). Terminal position and relative-weight effects are both present; labeling the atoms by their initial point avoids conflating odds with a fixed spatial-support comparison.

Each individual quadratic flow is complete forward in time, with positive weights and compact images of compact supports. Both protocols last 2t and spend total time t under each objective. Thus this counterexample uses no negative-duration stage or unjustified inverse-time intervention. The exact endpoint discrepancy is nonzero for every t>0. The general normalized mean formula is the stated local asymptotic, not a claim that its cubic polynomial equals the full finite-time mean difference.

## 6. Sources, bounded deduplication and retained boundaries

The reviewer directly checked the inherited H-formalisation's tensor-algebra/order passages and future-safe quotient criterion; H-Continuation §5's ordered products, branch mass and terminal numerators; the symmetric-moment and direct-sum restrictions in tensor-moment continuation; the full moving-objective-order report; the pure-reweighting switching report; and the audit-continuation posterior-only/projective discussion. These support the author's stated ownership distinctions.

The 211-file bounded top-level scan is retained as the author's search record. This reviewer checked its scope and the named consequential inherited comparators, rather than claiming to have independently read every scanned document or exhausted prior art. The degree-two bracket, translated quadratic FG/GF effect, warning about nested killing, and mass-versus-normalized-state distinction are correctly treated as inherited. The new packet's bounded contribution is their explicitly typed finite-jet/projective interface and the equal-low-grade positive protocol. No field-priority assertion is accepted or needed.

The retained Fliess text was inspected at printed p.10, pp.20–24 and pp.29–31. It supports iterated-integral definitions, differential-operator series, local convergence qualifications in its own analytic setup, the commuting-field reduction, and Chen concatenation. Printed p.21 explicitly warns of its reverse word convention; the report supplies its own consistent convention. IV.1's path-characterization wording is not imported. The review checked the retained PDF/text byte bindings, not an independent source acquisition or full-paper authenticity. The author's proof does not depend on the external paper to justify an unrestricted convergence assertion.

Finally, scalar objective shifts preserve normalized laws but change mass. Arbitrary killing weights are not automatically calibrated likelihoods or survival probabilities. Nothing here identifies the numerical control alphabet with semantic roles, licenses source-history deletion, proves empirical cognition or warrant, establishes unrestricted nonlinear moment closure, or closes T20. These are substantive boundaries retained in the accepted report.

## Replay

Run `python independent_checks.py` from any working directory to regenerate the reviewer's nine-group `CHECK_RESULTS.json`; only Python and SymPy are required. No source document bytes are required for that mathematical replay.

For the unmodified author check, place its directory beside the relative paths in `INPUT_BINDINGS.json` and run `python ordered-control-projective-transport-20261011/check.py`. The last two checks require the retained Fliess PDF and text and only compare their bytes. A public or portable package excluding those bodies must disclose any working-copy removal of those two external-source hash checks; such a 39-control replay is not the original 41-control replay. The original script and original full-run receipt should remain preserved. Other omitted inherited inputs likewise require explicit treatment rather than silent claim of complete replay.
