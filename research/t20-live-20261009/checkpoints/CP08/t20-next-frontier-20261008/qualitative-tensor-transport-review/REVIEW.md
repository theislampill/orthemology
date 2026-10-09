# Independent adversarial review: finite predicate-functor tensor transport

8 October 2026. Separate scratch review. No repository work, integration, or closure.

## Result first

**No blocking correctness finding remains for the stated claim:** every finite expression in the explicitly completed, arity-indexed semantics transports exactly to Boolean coefficient arrays on a finite nonempty domain. The written all-syntax argument is valid; it is not inferred from the finite assertion count. The numerical/support, complement, signed-cancellation, basis, shared-witness, plurality, and inherited-theorem boundaries are substantively correct.

This verdict does **not** certify exact implementation of the Appendix's uncompleted literal sequence clauses at every syntactically admitted arity. Those clauses fail prefix locality at unary iota, and the completed interpretation is a genuine qualification. Neither the reviewed result nor this review supplies a metaphysical identification or actuality inference.

The review found one non-blocking ambiguity: the Appendix's model truth of an open predicate is universal satisfaction, whereas `total()` existentially closes its input. The author added an explicit distinction and three checks. The reviewer also supplied the stronger low-arity witness `c(iota F)`, now discussed in the final result. Both changes are included in the bound snapshot.

Independent probes passed **393,050 finite assertions**, using a direct sequence-satisfaction oracle against a separately implemented coefficient evaluator, including 910 expressions across 18 composite models. Replaying the frozen latest author script passed **553,359 assertions** and reproduced the author's report byte for byte. These are assurance checks, not independent theorems, all-model proofs, or new discoveries.

## Reviewed inputs and provenance

The precise reviewed report is `../qualitative-tensor-transport/RESULT.md`, SHA-256:

`23f930729f24a2e014f0d678992cd3c390ae13745e7054431c236333fd085b97`

The precise reviewed script is `../qualitative-tensor-transport/controls.py`, SHA-256:

`9f1890d70aba5d3f4ca953809a588471226f3e56bb46feaf7cb82c3cf0aa3bd2`

Copies are in `reviewed_snapshot/`. `REVIEW_INPUT_BINDINGS.json` records lengths and hashes. The source basis was:

- Dasgupta (2009), section 3 and the complete Appendix, from the retained layout extraction. Printed pages 56, 63, and 64 were independently inspected as images (`page-22`, `page-29`, and `page-30`). The images verify sigma/iota glyphs, conjunction arities, permutation direction, the first-slot existential, leading padding, nonempty domains, and the actual separated record.
- The frozen `INHERITED_GRADED_INTERFACE.md`, relevant sections 2–6 and 11. Its bytes independently reproduce SHA-256 `cd5070341a46658c0e4ac2c077d343d276cf16e50f0305f61ebb90ba0b624c2e` and Git blob `c094a9c44fae26484426df67ac5afd9e2190eb4d`. The Git blob was computed directly from the local bytes, without accessing a repository.

This review did not independently reread Kuhn or re-audit every later/external ancestry source cited in the result. It makes no claim about Kuhn's intended low-arity convention. Its inherited-theorem check is against the exact frozen original specified in the assignment.

## 1. Operation-by-operation source fidelity

The completed array operations match the source in their natural arity ranges:

1. Complement reverses membership in the fixed grade's whole cube `D^n`. It is not complement of an unbounded graded direct sum.
2. Conjunction has arity `max(n,m)` and aligns prefixes. Both arguments receive ignored trailing positions where necessary. Ordinary outer product alone would instead have arity `n+m` and would not perform this alignment.
3. Sigma is the **right-rotating pullback** `P(a_n,a_1,...,a_(n-1))`. Its corresponding operation on relation rows is left rotation. The apparent opposition between the script's set-image and array-index directions is correct.
4. Iota swaps the first two slots when they exist.
5. `c` eliminates the first input slot by existential choice and lowers positive arity by one. At arity zero it is identity under the stated completion, also explicitly described on printed p.63.
6. `p` adds an ignored leading slot. It is different from the implicit trailing padding used by conjunction.
7. `I` is equality of the retained domain elements, not equality of qualitative display labels.

The source's exact example is therefore `c c (F & p G & R & not I)`. Replacing `p G` by trailing padding, reversing the sigma convention, replacing conjunction with outer product, or forgetting the shared axes would change the result. None of those mistakes occurs in the reviewed implementation.

## 2. Why the all-expression claim is warranted

A precise induction invariant is stronger than a list of operation checks:

