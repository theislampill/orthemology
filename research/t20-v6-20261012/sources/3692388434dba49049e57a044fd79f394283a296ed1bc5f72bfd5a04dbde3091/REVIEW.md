# Independent review of fibrewise exact-law W–FR correction

11 October 2026 UTC. **PASS within the stated mathematical and implementation scope.** The author packet was frozen before final reread, replay, and digest verification. The reviewed RESULT.md is SHA-256 470c32630baad4b42a5ce960b73de9bf5c6e5cad0a1e32cf1d3f964a5373967d; AUTHOR_FREEZE.json is 8dd58daac1f3386c93f1540b346995cf12a338a26d18b2287667a9ec2b779445. BINDINGS.json records the remaining reviewed identities. No author or protected files were edited. This review grants no integration, release, or programme-closure authority.

## 1. Mathematical scope accepted

The construction is a discrete map on conditional probability laws with a fixed entire observed marginal. Its hypotheses are a Borel marginal ν, a Borel target mean g(y), a single fixed positive-definite target covariance T, and a finite integrated target-relative quadratic moment. These hypotheses permit arbitrary singular conditional starting laws and do not require ν or g to have ordinary second moments or joint smooth densities.

For each positive step, the OU transition covariance T(I−A²), A=exp(−hT⁻¹), is positive definite. Its Gaussian kernel yields a bounded, positive, jointly Borel latent density. Integrating a jointly Borel function against a probability kernel justifies the conditional measurability claim. Normalizing each reaction separately retains a probability kernel, so both substeps preserve exactly ν. Entropy can be expressed using the nonnegative integrand f log f−f+1, avoiding any measurability ambiguity from its signed form. Versions on a ν-null set do not change the joint law.

The Gaussian-transition KL is exactly

    ½ (x−g)ᵀ A T⁻¹ A (x−g) − ½ tr(A²) − ½ log det(I−A²).

Mixture convexity or KL data processing therefore gives the reported bound. It is an upper bound on mixture entropy, not an assertion that mixture KL equals averaged component KL; equality holds for a single atom. The coefficient and constant have both been independently checked. Finite integrated relative moment makes the bound integrable even when initial KL is infinite. No initial density, finite entropy, Fisher information, or endpoint action is being silently assumed.

## 2. Reaction, moment closure, and descent

For 0<a<1, the partition function ∫f^a dπ is strictly positive and at most one for every probability density f, including densities with zeros. On compact parameter intervals inside (0,1), powers multiplied by any fixed log power are dominated by a multiple of 1+f. Consequently the stated differentiation and finite interior entropy are valid. Differentiating aψ′−ψ gives aψ″, with ψ″ the tilted log-density variance. The finite-KL endpoint a↑1 follows by separate domination above and below f=1; finite log variance at that endpoint is not needed or asserted.

The normalized map solves the conditionally centred reaction equation at positive reaction times and composes as a semigroup. A positive-time power retains the exact zero set. In particular a normalized indicator remains fixed with positive KL, so reaction alone does not create full support or repair a singular law. The OU-first order supplies the density needed for the power map. The report distinguishes these domains correctly.

The entropy variational inequality at θ=1/4 gives

    M(μ) ≤ 4 KL(μ||π) + 2m log 2.

Applying it first to bounded truncations justifies the conclusion without presupposing the very moment being proved. This is the essential integrated step: no integrability of reciprocal fibre normalizers is needed. Smoothing gives finite entropy, reaction lowers it, and entropy restores a finite relative moment. Induction therefore closes for every finite iterate.

Classical Gaussian OU entropy contraction has coefficient exp(−2h/λmax(T)); density approximation extends it beyond smooth inputs. The reaction does not increase entropy. Thus every conditional entropy decreases, with the stated factor once finite, and its integral decreases by the same factor. The disintegration chain rule and Pinsker give joint KL/TV convergence to ν(dy)π_y(dz). An originally different target marginal leaves its fixed marginal-KL residual. This is discrete fixed-step convergence, not a theorem about the coupled PDE.

## 3. Singular shrinking-step trace

The identity

    KL(fπ || R_a(fπ)) = (1−a) KL(fπ||π) + log Z(a)

is correctly oriented. Since log Z≤0, it bounds the reaction displacement by (1−a) times the smoothed entropy. The smoothing constant grows only as (m/2)log(1/h)+O(1), so multiplying by 1−exp(−h) makes the integrated bound vanish. OU coupling tends to the original law because its displacement uses Z−g(Y), whose second moment is finite, rather than requiring a finite second moment of Y or g(Y).

It follows that one shrinking composite step converges weakly to the initial law. This does not imply TV convergence to a singular law, finite initial action, a continuous singular entrance, convergence of iterated splitting to a PDE, or all-law uniqueness. The report explicitly excludes those stronger statements.

## 4. Gaussian implementation and first-order distinction

