# A regular exact-success comparator with the same zero LP

Independent constructive audit addition, 2026-10-01. Ordinary proof; no new kernel theorem or novelty claim.

The odds-ratio exact-success example has endpoint-singular curvature, whereas the general second-order theorem assumes C3 positive-Hessian potentials on an open neighborhood containing the full hull. The following entire analytic potential removes that mismatch.

Let psi_plus(t)=exp(4(t-1/2))/16. Then psi_plus''(t)=r_plus(t)=exp(4(t-1/2))>0 everywhere. On the duplicate-coordinate line, use F_plus=psi_plus(x1)+psi_plus(x2) and G=(x1^2+x2^2)/2. At the context s=1/2 and ray h=(1,0), r_plus(s)=1 and r_plus'(s)=4. Thus the common first-order projection is (1/2,1/2), and the exact second-order score-gain rows in correction b are precisely:

    G0: 1/4-b
    G1: 1/4+b
    F0: 3/4-b
    F1: b-1/4

At b=1/4 all rows are nonnegative; averaging the first and fourth gives zero for every b, so the optimum is exactly zero. These are the same LP data as the polynomial CriticalZero failure example.

Nevertheless log r_plus has derivative 4 at every s. On 0<s<1,

    4 <= 1/[s(1-s)]

because 1-4s(1-s)=(2s-1)^2>=0. The pairwise isolated rank-one exact-repair criterion is therefore satisfied throughout the coherent segment. The reviewed generalized-mean comparison proof supplies a common weak coherent repair for every forecast tuple in the open attained box, hence for all sufficiently small perturbations of the specified context. All potentials are globally smooth and strictly convex, including around both truth endpoints.

Consequently even within the full endpoint-regular hypotheses of the second-order variational theorem, identical zero-margin LP data permit exact success and exact failure. The polynomial failure example and this analytic success example differ in higher derivatives. The correct sign trichotomy is positive margin => local strict success; negative margin => local weak impossibility; zero margin needs higher-order or exact information.
