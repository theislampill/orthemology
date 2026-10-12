# U04 / CV-O — complete engine-state refinement proposal

**Primary obligation: PARTIAL.** The complete-state relation, step obligations, a fresh mutation counterexample and a tested proposal are supplied. Neither the deployed engine nor CV-O has acquired a new kernel proof.

## 1. Exact source and predecessor scope

The assigned statement is **“Operational formal model to actual registry/lock implementation”**. Its blocker is that the typed `Plan` model abstracts resource refusal and does not contain the full mutable issuer registry or probability grammar. The method requires a simulation over complete Gamma / issued-record / lock states, with successful concrete transitions, failure atomicity and concurrency linearisation. Canonical status remains `OPEN_RESEARCH`.

Predecessors: `V4::V4-O1`, `V4::V4-O2`, `V4::V4-O3`, `V4::V4-O4`, `V5::CV-O`. Concept predecessors: `A4C-C033,C035,C036,C038,C039,C040,C054`. Aliases `CV-O`, `R-REFINEMENT:registry`, `A4C-O006:implementation` are preserved. Full exact source hashes and source records are in `inputs/OBLIGATION_CONFIRMATIONS.json`; `operational.py` is bound to SHA-256 `3e325d5b4b0ffa71cb3612a88a488a090427695896bc226c1142d8714b09fd99`.

Later accepted mapped-native results govern their exact Lean declarations, including the typed positive OWOU construction and revision results. The old catalogue's “uncompiled” prose is preserved historical metadata, not permission to downgrade accepted mapped-native results. The abstract CV-O mathematical text is not an already supplied universal Lean theorem. `FORMAL_OPEN_ITEMS.json` makes that separation explicit.

The `DEPENDENCY_DAG.json` edge U03→U04 is an **IMPLEMENTATION_INTERFACE** edge. Every claim here using concrete parsing or source proofs is conditional on the U03 bridge. No result from P01/P02/P12 is presumed to have passed.

## 2. Preserved negative evidence

The generic-wrapper construction defeats novelty from the bare positive-operation / negative-SCUU conjunction. The positive scenarios are real, non-reject-all examples, but finite tests do not prove every deployed execution. The old `Plan` schema contains typed functions and finite stamp lists; it has no Python issuer identity, mutable registry, JSON objects, locks, entropy retry or operational exception model. Any relation identifying that entire model literally with the engine would lose essential state.

No stale-licence acceptance after a relevant completed revision was found. The new counterexample below concerns **input capture and committed state validity**, not the existing serialisation of revision versus dispatch check/use.

## 3. Full state and representation relation

Fix source version K for a run. K includes all bound parser, checker, compiler, execution and helper-module bytes. Engineering changes from K to K′ are not Gamma-only revisions; the proposed patches therefore live on a separate surface.

At an API call boundary define the logical state

```text
Gamma = (I, R, V, J, e, P, Q)
```

where I is native issuer identity; R is the rule/stamp map; V maps invariant-observation names to immutable finite natural signatures; J maps ticket strings to issued immutable records; e is the revision-resource counter; P maps probability-model names to frozen source bytes; Q maps ordinary policy keys to a model name and rational threshold. The full concurrent machine additionally contains lock owner / recursion count / waiting threads and per-call program counters, owned inputs, local budgets and temporary compilation values. Lock scheduling is not discarded from the concurrent proof, even though it is not a logical Gamma field.

An issued record is

```text
(source bytes, compiled plan, complete captured bindings, computed probability evidence).
```

A handle is `(ticket, issuer identity)`, not merely ticket text. A compiled plan owns its tag, input/output interfaces, immutable data, child plans, dependency set and node count. Helper datatypes and source-to-compiled correspondence require separate proofs; a frozen outer dataclass alone is not a universal deep-immutability theorem.

The proposed relation R_K between concrete and abstract states requires equality under explicit encodings of **all seven** Gamma components, injective correspondence of live engine identities, ticket-key correspondence, and a well-issued-record invariant. It also relates the active lock owner/recursion bookkeeping and each call's owned input. It does not permit arbitrary caller-created dataclasses to stand for evidence.

### Well-issued-record invariant

For every J[t], there was a successful `admit_json` at fixed K, using that exact frozen source, producing that compiled plan. The captured key set is exactly

```text
D = deps(compiled)
    ∪ {need:k | k is an ordinary compiled dependency}
    ∪ {probobs:name | a present requirement on such k refers to name}.
```

“Ordinary” here excludes schema, vocabulary and `obs:` keys, exactly as the implementation does. Sorted unique D, not a caller assertion, supplies the binding list. Each captured stamp was enabled and equal to the actual stamp at issuance. Probability evidence was computed from the named frozen model and threshold, not accepted as a `pass` field. The record persists unchanged, and no ticket is overwritten or reused within that issuer's lifetime.

`_current` only compares stored bindings. It does **not** recompute coverage. Therefore its correctness depends on this issuance invariant and the trusted-host no-private-mutation condition. Replacing that invariant by “the caller supplied a bindings list” would be unsound.

