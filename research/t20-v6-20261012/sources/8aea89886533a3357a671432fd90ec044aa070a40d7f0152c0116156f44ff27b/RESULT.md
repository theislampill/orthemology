# Channel-natural Bregman geometry and normalization repair

9 October 2026 UTC. Local T20 mathematical synthesis. Ordinary written proofs and exact symbolic/rational controls; no protected edits, integration, empirical warrant, or programme closure. The simplex uniqueness theorem is classical Chentsov/Fisher mathematics, with directly relevant established Bregman characterizations. It is not a new field theorem.

## 1. Decisive result

For one C² strictly convex potential f_n on each open finite probability simplex, contraction of its Bregman divergence under **every** column-stochastic map between **every pair of dimensions** forces

    f_n(p) = c Σ_i p_i log p_i + an affine function of p,

with one c > 0 shared by all dimensions. Fisher geometry is the conclusion of the proof, not an assumed premise. Strict convexity is not silently identified with positive-definite Hessian.

Combine this with the actually established normalization-repair classification F_n(sp) = s f_n(p) + a_n(s):

- Contraction tested only on normalized laws determines f_n but does not constrain a_n.
- Full-positive-cone contraction forces the radial Bregman divergences D_an to agree across dimensions, while their common strictly convex shape remains arbitrary.
- Thus, up to affine potentials, the full contracting repair family is

      F_n(x) = c Σ_i x_i log(x_i/s) + a(s),   s = Σ_i x_i,
      D_Fn(sp,tq) = c s KL(p || q) + D_a(s,t).

- Additional coordinate-additivity of the cone potential forces a''(s) = c/s. Only with that extra condition does the cone divergence reduce to c times generalized, unnormalized KL.

The local contribution is the explicit synthesis and scope discriminator for the programme's existing repair and transport results. Neither the classical uniqueness nor the perspective divergence identity receives fresh priority credit.

## 2. Hypotheses and notation

For n ≥ 2 let Δ_n° = {p ∈ R^n : p_i > 0, Σ_i p_i = 1} and T_n = {v : Σ_i v_i = 0}. Let f_n : Δ_n° → R be C² and strictly convex, with intrinsic affine-simplex derivative. Set

    D_fn(p,q) = f_n(p) − f_n(q) − df_n(q)[p−q].

For every n,m ≥ 2, let K be a nonnegative m-by-n matrix with column sums one and no zero row. It maps Δ_n° into Δ_m°. The contract is

    D_fm(Kp,Kq) ≤ D_fn(p,q)   for all p,q ∈ Δ_n°.             (C)

No reference measure, preferred prior, partition weight, or other transported object is an input to f_n. The family is indexed only by the finite outcome coordinates. Potentials may change by affine terms without changing divergences. No symmetry of the potentials themselves is assumed.

The one-outcome simplex can be adjoined with zero divergence; it is not needed in the proof. Boundary states, zero output rows, infinite alphabets, and non-mass-preserving maps are outside the stated contract. No boundary differentiability is needed.

## 3. Elementary proof of the classical simplex classification

### 3.1 Divergence contraction gives tangent-Hessian contraction

Write g_n(p)[v,v] = Hess f_n(p)[v,v]. Taylor expansion of (C) with p = q + εv yields

    g_m(Kq)[Kv,Kv] ≤ g_n(q)[v,v].                            (H)

Conversely, (H) implies (C), using the exact segment identity

    D_fn(p,q) = ∫_0^1 (1−r) g_n(q+r(p−q))[p−q,p−q] dr.

All segment points are interior. This is the already proved transport iff, recalled to make the proof self-contained. Convexity gives positive-semidefinite g_n; nondegeneracy has not been assumed.

### 3.2 Reversible refinements and permutations are isometries

Let E be a column-stochastic coordinate-splitting matrix and R its deterministic block-sum matrix, with RE = I. Both have no zero output row. Apply (H) first to E and then to R:

    g_n(p)[v,v] ≥ g_N(Ep)[Ev,Ev] ≥ g_n(REp)[REv,REv].

