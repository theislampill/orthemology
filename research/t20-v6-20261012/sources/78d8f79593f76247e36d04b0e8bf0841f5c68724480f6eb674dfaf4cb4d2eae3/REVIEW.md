# Independent review: quadratic probability-geometry transport

Date: 9 October 2026. Scope: mathematical review of the root derivation and two transport reports, without integration, protected-file edits, empirical claims, or T20 closure.

## Review status

PASS, bound to the exact root and author files recorded in Section 7 and REVIEW_RECEIPT.json. The root and both author reports pass under their explicit finite-dimensional hypotheses. This is ordinary mathematical review plus exact symbolic/rational controls, not proof-assistant certification. The review is finite: no later Fisher, tensor, state-dependent-mobility, or other additive report is covered.

The exact controls are in `check_independent.py`; 45 checks pass. They include additional negative controls for arbitrary Bregman generators, reference-resetting, two-law versus three-object recovery, absolute score versus regret, unreachable tangents, nonorthogonal coordinate descriptions, and finite-time loss of interiority.

## 1. Independent proof of weighted quadratic contraction

Let K be a nonnegative m-by-n column-stochastic matrix with no zero output row. Let μ_i>0, ν=Kμ, M=Σ_i μ_i=Σ_j ν_j. For any p,q in the same finite-dimensional real space, set δ=p−q and

D_μ(p,q) = (1/2) Σ_i δ_i²/μ_i.

This is the Bregman divergence of f_μ(p)=(1/2)Σ_i p_i²/μ_i. Positivity/coherence of p,q is needed for their stated probabilistic interpretation, but not for this algebraic inequality.

For each j define w_ji=K_ji μ_i/ν_j and d_i=δ_i/μ_i. The weights w_ji are nonnegative and sum to one. The exact gap is

2[D_μ(p,q)−D_ν(Kp,Kq)]
= Σ_j ν_j [Σ_i w_ji d_i² − (Σ_i w_ji d_i)²].

It is a sum of nonnegative variances. Equality holds exactly when d_i is constant over the support of every output row separately. This includes supports of size one; no connectivity or strict positivity of every K_ji is required.

If a column-stochastic R recovers p,q,μ simultaneously, then applying the inequality first to K and then to R gives equality. Recovery of p,q alone does not suffice. Conversely the displayed equality condition is the precise criterion; three-object recovery is a sufficient condition and has not been asserted to be necessary.

### Guard A: two-law sufficiency does not entail weighted equality

Use

p=(3/8,3/8,1/4), q=(1/4,1/4,1/2),
K=((1,1,0),(0,0,1)),
R=((1/2,0),(1/2,0),(0,1)).

R K p=p and R K q=q. For μ=(1,2,1), ν=(3,1), however,

D_μ(p,q)=11/256,
D_ν(Kp,Kq)=1/24,
fine−coarse=1/768>0.

R K μ=(3/2,3/2,1)≠μ. A pairwise recovery argument cannot silently substitute the reference measure for one of the probability arguments.

### Guard B: contraction does not extend to arbitrary weighted Bregman generators

For the strictly convex generator φ(t)=t⁴ on t>0 define

D_μ^φ(p,q)=Σ_i μ_i [φ(p_i/μ_i)−φ(q_i/μ_i)−φ′(q_i/μ_i)(p_i/μ_i−q_i/μ_i)].

Take the same deterministic K, μ=(1,1,1), ν=(2,1), and strictly positive coherent vectors

p=(19/100,1/100,4/5),
q=(31/100,29/100,2/5).

Then

D_ν^φ(Kp,Kq)−D_μ^φ(p,q)=921/1562500>0.

This is an exact counterexample to the unrestricted weighted-Bregman contraction claim. It does not oppose the stated quadratic theorem. Joint convexity of the scalar Bregman kernel would give a Jensen-based sufficient hypothesis for an extension, but arbitrary strict convexity of φ does not supply that hypothesis.

## 2. Independent information-versus-score check

For the p,q,K,R in Guard A but μ=(1,1,1), both probability laws and μ are recovered. K is injective on the declared submodel {(a,a,1−2a):0<a<1/2}; R is its stochastic inverse on this submodel. This recovers distributions, not the original fine atom in each realized sample.

The ordinary half-Brier regrets are

D_1(p,q)=3/64,
D_1(Kp,Kq)=1/16.

With the transported reference ν=(2,1), D_ν(Kp,Kq)=3/64. Resetting ν to a fresh all-ones vector changes the chosen geometry; it is not faithful reference transport.

The numbers above are regrets or Bregman divergences, not absolute expected losses. With truth law p and forecast q, ordinary half-Brier expected losses are 3/8 fine and 1/4 coarse; the corresponding Bayes risks are 21/64 and 3/16. Under the transported weighted score, the coarse absolute expected loss is 3/16. Thus preserving this pair-divergence does not assert preservation of all statewise vertex losses or absolute expected risks.

