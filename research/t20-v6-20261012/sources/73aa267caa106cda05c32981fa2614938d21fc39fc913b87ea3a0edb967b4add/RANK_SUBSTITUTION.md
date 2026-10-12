# Substitution into the existing quadratic-rank counterpath

This note identifies an exact premise replacement in Section 6 of
`partial-quadratic-rank-classification-20261010/RESULT.md`. It does not modify
that packet, reprove its positive-direction classification, or assert its
independent-review status. Its previous imported full-functional existence
premise may be supplied by the explicit functional proved in `PROOF.md` here.

Fix d≥1, 0≤r≤d with d−r≥2, and h(x)=x₁²+⋯+xᵣ². Define the algebra substitution

    E(p)(u,v)=p(0,…,0,u,v,0,…,0),

where u and v occupy two uncontrolled coordinates. With the full functional Λ
of `PROOF.md`, set B(p)=Λ(E(p)). Then:

- B(1)=1 by normalization.
- B(q²)=Λ(E(q)²)≥0 because E is an algebra homomorphism and Λ is positive on
  squares of every degree, including zero. B itself need not be strictly
  square-positive: E has a kernel when other coordinates are present.
- B(hp)=0 for every p because E(h)=0.
- For the embedded witness F=1+u⁴v²+u²v⁴−u²v², B(F)=−1 and F≥3/4 everywhere.

These are exactly the four properties used by the existing stationary and
Gaussian-mixture construction. In particular, no finite-degree test or
truncated functional is substituted for a universal premise.

Retain the existing standard product-Gaussian functional

    G_t(p)=∫p(x)e^(−th(x))dγ_d(x),
    Z_r(t)=(1+2t)^(−r/2),
    A_t=(13/14)B+(1/14)G_t,
    L_t=A_t/A_t(1).

The unchanged Gaussian identities give G_t(1)=Z_r(t) and G_t(F)=6Z_r(t): in
the two independent standard Gaussian uncontrolled coordinates, the witness
expectation is 1+3·1+1·3−1·1=6. Thus

    A_t(1)=(13+Z_r(t))/14>0,
    A_t(F)=(−13+6Z_r(t))/14≤−1/2<0

for every t≥0, since 0<Z_r(t)≤1. The genuine Gaussian part makes L_t strictly
positive on every nonzero polynomial square at every finite time. Both B and
G_t satisfy the same unnormalized killing hierarchy, so the quotient obeys
the existing normalized hierarchy. The embedded globally positive F excludes
a representing measure at every time. The existing nonstationarity argument
when r≥1 and stationarity edge when r=0 are unchanged.

Consequently the full-functional component of that counterpath no longer
needs to remain an unconstructed imported existence input: Sections 2–7 of
`PROOF.md` explicitly construct and prove it. This discharges that mathematical
premise only. Classical credit is retained, and the construction is not yet a
formal Lean proof of the hierarchy or the full functional.
