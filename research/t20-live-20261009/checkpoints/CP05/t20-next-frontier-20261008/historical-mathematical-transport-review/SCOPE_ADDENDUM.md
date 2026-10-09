# Governing scope qualification for the frozen historical transport

This addendum qualifies the Proposition 6 paraphrase in `historical-mathematical-transport/ANALYSIS.md`, SHA-256 `c70ade3f34431728761e0f1e0c3493823b43703120a45c85c096fea1064f235c`, line 24. The frozen author bytes are unchanged. Read the following qualification together with the review verdict.

The exact sentences qualified are: "It identifies D as the record-kernel directions supported on the union of feasible supports." and "Only with a full-support feasible law may one replace D by the entire kernel of A."

For any linear record A on a finite signed-law space, with nonempty probability fibre M and S the union of its feasible supports, the generally valid identity is

    D = span(M-M)
      = ker(A) intersect {d: sum_x d(x)=0}
               intersect {d: d(x)=0 for x outside S}.

The archived Proposition 6 explicitly assumes that A retains total mass: ker(A) is contained in the mass-zero subspace. Under that assumption, the mass-zero condition is redundant. A full-support feasible law makes the support condition redundant. With both conditions, D=ker(A), and constant output law is equivalent to ker(A) being contained in ker(T).

Full support is a sufficient way to remove the support restriction, not a logically necessary condition for D=ker(A). Without it, that simplification is still valid if every kernel direction already vanishes outside S and has mass zero; otherwise use the displayed intersection.

The transport's actual application in ANALYSIS.md lines 99-104 meets the archived hypotheses: its record has a row of ones, and (1/4,1/4,1/2) is a full-support feasible law. No conclusion or numerical value in that application changes.

Negative control: on two input states, let A=0 and let T=(1,1) reset every input to the same single output. M is the whole probability simplex and contains full-support laws. Every probability input has the same output, but ker(A) is the whole two-dimensional signed-law space and T does not annihilate it. D is only the mass-zero line. Thus the unrestricted paraphrase must not be used without this mass qualification.

This is a review-side scope correction, not an edit to the author artifact, a new scientific theorem, or acceptance/integration authority.
