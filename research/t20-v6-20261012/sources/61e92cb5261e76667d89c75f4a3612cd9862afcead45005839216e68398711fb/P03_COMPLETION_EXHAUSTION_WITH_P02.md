# P03 COMPLETION / EXHAUSTION ROUND — CONSUME COMPLETED P02 NOW

Continue the SAME merged Orthemology programme and SAME P03 research surface.

This is **NOT a restart**.

The existing checkpoint:

`Orthemology_P03_Engine_Refinement_Checkpoint_attempt-0001.zip`

is accepted as a genuine intermediate advance, but **not as the terminal P03 deliverable**.

Preserve it exactly as predecessor evidence.

Its current statuses are:

- `U03 = PARTIAL`
- `U04 / CV-O = PARTIAL`
- `Q1f = PARTIAL`

I am also supplying the **completed P02 checkpoint/result** from the separate Measure semantics / CV-R / CV-C research thread.

P02 owns:

- `U05`
- `U08`
- `CV-R`
- `CV-C`
- `Q1c`

You must **verify and consume the actual P02 output now**, rather than leaving P03 blocked on a hypothetical future P02 result.

Do not assume that P02 is PASS merely because it is complete as a thread. Read its actual receipts, statuses, theorem statements, countermodels, interfaces, limitations, hashes and evidence boundaries. Reuse only what P02 actually establishes.

The objective of this continuation is:

> **MAXIMISE P03 TO ITS STRONGEST LAWFUL TERMINAL STATE, INCLUDING DISCHARGING EVERY P02-OWNED DEPENDENCY THAT THE COMPLETED P02 CHECKPOINT ACTUALLY SATISFIES.**

Do not redo already established P03 counterexamples, finite tests, proposal diffs, preimages/postimages or source comparisons except where fresh execution is necessary to discharge a remaining acceptance obligation.

---

## 1. FIRST — VALIDATE AND BIND BOTH PREDECESSORS

Before new research:

1. independently verify the P03 attempt-0001 ZIP identity, CRC/integrity, manifest, receipt(s), output hashes and source/evidence bindings;
2. independently verify the supplied completed P02 checkpoint/result in the same way;
3. extract the exact P02 statuses for `U05`, `U08`, `CV-R`, `CV-C`, and `Q1c`;
4. extract every theorem, countermodel, formal statement, interface and limitation that P03 may lawfully reuse;
5. construct an explicit **P02 → P03 dependency map** showing:
   - which P03 claims depend on which exact P02 result;
   - whether that dependency is fully discharged, only conditionally discharged, or still open;
   - the exact source/evidence supporting the disposition.

Do not silently upgrade P03 because P02 exists.

Do not silently weaken P03 because P02 remains partial in some unrelated scope.

---

## 2. U03 — DRIVE PARSER / CHECKER / EXPORT TO A GENERAL RESULT

The first P03 checkpoint already established:

- encoder/decoder depth-domain counterexample;
- structured exporter-refusal counterexample;
- tested bounded repairs;
- ordinary shift/substitution arguments;
- checker/export constructor mappings;
- explicit budget/refusal semantics.

Continue from those results.

Do **not** stop merely at “tested proposal”.

Resolve the remaining U03 gates:

1. state the exact deployed Python/JSON source and target domains;
2. state the refined encoder/decoder relation including all refusal cases;
3. determine whether a total round-trip theorem is false and, if so, replace it with the strongest correct partial/refinement theorem;
4. prove or finitely falsify:
   - accepted-source encode → decoder acceptance;
   - decode/encode correspondence where defined;
   - rejection monotonicity / fail-closed behaviour;
   - constructor preservation;
   - budget/depth preservation;
   - malformed/native-row refusal semantics;
5. completely classify native-input ownership:
   - caller-owned mutable data;
   - copied values;
   - immutable values;
   - host/runtime-originating values;
   - exception-producing host operations;
6. specify and justify host-exception treatment rather than leaving it as an open implementation note;
7. determine the exact status of arbitrary two-item iterable compatibility:
   - required public behaviour,
   - accidental tolerance,
   - or lawful proposed restriction;
8. produce the strongest general refinement/extraction statement actually supported by the implementation.

Where universal claims are false, produce minimal countermodels and reformulate the theorem rather than leaving the obligation merely `PARTIAL`.

The target is:

`U03 = PASS`

if every research-level acceptance condition can be discharged.

Otherwise reduce the remaining blocker to an exact irreducible implementation/external condition.

---

## 3. FORMAL TOOLCHAIN — EXIT 127 IS NOT A TERMINAL RESULT

P03 attempt-0001 reports:

`lean --version` → exit `127`.

