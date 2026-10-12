# Independent review: moving-objective order interface

10 October 2026 UTC. Separate ordinary mathematical review. No kernel theorem, external peer-review status, protected integration, empirical cognitive validation, or programme closure is claimed.

## Verdict and source binding

**Accepted as scoped. No correction is required.** The physical/observable order, sign, normalization, local remainder, arbitrary-dimension formula, and higher-order limitations are correct.

Reviewed author directory: `moving-objective-order-interface-20261010`.

- `RESULT.md`: SHA-256 `876e433d5340f1c25eec7a3a6e911b0d36e44a4875feb90b0bebbb329918346d`.
- `check.py`: SHA-256 `e8a7281115306f2ec9f5f5fb555fa0fcd5f39465b199f20ad90f47633bb99a43`.
- `INPUT_BINDINGS.json`: SHA-256 `b27624ca731d2436d7ff264988acd29c1632cc6697cce57e705646291ccac518`.

`FROZEN_AUTHOR_INPUTS.json` binds these files, the frozen author manifest, and the author check output. The four inherited hashes all match their source files; exact copies are in `predecessors/`. The author and predecessor files were not changed by this reviewer.

## 1. Physical order and generator sign

Let L_F(t) act on finite measures by weighted pushforward under the F-gradient flow. Its dual observable operator is precisely T_F(t):

    (L_F(t)μ)(p)=μ(T_F(t)p).

For physical F followed by G, the measure operator is L_G(t)L_F(t), whose observable pullback is T_F(t)T_G(t). Thus the author's displayed observable order is correct; reversing it would reverse the claimed bracket sign. The derivative of the characteristic expression is B_F=−∇F·∇−F. No additional Jacobian belongs in this test-function identity, whether μ is discrete, singular, or has a density.

The exact shifted-quadratic discriminator independently fixes the sign. If q=e^(−t), the F flow is x↦qx and the G flow is x↦qx+a(1−q). Their physical compositions differ by +a(1−q)². For a>0 this is a positive spatial displacement. In one dimension Hess(G)F'−Hess(F)G'=x−(x−a)=a, so the bracket prediction agrees. Normalization leaves each evolving Dirac measure concentrated at its actual endpoint.

## 2. Dimension-free commutator

For general first-order operators U=b·∇+f and V=c·∇+g, the product rule gives

    [U,V]p = Σ_j [Σ_i(b_i ∂_i c_j−c_i ∂_i b_j)] ∂_j p
               +(b·∇g−c·∇f)p.

The second-derivative terms cancel because ∂_i∂_j p is symmetric, and the additional first-derivative multiplication terms cancel pairwise. This calculation is valid for every finite dimension; no specifically two-dimensional fact is used.

Putting b=−∇F, c=−∇G, f=−F and g=−G gives the stated transport vector Hess(G)∇F−Hess(F)∇G. The scalar term is ∇F·∇G−∇G·∇F=0. Therefore [B_F,B_G]1=0. Independent symbolic checks repeat the arbitrary-function identity in three dimensions and verify the general one-dimensional independently chosen drift/killing formula. These supplement the dimension-free written proof rather than proving arbitrary dimension by testing a few dimensions.

Adding arbitrary constants to F and G changes each operator only by a scalar multiple of the identity, which commutes. A separate control verifies that the bracket is unchanged, consistent with the normalized dynamics' energy-shift gauge.

## 3. Projective normalization

Each unnormalized stage is linear and homogeneous in its input measure. Dividing the first-stage output by its mass therefore multiplies both the second-stage numerator and mass by the same positive constant. Intermediate normalization cancels exactly. It is not an approximation and does not assume equal stage masses.

Write the two unnormalized observable numerators as N_FG and N_GF and their masses as D_FG and D_GF. Operator expansion gives

    N_FG−N_GF = t² μ([B_F,B_G]p)+O(t³),
    D_FG−D_GF = t² μ([B_F,B_G]1)+O(t³)=O(t³).

Both masses equal 1+O(t), so are bounded away from zero near t=0. Dividing changes the displayed t² coefficient only by O(t³); the possible third-order denominator mismatch is itself an O(t³) contribution. Consequently no missing covariance, subtraction of μ(p), or derivative-of-normalization term is needed at the displayed order. For a general drift/killing commutator with nonzero value on 1, such a subtraction would be necessary, which is why the gradient cancellation matters.

Independent checks verify exact cancellation of an intermediate normalization with unequal positive weights and stage factors, and verify the quotient coefficient even when the two denominators have unrelated third-order coefficients. The author's simpler common-denominator check is valid but does not itself exercise this last distinction.

## 4. Compact-uniform local expansion

The proposition deliberately assumes compact initial support and polynomial objectives/observable, or sufficient smoothness for the stated expansions. A sufficiently small common interval places all first-stage and two-stage characteristic images in a compact neighborhood. Smooth local ODE dependence then makes the two-time characteristic observable

    (s,t,x) ↦ T_F(s)T_G(t)p(x)