The end terms agree, so both inequalities are equalities. The same argument applied to a permutation and its inverse gives permutation invariance of g_n. This is a consequence of the contraction contract, not an extra axiom.

### 3.3 At a uniform law the quadratic form has one scalar

Let u_n = (1/n,…,1/n). Extend the tangent form to R^n by applying the Euclidean projection P_n = I − 11ᵀ/n to both arguments. The representing symmetric matrix is invariant under every coordinate permutation. Consequently its diagonal entries agree, and its off-diagonal entries agree. On T_n the all-ones matrix vanishes, so

    g_n(u_n)[v,v] = α_n Σ_i v_i²,

for a scalar α_n ≥ 0. This elementary matrix argument includes n = 2.

### 3.4 Uniform splitting fixes the dimension scale

Split each of n coordinates into k equal subcoordinates. Then E u_n = u_nk, while Ev repeats v_i/k exactly k times. Isometry gives

    α_n ||v||² = (α_nk/k) ||v||².

For a nonzero tangent v, α_nk = k α_n. Comparing n and m through nm shows

    α_n/n = α_nm/(nm) = α_m/m = c ≥ 0.                     (1)

The comparison uses the family across arbitrarily large finite dimensions.

### 3.5 Rational points reduce to uniform points

Take a rational positive law p_i = k_i/N, with positive integers k_i summing to N. Split coordinate i into k_i equal subcoordinates. Then Ep = u_N, and Ev has k_i copies of v_i/k_i. Hence

    g_n(p)[v,v]
      = α_N Σ_i k_i (v_i/k_i)²
      = c Σ_i v_i²/p_i.                                    (2)

Rational positive laws are dense in Δ_n°, and g_n is continuous. For each fixed tangent v, equation (2) therefore holds for every positive law. Polarization gives the full bilinear form

    g_n(p)[v,w] = c Σ_i v_i w_i/p_i.                        (3)

### 3.6 Integrate the Hessian and exclude the zero scalar

The function H_n(p) = Σ_i p_i log p_i has exactly the tangent Hessian in (3) with c = 1. Thus f_n − cH_n has zero Hessian in affine coordinates on the connected convex simplex. Its gradient is constant, so it is affine. If c = 0, every f_n is affine, contradicting strict convexity. Therefore c > 0.

In particular the tangent Hessian becomes positive definite as a theorem, even though that property did not follow from C² strict convexity alone before imposing the contract.

### 3.7 Converse

Affine terms disappear from Bregman divergences and D_Hn = KL. For each output row, log-sum applied to K_ji p_i and K_ji q_i gives

    (Kp)_j log((Kp)_j/(Kq)_j)
      ≤ Σ_i K_ji p_i log(p_i/q_i).

Terms with K_ji = 0 contribute zero. Summing rows and using the column sums proves KL(Kp || Kq) ≤ KL(p || q). Thus every stated potential satisfies (C). This completes the iff.

## 4. Combination with normalization repair on positive cones

Let C_n = R_{++}^n. Assume each F_n is C², strictly convex, and has ordinary normalization as its first-argument Bregman projection onto Δ_n°. The inherited repair theorem gives

    F_n(sp) = s f_n(p) + a_n(s),
    D_Fn(sp,tq) = s D_fn(p,q) + D_an(s,t),                  (4)

where f_n = F_n|Δ_n° and a_n(1) = 0. Both f_n and a_n are strictly convex. This actual theorem is stronger than testing null attenuation only on already coherent priors; those restricted tests alone do not classify a nonseparable full-cone extension.

### 4.1 Normalized-only contraction

If (C) is imposed only at s = t = 1, the radial term in (4) is zero. Section 3 therefore selects the common KL coherent divergence, but each a_n may be any C² strictly convex radial function independently. Such a family need not contract at unequal masses.

### 4.2 Full-cone contraction forces one radial divergence

Now impose

    D_Fm(Kx,Ky) ≤ D_Fn(x,y)    for every x,y ∈ C_n.        (FC)

