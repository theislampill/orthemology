# Independent review: constructive full-polynomial nonmoment functional

Date: 2026-10-10 UTC.

## Verdict and exact scope

**PASS: the frozen target proves, by ordinary mathematics, one normalized real linear functional on all of R[x,y] that is strictly positive on every nonzero polynomial square, has computable dyadic monomial moments, and has no representing positive Borel measure. No mathematical repair is required.**

This verdict covers the universal argument, not merely the tested prefixes. The finite implementation agrees with that argument on its intended integer-exponent/rational-coefficient domain. The all-degree theorem is not currently a Lean theorem. Independent Lean replay certifies only the global scalar bound for the separating polynomial and the seed arithmetic, with the exact limitations stated below.

The reviewer did not develop or edit the author construction. All replays and this report were written in the independent review directory. No author source, protected source, rank-classification packet, integration state, or closure state was changed.

### Bound target

The author's frozen manifest was received before replay. Its SHA-256 is:

`94de1970b395a0f96c94fbfeb3eb7b621432959a6843cbc7024ffc8faaaa3561`

All 26 listed files were verified by byte count and digest against both the author directory and a private review snapshot, before replay. The original author files were checked again afterward and remained unchanged.

Core target digests:

- `PROOF.md`: `08fdec67591a4a0639fa4ca721293bd8c480ec405dcd1a7c5a08d3244aa84c80`
- `countermodel.py`: `7cc30cf19b820541630eb55b0a9305c4e1b707630f7b1ded1b4bff61f69e403b`
- `check_exact.py`: `48360e431f4856594bc079ae73daf5892d87d2fcd3d19037543ad72e208d6ba0`

The precise frozen files are retained in `frozen-target/`. Replay outputs are kept separately.

## 1. Universal mathematical obligations

### 1.1 Enumeration and its inverse: accepted

`PROOF.md`, Section 2, orders exactly the ten distinct exponent pairs of total degree at most three first. For degree d >= 4, the formula m(a,b)=T_d+b+1, T_d=d(d+1)/2, produces the interval [T_d+1,T_{d+1}]. Consecutive intervals meet without gaps or overlap; their union is every integer at least 11. This proves injectivity and surjectivity without bounded enumeration assumptions.

The implementation's integer-square-root inverse, `countermodel.py:24–32`, is also correct. For n >= 11, its d is the unique integer satisfying T_d <= n-1 < T_{d+1}; b=n-1-T_d then lies between 0 and d. No floating-point approximation is involved. The exceptional branch handles n <= 10 exactly.

### 1.2 Global midpoint precedence: accepted

The full assertion needed is: for distinct p,q with componentwise-even sum, the index of their midpoint is strictly below max(m(p),m(q)). A weaker assertion about degree or a check of finitely many pairs would not suffice.

The proof's three cases are exhaustive:

1. Both degrees at most three. The four parity classes of the exceptional ten indices are {1,7,8}, {2,6,10}, {3,5,9}, and {4}. Thus precisely nine unordered distinct pairs have an integral midpoint. Their listed midpoint indices are correct and each is below the larger endpoint index.
2. Unequal endpoint degrees with maximum D >= 4. The midpoint has integral degree strictly below D. It therefore belongs either to the exceptional initial block or to an earlier ordinary degree block. In either case it precedes the degree-D endpoint, regardless of the exceptional internal permutation.
3. Equal endpoint degrees D >= 4. Distinct exponent pairs of this degree have distinct second coordinates. Their integral midpoint has second coordinate strictly between the two, so precedes the larger endpoint under this shell's linear order.

This proves the assertion for all exponent pairs. In particular, every off-diagonal entry in a new Gram row depends only on a previously assigned moment. Equal endpoints are excluded correctly: their midpoint is their own index and supplies the new diagonal.

### 1.3 Initial Gram matrix and preserved entries: accepted

The first four exponents have the four distinct componentwise parities 00, 01, 10, 11. Every product between two distinct such monomials has an odd component and hence moment zero. Their diagonal moments are exactly 1,1,1,4. Consequently the initial matrix really is diag(1,1,1,4), rather than an arbitrary positive matrix incompatible with the moment convention.

For every earlier matrix entry, the associated moment index is at most the larger endpoint index. Thus appending j_n cannot revise any already assigned entry. Repeated products with identical exponent sums receive the same moment because entries are defined from exponent sums, not independently assigned matrix positions. This resolves the Hankel consistency issue across all extensions.

### 1.4 Total recurrence and dyadic computability: accepted

The explicit state comprises the finite list of j values and a finite matrix B. Each new v uses only the earlier list; w=Bv, q=v^T w, j_n=1+q, and the displayed update of B require finitely many additions and multiplications. The only nonintegral initial value is 1/4. Therefore the recurrence exists at every natural-number stage over Z[1/2], without assuming in advance that a matrix can be inverted, invoking numerical tolerances, or searching for an adequate diagonal.

