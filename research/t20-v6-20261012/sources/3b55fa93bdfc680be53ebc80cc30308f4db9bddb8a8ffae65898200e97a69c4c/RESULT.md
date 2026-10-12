# KL constraint repair that commutes with a fixed positive evidence channel

10 October 2026 UTC. Separate mathematical continuation. Ordinary proof and exact symbolic/rational controls. Author verification only; no protected edit, integration, formal-kernel certification, empirical warrant, or programme closure.

## 1. Result and its bounded increment

For one finite, strictly positive, normalized passive channel and a nonempty closed convex probability family, the following are equivalent:

1. Every channel outcome preserves the family at every prior in that family.
2. First-argument KL projection onto the family commutes with every outcome update at **every strictly positive input law, including off-model inputs**.
3. The family is the convex join of arbitrary closed convex families on the channel's equal-column blocks, with unrestricted mixture weights between the selected blocks.

The equivalence of 1 and 3 is the inherited fixed-channel theorem. The increment proved here is its equivalence to the coherent-state **repair/evidence commutation** contract, with an explicit projection formula. It does not re-prove a new invariant-family classification or a new normalization theorem. Neither the invariant-family theorem, the KL chain rule, nor the inherited fixed-marginal information-erasure counterexample receives fresh novelty credit.

If the within-block projection cost is d_a and the input mass of that block is s_a, repair assigns block weight proportional to s_a exp(−d_a). Actual evidence in the fixed channel changes s_a by the block likelihood and leaves the within-block input, projection, and cost unchanged. Consequently either order gives exactly the same law.

The hypotheses deliberately exclude zero channel entries. They allow boundary-valued repairs, omitted channel blocks, lower-dimensional constraints, nonsingleton within-block families, and curved coupled constraints. They do not require an interior point of the feasible family.

## 2. Definitions and well-posedness

Let X={1,…,n}, n≥1, and let Y be nonempty and finite. Fix a passive channel about the unchanged target X:

    K(y|i)>0,                 Σ_y K(y|i)=1 for every i.

For p in the closed probability simplex Δ_n, set

    α_y(p)=Σ_i K(y|i)p_i,
    B_y(p)_i=K(y|i)p_i / α_y(p).

For each y, α_y(p)≥min_i K(y|i)>0 on the whole simplex. Thus B_y is defined and continuous everywhere on Δ_n, and sends Δ_n° to itself.

Let ∅≠C⊆Δ_n be closed and convex. For p∈Δ_n° define

    D(q||p)=Σ_i q_i log(q_i/p_i),       0 log(0/p_i)=0,
    Π_C(p)=argmin_{q∈C} D(q||p).

All logarithms are natural. This notation denotes a single law: the objective is finite and continuous on the compact C, and is strictly convex in q because x log x is strictly convex on [0,∞). Hence the minimizer exists and is unique, even if C lies on a boundary face. No gradient at a zero coordinate is used. Gibbs' inequality gives D(q||p)≥0, with equality exactly when q=p. One direct proof uses −log t≥1−t on supp(q): D(q||p)≥1−p(supp(q))≥0. Equality forces p=q at every supported coordinate and no mass elsewhere.

Partition X into maximal equal-channel-column blocks I_1,…,I_m:

    i∼j iff K(y|i)=K(y|j) for every y.

Write κ_a(y)>0 for their common column entries, Δ(I_a) for the corresponding coordinate face, and

    C_a=C∩Δ(I_a),        A={a:C_a≠∅}.

Empty intersections are allowed. In the decomposition below, A is nonempty and only these active blocks participate. Laws on I_a are identified with their zero extensions to X.

## 3. Exact equivalence

**Theorem.** Under the preceding hypotheses, these conditions are equivalent:

(I) B_y(c)∈C for every c∈C and y∈Y.

(E) Π_C(B_y(p))=B_y(Π_C(p)) for every p∈Δ_n° and y∈Y.

(J) C=conv(⋃_{a∈A}C_a).

In (J), every C_a is compact and convex, and C consists precisely of laws

    q=Σ_{a∈A} w_a r_a,       w∈Δ_A, r_a∈C_a.

Weights equal q(I_a); conditional laws in zero-weight blocks may be chosen arbitrarily. All choices of the positive-weight block conditionals and of the weights are independently permitted. There is no cross-block coupling of these choices beyond the total mass equation.

### 3.1 Inherited implication (I) ⇔ (J)

This is Theorem 1 of `../repeatable-channel-constraints-20261010/RESULT.md`, restricted to strictly positive channels. Its essential argument is recalled to locate the dependence, not to claim it anew.

