# Codec and Mealy executable fixtures: exact source qualification

## Result

All five assigned fixture identities now have justified source dispositions. Three small executable interfaces were read in full. The two large `Differential.lean` bodies were qualified through full reading of their original deterministic generators and the exact previously examined Python codec, followed by fresh unchanged generation and comparison of every resulting byte. Both hashes match. This is complete generated-data qualification, not an invented line-by-line reading of 9,910 repeated fixture lines.

The exact rational control program also freshly passed **7,004 assertions**. No Lean compilation or execution was performed in this branch. Historical Lean and cross-language receipts retain historical status. In particular, the original 260-machine Python comparator imports an absent, un-hashed `cvc_probe.py`; that historical comparison cannot presently be reverified exactly. This does not undermine the separately examined Lean Mealy solver proofs.

`READ_LEDGER.json` contains 110 exact identities: 36 new full bodies, two qualified generated bodies, one selected historical receipt range, and 71 exact prior full-body reuses. The five recursive custom import closures have 16, 48, 52, 48 and 13 sources including their respective seed; all 65 distinct nonseed custom imports have adequate exact prior full reading. Official Lean/mathlib libraries are not counted as original research reading.

## 1. Codec differential fixtures

Original generator `57a6193eaa60…` constructs 82 programs and 758 assertions against the exact Python codec `dd79f63f5af9…`. Its finite coverage includes every binary-expression constructor, bounded exponentiation, skip and sequential normalization, captured-bound loops, deterministic bounded random trees, invalid numeric indices, malformed byte encodings, accepted and rejected byte mutations, wrong arity, and variadic sequences of length zero through four. Four input pairs per program compare interpretation. Resource-limit probes require an exception rather than silently returning zero.

The generated Lean main throws at each failed comparison; its printed count alone would not establish success. Fresh generation exactly reproduced `99b892d980f3…`. The small `da6332886eaf…` fixture repeats the first seven checks and is a useful diagnostic rather than a separate broad validation argument.

The controlling effective-index audit preserves several important conditions:

- Numeric encoding injectivity and byte round trips concern genuine byte lists. Arbitrary natural-valued lists can collide, for example by carrying a value 256 across a base-256 boundary.
- Variadic sequence decoding normalizes syntax, so semantic round trips do not imply identity of arbitrary original byte encodings.
- Invalid or wrong-arity numeric indices are assigned zero by the defined evaluator. Host resource exhaustion has a separate error meaning.
- Each fixed LOOP program gives primitive-recursive evaluation and parameter specialization. This is not a uniform primitive-recursive universal evaluator over all encoded programs.
- The reduction uses a fixed, jointly primitive-recursive relation and an effective parameter map. A proved lower-bound reduction alone is not the corresponding upper-bound classification.

The historical verifier initially missed attributed declarations in its regex scan. The complete readback `34895394b9b8…`, now read in full, lists all 82 check/axiom pairs. It is mechanical declaration evidence; its proof targets have independent exact full-body routes in the import closure. We do not promote an earlier 73-target count into an 82-target fresh replay.

## 2. Numeric membership fixtures and hard-threshold boundaries

Generator `bcc7910dfd0e…` creates 27 indices, including three invalid/sentinel cases, and evaluates all finite source words at depths zero through four. Each stage of output construction receives only its proper shorter prefix. Exact `Fraction` arithmetic supplies cylinder probabilities, inclusive heavy-mass sums, and the rational-coded numerical matrix. The 2,214 checks are distributed among 56 batches. Fresh generation exactly reproduced all bytes of `f2a567ec2297…`.

The controlling characterization uses a **finite measure**, nested separating Cantor-cylinder partitions, and inclusive threshold cells. Writing H(k,n) for the total mass of depth-n cells whose mass is at least 2^(-k), the atomic mass is sup_k inf_n H(k,n). For probability laws, full atomicity has the rational approximation pattern: for every q < 1 there exists a threshold k such that for every depth n, q ≤ H(k,n). These quantifiers cannot be exchanged and q = 1 cannot replace the approximating q < 1.

The fresh 7,004-check exact-rational run exercises the source formulas:

- Fair Cantor: H(k,n) equals one exactly when n ≤ k. Every bounded depth window can pass although atomic mass is zero.
- Geometric atom law: H(k,n) equals one for n ≤ k and 1 - 2^(-k) thereafter. Atomic mass is one but no fixed finite threshold captures all mass at every depth.
- Half Dirac plus half fair: every zero-branch cylinder has mass strictly greater than 1/2, while the limiting singleton has mass exactly 1/2. This distinguishes the strict-cylinder intersection from the intended inclusive atomic threshold.

The ordinary argument, not the finite grid, establishes the limiting statements. Infinite total mass can defeat continuity from above; nonseparating cells can hide diffuse mass; the older soft/excess expression is not silently substituted for this hard-threshold theorem.

