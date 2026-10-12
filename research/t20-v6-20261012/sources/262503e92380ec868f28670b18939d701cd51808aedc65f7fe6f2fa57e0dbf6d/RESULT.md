# Effective recovery of capped countable laws from tensor moments

10 October 2026 UTC. Additive ordinary mathematical research in ACTIVE T20.
No protected edit, canonical integration, field-priority claim, fresh Lean/kernel claim, empirical inference, sampling-optimization programme, or T20 closure.

## 1. Result and inherited ownership

Known countably many channel columns do admit effective full-law recovery from their complete tensor moments when a common effective summable cap is supplied. The output is an arbitrarily accurate ℓ¹ name of the indexed law. More strongly, for each requested accuracy one can compute a finite moment degree and a positive precision threshold that work uniformly over that fixed capped domain. A finite rational moment-band record then supports a terminating containment-certificate search for an approximate law.

These conclusions do not imply one fixed finite exact moment cutoff. If the cap has total mass strictly greater than one and infinitely many positive coordinates, every fixed finite cutoff has different cap-admissible laws in a common fibre. Conversely, cap total one gives a singleton domain. Without effective cap tails, full moments can be uniformly computable while the unique indexed law is noncomputable, even for a fixed computable support in the binary simplex.

The ownership boundary is important:

- `tensor-moment-continuation-20261009/RESULT.md`, §§3–5, already proves finite known-support tensor recovery and exact tilt continuation. It distinguishes duplicate-column aggregates from fine labels and the graded product from the algebraic direct sum.
- `measure-moment-continuation-boundary-20261009/RESULT.md`, §3, already proves compact-support full-moment determinacy, including infinitely many channel columns, and explicitly makes no effective-recovery claim. Its noncompact lognormal counterexample and unbounded-output limitations remain unchanged.
- `effective-stationary-selection-20261010/RESULT.md`, §4, already proves effective upper compactness of the cap envelope and uniform computation of a unique computable zero. The present proof transports that machinery to the injective moment map, rather than presenting it as a new selection theorem.
- The retained T10 `MINIMAL_ADDENDUM.md`, §1, already supplies compact finite-warrant reasoning and its effective upper-compact input requirement. The present finite moment-band certificates instantiate that reasoning in ℓ¹.
- The earlier countable-signature result at CP02 concerns finite integer route histograms, an exact rational multiplicative code, and its approximation-oracle boundary. It does not identify this capped infinite real-weight moment problem with that different representation.

A bounded scan of 68 direct local `RESULT.md` records, the actual relevant later records, the retained four-entry T10/T18 registry excerpt, and targeted repository searches found these ancestors and no already completed capped ℓ¹ moment-recovery theorem in the inspected material. Searches are discovery evidence, not an exhaustive absence or novelty certificate. Precise paths and source scopes are recorded separately.

The classical mathematical ancestry is polynomial density, measure uniqueness, and effective compact inversion. For primary polynomial-density ancestry, M. H. Stone's 1948 paper is the historical source; the directly inspected research proof is Louis de Branges, *The Stone-Weierstrass Theorem*, Proceedings AMS 10 (1959), 822–824, especially the theorem and proof on pp. 823–824: https://sites.math.rutgers.edu/~zeilberg/purdue22/LdeBstone.pdf . For effective compact zeros, Galatolo–Hoyrup–Rojas, *Dynamics and abstract computability: Computing invariant measures*, Theorem 2.9 and Remark 5, explicitly give uniform unique-zero computation: https://members.loria.fr/MHoyrup/computinvmeas.pdf . These general mechanisms are prior mathematics. The project-relative addition is their represented-input transport, finite-data certificate, and matched boundary controls here.

## 2. Exact representation contract

Fix a finite dimension d≥1 and the closed probability simplex

    Δ_d = {z∈R^d : z_a≥0, Σ_a z_a=1}.

The input includes:

1. A known sequence `(κ_j)_(j≥0)` in Δ_d, uniformly computable in j, with the promise that its vectors are pairwise distinct. Uniformly computable means a single algorithm, on `(j,a,k)`, returns a rational within `2^−k` of coordinate a. No support-separation radius, computable inverse indexing, decidable real equality, or discrete/closed support set is required.
2. Nonnegative cap coordinates c_j, uniformly computable, and a supplied computable tail modulus m with `Σ_(j≥m(k)) c_j ≤ 2^−k`. The total C=Σ_j c_j is promised at least one. These data compute c in ℓ¹ and C as a real.
3. A complete moment name `(A_r)_(r≥0)`, uniformly in grade, tensor coordinate, and precision, with the promise that for some p in

    K_c = {p∈ℓ¹ : 0≤p_j≤c_j, Σ_j p_j=1}

