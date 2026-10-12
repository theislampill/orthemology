# Independent mathematical analysis: channel-natural repair

Date: 2026-10-09 UTC. Review scope: ordinary mathematics, exact controls, source-hypothesis comparison, and immutable artifact binding. This is not a kernel proof, implementation audit, integration decision, philosophical warrant finding, or T20 closure.

## Result

The parent candidate derivation and the author's matching simplex, cone, and coordinate-additivity conclusions are correct with the stated quantifiers. No material mathematical defect was found. The direct proof is important because it does not start with a Riemannian metric or presume that a C² strictly convex function has an everywhere positive-definite Hessian. The common positive Fisher coefficient follows from channel contraction and coherence across dimensions.

## Independent proof reconstruction

Let h_n(p) be the Hessian of f_n on the affine tangent space T_n, with n≥2. The stated forward divergence is D_f(p,q)=f(p)−f(q)−df_q(p−q). Taylor expansion in its first argument gives local contraction h_m(Kq)[Kv,Kv]≤h_n(q)[v,v]. The reverse implication is valid by the integral with weight 1−t along q+t(p−q). Positivity of p,q and no zero output row ensure all points at which a potential is evaluated are interior. C² suffices for both steps.

1. A strictly positive coordinate splitting E has a deterministic block-sum left inverse R, and both maps satisfy the allowed channel conditions. Applying local contraction to E and R gives equality. Permutations similarly have their stochastic inverses in the contract. This concerns Hessians and divergences; the original potentials need not literally be symmetric because affine gauges are invisible.
2. At the uniform law, extend h_n by the sum-zero orthogonal projection to the whole coordinate space. Permutation invariance of the resulting symmetric matrix forces equal diagonals and equal off-diagonals. Its tangent restriction is α_n times the Euclidean form, α_n≥0. This is valid in binary dimension as well; no nonzero tangent exists in one-state dimension.
3. Uniform n→nk splitting divides the squared Euclidean tangent norm by k, so α_nk=kα_n. Comparing n and m through nm gives α_n/n=α_m/m=c. This step needs the actual cross-dimensional family assumed in the theorem. The proof does not establish the same conclusion for an arbitrary finite cutoff or an isolated binary simplex.
4. For p_i=k_i/N, the splitting into k_i subcells sends p to the N-state uniform law and repeats v_i/k_i exactly k_i times. Thus h_n(p)[v,v]=c Σ_i v_i²/p_i. Positive rational laws are dense; continuity of the Hessian extends this equality to every interior point for each fixed tangent. Polarization yields the bilinear formula.
5. Negative Shannon entropy has this tangent Hessian with c=1. Subtracting c times entropy leaves zero Hessian in global affine simplex coordinates; integrating the constant gradient on the convex domain gives an affine function. If c=0 then every nontrivial f_n is affine, contrary to strict convexity. Consequently c>0 and the tangent Hessian is everywhere positive definite as a conclusion.
6. The converse is ordinary rowwise log-sum. Entries with K_ji=0 contribute zero and are harmless; each row has a positive output total. Summing the inequalities and using column sums one gives the required forward KL contraction. Its orientation is KL(p||q), not its reverse.

This is a complete ordinary proof of the stated iff. Finite controls cannot replace its density, all-channel, all-dimension, or integration steps.

## Cone argument and exact gauges

Under the independently established normalization-repair theorem, F_n(sp)=s f_n(p)+a_n(s) and D_Fn(sp,tq)=sD_fn(p,q)+D_an(s,t). The first mass s is correct. Its coefficient is not t and it is not a symmetric average.

Normalized-only tests set both masses to one, eliminating every radial divergence. They therefore permit dimension-dependent radial functions, subject only to the regularity and strict-convexity needed for the original cone hypothesis.

Full-cone tests on proportional inputs sp,tp remove the coherent term instead. A positive stochastic channel exists for every ordered dimension pair (choose identical positive columns). They yield D_am≤D_an; the reverse ordered dimension comparison gives equality. This is equality of radial divergences, not equality of the literal functions. Since the functions are C², differentiating twice in the first argument shows their difference is affine. If every a_n(1)=0, the difference is a multiple of s−1. Coherent affine terms multiply by s to become ambient affine terms, and remaining radial affine terms also are ambient affine. A single radial representative can therefore be selected without changing any divergence.

Conversely, the common radial term is invariant because column-stochastic maps preserve both masses. KL contraction proves full-cone contraction for any common C² strictly convex radial shape. The perspective strict-convexity criterion from the input packet ensures genuine strict convexity of these cone generators. No positive radial second derivative is implied by strict convexity alone: (s−1)^4 is a valid strictly convex radial shape with zero second derivative at s=1. Inverse-Hessian statements would need a''>0. The quadratic radial choice produces a positive-definite cone Hessian and a non-KL cone divergence despite a KL restriction to the simplex.

