# Exact descent of event feasibility through finite observable records

10 October 2026 UTC. Separate scratch mathematical continuation. Complete ordinary proofs and bounded exact rational controls; author verification, not independent review or a formal-kernel certificate. No protected-source edit, integration, actual implementation or psychological-warrant claim, or T20 closure.

## 1. Result and the precise inherited difference

For a finite observable map retaining mass, the question “does this event have positive probability?” is determined by the observable record for every prior, including boundary priors, exactly when the zero-likelihood atoms are **all the supplied columns lying on one exposed face of the observable polytope**. Equivalently, some nonnegative retained observable has exactly the likelihood's support. The actual likelihood need not be retained.

The face criterion is a classical finite-polytope consequence, proved below without a literature search or a historical novelty claim. Its role here is to finish one specifically omitted information-preservation boundary.

The direct inspected inputs are hash-bound in INPUT_BINDINGS.json:

- `hierarchical-marginal-core-20261010/RESULT.md`, §6, gives normalized-only support-cylinder descent and explicitly leaves the broader feasibility classification untreated. Its probability-plus-posterior and common-core theorems are not additions here.
- `tensor-likelihood-closure-20261010/RESULT.md`, §§3 and 5, supplies unnormalized descent and the normalized support-rank dichotomy. Its boundary parity example handles singleton revelation, not arbitrary event-support feasibility.
- `leafwise-noetic-geometry-20261010/RESULT.md`, §§3 and 6, correctly requires the actual moment-polytope relative interior for finite-parameter full-support exponential leaves. Section 6 below gives a concrete distinction between this prerequisite and strictly positive individual marginals.

The similarly named `bayes-feasibility-compatibility-20261010` and `measure-bayes-face-transport-20261010` discuss preservation of independently restricted classes of prior laws. Their inspected opening statements concern a different meaning of feasibility. No exhaustive project-wide priority scan was performed.

## 2. Definitions and endpoint conventions

Let X be a nonempty finite set and let M be an r-by-|X| real matrix of full row rank. Write m_x = M e_x for its columns, V = row(M), and assume mass is retained:

    1_X belongs to V; equivalently, there is u in R^r with u^T M = 1_X^T.

The mass row need not literally be the first row. Let

    Delta = {p >= 0 : sum_x p_x = 1},
    P = M Delta = conv{m_x : x in X}.

Thus every point of P has u^T z = 1. Distinct atoms may have identical columns, and some supplied columns may not be vertices of P. Neither case is discarded.

Fix L >= 0, initially nonzero. Define

    S = {x : L_x > 0},     Z = X \ S,
    alpha_L(p) = L^T p,
    E_L(p) = 1 if alpha_L(p) > 0, and 0 otherwise.

“Feasibility descends” means that an arbitrary function g:P -> {0,1} satisfies E_L(p)=g(Mp) for every p in Delta. No continuity, linearity, probability output, or posterior output is included in this contract. Because L is nonnegative,

    alpha_L(p)=0  iff  supp(p) is contained in Z.           (1)

An exposed zero face means a set

    F = {z in P : a^T z = 0},    with a^T z >= 0 on P.   (2)

Every nonempty proper exposed face in the usual affine definition can be written this way: subtract its minimum using the retained mass covector u. We allow the improper faces F=P (take a=0) and F=empty (take a=u, strictly positive on P). The empty set is not claimed to be a nonempty argmin face under conventions that exclude it. Write conv(empty)=empty.

For the assumed nonzero L, Z=X cannot occur. For completeness L=0 will be included as the always-impossible endpoint, with S=empty and F=P.

## 3. Support-face classification

**Theorem 1.** The following are equivalent, also with the L=0 convention:

1. Event feasibility descends through M on all of Delta.
2. Every representation of every point of conv{m_z:z in Z} as a convex combination of supplied columns uses only indices in Z. Equivalently,

       M^(-1)(conv{m_z:z in Z}) intersect Delta = Delta_Z,

   where Delta_Z consists of the laws supported in Z and is empty when Z is empty.
3. F=conv{m_z:z in Z} is a face of P and it is column-saturated:

       Z = {x in X : m_x belongs to F}.

4. There is an exposed zero face F of P with precisely those zero columns:

       Z = {x in X : m_x belongs to F}.

5. There is v in V with v >= 0 and supp(v)=S.

If v=M^T a is such a witness, a complete feasibility decoder is

    g(z) = 1_{a^T z > 0}.                               (3)

The weights of L on S do not enter this classification.

### Proof: fibre classification forces a saturated face

Suppose (1) holds, and let z in F=conv{m_x:x in Z}. Some q supported in Z represents z and has alpha_L(q)=0. Every p with Mp=z must also have alpha_L(p)=0, so (1) implies supp(p) is contained in Z. This proves (2); its converse is immediate from (1).