one has

    A_r = M_r(p) = Σ_j p_j κ_j^⊗r,     r≥0,     A_0=1.

The validity and distinctness promises are premises, not decidable tests supplied by the theorem. Saying each A_r separately has some computable name is insufficient unless these names are available uniformly in r. Equivalently, the recovery is a Type-2 operation relative to the input names; when those names are computable, its output is computable.

Each grade is represented as its finite array of d^r ordered coordinates, with the maximum norm. Symmetry is automatic. A symmetric-coordinate encoding is equivalent, but its multiplicities must be declared. Every grade has nonnegative entries, coordinate sum one, and maximum norm at most one. The full sequence lies in the graded product `Π_(r≥0) Sym^r(R^d)`, not the algebraic direct sum: contracting against the all-ones covector in every slot gives one in every grade. A finite prefix is a legitimate finite graded record.

An ℓ¹ name of p returns a finitely supported rational vector q_k with `||q_k−p||₁<2^−k`. The approximants need not themselves lie in K_c. This is exact recovery in the computable-analysis sense, not a finite list of rational coordinates equal to the whole law.

Zero cap coordinates force zero weights; no algorithm needs to decide which caps vanish. The domain is nonempty because c/C∈K_c. Pairwise distinctness could be weakened to injectivity of the moment map on the actual constrained domain, but the stated support premise is an explicit sufficient condition.

An effective tail need not arrive as separately supplied metadata: nonnegative uniformly computable coordinates together with a computable exact total C also produce one. For each requested tail bound, search for a finite partial sum certified within that bound of C. Classical summability or a computable upper bound on C alone does not provide this equivalent information.

## 3. Computable moments and classical injectivity

### Lemma C1: the moment map is computable

For every r≥0, the linear map

    M_r(x)=Σ_j x_j κ_j^⊗r

is defined on all of ℓ¹, computable uniformly in r, and has norm at most one from ℓ¹ to the grade's maximum norm. In fact the analogous grade ℓ¹ norm also has operator norm at most one.

**Proof.** Since `||κ_j^⊗r||₁=1`, absolute convergence and

    ||M_r(x)−M_r(y)||∞ ≤ ||M_r(x)−M_r(y)||₁ ≤ ||x−y||₁

follow directly. Approximate x in ℓ¹ by a finite rational vector, evaluate its finitely many computable support tensors to sufficient accuracy, and use this norm bound for the input error. All finite tensor dimensions and products are effectively obtained from r and d. No cost bound is asserted. ∎

On K_c, finite truncation may instead use the supplied cap tail directly. The map's computability does not require distinctness; distinctness is used only for its inverse.

### Lemma C2: complete moments identify the indexed law

If p,q are probability laws on the known pairwise distinct support and `M_r(p)=M_r(q)` for all r, then p=q, whether or not either law obeys a cap.

**Proof.** Put `μ_p=Σ_j p_j δ_(κ_j)` and similarly μ_q, as Borel probabilities on the compact simplex. Tensor coordinates are coordinate monomials, so moment equality gives equality of integrals of every polynomial. Coordinate polynomials restricted to Δ_d contain constants and separate points. Stone–Weierstrass gives density in C(Δ_d), and uniform approximation gives equal integrals of all continuous functions.

For completeness, this last equality determines the measures: for any closed F⊂Δ_d, the continuous functions `f_n(z)=max(0,1−n dist(z,F))` decrease to its indicator, so dominated convergence gives μ_p(F)=μ_q(F). Closed sets form an intersection-stable generating class for the Borel sigma algebra, and finite-measure uniqueness gives equality on every Borel set. In particular

    p_j = μ_p({κ_j}) = μ_q({κ_j}) = q_j,

because the support sequence is injective. ∎

Support accumulation causes no failure of this equality proof. A singleton remains a Borel set even if other κ_i accumulate at it; no continuous singleton indicator or isolated atom is presumed. Computing that singleton mass without the cap is a different question, addressed in §7.