three times continuously differentiable on a compact parameter/support set, with bounded third derivatives. Multivariate Taylor expansion has uniform remainder O((s+t)³); restricting to s=t gives O(t³). Its coefficients are the stated B_F, B_G, B_F², B_G², and B_FB_G terms. The reversed protocol is treated identically.

This argument justifies the product expansion directly without applying differential operators to an uncontrolled remainder. Uniform remainders integrate against the compactly supported probability, and positivity of the bounded characteristic weights gives finite strictly positive normalizers. The argument requires neither a density for μ nor a formal power series with unspecified convergence.

Forward completeness of coercive-polynomial gradients is adequate for the global quadratic example but is not needed for the local proposition. Conversely, no arbitrary-law, infinite-moment, uniform-in-support, or total-variation expansion follows from this proof. The source does not assert one. In particular, a moving Dirac law generally does not have a total-variation derivative, which the report expressly excludes.

## 5. Higher-order limitation: direct dynamic verification

The source's nested commutator is correct:

    [−x∂_x−x²/2, a∂_x] = a∂_x+ax.

It does not annihilate 1 when a≠0. Thus the class of pure-transport first commutators does not remain pure transport under further commutation with B_F.

An independent exact finite-protocol calculation strengthens this scope check. For the same F=x²/2 and G=(x−a)²/2 and q=e^(−t), the integrated killing costs from initial z are

    K_FG(z)=(1−q²)[z²+(qz−a)²]/4,
    K_GF(z)=(1−q²)[(z−a)²+(qz+a(1−q))²]/4.

Their difference is

    K_FG−K_GF = −a(2z−a)(q−1)³(q+1)/4
             = a(2z−a)t³/2+O(t⁴).

This depends on z, so normalization does not remove it for a general multi-atom law. For the concrete compact law μ=(δ_0+2δ_2)/3 and a=1, independent exact derivatives of the full characteristic expressions give:

- For p(x)=x², the normalized physical observable difference has coefficient (8/3)t², exactly μ(a p')t².
- The two protocols' unnormalized masses agree through degree two.
- The normalized weight of the label initially at 2 agrees through degree two, but its F-then-G minus G-then-F difference is −(4/9)t³+O(t⁴).

These controls include genuinely unequal masses and nontrivial killing, unlike a Dirac-only example. They demonstrate why the first-order-operator commutator cancellation does not justify removing reweighting from finite or higher-order protocols.

Vanishing of the displayed coefficient for a particular μ and p does not imply order-neutral laws. Identically vanishing commutators have stronger local implications under appropriate regularity/domain conditions, but the source appropriately does not infer a global commutation theorem merely from a second-order truncation.

## 6. Inheritance and interpretation

The bound pure-reweighting result explicitly retains a fixed state variable and uses the weight exp(−Σ_j t_j h_j). Fixed functions and their durations commute under this multiplication, so the reported order neutrality follows directly there. Introducing characteristic transport changes the composition rule. The shifted-quadratic example therefore defeats an attempted transfer of the old conclusion to a stronger mechanism; it does not contradict or repair an error in the pure-tilt theorem itself.

The atomic-geometry ancestor supplies the matching gradient/killing equations. The general energy-drift ancestor supplies a broader represented characteristic setting under its own assumptions; none of its reverse-representation hypotheses is silently removed here. The new local calculation starts with a supplied compactly supported probability. The complete-experiment ancestor concerns observation about a fixed latent target, including omitted outcomes; moving the states in the present dynamics supplies no such observation model. Those inherited distinctions remain intact.

The report makes no claim that order sensitivity is beneficial correction, manipulation, epistemic warrant, a cognitive implementation, or a new field-wide theorem. Its programme-level contribution is a bounded interface correction about which mathematical structure survives a change of mechanism. The stated boundaries are appropriate.

## 7. Executed controls and portability

The unmodified author checker passes all seven separately named exact controls. It does not itself validate the four predecessor hashes; that verification is supplied by this review. The author manifest records an initial syntax typo corrected before its successful frozen run. This review concerns only the final hash-bound version. The reviewer's initial checker also had an unmatched parenthesis corrected before its successful runs; no source theorem or author file changed.

`check_independent.py` passes 38 checks:

- 21 exact mathematical controls.
- Five current-author file hashes and five snapshot hashes.
- Four predecessor-copy hashes.
- Two author-replay checks.
- One count audit confirming seven distinct executed author controls.

`INDEPENDENT_CHECKS.json` lists each check. `AUTHOR_REPLAY.log` and the snapshot output preserve the author replay. These controls support the written proof and do not constitute a formal-kernel proof or exhaustive theorem verification by examples.

For replay, place the unchanged author and review directories as siblings and run:

    python moving-objective-order-independent-review-20261010/check_independent.py

All predecessor copies are included under the review directory and checked against the unchanged relative input bindings. There are no absolute ancestor paths to rewrite. `REVIEW_RECEIPT.json` binds all final review artifacts. No author or predecessor changes, protected integration, or closure decision is authorized by this verdict.
