# Elementary polynomial linear-closure boundary

11 October 2026 UTC. Small root-proposed corollary, kept separate from the frozen ordered-control packet. Written proof only; not yet independently reviewed. No field-priority claim or new general closure theory.

Let P=R[x_1,…,x_d], d≥1, and let F be a nonconstant polynomial of degree D≥1. Define B_Fp=−∇F·∇p−Fp. Then for every nonzero p of degree k,

    deg(B_F p)=k+D.

Indeed, the derivative term has degree at most k+D−2 (or is zero), while −Fp has nonzero highest homogeneous component −F_D p_k of degree k+D, since the polynomial ring is an integral domain. Thus cancellation of the leading term is impossible.

Inductively, deg(B_F^n p)=k+nD. These iterates have distinct degrees and hence are linearly independent. Consequently P has no nonzero finite-dimensional B_F-invariant real linear subspace. In particular there is no finite polynomial observable space containing 1 with an exact closed **unnormalized linear** update under this generator on the unrestricted state domain.

This separates the finite-jet contraction in ordered-control-projective-transport-20261011/RESULT.md §3 from an exact finite linear-feature continuation. It neither rules out arbitrary nonlinear normalized coordinates nor contradicts known finite-support closure: functions on a fixed finite support satisfy polynomial relations, so the full-ring degree argument no longer applies there. It also does not rule out finite-dimensional restricted atomic-law manifolds or special nonpolynomial observables. The drift-only operator can have finite invariant polynomial spaces; the nonconstant killing term is essential to this particular degree proof. Constant F gives scalar B_F and is the excluded opposite case.

Bounded dedup: current top-level */RESULT.md and */REPORT.md files were searched for finite-dimensional/invariant polynomial-space, closure, degree-raising and leading-term phrases. Targeted followup inspected matching passages in measure-moment-continuation-boundary, tensor-realizability-extension, tensor-moment-continuation, general-coercive-energy-drift, joint-atomic-gradient-lift, and the pinned H-formalisation/H-Continuation sources. Those passages preserve finite-support and finite-state positive closure results and disclaim universal closure; no exact full-polynomial-ring invariant-subspace no-go was found in this bounded search. This is not exhaustive inherited or literature absence evidence. H-Continuation's finite-state invariant-span theorem is inherited; its finite-domain hypothesis is why that positive theorem remains unaffected.
