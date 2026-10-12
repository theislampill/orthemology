# Exact binder-sensitive syntax transformations on retained codes

## Proved operations

Every numerical operation below has an unconditional Mathlib `Primrec`/`Primrec₂` theorem and an exactness theorem on the unchanged retained source encoding.

- `freeZeroCode`, `dropCode`, `abstractCode`: actual P01D.freeZero/drop/abstract. Abstraction follows the exact source branch structure, including the K branch for a body without variable zero.
- `substituteCode`: actual P01D.psub for a finite image list followed by an explicitly shifted variable tail. Inputs are first-order finite data, not arbitrary function environments.
- `shiftCode`: all variable shifts, including actual `pren Nat.succ`.
- `instPolyCode`: actual single polynomial substitution `P01F.cons a Poly.var`.
- `liftEnvCode`: exact coded update for the actual capture-avoiding `P01D.pup`. The theorem `lifted_substituteCode_exact` connects the update directly to source substitution after entering a binder.
- `checkTyScope`: exact actual `TyScoped`; pi/sigma increment the term-variable bound in the codomain, while all does not.
- `substTyCode`: actual `P01AC.subst` for every finite polynomial environment, lifting it beneath dependent term binders and substituting the identity polynomials.
- `wkTyCode`, `instTyCode`: actual P01AC.wk and P01AC.inst.

Central declarations are `primrec_abstractCode`/`abstractCode_exact`, `primrec_substituteCode`/`substituteCode_exact`, `primrec_liftEnvCode`/`lifted_substituteCode_exact`, `primrec_checkTyScope`/`checkTyScope_exact`, and `primrec_substTyCode`/`substTyCode_exact`.

## Exact finite-environment interface

`finiteEnv images tailShift n = images[n]?.getD (.var (n - images.length + tailShift))`.

Its binder lift is proved extensionally equal to actual pup:

`finiteEnv (.var 0 :: images.map (pren Nat.succ)) (tailShift+1) = pup (finiteEnv images tailShift)`.

This is essential: entering a binder shifts stored substitution images as well as preserving the new variable zero. The encoded image list has type List Nat, where each entry is the existing source code. This is not a replacement source encoding.

## Method and shared foundation

Poly analysis and finite substitution use Mathlib nat_strong_rec with exact arithmetic child-code decrease. Binder-sensitive Ty scoping reuses the validity worker's small `evaluate` engine, whose primitive-recursiveness is proved with Mathlib nat_omega_rec'. Ty term substitution uses a small natural-output bounded fold, also proved with nat_omega_rec'. These are explicit first-order recursion proofs, not an inference from Lean executability.

Only `ExactSyntaxValidity.lean` and `CoreGrammar.lean` are used from the parallel validity work. Their actual validity-recognition theorem is not assumed. The verifier recompiles those foundation sources and all selected dependencies into fresh output.

## Discriminating controls

Positive controls cover bound and free variables, literal closed-body abstraction, both application subtrees, finite images versus tail fallback, nonzero tail shifts, one and two nested pi/sigma binders, preserved bound variables, correctly shifted substituted free variables, and unchanged term substitution beneath all.

Four false controls must be rejected: treating all as a term binder, failing to shift a polynomial substitution image, replacing the compiler's closed-body K branch by the S branch, and capture-causing type substitution under pi.

## Scope and next actual dependency

All exactness statements concern genuine encoded source data. Malformed inputs are totalized without a claim that the outputs are valid or coincide with a decoder's behavior. The separate canonical validator must establish representability before a code checker relies on them. For source r.e., a canonical checker sound on every accepted code and exact on actual certificate encodings suffices; reproducing an operational decoder on all noncanonical codes is unnecessary.

This layer does **not yet prove** type-variable renaming/substitution, mixed substitution, finite TypeCode interpretation/support, rule payload computability, auxiliary certificate checker computability, or full Joint/E derivability r.e. The next transformation layer is finite type environments, their term-weakening update under pi/sigma and type-weakening update under all, and exactness to `P01AC.mixed`, `tinst`, and `tsubst (typeImages τ)`. That work belongs in a separate additive directory so this coherent layer can be reviewed unchanged.

No accepted prior family/scoping source was edited. No custom axiom, admitted proof, source adoption, integration, or T20 closure is claimed. Central dependency audits allow only propext, Classical.choice, and Quot.sound.

## Replay

Run `python hase-coded-poly-transformations-20261010/verify.py`. It pins retained final-codec imports, the accepted upstream source layer, shared foundation sources, and this candidate. It compiles selected source modules with Lean 4.19 `--trust=0` in fresh output, rejects all four mutations, and rechecks pins. It does not rebuild the full baseline.

Failed proof attempts remain in diagnostics with their logs: simplification order in finite substitution; binder environment map normalization in type substitution; missing type annotations/reverse unfolding in TypeScope; and exploratory source-name probes. They are not accepted proof inputs.