Column normalization gives Bayes plausibility:

    c=Σ_y α_y(c) B_y(c).

If c is extreme in C and (I) holds, every displayed posterior equals c. For each i in the support of c, cancellation gives K(y|i)=α_y(c) for every y. Thus the support lies in one equal-column block. Finite-dimensional compact-convex generation by extreme points yields (J). Conversely, each B_y only reweights the blocks in the displayed mixture, so (J) gives (I). The predecessor includes a complete ordinary proof of the compact-convex generation step.

Normalization and **every outcome** enter this implication. A single forward-preserving likelihood is insufficient; §6 gives an exact countercontrol.

### 3.2 Projection formula under (J)

Fix p>0. For every active block define

    s_a=p(I_a)>0,
    p_a=p(·|I_a)>0,
    r_a=argmin_{r∈C_a} D(r||p_a),
    d_a=D(r_a||p_a),
    Z(p)=Σ_{a∈A} s_a exp(−d_a).

The conditional minimizers exist uniquely by the same compactness and strict-convexity argument. Each d_a is finite and nonnegative, so 0<Z(p)≤Σ_{a∈A}s_a≤1. Input mass on inactive blocks is not silently renormalized before this calculation.

The projection and its optimal value are

    w_a*=s_a exp(−d_a)/Z(p),
    Π_C(p)=Σ_{a∈A} w_a* r_a,                         (1)
    min_{q∈C} D(q||p)=−log Z(p).                    (2)

In particular every active block has strictly positive projected mass, though individual coordinates can be forced to zero by C_a.

**Proof.** Write a feasible law q=Σ_a w_a t_a. Splitting the sum over its disjoint blocks gives the exact KL chain rule

    D(q||p)=Σ_a w_a log(w_a/s_a)+Σ_a w_a D(t_a||p_a).  (3)

Terms with w_a=0 are zero. Hence the minimum over conditionals is attained at r_a, leaving

    Σ_a w_a log(w_a/s_a)+Σ_a w_a d_a
      =Σ_a w_a log[w_a/(s_a exp(−d_a))]
      =D(w||w*)−log Z(p).                           (4)

Gibbs' inequality uniquely minimizes (4) at w=w*. Since all w_a*>0, every selected conditional is then uniquely r_a. This proves (1)–(2). Equations (3)–(4) also handle inactive blocks correctly: q has zero coordinates there, while their input mass contributes through the active s_a not summing to one. □

This is a reduction to smaller convex minimizations, not a claim that an arbitrarily described C_a has a closed-form or efficiently computable minimizer.

### 3.3 (J) implies (E): evidence reweights the same corrected blocks

For p′=B_y(p), block constancy gives

    s_a′=κ_a(y)s_a/α_y(p),       p_a′=p_a.

Therefore r_a′=r_a and d_a′=d_a. Formula (1) gives projected weights

    w_a′=κ_a(y)s_a exp(−d_a) / Σ_{b∈A}κ_b(y)s_b exp(−d_b)
         =κ_a(y)w_a* / Σ_{b∈A}κ_b(y)w_b*.

These are precisely the block weights of B_y(Π_C(p)); its conditionals are also r_a. This proves (E) for every positive p, whether or not p∈C. □

The same calculation supplies the optional exact value identity, with V(p)=D(Π_C(p)||p):

    Z(B_y(p))=Z(p) α_y(Π_C(p))/α_y(p),
    V(B_y(p))=V(p)+log α_y(p)−log α_y(Π_C(p)).        (5)

Evidence and repair need not assign the same outcome probabilities before and after repairing an off-model input. Commutation concerns their resulting probability law and their order, not equality of these two likelihood normalizers.

### 3.4 (E) implies (I), without a boundary continuity assumption on Π_C

Take any c∈C, including a boundary point, and let u be the uniform law. For 0<ε<1 set

    p_ε=(1−ε)c+εu>0,       q_ε=Π_C(p_ε).

By minimization and the coordinate inequality p_ε,i≥(1−ε)c_i on supp(c),

    0≤D(q_ε||p_ε)≤D(c||p_ε)≤−log(1−ε)→0.          (6)

The finite Pinsker inequality in natural logs gives

    ||q_ε−c||_1
      ≤sqrt(2D(q_ε||p_ε))+||p_ε−c||_1
      ≤sqrt(−2log(1−ε))+ε||u−c||_1→0.               (7)