For every expression `E` of declared arity `n` in the **completed** syntax, (a) its sequence satisfaction depends only on the first `n` coordinates, and (b) for every such prefix `a`, its coefficient array at `a` is exactly the satisfaction indicator.

The invariant is proved simultaneously by structural induction:

- Atomic relation symbols satisfy both clauses by their interpretation on `D^n`; equality satisfies them at arity two.
- For complement, the inductive truth value is negated at the same prefix, so no additional coordinates can matter.
- For conjunction, a `max(n,m)`-prefix contains both shorter required prefixes. Multiplication in the Boolean semiring returns one exactly when both subexpressions hold under that common assignment.
- For positive-arity `c`, the subexpression at prefix `(x,a)` is true for some `x` precisely when its finite Boolean sum is one. The subexpression's locality eliminates any dependence on the rest of the sequence. For scalar `c`, both interpretations retain the same scalar.
- For `p`, removing the first coordinate leaves exactly the old argument prefix. The ignored added coordinate introduces no new dependence.
- For sigma and iota in arity at least two, the same finite prefix permutation is used on both sides. At lower arities their declared identity completion preserves the invariant.

These exhaust the constructors, and each constructor acts on strictly smaller subexpressions. Therefore the statement covers **all finite expressions**, with arbitrary finite nesting and arity, for each admitted finite nonempty domain. There is no bound inherited from the generated test set. Characteristic arrays and supports are inverse grade by grade, giving the extensional many-sorted algebra isomorphism claimed in the report.

The theorem does not identify distinct syntax, intensional properties, or arbitrary inherited episode records. The supplied extraction and role/domain alignment are hypotheses. It also does not prove the source's unrestricted consequence theorem through finite checking. The finite-domain consequence statement follows semantically because truth is preserved in each finite nonempty model.

### Open truth versus existential closure

Printed p.64 defines truth of an open Q predicate in a model by satisfaction under **all** assignments. The array readout is consequently `all(coefficients == 1)`. Applying `c` repeatedly computes existential closure and uses `any`. For `F={0}` on `{0,1}` these values are respectively zero and one. They coincide at grade zero. This is now expressly stated in the reviewed result; the main grade-zero examples were always using the correct closure.

## 3. Literal low-arity qualification is necessary

The printed syntax permits unary iota while declaring it unary. The literal sequence clause swaps coordinates one and two before evaluating its operand. If `F={0}`, sequences `(0,0,...)` and `(0,1,...)` agree on the declared one-coordinate prefix but give different values to literal `iota F`.

The problem propagates to a syntactically closed expression: literal `c(iota F)` first prepends a witness and then swaps it with the old first coordinate. Its value is `F(d_1)`, independent of the proposed witness but dependent on the external environment. Thus a scalar coefficient cannot represent that literal sequence interpretation. The independent script executes both witnesses.

The identity completion removes this nonlocality. Sigma at arity zero also needs a convention because the printed formula accesses `d_n`, and the p.64 satisfaction list does not include a separate scalar `c` case. These facts justify the result's qualification; they do not show that the source author's intended theory, or Kuhn's system, is defective.

Terminology caution: when the result says that it agrees with every “well-typed displayed clause,” this must mean the clauses in their **natural coordinate-valid ranges**, not every term admitted by the literal printed syntax. Section 4 makes the distinction explicit, so this is not a blocking ambiguity in the final report.

## 4. Numerical coefficients, negation, and truth wires

The positive transport is correct because support on the nonnegative reals or natural numbers preserves zero, one, finite sums, and products. The exact identities are sufficient for structural induction through contraction, prefix-aligned products, padding, permutations, and equality wiring. The independent probes additionally use exact nonnegative rational weights, so they exercise non-characteristic intermediate values without floating-point artefacts.

Raw numerical contraction counts or sums; it does not itself return existential truth. In nested expressions the counts can count combinations of witnesses or derivations, rather than distinct assignments to a single flattened formula. The report correctly avoids the stronger false assertion.

For general nested negation, zero-testing a nonnegative coefficient satisfies `support(z(x)) = not support(x)`. It is an additional nonlinear operation. `1-x` fails after counting has produced values greater than one. The monotonicity obstruction rules out coefficient complement using only fixed positive Boolean-semiring tensor networks.

The one-hot truth-wire alternative is valid and does not evade that obstruction: Boolean gates act on a different encoding, and the lift `b -> (not b,b)` already contains the nonmonotone step relative to the original single coefficient. Literal-index probes verify nested NOT/AND/OR circuitry and copying, not merely isolated truth tables. This is standard circuit representation, not an inherited real-linear negation theorem.

