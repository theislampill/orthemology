# CV-C — exact index sets with a concrete reduction binding

Mathematical status: ORDINARY_PROOF. Concrete numbering: **P02-L1**, defined and implemented in `CV_C_CODEC_AND_CORRESPONDENCE.md` and `code/prcodec.py`. The original source's abstract total-PR numbering is preserved; these are new explicit codes with an ordinary equivalence-of-expressive-class proof, not recovered historical indices. No claim of priority or external review is made.

## C2-08. Measure and soft-mass representation

Use fair product probability λ on `2^ℕ` with its product Borel σ-algebra. For each natural index e use the total synchronous q_e of C2-05, including invalid-code zero semantics, and set ν_e=(q_e)_*λ. Its cylinder probabilities are the exactly computable dyadic values

`p_e(σ)=2^-n #{u∈2^n:output_e(u)=σ}`, for |σ|=n.

For k,n≥0 define `B_e(k,n)=Σ_(|σ|=n) max(p_e(σ)-2^-k,0)`. It belongs to [0,1], increases with k and decreases with n: when a cylinder of mass p is split into masses p0+p1=p, `max(p0-ε,0)+max(p1-ε,0)≤max(p-ε,0)`.

For y∈2^ℕ let m_n(y)=ν_e[y↾n]. These measurable functions decrease to ν_e{y}, since the cylinders decrease to {y} and ν_e is finite. Put `φ_ε(0)=0`, and for t>0 put `φ_ε(t)=max(1-ε/t,0)`. It is continuous at every t≥0, including zero because it vanishes on [0,ε], and bounded by 1. On each cylinder the integral contributes `p max(1-ε/p,0)=max(p-ε,0)` (zero if p=0). Therefore

`B_e(k,n)=∫φ_(2^-k)(m_n(y))dν_e(y)`.

Dominated convergence gives

`b_e(k):=inf_n B_e(k,n)=∫φ_(2^-k)(ν_e{y})dν_e(y)`.

The integrand vanishes off the countable positive-singleton set S(ν_e), so this is `Σ_(y∈S)max(ν_e{y}-2^-k,0)`. As k→∞ the integrands increase to 1_S. Monotone convergence proves

`a_e:=a(ν_e)=sup_k inf_n B_e(k,n)`, `d_e=1-a_e`.

No sample-size truncation replaces either limit. U05 supplies the countable/measurable S and the normalized measure semantics; no fixed-point theorem is used.

## C2-09. Membership at every rational threshold

For rational r,

`a_e>r iff ∃k ∃t∈ℚ [t>r ∧ ∀n B_e(k,n)≥t]`.

Forward: choose k with b_e(k)>r, then rational t strictly between them. Reverse: the universal lower bound gives b_e(k)≥t>r. The rational gap is essential; `∀n B_e(k,n)>r` alone could have infimum exactly r.

The right side is Σ⁰₂, since B is uniformly computable and rational comparison decidable. This does **not** assert that the universal PR-program evaluator is primitive recursive in e. For an explicitly PR matrix, let T(e,k,t,n,s) mean that bounded simulation through s steps of the total cylinder-comparison algorithm has not returned false. Then `∀n B_e(k,n)≥t` is exactly `∀n∀s T(e,k,t,n,s)`. Bounded machine simulation is PR, and pairing n,s keeps the same universal block. The comparison t>r is an exact integer/rational test. Hence this normal-form conversion does not add an alternation or assume a uniformly PR evaluator. Also

`a_e≥r iff ∀j≥1 a_e>r-2^-j`,

which is Π⁰₃ after expanding the previous formula. Complementation and d=1-a give the upper bounds below. For `0<q<1`, equality d=q is the conjunction of the Π⁰₃ condition d≤q and the Π⁰₂ condition d≥q, hence Π⁰₃. These are formulas over **indices**, not over arbitrary unencoded measures.

| Index set, fixed rational 0<q<1 | Membership |
|---|---|
| {e:d_e<q} | Σ⁰₂ |
| {e:d_e≥q} | Π⁰₂ |
| {e:d_e≤q} | Π⁰₃ |
| {e:d_e>q} | Σ⁰₃ |
| {e:d_e=q} | Π⁰₃ |