Coordinate-additivity in any dimension n≥2 forces mixed derivatives to vanish. For the classified family these are a''(s)−c/s, hence a''=c/s on all positive masses. Integration gives a=c s log s+As+B and the usual unnormalized KL divergence. The same conclusion follows from coordinate-pair additivity of the divergence, by mixed first-vector derivatives. Tensor-product additivity is a different condition and is not used. Coordinate-additivity in dimension one alone would be vacuous and could not fix a; the theorem's n≥2 setting avoids that error.

## Edge and countermodel audit

- n=1 can be adjoined with the unique zero coherent divergence. Strict convexity on a singleton, if defined vacuously, cannot identify c. Cross-dimensional cone comparison including n=1 can align its radial divergence with the common one, but no n=1 assumption is needed for the result.
- The isolated n=2 quadratic example is correct for every binary stochastic channel. Its scalar tangent factor is a−b with absolute value at most one. It is a genuine countercontrol to an overbroad binary-only uniqueness claim. This does not say that all-dimensional hypotheses are minimal; established fixed-alphabet results in larger dimensions have their own hypotheses.
- A no-zero-row channel may contain zeros elsewhere. Deterministic coarsenings and disjoint refinements used in the proof are therefore allowed. Replacing the contract with strictly positive matrices alone would require a separate limiting argument, not given here and not needed.
- No extension of arbitrary interior potentials to boundary states is presumed. Boundary continuity is an additional assumption in some cited Bregman theorems, which cannot be silently imported here.
- Transported-reference quadratics are indexed by (n,μ), with target (m,Kμ); they are not the n-only family classified above. Resetting a reference after merging changes the hypothesis. The independent controls reproduce exact fine/reset values 3/64 and 1/16 and transported equality 3/64.
- Fixed-truth evidence garbling compares posterior random vectors in one truth simplex under one score and joint law. Jensen monotonicity for all convex potentials, including Brier, is compatible with the cross-truth-coordinate uniqueness theorem.
- Affine gauge freedom includes constants on a simplex; these need not be coordinatewise identical across dimensions. The theorem fixes divergences and tangent Hessians, not canonical numerical potential values. Affine additions also cancel from vertex-form Bregman losses wherever these are defined. Arbitrary proper-score outcome baselines are separate choices; they do not arise from affine changes to the Bregman generator. Recoverable splitting may preserve KL while changing absolute Bayes risk: splitting the first cell into equal halves adds p_1 log 2 to entropy.

## Classical source comparison and reading limits

Primary research inspected directly through web-extracted text:

1. [Jiao, Courtade, No, Venkat and Weissman (2014), author-hosted published paper](https://people.eecs.berkeley.edu/~courtade/pdfs/CuriousCase_TIT2015.pdf), §II definitions/Remark 1 and §III-C Theorem 4 and discussion, printed pp.7617–7620. It establishes KL uniqueness for fixed-alphabet Bregman sufficiency when n≥3, with binary exceptions, and uses the same forward divergence. Its definition has a closed-simplex generator and same-alphabet channels. Accordingly it provides direct classical Bregman ancestry but is not invoked here as a literal theorem under identical hypotheses. The binary square example and relevant Appendix C symmetry lemma were also inspected. The full Appendix C proof was not audited.
2. [Montúfar, Rauh and Ay (2014), author preprint](https://arxiv.org/pdf/1404.0198), §3 Definition 1, Theorems 2–3, and Remark 4, printed pp.4–6. These record the classical all-simplex Chentsov theorem, the larger Campbell cone metric family, and the need to justify extension when deducing one from the other. This supports the classical attribution and the warning against assuming a unique radial extension. It is a primary research paper reporting earlier theorems, not an original-source reading of Chentsov or Campbell.

Additionally, [Fujiwara, Hommage to Chentsov’s theorem](https://link.springer.com/article/10.1007/s41884-022-00077-7), publisher introduction and beginning of §2, was checked against the author’s added citation. It explicitly points to Chentsov Theorem 11.1 for the metric result and distinguishes the affine-connection appendix. This is survey confirmation only, not an original-source proof audit.

The original [Campbell publisher PDF](https://community.ams.org/journals/proc/1986-098-01/S0002-9939-1986-0848890-5/S0002-9939-1986-0848890-5.pdf) returned a retrieval error on this reviewer's distinct attempt; the indexed primary abstract was accessible. The original Chentsov book was not read. No PDF downloads were made, avoiding duplicate source copies. These limitations do not weaken the independent elementary proof, but they limit any claim of classical-original-source audit. The author openly records the same distinction. This review makes no field-novelty, historical-priority, or exhaustive-literature claim.

## Independent controls

independent_controls.py uses SymPy exact rational/symbolic arithmetic. Its 43 passed assertions cover rational uniformization, reversible refinements, dimension scaling, all-binary symbolic tangent scaling, selected binary channels, reset/reference quadratic distinctions, an all-tangent rational noisy Fisher comparison through exact PSD principal minors, cone Hessian and forward-divergence identities, coordinate-additivity, strict-convexity degeneracy, unequal radial terms, and affine gauges. The ordinary reasoning above establishes universal conclusions; the script checks examples and identities only.

All existing inputs are preserved. The final review seal records the exact author and review artifacts to which the assessment applies.