Restriction to normalized inputs gives the common c from Section 3. Next choose proportional inputs x = sp, y = tp. Their coherent divergence is zero. Equation (4) gives

    D_am(s,t) ≤ D_an(s,t).

A positive stochastic map exists from any dimension to any other, for example a matrix all of whose columns equal a chosen positive target law. Applying the same argument in the opposite dimension direction gives the reverse inequality. Thus D_am = D_an for all s,t > 0 and all n,m.

Equality of one-dimensional Bregman divergences means a_n − a_m is affine: differentiating twice with respect to the first argument gives a_n'' = a_m'', and integrating twice yields the claim. Under the literal convention a_n(1) = 0 these differences have the form λ_nm(s−1). Thus the invariant object is a shared radial divergence, not literally identical normalized functions before choosing gauges.

Absorb affine coherent and radial terms into an ambient affine potential. We obtain, with one C² strictly convex a,

    F_n(x) ≡ c[Σ_i x_i log x_i − s log s] + a(s),
    D_Fn(sp,tq) = c s KL(p || q) + D_a(s,t).               (5)

Here ≡ means equality up to an affine function of x, and the coefficient of KL is the **first** mass s. Conversely, any family (5) contracts, because K preserves s and t, leaves the shared radial term unchanged, and contracts KL. It also has the required normalization repair by the inherited classification.

Full-cone contraction therefore imposes no further radial shape restriction. The ordinary proof above classifies the intersection of normalization-compatible families and (FC); no broader theorem about all cone Bregman potentials is asserted here.

### 4.3 Metric and countercontrols

In mass/simplex coordinates, the Hessian metric is

    g_F = a''(s) ds² + c s Σ_i (dp_i)²/p_i.               (6)

An everywhere positive-definite cone Hessian additionally requires a''(s) > 0. Strict convexity of a alone allows a'' to vanish at isolated points. For example a(s) = (s−1)^4 remains strictly convex and defines a contracting repair family, while its radial Hessian degenerates at s = 1. Inverse-Hessian flow claims would require the extra nondegeneracy hypothesis.

The smooth choice a(s) = s²/2 gives

    D_Fn(sp,tq) = c s KL(p || q) + (s−t)²/2,

with a positive-definite cone Hessian. This is a concrete non-KL **cone** divergence satisfying all-dimensional contraction and normalization repair, though its normalized divergence is KL.

For normalized-only versus full-cone contraction, choose a_2(s) = s²/2 and a_3(s) = s², ignoring affine gauge adjustments. Both dimensions have coherent KL, but on x = 2p, y = p a map 2 → 3 changes the radial divergence from 1/2 to 1, violating (FC). Subtracting constants to impose a_n(1)=0 changes no divergence.

## 5. Coordinate-additivity is a further premise

Define coordinate-additivity precisely as F_n(x) = Σ_i φ_ni(x_i) up to an affine function, with C² univariate φ_ni on (0,∞). From (5), for distinct i,j,

    ∂_i∂_j F_n(x) = a''(s) − c/s.

An additive potential has zero mixed derivatives. Since every s > 0 occurs in a positive n-vector, this forces a''(s) = c/s, hence

    a(s) = c s log s + A s + B,
    F_n(x) ≡ c Σ_i x_i log x_i,
    D_Fn(x,y) = c Σ_i [x_i log(x_i/y_i) − x_i + y_i].      (7)

Conversely, (7) is coordinate-additive and satisfies the prior contracts. The same restriction follows if divergence is assumed to be a sum of coordinate-pair terms: its mixed second derivatives in the first vector must vanish. No additivity across tensor products or independent experiments is being conflated with coordinate-additivity.

For the quadratic radial countercontrol, the mixed derivative is 1 − c/s, which is not identically zero. It passes (FC) precisely without satisfying this extra premise. This explains why the older separable normalization theorem and the broader nonseparable repair theorem are compatible.

## 6. Essential scope controls

### Fixed binary dimension is not the family theorem

