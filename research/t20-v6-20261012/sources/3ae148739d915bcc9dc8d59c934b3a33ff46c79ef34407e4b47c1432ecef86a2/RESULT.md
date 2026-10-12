# When moment completion commutes with Bayesian conditioning

10 October 2026 UTC. Separate scratch continuation, leaving the frozen face-stratified packet unchanged. Ordinary finite proof and exact symbolic controls; author verification only. No protected edit, integration, empirical or psychological identification, actual-warrant claim, historical novelty claim, or programme closure.

## 1. Exact answer and inherited scope

Let R_r select the unique fixed-reference relative-entropy completion of a retained moment record. For a nonzero nonnegative likelihood weight L:

- On every strictly positive input law, R_r B_L = B_L R_r exactly when either L is in the retained observable space's stabilizing algebra, or L is a positive constant on the entire duplicate-column fibre of one exposed vertex and zero elsewhere.
- The same classification already gives commutation on every boundary input whose actual Bayesian branch is possible.
- Requiring, in addition, exact feasibility preservation for all boundary inputs removes the extra vertex case: the answer is precisely L in the stabilizing algebra. This requirement concerns Boolean possibility, yet the resulting class also preserves exact branch mass.

Thus preservation of a closed model under an observation is weaker than commuting with completion of arbitrary input laws. Completion may create a possible branch absent from the input law. It never makes an actually possible branch impossible in this finite model.

The parent supplied the commutation question and proposed classifications. This packet proves their exact quantifiers and gives executable countercontrols. Its bounded addition is the classification of the composed **completion and observation operators**, not another proof of the inherited ingredients:

1. `face-stratified-noetic-geometry-20261010/RESULT.md`, Theorems 1–3, supplies facial closure, the unique entropy completion, continuity, and the same-reference zero-likelihood criterion. Corollary 4 gives zero-inclusive retained-local preservation of the closed model.
2. `tensor-likelihood-closure-20261010/RESULT.md`, §5, supplies the normalized-posterior dichotomy: L stabilizes V, or all retained columns on supp L are equal. Its theorem explicitly has the same classification when only positive priors are required.
3. `event-feasibility-descent-20261010/RESULT.md`, §3, supplies the all-prior zero-set facial criterion and equivalent same-support nonnegative retained witness.
4. The leafwise and hierarchical-marginal reports supply the finite stabilizing algebra and common-core calculation. Neither the present question nor its composed-operator iff was found in the inspected passages. This is a bounded comparison, not a whole-project priority claim.

The finite geometry is classical, with primary attribution already documented in the frozen face-stratified packet. The elementary operator combination below is proved directly and makes no new literature-priority claim. INPUT_BINDINGS.json includes byte-identical snapshots and the frozen geometry manifest identity; no independent-review credit is inherited by this packet.

## 2. Definitions and domains

Let X be finite and nonempty, and let V=span{1,phi_1,...,phi_d} be a minimal real observable space retaining mass. Put M=[1;phi], and P=conv{phi(x):x in X}. For r_x>0, let C_r be the closure of the exponential family proportional to r_x exp(theta·phi(x)). For every z in P let q_r(z) be its unique C_r member, equivalently its relative-entropy minimizer. Define

    R_r(p)=q_r(E_p[phi]),
    alpha_L(p)=sum_x L_x p_x,
    B_L(p)_x=L_x p_x/alpha_L(p),   only when alpha_L(p)>0.

R_r is continuous, idempotent, and preserves the complete retained record. It fixes exactly C_r. Its support is all supplied atoms on the minimal face of the input mean. The stabilizing algebra is

    A(V)={a in R^X: a f belongs to V for every f in V}.

It contains 1, is closed under sums and pointwise products, and is a subspace of V. All likelihoods here are nonnegative weights. Scaling by a common positive constant leaves the posterior and all stated commutation/feasibility tests unchanged. For a probability-valued channel event, scale to at most one and supply the complementary outcome.

For a vertex v of P write

    S_v={x:phi(x)=v}.

