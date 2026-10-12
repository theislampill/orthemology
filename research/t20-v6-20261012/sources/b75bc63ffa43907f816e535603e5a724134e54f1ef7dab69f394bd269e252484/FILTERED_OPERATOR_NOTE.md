# A graded obstruction to a universal square-positivity repair

10 October 2026 UTC. Root-derived ordinary algebraic consequence of the heat comparison. This note is additive to the frozen explicit diagnostic. It claims no literature-wide novelty and no empirical or metaphysical application.

Let V be the real polynomials in n variables of degree at most 2d. Let P be its cone of globally nonnegative polynomials and S its sum-of-squares cone. Assume P strictly contains S. The finite-dimensional cone S is closed; both cones are invariant under every invertible positive spatial dilation D_a f(x)=f(ax). To check closedness without assuming that every linear image of a closed cone is closed, use the degree≤d monomial vector v and a Gaussian moment matrix H=∫vvᵀdγ≻0. For coefficientwise convergent SOS polynomials p_k=vᵀQ_kv with Q_k≽0, trace(HQ_k)=∫p_kdγ is bounded. Hence the Q_k are bounded and have a positive-semidefinite convergent subsequence representing the limit. No general closed-image claim is needed.

**Claim.** Let T:V→V be linear. If T=mI+N with m>0 and N strictly lowers polynomial degree, then T cannot send all of P into S.

**Proof.** Decompose V by homogeneous degree. The component N_jk from degree k to degree j vanishes unless j<k. Consequently

    D_(1/a) T D_a = mI + Σ_(j<k) a^(k−j) N_jk → mI

as a↓0 in the finite-dimensional operator topology. If T(P)⊆S, then for every f∈P every D_(1/a)TD_af belongs to S. Closedness yields mf∈S, hence f∈S. This contradicts P≠S. ∎

This is a statement about the associated graded action of the operator. It does not merely compare terminology across subjects: the homogeneous filtration, the dilation conjugation, both cones and the closed-cone limit are the exact preserved structures used by the proof.

## Consequences and exact limits

1. Fixed positive heat time is a special case: exp(tΔ)=I+N, with N strictly degree lowering on V.
2. Any fixed convolution by a positive measure of nonzero finite mass m, with moments through degree 2d, has the form mI+N. Taylor expansion of f(x+y) shows that all terms involving a nonzero power of y lower the degree in x. Hence no such fixed averaging kernel can turn every globally nonnegative member of V into a sum of squares when P≠S. The all-zero kernel is excluded by m>0.
3. T is invertible because m>0 and N is nilpotent. There also cannot be a universal truncated representation certificate of the form “L∘T^(-1) is strictly square-positive, therefore L has a positive representing measure.” Indeed choose f∈P with Tf∉S. Separation from the closed cone S gives a functional Λ nonnegative on S with Λ(Tf)<0. Add a sufficiently small positive multiple of Gaussian integration: this makes Λ strictly positive on every nonzero member of S while retaining Λ(Tf)<0. Set L=Λ∘T. Then L∘T^(-1)=Λ is strictly square-positive but L(f)<0, so L has no positive representing measure.

The last argument is an existence proof using finite-dimensional separation. The accompanying ternary-quartic diagnostic gives a fully explicit rational example for heat, with a 10×10 positive-definite square matrix and a nonnegative polynomial of strictly negative value. No general separation algorithm is implemented here.

The obstruction concerns a fixed operator required to work on the entire cone. It does not prohibit data-dependent transformations, restricted normalized families with additional conditions, individual polynomials becoming SOS, or the successful coercive-killing hierarchy results. Those kill dynamics raise degree on polynomial observables and impose whole-path constraints; they are not a single degree-lowering preconditioner on this truncated space.
