# Exact canonical syntax validity on the retained encoding

## Proved result

The unchanged existing `Encodable` instances now have an actual Mathlib primitive-recursive canonical-image validator for all four core syntax sorts:

- `primrec_valid : Primrec₂ valid`
- `valid_term c : valid 0 c = true ↔ ∃ a : Term, encode a = c`
- `valid_typeCode c : valid 1 c = true ↔ ∃ a : TypeCode, encode a = c`
- `valid_poly c : valid 2 c = true ↔ ∃ a : Poly, encode a = c`
- `valid_ty c : valid 3 c = true ↔ ∃ a : Ty, encode a = c`

These theorems validate all six Term, four TypeCode, three Poly, and seven Ty constructors. They prove both soundness on arbitrary natural inputs and completeness for every actual encoded object. They use the literal retained constructor encodings, with no alternate syntax codec and no assumed source `Primcodable` or `Computable` instance.

## Decoder correspondence, precisely scoped

`normalize s c` returns `some c` exactly when the corresponding validator accepts, and returns `none` otherwise. It is primitive recursive. For each core sort, `normalize_*` proves:

`normalize s c = (Encodable.decode₂ SourceSort c).map Encodable.encode`

The four `primrec_*_decode₂_reencode` theorems consequently prove that `c ↦ encode (decode₂ SourceSort c)` is primitive recursive under the existing source codec. Here `decode₂` is Mathlib's canonicality-checking decoder. This does **not** assert that an arbitrary `Encodable.decode` is canonical, does not replace the existing instance, and does not claim equivalence to the old certificate checker on all natural numbers. Canonical-image validation suffices to build a checker accepting exactly codes of genuine certificates, once the remaining certificate grammar/checker operations are proved.

The separately preserved optional `hase-exact-decoder-canonicality-20261010` result proves ordinary `decode` canonicality for Term only; it is not an input to this package. TypeCode/Poly/Ty ordinary-decoder canonicality was deliberately left unattempted after the canonical checker route was chosen.

## Reusable recursion engine

`ExactSyntaxValidity.evaluate` takes a Boolean local shape check and a finite list of sorted code dependencies. Recursive calls are guarded by strict decrease of the natural code. `primrec_evaluate` proves the evaluator primitive recursive whenever the shape and dependency-list functions are primitive recursive, using Mathlib's existing `Primrec.nat_omega_rec'` engine. The proof filters the dependency list only to construct the primitive-recursion witness and separately checks **all** bounds, so an invalid nondecreasing child is rejected, never silently ignored.

`evaluate_exact` and `evaluate_exact_of_image` provide image-correspondence induction principles. The second needs code-decrease only for actual canonical objects; rejection guards preserve soundness for arbitrary malformed inputs.

`ExactSyntaxValidity.lean` and `CoreGrammar.lean` were frozen early for the binder-transformation worker; `validation/FOUNDATION_FREEZE.json` pins their source and original author objects. They are unchanged in this final package.

## Why malformed inputs are rejected

The shape checker reconstructs the complete candidate code from its arithmetic fields and compares it to the input. This checks the constructor tag leaf, every payload node, arity, required external-sort leaf wrappers, and final zero-leaf terminator. Recursive fields are checked in their actual expected sort: Poly atoms require Term codes; Ty identity has one Ty child and two leaf-wrapped Poly children. A tag or a scoping Boolean alone cannot pass these checks.

Sort codes are not artificially made disjoint. Actual code coincidences such as Term.k/Ty.bottom and TypeCode.var/Poly.var/Ty.param are preserved and tested.

## Verification

Run `python hase-exact-syntax-validity-20261010/verify.py`.

The verifier compiles the upstream FamilyComputability and CodedScope sources, then all eight new modules, into a fresh output directory with retained Lean 4.19 `--trust=0` and the final codec object pins. It verifies input hashes before and after. This is a selected-module replay over pinned dependencies, not a full-baseline rebuild.

Controls include universal source-code acceptance, executable acceptance for all 20 constructor forms, zero/unknown-sort/tag failures, bad tag shape, missing/extra payload, wrong terminator, missing leaf wrapper, actual cross-sort rejection, all three Ty-identity fields, the known scoping-versus-validity distinction, true cross-sort code aliases, and a self-child guard. Five false controls must fail: bad terminator acceptance, invalid atom payload acceptance, ignoring the right identity Poly, a wrong TypeCode tag, and ignoring a nondecreasing child.

Central audited axioms are limited to `propext`, `Classical.choice`, and `Quot.sound`. No custom axiom, admitted proof, source adoption, protected edit, integration, source-derivability r.e., or T20 closure is claimed.

## Preserved diagnostics

Early private-name/API probes are retained. The initial inline Ty-shape PR proof hit a definitional-equality elaboration hotspot at composition through a triple-coded domain; the superseded high-heartbeat run was interrupted (exit 130), and bounded probes preserved the failure. Direct node-composition proves the same statement without that hotspot. An initial malformed-input control attempted `decide` on a well-founded recursive definition; this correctly did not reduce. The accepted controls use the evaluator equation, local shape evaluation, and kernel-checked child-rejection lemmas, with separate runtime checks. Temporary missing-import and Boolean-equality-parenthesization diagnostics are not accepted inputs.

## Remaining actual checker dependency

This removes the core syntax canonical-validity obligation only. Auxiliary certificate/payload/Claim/Rule/SerialCert validity, actual remaining checker operations, all auxiliary checker branches, and serialized checker recursion still need their own proofs. The final source r.e. composition remains conditional on those real results.