For f_2(p) = ||p||²/2, write p = (r,1−r), q = (t,1−t). Then D_f2(p,q) = (r−t)². Every binary stochastic matrix has columns (a,1−a) and (b,1−b), with a,b ∈ [0,1]. The output first-coordinate difference is (a−b)(r−t), so

    D_f2(Kp,Kq) = (a−b)² D_f2(p,q) ≤ D_f2(p,q).

This is not a scalar multiple of KL: the intrinsic Hessian in r is constant, whereas entropy's is 1/[r(1−r)]. The all-dimensions hypothesis prevents this binary exception. The exact split/coarsen witness from the inherited transport report also shows why resetting Euclidean weights fails: fine divergence 3/64 becomes coarse divergence 1/16 on a recoverable three-to-two submodel.

### Transported-reference quadratics carry different data

The inherited family f_μ(p) = (1/2) Σ_i p_i²/μ_i contracts when μ is also transported to Kμ. The target geometry is selected by (m,Kμ), not by m alone. It is therefore outside the family hypothesis in Section 2, and its positive contraction result survives unchanged. A default choice μ_n = (1,…,1) cannot silently be reset after merging: a block of size two transports to weight two, not weight one. With the inherited three-to-two example, transported weights (2,1) preserve 3/64, while reset weights (1,1) give 1/16.

### Fixed-truth evidence garbling is different again

Under one fixed joint law X → Y → Z and one fixed convex f on the truth simplex, the inherited Jensen identity I_f(X;Y)−I_f(X;Z) = E D_f(P(X|Y),P(X|Z)) is nonnegative for every convex f. That theorem includes Brier. It is not the cross-truth-coordinate contract (C) and does not entail the uniqueness proved here.

### Divergence agreement is not absolute-risk calibration

Affine potential terms cancel from both the divergence and vertex-form Bregman losses D_f(e_i,p). They therefore do not themselves create a different vertex loss. Nevertheless, comparison of divergences across different outcome spaces neither identifies the outcome-dependent utility baselines of arbitrary proper scores nor preserves absolute Bayes risk. Even logarithmic loss has different absolute risk under recoverable splitting: for E(p_1,p_2)=(p_1/2,p_1/2,p_2), fine entropy equals coarse entropy plus p_1 log 2, although KL(Ep || Eq)=KL(p || q). The inherited weighted-quadratic example likewise preserves information gains with a nonzero absolute-risk difference. Thus the classification selects a divergence/geometry contract with one free positive scale; it does not supply an absolute normative utility calibration, justified prior, or justified objective.

## 7. Classical attribution and actual reading

The argument in Section 3 is an elementary form of the classical Chentsov uniqueness mechanism: permutations, congruent Markov embeddings, uniform refinements, rational laws, and continuity. It does not receive fresh priority credit. The root independently supplied the same candidate proof and cone/additivity synthesis in `channel-natural-repair-root-check-20261009/DERIVATION.md`; this worker checked that proof and wrote the explicit hypotheses, source comparison, and controls. This is workflow attribution only.

