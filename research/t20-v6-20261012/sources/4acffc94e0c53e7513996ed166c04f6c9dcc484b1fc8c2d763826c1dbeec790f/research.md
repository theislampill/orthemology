# Successor: exact affine-Boolean disclosure over rational weight polytopes

**Scope:** separate successor to the immutable P15 interval return. This document develops an ordinary mathematical proof and a small research prototype; it makes no kernel-verification, normative-authority or global novelty claim.

## 1. General theorem

Let P={w∈R^m: Aw≤b, Ew=f} be a bounded rational polyhedron (possibly empty or lower-dimensional). Fix finitely many rational affine functions ℓ_j(w)=a_j·w+b_j. Let φ be a Boolean combination of comparisons ℓ_j>0 or ℓ_j≥0. Repeated expressions can share one atom.

For each σ∈{−1,0,+1}^k define the sign cell C_σ={w∈P: sign ℓ_j(w)=σ_j for all j}. Every w∈P lies in exactly one such cell, and the target is constant on each cell, by induction on its Boolean syntax. Therefore the truth values realized by φ on P are precisely those associated with the nonempty cells. A complete decision method must account for zero-sign faces and strictly signed relative interiors, including within a lower-dimensional P.

This sign decomposition is standard real linear arithmetic/hyperplane-arrangement reasoning. The application contribution is the exact disclosure/certificate boundary and negative controls, not a novelty claim for the decomposition.

## 2. Strict feasibility by one bounded slack

Construct Q_σ in variables z=(w,t):

- w∈P and 0≤t≤1
- ℓ_j(w)=0 for σ_j=0
- σ_j ℓ_j(w)≥t for σ_j≠0

**Theorem S1.** C_σ is nonempty iff Q_σ has a point with t>0, equivalently iff Q_σ is nonempty and its maximum t is positive.

**Proof.** From a point in the sign cell, every one of the finitely many signed nonzero expressions has a strictly positive margin. Choose t as the minimum of these margins and 1. If there are no such expressions, choose t=1. Conversely, t>0 enforces precisely the required strict signs, while the zero equations enforce ties. Boundedness of P and the slack bounds make Q_σ compact, so a nonempty Q_σ attains its maximum. ∎

**Boundary guard.** Q_σ may be nonempty with maximum t=0 while C_σ is empty. Closure feasibility is not strict feasibility. A fixed numerical epsilon is not equivalent to t>0: valid cells can have arbitrarily small rational margins. The common slack is used per cell; no uniform positive slack across all possible input instances is assumed.

## 3. Rational witnesses and a complete certificate alternative

Convert all equalities in Q_σ into pairs of weak inequalities and write it as Cz≤d. All data are rational. Its number of variables is n=m+1.

There are three sufficient certificate types:

1. **Positive witness:** rational z with Cz≤d and t>0.
2. **Nonpositive slack bound:** rational λ≥0 with Cᵀλ=e_t and dᵀλ≤0. Every feasible z then satisfies t≤dᵀλ≤0, so the strict cell is empty.
3. **Infeasible closure:** rational λ≥0 with Cᵀλ=0 and dᵀλ<0. Any feasible z would give 0≤dᵀλ<0, a contradiction.

Each certificate is checked by exact additions, multiplications and comparisons. No optimizer result needs to be trusted by that checker. Types 2 and 3 may overlap as sufficient refutations, but type 1 cannot coexist with either.

**Theorem S2 (completeness for rational bounded inputs).** Every σ admits one of these rational certificate types.

**Proof.** If Q_σ is empty, the linear alternative supplies type 3. Its multipliers can be rational: Fourier–Motzkin elimination over rational data constructs a nonnegative rational combination giving a contradictory constant inequality. Scale its negative bound to −1. If Q_σ is nonempty, a linear objective on its compact polytope attains an optimum at a vertex. Each vertex is the unique solution of a full-rank subsystem of rational active equations and is rational by Gaussian elimination. A positive optimum gives type 1. Otherwise the imposed t≥0 means the optimum is exactly zero. Linear-programming strong duality supplies nonnegative multipliers with objective bound zero, giving type 2. Rationality also follows by a rational basic solution of the dual's exact linear constraints, or by a conic representation with linearly independent rational generators. ∎