Now assume (2). If z=t a+(1-t)b belongs to F for a,b in P and 0<t<1, choose representing laws p_a and p_b. The mixture t p_a+(1-t)p_b represents z, hence is supported in Z. Nonnegativity and the strict weights force both p_a and p_b to be supported in Z. Therefore a,b belong to F, proving the face property. If m_x belongs to F, its point-mass representation e_x is also supported in Z, so x belongs to Z. This proves column saturation and (3).

Conversely, if (3) holds, any convex representation of a point in F has all its positive-weight columns in F. This follows by isolating each coefficient strictly between zero and one in the face definition; a coefficient equal to one is immediate. Saturation then puts all its indices in Z, giving (2). Empty/full endpoints satisfy the same statements directly.

### Proof: a direct finite exposing functional

For completeness we prove the needed finite exposure, rather than only invoke the classical fact that polytope faces are exposed. Assume (2), with S and Z both nonempty. Set W=span{m_z:z in Z}, let Q be orthogonal projection onto W-perpendicular, and set

    K = conv{Q m_s : s in S}.

We claim 0 is not in K. Otherwise there are lambda_s >= 0 with sum_s lambda_s=1 and

    sum_s lambda_s m_s = sum_z b_z m_z.                 (4)

Apply the retained mass covector u. This yields sum_z b_z=1. Split b_z=b_z^+ - b_z^- and put A=sum_z b_z^+=1+sum_z b_z^- > 0. Then (4) becomes an equality between two nonnegative combinations of the same total mass A:

    sum_s lambda_s m_s + sum_z b_z^- m_z
       = sum_z b_z^+ m_z.

After dividing by A, the right side is a law supported in Z; the left side uses S with total weight 1/A>0. They have the same record, contradicting (2).

K is compact and convex and excludes 0. Let a be its closest point to 0. Then a is nonzero and belongs to W-perpendicular. For every k in K, minimality along the segment from a to k gives

    a^T(k-a) >= 0, so a^T k >= ||a||^2 > 0.

Consequently a^T m_z=0 on Z, while a^T m_s=a^T Qm_s >= ||a||^2>0 on S. Thus v=M^T a is nonnegative with exactly support S, establishing (5). Its zero set on P is exactly conv{m_z:z in Z}, so (4) follows too. This argument uses only finite-dimensional convex geometry and mass retention.

If Z is empty, choose v=1_X and a=u. If S is empty, choose v=0 and a=0. These handle the two endpoint conventions.

Finally (4) immediately gives (5) by evaluating its exposing functional on all columns. If (5) holds, then for any p>=0,

    L^T p > 0  iff  v^T p > 0  iff  a^T Mp > 0.

This proves (3), establishes (1), and completes all equivalences. QED.

### Qualifications that prevent false simplifications

- It is not enough that the convex hull of the zero columns happens to be a face. It must contain no positive-likelihood column. For columns (1,0), (1,1/2), (1,1), let L=(0,1,0). The zero columns span all P, a face, but the midpoint is a positive-likelihood column in that same face. Equal-record priors e_mid and (e_left+e_right)/2 have different feasibility.
- Duplicate columns must receive the same zero/nonzero status, although their positive likelihood values may differ. Otherwise their two point masses immediately violate feasibility descent.
- Boundary priors are essential. On strictly positive priors every nonzero L>=0 is feasible, regardless of the criterion. The theorem classifies all-prior support status, not an interior-only question.
- Retained mass converts affine exposure into row-space membership. Without it that membership criterion can fail: M=(0,1) on two atoms determines every law through p_2, and the support of L=(1,0) is feasible iff p_2<1, but no vector in row(M) has support {1}. Full row rank merely removes redundant coordinates; the theorem continues to hold with redundant rows if mass is retained.
- Exact positivity is the contract. A row-space certificate does not supply numerical tolerance, robust finite-precision inference, or a lower bound on a nonzero probability.
- Finiteness is essential to the stated exposed-face formulation. The proof uses finitely supplied columns and a compact convex hull after projection. General compact convex state spaces can have nonexposed faces; no unrestricted cone, measure, or infinite-state transport is asserted.

## 4. Three different information contracts

This section positions the new criterion alongside the inherited results, rather than reproving their classifications.

**Probability alone.** alpha_L(p) is determined by Mp for every prior exactly when L belongs to V. The short quotient check is that any d in ker M has sum d=0; perturbing an interior law by a small multiple of d forces L^T d=0. Conversely L=M^T a gives alpha_L(p)=a^T Mp. Probability descent therefore implies feasibility descent, but Theorem 1 only asks for some v in V with the same support as L.

