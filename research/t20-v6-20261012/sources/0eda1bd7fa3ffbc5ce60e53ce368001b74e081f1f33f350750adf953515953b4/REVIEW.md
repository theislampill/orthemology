# Independent review: complete-development extraction and source replay

10 October 2026.

## Disposition

PASS for the exact bounded addition. No blocking finding remains after the frontend resource and open-scope fixes described below. The new result is a computable count extractor on the actual closed-input HasE domain, justified by complete-development cofinality on the actual open carrier, together with source-faithful finite conversion/source-instance certificates. The independently checked partial negative theorem rejects only the specific closed Church-input typing judgment when its finite premises succeed.

This is not a normal-order completeness proof, strong normalization theorem, second Church-canonicity result, complexity bound, universal source-completeness theorem, or a solution of the universal bound-variable scalar-fusion judgment. The latter and its negation remain open.

## What was established

1. `OpenDevelopments.development_complete` proves that any actual `OpenTermStandardness.T` term convertible by the actual `Conv` to a parallel-rigid normal form reaches that form by repeated executable `dev`. The proof uses the triangle law twice to obtain development monotonicity, lifts it over finite iteration, proves reachability invariant in both directions along a parallel step, then covers the complete actual conversion grammar through `conv_chain`. All seven conversion constructors are covered: reflexivity, symmetry, transitivity, application congruence, I, K, and S. Variables, I/K/S, zero/one, and application are the original open carrier, without substitute markers or a changed language.

2. The parallel relation and triangle proof are an explicit open-variable port of inherited `P01Confluence`. The new cofinality/search composition is the relevant additional work. Ordinary compatible redex-freedom implies the parallel rigidity required by the theorem, through `redexFree_normal` and the exact open `Step`. Neither Lean nor Python treats `dev t = t` as its successful stopping condition.

3. For every supplied actual `HasE [] n N`, `closed_HasE_development_terminates` gives one count k and finite development indices for both original generic-open scalar endpoints. The right endpoint retains the literal imported `originalQ`; the left retains the original n. The common target is exactly `var(1)^k var(0)`. This uses the already reviewed full-PER/closed-source standardness result to obtain conversion, then the new strategy theorem. It does not silently strengthen inherited `FiniteDerives` to arbitrary `HasE`.

4. `readIteration` is executable structural recognition returning a count with an equality proof. `extractIteration` is an ordinary computable Lean definition using the decidable `Nat.find` search, not `Classical.choose` as a runtime data source. Its existence/termination arguments live in Prop and are erased. `extractIteration_uniform` identifies the returned count with the inherited uniform count for all raw open f/a. Independent evaluation returned 0, 1, 2, 2, 2 for source numerals 0/1/2, K numeral2 Ω, and atom-packed numeral2. Logical dependencies include ordinary `propext`, `Classical.choice`, and `Quot.sound`; this fact is not concealed and does not make the executable definition a choice oracle.

5. `DomainControls.padded_has` is an actual source typing proof for K numeral(k) Ω, obtained by the actual conversion rule without typing Ω. The inherited raw three-cycle proves this term is not strongly normalizing. Independently, `IndependentControls.padded_not_open_SN` reproduces the cycle under the exact new open `Step` and proves non-accessibility there. Thus the weak-normalization domain genuinely exceeds strong normalization, while the chosen development discards the divergent argument.

6. `ScalarCertificates` checks finite contraction addresses on the actual open carrier and returns evidence of actual compatible conversion. The checker is separate from the complete-development producer. `checkedIteration` and `checkedRightIteration` bind the count to exact iteration syntax. Generic reflection explicitly passes through the inherited term/atom/application bridge and produces actual source `PolyConvPlus`, rather than silently identifying packed atoms with polynomial applications.

7. `sourceInstanceFromConversions` and the exact-source wrapper reconstruct actual `HasE [] (c3 n) (inst frozen_W_body n)` from the two finite iteration conversions and an actual closed-scope proof. They use the independently typed iteration and the original HasE conversion, identity, Pi, and All rules. They do not infer `HasE [] n N` from JSON, and do not call semantic standardness or the prior general closed-instance theorem. A checked declaration-dependency audit verifies this separation. The generic source-reconstruction theorem and address-checker API have no `Classical.choice` dependency; concrete literal-Q rebinding may introduce it through its equality proof, and is covered by the same ordinary-axiom audit. It is a positive source proof, not a serialized full source derivation tree or a universal judgment.

