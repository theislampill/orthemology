# Independent ordinary review of the mixed rank example

## Literal geometry

The six frozen vertices are Boolean. Their last four coordinates are exactly all six weight-two Boolean vectors, and their first two coordinates duplicate the AND of the first two high coordinates. The difference matrix has rank 4. Every vertex satisfies x1=x2 and x3+x4+x5+x6=2; those two independent affine equations therefore give the full affine hull.

The tangent space is the direct sum of the duplicate pair and the four-coordinate sum-zero space. Its elementary supports are the duplicate pair and every pair of distinct high coordinates. No singleton tangent support exists. These give exactly rank-one and rank-three blocks. The rank-three score-curvature ratio is the single constant 100, so the higher-rank scale requirement is respected rather than bypassed.

The hull is not the product of its projections: for example (1,1,0,0,1,1) belongs to the product, but violates x3>=x1, an inequality valid at every listed coupled vertex. Both projected hulls and the affine tangent data still coincide.

## All contexts and directions

Choose any p in the relative interior. The finite-hull positive-barycentric fact supplies positive weights alpha0,...,alpha5 on all six listed vertices. Write p=(s,s,z,w,u,v). Direct reconstruction gives:

- s=alpha0>0
- z-s=alpha1+alpha2>0
- w-s=alpha3+alpha4>0
- T-2s=alpha1+alpha2+alpha3+alpha4>0
- 1+s-T=alpha5>0

Thus the already verified polynomial margin inequality applies at every such context. The common projection subtracts the high-block mean kappa from all four high direction coordinates and averages the duplicated pair. A direction is transverse exactly when e+E_H>0, where e=(h1-h2)^2/4 and E_H=2*kappa^2.

The author's correction (beta,beta,gamma/2,gamma/2,-gamma/2,-gamma/2) lies in the tangent space. Exact symbolic expansion against all six actual vertices gives the old polynomial AND leading coefficients plus E_H under G and plus 100E_H under F. Twelve identities were checked without substituting favorable contexts or directions.

If e>0 the old strict margin applies. If e=0, beta=gamma=0, and the actual score gains are exactly 2*kappa^2*epsilon^2 and 200*kappa^2*epsilon^2 at every truth, even with arbitrary tangent components of h. This important family is covered: it is not silently excluded by borrowing the original h1!=h2 hypothesis. Twelve separate exact identities check this case.

Finite polynomial remainders and finitely many truths then give a positive context/direction-dependent common epsilon radius. The baseline starts inside the open cube: positive weights on all vertices make every Boolean coordinate strictly between zero and one. There is no uniform radius or boundary-context assertion.

## Constructive admissibility

The relative-interior argument is sound, and a concrete barycentric right inverse makes it explicit. For a tangent displacement d=(ds,ds,dz,dw,du,dv), with dz+dw+du+dv=0, change the six initial weights by

    (ds, 0, dz-ds, du-ds+dz+dw, -du-dz, ds-dz-dw).

The changes sum to zero and reconstruct d exactly. Apply this separately to the candidate's epsilon and epsilon-squared coefficient vectors. Initial weights are all positive; their finite polynomial perturbations remain positive for sufficiently small epsilon. This certifies membership in the actual six-vertex hull, not only satisfaction of its affine equations.

The independent tests use this right inverse for 82 positive barycentric weight configurations and six directions. All 492 cases have exact positive weights, exact reconstruction, open-cube baselines and all 12 strict score comparisons. Of these, 164 have e=0 and E_H>0. The concrete test search is bounded and supplementary; the universal radius is proved by the positive-leading-coefficient/continuity argument.

## Product contrast

The initial draft's suggestion to hold a high-block truth at an interior baseline was invalid as stated. The frozen v2 text correctly replaces it with barycentric averaging. At any interior high-block baseline p_H, choose weights on the six high truths with that barycenter. Perturb only the duplicate block. For any coherent product candidate c_H, the expected high-block gain equals -D_H(p_H,c_H), which is nonpositive under each score. Hence all product truth comparisons force the corresponding isolated duplicate-block inequalities at each of its two endpoints. The verified isolated obstruction at s=1/4 rules these out for every sufficiently small positive epsilon.

For p_H=(1/2,1/2,1/2,1/2), uniform weights on the six high truths give an especially transparent exact identity: averaged quadratic high gain is minus one-half the squared distance from c_H to p_H; nonlinear high gain is 100 times this. The independent symbolic test checks that identity.

Therefore the coupled and product hulls have identical affine hull, block ranks, projected hulls, generators and common Hessian projection fields, but opposite universal local exact-repair answers. No free singleton coordinate is needed for the rescue. The ordinary proof passes after the product-comparison correction. This audit does not promote the mixed-rank example to a kernel theorem.