Treat that as an execution-environment defect, **not** evidence against the Lean proposal and **not** by itself a sufficient reason to leave Q1f PARTIAL.

Make reasonable attempts to acquire and execute the **exact required Lean 4.19.0 environment**.

Inspect the merged repository, P03 packet, and any relevant P02 formal evidence for the exact:

- `lean-toolchain`;
- Lake version;
- Mathlib/dependency revision;
- project layout;
- required build/audit commands.

You are authorised, within the research workspace, to acquire an isolated exact toolchain through normal reversible mechanisms such as Elan or project-local tooling if available.

Do not modify authoritative GitHub state.

Do not substitute Lean 4.32.2 for a 4.19.0 obligation.

Do not claim `TOOLCHAIN_UNAVAILABLE` until reasonable exact-version acquisition attempts have been executed and recorded.

If the environment fundamentally prevents exact native Lean execution even after those attempts, distinguish:

- `HOST_EXECUTION_BLOCKED`
- `FORMAL_RESULT_UNPROVED`

and prepare a minimal deterministic external formal-execution packet for Codex.

A missing executable must not terminate the mathematical/formal research prematurely.

---

## 4. Q1f — FINISH THE GUARDED REASON / VERSION ANALYSIS

Preserve the checkpoint's negative result:

> edge preservation, including injective edge preservation in the supplied countermodel, does not by itself imply acyclic target structure.

Also preserve:

> this does **not** refute VCT when its declared finite-DAG premise is enforced.

Continue beyond the graph-only proposal.

Explicitly decompose full VCT into its independently necessary layers, including at least:

- graph/DAG structure;
- reason/evidence structure;
- authority/admissibility structure;
- version/currentness structure;
- semantic-preservation structure;
- declared transport/witness conditions.

For each layer:

1. state the exact source condition;
2. state the target condition;
3. determine whether preservation follows from prior layers;
4. provide proof or countermodel;
5. identify whether the layer is independent;
6. identify the smallest sufficient strengthening.

The ranked-DAG encoding must remain explicitly a **proposal** unless proved equivalent to the accepted graph obligation under stated hypotheses.

Do not silently redefine VCT.

If the graph-only Lean candidate can be executed under 4.19.0:

- compile it;
- preserve `.olean` evidence where applicable;
- perform declaration/type readback;
- perform axiom audit;
- record exact toolchain identity.

Then determine whether further VCT layers admit Lean candidates without inventing new accepted mathematics.

Optional TRC prerequisites must remain separate from what Q1f actually requires.

The target is:

`Q1f = PASS`

or an exact decomposition showing the one or more genuinely non-P03 prerequisites that prevent PASS.

---

## 5. U04 / CV-O — COMPLETE THE CONCURRENCY / OPERATIONAL REFINEMENT

The first P03 checkpoint already has:

- complete-state relation proposal;
- `Γ`, issued records, locks and call-local state;
- absence/version/read-set analysis;
- rejection and linearisation obligations;
- deterministic mutation counterexample;
- tested snapshot repair.

Continue with the full non-probabilistic and probability-dependent CV-O obligations.

At minimum investigate:

- linearisation points for every relevant operation;
- validation-before-lock / snapshot-before-lock / lock-held phases;
- read-set stability;
- ABA/version changes;
- rejection histories;
- partial failures and exceptions;
- rollback/no-effect histories;
- concurrent successful histories;
- concurrent rejected histories;
- observational equivalence between implementation histories and abstract histories;
- failure refinement;
- whether complete-state simulation is forward, backward, stuttering, or requires a mixed relation;
- which state components are observationally hidden;
- exact assumptions required for concurrent-history composition.

Use small executable/concolic history exploration where useful, but do not confuse finite testing with universal proof.

If a universal claim fails, supply the counterhistory and strengthen the state relation or theorem.

---

## 6. CONSUME P02 NOW — DISCHARGE THE PROBABILITY / MEASURE DEPENDENCIES

P02 is no longer a future dependency. Its completed checkpoint is supplied in this continuation.

Build an explicit cross-packet table:

| P03 target | Exact P02 prerequisite | P02 actual status/result | Reusable statement/evidence | P03 consequence |
|---|---|---|---|---|

In particular inspect whether and how P02's accepted work on:

- `U05`;
- `U08`;
- `CV-R`;
- `CV-C`;
- `Q1c`;

discharges the probability-extension, measure-semantics, refinement, conditioning, convergence, or finite-probability prerequisites needed by `U04 / CV-O`.

Do not merely cite P02 generally.

Bind each reuse to an exact P02 theorem/result.

If P02 establishes a suitable probability-extension interface, instantiate it in the P03 operational theorem.