Completing the Gaussian quadratic exponent gives the reaction precision a S_D⁻¹+(1−a)T⁻¹ and relative mean S_+ a S_D⁻¹ Aδ. These factors must retain their order. The independent exact fixture uses T=diag(1,1/2), h=log2, and a rank-one initial covariance with every entry one. It yields noncommuting precisions after smoothing, strictly positive output covariances, and rejects a swapped matrix order. This fixture differs from the author's stated fixture.

Independent full-density differentiation verifies the transport and centred-reaction generators separately and together. The resulting derivatives are

    δ′ = −T⁻¹δ − S T⁻¹δ,
    S′ = 2I − T⁻¹S − S T⁻¹ + S − S T⁻¹S.

This is more than a moment match. The corresponding Gaussian entropy derivative equals negative latent Fisher information minus log-density variance.

The general first-order statement is correctly restricted to f=1+u, with a compactly supported smooth perturbation, positive lower bound, and bounded upper bound. OU has an L¹ generator derivative there; bounded power/logarithm Taylor remainders justify the reaction derivative and their composition. Integrated differentiation additionally needs domination, as the text states. This does not include singular initial inputs.

The consistency target is the inherited stricter field rule v_y=0 and conditionally centred reaction. It is not the full fixed-marginal orthogonal projection. Independent controls reproduce the predecessor's positive fibre-entropy derivative at b=1, s=11/10 for that full projection, while the strict fibrewise derivative is nonpositive. The fields may fail to minimize the ambient action of their density tangent. No metric optimality is inferred merely from preservation and descent.

Finite covariance/feature updates are a valid restricted implementation interface. Arbitrary conditional kernels, measurable functions, or real parameters need not have a finite computable representation. Fractional powers of total mixture densities cannot generally be replaced by componentwise Gaussian powers; the report's cosh-versus-square-root-cosh countercontrol checks directly. Exact law formulas and floating-point evaluation remain separate claims.

## 5. Prior art and credit

Independent primary inspection of Crucinio–Pathiraja [v1](https://arxiv.org/html/2511.18060v1), §2 (2.5)–(2.6), §3 (3.3)–(3.4), and Appendix B.1 establishes direct prior art for exact normalized W→FR, power reaction, and Gaussian updates. Supplementary inspection of the preserved [v3](https://arxiv.org/html/2511.18060v3) confirms its version-specific hypotheses. Both versions expressly assume FR/WFR well-posedness; v3 uses bounded Hessians. No all-law PDE theorem is imported. Credit is a faithful fibrewise application with directly proved domain/interface guarantees, not a new splitting algorithm or field-priority result.

[Mielke–Zhu, Theorem 3.2](https://arxiv.org/html/2501.17049v1) supports the classical 2κ normalization. The [Gallouët–Monsaingeon primary abstract](https://arxiv.org/abs/1602.04457) supplies older variational W/FR splitting ancestry, with no full-paper reread claimed. SOURCE_READING.json records the independent inspection boundaries. Local predecessors already own the stricter control class, the per-fibre-worsening separator, and related Gaussian continuous-flow mechanisms.

## 6. Verification and limits

The independently written check.py imports no author or root checker. Normal and optimized runs each pass 36 controls: 20 exact algebraic controls and 16 numerical controls. Explicit exceptions retain checks under Python -O. Numerical quadrature and finite-difference examples supplement the universal proofs; they do not prove arbitrary-law inequalities, PDE existence, or computability. Portable replay requires Python, SymPy, NumPy, and SciPy:

    python3 check.py --output private-locator:e5bdeb04ed4ee617a198
    python3 -O check.py --output private-locator:ec503e28ddb2a0c2c095

The frozen implementation also passes 15 independent implementation controls in each mode, including 24 separately generated matrix-exponential oracle cases and a distinct exact rational fixture. Those controls reject complex entries in all four array arguments and nonreal steps, test tiny-step singular regularization, and check input immutability. The root-reported silent complex-to-real coercion defect was independently reproduced before the author fixed it. IMPLEMENTATION_FINDING.json preserves the failed digest and the fixed digest; it was an implementation validation issue, not a failure of the theorem. The final implementation SHA-256 is 76ff5de8c0a2f299530a4fb84905c622cd19b7188df11109988592f18a722711. Floating-point checks remain finite examples, not certified error bounds for every input.

The frozen author checker was independently replayed normally and with -O: both pass 65 controls with the five live predecessor comparisons (60 in the portable snapshot-only mode). The 13 author implementation test methods pass in both modes. These are labelled author replay, distinct from the independent controls. All 31 inventoried author files, the author-freeze digest, five input snapshots and their originals, and key reviewed identities pass 44 digest checks.

No blocking finding remains at these frozen bytes. The accepted mathematical scope does not authenticate the supplied target, add protected edits, establish formal-kernel certification, or close T20.