**Probability and the entire retained posterior.** The inherited exact criterion is

    M diag(L) = T M for a linear T,

equivalently multiplication by L preserves V. This is stronger than retaining alpha_L alone.

**Normalized posterior alone.** For L nonzero, the inherited support-rank dichotomy says that the retained posterior on positive branches descends iff the preceding unnormalized criterion holds or all columns indexed by S are identical. No feasibility output is included in that exception.

Combining the dichotomy with Theorem 1 gives the exact posterior-plus-feasibility contract: either unnormalized descent holds, or the supported columns are identical and a nonnegative v in V has precisely support S. This logical combination does not turn the likelihood values into a retained observable.

In particular, take columns (1,0), (1,0), (1,1) and L=(1/2,1,0). Feasibility is determined by z_2<1, and every positive-branch retained posterior is (1,0). But the first two point-mass priors have equal records and branch probabilities 1/2 and 1. Thus even posterior plus feasibility need not determine probability when columns can coincide. This is consistent with the inherited omitted-coordinate discussion.

## 5. Exact pairwise-moment countercontrols

Let X={-1,+1}^3 and retain the seven rows

    1, x, y, z, xy, xz, yz.

This is the complete pairwise-marginal record. Define

    q(x,y,z) = (1+xy+xz+yz)/4.

q is 1 at +++ and --- and 0 at the other six atoms. It is a nonnegative retained observable. Therefore **any** nonnegative likelihood with precisely these two supported atoms has observable feasibility:

    alpha_L(p)>0  iff  E_p[q]>0
      iff  1+E_p[xy]+E_p[xz]+E_p[yz] > 0.               (5)

Choose

    L = q(1+x/3)
      = (1+xy+xz+yz)/4 + (x+y+z+xyz)/12.

Its cubic coefficient is 1/12, so L does not belong to V. It therefore separates feasibility from branch mass. L takes values 4/3 and 2/3 at the two supported atoms, so it is a likelihood weight, not a probability-valued event likelihood. The rescaling L_tilde=3L/4 takes values 1 and 1/2 and is a genuine outcome of the binary channel (L_tilde,1-L_tilde), with identical support and normalized posterior.

For 0<epsilon<1 let

    p_+(x,y,z) = (1+epsilon xyz)/8,
    p_-(x,y,z) = (1-epsilon xyz)/8.

These strictly positive priors have identical retained record (1,0,0,0,0,0,0). Their branch masses and posterior means are

    alpha_L(p_±) = 1/4 ± epsilon/12,
    E_(B_L(p_±))[x] = E[y] = E[z]
                     = (1 ± 3epsilon)/(3 ± epsilon),
    E_(B_L(p_±))[xy] = E[xz] = E[yz] = 1.

At epsilon=1/2 the branch masses are 7/24 and 5/24; the probability-valued L_tilde masses are 7/32 and 5/32. The posterior unary means are 5/7 and -1/5. Both branches are feasible, as known from their common E[q]=1/4, while both probability and normalized-posterior descent fail.

Two nearby controls separate the other contracts:

- With likelihood q itself, the two branch probabilities are both 1/4, but posterior unary means are +epsilon and -epsilon. Retained probability need not retain the posterior.
- With singleton likelihood 1_{+++}, the positive-branch posterior is constant. At epsilon=1, the boundary parity priors have the same pairwise record, but one gives +++ mass 1/4 and the other mass 0. Normalized-only descent need not retain feasibility.

For this particular seven-row/eight-column matrix, ker M is spanned by the parity vector h=xyz. A further exact support check is available: every nonempty S meeting both parity classes has a row-space witness, while a nonempty S contained in either one parity class fails. Indeed row-space membership is the single condition sum_x h_x v_x=0; a positive vector on S can satisfy it exactly when S meets both signs. When S has only one sign, the two boundary parity priors supply a fibre ambiguity. Including S=empty gives 226 feasible support patterns out of all 256. This finite special-case count checks the general theorem but does not replace its proof.

## 6. Global facet, local positivity, and the exponential-leaf prerequisite

Let Z be the six zeros of q. The full observable matrix has rank 7; its six zero columns have rank 6. Since all columns have mass coordinate 1, P has affine dimension 6 and F=conv{m_z:z in Z} has affine dimension 5. Thus q=0 exposes a **facet** of this global pairwise marginal polytope.

Yet q cannot be represented as a sum of pointwise-nonnegative potentials, each depending on at most two of the three variables. For every pair of variables, all four assignments occur among the six zeros of q. This also implies full projection onto every unary scope. If

    q(x) = sum_j f_j(x_(A_j)),     |A_j|<=2, f_j>=0,