The inverse property is subsequently proved by induction. This is important: the definition is not circular. Since every requested exponent has a finite index, a finite prefix computes its dyadic moment. Practical time or memory bounds are not claimed.

### 1.5 Positivity, inverse, determinant: accepted

Suppose A is symmetric positive definite, B=A^{-1}, w=Bv, and q=v^T w. Then Aw=v and w^T A w=q. Expanding the proposed new quadratic form gives

    (u,t)^T [[A,v],[v^T,1+q]] (u,t)
      = (u+t w)^T A (u+t w) + t^2.

For a nonzero real vector (u,t), this is strictly positive, whether t is nonzero or zero. The proof therefore covers arbitrary real vectors, not only the rational vectors used in diagnostics.

Direct block multiplication of the displayed inverse update gives the identity matrix. The lower-left block vanishes because v^T B=w^T and v^T w=q; the lower-right block is (1+q)-q=1. Symmetry also gives the reverse product. Thus the recurrence has exactly the stated diagonal j_n=1+v^T A^{-1}v.

The change (u,t) -> (u+t w,t) is unit triangular. Its congruence reduces the matrix to diag(A,1), preserving determinant, so det A_n=4 for all n >= 4. The first three leading matrices have determinant 1 and are identities.

No growth estimate or monotonicity is needed. The explicit fall from j_11=479723268580926 to j_12=5/4 rules out monotonicity and invalidates any attempt to import a proof requiring the book's rapidly increasing diagonal sequence.

### 1.6 Full algebra and strict positivity: accepted

Every exponent pair receives exactly one finite value, using zero for an odd component and j_m for even components. The monomials form a real vector-space basis of R[x,y], so finite linear extension is a well-defined real linear functional. No infinite series or limit of functionals is being assumed.

For every nonzero real polynomial p, its finite support lies among some first N monomials. Its unique coefficient vector c is nonzero. The moment-entry definition and finite distributivity give Lambda(p^2)=c^T A_N c>0. This is the essential passage from arbitrarily long compatible prefixes to one universal functional. It is valid because the sequence is defined by a single total recursion and prefixes never change.

The Python API works with rational coefficients; the real-linear extension in the proof does not claim that arbitrary real inputs are computationally encoded. Normalization is Lambda(1)=j_1=1.

### 1.7 Positive witness and measure obstruction: accepted

For F=1+x^4 y^2+x^2 y^4-x^2 y^2, write u=x^2, v=y^2 and s=u+v. Then F=1+uv(s-1). If s>=1, F>=1. If s<=1, the inequalities 4uv<=s^2<=1 and 0<=1-s<=1 imply uv(1-s)<=1/4. Hence F>=3/4 globally.

The four frozen seed moments give Lambda(F)=1+1+1-4=-1 exactly. A representing positive measure would have mass one and finite integrals of those monomials. Its integral of F would simultaneously equal -1 by finite linearity and be at least 3/4 by positivity, a contradiction. There is no reliance on a truncated separation theorem or on a claim that every square-positive functional is a moment functional.

## 2. Distinct proof control: determinant-affine completion

An independent way to establish the universal completion supports the review and generates the independent replay.

Assume the leading moment matrix through n-1 has determinant 4 and all earlier moments are fixed. Midpoint precedence fixes every off-diagonal entry of the next matrix. Let C_n(t) be this symmetric matrix with its new diagonal set to t, and let d_0=det C_n(0). Expanding the determinant in that single entry gives exactly

    det C_n(t) = d_0 + 4t.

Choose t=(4-d_0)/4. This is a dyadic number since d_0 is a determinant of a dyadic matrix. It makes the new determinant 4. Starting from diag(1,1,1,4), every leading principal determinant is then 1,1,1,4,4,... . Sylvester's finite-dimensional criterion gives positive definiteness at every stage. This is an independent all-stage construction with a fixed nonzero divisor 4.

For a fixed previous matrix and border there is only one t giving determinant 4. The author's Schur-completed matrix also has determinant 4, so induction identifies the determinant construction with the author's sequence at every index, not merely on the computed prefix.

The reviewer implementation evaluates d_0 by Bareiss elimination. It neither uses the author's inverse update nor calls the author's Gaussian solver or LDL checker to generate its reference sequence. It imports the author module only after constructing that independent sequence, for comparison.

## 3. Executed checks and rejection controls

### Independent replay

`check_independent.py` passed **44,637 exact assertions**:

- Diagonals reconstructed independently through index 25 by determinant-affine completion.
- Direct enumeration of all 5,151 exponents of total degree at most 100, checked against both indexing functions.
- 300 integer-only inverse checks at indices up to 10^100+1.
- Every one of 30,600 parity-compatible distinct pairs through degree 30 satisfies midpoint precedence, including precisely the nine exceptional pairs.
- Every leading determinant through 25, seed Gram matrix, prefix stability, dyadic moments and inverse entries, and both inverse products.
- Independent multiplication/evaluation of 50 nonzero rational polynomial squares, normalization, odd moments, and the witness value -1.

These checks are finite diagnostics. Sections 1 and 2 of this report, together with the frozen proof, are the universal argument.

Executed negative controls:

- Swapping exceptional positions 5 and 10 breaks precedence: endpoints 1 and 7 then require midpoint index 10.
- Changing the first Schur slack from 1 to 0 gives Lambda((x-4xy^2)^2)=0, failing strict positivity.
- Changing it to -1 gives the same square value -1, failing positivity.
- Zero extension after j_10 gives Lambda((y^4-1)^2)=-163029.
- The sequence's actual j_11,j_12 reject monotonicity.
- Increasing the twelfth diagonal by 1/4 changes its determinant from 4 to 5, and the determinant-completion equality rejects it.

Receipt: `INDEPENDENT_RECEIPT.json`; full console output: `INDEPENDENT_CHECK.log`.

### Fresh author replay

The unchanged author's `check_exact.py` was run in `author-replay/`, where it passed **37,588 assertions**. Its generated prefix-25 file exactly matches the frozen prefix digest. This is additional reproducibility evidence, separately counted from the independent checker.

### Fresh bounded Lean replay

The frozen scalar source was copied into `lean-replay/` and independently compiled with the retained Lean 4.19.0 binary at `--trust=0`, without a dependency rebuild. Four printed theorem axiom lists contained only `propext`, `Classical.choice`, and `Quot.sound`. Source inspection found no `sorry`, `admit`, introduced `axiom`, `native_decide`, or `implemented_by` token. The retained matrix-import probe passed; both false scalar claims were rejected by proof checking, not by unavailable imports.

This certifies the real scalar statements F>=3/4, F>0, and 1+1+1-4=-1. It does **not** certify in Lean a defined infinite moment sequence, the indexing lemma, a linear functional on the polynomial algebra, universal square positivity, its evaluation on F, or the no-measure conclusion. Scalar arithmetic is not a formal evaluation theorem for an absent formal functional.

Receipt: `FROZEN_REPLAY_RECEIPT.json`; logs: `author-replay/` and `lean-replay/`.

## 4. Ancillary substitution and attribution boundaries

The algebra in the frozen `RANK_SUBSTITUTION.md` was also inspected. For the homomorphism E setting damped coordinates to zero and retaining two uncontrolled coordinates, B=Lambda composed with E has B(1)=1, B(q^2)>=0, B(hp)=0, and B(F)=-1. B is not asserted to be strictly square-positive when E has a kernel. For the stated Gaussian mixture, G_t(F)=6Z_r(t), and A_t(F)=(-13+6Z_r(t))/14<=-1/2 for t>=0. A positive Gaussian component supplies strict positivity for every nonzero square at finite times. These formulas are consistent with replacing the existing counterpath's full-functional premise. This review does not re-review every positive-direction theorem in the separate rank-classification packet or grant any integration/closure status.

The exceptional ordering, seed moments, parity convention, separating polynomial, and the nonmoment phenomenon are credited to the classical construction recorded in Schmudgen's *The Moment Problem*, with that book's attribution to Friedrich. This work is an explicit Schur-completion realization of that obstruction; no field-novelty claim is justified or needed. The recurrence has its own proof and does not depend on parsing the book's factorial formula.

The author explicitly distinguishes inspected searchable secondary-source text from unavailable page screenshots and an original Friedrich article not independently bibliographically checked. This reviewer did not repeat a source-retrieval campaign, inspect the original article, or upgrade that stated source status. The mathematical verdict is self-contained and does not depend on resolving that bibliography.

## 5. Limitations and final disposition

No blocking mathematical or implementation finding was identified in the frozen target. There are no requested repairs.

This construction is distinct from the earlier ternary truncated Lean functional. It does not extend that particular truncated datum or erase its known higher-degree failure. It also does not independently give a coercive heat-equation or diffusion counterexample, a moment-reconstruction algorithm, or a determinacy theorem. The nonexistence of a measure is precisely what is proved.

The accepted result is **universal mathematical construction plus bounded computational corroboration and scalar-only Lean support**. It is not a full functional kernel certificate or an audit/closure decision.

Replay from the workspace root:

    python3 full-polynomial-moment-independent-review-20261010/check_independent.py
    python3 full-polynomial-moment-independent-review-20261010/replay_frozen.py

The second replay expects the existing retained toolchain and dependency paths in this workspace. It operates only in review-owned replay directories and verifies the author originals remain frozen.