For completeness, the version used here has an elementary proof. If q≠p, let S={i:q_i>p_i} and t=q(S)−p(S)=||q−p||_1/2. Log-sum on S and its complement gives D(q||p)≥d(q(S)||p(S)), the binary KL divergence. For fixed b=p(S)∈(0,1), the binary function has value and first derivative zero at a=b and second derivative 1/[a(1−a)]≥4. Integrating twice gives d(a||b)≥2(a−b)^2, including endpoint a by continuity. Thus D(q||p)≥||q−p||_1²/2. The case q=p is immediate. Here p=p_ε is strictly positive, so these aggregations are valid.

By (E), B_y(q_ε)=Π_C(B_y(p_ε))∈C. Positivity of K makes B_y continuous at c, so B_y(q_ε)→B_y(c). Closedness of C implies B_y(c)∈C. Since c and y were arbitrary, (I) follows. This uses no definition of Π_C at a boundary second argument and no assumed continuity of that projection there. □

Together §§3.1–3.4 establish the equivalence.

## 4. A genuinely informative channel with curved, variable conditional repair

Take five states, blocks I_A={1,2,3}, I_B={4,5}, and

    K(+|·)=(3/4,3/4,3/4,1/4,1/4),
    K(−|·)=(1/4,1/4,1/4,3/4,3/4).

This is a strictly positive normalized informative channel. Define the within-block families

    C_A={r∈Δ_3: Σ_{i=1}^3(r_i−1/3)^2≤1/24},
    C_B={(t,1−t): 1/2≤t≤1},
    C=conv(C_A∪C_B),

with disjoint-block embeddings understood. C_A is a two-dimensional closed disk in its affine plane. Its radius is smaller than the distance from the barycenter to the simplex boundary, since 1/24<1/6. Thus it is a genuinely nonpolyhedral compact convex family of strictly positive conditionals. Its quadratic constraint couples all three coordinates. C_B is a nonsingleton closed segment. The join C is nonpolyhedral because its intersection with the first block face is C_A.

Use the off-model positive input

    p=(2/5,1/20,1/20,1/4,1/4).

Its block masses are (1/2,1/2), with conditionals p_A=(4/5,1/10,1/10) and p_B=(1/2,1/2). The conditional KL repairs and costs are exactly

    r_A=(1/2,1/4,1/4),       d_A=log(5/4),
    r_B=(1/2,1/2),           d_B=0.

**Why the curved projection is exact.** Uniqueness and invariance under swapping coordinates 2 and 3 force the minimizing conditional to have form (t,(1−t)/2,(1−t)/2). The disk condition becomes 1/6≤t≤1/2. The objective is binary KL d(t||4/5), strictly decreasing on this interval since its derivative is log[t/(4(1−t))]<0. Hence t=1/2. Substitution gives d_A=(1/2)log(5/8)+(1/2)log(5/2)=log(5/4). This is an ordinary exact minimization proof, not a numerical optimizer result.

Formula (1) therefore yields

    Z=9/10,       w*=(4/9,5/9),
    Π_C(p)=(2/9,1/9,1/9,5/18,5/18).

For the two actual outcomes, both orders agree exactly at

    Π_C(B_+(p))=B_+(Π_C(p))=(6/17,3/17,3/17,5/34,5/34),
    Π_C(B_−(p))=B_−(Π_C(p))=(2/19,1/19,1/19,15/38,15/38).

The repaired law's outcome probabilities are 17/36 and 19/36; the original input's are each 1/2. The repaired block masses change informatively to (12/17,5/17) or (4/19,15/19). The projection values are V(p)=log(10/9), V(B_+p)=log(20/17), and V(B_−p)=log(20/19), verifying (5).

These are not fixed conditional templates. For example the feasible input

    (1/6,1/6,1/6,3/8,1/8)

is fixed by Π_C and has different conditionals in both blocks. A second off-model input with masses (2/3,1/3), conditionals (1/10,4/5,1/10) and (4/5,1/5), projects to

    (2/13,4/13,2/13,4/13,1/13).

Its first conditional repair is (1/4,1/2,1/4), with the same exact cost log(5/4). The script checks both actual outcomes in both off-model examples. The general proof allows arbitrary nonsymmetric compact convex C_a as well; the symmetry here makes the control exactly solvable.

## 5. Omitted blocks, boundary outputs, and elementary limiting cases

Append a sixth state forming its own channel block, with K(+|6)=K(−|6)=1/2, and require q_6=0 in C. All other block families remain as in §4. At

    p=(4/15,1/30,1/30,1/6,1/6,1/3)>0,

the first two block masses and the omitted block mass are each 1/3. Formula (1) uses Z=3/5 and yields the same five-coordinate projection as §4, with a zero sixth coordinate. Both outcomes still commute, with the same resulting five-coordinate posteriors and zero sixth coordinate. This tests active-block omission and a boundary-valued repair without a support/domain failure.

