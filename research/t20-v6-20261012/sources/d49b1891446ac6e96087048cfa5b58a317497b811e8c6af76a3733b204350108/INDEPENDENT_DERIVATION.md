# Independent mathematical derivation: finite moment and continuation bridge

9 October 2026 UTC. Ordinary mathematical review only. This is a derivation and executable-control record, not an audit, source-currentness certification, or lifecycle decision. The derivation was completed before reading the tensor author's proof.

## Declared model

After merging duplicate channel columns, let the known fixed support be distinct points \(k_1,\ldots,k_N\in\Delta_m\), with positive normalized aggregate weights \(a_j\). Let the same numerical control \(g(t)\in\mathbb R^m\) be applied to the compared states. Piecewise-constant controls should have finitely many switches on every bounded time interval; more generally local integrability suffices. Put

\[
q=\sum_jw_jk_j,\qquad
\dot w_j=-w_j(g\cdot k_j-g\cdot q).
\]

For \(G(t)=\int_0^tg(s)\,ds\), direct differentiation gives the unique normalized solution

\[
w_j(t)=\frac{a_j e^{-G(t)\cdot k_j}}{\sum_i a_i e^{-G(t)\cdot k_i}}.
\]

Its weights remain positive at every finite time for which \(G\) is finite. At control jumps the moment equations hold on each constant-control interval and almost everywhere, rather than asserting a two-sided classical derivative at the jump. Duplicate-column group weights obey this same equation, whereas the ratios of the fine weights inside each duplicate group remain constant and invisible to \(q\).

## 1. Exact tensor hierarchy and finite closure

Define \(M_r=\sum_jw_jk_j^{\otimes r}\), including \(M_0=1\). For a fixed covector \(g\), write \(\iota_g\) for contraction of the final factor. Termwise differentiation gives

\[
\dot M_r=-\iota_gM_{r+1}+(g\cdot M_1)M_r.
\]

The equation at \(r=0\) gives zero, as required. This is a tensor equation at a given control; it is not obtained by repeatedly differentiating \(q\), which would require accounting for derivatives of a varying control.

Choose \(v\) outside the finitely many hyperplanes \(v\cdot(k_i-k_j)=0\). Then \(\lambda_j=v\cdot k_j\) are distinct. The directional moments

\[
z_r=\langle M_r,v^{\otimes r}\rangle=\sum_jw_j\lambda_j^r,
\quad 0\le r\le N-1,
\]

satisfy \(z=Vw\) for the invertible Vandermonde matrix \(V_{rj}=\lambda_j^r\). Thus \(w=V^{-1}z\). Equivalently, the Lagrange polynomials

\[
L_j(x)=\prod_{i\ne j}\frac{x-\lambda_i}{\lambda_j-\lambda_i}
       =\sum_{r=0}^{N-1}c_{jr}x^r
\]

give \(w_j=\sum_rc_{jr}z_r\). Every tensor of every order is consequently a fixed linear function of \((M_0,\ldots,M_{N-1})\): first recover \(z\), then \(w\), then \(\sum_jw_jk_j^{\otimes r}\). In particular \(M_N\) has this linear closure, closing the displayed hierarchy at degree \(N-1\).

The finite evolution is nonlinear, generally quadratic in its moment state, because of the normalization term \((g\cdot M_1)M_r\). On the admissible moment image it is conjugate to the positive-weight dynamics. An arbitrary point in the ambient tensor space need not encode valid weights, and no global claim about such extraneous initial states is needed.

For \(N=1\), \(M_0=1\) alone is sufficient because the single known support vector reconstructs all higher tensors; there is no dynamical weight freedom. For larger \(N\), degree \(N-1\) is a universal sufficient bound, not always the smallest available degree for a particular support.

The full sequence lies in \(\prod_{r\ge0}\operatorname{Sym}^r(\mathbb R^m)\). Indeed, contracting \(M_r\) against \(\mathbf1^{\otimes r}\) gives 1 at every degree, so the sequence has no finite degree support. The finite tuple lies in the finite graded direct sum through degree \(N-1\), or its admissible affine image. The latter representation can be placed in a declared tensor algebra, but this does not identify the infinite sequence with an element of the algebraic direct sum or turn the complete dynamics into a linear degree-lowering operator.

## 2. Exact continuation equivalence

Fix the support, the initial time, and the control repertoire. Define continuation equivalence by equality of all future \(q\)-records under every common admissible control. Equal aggregate weights imply equal records by the explicit solution.

Conversely, use the one constant control \(g=v\) chosen above. For initial weights \(a\), put

\[
Z_a(t)=\sum_ja_j e^{-\lambda_jt},\qquad
h_a(t)=v\cdot q_a(t)=-\frac{d}{dt}\log Z_a(t).
\]

If two scalar records agree on any interval with positive duration, then \(Z_a=CZ_b\) on that interval for some \(C>0\). Choose an interior time \(t_0\). Differentiating this equality for orders \(0,\ldots,N-1\) gives

\[
\sum_j(a_j-Cb_j)e^{-\lambda_jt_0}(-\lambda_j)^r=0,
\quad 0\le r\le N-1.
\]

