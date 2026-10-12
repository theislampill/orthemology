# Formal coverage and assurance boundary

## What “source complete” means in this packet

Every declaration in the candidate inventory has an authored definition or proof
body; no omitted proof, assumed theorem axiom or placeholder is an intended
completion step. This is an **authoring** statement, not a successful-elaboration
statement. At Lean 4.19.0, tactic/notation/type errors may still be exposed and
must be repaired against the unchanged theorem contract before formal credit.
Static source hygiene and successful Python tests cannot establish that a Lean
proof body elaborates.

The definitive machine inventory is `formal/SOURCE_INVENTORY.json`, including
all source hashes, modules, imports, declaration names and source-line beginnings.
`formal/TARGETS.json` is the convenient target view. Actual expected load-bearing
theorem types are also supplied as declarations in `P01TypeAssertions.lean`.
`P01Audit.lean` contains exact `#check`, transitive `#ortho_audit`, and
`#print axioms` commands for every public explicit candidate declaration.

## Candidate modules

| Module | Exact role |
|---|---|
| P01SNReflection | Unchanged attempt-0001 candidate for accessibility reflection along positive simulations; no inherited kernel credit. |
| P01TypeAlgebra | Canonical type renaming/substitution identities, compositions and binder squares. |
| P01LambdaSyntax | Curry runtime syntax, capture-avoiding operations, beta relation and closure laws. |
| P01SystemF | Actual five-rule Curry typing, both substitutions, lambda generation through forall rules, subject reduction. |
| P01Translation | Exact Term/TypeCode translation; all seven FiniteDerives rules; positive compatible simulation; finite/chain consequences; conversion preservation only. |
| P01Candidates | Direct source reducibility candidates, I/K/S expansion, all/intersection, full FiniteDerives strong normalisation. |
| P01Confluence | Raw parallel complete developments, confluence, normal form existence/uniqueness, conversion characterisation, I/SKK separation. |
| P01Omega | Actual Ω reduct invariant, nonnormalisability and finite-source nonrepresentability. |
| P01ReflectionCountermodel | Target-beta/raw-source-conversion nonreflection, in a separate module so direct source proofs do not depend on the System-F bridge. |
| P01Polynomials | Finite SKI tracker substitution, K-priority abstraction beta, literal lifted-substitution naturality and after-application conversion, pair/J trackers. |
| P01PER | Endpoint-aware PER/link operations, coherent Pi, represented Sigma, identity/based J, explicit parametric All interfaces. |
| P01DependentCore | Intrinsic valid contexts/types/tracked terms/substitutions; structural laws; Pi/Sigma/identity/type-binder/All constructors. |
| P01ContextualJ | Based J in the actual endpoint-plus-proof context and explicit proof-inspecting incoherence witness. |
| P01Certificates | Positive raw path replay, exact finite/dependent proof envelopes, refusal-preserving replay soundness and exact target-vocabulary nonimage proofs. |
| P01Examples | Nonempty tracked instances: polymorphic identity with discharged uniformity, self-instantiation, dependent reflexivity, represented pair and contextual J. |
| P01GeneratedExports | Six actual generated finite Certs, canonical check calls, exact bound output objects and theorem targets; uncompiled. |
| P01UniverseBoundary | Exact PER Realiser specialisation of preserved Girard-sensitive no-self-product obstruction, separate from legal All self-instantiation. |
| P01TypeAssertions | Explicit expected types of the principal claims; compilation must establish these, not a parser's guessed theorem type. |

The 12 vendor modules are byte-for-byte canonical preimages. They are compiled
as dependencies by the external driver, not relabelled as new mathematics. Their
historical comments and embedded commands are source evidence, not new campaign
instructions. The lake project is new; its root package name is p01Attempt3.
The original Mathlib/transitive dependency revisions are preserved exactly in
the new lock. Changing that root package name is separately recorded as project
metadata, not a change to the canonical lock preimage retained in `inputs/`.

## Explicit interfaces that are not silently discharged

A coherent PER family must supply coherence. A contextual substitution must
supply its finite-code tracking equations. A ParamFamily must supply its body
relation and identity-extension proof. All introduction needs a uniformity proof,
not just unary body membership. Based J needs proof-coordinate as well as
endpoint coherence. The proof-carrying core checks these as formation/typing
obligations; they are not global axioms about arbitrary semantic objects.

The preserved U10 ordinary model and abstraction theorem explain those
hypotheses at their stated syntax scope. This packet does not newly claim a
kernel-mechanised recursive interpreter for every ordinary U10 construction.
The All instances in P01Examples supply real bodies/proofs rather than leaving
that interface wholly uninhabited.

## Refinement scope is intentionally exact

The formal replay target verifies a decoded, explicitly bound target object.
It does not prove a theorem about the semantics of arbitrary untrusted JSON or
about every branch of the Python interpreter. The canonical finite exporter is
partial, with an ordinary structural proof for its successful domain and actual
generated fixture targets. The new dependent envelope gives universal
proof-replay soundness for the intrinsic core. A typed frontend Id/Sigma result
refutes *total literal export to the unchanged TypeCode vocabulary*, not the
soundness of the partial replay boundary. No total interpreter is claimed under
a misleading “partial proof complete” label.

## Actual execution state

Exact pin: leanprover/lean4:v4.19.0, commit prefix6caaee842e94.
Mathlib: c44e0c8ee63ca166450922a373c7409c5d26b00b.
Actual local/Elan/project/offline search found no compiler. Exact release download
attempts failed, including a direct-IP transport check. The final strict driver
returned HOST_EXECUTION_BLOCKED with exit3, no compiled artifacts and an empty
declaration/axiom readback. The source inventory hash is bound in that report.

No `sorryAx`, alternate compiler version, elaboration failure, empty/stale
artifact or incomplete audit is accepted. The allowed transitive axiom set is
{propext, Classical.choice, Quot.sound}; **that is a policy, not an observed
axiom list for the uncompiled candidates**. Historical 4.32.2 outputs and mapped
4.19.0 outputs remain separately preserved evidence, never new P01 proof credit.

The later driver exits nonzero on missing compiler, source mismatch, wrong
version/commit, dependency drift, failed build, empty output, incomplete target
coverage, missing type header, sorryAx or unapproved axioms. Failure logs survive.
Only real compiler output can populate a kernel-qualified receipt. Policy tests
use synthetic strings to check refusals and never manufacture such a receipt.
