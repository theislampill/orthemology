# Independent source and kernel review: syntactic substitution admissibility

## Decision

Accept the bounded extension at candidate v1. Both universal theorems are proved for the exact original `P01DF.Has` judgement and arbitrary total substitution maps:

- `Has p A → Has (psub σ p) (substIndex σ A)`.
- `Has p A → Has p (substType τ A)`.

There is no new typing, well-formedness, closed-image, semantic-validity, or finite-support premise. The finite-support argument is an internal theorem about the existing finite type syntax. The type theorem preserves the literal source polynomial, including opaque composite finite atoms.

This conclusion combines independent mathematical/source inspection with a separate source-only kernel build. It is not human-specialist validation or a claim of independent invention.

## Source custody and verification

Accepted input snapshot: commit `19de267cd41d2a5eeeb3eaf0b91562f706e2a916`, tree `08a6452e50e8e4791d02410d1c1732875e520f2e`.

The exact 28-module actual local import closure was independently reconstructed from hash-pinned accepted source bytes. No compiled author artifacts were copied. All 28 dependencies, five frozen candidate/contract/readback modules, and the new independent-control module compiled successfully in a separate build location. All 34 invocations exited zero, on the first review attempt. Dependency compilation is reconstruction evidence, not credit for rerunning prior scientific suites.

Toolchain: Lean 4.19.0, Mathlib revision `c44e0c8ee63ca166450922a373c7409c5d26b00b`. The existing qualified toolchain was reused without downloads or installations. The review used a single serial compiler lane, `-j1`, default heartbeat and recursion settings, and a 180-second cap per module. Compilation began only after the authored theorem and exact contract had compiled and the source reconstruction was hash-complete. The full frozen candidate was copied and identity-checked before its separate compilation.

All accepted source hashes and frozen candidate hashes were checked again after compilation and remained unchanged. The accompanying verification record supplies per-module identities, timestamps and results. No canonical source edit, push, merge or publication was performed.

Core candidate identities:

- `SubstitutionSyntax`: `ad4e0896abf3a7a3354a14db6743349421520d10eca0790cd632821ecd995649`.
- `SubstitutionAdmissibility`: `6ae02ec07b67a81f3019192118e44d4ac37cd26f9ad61f09831c8fafd55ce121`.
- `SubstitutionControls`: `c3d31d2c24e9db193bbe60801bffdbc54e1a61ddb13a21ca19672259c57e7dec`.

## Mathematical inspection

The original `Has` has fifteen constructors and remains unchanged. The index theorem uses its actual recursor, with a case for every constructor. `raw` admits each substituted raw polynomial. `finite` reuses the original finite derivation because index substitution fixes its embedded type and opaque atom. The combinator, All, and application cases reconstruct their exact constructors. Pi introduction uses literal abstraction naturality with `pup σ`; elimination and Sigma cases use literal index-instantiation identities. Identity introduction and conversion use the seven-case `PolyConv` substitution proof. J uses `pup (pup σ)` on the motive, with proof coordinate 0, endpoint coordinate 1, and all outer indices shifted through both binders.

The equations are equalities of `Ty` and `Poly` syntax, not equalities of interpretations. Source readback confirms the original raw-index syntax, conversion rules, substitution operations, lifts, and judgement. There is no atom-expansion rule, abstraction-congruence extension, or new calculus.

The type theorem uses unconditional existing All introduction/elimination, rather than attempting to reconstruct arbitrary dependent images through the finite calculus. The finite-prefix successor equation cancels the temporary type shift of each previously inserted image. Hence free type variables in an image survive later eliminations. `freeTypeBound` uses maximum for arrows, preserves the bound through Pi/Sigma, and takes predecessor through All. The agreement lemma justifies replacing the bounded prefix by the caller's unrestricted total map. No caller restriction follows from this proof device.

Type/index interchange correctly transforms the type images: `fun n => substIndex σ (τ n)`. An unchanged-image commutation law is deliberately rejected by a syntax inequality. Type composition correctly substitutes into earlier images; its order is not interchangeable.

## Discriminating controls

The candidate's controls passed independently. These include raw-binder capture avoidance and its wrong-lift inequality; free type-image capture during successive eliminations; open terms in both sorts; a J motive using proof, endpoint and outer coordinates; an opaque `atom skk` substituted into genuinely dependent types; actual composition with the accepted dependent-polymorphic certificate and an open Sigma pair; and reuse through Sigma projection, exact candidate-envelope code retention, and scoped canonical Sigma admission.

The additional independent controls were authored for this review and all passed:

1. An inserted image has its own All and Sigma binders and enters a surrounding All/Pi/Sigma nest. Internal bound coordinates remain fixed while both free sorts shift correctly. A wrong raw-coordinate capture is proved unequal.
2. Alternating All/Pi/Sigma binders preserve both distinct bound raw coordinates while transforming an outer index into an open application.
3. A certificate using sparse type parameter 7 is instantiated with a dependent image. A support bound is checked against a sparse parameter, and an insufficient prefix is proved different from the requested substitution.
4. Two noncommuting type maps produce a concrete `Has` certificate in the specified composition order; reversing them is proved to produce different syntax.
5. J's proof and endpoint coordinates occur underneath an additional Pi binder, while another coordinate remains bound there. The exact transformed syntax and nonexchangeability of proof/endpoint are checked.
6. Explicit independent contract declarations accept exactly the two universal target signatures.

These are discriminating symbolic checks, not an exhaustive enumerator over inputs.

## Axioms and scope

The theorem and definition outputs were read, including the generated proof term for the fifteen-case index theorem and the finite-prefix type theorem. Both universal targets, their composition/interchange consequences, and substantive certificate controls report only `propext` and `Quot.sound`. There are no custom axioms, admitted holes, unsafe proof substitutes, or weakened conclusions in the new sources. Several literal independent syntax controls use no axioms at all. The claims are kernel proofs in the existing Lean logical foundation, not claims of an axiom-free development.

The result is proof-level constructive substitution admissibility and reusable source certificates. `Has` lives in `Prop`; this review does not establish a serialized derivation transformer, parser/checker interface, executable extraction, or successful transformation of externally serialized proof inputs. It does not establish general dependent type theory, normalization, unrestricted heterogeneous typed-index transport, repaired recursive unary-Code equality, or broader project closure. No physical or metaphysical conclusion follows.

The earlier source obstructions and scope limits are unaffected. No new counterexample to either exact target was found, and no issue remains blocking this bounded theorem extension.