**Duplicate columns.** If κ_i=κ_j for different labels, moments see only the aggregate mass on their common value. For example, with those two labels and cap (1,1), `(1/3,2/3)` and `(2/3,1/3)` have every tensor moment equal. The positive inverse theorem must not reconstruct these hidden allocations. A supplied effective listing of distinct aggregate support values with effective aggregate caps gives the same theorem for aggregate weights; merely having computable original columns does not supply a decidable equality partition or that listing. Constraints can exceptionally determine an allocation despite duplicates, as in a singleton K_c, but duplicates alone never justify indexed-law recovery.

## 4. Uniform ℓ¹ recovery by a unique zero

### Lemma C3: effective upper compactness

The supplied cap makes K_c uniformly effectively upper compact: for each effectively open U⊂ℓ¹, `K_c⊂U` is semidecidable. The same holds for K_c×K_c.

**Proof summary of the inherited E2 construction.** The box `B_c={x:0≤x_j≤c_j}` has computable finite nets: truncate at a supplied small cap tail, use a finite rational mesh in the remaining coordinates, and clip mesh points by the computable map `u↦min(u,c_j)`. Approximate those finitely many computable centers by rational ideal points with budgeted error. Refining the nets semidecides every genuine finite open-ball cover by strict margins, and dovetailing finite subfamilies handles an enumerated open set. Completeness and the same uniform tails prove ordinary compactness.

The sum S(x)=Σ_jx_j is a computable continuous functional and

    K_c⊂U  iff  B_c⊂U∪{x:S(x)≠1}.

Thus no decision of which grid points satisfy exact normalization is needed. For the product, interleave two copies of c to get an effective compact box and impose the two computable closed sum constraints separately. This gives K_c×K_c in the sum product metric. ∎

### Theorem C4: computable exact inverse on the promised class

The complete moment name computes the unique p∈K_c uniformly in the supplied support, cap, and their names.

**Proof.** Define on K_c

    ρ_A(x) = Σ_(r=1)^∞ 2^−r ||M_r(x)−A_r||∞.

All terms are nonnegative and at most 2^−r. Truncating after grade R has error at most 2^−R. Lemma C1 and the uniform moment name therefore compute ρ_A; it is 1-Lipschitz in x. Its zero set Z is exactly `{p}` by validity and Lemma C2.

For any effectively open U,

    Z⊂U  iff  K_c⊂U∪{x:ρ_A(x)>0}.

The right side is semidecidable by Lemma C3. To obtain error less than 2^−k, enumerate all finitely supported rational centers q and run these semidecisions in parallel for `U=B₁(q,2^−k)`. A center within half that radius of p exists, so at least one search terminates. Every returned center approximates the same unique p within the requested error. This is the inherited effective compact singleton method applied to the moment residual. ∎

If an ambient total computable extension is desired, replace each norm term by its minimum with one. This leaves the zero set unchanged and supplies the same uniform tail bound on all of ℓ¹; the argument only needs computability on K_c.

The theorem never decides exact zero of an arbitrary real, support equality, validity of a moment name, or uniqueness in an arbitrary inverse problem. The algorithm is allowed not to terminate on invalid inputs. Finite successful computations query only finitely many grades and precision requests, but the next theorem provides a domain-uniform finite requirement before the particular law is known.

## 5. Finite grade/precision certificates and actual approximate output

### Theorem C5: effective uniform finite moment separation

From the support and effective cap, and any rational ε>0, one can compute integers R≥1 and n≥0 such that for every p,q∈K_c,

    max_(1≤r≤R) ||M_r(p)−M_r(q)||∞ ≤ 2^−n
        implies ||p−q||₁ < ε.                                  (1)

Both R and the precision threshold depend on this support and cap. They are uniform over the laws in that domain, not a universal numerical bound independent of the inputs.

**Proof.** For each R,n form the effectively open set

    U_(R,n) = {||p−q||₁<ε}
              ∪ ⋃_(1≤r≤R) {||M_r(p)−M_r(q)||∞>2^−n}.

Lemma C3 semidecides `K_c²⊂U_(R,n)`. Search all R,n in parallel. Every pair either has distance less than ε or is distinct, in which case Lemma C2 gives a positive difference in some grade. Thus the U_(R,n) cover K_c². They increase with R and n, so compactness gives one such U_(R,n) covering the entire product. The search terminates, and the accepted inclusion is exactly the contrapositive of (1). ∎