## 4. Complete reads, absence and fresh keys

`_stamp` gives absent `need:k` the virtual stamp `(0,true)`, while an absent ordinary rule/model key has no stamp. Admission binds the absence of a probability requirement via `need:k`. Adding the requirement materialises `(1,true)`; removing it produces `(2,true)` rather than deleting the version history. Thus returning to the same absent/present semantic condition cannot restore the old stamp.

An invariant `edge` examines **every** active observation. Its dependency set includes both `obs:name` for each present name and the global `vocabulary` key. That vocabulary read covers names which did not exist at admission. Capturing only previously present observation names would not suffice when a new predicate is added.

Setting an observation touches its own stamp and vocabulary; removing it retains a disabled tombstone and advances vocabulary. Revising a probability model advances its stamp even if its numeric law is unchanged. Requirements bind both their `need:` key and the actually referenced model's `probobs:` key.

The revision counter e is a resource boundary, not a replacement for per-key dependencies. An unrelated revision may increase e while leaving a licence current. Registry size may prevent a new admission while an old current operation remains dispatchable.

### Relation to the old total Context

The old Lean model uses `Nat → Stamp` and increments an existing natural version. Python introduces a previously absent ordinary key at version zero. A literal equation of raw version numbers would be wrong. A candidate projection can map absence to `(0,false)` and a present `(v,b)` to `(v+1,b)`, treating virtual `need:` stamps explicitly; alternatively a new resource-aware model can use optional stamps and fresh-key creation directly. Neither definition is silently patched into `OperationalKernel.lean`.

The old dependency list can contain repetitions; concrete bindings are sorted and deduplicated and include extra authority reads. Equality of those raw lists is not the representation relation. A proof must map keys and derive the old required coverage from the stronger concrete invariant, or use the new complete-record model.

## 5. Fresh counterexample P03-U04-CE01

Proposed overbroad property:

> Every successful `set_observation(name,values)` commits a finite natural signature whose actual committed values passed validation, without requiring the caller to keep its list stable.

The unchanged method validates `values` **before** acquiring the engine lock, but constructs `tuple(values)` **after** acquiring it. A deterministic two-thread schedule is:

1. Hold the engine lock as a scheduling device; start the setter on `[0,0]`.
2. Observe via a Python line-trace event that it has passed validation and reached the `with self._lock` line.
3. Mutate only the caller-owned list to `[0,'changed-after-validation']`.
4. Release the lock. The setter succeeds and stores the changed tuple.

The test never writes an engine private field. Access to the lock is used solely to make an otherwise possible wait schedule reproducible. The same waiting interval can arise from another engine call. The committed second component is not an integer and was not checked. The red result and exact test source are sealed.

This does not refute V4-O3's statement that a relevant revision cannot interleave between dispatch validation and use: that lock is still held throughout. It refutes a stronger input-ownership/state-validity claim absent from the simple typed model. A contract expressly restricting native inputs to stable owned values would exclude this schedule; such an extra hypothesis must be stated, not silently presumed.

### Proposal and exact ceiling

The proposed setter first requires an exact list/tuple, captures a bounded tuple of at most 4,097 elements, validates that tuple, and commits the **same immutable tuple**. The cap makes an oversized native list reject without an unbounded copy. Successful validation implies its elements are immutable natural integers within the ordinary tree/integer bound. Caller mutation after capture cannot change what is committed.

This repairs the exhibited flat-signature gap. It is not a general snapshot theorem for nested Python graphs, a promise that the input is captured at method invocation, or a proof of free-threaded CPython internals. Other native APIs must retain an explicit stable-input or owned-byte-snapshot contract. No hostile-host security boundary is claimed.

## 6. Successful-step and refusal obligations by method

| Method | Logical successful change / observation | Linearisation and refusal obligation |
|---|---|---|
| `revise_rule` | Advance named ordinary stamp; update enabled flag; e+1 | Lock held. Validate key and revision cap before update. |
| `set_observation` | Store validated signature; advance vocabulary and obs:name; e+1 | Snapshot proposal above; all rejection checks before first write. |
| `remove_observation` | Remove V entry; advance vocabulary; retain disabled obs stamp; e+1 | Existence/cap checked first; no erasure of stamp history. |
| `set_probability_observation` | Store checked frozen bytes; advance probobs:name; e+1 | Parsing/checking before commit; capacity/cap under lock. |
| refine/coarsen probability observation | Compute appropriate factorisation report; invoke versioned set under re-entrant lock | Model semantics conditional on included checker/ordinary premises; no P02 promotion. |
| add/remove probability requirement | Change Q; advance need:key; e+1 | Existence/rational checks before write; absence stays versioned. |
| `admit_json` / `admit` | Add exactly one fresh immutable issued record and return same-issuer handle | Owned parsed bytes, compile and authority checks before insertion; eight nonce collisions refuse without overwriting. |
| `revalidate` | Use retained old source to perform a new admission | Old currentness is not inherited. Nested RLock preserves atomic engine access. |
| `describe` | Return currentness, source digest and copies of bindings/evidence | No Gamma mutation; observation valid at its locked point only. |
| `dispatch` | Return a detached serialised result; Gamma unchanged | Issuer/issuance/currentness, intermediate checks, execution and output serialisation share one lock. |
| `project` | Return bounded page of currently issued records | No Gamma mutation; page not a durable licence, complete universal enumeration or snapshot across separate calls. |