At the endpoints, {d=0} is Π⁰₃, {d>0} Σ⁰₃, {d=1} Π⁰₂, {d<1} Σ⁰₂. The sets d<0 and d>1 are empty; d≥0 and d≤1 are all indices. Thus d≤0=d=0 and d≥1=d=1. Thresholds outside [0,1] reduce by the same order facts. No strict comparison is silently interchanged with a non-strict one.

## C2-10. Σ⁰₂/Π⁰₂ hardness using `compile_sigma2`

Take any Σ⁰₂ set A in normal form `e∈A iff ∃s∀t R(e,s,t)`, where R is a fixed PR boolean predicate. By C2-03 compile R to an arity-three P02-L1 matrix. Let r_e(u) be the least surviving candidate defined in C2-06.

Once a candidate s fails a bounded test, that specific counterexample remains visible at every later stage. Hence r_e is nondecreasing. If a permanent witness s exists, let s* be the least one. All finitely many smaller candidates have finite counterexamples; eventually these and s* itself lie within the bounds, so r_e(u)=s* forever. If no permanent witness exists, every fixed candidate is eventually refuted; r_e(u) tends to infinity and changes infinitely often.

The actual compiled observer reveals a fresh independent input bit exactly at changes and writes zero elsewhere. If there are finitely many changes, its output distribution has finite support, so d=0. If there are infinitely many, any specified output stream constrains at least k independent fair coordinates for every k, so its probability is ≤2^-k and hence zero; d=1. Thus

`e∈A iff d_(encode(compile_sigma2(R,e)))=0`.

For every fixed 0<q<1 this equivalently reduces A to d<q; it also reduces A to d<1. The map from e to the emitted numeric observer code is primitive recursive by C2-02. This proves Σ⁰₂ hardness without an unimplemented “standard compiler” or a borrowed FIN label. Applying the same compiler to the complement characterization proves Π⁰₂ hardness of d≥q and d=1.

## C2-11. Π⁰₃/Σ⁰₃ hardness using `compile_pi3`

Take any Π⁰₃ set A in normal form `e∈A iff ∀i∃s∀t R(e,i,s,t)` with PR R. Compile R as an arity-four matrix. The actual observer copies the first selector word 1^i0, of probability w_i=2^-i-1, then uses the row-i change observer on the independent tail. The all-ones selector stream has probability zero and remains productive.

Conditioned on selecting i, the row law has defect 0 iff that row has a permanent witness and 1 otherwise, by C2-10. Prefixing by a finite word is an injective measurable map of Cantor space preserving all singleton masses; different row prefixes are disjoint. More importantly, the general countable-mixture identity M2-04 applies, so

`d_(compile_pi3(R,e))=Σ_i 2^-i-1 · 1[¬∃s∀t R(e,i,s,t)]`.

Every w_i is positive, and the terms are nonnegative. The sum is zero iff every row is good. Therefore e∈A iff the compiled observer has d=0. This is an explicit PR many-one reduction bound to the code, giving Π⁰₃ hardness of zero defect. Complementation gives Σ⁰₃ hardness of positive defect. It neither uses nor presumes the result of another packet.

## C2-12. Arbitrary rational thresholds via `compile_shift`

For q=a/b∈[0,1], the dyadic interval selector stops almost surely: after n bits at most one length-n cylinder straddles a non-dyadic q, of probability 2^-n. For dyadic q every interval at sufficiently fine depth lies on one side. Endpoints terminate after a harmless copied bit in the implemented version.

The stopping words form a countable prefix-free set, split into below words of total mass q and above words of total mass 1-q. The total unresolved set has mass zero. The implementation copies each stopping word, then produces an independent fair diffuse stream below q, or the base observer's law on fresh tail bits above q. Prefixing preserves defect. M2-04 therefore proves the exact relation

`d_shift=q+(1-q)d_base`.

For 0<q<1, d_shift≤q iff d_base=0, d_shift=q iff d_base=0, and d_shift>q iff d_base>0. Applying this explicit compiler to the C2-11 reductions proves Π⁰₃ hardness of d≤q and d=q, and Σ⁰₃ hardness of d>q. Combined with C2-09 and C2-10, **all entries of the threshold and endpoint table are complete** under computable many-one reductions, with PR code transformers available for the displayed constructions.