For the bounded moment metric

    d_M(A,B)=Σ_(r=1)^∞ 2^−r ||A_r−B_r||∞,

(1) gives an effective uniform inverse modulus, for example `d_M(A,B)≤2^−(R+n)` implies its premise. The main certificate is (1), which uses a finite prefix directly and does not require summing an infinite observed record.

### Corollary C6: finite rational data produce an approximate law

Given ε>0, first apply C5 with ε/2 to obtain R,n and put δ=2^−n, η=δ/4. Suppose rational arrays a_1,…,a_R are provided, with the promise that

    F = {p∈K_c : ||M_r(p)−a_r||∞≤η for every 1≤r≤R}

is nonempty. Then one can compute a finitely supported rational center q and a terminating open-cover certificate that every p∈F has `||p−q||₁<ε`.

**Proof.** If p,p′∈F, their moment differences through R are at most 2η=δ/2≤δ, so C5 gives `||p−p′||₁<ε/2`. Thus F has diameter at most ε/2. It is effectively upper compact, since

    F⊂B₁(q,ε) iff
    K_c⊂B₁(q,ε) ∪ ⋃_(r=1)^R {||M_r(p)−a_r||∞>η}.              (2)

All sets on the right are effectively open. Enumerate rational ideal centers q and semidecide (2). For any p*∈F, a rational q within ε/4 of p* exists; then all of F lies within 3ε/4 of q. So a certificate is eventually found. Its right side contains only finitely many moment bands and an effective compact containment assertion. ∎

A valid complete moment name supplies such a_1,…,a_R by requesting error at most η in every coordinate. Thus this is an actual approximate-output algorithm from finitely much certified data, not only a claim that all compatible laws are close. The output center need not satisfy the exact cap or normalization; its guaranteed distance is to every genuine compatible law. No dense enumeration of K_c points or exact cap membership test is used.

The validity of the cap-tail name and the data error bounds remains part of the input contract. A finite certificate is a terminating trace of strict rational margins in the effective upper-cover procedure, relative to those valid names; this note does not claim to have implemented a universal checker or to certify arbitrary data acquisition. If F is empty the inclusion tests can succeed vacuously. No correct diagnosis or law-recovery guarantee is asserted without the nonempty-consistency promise.

These precision statements concern exact mathematical names and valid enclosures. There is no random sample, confidence level, experiment budget, statistical noise model, or optimization of R,n here.

## 6. Every fixed finite exact cutoff fails on a genuinely infinite cap domain

### Theorem C7

If C>1 and infinitely many c_j are positive, then for every fixed R≥0 there exist distinct p+,p−∈K_c with identical tensor moments through grade R.

**Proof.** Put b=c/C. On every positive-cap coordinate,

    0<b_j<c_j.

The finite prefix moment map, including its mass coordinate M_0, has a finite-dimensional codomain of dimension at most `D_R=Σ_(r=0)^R d^r`. Choose more than D_R distinct positive-cap indices, possible by the hypothesis. Their finite feature columns `(1,κ_j,…,κ_j^⊗R)` have a nonzero real linear dependence h. Extend h by zero to the other coordinates. Then

    Σ_jh_j=0,    M_r(h)=0 for 1≤r≤R.

The support of h is finite and b has positive slack on both sides there. Choose t>0 so that `t|h_j|<min(b_j,c_j−b_j)` whenever h_j≠0. Then p±=b±th belong to K_c, have the same normalization and moments through R, and are distinct. ∎

This proof uses an ordinary finite linear dependence and does not need an algorithm to decide ranks of arbitrary named real matrices. It is not claimed that every finite prefix fibre is nontrivial or that every individual law needs infinitely many grades. It says no one finite cutoff is injective on this whole capped domain. It does not rule out other encodings or contradict C5's accuracy-dependent finite certificates.

If C=1, the nonnegative coordinates c_j−p_j sum to zero for every p∈K_c, so p=c and no moment is needed. If only finitely many cap coordinates are positive, the inherited finite-support theorem supplies a finite exact cutoff after those active distinct support values are specified. Effectively discovering an unknown finite active support from real-coordinate names is a separate representation problem, not promised here.

## 7. What goes wrong without effective tails