The original mutation runner was read fully. It first compiles the unmodified source, then separately changes inclusive to strict threshold, changes the cylinder denominator from 2^N to 2^(N+1), or supplies the complete source word too early. Its rejection checks exclude missing-module/object-file failures. Exact boundary and endpoint control bodies, as well as the false-atomicity control, already have full hash-bound reading routes and are reused explicitly.

The 25-line total-computability argument `c90c6726fd1f…` was newly read in full: finite varint parsing, syntax fuel, captured finite LOOP bounds, finite touched-register support and finite word enumeration establish an ordinary uniform total-recursive algorithm. It is not a formal Mathlib `Computable` certificate and not a uniform primitive-recursive universal interpreter.

## 3. Compiler AST comparison

`IndependentAstComparison.lean` (`6e21dadcecdb…`) defines JSON export for all ten expression constructors and statement structure, flattening sequences and skips. Its 32 `#eval` expressions emit data; there is no assertion of correspondence inside that Lean file.

The actual driver `f2bb2ce56c2c…`, newly read in full, verifies the Python codec hash, constructs four designated and 28 seeded random compiler inputs, normalizes the Python AST's sequential lists, invokes the Lean exporter and compares all 32 JSON rows. This is finite constructor-level correspondence. It does not prove universal equality of Python parsing, serialization, interpretation, or numeric compilation.

The accompanying scope report describes the fresh-register allocator, caller-frame conditions, first-witness freezing and previous-state renaming. Its statement that codec formalization was still pending belongs to that historical stage. Later exact codec proof bodies, already examined and linked here, supply the actual successor scope; the old report must not be treated as a current theorem failure.

## 4. Mealy solver fixture and historical limitation

`SolverProbe.lean` (`b75a20f398ce…`) uses base-(2m) coding to enumerate the four one-state and 256 two-state deterministic binary Mealy tables and prints `solveDefect` at initial state zero. The Fin-state construction includes the necessary bounds. It is an executable enumeration, not an assertion that the printed values equal an external implementation.

The actual `compare_small.py` (`df33d22651ce…`) checks 260 CSV rows by reconstructing the same tables and comparing exact fractions against `cvc_probe.py.defect(table)[0]`. Its row-count check does not by itself establish uniqueness or exhaustive population; the producer supplies that property. The historical result `bdfee5f1232e…` reports four plus 256 matches and expressly limits the result to executable regression.

The original reference script is named only by `private-locator:71d899355bd9e81c1732`. No exact digest or extant custody object has been found. Controller has confirmed that absence in current frozen and recovered joins. No same-function substitute was introduced, and no broad acquisition was reopened. **Exact fresh cross-language re-verification remains unavailable for this historical harness.**

The Mealy Stage-2 README `34ea6b66d1ab…` contains a stale paragraph saying the infinite-horizon solver remains existential. The actual Stage-2 solver, executable fixtures and later audit demonstrate the constructive successor scope. The earlier paragraph is retained as historical writing, not as a claim about the final solver.

## 5. Exact dependency and replay accounting

`EXACT_IMPORT_CLOSURES.json` binds every custom import by SHA. Two Atomic Membership archive ambiguities are resolved by the actual `receipts/20260930T163934Z/sources/` baselines, not by choosing a mutant with the same filename. Five external Mealy predecessors are bound by the final hash lines of historical verifier log `27ab66e7430c…`, whose producing shell `a20a9c66756b…` was read in full. Every resulting source is present and byte-verified, and every nonseed has numerical full-body prior read ranges.

The original rebuild/readback helpers were themselves examined rather than counted as mathematical proofs. Older first-match source lookup, permissive missing-custom traversal and weak generic negative-test diagnostics are qualified in the ledger. These historical helper limitations do not invalidate later exact isolated source builds, nor do those later builds automatically certify every historical helper.

Fresh evidence in this branch is exactly:

1. Original codec generator → byte-identical 758-check Lean fixture.
2. Original membership generator → byte-identical 2,214-check Lean fixture.
3. Unchanged exact-rational Python program → 7,004 passing assertions.

All commands, hashes and exit codes are recorded in `GENERATED_BODY_VERIFICATION.json` and `FRESH_EXACT_CONTROLS.json`. Generation does not imply that Lean has run the generated assertions. The only unclosed consequential scope in this bounded fixture family is the missing exact historical Python reference comparator; all custom proof imports are resolved and substantively credited.

## 6. Earlier-to-later interpretation

This family supplies a concrete finite-data boundary relevant to later skyline and inquiry claims: passing every observation up to a supplied finite horizon cannot certify global atomicity without additional structure. Exact source access and an independently proved model theorem can justify a solver or a reduction, while finite trace comparisons remain bounded implementation evidence. Conversely, the positive Mealy atomic-restriction approximation results are retained: this finite-prefix obstruction does not erase constructive approximation when the actual finite-state law and its proved structure are supplied.
