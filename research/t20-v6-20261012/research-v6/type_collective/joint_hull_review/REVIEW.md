# Independent review: joint-hull obstruction

Disposition: ACCEPTED as an ordinary source-derived synthesis corollary, with the ambient-score qualification now included in the reviewed report. This review claims no historical novelty and no new Lean replay.

## Exact mathematical checks

The six C vertices, twelve product vertices P, both positive weight lists and their common barycenter p are correct. Exact rational checks independently verify the two block projection sets, dimension four for each affine hull and for their joint span, the common tangent equations, transversality of h, and membership of all four product test truths. The product hull is genuinely larger: (1,1,0,0,1,1) belongs to P but violates x0≤x2, an inequality satisfied by every C vertex and hence by hull(C).

Intrinsic interior is justified without reversing a one-way library theorem. MixedHull supplies explicit coefficients for any tangent displacement d: (d0,0,d2−d0,d4−d0+d2+d3,−d4−d2,d0−d2−d3). They sum to zero and their centered weighted truth sum is d under the two tangent equations. Adding them to the strictly positive C weights keeps every weight positive for all sufficiently small tangent d, since these coefficients are continuous linear functions. Thus a relative neighborhood of p lies in hull(C). Since hull(C) is contained in hull(P) and their affine hulls coincide, the same neighborhood proves intrinsic interior for P. The positive P presentation is independently correct as well.

MixedGeometry identifies the full tangent space. MixedRepair proves actual hull-valued strict simultaneous Bregman improvement for every sufficiently small positive perturbation at every intrinsic-interior C context with transverse h. Here p0=p1=1/4, the high coordinates are all 1/2, and h0≠h1. The AND correction premises specialize to 0<s<1 and 2s<T<1+s with s=1/4 and T=1. Its polynomial positivity certificate is an explicit eight-cell Bernstein bound, fully inspected here.

ProductObstruction uses G at (0,0,1,1,0,0) and (0,0,0,0,1,1), and F at (1,1,1,1,0,0) and (1,1,0,0,1,1). All four are actual P truths. Its averaging identities add nonnegative high-coordinate spread to the two incompatible scalar bounds. IsolatedObstruction proves their incompatibility for 0<epsilon≤1/100 using the explicit envelope, strict endpoint-loss antitonicity and positive polynomial remainder. Every hull(P) output has first coordinates (q,q), 0≤q≤1. The theorem permits arbitrary real high coordinates, so its scope certainly includes every such output. It excludes even simultaneous weak improvement for the selected four tests, hence excludes the stronger full-family strict repair. Taking the minimum of the positive C neighborhood radius and 1/100 gives the claimed common interval.

## Logical meaning

The complete shared score functions are the ambient maps (v,c)↦G(v,c), F(v,c). The admissible truth-indexed collections of score instances differ, and those collections already encode the joint truth family. The revised report explicitly retains this distinction. Identical ambient functions imply identical derivatives at the shared context; the counterexample does not depend only on matching finitely many derivatives.

A rule receiving only the stated compressed inputs receives identical data on the two instances but the local feasibility property has opposite values. That proves failure of decision factorization on any class containing both. It does not prove that the whole joint hull is a uniquely minimal representation, that all moments are necessary, or that an actual cognitive system implements the example. The noetic/source-support connection is a conditional transport test, not an empirical or metaphysical conclusion.

The finite LP diagnostic values are unnecessary for this derivation and were not independently recomputed in this review. The exact rational check is confined to finite geometry and membership; the nonlinear conclusion follows from independently inspected proof bodies.

## Evidence

REVIEW.json records exact reviewed-report and source hashes and complete read ranges for ten original Lean modules (1,187 lines). EXACT_GEOMETRY.json and exact_geometry.py retain the fresh rational checks. Root's separate compilation receipts, when available, control kernel assurance; this review does not infer compilation from source inspection.
