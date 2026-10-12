# Atomic-membership bridge: independent audit

Status: independent PASS at the stated scope. No mathematical or implementation defect was found in the frozen hard-threshold bridge. All 53 custom modules rebuilt in an isolated library; 44 author targets and 19 independent review theorems were checked with only standard Lean axioms. Exact executable differential checks and false-mutant controls also passed. This is an independent research qualification, not canonical adoption or closure of every research obligation.

The reviewed subject is the exact 144-member author archive Atomic_Membership_Research_Return_20260930.zip, SHA256 1a08827157bbaedd7a764a36a7f1f2b2d49599b7e54853333d1a787ffe8de13a. All 143 manifest entries and all 53 custom-source hashes match the isolated replay. The archive seal SHA256 is 3fa409afb329d0384258c1825c0a01cb51f13c406520b62e7d707481541dc5dc.

## Precisely scoped result under review

For a finite measure μ on Cantor space, let H(k,n) be the union of length-n cylinders whose μ-mass is at least 2^-k. The claimed identity is

  μ({x : μ({x}) > 0}) = sup_k inf_n μ(H(k,n)).

For a probability measure this yields μ({x : μ({x}) > 0}) = 1 iff for every rational 0 ≤ q < 1 there is a threshold index k such that at every depth n, q ≤ μ(H(k,n)). Finite cylinder partitions make each heavy mass an exact finite sum. This is a hard-threshold alternative; it does not establish the earlier cylinder-excess/soft-threshold formula.

## Mathematical checks

1. Prefix cylinders shrink with n and their intersection is exactly the singleton. This uses all Cantor coordinates, not merely an arbitrary observation sequence.
2. Finite-measure continuity from above gives μ({x}) = inf_n μ(C_n(x)). The proof explicitly provides a finite first set; no interchange of unrelated limits is occurring.
3. Inclusive comparison is exact: a ≤ inf_n b_n iff every b_n ≥ a. Consequently the fixed-k intersection of heavy events is the set of singleton masses at least 2^-k.
4. Continuity from above applies again to the heavy events because they decrease and are measurable under a finite measure.
5. Threshold levels grow as k grows and their union is exactly the positive-singleton set. Continuity from below gives the outer supremum. Threshold positivity and cofinality near zero are explicit.
6. The rational normal form has the required order ∀q∃k∀n. In the forward implication q<1 yields a strict witness below the supremum. In the reverse implication rational density separates any atomic mass <1 from 1. The constraint q<1 cannot be replaced by q≤1.
7. Length-n cylinders form a finite disjoint measurable partition. Summing the whole cylinder mass, including tied threshold cells, therefore exactly measures the heavy event.
8. The semantic result needs only finite μ; the mass-one characterization as written assumes probability. There is no unsupported use of finite measure as probability.

## Independent countercontrols

### Wrong quantifier order

For fair Cantor measure, every n-cylinder weighs 2^-n. Thus H(k,n) has mass 1 when n≤k and 0 otherwise. The correct sup_k inf_n is 0, but inf_n sup_k is 1. A depth-dependent threshold ∀n∃k therefore declares the diffuse fair measure atomic. The Lean control proves actual fair-Cantor atomic mass 0 and ∀n∃k heavy mass 1. No finite maximum tested depth can decide this distinction.

### Dropping finite measure

The actual measure ν = ∞ • fairCantor has singleton mass 0 everywhere but every nonempty cylinder has mass ∞. All its heavy events are universal, so the proposed right side is ∞ while positive-singleton mass is 0. This is an exact Lean counterexample to dropping finiteness, and leaves Cantor separation intact.

### Losing separation

Blind cells C_n(x)=univ have limiting fair measure 1 even though every singleton has fair measure 0. An arbitrary nonseparating observation family computes fibre/history information instead of the original singleton mass. The independent Lean control establishes this mismatch.

### Strict comparison at a tied atom

For μ = (1/2)δ_(all-zero) + (1/2)fairCantor, the all-zero singleton has mass 1/2, while each of its length-n cylinders has mass 1/2 + 2^(-n-1), strictly greater than 1/2. Therefore replacing both inclusive comparisons by strict comparisons makes the fixed-k level/intersection equality false. The independent Lean control uses this actual mixture measure. This refutes the local strict-threshold proof step; it does not claim that every differently proved outer-limit formula with strict thresholds would fail.

### Requiring the q=1 endpoint

Let e_j have its sole 1 at coordinate j and μ = Σ_(j≥0) 2^(-j-1)δ_(e_j). The law is wholly atomic. Its length-n partition consists of n isolated atoms with masses 2^(-j-1), j<n, and the all-zero-prefix tail of mass 2^-n. Thus heavy mass is 1 when n≤k and 1−2^-k when n>k. Its outer supremum is 1 but no finite k has inf_n heavy mass 1. The strict rational upper bound q<1 is essential. Exact Fraction tests check this formula and its monotonicities; this countable-mixture example is an analytic counterexample, not advertised as a separately Lean-formalized measure construction.

## Atomicity vocabulary

The imported definition `mass` is explicitly positive-singleton mass. In finite Borel Cantor space it agrees with measure-algebra atomic mass: a positive measure-algebra atom has, at each finite partition, one cylinder carrying its full mass; nested full-mass cylinders determine one point, and continuity from above concentrates the atom there. That additional identification is mathematically valid but is not a separate theorem furnished by the reviewed files. No general equivalence for arbitrary measurable spaces is claimed.

## Effective boundary

