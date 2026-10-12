# Exact passive updates of hierarchical marginal records

10 October 2026 UTC. Separate scratch mathematical continuation, jointly developed by the root and worker. Ordinary proofs and bounded exact controls; this is author verification, not independent review. No protected-source change, integration, formal-kernel certification, empirical or actual-warrant claim, or programme closure.

## 1. Result and inherited scope

For arbitrary joint laws on a finite product, retain the marginals in a downward-closed family F. Let C be the intersection of its maximal retained slot sets. Then the stabilizing algebra of the retained observable space is **exactly the functions of C**. Consequently:

- A passive likelihood has an all-prior exact update of branch probability and the complete retained posterior record exactly when it depends only on C.
- The globally autonomous Fisher-gradient moment objectives are exactly the smooth functions of the C-marginal.
- In a star record containing each center–leaf marginal, informative center evidence updates every retained marginal exactly, with no independence assumption. A chain of three edges or two disjoint cliques has empty common core and admits only constant likelihoods under the full probability-plus-posterior contract.

Here “hierarchical” specifies a family of retained marginals, **not a log-linear restriction or graphical factorization of the allowed laws**. All priors are allowed. A junction-tree or connected graph alone does not give the required common core.

The direct inherited input bytes are recorded in INPUT_BINDINGS.json:

1. tensor-likelihood-closure-20261010/RESULT.md, §§3–5, already proves the arbitrary-decoder multiplier criterion, the constant stabilizer for uniform proper interaction cutoffs, and the normalized support-rank dichotomy. Its §7 already gives the six-dimensional three-bit star enlargement for first-slot evidence. That example is not new here; its review clarifies the nonconstant likelihood and specified-channel conditions.
2. leafwise-noetic-geometry-20261010/RESULT.md, §§3–4, already proves the individual-objective stabilizer criterion and the global stabilizer-block objective classification. Those general theorems are inputs, not additions of this packet.
3. The inherited semantic tensor manuscript defines a free algebra graded by ordered semantic words. The function tensors used below are the finite-product evaluation realization already declared in the tensor-likelihood packet. Pointwise multiplication and interaction order across distinct labeled coordinates are not identified with workflow composition or the manuscript's semantic word degree.