The use of arbitrary rational q is not restricted to dyadic mixtures. The selector has potentially unbounded stopping depth but each individual output stage performs a bounded prefix computation. Therefore the resulting observer remains synchronous and syntactically total PR. Almost-sure selector resolution does not mean that every bit sequence resolves it.

## C2-13. Exact scope of the classification

The result is for the natural-number indices of **the declared total PR prefix observer class driven by fair Cantor input**. Within that class, invalid indices are fixed zero programs. The same construction applies to any effectively equivalent numbering with computable translations in both directions; no such translation to absent historical bytes is claimed.

Finite Mealy machines have a separate decidable representation. General computable synchronous observers form a larger class; one must specify a totality promise or an index convention for partial programs before assigning a hierarchy. Arbitrary measurable observers have no supplied effective numbering. No table above is transferred to either broader class. Similarly, an unknown or noncomputable input law would invalidate the uniformly computable dyadic cylinder matrix. These are necessary semantic restrictions, not optional implementation choices.

## C2-14. Finite Mealy theorem and implementation correspondence

The predecessor supplies the exact rational implementation and 46,656-machine census, retained unchanged inside the original ZIP. Let S be finite nonempty, with δ:S×2→S and output o:S×2→2, driven by fair independent bits. Define E as the greatest subset of S² such that `(s,t)∈E` implies, for all b,c∈2, equal outputs and `(δ(s,b),δ(t,c))∈E`. Let D={s:(s,s)∈E}.

Starting with S² and deleting violating pairs terminates after at most |S|² strict deletion rounds. At the kth approximation a pair agrees under all pairs of input words through the corresponding finite depth, by induction. The stable relation therefore gives agreement at every finite depth, and conversely any pair with all infinite behaviors equal is a postfixed relation and never deleted. Thus D is exactly the set of states with one deterministic infinite output, and is transition-closed. This proves the universal interpretation of the predecessor greatest-relation algorithm; its independent possible-state-set checker is corroborating evidence, not the proof.

Let τ be the first hit of D. All hit paths yield outputs in a countable set (finite input prefix plus one of finitely many deterministic tails). Any output obtained from a finite hitting prefix has positive singleton mass, because that prefix has positive input-cylinder probability.

For s∉D there are two finite input words with different output prefixes. Finiteness gives a common length L at which every non-D state has two such witnesses (extend shorter words). For any specified output block, at least one length-L input word disagrees, with probability ≥2^-L. Iterating conditionally while avoiding D bounds the chance of matching a prescribed output for k blocks without hitting D by `(1-2^-L)^k→0`. Therefore each output singleton has zero mass on {τ=∞}. The set of positive output singletons is countable by M2-01; its entire mass on {τ=∞} is also zero. Hence

`a_s=Pr_s(τ<∞)`, `d_s=Pr_s(τ=∞)`.

The source solver finds the states R that can reach D, sets h=1 on D and h=0 off R, and solves `h_s=(h_(δ(s,0))+h_(δ(s,1)))/2` on R\D. Reachability means every such state has a finite path to D. By finiteness there is a uniform block length and positive exit probability, so the substochastic matrix on R\D is transient; its powers tend to zero and I-P is invertible. Gaussian elimination over exact rationals therefore returns the unique solution. First-step conditioning and uniqueness identify that solution with the hitting probabilities.

This proves both directions needed by the finite implementation: returned values equal the mathematical a_s, and every well-formed finite machine has such a rational solution computable by the algorithm. It does not identify the general PR index problem with a finite matrix. No novel finite census is run for this already tested implementation.

## Evidence dimensions

- Finite execution: predecessor Mealy census preserved; new codec/compiler/flow unit and comparison tests in `evidence/FINAL_*`.
- Ordinary universal proof: C2-01 through C2-14.
- Reduction proof: explicit code transformers, input/output contracts, simulation invariants and semantic measures above.
- Hierarchy membership: C2-09.
- Hierarchy hardness: C2-10 through C2-12.
- Implementation correspondence: successful-return simulation C2-07; finite solver C2-14; no silent resource-as-zero semantics.
- Lean compilation/readbacks/axioms: recorded independently, not inferred from any of these items.