This includes every duplicate-column atom at v. A finite-polytope vertex is exposed; d=0 is permitted, in which case P is its single vertex and S_v=X.

Positive-input commutation means

    R_r(B_L(p))=B_L(R_r(p)) for every p_x>0.             (1)

Both denominators are positive there. Full feasibility-sensitive commutation means equality of the partial maps on the entire simplex: their domains agree and their values agree on that domain. Equivalently require

    alpha_L(p)>0 iff alpha_L(R_r(p))>0                  (2)

for every p, together with (1) on all possible branches. No equality of branch probabilities is included in this definition.

## 3. Positive inputs: an exact algebra-or-vertex theorem

**Theorem 1.** For any fixed r>0 and nonzero L>=0, the following are equivalent:

1. Positive-input commutation (1) holds.
2. The posterior stays in C_r from every full-support model member, and its retained normalized record is determined by Mp across all strictly positive input laws.
3. At least one of the following holds:

       (a) L belongs to A(V);
       (b) L=c 1_(S_v) for a vertex v of P and a constant c>0.

The alternatives may overlap. The classification is independent of r, so holding for one positive reference is equivalent to holding for every positive reference.

### Proof of the composition criterion

Assume (1). For p in the positive exponential family, R_r(p)=p, so

    R_r(B_L(p))=B_L(p).