If all channel columns are distinct, every block is a singleton. The inherited classifier forces C to be a coordinate face Δ_S, and (1) reduces to ordinary restriction and renormalization:

    Π_{Δ_S}(p)_i=p_i/p(S) on S, and 0 outside S.

This commutes with every positive likelihood, as expected. If all columns are equal, there is one block, every B_y is the identity, and arbitrary nonempty closed convex C is allowed. For n=1 all statements reduce to the unique one-point law. These cases require no extra hypotheses.

## 6. Exact negative controls and scope limits

### A single forward-preserving likelihood does not suffice

Let C={q∈Δ_2:q_1≥1/2} and L=(3/4,1/4). Its Bayes action sends first coordinate t to 3t/(1+2t), so it maps C into C. Yet, at p=(1/4,3/4),

    Π_C(p)=(1/2,1/2),
    Π_C(B_L(p))=(1/2,1/2),
    B_L(Π_C(p))=(3/4,1/4).

The projection formula here is (max(p_1,1/2),1−max(p_1,1/2)), by the derivative of binary KL. The complementary normalized outcome L_−=(1/4,3/4) takes (1/2,1/2) outside C. Thus this example does not contradict the theorem: the complete channel fails (I). It isolates the missing quantifier and normalization argument.

### Fixed marginal repair that erases legitimate evidence is inherited

The Bayes-feasibility predecessor §6 already supplies the countermodel

    C={q∈Δ_3:q_1=1/2},       p=(1/2,1/4,1/4),
    K(+|·)=(3/4,1/4,1/4),    K(−|·)=(1/4,3/4,3/4).

The two ordinary posteriors are (3/4,1/8,1/8) and (1/4,3/8,3/8), and their fixed-marginal KL projections are both p. Since Π_C(p)=p, commutation fails already at this on-model input. The inherited composition and null-neutrality identities for the constrained update survive; they are weaker than (E). This packet repeats the exact values only as a regression control and claims no new information-erasure example or scoring result.

### Strict positivity is a deliberate domain guard

The inherited invariant-family classifier permits nonnegative channels on defined branches. The present commutation statement does **not** silently inherit that extension: Π_C is defined here only for positive second arguments, and an outcome possible before repair can become impossible after repair.

For example, let C={e_1}, p=(1/2,1/2), and let the channel perfectly reveal either state. Its second outcome has positive probability at p but zero probability at Π_C(p)=e_1. Thus B_2(Π_C(p)) is undefined, and B_2(p) is a boundary second argument outside this packet's projection domain. A theorem for zero entries would need an explicit restricted domain and extended-divergence contract. No such theorem is claimed here.

### Invariance does not make every metric projection commute

Keep first two states in one equal-column block and put

    u=(3/4,1/4,0),       v=(0,0,1),       C=conv{u,v},
    K(+|·)=(3/4,3/4,1/4),                K(−|·)=(1/4,1/4,3/4).

This C satisfies the block-join theorem. Let P_E instead be the squared-Euclidean projection. For q(t)=tu+(1−t)v, the unconstrained minimizing parameter is

    t_E(p)=((p−v)·(u−v))/||u−v||²,

clipped to [0,1]. At p=(1/10,2/5,1/2), the three relevant first-block weights are

    t_E(p)=27/65,
    t_E(B_+(p))=81/130,
    (B_+(P_E(p)))(I_A)=81/119.

The first two are interior, so no clipping occurs. Hence P_E does not commute, although the KL projection does. This is an operator-specific guard. It does not prove or claim that KL is the unique divergence with any commutation property.

### The face-stratified entropy completion is a different operator

The nearby `face-stratified-noetic-geometry-20261010/RESULT.md`, Theorem 2, defines a reference-dependent selector R_r(p)=q_r(Mp). It minimizes D(q||r) on the **moment fibre Mq=Mp**, taking r normalized. Its range is the closure of a generally nonconvex exponential model. For positive p this can equivalently be viewed as minimizing the **other orientation** D(p||q) over that model: if q*=R_r(p) and q is a positive member of the exponential family, then log(q*/q) is retained, so matching means gives D(p||q)−D(p||q*)=D(q*||q)≥0; boundary q has infinite divergence from positive p. It is not this packet's minimization of D(q||p) over one fixed closed convex C. The shared word “repair” provides no mathematical identification of these operators.

Here is a strictly positive control that needs no boundary caveat. On X={−1,+1}² with uniform r and retained V=span{1,x,y}, the reference model is the independent product family. Put

    p_±(x,y)=(1±xy/2)/4,
    K(+|x,y)=(2+x)/4,       K(−|x,y)=(2−x)/4.