The standard alternatives and duality are used only for finite linear inequalities. This is not an extension to arbitrary conic, nonlinear or infinite-dimensional systems. [Goemans, Linear Programming and Polyhedral Combinatorics, §§3.1–3.2](https://math.mit.edu/~goemans/18433S15/polyhedral.pdf), [Boyd–Vandenberghe, duality lecture, theorem-of-alternatives section](https://web.stanford.edu/class/ee364a/lectures/duality.pdf)

**Elementary finite search specification.** Enumerate every n-row subsystem of C, solve it exactly, retain each full-rank solution satisfying all rows, and inspect its slack. This enumerates all vertices, including vertices of lower-dimensional polytopes because enough always-active equalities supply part of the rank. If no positive vertex exists, search for a conic representation of (e_t,0) (type 2 at zero bound) or (0,−1) (normalized type 3) using the row vectors (C_i,d_i). A conic Carathéodory reduction leaves at most n+1 linearly independent generators: if a representation has dependent generators, choose a nonzero dependence, adjust coefficients in an orientation with some positive coefficient until one nonnegative coefficient reaches zero, and iterate. Enumerate these subsets and solve the resulting rectangular full-column-rank systems exactly. This is complete but deliberately inefficient.

The low-dimensional prototype uses this finite search, not a floating-point LP backend. Its independent checker validates certificate equations and cell coverage without repeating the vertex or conic search.

## 4. Why original-polytope vertices fail

Take three normalized weights with w_j≥1/10. P is the triangle with vertices (4/5,1/10,1/10) and permutations. The target

`w_1>1/5 AND w_2>1/5 AND w_3>1/5`

is false at every original vertex and true at (1/3,1/3,1/3). A vertex-only Boolean check wrongly declares it invariant false. Linear objectives can be optimized at original vertices, but a Boolean combination of several linear comparisons is not one linear objective.

The negation is true at all original vertices and false at the center, so even a vertex-only invariance-true rule fails. Restricting P to a line or point can make equality faces decisive; a generic interior sampler can miss those as well.

## 5. Scope of the implementation

The intended executable probe handles three normalized criteria, a supplied positive lower bound, a bounded number of rational linear restrictions, and at most a few distinct affine comparison atoms. It checks all 3^k sign patterns. Exponential certificate size and subset enumeration are explicit limitations. A scalable implementation could use a trusted or certifying exact LP solver and traverse only realizable cells, but would need an independently checked coverage argument if it stopped enumerating all patterns.

The weights, coordinate extraction, orientation and admissibility constraints are supplied inputs. Exact geometry certifies none of their normative authority. P15's declared-kind, source identity, model-uncertainty and metaphysical-admissibility distinctions continue to apply. Strictly positive weights preserve nonzero nonnegative vector improvement only when positivity is genuinely enforced; boundary-zero weights require the weaker result recorded by P14.

## 6. Executed prototype and independent checks

`polytope_disclosure.py` implements exactly three weights with sum one, a supplied rational minimum weight ε in (0,1], up to four additional weak inequalities, up to two additional equalities, and at most three supplied affine atoms. ε>1/3 deliberately represents an empty class. Every coefficient has a 128-bit numerator/denominator bound. The finite Boolean grammar has 64 nodes and depth 12 bounds. This is an isolated research module, not a deployed service or a replacement for P15's broader provenance envelope.

`audit(polytope, atoms, target)` constructs one certificate for every ternary pattern. `verify(polytope, atoms, target, certificate)` independently checks input identity, exact field types, all pattern coverage, rational witness feasibility, nonnegative multiplier identities and the derived final truth values. It does not invoke vertex enumeration or conic certificate search. The returned scope is always `RELATIVE_RATIONAL_POLYTOPE_DISCLOSURE_ONLY`; authority is always `SUPPLIED_NOT_CERTIFIED`.

Certificate kinds are `POSITIVE_WITNESS`, `DUAL_ZERO_BOUND` and `FARKAS_CONTRADICTION`. The producer uses exact-zero dual bounds and −1-normalized contradictions; the verifier accepts any valid nonpositive dual bound or strictly negative contradiction. The name DUAL_ZERO_BOUND names the producer's normalized construction, not a tolerance test. Signed patterns reject Boolean/integer coercion. Unknown operations, malformed or stale certificates and incomplete/duplicate pattern coverage are rejected.

A potential integer-size concern is also bounded in this tiny grammar. Each generator has five rational coordinates, each with numerator/denominator at most 128 bits. Clearing denominators per row uses at most five factors. A full-rank 5×5 determinant then has magnitude below 5!·2^3200; Cramer's rule therefore gives a numerator/denominator below 3207 bits after reduction. The 4096-bit certificate-number allowance safely exceeds that crude bound. Vertex systems are only 4×4. This resource argument is specific to the stated dimensions and raw coefficient bounds.

The complete test-first cycle produced 16 failing tests before implementation and 16 passing tests afterward. Tests cover both directions of the original-vertex counterexample, singleton and lower-dimensional ties, empty classes, zero-slack versus strict feasibility, constant impossible atoms, a positive margin of 10^-12, stale input, corrupt multipliers/witnesses, omitted cells, Boolean signs and unsupported target syntax.

An independent exact reference implementation in `exact_reference_probes.py` eliminates **strict inequalities directly** using Fourier–Motzkin, without the common slack or vertex method. Positive combinations propagate a strict flag if either input is strict. Contradictory constant rows decide emptiness. It was compared with the certificate producer on:

- 423 rational input instances and 2,349 sign cells
- 978 feasible positive-witness cells
- 1,083 infeasible-closure Farkas cells
- 288 nonempty-closure but empty-strict-cell dual-bound cases
- 128 invariant-false, 122 invariant-true, 92 disagreement and 81 empty-domain instance verdicts

There were zero mismatches. Forty-two deliberate certificate corruptions were rejected. A replay replaced both search routines by exceptions; the verifier still accepted the already generated valid certificate. These are exact finite checks, not randomized empirical validation or a formal proof-assistant result. The general completeness argument remains the ordinary proof above.

`interior_example.json` contains the complete 27-pattern certificate for §4. The original vertices make the target false, but a rational interior positive witness makes it true. Keeping every zero-sign pattern supplies tie coverage that a generic interior-only arrangement sample would miss.

## 7. Handoff and claim ceiling

This successor is bound to the sealed P15 archive SHA-256 `48eb8179e41e66addccc094d6b48033bc786e83d42fcd47a6ed9780c1764dd61`; it does not alter that artifact or its two-criterion interface. It adds a general ordinary proof/specification and a bounded three-criterion prototype. All source-extraction, admissibility, authority, naturalism, metaphysical-possibility and adoption ceilings of that predecessor remain in force.

For later authorized implementation, separate the untrusted search producer from the small certificate checker, bind the complete descriptive/mixed input and bridge regime, pin arithmetic/parser versions, and preserve strictness/coverage fixtures. A scalable solver may replace enumeration without changing the linear-certificate checker, provided it emits exact rational certificates. If a solver reports a timeout, numerical uncertainty or no certificate, return an explicit unresolved status rather than an invariance result. A partial list of feasible cells can refute invariance when it contains both truth values, but cannot certify invariance or empty-domain status.

The complete enumeration has 3^k patterns and combinatorial vertex/conic searches. No polynomial complexity or practical scaling claim is made. Distinct atoms, repeated expressions, constant atoms and degenerate faces need deliberate normalization if optimized. Any generalization beyond three criteria/atoms must recheck numeric and resource bounds. Unbounded polyhedra require a different completeness justification for vertex search; this implementation exploits the normalized positive-weight compact domain.