The posterior therefore belongs to C_r. Also if p,p' are positive with Mp=Mp', then R_r(p)=R_r(p'). Commutation gives R_r(B_L(p))=R_r(B_L(p')). Taking moments, which R_r preserves, gives M B_L(p)=M B_L(p'). Thus the normalized posterior record descends.

Conversely suppose the two conditions in 2 hold. For a positive p, R_r(p) is a full-support model member with the same moment. Posterior-record descent gives

    M B_L(p)=M B_L(R_r(p)).

The right-hand law belongs to C_r by model preservation. R_r(B_L(p)) is the unique member of C_r at the left-hand moment. Uniqueness gives their equality. This proves 1 iff 2.

### Apply the inherited dichotomy, retaining the model condition

Write S=supp L. The inherited normalized-record criterion says that condition 2's descent clause is equivalent to

    L in A(V)  or  all columns phi(x), x in S, equal.   (3)

The frozen boundary theorem says that its model clause is equivalent to

    S is the full saturated support of a face F,
    log L restricted to S belongs to V restricted to S.              (4)

If the columns in (3) all coincide, (4) forces F to be a single vertex v and S=S_v. Every retained function is constant on S_v, so the logarithmic condition forces L to have a single positive value c there. Conversely such c 1_(S_v) satisfies both clauses. Merely having rank-one supported columns is insufficient if the column is nonvertex, the duplicate fibre is only partly included, or the positive weights differ within that fibre.

It remains to show that L in A(V) automatically satisfies (4), including when it has zeros. On the finite set of values taken by L, interpolate real polynomials b and h such that

    b(t)=1 for t>0, b(0)=0 when 0 is present;
    h(t)=log t for t>0, h(0)=0 when 0 is present.

A(V) is a unital algebra, so b(L)=1_S and h(L) belong to A(V), hence to V. The affine observable 1_S exposes S as its maximum set, giving a saturated face. The restriction of h(L) is log L. Thus (4) holds. This proves all equivalences. The resulting criterion contains no r. QED.

The exception is not a probability-preservation statement: conditioning on a single exposed vertex always yields its fixed completed law, even if the likelihood mass of that vertex cannot be recovered from the retained prior mean.

## 4. What changes at boundary inputs

**Lemma 2 (possible branches cannot be destroyed by completion).** For every law p,

    supp p subset supp R_r(p).                          (5)

Consequently alpha_L(p)>0 implies alpha_L(R_r(p))>0 for every L>=0.

**Proof.** Every representation of a mean in a face is supported on that face's supplied columns. R_r(p) is positive on every supplied column of the mean's minimal face. Thus each atom having positive p mass has positive completion mass. Nonnegative L gives the consequence. QED.

**Proposition 3.** Positive-input commutation is equivalent to commutation on every p with alpha_L(p)>0, including boundary p. It does not by itself imply (2).

**Proof.** Necessity follows by restricting to positive laws. For sufficiency, approximate any possible boundary input by p_epsilon=(1-epsilon)p+epsilon u with u strictly positive. The original branch mass stays positive near p. Lemma 2 makes the completed branch positive at p as well. R_r is continuous; B_L is continuous wherever its denominator is positive. Taking limits in the positive-input equality yields the boundary equality. QED.

Thus the extra boundary issue is exactly an input p with zero branch mass while R_r(p) has positive branch mass. This is a domain mismatch of partial operations, not a failure of their values to agree on a genuinely possible branch.

**Theorem 4 (all-input feasibility-sensitive classification).** Full feasibility-sensitive commutation on the entire simplex holds if and only if

    L belongs to A(V).                                 (6)

In this case alpha_L(R_r(p))=alpha_L(p) for every p, so exact branch mass preservation follows as an additional conclusion.

**Proof, sufficiency.** Theorem 1 and Proposition 3 give equality on all possible inputs. L belongs to V since 1 belongs to V and L stabilizes it. Therefore alpha_L is retained and has the same value before and after completion. This proves (2) and the claimed mass identity.

**Proof, necessity.** Theorem 1 leaves only its vertex case to consider: L=c 1_(S_v). Condition (2) makes event feasibility constant on every moment fibre, because R_r is the same for every law in that fibre. The inherited feasibility theorem therefore supplies w in V with

    w>0 on S_v,    w=0 off S_v.

All retained functions have one common value on the duplicate-column fibre S_v; hence w=lambda 1_(S_v), lambda>0. Therefore 1_(S_v) belongs to V. For every f in V, f has a constant value f(v) on S_v, so

    1_(S_v) f=f(v) 1_(S_v) belongs to V.

Thus 1_(S_v) belongs to A(V), and so does L. QED.

Geometrically, exact feasibility in this exceptional case says that the complement X\S_v must itself be a saturated face support F. If the complement is nonempty, all supplied columns lie either in F or at v, so P=conv(F union {v}). Since F is an exposed proper face and v is outside it, its exposing hyperplane contains aff F but not v. Therefore v is outside aff F, and dim P=dim F+1. There is an affine functional equal to zero on aff F and one at v; on the supplied columns it is exactly 1_(S_v). Thus the complementary-face condition produces the retained affine indicator explicitly, including all duplicate columns. Conversely a retained indicator has that complementary zero face. If the complement is empty, all columns equal v, d=0, and the constant indicator one supplies the same conclusion. For a genuine extra exception outside A(V), the complementary face condition necessarily fails.

If desired, introduce a distinct impossible symbol bottom, extend B_L(p)=bottom when alpha_L(p)=0, and set R_r(bottom)=bottom. Then Theorem 4 simply classifies equality of these totalized operators. The impossible symbol is a domain convention, not a probability law or arbitrary posterior at zero mass.

## 5. Exact countercontrols and positive control

### A. Local closed-model preservation can fail arbitrary-input commutation

On two bits x,y in {-1,+1}, retain (1,x,y), use uniform r, and take

    p_rho(x,y)=(1+rho xy)/4,    rho=1/2,
    L=1_(x=+1).

Both input means are zero, so R_r(p_rho) is uniform. L is retained and therefore branch mass is exactly 1/2 before and after completion. It also preserves the entire closed product model, by the frozen local-update corollary. Nevertheless

    E_(R_r(B_L(p_rho)))[(x,y)]=(1,1/2),
    E_(B_L(R_r(p_rho)))[(x,y)]=(1,0).

The first posterior already lies on the product model's edge, so completion does not change it. In --,-+,+-,++ order the two laws are (0,0,1/4,3/4) and (0,0,1/2,1/2). Closed-model preservation plus exact mass preservation still does not give arbitrary-input evidence-faithful completion.

### B. The extra vertex case commutes but can invent a possible branch

For the same square, take L=1_(++). Both compositions equal e_(++) for every strictly positive p, and indeed for every p with p_(++)>0. Yet with p uniform on the opposite diagonal {(+,-),(-,+)},

    alpha_L(p)=0,    R_r(p)=uniform,    alpha_L(R_r(p))=1/4.

The other diagonal law, uniform on {(--),(++)}, has the same zero mean but vertex mass 1/2. Thus these two boundary laws have identical records and opposite feasibility; both complete to the same uniform law.

Even among positive inputs, branch mass can change: p_(1/2) has p_(++)=3/8 whereas its completion gives 1/4. The singleton vertex indicator does not stabilize V, and the square with that vertex removed is not a face.

### C. Duplicate saturation and constant weights are indispensable

Take statistic columns (0,0),(0,0),(0,1),(1,0),(1,1), with reference

    r=(1/12,1/6,1/4,1/4,1/4).

The aggregate reference on the four distinct square columns is uniform. Completion uses the product law on those columns and splits the duplicated vertex in the ratio 1:2.

For L=(1,1,0,0,0), both compositions on every positive input return (1/3,2/3,0,0,0): this is the full-duplicate-fibre vertex exception. For L=(1,2,0,0,0), completing the actual posterior still returns (1/3,2/3,0,0,0), whereas conditioning the completion returns (1/5,4/5,0,0,0). For L=(1,0,0,0,0), the latter is a point mass and again fails. These failures have identical supported column values; normalized-record descent alone cannot establish commutation of the laws.

A nonvertex rank-one support also fails. Use columns -1,0,+1, uniform r, and L=(0,1,0). The retained posterior mean is always zero, but R_r(e_middle)=uniform whereas B_L(R_r(uniform))=e_middle. The support is not a facial support.

### D. A nontrivial stabilizer gives genuine all-input commutation

Retain only (1,x) on two bits, and use reference weights (1,3,2,4). Completion preserves the two x-block masses and fills the conditional y distributions in ratios 1:3 and 1:2. Every L=(a,a,b,b), a,b>=0, not both zero, belongs to A(V) and commutes on every possible input, with exact branch mass and feasibility. Zeros a=0 or b=0 are allowed. Unequal positive likelihood values within one duplicated x-column block fail the restricted constant-weight requirement.

## 6. Executable scope and interpretation

`verify.py` checks the bound inputs and performs exact symbolic polynomial identity tests for all 80 nonzero two-bit likelihood-weight arrays with entries 0,1,2. On the uniform-reference unary square it finds exactly 10 commuting arrays on all positive inputs: two nonzero constants and eight singleton weights. The feasibility-sensitive class has only the two constants. The same 80-array test for the one-coordinate record finds exactly the eight nonzero blockconstant arrays, with no extra boundary exception. Symbolic numerator identities range over arbitrary positive atom weights; they are not a sample of numerical priors.

The preserved run passed 24 exact assertion groups. The verifier also checks the explicit countercontrols, duplicate saturation and weights, a nonvertex support, and the nontrivial stabilizer's exact symbolic branch-mass identity. These checks supplement the general ordinary proofs. They do not establish numerical robustness, a practical fitting algorithm, an empirical cognitive model, or the correctness of a supplied likelihood.

For complete proper interaction spaces, the inherited constant-stabilizer theorem specializes the result: all-input feasibility-sensitive commutation permits only constant nonzero likelihoods; positive-input commutation additionally permits point-revealing singleton likelihoods because unary observables distinguish and expose every atom. For hierarchical marginal records, all-input commutation permits exactly common-core likelihoods by the inherited algebra calculation. These are consequences of the same theorem, not additional all-prior obstructions or computational lower bounds.

The contrast is operational and conditional: a selected closed model may be stable under an update while completion of an arbitrary law before that update changes its result or its feasibility. Nothing here identifies completion with warranted psychological correction, claims an actual implementation made that substitution, or changes any protected implementation or programme status.
