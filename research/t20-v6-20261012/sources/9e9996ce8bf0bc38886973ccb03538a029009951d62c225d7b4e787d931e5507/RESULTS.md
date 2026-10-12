# P01 raw-index dependent relational successor

## Result and exact U11 advance

This is a new shadow-research successor, not canonical adoption. It supplies a **syntax-generated first-order dependent relational calculus**, with Pi, represented Sigma, raw-index Id, impredicative All, explicit two-sort substitution, a syntax-inductive fundamental theorem, and a literal-code-exact map into the repaired/qualified P01 candidate dependent core.

The original U11 shortfall was not the existence of generic PER constructors. Those already existed in `P01D`. The missing step was to generate coherent dependent families and their heterogeneous relations from finite syntax, derive the fundamental theorem, and discharge the candidate core's extra `allIntro` uniformity obligation. This successor accomplishes those steps for the explicitly delimited raw-index fragment. It does not claim the full arbitrary-typed-index/frontend obligation.

## The exact fragment

Types are the finite constructors:

- type parameter, bottom, raw-index sort
- identity between two finite SKI index polynomials
- arbitrary nondependent arrow
- Pi and represented Sigma binding one **raw SKI index**
- impredicative All binding one PER/type parameter

Pi/Sigma domains are the raw PER `Conv`, not arbitrary interpreted types. Id is `IdPER rawPER`; it is not Id over an arbitrary type parameter. Free runtime variables are raw-index variables, represented by a total environment; every finite polynomial reads only finitely many entries. There is no rule treating a raw variable as an arbitrary type parameter.

Every term is an actual finite `P01D.Poly`, using the existing K-priority bracket abstraction, pairing, projection and J trackers. The finite typing rules are raw indexing, the unchanged `FiniteDerives` embedding, I/K/S, All introduction/elimination, application, raw-index Pi introduction/elimination, represented Sigma introduction/second projection, explicit raw identity introduction, two-coordinate based J, and explicit open raw conversion. No typing constructor accepts semantic validity, arbitrary coherent families, a `ParamFamily`, or desired uniformity as an input.

## Main proved results

1. **Recursive model and transport.** Every syntax type computes a PER/object and endpoint-aware heterogeneous relation. Coherence under pointwise canonical `Conv` of raw-index environments, endpoint restriction, respectfulness and identity extension are derived by constructor recursion.
2. **Two sorts of capture avoidance.** Actual finite index substitution commutes with interpretation. Actual arbitrary dependent-type substitution also commutes with interpretation. Passing a raw-index Pi/Sigma binder shifts free term indices in each replacement type; passing All shifts free type parameters. Both lifts are substantive and covered by a nested two-sort control.
3. **Fundamental theorem.** `fundamental` proves by induction on every `Has` derivation that arbitrary `REnv` type-parameter links relate the two compiled evaluations at Conv-related raw-index environments. It is not an external validity assumption. Unary soundness and both semantic substitution corollaries follow.
4. **Impredicative dependent All within this fragment.** Its body may contain Pi/Sigma/Id/All and both free sorts. Uniformity is derived using the induction hypothesis at extended endpoint/link environments. All elimination accepts an arbitrary new syntax type, and legal self-instantiation is an explicit typing theorem. This is not universe reification or an arbitrary-typed-index theorem.
5. **Candidate-core representation.** `candidateEnvelope` maps every derivation to an actual `P01Certificate.DependentEnvelope`, with its code binding literally equal to the input polynomial. The named representation theorems identify Pi/Sigma/Id/All with the candidate core's `piTy`, `sigmaTy`, `identityTy`, and `allTy`. The raw binder is an actual tracked `Sub`; index substitution agrees with `Ty.pull` and term substitution. `candidate_all_uniformity` discharges the existing candidate `allIntro` premise, and introduction/elimination retain exact code.

The finite type embedding is identified with the already-qualified successor's recursive interpretation. It is **not** identified with canonical unary `Code`.

## Nonvacuity and negative controls

- The fibre Id(x,I) is inhabited at I and empty at SKK: genuine dependence is proved, not only claimed.
- Dependent reflexivity has concrete code K I. A represented dependent pair and its second projection are typed and inhabited.
- The J motive actually mentions its proof coordinate; the target equality proof is the convertible raw term I I. Both endpoint and proof coordinates are included in transport.
- All A. Pi x. A → Id(x,I) → A has a concrete inhabitant, and its self-instantiation is typed.
- A raw-index variable cannot be typed as an arbitrary type parameter.
- Raw Omega is intentionally typed at the raw-index sort and has no normal reduct. Thus the new soundness theorem does not imply source normalization, and it cannot inherit `FiniteDerives`' source-SN conclusion.
- Omitting dependent-Pi coherence can destroy symmetry: a concrete bare Pi relation is related in one direction and not the reverse. It is explicitly not an instance of the lawful `PiPER` constructor.
- Most importantly, there is a legitimate respectful link at the inhabited polymorphic identity PER relating I and SKK, while Id(x,I) changes from inhabited to empty across that link. **Arbitrary heterogeneous index-link transport is false for these raw identity fibres.** Conv-only index transport is a mathematical restriction, not a presentation choice.

The independent review adds further stress controls, including an inhabited Pi with provably unequal nonempty fibres, nested mixed binders, a J witness changing both coordinates, and mutation failures at omitted index lift/type lift/proof-coordinate transport. Those independent additions have their own report and receive no duplicate source credit here.

## Qualification and authority

The authoritative receipt is `qualification-final/QUALIFICATION.json`. It records a fresh build of every local imported predecessor module and all five new modules, using Lean 4.19.0 commit 6caaee842e94 and pinned Mathlib c44e0c8ee63ca166450922a373c7409c5d26b00b. Only pinned standard-library/Mathlib package caches are reused read-only; no parent/successor `.olean` is used as a local import.

The final run rebuilt 31 local modules before the audit and checked 114 top-level declarations, including 69 theorem declarations. Every declared top-level item in the five new modules receives exact type and axiom readback. The allowed axiom union is limited to propext, Quot.sound, and Classical.choice. New sources are scanned with the predecessor's comment/string-aware proof-hygiene guard, and new-module compiler output must be empty. Contract modules check that promised targets exist. The receipt binds all source bytes, local artifacts, compiler, qualification driver/helpers, predecessor inventory/receipt, sealed successor ZIP and dependency revisions. Counts are taken from that receipt, not advertised as counts of novel mathematical theorems.

Canonical checkout 03e2604dfcef278b01c60d19b05370fcec4194b6 remains clean and unchanged. The sealed P01 recursive successor SHA256 remains e4698d9acf9f2b3ab637c0b35bbfb361b8c31a58368bef4ddbace53693867f24. No original theorem, source Conv, checkpoint, canonical status, or historical disposition is rewritten.