The common-core calculation for every downward-closed family, and its explicit design corollary below, are not stated in these inspected passages. This is a bounded new-to-these-inputs deduction, not a project-wide or field-wide novelty claim. [Randriambololona, Definition 2.6 and Proposition 2.11](https://arxiv.org/pdf/1312.0022), supplies the classical componentwise stabilizing-algebra and disjoint-support decomposition framework, over arbitrary fields in these sections. The present result computes that algebra for one real marginal-observable class; the general framework is not new.

## 2. Definitions

Let I be a finite coordinate set and X=product_(i in I) X_i, where q_i=|X_i|>=2. Under uniform probability on each factor write

    R^(X_i) = span{1_i} direct-sum H_i,
    H_i = {h: sum_(a in X_i) h(a)=0}.

Evaluation of a pure tensor as the product of its coordinate functions identifies the function space on X with the finite tensor product. For S subset I, let H_S have contrast factors on S and constant factors elsewhere. Then

    R^X = direct-sum_(S subset I) H_S.

Let F be a nonempty downward-closed family of subsets of I. It therefore contains the empty set. Define

    V_F = direct-sum_(S in F) H_S,
    Max(F) = the inclusion-maximal members of F,
    C = intersection_(T in Max(F)) T,
    A = union_(T in F) T,
    A(V_F) = {L in R^X : L v belongs to V_F for every v in V_F}.

The letter A denotes the set of covered coordinates only when written without the argument (V_F). The finite family Max(F) is nonempty, including Max({empty})={empty}.

V_F is equivalently the span of all functions depending on a retained slot set. Knowing its expectations is equivalent to knowing all retained marginals, or just the maximal marginals with their common submarginals. Choose a full-row-rank basis evaluation matrix M with first row 1. Its normalized record is z=Mp for a probability column p. Basic dimensions are

    dim V_F = sum_(S in F) product_(i in S) (q_i-1),
    dim R^(X_C) = product_(i in C) q_i,

where empty products are 1. Coordinates outside A are unobserved, not silently assumed absent from the latent law.

## 3. Common-core stabilizer theorem

**Theorem 1.** For every real function L on X,

    L V_F subset V_F  iff  L(x)=ell(x_C) for some ell on X_C.

Thus A(V_F)=R^(X_C), embedded as cylinder functions on X. No positivity assumption is needed for this algebraic theorem.

**Proof, sufficiency.** If T is retained, choose a maximal face Q containing T. By definition C subset Q, so C union T subset Q and belongs to F. A function of C times a function of T depends only on C union T; the entire function space on that union is contained in V_F. Linearity gives L V_F subset V_F.

**Proof, necessity.** Since 1 belongs to V_F, stabilization first forces L=L·1 to belong to V_F. Expand it uniquely as sum_(S in F) L_S with L_S in H_S. Suppose some nonzero L_S has S not contained in C. Choose such an offending S of maximal cardinality among the offending components.

There is a maximal T in F with S not contained in T. Set U=T\S. Then U is retained, disjoint from S, and S union T is not retained: it strictly contains the maximal face T. Also U is nonempty. Otherwise T would be a proper subset of the retained S, contradicting maximality of T.

Choose nonzero h_i in H_i for each i in U and put h_U=product_(i in U) h_i. Each contrast space is nonzero because q_i>=2. Project L h_U onto H_(S union T)=H_(S union U).

Multiplication by h_U changes no coordinate factor outside U. Therefore a component L_R h_U can contribute to that projection only if R\U=S: a missing contrast outside U cannot be created, and an extra contrast there cannot disappear. This necessary condition implies R contains S. Such an R is also offending, since S is not contained in C. Maximal offending cardinality gives |R|<=|S|, so R=S.

Consequently the entire forbidden projection is exactly L_S tensor h_U. It is nonzero because tensoring nonzero vectors over R is nonzero. This statement does not require L_S to be a pure tensor. Since S union T is not retained, this contradicts L h_U in V_F. Thus every component of L is supported on a subset of C, and L is a function of C. QED.

This argument does not assume binary contrast multiplication rules. Overlapping categorical contrast products can have constant and contrast components; the disjoint U and maximal-offending choice exclude all competing components before any such rule is needed. Nor must S have maximal degree among all components: a higher-degree core component cannot contain offending S and cannot contribute.

## 4. Exact Bayesian contract and positive structural design

Let L>=0, D_L=diag(L), alpha_L(p)=sum_x L(x)p(x), and B_L(p)=D_Lp/alpha_L(p) on positive branches. For an outcome of a passive channel also require L<=1; a complete channel has nonnegative likelihoods summing pointwise to 1.

**Corollary 2.** The following are equivalent:

1. An arbitrary decoder of Mp gives the branch probability and the entire retained posterior record for every prior, with an impossible-branch status when alpha=0.
2. A linear map T_L satisfies M D_L=T_L M.
3. L depends only on x_C.

This holds already if the test priors are all full-support laws. By inherited Proposition 1, (1) and (2) are equivalent to L V_F subset V_F, so Theorem 1 gives (3). At zero probability, nonnegativity forces D_Lp=0; division is not performed. The zero likelihood is the zero descended map with no possible normalized branch.

For L(x)=ell(x_C), the update is particularly direct. Write w=p_C and, for a maximal T, write a_C for the C-part of a configuration a on T. Then

    alpha = sum_c ell(c) w(c),
    p_T'(a) = ell(a_C) p_T(a) / alpha,       alpha>0.       (1)

All smaller retained marginals are recovered by summing a maximal one. If S does not contain C, its numerator uses the retained marginal on S union C. The updated maximal marginals remain mutually consistent because they are marginals of the same actual Bayesian posterior. No joint reconstruction, conditional independence, or selected exponential leaf is assumed. Repeated declared core likelihoods and complete channels with core-dependent outcomes preserve this same record; this is a consequence of the algebra, not permission to treat a reread as fresh evidence.

**Corollary 3 (least enlargement for a declared evidence coordinate set).** Fix D subset I. The smallest observable space containing V_F and invariant under multiplication by every function of x_D is

    W = span{g_D v : g_D in R^(X_D), v in V_F}
      = V_(F[D]),
    F[D] = {S : S subset T union D for some T in F}.       (2)

**Proof.** Functions on T union D are spanned by products of a T-function and a D-function: this follows from products of coordinate indicators, including their shared coordinates. Their sum over T yields (2). W contains V_F, and multiplying again by a D-function leaves W invariant. Every invariant containing space must contain every displayed product, proving minimality even among all linear observable spaces, not only hierarchical ones. Its maximal faces are the inclusion-maximal sets T union D, so their core contains D. QED.

The invariant-enlargement mechanism is inherited from H-Continuation; (2) computes it for the specified family of all D-likelihoods. One fixed categorical likelihood may generate a smaller algebra, so (2) is not claimed to be minimal for every single likelihood. For a nonconstant likelihood on one binary coordinate, 1 and L already span all functions of that coordinate, recovering the inherited six-dimensional three-bit star example from unary marginals.

It suffices to require every strictly positive D-likelihood with values below 1: their linear span is the full function space on D. For several such declared coordinate sets, replace D by their union, since the generated product algebra is the function algebra on that union. In particular, supporting arbitrary local evidence separately at every coordinate forces the full joint hierarchy; a single proper evidence scope need not do so. These are exact representation statements, not computational or sampling bounds.

This differs from the inherited fixed exponential-leaf remedy. On a specified unary exponential leaf, positive unary likelihoods have log likelihood in the retained space and preserve that leaf; unary marginals can then close because the higher-order log-density class is fixed model data. The leaf is generally nonconvex as a set of laws. Requiring an exact linear summary for unrestricted priors omits that model restriction and produces the full-joint requirement above. There is no contradiction, and no conclusion about the validity of generic approximate methods.

## 5. Global Fisher objectives

Equip the strictly positive law simplex with its evolving Fisher metric. Let Z°=M Delta° and let J be C² on this relative interior moment domain. An ambient representative g of dJ_z gives fitness f=M^Tg and fine negative-gradient field

    X_J(p)=-(diag(p)-p p^T)f.

The mass-coordinate gauge changes f only by a constant and changes no field. The inherited leafwise Theorems 1 and 3 say that projected field constancy over each positive moment fibre is equivalent to f in A(V_F), and global autonomous objectives are exactly functions of the stabilizer-block masses.

**Corollary 4.** The field M X_J(p) depends only on Mp throughout Delta° if and only if

    J(z)=Phi(p_C)                                        (3)

for a C² function Phi on the positive C-marginal simplex. Theorem 1 identifies the stabilizer blocks as {x:x_C=c}; their masses are exactly p_C, so the inherited global theorem applies. This is a classification of the actual projected fine Fisher field for one objective at a time, not the choice of a substitute coarse metric.

Writing b_c for any representative of dPhi_w and bar_b=sum_c w(c)b_c, the closed equations are

    wdot(c) = -w(c)(b_c-bar_b),
    pdot_T(a) = -p_T(a)(b_(a_C)-bar_b)                   (4)

for every maximal T. At empty core, (3) permits only constant objectives and (4) is zero. A nonempty core permits nonstationary objectives and evolves other retained marginals according to their actual retained correlations with the core. These flow statements hold on the maximal positive existence interval; arbitrary C² objectives do not imply unrestricted all-time existence.

## 6. Normalized-only and support boundaries

Do not replace Corollary 2's contract with posterior-only sufficiency. The inherited support-rank dichotomy gives a precise specialization here.

**Corollary 5.** Let L>=0 be nonzero. An arbitrary all-prior decoder of the retained posterior on positive branches exists exactly when either:

(a) L is a function of C; or

(b) its support is contained in one cylinder {x:x_A=a} for a fixed assignment a of all covered coordinates.

Indeed the inherited dichotomy says either unnormalized descent holds or all supported columns M e_x are identical. Those columns are identical exactly when x_A is identical: every covered coordinate has its singleton in F, so the retained observables distinguish its values, while no retained observable sees coordinates outside A. In case (b) the retained posterior is the constant record of that covered assignment. The result also holds when the test priors are only full-support laws.

If A=I, this exception means singleton support. If A is a proper subset of I, it can contain many latent atoms and L may vary among them. If A is empty, the record is only mass and every possible normalized posterior has that same trivial record. For A nonempty, strictly positive L cannot satisfy (b), so positive posterior-only descent has the same core classification as Corollary 2. L=0 has no normalized branch and is only vacuously posterior-only sufficient.

Feasibility must still be treated separately. A partial cylinder support can give equal records to two point masses with different feasibility. Even full singleton revelation in a proper all-coordinate hierarchy can have equal-record parity priors with different feasibility. Conversely, if the full A-marginal is retained and L is positive throughout one whole A-cylinder, feasibility is determined by that cylinder's mass, while variation of L inside the cylinder can leave its branch probability undetermined. Thus omitted coordinates prevent a blanket assertion that adding feasibility removes every posterior-only exception. The exact controls include all three boundaries. No broader feasibility classification is needed here.

## 7. Discriminating examples and verification

For three binary slots (c,a,b), retain {c,a} and {c,b}. The two strictly positive laws

    p_±(c,a,b) = [1+ca/4+cb/3 ± ab/5]/8

have retained moment record (1,E[c],E[a],E[b],E[ca],E[cb])=(1,0,0,0,1/4,1/3). Both have conditional dependence between the leaves given the center: their conditional covariance is ±1/5−1/12, which is nonzero.

For center likelihood L=(1+c/2)/2, both branch probabilities are 1/2 and both retained posterior records are

    (1,1/2,1/8,1/6,1/4,1/3).

The fine posteriors are nevertheless different. For leaf likelihood L=(1+a/2)/2 the probabilities are still 1/2, but the retained posterior mean of b is +1/10 or −1/10. For Fisher objective J=E[c], both projected velocities are (0,−1,−1/4,−1/3,0,0); for J=E[a], the b-velocities are −1/5 and +1/5.

The exact matrix controls use marginal-indicator rows and solve M diag(L) ker(M)=0 in the full ambient likelihood coordinates, independently of the ANOVA proof. Selected cases are:

- Four-bit star: 8 retained dimensions, stabilizer dimension 2.
- Four-slot chain with edges 01,12,23: 8 retained dimensions, stabilizer dimension 1. A two-edge chain instead has its middle slot as core and is a star; “chain” without its length would be ambiguous.
- Disjoint cliques 01 and 23: 7 retained dimensions, stabilizer dimension 1.
- Ternary-centered star with two binary leaves: 9 retained dimensions, stabilizer dimension 3.
- Faces 012 and 013 with alphabets (2,3,2,2): 18 retained dimensions, two-slot core and stabilizer dimension 6.
- Omitted-coordinate, mass-only, full-order and proper-order boundary controls.

Further controls verify symbolic arbitrary-prior maximal-marginal numerators, explicit chain/disjoint-clique failures, a rank-two non-pure categorical tensor, cylinder support boundaries, and the least-enlargement product span. Run `python3 verify.py` from this directory. All arithmetic assertions use exact SymPy integers and rationals. CONTROL_RESULTS.json and verification.txt record 34 passing assertion groups, including five direct-input identity checks. These bounded controls supplement the ordinary universal proofs; they are not a large enumeration, performance campaign, formal proof, or independent review.

The complete order cutoff F={S:|S|<=k}, 0<=k<|I|, has empty core, recovering the inherited constant-stabilizer theorem (with the mass-only endpoint included algebraically). At full order there is one maximal face I, so C=I and every likelihood stabilizes. The general result therefore includes both inherited endpoints without extending a proper-order obstruction to informative nonempty-core records.

The script checks the currently bound direct inputs. It does not rerun or re-certify the tensor packet's older transitive cone dependency; that packet's independent review records its historical input-drift qualification. No source bytes were silently replaced. MANIFEST.json binds this packet's final files.

The mathematical design criterion preserves specified information under specified likelihoods and objectives. It establishes no sampling efficiency, empirical model identification, actual cognitive implementation, truth or warrant test, intervention permission, or universal reduction for arbitrary evidence. Restrictions on possible priors and the fixed-reference exponential-leaf remedy remain separate contracts.