A supplied table with an exactness hypothesis is a semantic interface, not an effective algorithm by itself. The concrete program bridge must enumerate actual finite source words, execute the actual decoded evaluator, count output-prefix fibres, and prove the resulting rational equals the pushforward cylinder mass. It must retain invalid-index and wrong-arity fallback semantics and the exact N-bit dependence of the first N output bits.

The concrete FiniteOutputTable implementation passes this interface check. Its first N output bits depend on exactly the N supplied source bits, using each stage's shorter prefix. The correctness proof covers arbitrary P; its indexTable specialization uses the actual decoded numeric evaluateIndex. No cylinder-mass oracle is an argument of the executable numerical matrix.

NumericMembership supplies a surjective effective natural-number coding of nonnegative rationals by NNRat.divNat applied to Nat.unpair. Canonical numerator/denominator codes reach every rational. Zero-denominator codes denote zero; codes for q≥1 produce a vacuous matrix implication. Neither changes the quantified property. The exact theorem now has only natural quantifiers: e is a zero-defect index iff ∀i∃k∀n membershipMatrix(e,i,k,n); the complement is ∃i∀k∃n ¬membershipMatrix(e,i,k,n).

I independently accept TOTAL_COMPUTABILITY_ARGUMENT.md as ordinary, source-driven computability reasoning. The numeric and varint decoders decrease their numeric/list arguments; syntax parsers decrease explicit fuel or child counts; evaluation is structural on finite syntax with captured finite loop bounds; and only finitely many literal register indices occur. Thus a finite-map interpreter computes every output bit and terminates. Finite source-word enumeration, dyadic counting, Nat.unpair and rational comparisons supply a uniform total recursive decision procedure for the matrix. This supports an ordinary mathematical Π3 upper bound and a Σ3 complement upper bound, beyond a merely supplied semantic table.

The kernel-checked fixed-index Primrec theorem is pointwise in e and is not the reason the uniform algorithm is recursive. A uniformly primitive-recursive evaluator for all PR programs is not claimed. Executable definitions plus the accepted ordinary argument still do not constitute an internal Mathlib Computable theorem or a formal arithmetical-hierarchy membership certificate. These are separate mechanisation boundaries.

The reviewed author theorem's complement is “not zero defect.” Additional review-derived EndpointControls theorems establish that nonzero is positive for these probability laws, and derive the exact ∃i∀k∃n normal form for positive defect without editing any frozen author source.

## Verified evidence

- Lean 4.19.0, commit 6caaee842e94; Mathlib c44e0c8ee63ca166450922a373c7409c5d26b00b
- 53 custom-source modules rebuilt from the frozen bytes; only pinned official dependency object caches reused
- All 44 author bridge/table theorem signatures and their transitive axioms inspected
- 19 independent theorem controls, including three positive-defect endpoint corollaries, compiled and axiom-checked
- 2,214 runtime differential checks against the separately recovered Python evaluator: 27 valid and fallback numeric programs; depths 0–4; exact output-cylinder masses; actual rationalHeavyMass; actual membershipMatrix decisions; inclusive ties; q≥1 vacuity; zero-denominator and redundant rational codes
- 7,004 exact Fraction checks of the wrong-quantifier, strict-tie, q=1 endpoint, monotonicity and finite-horizon false-positive examples
- Three exact source mutations rejected, each following a successful unchanged baseline: strict versus inclusive heavy selection, a 2^(N+1) denominator, and passing a whole source word too early to each output stage
- One deliberately false actual-Cantor atomicity claim rejected
- Source scan found no sorry, admit, axiom, unsafe, implemented_by or native_decide tokens outside comments/strings in the copied custom source closure
- All original author source hashes remained unchanged

Build receipt: receipts/20260930T163934Z/RESULT.json, SHA256 d72b265c4ce23eba5b1df92b9f96cc3137fefbee16244879d1e2993f79a198d1.

Control receipt: receipts/20260930T163934Z/CONTROLS_RESULT.json, SHA256 353e441455184a23e014559e2e60817fb693d7d4ae3d536e727efdc3fa18940e.

A harness-only diagnostic assertion initially required the literal impossible goal `0 = 1`; norm_num correctly reduced it to `False`. Every control process had already returned its expected exit code. The driver was corrected to accept either exact impossible-goal diagnostic, the rejection was rerun, and the retained command/log/source hashes were revalidated before issuing the control receipt. No reviewed source, theorem, expected exit, or vector was changed. HARNESS_RECOVERY.json retains this distinction.

## Review-derived endpoint theorems

EndpointControls.lean proves, separately from the immutable subject:

1. AtomicMembershipAudit.probability_defect_pos_iff_ne_zero: positive defect iff nonzero defect for probability measures on Cantor space, using positive-singleton mass ≤ total mass = 1
2. AtomicMembershipAudit.numeric_positive_defect_iff_not_member: the actual decoded numeric law has positive defect iff the index is outside zeroDefectIndices
3. AtomicMembershipAudit.numeric_positive_defect_nat_normal: the same actual positive defect iff ∃i∀k∃n ¬membershipMatrix(e,i,k,n)

The author classification paragraph is consistent with this audited ordinary upper bound, the previously established fixed-PR-matrix reduction, and the standard arithmetical-hierarchy normal-form theorem. This review does not present that standard metatheorem as a newly mechanized theorem.

## Preserved boundaries

The exact hard-threshold result is accepted. The earlier soft/excess formula, full host-Python runtime refinement, general measurable-space atom identification, formal internal Computable/hierarchy certification, and later stack-machine additions are not covered by this award. Finite tests are regression evidence, not proofs of an infinite quantifier statement. Author files were preserved, and no canonical sources were edited.