Two different operations must remain separate:

1. Garbling observations while retaining a fixed truth space and fixed score: conditional posteriors average, and proper-score information cannot increase. If a statistic preserves the posterior, the fixed-space information value is preserved.
2. Mapping the state/truth coordinates themselves from p to Kp: comparing fresh ordinary Euclidean/Brier scores on the two coordinate spaces changes the score representation. Sufficient recovery of a declared family of laws does not force those independently selected scores to be isometric.

The example supports only the second distinction. It does not refute an inherited injectivity, sufficiency, or recoverability claim stated in the first setting.

## 3. Independent canonical-versus-induced dynamics proof

The fine tangent space is T={h:1ᵀh=0}. The positive tangent metric is H=diag(1/μ). Define

G_μ=diag(μ)−μμᵀ/M.

For any ambient covector g, G_μg belongs to T. Since H G_μ=I−1 μᵀ/M, for every h∈T,

hᵀH G_μg=hᵀg.

This proves that G_μ is the inverse metric from covectors modulo constants to tangent vectors. It is not obtained by merely using the unconstrained diagonal inverse and ignoring the simplex constraint.

For J=Jbar∘K the fine negative gradient is −G_μ Kᵀ∇Jbar, and its projected velocity is −B∇Jbar where B=K G_μ Kᵀ. The canonical coarse reference ν instead gives −G_ν∇Jbar. The difference is

C=G_ν−B=diag(Kμ)−K diag(μ) Kᵀ.

For every z,

zᵀCz=Σ_i μ_i [Σ_j K_ji z_j²−(Σ_j K_ji z_j)²]≥0.

An alternative exact iff argument uses the trace:

tr(C)=Σ_i μ_i(1−Σ_j K_ji²).

Each summand is nonnegative; with μ_i>0 it vanishes exactly when column i is concentrated at a single output. Consequently C=0 if and only if every column of K is deterministic. If μ has zero entries, zero-weight columns escape this conclusion, which is one reason the positive-reference hypothesis must remain explicit.

Both B and G_ν annihilate constants and take values in the coarse tangent space. Equality of intrinsic fields for every smooth coarse objective is therefore equivalent to equality of the ambient matrices: linear objectives realize every coarse tangent covector modulo constants. The deterministic restriction is universal over objectives. A noisy K can still preserve an individual objective whenever C∇Jbar=0 along the relevant states.

Exact binary control: μ=(1/2,1/2), K=((3/4,1/4),(1/4,3/4)), Jbar(r)=r_1 give projected velocity (−1/16,1/16) and canonical velocity (−1/4,1/4). Their difference is nonzero despite divergence contraction. The author controls additionally test a ternary direction change, so the failure is not generally removable by changing the time scale.

These are local interior flow statements. A linear objective already gives a constant nonzero tangent field which can meet the simplex boundary in finite time. Even a deterministic lumping can keep the coarse state interior while a fine coordinate reaches zero. No claim of global simplex invariance follows for arbitrary tangent objectives.

## 4. Independent quotient metric and minimum-energy lift

Let W=K(T) be the reachable coarse tangent image. Since G_μ is positive definite as a cometric on T and has kernel span(1),

range(B)=range(K G_μ Kᵀ)=K(T)=W.

One proof factors G_μ=AAᵀ with range(A)=T; then range(B)=range(KA). The induced cometric is positive definite on covectors modulo W⊥. Equivalently, its inverse defines a positive metric on W. It need not define a finite metric on the whole coarse tangent space.

For v∈W, write B⁺ for a Moore–Penrose inverse in a Euclidean coordinate representation and set

h*=G_μ Kᵀ B⁺v.

Then h*∈T and Kh*=BB⁺v=v. Any other feasible tangent lift is h*+z with z∈T∩ker(K). By tangent duality,

zᵀHh*=zᵀKᵀB⁺v=0.

The exact energy decomposition is

(h*+z)ᵀH(h*+z)=h*ᵀHh*+zᵀHz.

Strict positivity of H gives a unique minimizer. Its energy is

h*ᵀHh*=(B⁺v)ᵀBB⁺v=vᵀB⁺v.

This argument proves both the formula and representation independence. The displayed pseudoinverse itself need not transform tensorially under a nonorthogonal coordinate change; its restricted energy and the reconstructed lift do, because they represent this unique constrained optimization problem. The controls explicitly verify a nonorthogonal re-expression.

For v outside W, the lift constraint is infeasible. The expression vᵀB⁺v alone must not be misread as assigning a finite cost to such directions; it discards the nullspace component and is only the quotient metric on W.