## 5. Signed coefficients and basis changes

The cancellation witness `(1,-1)` is decisive: numerical contraction gives zero while Boolean projection of its nonzero support gives one. The positive-part test also fails on signed coefficients because two negative factors can multiply to a positive value. The short argument excluding a unital semiring homomorphism from a nonzero ring to the Boolean semiring is valid.

For the displayed matrix `g`, the new vector is `(1,-1)`, the old augmentation returns zero, and the transported covector is `(2,1)`, returning one. The inverse and both contractions are checked independently. This correctly separates invariant numerical transport with all structure moved from preserving old entrywise membership meanings under arbitrary linear changes of basis.

The real-linear OR obstruction is also valid when the domain has at least two elements. It does not forbid the explicitly declared Boolean contraction or nonnegative support quotient.

## 6. Shared witnesses, plurality, and inherited reuse

The equality-network formula has exactly one surviving internal tuple for a fixed output assignment: `b_j=a_alpha(j)` for every `j`. Consequently the same coefficient is returned even for repeated or unused output slots. This proves the general wiring identity directly; finite slot-map tests do not supply that general proof. The report correctly distinguishes diagonal pullback from a trace, which would lose the remaining free coordinate.

The forward/reverse two-element source models agree on the three actual separated-existence assertions, and also on their witness counts and added distinctness scalar, while the joint target differs. The third separated assertion already contains a relation; the failure is lost endpoint binding. Preserving oriented `R`, `F`, and `G` on aligned domain axes repairs this specific computation. It does not show that every structured decomposition fails.

The plurality term yields Boolean truth exactly when at least two F-elements exist and numerical value `d(d-1)` when F is universal. Distinct indices with the same unary label are retained. Quotienting by that label can change truth. None of this makes indices metaphysically primitive or identifies model elements with actual bearers.

The exact inherited reuse is properly bounded:

- Definition 2.1: the representation declaration and its preserved observables are substantive. Changing the real scalar field to Boolean semimodules is a declared change.
- Proposition 4.1: faithful record encoding does not itself prove the new semantic intertwining law.
- Theorem 4.2 and Corollary 4.3: the two source models supply one fibre collision with differing target values, so no decoder of the separated record exists. This is an application, not a newly proved general factorisation theorem.
- Theorem 5.1: cancellation of a signed difference establishes equality of marginals of positive distributions; it does not turn signed support into truth. The source orientation pair is not relabelled as the old parity theorem.
- Proposition 6.2 and Counterexample 6.3: substantive basis/augmentation choice and possible information loss under contraction are correctly reused.
- Theorem 11.2: no dynamics or landscape descent is asserted or inferred here.

## 7. Empty-domain and actuality boundary

The new boundary section is correct and consequential. In an empty-domain array extension, `D^0={()}` still holds and the scalar one exists. Its leading padding is the empty unary array, whose existential contraction is zero. Thus `c(p(1_0)) != 1_0`, while the separately declared scalar operation `c(1_0)=1_0` remains valid.

These controls are explicitly outside the source's nonempty-model class. They do not import the Appendix's all-infinite-sequences definition into an empty domain. They expose the premise needed for dummy-witness elimination in another sort. An inhabited capacity/carrier sort does not establish that a created-token extension is inhabited. The scalar unit or empty tuple does not itself certify an actual token, event, resource, individual, or being. The review makes no theological or metaphysical adjudication.

## 8. Executable assurance and limitations

Files:

- `independent_probes.py`: independently written sequence-oracle and array probes; imports no reviewed code.
- `INDEPENDENT_PROBE_RESULTS.json` and `INDEPENDENT_RUN_OUTPUT.json`: identical independent results.
- `reviewed_snapshot/controls.py`: exact copy of the author's script, executed only in this sibling directory.
- `REPLAY_RUN_OUTPUT.json`: byte-identical to the author's latest `CONTROL_RESULTS.json`.
- `REVIEW_INPUT_BINDINGS.json`: exact snapshot/source bindings.
- `VERIFICATION.json`: final local hash, output-equality, source-stability and assertion-count verification.

The author script's generated expressions are a finite sample, not exhaustive syntax; the independent generator is also bounded and deterministic. Independent primitive exhaustive tests, tail-locality checks, positive rational tests, source countermodels and truth-wire circuitry raise assurance but do not convert enumeration into general proof. The general warrant is the completed-language induction and elementary algebra above.

All writes performed by this reviewer were confined to this new sibling review directory. Existing result, source, code and repository files were not modified by the reviewer. No integration or closure action was taken or authorized by this verdict.
