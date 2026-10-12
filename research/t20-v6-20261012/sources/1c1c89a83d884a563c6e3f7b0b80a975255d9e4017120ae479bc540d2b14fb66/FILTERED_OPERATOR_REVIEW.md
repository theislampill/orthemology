# Separate review: filtered-operator obstruction

10 October 2026 UTC. Bounded independent review of heat-truncated-certificate-diagnostic-20261010/FILTERED_OPERATOR_NOTE.md, final SHA-256 b75bc63ffa43907f816e535603e5a724134e54f1ef7dab69f394bd269e252484. The initial reviewed version had SHA-256 5d3b74f7e30e3a5535a54a0e6eed527de62afcd0bbdd814bb646dee6a212ddd4; the final version only makes the linearity premise explicit. Both versions were read. The preceding four reviewed conclusions and their receipt are unchanged.

## Verdict

PASS under the final note's explicit linear-operator premise: T and N are real linear endomorphisms of the stated finite-dimensional polynomial space. The main claim, Gaussian Gram proof of SOS closedness, nonzero averaging-kernel corollary, and dual strict-square-positive countercertificate are sound. The wording recommendation to make linearity explicit has been incorporated.

## Checks

1. Let V_k denote the homogeneous degree-k subspace. A degree-lowering linear N has components N_jk only for j<k, and N^(2d+1)=0. D_a multiplies V_k by a^k. Hence the conjugated component from V_k to V_j is exactly a^(k−j)N_jk. Every exponent is positive, so D_(1/a)TD_a tends to mI as a decreases to zero. This is a finite sum in a finite-dimensional operator space, with no hidden limit interchange.

2. Spatial dilation and its inverse preserve both global nonnegativity and SOS. If T(P) were contained in S, each conjugate would therefore send P into S. Closedness would imply mf∈S for every f∈P. Since m>0 and S is a cone, this would imply P=S, contrary to the premise.

3. The stated closedness proof is valid. For a nondegenerate Gaussian and the degree-at-most-d monomial vector v, H=∫vvᵀdγ is positive definite because every nonzero polynomial has positive squared Gaussian integral. If Q_k is a positive semidefinite Gram matrix of p_k, then trace(HQ_k)=∫p_kdγ. The latter is bounded for coefficientwise convergent p_k, because this integral is a fixed linear functional on V. If λ is the smallest eigenvalue of H, then λ trace(Q_k)≤trace(HQ_k). Bounded trace bounds each Q_k in finite-dimensional matrix norm. A convergent subsequence consequently has a positive semidefinite limit whose polynomial is the limit of p_k. This does not assume a general closed-image theorem for the positive semidefinite cone.

4. For convolution with a positive measure of nonzero finite mass m and finite moments through degree 2d, the polynomial Taylor formula has leading term mf. Every remaining term involves a derivative of positive order and has lower degree. Thus the convolution operator indeed has the form mI+N, regardless of the sign convention for translation. The zero measure is correctly excluded.

5. Nilpotence makes T invertible, with the finite inverse m^(-1)Σ_r(−N/m)^r. The established failure of inclusion supplies an f∈P with Tf∉S. Finite-dimensional separation of the point Tf from the closed convex cone S supplies Λ≥0 on S with Λ(Tf)<0. Gaussian integration G is strictly positive on every nonzero member of S. For sufficiently small ε>0, Λ+εG remains negative on Tf and is strictly positive on S\{0}. This reasoning does not require Tf itself to be pointwise nonnegative.

6. With Λ replaced by that strict perturbation and L=Λ∘T, one has L∘T^(-1)=Λ, but L(f)<0 for the globally nonnegative f. A positive representing measure for L is therefore impossible. The argument is entirely truncated and does not assert that Λ or L extends to a square-positive full polynomial functional.

## Scope retained

This is an ordinary universal proof check, not a new numerical or source-research campaign. No general algorithm for separation is provided. The result concerns one fixed scalar-leading filtered operator acting on the entire bounded-degree cone. It does not rule out polynomial-dependent transformations, suitably restricted families, or whole-path conclusions for degree-raising coercive killing. No field-priority, formal-kernel, protected-edit, or T20-closure claim is added.

A useful hypothesis control is the Gaussian averaging projection R(p)=(∫p dγ)·1. This linear positive operator sends every globally nonnegative polynomial to a nonnegative constant, which is SOS. It is outside the theorem: its associated graded action is zero on every positive degree, whereas mI+N has the nonzero scalar action mI at every grade. Equivalently, R−mI cannot strictly lower degree for m>0. Thus the no-go statement is not a claim against all positive linear operators or every information-losing repair.
