# Independent review: conditional entropy through fixed-marginal correction

11 October 2026 UTC. Disposition: **PASS within the stated mathematical scope**.

The reviewed author result is `conditional-entropy-control-20261011/RESULT.md`, SHA-256 `fd04c9de5028dc997c1714d09a8fa853b87861137f1a4e77ef6553f69f084151`. Its author manifest SHA-256 is `f3851ad2debc5a4fd5d089304c1843f51f7d1417e55588b73683d5144d32e746`. The author declared the packet frozen before the final digest check. This review changes no author or protected bytes and grants no integration, release, or programme-closure authority.

## 1. Main result checked

For the inherited unit transport/centred-reaction tangent geometry, subtracting a potential that depends only on the observed coordinate cannot change the latent gradient. Splitting the spatial gradient and applying conditional total variance gives exactly

    D = Eν[I_z] + Eν[Var(q | Y)]
        + Eμ[|∇_y q − ∇φ|²] + Varν(h − φ).

All four terms have the correct signs and constants. The decomposition itself does not assume a product target. Identifying this squared norm with entropy dissipation additionally uses the weak multiplier equation and the explicitly inherited minimum-field/duality domain. Testing that equation by φ supplies the required projection orthogonality.

A uniform conditional inequality KL ≤ C I/2 therefore gives D ≥ 2E/C. The reported exponential decay follows from the separately assumed entropy chain rule or differential energy inequality and local absolute continuity. A distributional PDE alone does not suffice; the author explicitly says so. Global convergence is conditional on a globally admissible solution. No non-Gaussian existence, uniqueness, or singular-entrance theorem has been proved.

The weak multiplier solve is coercive in the weighted H¹ norm because of its zeroth-order term. Conditional Jensen controls both right-side quantities. The constant function belongs to the cutoff closure for a probability marginal, so testing by it justifies the centred gauge. No observed-marginal Poincaré assumption is hidden in this argument.

## 2. Genuine non-Gaussian control

The dependent quartic example was rederived independently with symbolic, unrestricted a and δ=b−a. Under the current law, Y is Gaussian and e=z−by is independent with density proportional to exp(−e²/2−e⁴/4). Differentiation in y must hold z fixed; the independent checker uses ∂y−b∂e explicitly.

Integration by parts gives Mₙ₊₄=(n+1)Mₙ−Mₙ₊₂, hence M₄=1−c and M₆=4c−1. With A=1+3c, the report's conditional mean h, observed score m, and Hermite multiplier coefficients R₂ and R₄ are correct. In particular the −a terms from the target's observed score are indispensable.

The independent controls calculate the entire density generator Kμ(q−φ)/μ, average it conditionally, and obtain zero polynomial marginal drift. They also verify the full density entropy pairing E[q Kμ(q−φ)/μ]=D and all four dissipation terms. This goes beyond agreement of a few covariance moments. Omitting the target-score flux gives a nonzero residual; at a=δ=1 its y⁴ coefficient is −1.

The controls additionally derive

    E = δ²(6c + 3δ² + 2)/4,
    I = δ²(10−3c) + (6+45c)δ⁴ + 15δ⁶,
    I−2E = (9−6c)δ² + (9/2+45c)δ⁴ + 15δ⁶.

Since 0<c<1 by the positive quartic moments, the last expression independently verifies the claimed latent coercivity on this translated family. It is not a proof of the all-law LSI. The author correctly avoids claiming this translated-quartic family is invariant under its projected PDE.

The Cauchy-observed, sin(y)-translated quartic target has latent curvature at least one while its observed marginal has no Poincaré inequality. The stated rescaled odd-test argument verifies that failure directly. A joint LSI would imply an observed-marginal LSI and hence Poincaré, so the example genuinely avoids joint coercivity. Its smooth translated current states satisfy the declared finite-moment domain.

## 3. Scope controls checked

- Fixed target π=N(0,T), current N(n,1/n): separate innovation integration recovers E, Fisher information, and reaction variance. Exact limits give E/n²→1/(2T), D/n²→1/T², and D/E→2/T. Reaction is retained. The claim is instantaneous all-state sharpness for this product target, not an asymptotic trajectory exponent or sharpness for every dependent target.
- At b=1, s=11/10, the inherited full Gaussian flow gives h′(y)=169/2200−103y²/30. Its value at zero is positive and its observed average is −22153/6600. This proves the stated integrated-versus-per-fibre distinction. The added fibrewise comparator has the correct negative derivative and is properly restricted to its field-representation class.
- The logistic construction's transformed integrals give 1/2, ζ(2), and 2ζ(3). The Gaussian density envelope then yields the report's constants, including reaction. The target varies with T; this does not refute fixed-target coercivity or prove LSI necessary.
- Target-marginal mismatch leaves a fixed positive marginal KL residual. The final report correctly decays only excess conditional KL. Its extra coarse-potential domain condition is necessary to identify the full-KL projected fields, beyond merely using KL disintegration. An independent Gaussian mismatch computation verifies that adding the coarse log-ratio is annihilated by the projection. This scope paragraph was requested during review and then checked in its frozen form.

## 4. Ancestry and source bounds

The product-target transfer is already in the copied fixed-marginal predecessor §5, equation (16). The general conditional-score flux and weak resolvent are already in the copied correlated-target predecessor §3. Neither receives new-result credit here. The present report combines them for nonproduct conditional coercivity and supplies an explicit remainder and controls; this is a bounded local addition, not a literature-priority claim.

Independently accessed primary sources support the classical constants and ancestry:

- [Mielke–Zhu, arXiv:2501.17049v1](https://arxiv.org/html/2501.17049v1), Theorem 3.2 gives the curvature coefficient 2κ; Theorem 4.4 and Corollary 4.6 transfer Wasserstein coercivity to unconstrained SHK. They do not establish this entire-marginal constraint result.
- [Bakry–Émery, 1985](https://www.numdam.org/item/SPS_1985__19__177_0/), printed page 199 was visually checked in the preserved primary PDF render. Its curvature and entropy constants agree with the report's normalization. No whole-paper reread or independent reading of Gross's unavailable full text is claimed.

## 5. Verification and exclusions

`check.py` was independently written before reading the author's checker; it imports no author or root checker. Normal and optimized runs each pass **30 exact controls**, with explicit failure exceptions rather than optimization-removable assertions. `CHECKS.json` and `CHECKS_OPTIMIZED.json` record the results. Python 3 and SymPy are required. Portable replay:

    python3 check.py --output private-locator:459a60a2a37d7a790c17
    python3 -O check.py --output private-locator:9abd8e5f915725dbdf47

The frozen author checker was also rerun with originals and passed 47 checks; that is replay evidence, separately labelled from independent controls. The author manifest and five input bindings were checked against the live frozen bytes. `BINDINGS.json` records the reviewed identities.

No blocking mathematical finding remains at this digest. The checks establish only the named algebra and examples. The proof of the general transfer still rests on the stated functional inequality and inherited tangent-domain facts; the trajectory conclusion still rests on existence and energy-chain-rule assumptions. No formal-kernel proof, empirical/noetic target authentication, protected edit, or T20 closure follows.