### 7.1 Accumulating support separates the topologies

Let

    κ_0=(0,1),    κ_j=(2^−j,1−2^−j), j≥1.

These are a fixed uniformly computable pairwise distinct sequence in Δ_2. For the indexed laws δ_j and δ_0,

    ||δ_j−δ_0||₁=2,
    ||M_r(δ_j)−M_r(δ_0)||∞≤r2^−j.

The second bound follows by telescoping a product of r factors in [0,1], each changing by at most 2^−j. Each grade therefore converges, and the bounded product metric obeys `d_M(M(δ_j),M(δ_0))≤2^(1−j)`, because Σ_r r2^−r=2. The inverse is discontinuous at the valid moment record of δ_0 on this uncapped domain, so it is not a Type-2 computable inverse for the standard moment/ℓ¹ representations. There cannot even be one uniform finite-precision requirement on this domain.

Every one of these Dirac laws is individually computable. This example by itself does not exhibit an individual noncomputable recovered law. It also does not prove that every support without a supplied cap has discontinuous inverse. In particular, pointwise continuity and uniform continuity are different when accumulation occurs only outside the listed atoms. A summable common cap cannot contain all these Diracs, since it would require c_j≥1 for every j. The positive theorem therefore does not apply to this sequence of laws.

### 7.2 A computable full moment name can identify a noncomputable law

The following sharpened control was developed with a participating reviewer; it is a new-to-this-packet construction using classical halting encoding, not an independent reviewer rediscovery or a field-priority claim. A different reviewer independently checked this subsection; that scoped check is recorded separately in `hidden-mass-independent-review-20261010/REVIEW.md`.

Keep the exact support in §7.1. Fix an effective machine enumeration and its undecidable diagonal halting set H. Let

    w_e=4^−(e+1),    α=Σ_(e∈H) w_e,    0≤α≤1/3.

The real α is noncomputable. Indeed, after deciding the earlier digits, the residual at e is at least w_e if e∈H and at most w_e/3 if e∉H. Approximations of a computable α with error, say, w_e/12 would decide these alternatives successively using threshold 2w_e/3, and hence decide H.

Use the Cantor bijection `⟨e,t⟩=(e+t)(e+t+1)/2+t` from ℕ² to ℕ. Assign each positive index uniquely by `j=1+⟨e,t⟩`, and define

    p_j = w_e if machine e on input e first halts at exactly stage t,
          0 otherwise,                                      j≥1;
    p_0 = 1−α.

A stage convention starts with the initial configuration at t=0; whether the first halt is exactly t is determined by simulating the finite t steps and checking prior configurations. Thus the positive-index coordinates are uniformly computable rationals, their total is exactly α, and p is a probability. But p_0, hence the ℓ¹ law p, is noncomputable.

Nevertheless all tensor moments have the uniformly computable formula

    M_r(p) = κ_0^⊗r
             + Σ_(j≥1) p_j (κ_j^⊗r−κ_0^⊗r).                 (3)

For r≥1, the maximum-norm error after retaining 1≤j<N is at most

    Σ_(j≥N) p_j r2^−j ≤ r2^−N Σ_(j≥N)p_j ≤ r2^−N.

For strict error less than 2^−k, take `L=min{ℓ≥0:2^ℓ≥r}` and `N=k+L+1`. Every retained coefficient and tensor is rational and exactly computable by finite simulation. Grade zero is one. This is a single uniform algorithm for all grades and coordinates. The noncomputable baseline mass has cancelled from (3); pretending to evaluate p_0 directly would miss the point of the construction.

Now supply c_0=1 and c_j=p_j for j≥1. These cap coordinates are uniformly computable, c is classically summable with `C=1+α≤4/3`, and p∈K_c. There can be no computable cap-tail modulus, since it would compute C and hence α. The bound 4/3 is computable; the exact total C is not. Supplying a computable exact total would restore an effective tail by §2 and is expressly excluded from this control. Thus replacing effective summability by coordinate computability plus classical summability makes C4 false even for a fixed computable support and a genuinely valid computable complete moment name. Lemma C2 still gives unique indexed-law determination.

The small cap total does not contradict the inherited stationary-law contraction result: no computable row-dominated Markov operator having this p as its stationary law is supplied here. A constant-row operator with row p would itself have a noncomputable entry. The moment-inverse and selected-operator input contracts are different.

