# Separate verdict: exact truncated backward-heat diagnostic

10 October 2026 UTC. Independently checked parent-supplied rational construction. This is a degree-at-most-four diagnostic and is kept distinct from the full-functional heat obstruction. No extension of this particular truncated functional to the entire polynomial algebra is assumed or proved.

## Exact functional and positivity

On R[x,y,z] of total degree at most four, define Λ by

    Λ(1)=1,
    Λ(x_i²)=4,
    Λ(x_i⁴)=50,
    Λ(x_i²x_j²)=1  (i≠j),
    Λ(xyz)=3/2,

and set all other nonconstant monomial values in this degree range to zero. These assignments specify a real linear functional on the whole indicated finite-dimensional space.

In the reordered quadratic monomial basis

    (1,x²,y²,z², x,yz, y,xz, z,xy),

its moment matrix is block diagonal. The first block is

    E = [[1,4,4,4],
         [4,50,1,1],
         [4,1,50,1],
         [4,1,1,50]],

and each of the remaining three blocks is

    O = [[4,3/2],[3/2,1]].

The Schur complement of E's leading entry is the 3×3 matrix with diagonal 34 and off-diagonal −15. Its eigenvalues are 4,49,49, so E is positive definite. O has positive leading entry 4 and determinant 7/4, so it too is positive definite. Therefore the full quadratic moment matrix is positive definite. In particular Λ(q²)>0 for every nonzero polynomial q of degree at most two, and Λ(g)>0 for every nonzero SOS polynomial g of degree at most four. The latter follows because any such SOS has at least one nonzero square and no summand can have degree above two.

This strict positivity is exact, not an SDP tolerance conclusion. As an additional determinant check, det(E)=9604 and the full matrix determinant is 823543/16.

## Nonnegative witness under heat

For the nonnegative Choi–Lam polynomial f=1−4xyz+x²y²+x²z²+y²z²,

    Λ(f)=−2,
    Λ(H_t f)=−2+48t+12t².

The second expression is increasing on t≥0 and equals −3797/2500 at t=1/100. It is consequently negative throughout [0,1/100]. No positive measure can represent any of these heat-shifted truncated functionals on that interval.

## Any fixed backward-heat window fails as a universal certificate

Fix any finite T≥0. For a>0 let Λ_a=Λ∘S_a and f_a=S_(1/a)f. Dilation is invertible on polynomials of degree at most two and preserves nonnegative polynomials, so Λ_a retains strict square positivity and f_a≥0. The correct dual scaling identity gives

    Λ_a(H_T f_a)=−2+48T/a²+12T²/a⁴.

Choose a²≥100T and a>0. Then T/a²≤1/100, so this expression is strictly negative. Define the truncated functional L=Λ_a∘H_T. It is not a moment functional, as witnessed by f_a. Nevertheless, since polynomial heat exponentials are finite and inverse to each other at opposite times,

    L∘H_(−T)=Λ_a.

The backward-shifted functional is strictly positive on every nonzero SOS polynomial in the degree-four space. Thus for every proposed fixed finite T, a nonmoment L passes that exact strict-square-positive backward-heat condition.

This supplies a finite explicit diagnostic against replacing the nonexistent uniform parameter of the paper's Corollary 3.22/3.25 route by an arbitrary fixed heat window. It is not an argument about the pointwise Theorem 3.21, which allows the necessary time to depend on the input polynomial. The backward-shift formula uses a truncated linear functional, not an assumed measure evolving backward under the heat equation.

## Scope and verification

The exact controls reconstruct all entries of the 10×10 moment matrix from the monomial specification, verify its block form and positive Schur/determinant certificates, verify both witness formulas, and check the inverse-heat composition on every monomial of total degree at most four. These finitely many checks completely cover the displayed finite-dimensional identities. They do not prove a full-functional extension or an infinite hierarchy representation theorem.

The parent's actual written proof was read after it was frozen: heat-truncated-certificate-diagnostic-20261010/RESULT.md, SHA-256 abdecfe71002743674e02a280c1523b57bd03417e30ad233427e0cc645e44c00. Its complete claims agree with this review. The parent's check_exact.py was copied into this review's isolated truncated-independent-replay/ directory and executed there. It passed, and its generated EXACT_RESULTS.json is byte-for-byte identical to the parent's frozen result (SHA-256 305e1ae8496268ae8948338cdb5a48459335fc73aac177795f2a5eb34378b8ca). The reviewer's separate matrix reconstruction and symbolic controls also passed. No parent file was modified by either run.