Both input means are (0,0), so R_r(p_±) is uniform. Each channel outcome is unary and strictly positive, and it preserves the entire closed product model. Yet

    means of R_r(B_+(p_±)) = (1/2, ±1/4),
    means of B_+(R_r(p_±)) = (1/2, 0).

Thus model preservation does not imply all-input commutation for this different selector. These are the familiar hidden-correlation controls in a positive unary form, not a new parity mechanism. The countercontrol alone is asserted here; an exact commutation characterization for R_r, including prior-domain issues at zero likelihoods, is a separate question and is not attributed to the convex-C theorem.

### Other boundaries retained

- Closedness, convexity, finite dimension, the first-argument KL orientation, the fixed feasible family, and the unchanged passive target are stated premises. No classification for arbitrary divergences, changing targets, or changing C is supplied.
- Off-model commutation does not say Π_C(B_y(p))=B_y(p). Repair may change an off-model law, including its block masses. It says that repairing before or after the **same declared** evidence update produces the same corrected law.
- Repeating the algebra yields commutation for finite compositions of the declared B_y. Interpreting products as physically available fresh evidence still requires the appropriate joint or conditional channel. A copied receipt is not a fresh independent observation.
- Within-block constraints may be nonlinear and coupled. The classifier does not permit additional coupling between different block choices while retaining the global all-outcome contract.
- A family of admissible priors need not be a family constraining every posterior report. The theorem is conditional on that model-wide role for C, not an instruction to impose it.

## 7. Predecessor comparison, attribution, and verification

The exact local inputs and SHA-256 hashes are in `INPUT_BINDINGS.json`. The following complete reports were read for a bounded programme-local comparison:

1. `repeatable-channel-constraints-20261010/RESULT.md` already proves (I)⇔(J), including its wider nonnegative-channel classifier. It supplies the block decomposition and owns that result.
2. `bayes-feasibility-compatibility-20261010/RESULT.md` already distinguishes ambient normalization from coherent-state constraint projection, gives the fixed-marginal KL formula, and exhibits informative evidence erased by fixed-marginal repair. Its §5 is an inherited interface premise; its §6 is the inherited regression countercontrol.
3. `nonseparable-bayes-repair-20261009/RESULT.md` proves normalization onto the **full simplex** for perspective-plus-radial Bregman generators and its equivariance P_F(L⊙b)=B_L(P_F(b)). It does not state the present classification of arbitrary closed convex **coherent-state constraint sets** by off-model projection commutation. In its notation, C is also used for the ambient positive cone, not this packet's constraint family. The symbols and codomains must not be conflated.
4. `channel-natural-repair-20261009/RESULT.md` classifies a cross-dimensional contraction contract and combines it with ambient normalization repair. That is a different contract; the present proof does not add a new Fisher/KL uniqueness theorem.
5. `face-stratified-noetic-geometry-20261010/RESULT.md` defines fixed-moment-fibre entropy completion into an exponential-model closure, proves its facial structure and Bayesian model-preservation criterion, and retains hidden-correlation countercontrols. Section 6 above explicitly separates that selector from Π_C and does not use its model-preservation result as this theorem's premise.

The local increment is an explicit corollary and constructive repair formula linking the inherited invariant-family theorem to exact order-independence of constraint repair and evidence. The parent supplied the proposed equivalence, projection formula, approximation-based necessity proof, one-likelihood discriminator, Euclidean-projection control, and entropy-completion orientation guard. This worker supplied the detailed hypothesis checks and ordinary proofs, exact curved-family and omitted-block controls, executable verification, and bounded predecessor comparison. These are joint derivation and author checks, not independent review.

The entropy chain rule, Gibbs inequality, Pinsker inequality, and convex optimization steps are classical elementary mathematics; they are derived here where used. No new external literature survey or field-wide novelty clearance was performed, and no field novelty is claimed. Inherited primary-source attribution remains in the bound predecessor reports; this operation does not claim to have re-read their external sources.

Run from this packet directory:

    python3 verify.py

`verify.py` checks twelve small exact control groups with SymPy symbolic arithmetic and rational arithmetic, and verifies all bound predecessor hashes. `CHECK_RESULTS.json` and `verification.txt` record the executed results. These checks supplement the ordinary universal proof; they are neither statistical sampling nor a proof-assistant certificate.

All conclusions remain conditional mathematics. They do not establish that C is correct, that the chosen KL repair is normatively justified, that the channel is true or available, that acquisition is permitted, that sources are authenticated or independent, that a faculty functions properly, that an actual belief is warranted, or that noetic restoration has occurred. No protected source, audit state, release, integration, or programme closure is changed.