## 8. Bounded continuation remains computable, with an enlarged cap

Let a finite cumulative control u∈R^d be computably supplied. On the known support define

    Z_p(u)=Σ_j p_j exp(−u·κ_j),
    (T_u p)_j = p_j exp(−u·κ_j)/Z_p(u).

Given a computable bound `||u||∞≤B`, simplex membership gives

    exp(−B)≤exp(−u·κ_j)≤exp(B),
    Z_p(u)≥exp(−B),
    (T_u p)_j≤exp(2B)c_j.                                  (4)

Recovered ℓ¹ p, the uniform support names, bounded multiplication, and the positive denominator compute T_u p in ℓ¹. The cap `exp(2B)c` has an effective tail modulus, obtained by requesting sufficiently small tails of c against a computable rational upper bound for exp(2B). The original cap generally is not invariant under a tilt.

Thus the full moment name also computes each admitted bounded-simplex tilt as an indexed ℓ¹ law and expectations of observables uniformly computable on the indexed support with a supplied uniform bound. For a finite-horizon control given by finitely many computable piecewise-constant covectors and computable switch times, u(t) and a finite B bound are computable, so the same argument applies uniformly over that horizon. The semigroup identity `T_v T_u=T_(u+v)` follows by cancellation of normalization exactly as in the finite ancestor. No finite exact moment closure or generic scalar separating projection is inferred.

### Direct moment continuation needs no cap

The preceding indexed-law reconstruction is stronger than what the original bounded channel-output interface needs. The compact exponential series already proved in `measure-moment-continuation-boundary-20261009/RESULT.md`, §3, has an effective consequence without any cap. Given a valid uniform complete moment name of any probability law on Δ_d and computable u with `||u||∞≤B`, define the unnormalized grade-s numerator

    N_s(u) = Σ_(r=0)^∞ (-1)^r/r! · contract_(u,r)(M_(s+r)),
    M_s(T_u μ) = N_s(u)/N_0(u).

Here `contract_(u,r)` contracts exactly the last r slots against u, without multiplicity factors; at r=0 it is the identity. For each output coordinate, the integral integrand is a product of s simplex coordinates times `exp(−u·z)`. That product is at most one in absolute value. Truncation after r=R therefore has error at most

    exp(B) B^(R+1)/(R+1)!,

by the scalar exponential Taylor remainder uniformly over Δ_d. A computable rational bound on B and exp(B) makes this an effective tail bound, while `N_0(u)=Z_μ(u)≥exp(−B)`. Thus all updated tensor grades, and in particular the original channel output M_1, are uniformly computable directly from the full moment name. This uses no support indexing, cap, or recovered ℓ¹ law.

Consequently the counterexample in §7.2 has computable bounded tensor/output continuation despite its noncomputable indexed law. The cap is a sufficient effective compactness hypothesis for the stronger ℓ¹ inverse theorem; it is not necessary for effective continuation of this original bounded-moment interface. This is an effectivity deduction from the inherited convergent series, not a new field-level tilt formula or a sampling bound.

Nor does this cap-free corollary compute every bounded computable indexed observable: the indicator of index zero is such an observable, and its expectation in §7.2 is the noncomputable p_0. What is computed here is the explicitly displayed tensor-moment/output family.

Recovering an ℓ¹ name alone does not compute every finite unbounded expectation. The earlier noncompact raw-trait mean and the `−log s` output still require their own effective weighted-tail/integrability information. The inherited noncompact moment-indeterminacy result is unaffected.

## 9. Evidence and claim ceiling

The universal claims C1–C7 and the no-tail construction are ordinary written proofs. The accompanying `check_controls.py` passed 1,304 exact-rational checks: finite moment collisions inside an explicit infinite cap, mass/cap margins, tensor-coordinate identities, duplicate aliases, accumulation bounds, band arithmetic, bounded reweighting/cap enlargement, and direct tilt-series coefficient identities. They do not prove universal computability, halt-set noncomputability, or termination of every promised-input cover search by running finitely many examples.

No general recovery engine, cost estimate, optimum cutoff, unknown-support recovery, empirical identification, population/sample equivalence, physical realization, source ownership, or metaphysical identity is claimed. Existing finite, compact, noncompact, effective stationary, and inherited formal results remain in their exact original scopes and bytes.
