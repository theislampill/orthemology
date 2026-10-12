# Approximate continuation: charge only newly acquired moment directions

11 October 2026. V6 ordinary cross-contribution, pending independent review. No Lean or empirical claim.

## Inherited inputs and question

The fully examined continuation manuscript SHA626504b64c2d7817b882e74992ba989d83c7ef8e67b1467b537101c2b804edb9 proves minimax moment defect equals best uniform approximation, exact continuous augmentation dimension, and an approximate Walsh-memory lower bound. The graph-continuation source supplies the actual accessible family of characters R_h(G). The present question is the approximate cost of supplementing an already retained, possibly oblique moment space, rather than reacquiring a representation from nothing.

Let X={−1,+1}^V, with probability-normalized uniform inner product. Let I be any finite chosen family of distinct nonempty accessible masks, q=|I|, and chi_S the associated orthonormal Walsh characters. Let W0 contain1 and denote the already retained observable space. A new linear acquisition space W contains W0 and has k=dim W−dim W0 additional independent moment coordinates. Decoders of moments in W can be arbitrary. Suppose every event b_S=(1−chi_S)/2 for S in I is recovered with uniform absolute probability error at most epsilon over the full probability simplex Delta(X).

The full-simplex, linear-acquisition and fixed-space premises remain essential. This is not a sample bound, bit bound, nonlinear-encoder bound or permission to acquire a source.

## Residual spectrum bound

Let P0 be orthogonal projection onto W0 and r_S=(Id−P0)chi_S. Define the positive operator

    A = sum_(S in I) r_S tensor r_S

on W0-perp. Let lambda1≥…≥lambdaN≥0 be its eigenvalues, including zeros. Then every such extension satisfies

    sum_(j>k) lambda_j ≤ 4 q epsilon².                 (1)

In particular,

    k ≥ sum_(S in I) ||r_S||² − 4 q epsilon²,         (2)

with integer ceiling and zero lower bound when appropriate. The bound can be applied to each subset I of the required questions; already exactly retained characters need not consume the error budget of a missing subfamily.

## Proof

The inherited defect theorem implies dist_infinity(chi_S,W)≤2epsilon. Since uniform measure has mass1, the best L² residual is also at most2epsilon. Write W=W0 orthogonal-sum U, dim U=k, and let PU be its projection. As U⊆W0-perp,

    chi_S−P_W chi_S = r_S−PU r_S.

Summing squared norms yields

    trace(A)−trace(PU A) ≤ 4 q epsilon².

For completeness, diagonalize A in an orthonormal basis e_j. The coefficients a_j=||PU e_j||² obey0≤a_j≤1 and sum a_j=k. Thus trace(PU A)=sum lambda_j a_j≤sum_(j≤k)lambda_j: allocating at most unit weight to the k largest nonnegative eigenvalues maximizes the sum. This proves(1).

Because the original chi_S are orthonormal, the operator sum chi_S tensor chi_S is an orthogonal projection. A is its compression to W0-perp, so0≤A≤Id and each lambda_j≤1. Hence trace(PU A)≤k, proving(2). No continuity or linearity of the decoders has been used.

## Exact endpoint reconciles the older augmentation theorem

At epsilon=0, (1) implies k≥rank A. The span of the residuals is the image of span{chi_S} in R^X/W0, so

    rank A = dim(W0+span{chi_S:S in I})−dim W0.

Acquiring a basis of that residual span attains exact recovery. Thus the spectral formulation recovers the inherited exact linear-augmentation count. The older continuous-encoder exact lower bound is stronger in encoder generality; it is not reproved or extended to arbitrary approximate nonlinear encoders here.

At intermediate epsilon, (1) is only necessary. An L² residual bound does not itself give a uniform-law decoder, so the optimal spectral truncation must not be advertised as an attained minimax solution.

## Discriminating example

Take two orthonormal characters chi_A,chi_B and an unrelated nonconstant character chi_C. Retain

    W0=span{1, cos(theta)chi_A+sin(theta)chi_C},

and require the two events for A and B, with0<theta<pi/2. On W0-perp the nonzero residual eigenvalues are1 and sin²(theta). For k=1, (1) demands sin²(theta)≤8epsilon². Whenever epsilon<sin(theta)/sqrt(8), one extra moment is impossible and at least two are needed. Merely counting the one old nonconstant coordinate would incorrectly suggest it replaces one required coordinate in the exact case: the retained direction mixes needed and irrelevant content.

Conversely if W0 already contains chi_A exactly, choose I={B}; then epsilon<1/2 forces at least one additional moment. Applying the bound only to the missing questions avoids diluting the certificate by already solved questions.

## Why this helps the synthesis

The graph result specifies which interactions the allowed future operations can expose. The inherited defect theorem specifies the error notion. The residual spectrum quantifies how much the existing representation already contributes to those questions. This joins continuation relevance, retained evidence and supplementary inquiry without treating tensor degree or the raw number of stored coordinates as sufficient measures of preservation.
