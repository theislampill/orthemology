# Actual auxiliary certificate checker code realizers

All five actual auxiliary checkers are now realized by total primitive-recursive functions on the unchanged retained natural-number encodings:

- `checkStepCode c t u`, exactly `AuxiliaryCertificates.checkStep` on encoded StepCert/Term inputs.
- `checkRedCode c t u`, exactly the actual finite reduction checker, including intermediate-term matching.
- `checkFiniteCode c t A`, exactly the actual finite typing checker, including TypeCode instantiation and finite reduction certificates.
- `checkPolyCode c p q`, exactly the actual polynomial conversion checker, including orientation, transitivity middle terms, congruence, and atom/application bridge syntax.
- `checkLookupCode c Γ n A`, exactly the actual lookup checker, including telescope encoding and binder-sensitive weakening.

Every checker has an unconditional Mathlib `Primrec` theorem for its right-nested Nat tuple input and an exactness theorem named `check…Code_exact`. The argument order is certificate first, then the original source checker arguments. No source `Primcodable` instance, checker-computability hypothesis, alternate codec, new proof rule, decoder-computability premise, or runtime/executable-to-PR inference is used.

## Mechanism

Actual constructor encodings are proved by kernel-checked definitional equality. External-sort fields retain their leaf wrappers; recursive same-sort fields remain direct trees. Each checker uses the frozen finite dependency evaluator whose `Primrec` proof is based on Mathlib `Primrec.nat_omega_rec'`. Recursive exactness proofs explicitly establish strict code decrease using `field_lt_pack`; field claims and requested endpoints are compared by exact retained-code equality. The finite checker uses the separately proved exact TypeCode substitution realizer. The lookup checker uses the separately proved exact Ty weakening realizer.

## Controls

Positive and rejecting assertions exercise contextual Step, reduction chaining, duplicate field claims, symmetry orientation, transitivity middle mismatch, bridge atom/application distinction, polymorphic instantiation, finite reduction mismatch, and actual identity-endpoint weakening. Six deliberately false mutation assertions must fail with their recorded Lean diagnostic. An additional positive countercontrol proves that an ungated checker extension accepts a malformed polynomial payload whose canonical grammar check rejects it.

## Boundary

These natural functions are total extensions and are only specified on actual encoded inputs. They do not validate arbitrary certificate or payload codes. A separate canonical-image gate is mandatory in a serialized checker. This package does not prove whole-source certificate-checker computability, source derivability RE, the final reduction, or T20 closure.

Fresh Lean 4.19.0 `--trust=0` replay is recorded in `validation/AUTHOR_REPLAY.json`, with exact source, retained-object, and toolchain pins checked before and after. The large inherited baseline is not rebuilt. Selected transformation/foundation sources and this complete layer are freshly compiled. Audit allowlist: `propext`, `Classical.choice`, `Quot.sound` only.