Exact rank-deficient control:

K=((1/2,0,1/4),(1/2,0,1/4),(0,1,1/2)), μ=(1,2,3),
v=(1,1,−2),
B=(17/96) vvᵀ,
h*=(28/17,−40/17,12/17),
minimum energy=96/17.

The fibre kernel is spanned by z=(−1/2,−1/2,1). The direction (1,−1,0) is an unreachable coarse tangent. All identities and the full Pythagorean polynomial in an arbitrary fibre scalar are checked exactly.

The quotient construction does not imply that the canonical reference metric was preserved by every noisy K. It constructs the geometry that faithfully represents the projected fine gradient.

## 5. Radial normalization versus tangent objectives

Mass preservation gives N(Kb)=K N(b) whenever both are defined. The inherited full-Hessian correction from the nonseparable repair has

ḃ=−(s−1)p/a″(s), s=Σb_i, p=b/s.

With the same radial function a at both resolutions, this field commutes with every mass-preserving K, and the prior global radial theorem remains intact. It is a different vector field from a newly chosen tangent objective flow. Adding a nonconstant tangent objective changes the correction and can increase the score at one truth vertex while decreasing it at another; the prior all-truth monotonicity guarantee cannot simply be retained for that augmented field.

## 6. Source and warrant boundaries

The root derivation is an independent mathematical argument. The Csiszár–Shields tutorial was checked through the online PDF extraction at §4, printed pp.447–448, including the f-divergence definition, χ² instance, inequality (4.1), and Lemma 4.1 with its proof. That source establishes classical ancestry for the convexity/lumping argument; it does not directly state the entire three-object signed-difference quadratic theorem, the current mobility comparison, or this project's interpretation. No full-paper reading, local PDF-byte hash, exhaustive novelty survey, or theorem-priority claim is made.

Source URL: https://www.renyi.hu/~csiszar/Publications/Information_Theory_and_Statistics:_A_Tutorial.pdf

The previously reviewed nonseparable repair RESULT.md §§6–7 was read to verify the inherited radial field and the difference between mass repair and evidence-driven discrimination. Author source bindings receive a separate byte-level check below.

The result is conditional on the mathematical representation, μ, K, score, and objective being declared and appropriate. None of their formal properties warrants the empirical existence or identifiability of such structures in actual human cognition, confers authority on a report or claimant, authenticates a historical source, or establishes metaphysical truth. The work does not close T20.

## 7. Frozen author review

### Noetic-gradient report: PASS after one localized scope repair

The complete report and verification script were read. All 33 exact control groups were rerun independently, with output preserved as `noetic-review-run.txt`. All five manifest entries passed their size and SHA-256 checks. Every local-source SHA-256 and all five supplied Git blob hashes were independently recomputed; results are preserved as `noetic-source-byte-check.json`.

One precise wording defect was found before approval: full row rank had been described as yielding a quotient metric on the “whole coarse simplex.” Full row rank guarantees the whole coarse tangent space; it does not imply that every coarse state has a positive fine lift. The author corrected this wording and added the binary reachable-interval control. No formula changed. The earlier RESULT digest 8333a3450ff263199fec6e261976b7453beb6a4ae2ef917a31571e8ce7966676 is superseded and is not the approved version.

The approved frozen bytes are:

- `noetic-gradient-transport-20261009/RESULT.md`: 27f85cd312cb2083d26257e6c74fea8e547c879dce07d94c04d8c87446c0f4a9
- `noetic-gradient-transport-20261009/MANIFEST.json`: d79d63fdebf48998126320cd9b81c7eb9325fe8237c9ca5f5b34cbf53258dcd4
- `noetic-gradient-transport-20261009/verify.py`: f5559d97ee52bd249c38e1a4a43f76df69d57fed4bbbdd0d3ee2efc963856570

The source comparison is appropriately bounded: the retained S1/S6 local-repair source positively records prior Hessian work and normal/tangent differences; H-ICS supplies a separate finite observation-congruence/result-determination contract; CP12 uses a differently typed calibrated statistic; and DAEE bounds literal gradient interpretation. Targeted source passages were independently checked, without upgrading their inherited verification status or extrapolating to the whole project.

Alvarez–Bolte–Brahic, *Hessian Riemannian gradient flows in convex programming*, §2.2 equations (7)–(10), was independently checked in the online PDF extraction. Its affine-constrained projected inverse-Hessian formula specializes to G_μ. This confirms the limited ancestry attribution, without importing its Legendre/global-flow hypotheses or results. Source: https://arxiv.org/pdf/1811.10331 . No local PDF-byte hash was established.

### Information-geometry report: PASS after two bounded evidence-quality repairs

