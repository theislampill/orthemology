# Length-two trace controls implementation plan

Goal: check the approved finite deletion-channel application and keep its inherited statistical/information-theoretic principles separate from new application evidence.

Spec: MODEL_DERIVATION_AND_PROPOSAL.md, approved by the coordinator on 2026-10-07 at 09:42 UTC. Implementation is explicitly authorized in this existing task's local workspace, with existing Lean 4.19 imports only. Independent review is the stopping boundary; no repository change, publishing, or merging.

## Ownership check

The canonical `theory/lineages/h-ics-v5/information-composition-and-self-revision-v5.tex` already states the record-fibre factorisation criterion (lines 53–62), feasible-support output determination (around lines 200–218), and observation congruence (lines 241–257). T9's `Orthemology_Ninth_Research_Final_v1_20261003.md`, sections “What the existing sources already establish”, “One missing bit”, and “Forks merges and occurrences” explicitly credits inherited observation-limited separation, the randomized one-half obstruction, and copied-root/occurrence conservation. It disclaims new general mathematics from renaming those mechanisms.

These prior results own the information principle. No new general nonidentifiability theorem is claimed. The two length-two trace distributions, exact retention/deletion convention, positive-M replication invariant, empty-data case, 5/8 randomized bound, source-label control and mask-position control are a new selected application/verification package. The generic finite sum steps are established mathematics, reproved locally only as needed; the upstream 4.34.1 implementation is not imported or credited as freshly checked.

A scoped search located no matching inherited Lean API for finite total variation or this deletion channel in the inspected T9/continuation interfaces. The canonical information argument inspected here is prose mathematics. This is a bounded reuse finding, not a claim that no equivalent file exists anywhere.

## Architecture and constraints

- One `TraceControls.lean` module, using only already-cached official 4.19 imports.
- Complete traces are the seven binary strings of length at most two, represented by `Fin 7` with explicit names and encoding.
- Masks are `Bool × Bool`; true means retained. Exact mass comes from independent retention probability 1/4.
- A duplicate observation is a constant function `Fin M → Trace`. Its law is the literal pushforward of the one-trace law, summed on its finite support; M=0 is handled separately.
- Randomized decisions use arbitrary real-valued probabilities in [0,1], not just deterministic or rational policies.
- Source labels do not occur in the content channel. This is an explicit model premise, not a verdict about an actual source.
- The fresh-product formula remains written mathematics plus exact coordinating/author finite enumerations. No asymptotic source theorem or decoder is implemented.
- No copied code from the OpenAI math repository is used. No dependency downloads or Lake invocation.

## Tasks and tests

1. Establish import/compiler availability. Write an empty module with the selected imports and a contract referring to the not-yet-implemented endpoint names. Run it and preserve the expected unknown-identifier RED output, separately from any environment/import failure.
2. Define words, masks, seven complete traces, mask weights, actual emission and summation into the complete trace law. Prove normalization/nonnegativity and exact 00/01 mass vectors, including the empty trace.
3. Define exact total variation, copied pushforward masses and finite support. Prove replication injectivity for M>=1, pushforward evaluation on its image, duplicate TV=1/4 for every positive M, and zero-data TV=0.
4. Define arbitrary randomized decisions and equal-prior success. Prove the 5/8 bound by the actual finite mass vector, then compose it with any decision on duplicated traces. Include the missing-mask-independence diagnostic without treating it as a theorem about all shared sources.
5. Add identical-content/different-source law equality and the known-00 retained-position ambiguity (two masks each conditional mass1/2). These instantiate inherited principles; they do not establish actual authentication.
6. Run the same contract GREEN. Preserve ordinary failed proof attempts. Read back each endpoint's full type and axiom dependencies under trust=0 using fresh local objects, binding source/compiler/dependency digests.
7. Run deliberately false scope promotions and require rejection for the expected false proposition, not an import/syntax error. Proposed promotions: TV is3/4 when retention is1/4; positive-M formula holds atM=0; known00 trace0 uniquely identifies the first position; different source labels force different laws.
8. Freeze source, tests, logs and readbacks, report exact scope, and stop for independent review.

## Review focus

Retention p=1/4 is not deletion q=1/4. The empty trace is real data. Fin0 is not covered by the injective-replication proof. Arbitrary randomized decisions require every relevant probability bound. Fresh masks of a shared word are legitimate independent evidence. Source identity and token-position attribution are distinct. Copies can improve availability and fault tolerance. The eight application conditions in the spec remain mandatory.

## Execution ledger

- Coordinating review design and bounded implementation approval recorded before new Lean code.
- Pre-flight: current environment provides Lean4.19 and the selected mathlib cache; no4.34 source build.
- Ruling: use a separate local analysis directory rather than a Git worktree or commits, because the task explicitly forbids repository mutations. Preserve all failures and final source identities in this directory.

- Compiler attempt01 failed because selected minimal imports omitted Fin big-operator lemmas, ordered-sum lemmas and the ring tactic, and the Bool sum lemma lives in Fintype. Added only already-cached imports and corrected that namespace; no theorem scope changed. Retained attempt01 source and diagnostic.
- Coordinating review approved ordered-field generalisation. No Archimedean or convergence statement is being formalised.
- Compiler attempt02 isolated two proof-engineering issues: closed Fin7 equality needed extensional value simplification, and rewriting copies0 to a term containing copies0 recursively looped. Added Fin.ext_iff and made the zero-output canonical function independent of copies. The mathematical model is unchanged.
- Compiler attempt03 exposed simplifier recursion from Fin.ext_iff on closed numerical code comparisons. Switched only equality tests in the complete trace coding to equality of Fin.val; Fin.val is injective, so this is the same observable law. Coordinating review informed; no change to mathematical or dependency scope.

- Author implementation complete: compile07 passed; replay-run03 passed with19theorem readbacks,13rationalfixtures,4semantic negative controls and2157objectbindings. Earlier sources/logs and replay-run01/run02 failures retained. No upstream theorem replay. Independent review is pending.