1. Montúfar, Rauh and Ay, *On the Fisher Metric of Conditional Probability Polytopes* (2014), §3 Definition 1 and Theorem 2, state Chentsov's all-simplex metric uniqueness. Their Theorem 3 records Campbell's positive-cone invariant metric family, and Remark 4 separates the simplex theorem from the cone extension. Actual reading here: the abstract, targeted §3 definitions/theorems/Remark 4, and bibliography entries for Chentsov and Campbell. The unrelated conditional-polytope results were not audited. [Author preprint](https://arxiv.org/pdf/1404.0198).

2. Jiao, Courtade, No, Venkat and Weissman, *Information Measures: The Curious Case of the Binary Alphabet*, IEEE Transactions on Information Theory 60(12), 7616–7626 (2014), §II and §III-C Theorem 4, characterize fixed-alphabet Bregman sufficiency, with an explicit binary exception. §III-A supplies squared binary divergence as a data-processing example. Their fixed-source-and-target-alphabet definitions and closed-simplex potential assumptions are not silently substituted for this report's interior all-dimensions hypothesis. Actual reading: abstract, §II definitions and Remark 1, relevant §III-A example and §III-C theorem/discussion. Appendix C was located but not audited. [Author-hosted paper](https://people.eecs.berkeley.edu/~courtade/pdfs/CuriousCase_TIT2015.pdf).

3. Chentsov's *Statistical Decision Rules and Optimal Inference* (AMS, 1982 English edition), Theorem 11.1, is the classical source identified by the inspected literature. The original book was not read here. Campbell, *An extended Čencov characterization of the information metric*, Proceedings AMS 98 (1986), 135–141, is likewise explicitly credited; its indexed abstract was inspected, but both attempted publisher-PDF opens failed. No full-original-source reading is claimed. [Campbell DOI](https://doi.org/10.1090/S0002-9939-1986-0848890-5).

4. Fujiwara, *Hommage to Chentsov's theorem* (published online 2022; Information Geometry 7, 79–98, 2024), §1 independently verifies the Chentsov attribution and precise Markov-invariance statement. Only the introduction and beginning of §2 were used; the appendix concerns affine connections and was not used as a metric proof. [Publisher text](https://link.springer.com/article/10.1007/s41884-022-00077-7).

The inherited nonseparable repair packet separately credits Nock–Menon–Ong's scaled Bregman theorem for the perspective identity. That original paper was not reread in this operation. Literature discovery was targeted, not an exhaustive novelty clearance.

## 8. Comparison with inherited programme coverage

The source pin is 7efc6217c090b92d65f2c4cb8b011c18eb96bf7c. `INPUT_BASELINE.json` and `SOURCE_LEDGER.json` bind the exact local bytes and disclose which reading was actually done.

- The inherited local-Hessian note, Setup and S1–S2, already studies common scorewise repairs and additive-score rigidity. S6 already distinguishes identical normal correction from inequivalent tangent geometry. Those hypotheses compare repairs for two score families on a fixed simplex; they do not impose (C). Their conclusions are preserved.
- The separable Bayes-repair predecessor, §4 Theorem 3, already selects a common entropy generator under normalization-compatible separable ambient repair. It works also in dimension two. That is a different hypothesis from binary channel contraction alone.
- The nonseparable repair result, §§3–5, proves the perspective-plus-radial classifier and divergence split. It supplies the ambient input here and is not replaced by an assumed separable form.
- The geometry-transport result, §§2–6, proves the Hessian iff, reset-Brier failure, fixed-truth garbling theorem, and transported-reference quadratic positive construction. It explicitly declines an anonymous-family characterization. The present operation supplies that missing cross-dimensional classification with classical attribution, while retaining the different structured-reference contract.
- The pinned sound-descent model comparison, G1/G2 sections, keeps literal differentiable geometry conditional on an explicit state space, metric, objective, and semantics. Channel-natural uniqueness does not discharge those declarations or empirical/normative warrant obligations.

The parent's earlier repository search for “Chentsov” had no results. That limited search is neither exhaustive absence evidence nor novelty evidence. This operation does not claim a complete repository or historical literature search.

## 9. Verification and stopping boundary

`verify.py` executes symbolic identities and exact rational controls for splitting/recovery, Fisher transport, binary contraction, reset versus transported quadratic weights, radial mismatch, the cone divergence split, mixed derivatives, affine gauges, and radial Hessian degeneracy. It checks that all six bound predecessor inputs remain byte-identical. These finite checks supplement the ordinary proofs; they do not prove the universal theorem or claim Lean certification.

No protected source was edited. No integration, adoption, publication, release, T20 closure, or T21 transition was performed. Selecting the all-channel contract instead of a declared-reference contract remains a modeling choice requiring its own justification. A uniqueness theorem conditional on that choice does not identify a true prior, establish an actual psychological model, settle metaphysical normativity, or establish warrant for a source. Further source or formal verification is prospective unless explicitly recorded in this packet.