The complete report and script were independently read. All 61 checks reran successfully; this count includes exact mathematical controls and source-byte checks, not 61 general theorems. The output is preserved as `information-review-run.txt`. Both reviewer-origin negative controls are written in the report and independently replayed in its script, and its ledger binds the reviewer’s frozen `NEGATIVE_CONTROLS.json` and 45-control script.

The additional written proofs were independently checked:

- Cross-space Bregman contraction for C² potentials is equivalent to the tangent-Hessian inequality at every fine interior point. Necessity is the local second-order expansion; sufficiency integrates the inequality on the full segment joining q to p. A single-point match is not enough.
- With one unchanged radial potential, the inherited ambient identity reduces full-cone contraction exactly to the coherent-space condition. It does not produce a new restriction on the radial function or assert that arbitrary likelihood multiplication descends.
- The positive binary observation channel realizes both displayed Brier witnesses as exact Bayes posteriors of the stated prior. Its conditional-law recovery and the KL equalities are correct. The equivalence of fine/coarse experiments is expressly about Y and the declared statistical submodel, not samplewise recovery of X.
- On a fixed truth space, conditional expectation gives p_Z=E[p_Y|Z], so the exact loss of coherent information under observation garbling is E D_f(p_Y,p_Z). Jensen and strict convexity give the stated nonnegativity and equality case. This does not transfer to model correction or changes of operative warrant.
- The reported prior/posterior weighted Bayes risks are correct; only their gains agree across the changed truth spaces.

Two bounded evidence-quality repairs were requested and verified, with no change to RESULT.md: the normalization control now recomputes the mass of K*raw explicitly; the local nonseparable scratch report’s ledger entry now claims only its actual SHA-256 binding rather than an unavailable Git blob check. Neither repair changed a mathematical claim.

The approved frozen bytes are:

- `information-geometry-transport-20261009/RESULT.md`: 077fabaf882988d2de23bda85fd40cc03f6f630c0ca859f12864d53c604fbd94
- `information-geometry-transport-20261009/MANIFEST.json`: 3029c31994f42b240c9eafb69758cefc661282e434621ba42db434f9e7d7560e
- `information-geometry-transport-20261009/verify.py`: 5be0ea120015682aafb73074d74c52608e55931589be4e82e50bc2c1309c2287
- `information-geometry-transport-20261009/SOURCE_LEDGER.json`: 75e52227b20200b07dae1751b498184c304233cc2dc6451d2ec1584ff545a201

The earlier information manifest 85dee5d066fb0bb2f34160ec225b259017a08c52008e7a8bde1f11102ffea6a3 is superseded and is not the approved evidence bundle.

H-formalisation Proposition 4.1, Theorem 4.2, and Corollary 4.3 were independently read with their proofs and status qualifications. They concern declared-view recoverability and target factorisation; the report correctly avoids attributing Bregman isometry to them or identifying typed tensors with probabilities by notation alone.

### Root derivation and independent controls

The approved root note `transport-interface-root-check-20261009/DERIVATION.md` has SHA-256 f9b7ebaa77b5ae925b60f30ac0267a63a41a7e6dd92da23ca5e34857f930ad37. Its revised explicit fixed-reference and regret-versus-risk qualifications were read. It receives PASS only for the bounded claims in that version.

The reviewer’s frozen negative-control JSON has SHA-256 f3f14571d2cf95d051ae45258e87fbef548757cae40afb85a1c0728f952dc6ee. The reviewer’s `check_independent.py` has SHA-256 c9f6d64073a1a69e3d9909a76882492391b1c9e9c4ab45402382d9eac1a0f497. These are separate controls, not proof-assistant certificates.

### Independent remote pin check and replay

After reading the relevant byte-matched local source passages, the reviewer directly fetched one line from each of the six repository sources at its exact declared commit through the GitHub connector. Every returned full-file Git blob matched the independently recomputed local blob: H-formalisation, H-ICS, the inherited S1/S6 Hessian note, sound-descent comparison, CP12, and the DAEE formalism. The actual returned metadata and narrow fetch scope are preserved in `REMOTE_SOURCE_BINDINGS.json`. This verifies commit-to-file binding without claiming a new full-source read.

`REVIEW_RECEIPT.json` binds the finite reviewed set, including author manifests, report and script bytes, all local sources, and the reviewer report. `REVIEW_MANIFEST.json` binds this reviewer packet. `verify_review.py` checks those bindings and replays all three scripts. The remote pin observations are historical connector evidence from this review, not a promise of a new remote query on each local replay.

No unresolved mathematical or source-scope defect remains within the approved versions. General claims are supported by ordinary written proofs; finite exact controls are supporting evidence; no new kernel-checked theorem is claimed. No protected source or repository integration was performed, no actual human or metaphysical warrant was established, and T20 is not closed.