For each explicit `Rejection` branch, the source-level obligation is that the logical Gamma state at method exit equals that at entry, except that concurrent calls are separately serialised; per-call temporaries and lock acquire/release are internal steps. The table concerns a call's linearised interval, not a comparison that forbids other completed calls from changing Gamma.

Inspection places the ordinary validation/resource rejections before the first mutating assignment in the mutators. `admit_json` makes insertion only after compilation, complete binding and uniqueness success. `dispatch` mutates no Gamma field. Coarsening computes its refinement report before setting the new model; adding a report label afterwards is a local operation, not a registered policy mutation.

This is an ordinary source-order argument, not a proof against every Python exception. Memory allocation failure, process termination, asynchronous interruption or an unexpected host exception between several assignments can leave a partially updated state. Strong crash/OOM atomicity is **not established** and is outside the stated operating-system-sandbox contract. A stronger target would require a separately reviewed transactional-state representation or rollback design; it cannot be obtained by calling all failures `Rejection`.

## 7. Currentness under revision: precise ordinary argument

Let a handle actually be issued in Gamma_0 with full captured set D and enabled stamps b_k. Suppose its issuer and issued record persist; the same K executes all steps; revisions only advance touched versions strictly, retaining tombstones/virtual-absence history; no private mutation, reset or rollback occurs. Let T_i be exactly the stamp keys changed by revision i.

Then

```text
current(Gamma_n, handle)
  iff for every k in D, stamp_n(k) = b_k
  iff D ∩ (T_1 ∪ ... ∪ T_n) = ∅.
```

The first equivalence expands `_item` plus the issued-record invariant and `_current`; captured enabledness was true at issuance. If no captured key is touched, induction over revisions preserves every stamp. If a captured key is touched, its first change strictly raises its version and every later change preserves or further raises that version. The original version cannot reappear. This proves the converse and the ABA exclusion. Persistence of issuer/record and complete reads are indispensable premises; code reset, deletion or context recreation cannot be ignored.

This is the existing CV-O transport architecture specialised to the actual stamp conventions, not a new foundational theorem. The current tests of complete state include exact `need:` absence bindings, additions/removals, observation deltas and record persistence; they do not establish the universal induction in a kernel.

## 8. Concrete execution versus typed Plan

For the shared deterministic structural/primitive fragment, map supported interface values to their mathematical types, bounded naturals into Nat, Booleans literally, and products componentwise. On **successful** concrete execution, induction over compiled plans gives the same value as mathematical `evaluate`: identity, copy, projections and primitives follow their definitions; composition uses the two induction hypotheses and checked intermediate interface equality; parallel uses them on each component.

A concrete successor at `2^256-1` may reject, while the total typed Plan returns `2^256`. Thus no biconditional equating concrete success with `execute` is asserted. A new resource-aware specification must admit explicit refusal observations without falsifying the old total theorem.

The core case additionally requires U03: an actual checked source arrow and an input proof produce the checked application with the same term and type. Selectors need their certified projection correspondence. Invariant edges need complete validated observations. Samplers and productive observers need their own finite helper contracts and declared probability/stream semantics. They are not all literal constructors of the old Plan model. Any extension of that model is a **new definition proposal**, not a retrospective theorem in its namespace.

The same RLock is held from dispatch authority validation through result construction. Under ordinary locking semantics, a relevant revision cannot take effect inside that interval. A dispatch ordered before the revision may succeed; a later call after the revision completes cannot use its now-mismatched captured stamp. This gives a source-level linearisation argument for the relevant shared state. It does not yield distributed leases, host durability or world authority.

## 9. Executed evidence and disposition

The final proposal passes the supplied 183 test methods in normal and optimised Python, plus sixteen new methods in each mode. Five of the twelve new contract methods exercise observation snapshots, full logical-state equality on fourteen explicit rejection branches, exact absence/requirement deltas, observation/ticket persistence and detached outputs. The test harness's state snapshots cover all seven logical Gamma components; lock ownership is checked at the quiescent boundary in the rejection test. This is finite evidence on the recorded CPython 3.13.5 environment.

U04 remains PARTIAL. Outstanding work is a mechanised complete-state operational model, a proof of its representation relation and input capture, every explicit refusal branch, helper-module correspondences, and a full concurrent history proof. An optional stronger crash-atomicity requirement must be separately specified. No owner policy, new proof premise or application semantics has been adopted here.