8. `NonstandardRejection.checked_non_iteration_refutes` has the precise negative conclusion `¬ HasE [] n N`. Its executable premises require a successful exact replay of the left endpoint to z, `normalB z = true`, and `readIteration z = none`. `normalB_sound` proves redex-freedom against the exact open Step. Assuming closed Church typing then contradicts normal-form uniqueness. The literal raw-zero control kernel-checks with an empty trace. Raw zero is distinct from Church numeral zero K I. This theorem does not reject the scalar-instance target, decide arbitrary typability, or turn resource exhaustion into evidence. A Python normal-non-iteration status remains diagnostic until these exact kernel obligations are discharged.

## Source binding and adversarial results

The Lean source export was independently rerun and was byte-identical to `source_ast.json`, preserving literal Poly variable/atom/application boundaries and the full original Q. `LiteralSourceQ.originalQ_expanded` is a kernel-proved equality to the unchanged imported source symbol. The JSON export itself is not trusted as proof.

Two independent attack controls demonstrate the boundary:

- Replacing the literal source n under unchanged certified count and paths makes both relevant Lean replay-success propositions false. Python also rejects a certificate when `expected_input` differs. The emitted theorem states its full literal input. A standalone certificate without an external intended-input binding cannot establish what input its caller intended; known source numeral aliases additionally have exact kernel input-binding theorems.
- After deliberately substituting local Q=I and recomputing its local digest, Python can certify the tampered local problem. Replaying that emitted certificate against the actual `FullPER.Application.originalQ` fails: Lean proves the asserted right-replay success is false. Restoring the actual Q digest also makes the Python checker reject the fake certificate. Thus Python-only success is diagnostic, and the literal kernel rebinding supplies the source-Q guarantee.

The intentionally failing files are named `ChangedInputMustFail.lean` and `FakeQMustFail.lean`; their nonzero exits and error logs are expected negative evidence. Lean emits error-recovery `sorryAx` mentions in these failed commands. No output from either failure is accepted, imported, or counted as a theorem. All accepted replays have zero exits, no admitted proofs, and no unexpected axioms.

Fifteen author Python tests pass independently. They cover actual numerals 0–6, compound atoms, I wrapping, discarded Ω, corrupted paths/endpoints/counts/inputs/digests, invalid constructors and Boolean naturals, exhaustion, open-input scope, producer/checker separation, and avoiding iteration allocation from an untrusted huge claimed count. Four author Lean rejection theorems independently pass for invalid addresses, nonredexes, forged endpoints, and forged counts.

The ten concrete generated cases were independently regenerated byte-for-byte and kernel-checked: source numerals 0–6, packed numeral3, wrapped numeral4, and K numeral2 Ω. Every closed case yields both exact iteration conversions and the exact original source instance. An open K numeral0 (var42) conversion certificate independently compiles while omitting a closed source-instance claim.

An additional deterministic reviewer sample contains 266 open terms, including all leaf constructors and structured I/K/S/application cases. Every Python development result agrees with independent finite address replay. A further 532 Lean equations check these results against the actual `dev` and polynomial interpretation functions. These are implementation cross-checks, not a formal equivalence proof for the Python runtime or a replacement for the general strategy theorem.

## Issues resolved during review

- Valid deeply nested input validation/interpretation initially occurred outside resource handling. The producer now reports host recursion/memory exhaustion as inconclusive. Certificate checking lets host exhaustion reach the same outer handler rather than conflating it with an invalid certificate.
- The emitter initially attempted a closed-scope source-instance proof for every valid conversion certificate, including open erased-variable inputs. It now emits conversion/iteration proofs for open input, and the actual scope/source-instance reconstruction only for checked closed syntax.
- Numeral6 exceeds the nominal 200,000-node diagnostic budget. This remains an explicit inconclusive regression test; a separate 5,000,000-node bounded run succeeds. No efficiency or total bounded-machine claim is made.
- Two reviewer test elaboration issues were corrected locally: a command syntax typo in the dependency audit and a need to simplify source abstraction before a literal inequality. They did not alter author proof source.

## Verification and preservation boundaries

Lean 4.19.0 was used with `--trust=0` for accepted new modules and independent controls. The compiler binary was hash-checked, not bootstrap verified. The reviewer reused 92 previously checked prerequisite objects plus the two independently reviewed closed-source helper objects; no inherited 83-module rebuild was performed. The 83 pinned original source files, relevant package manifests, source/object/log bindings, and predecessor receipts were rehashed: 429 inherited bindings were checked in the reviewer input record. The author's separate INPUTS additionally binds 94 reused objects and 18 inspected sources/receipts, including executable Nat.find's implementation.

All work is in the separate review directory. Author and predecessor proof sources were preserved. Exact accepted source/object/log hashes, expected-negative results, the final author records, and review scripts are bound in the review receipt and manifest. Reused third-party libraries and environment/toolchain dependencies remain explicit; this review is not a claim of a bootstrap-independent or universally standalone build.