then at every zero atom each nonnegative summand must vanish. The projections of Z cover every assignment on every A_j, forcing every f_j to be identically zero. That contradicts q(+++) = 1. The same proof excludes any nonzero sum of such nonnegative local potentials with exactly q's support. Signed local terms can of course represent q, as its displayed formula already shows. The obstruction concerns nonnegativity of each local summand, not absence of a pairwise linear formula.

For a concrete record on that facet, let p_0 be uniform on Z. Then

    E_(p_0)[x] = E[y] = E[z] = 0,
    E_(p_0)[xy] = E[xz] = E[yz] = -1/3,
    E_(p_0)[q] = 0.

Each pair marginal gives probabilities 1/6 to ++ and -- and 1/3 to +- and -+. Every unary and pair-marginal cell is strictly positive, while the combined record lies on a proper global face. Hence being in the interior of each local marginal simplex does not imply being in the relative interior of the actual joint marginal polytope. The record is globally compatible; incompatibility is not the issue.

This is a useful exact crosswalk to the inherited full-support exponential-leaf theorem. For any full-support reference r and finite theta,

    p_theta(x) = r_x exp(theta·phi(x)) / sum_y r_y exp(theta·phi(y))

is strictly positive at every atom, so E_(p_theta)[q]>0. No such finite theta can realize the record of p_0. In fact every prior with that record is supported in Z by the facet equation. The six zero columns are linearly independent, so the representing law is uniquely p_0. For the uniform reference, p_0 is a boundary limit of the pairwise exponential family: use theta·phi=-t(xy+xz+yz) and let t tend to +infinity. The six zero atoms have exponent t and the two others exponent -3t. This is a limit, not a finite-parameter member.

The inherited leaf theorem already states the correct global-interior hypothesis. This example invalidates a possible naïve substitution of componentwise local positivity for that hypothesis; it is neither a discovered error in that theorem nor evidence that an actual implementation made that substitution.

An adjacent realizability countercontrol makes the prerequisite distinction stronger. Prescribe three centered binary slots with all three pair correlations -2/5. Each proposed pair table is strictly positive: its two same-sign cells are 3/20 each and its two different-sign cells are 7/20 each. The tables agree on their uniform unary marginals. The corresponding proposed correlation/covariance matrix has diagonal 1 and off-diagonal -2/5, with eigenvalues 1/5, 7/5, 7/5, so it is positive definite. Nevertheless the proposed retained record gives

    E[q] = (1-6/5)/4 = -1/20,

which is impossible for any joint law because q>=0 pointwise. Thus local table validity plus positive-definite proposed covariance does not even certify global binary-law realizability. At correlation -1/3 the preceding p_0 is a realizable boundary point; at -2/5 the proposed record is outside P. The three-by-three proposed covariance is not itself a covariance under an existing binary law, and is not identified with the full six-statistic exponential-family Hessian. These examples constrain potential prerequisite shortcuts without alleging a failure of any actual model or implementation. The displayed fractions and this countercontrol were not found in the inspected direct result inputs or the bounded checks of the earlier tensor-moment and information-geometry result reports; no broader novelty claim follows.

## 7. Exact executable controls and scope of use

Run `python3 verify.py` from this directory. The script uses exact SymPy integers/rationals throughout; no floating-point tolerance or numerical optimizer certifies any result. It:

- verifies the three direct input hashes;
- constructs row-space support certificates or explicit equal-record feasibility counterexamples for every support subset in six small selected column configurations;
- checks all 256 supports of the three-bit pairwise matrix against the parity characterization;
- verifies the masses, posteriors, Walsh coefficient, facet rank, local nonnegative-potential zero coverage, positive local marginal cells, unique boundary representation, and omitted-coordinate contract separation;
- checks the positive-definite proposed covariance and positive local tables of the globally unrealizable -2/5-correlation control;
- checks the empty/full conventions and the necessity of mass retention for the linear row-space formulation.

The support-certificate search solves finite exact active-constraint systems. Every returned candidate is independently substituted into its zero, positivity, and row-space equations. Failure is never accepted merely because the search found nothing: each declared negative case must provide two explicit nonnegative normalized laws with identical records and opposite feasibility. The witness search uses finitely enumerated kernel circuits on these selected matrices. The script does not rely on a claim that a bounded search proves the universal theorem.

The completed run passed 29 assertion groups. Across 304 support patterns, 252 received exact support certificates and 52 received explicit equal-record feasibility ambiguities. CONTROL_RESULTS.json and verification.txt record the actual run; MANIFEST.json binds the packet files. Exact controls supplement the ordinary proof. They do not replay transitive inherited dependencies, inherit independent-review status, establish numerical robustness or sampling efficiency, or authorize new evidence operations. Event feasibility here means positive probability under a declared mathematical likelihood, not normative permission, source validity, actual cognitive warrant, or programme closure.