The coefficient matrix is a Vandermonde matrix times invertible diagonal matrices. Hence \(a_j=Cb_j\) for every \(j\); normalization gives \(C=1\). This proof covers observation intervals strictly after zero without an analytic-continuation assumption. It presumes the records are compared at the same time parameter; allowing an unknown time translation introduces a different observational problem.

Therefore continuation equivalence is exactly equality of aggregate weights at identical known support points. One separating constant-control scalar record already determines that equivalence class. The result identifies the model's aggregate weights. It does not identify distinctions between duplicated fine labels, actual source identity, truth, or any unmodelled variable.

## 3. When the first moment alone descends

Let \(\mathcal L\subseteq\mathbb R^N\) be the evaluation space of affine functions on the distinct support. It contains constants and separates every pair of support points. For all controls, the instantaneous projected field is

\[
\dot q=-(M_2-qq^T)g.
\]

If it is constant on every positive-weight fibre of \(q\), consider any signed perturbation \(d\) with \(\sum_jd_j=0\) and \(\sum_jd_jk_j=0\). Perturb a strictly positive reference weight by sufficiently small multiples of \(d\). Fibre constancy for every \(g\) yields

\[
\sum_jd_j k_jk_j^T=0.
\]

Thus every quadratic coordinate product, evaluated on the support, annihilates \(\mathcal L^\perp\) and belongs to \(\mathcal L\). Products of two affine functions therefore lie in \(\mathcal L\): it is a unital subalgebra. The separating linear function \(v\cdot k_j=\lambda_j\) lies in this algebra, as do its powers through degree \(N-1\). Vandermonde invertibility implies \(\mathcal L=\mathbb R^N\). This is precisely affine independence of the support.

Conversely, affine independence makes \(q\) determine all aggregate weights, and therefore \(M_2\), so the field descends. This includes \(N=1\). Duplicate columns must be merged before counting affine independence. The universal quantifiers over all positive weights and all controls are essential; a restricted control can have a descended field on an affinely dependent support.

## 4. Independent negative and positive controls

The independent script contains 38 exact groups.

1. **Beyond a covariance-only check.** Let \(k_j=(j/3,1-j/3)\), \(0\le j\le3\), and let
   \[
   a=(1/4,1/4,1/4,1/4),\quad
   b=a+(-1,3,-3,1)/24=(5/24,3/8,1/8,7/24).
   \]
   Both weights are strictly positive and normalized. All full tensors through degree 2 agree, but the first-coordinate third moment differs by \(1/108\). Under \(g=(1,0)\), \(q\) and \(\dot q\) initially agree while the first coordinate of \(\ddot q\) differs by \(1/108\). Thus retaining covariance does not universally finish the hierarchy.

2. **Sharpness as a universal degree bound.** On \(N\) collinear support points \(k_j=(j/(N-1),1-j/(N-1))\), the signed finite-difference weights \(d_j=(-1)^{N-1-j}\binom{N-1}{j}\) annihilate every polynomial of degree below \(N-1\), but not the degree-\(N-1\) monomial. Small perturbations of uniform weights remain positive. Full moments through degree \(N-2\) therefore need not suffice. The annihilation is the identity that the \(N-1\)-st forward difference vanishes on lower-degree polynomials and equals \((N-1)!\) on the leading monomial before the node rescaling. The script checks \(N=2,\ldots,7\); the identity supplies the general statement.

3. **Nonseparating controls.** For \(g=\mathbf1\), every support projection is 1 and every weight remains fixed. Distinct weights with the same initial \(q\) remain indistinguishable under this restricted repertoire. The scalar response is constant for every weight.

4. **Duplicate labels.** With repeated columns, different positive fine weights can have identical group sums and every tensor and continuation record remains identical. The theorem cannot recover their split.

5. **Noisy support with a descended field.** For two binary columns at first coordinates \(1/4\) and \(3/4\), the mean \(x\) determines the weights. Its mobility is \((x-1/4)(3/4-x)\), although the canonical binary Fisher mobility is \(x(1-x)\). Hence field descent is broader than the deterministic-channel canonical-Fisher identity.

6. **Known-support limitation.** With probe \(v=(0,1,2)\), the support pairs \(((1,0,0),(0,1,0))\) and \(((1,0,0),(1/2,0,1/2))\) have the same distinct scalar projections \((0,1)\). Equal weights produce the same entire scalar controlled response, while their vector responses differ. Without fixed known vector support, this selected scalar record does not identify the support vectors. This countercontrol does not concern full vector observations under all real controls, which form a stronger observation contract.

The script also checks exact tensor reconstruction through degree 6, hierarchy identities through degree 4, the positive-time tilted Vandermonde, the \(N=1\) case, and exact composition of normalized exponential tilts. These finite checks supplement the general proof, and do not establish a noisy-data reconstruction guarantee.

## Boundaries

This is an exact finite-support model theorem. No claim is made about unknown support recovery, finite-precision reliability, numerical conditioning, observation cost, practical availability of the control, actual sensing, field-wide novelty, cognitive realization, or metaphysical warrant. The inherited source already supplies general fibre and future-safe quotient criteria. The added content here is the explicit controlled-moment realization, the finite known-support sufficient representation, and the exact continuation equivalence for this model.