If P02 establishes only a conditional theorem, carry its exact premises into P03.

If P02 falsifies or narrows a prerequisite P03 assumed, revise the P03 proposal accordingly rather than preserving an obsolete stronger claim.

If P02 leaves a relevant item genuinely open, reduce the P03 blocker to the exact unresolved P02 statement rather than writing a broad `WAITING_ON_P02`.

The desired result is that no P03 obligation remains PARTIAL merely because P02 had not yet been read.

---

## 7. SEEK A FINAL CV-O THEOREM / REFINEMENT STATEMENT

After consuming P02, attempt to state the strongest lawful CV-O result in a form resembling:

- an abstract operational state relation;
- a concrete implementation state relation;
- admissible history/revision conditions;
- probability/measure assumptions inherited explicitly from P02;
- a simulation/refinement relation;
- success and refusal semantics;
- concurrency/failure conditions;
- observational equivalence or preservation conclusion.

Do not force a single theorem if the mathematically correct result is a family of theorems.

Where appropriate separate:

- sequential refinement;
- concurrent refinement;
- rejection/refusal refinement;
- probability-carrying refinement;
- failure/exception refinement.

The target is:

`U04 / CV-O = PASS`

if all research-level acceptance gates can now be discharged from P03 + verified P02 results.

If not, the remaining blocker must be stated at the smallest irreducible theorem/interface level.

---

## 8. DO NOT CONFUSE RESEARCH COMPLETION WITH REPOSITORY ADOPTION

P03 remains a research/proposal surface.

You are **not** being asked to:

- patch merged `main`;
- reopen the Integration DAG;
- adopt proposals into canonical source;
- release anything;
- claim Codex implementation credit.

A research obligation may reach `PASS` when its required theorem/countermodel/specification/formal evidence has been completed even though Codex has not yet adopted the resulting patch.

Conversely, do not call an obligation PASS merely because a proposed patch's finite tests pass.

The merged integration boundary remains authoritative and must not be mutated.

---

## 9. EXHAUSTION RULE

Do not stop at the first newly exposed ordinary research or formalisation subproblem.

Continue recursively:

`counterexample → refine statement → prove/test → expose next gate`

until one of these is true:

1. the obligation is `PASS`;
2. a genuinely external execution condition cannot be satisfied after reasonable attempts;
3. an exact prerequisite remains unresolved in the **actual supplied P02 result**;
4. completion would require changing an already accepted canonical theorem/concept rather than refining the P03 proposal;
5. a genuinely owner-only / external-evidence boundary is reached.

Ordinary difficulty is not itself a stop condition.

Do not end merely with “future work includes...”.

Perform that work now whenever it belongs to P03 and is supported by the supplied P02 result.

---

## 10. FINAL STATUS DISCIPLINE

For each of:

- `U03`
- `U04 / CV-O`
- `Q1f`

return one of:

- `PASS`
- `PARTIAL — EXACT IRREDUCIBLE BLOCKER: <specific item>`
- `REFUTED / REFORMULATED — <strongest surviving result>`

Do not use broad PARTIAL labels when the remaining issue can be decomposed more precisely.

For any result dependent on P02, state the exact P02 predecessor and whether it is:

- fully discharged;
- conditionally inherited with premises;
- still open.

---

## 11. DELIVERABLE

Produce:

`Orthemology_P03_Engine_Refinement_Checkpoint_attempt-0002.zip`

preserving attempt-0001 as predecessor evidence and binding the supplied completed P02 checkpoint as an explicit external predecessor.

Include at minimum:

- `README.md`
- exact P03 predecessor identity/readback;
- exact P02 predecessor identity/readback;
- `P02_P03_DEPENDENCY_MAP.json`
- exact terminal status for U03;
- exact terminal status for U04/CV-O;
- exact terminal status for Q1f;
- general theorem/specification statements;
- all new countermodels;
- concurrency histories;
- proof notes;
- executable/concolic tests;
- Lean source/results where executable;
- declaration/type/axiom audits where Lean succeeds;
- exact inherited P02 theorem interfaces;
- revised Codex implementation handoff;
- any remaining blockers reduced to irreducible external/dependency items only;
- manifest;
- receipt;
- detached SHA-256;
- independent fresh reopen/readback.

The Codex handoff must explicitly distinguish:

1. research results already established;
2. proposals ready for implementation;
3. formal results actually kernel-checked;
4. implementation steps still requiring Codex;
5. claims that remain open and must not be silently promoted.

**Do not stop simply because attempt-0001 was already sealed.  
Do not stop simply because P02 was produced by another thread.  
Consume the completed P02 evidence, discharge its dependencies, and drive P03 to its strongest lawful terminal state.**
