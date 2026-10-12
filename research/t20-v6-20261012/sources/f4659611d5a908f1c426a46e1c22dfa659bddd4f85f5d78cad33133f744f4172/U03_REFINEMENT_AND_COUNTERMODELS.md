# U03 — parser, finite checker and exporter refinement

**Primary obligation: PARTIAL. Bounded countermodels and three interface-level analyses are complete; whole deployed refinement remains OPEN_RESEARCH.** This is a separate P03 proposal, not an edit of accepted source or a kernel-proof claim.

## 1. Exact obligation, predecessors and status layers

The exact assigned statement is **“Whole deployed parser/checker/exporter refinement”**. The method is to extract the finite checker or prove raw decode / structural validation / substitution / check / serialize refinement, including budgets and rejection paths. The source selector is `items[id=U03]` in `experiments/orthemology-v5/source/ledgers/REMAINING_OBLIGATIONS.json`. The packet records `source_status=OPEN`, `current_status=OPEN_RESEARCH`.

Predecessors are `V4::T09`, `V4::T10`, `V4::V4-R2`; concept `A4C-C055`. T09 concerns renaming, simultaneous substitution and environment correspondence. T10 concerns finite-source semantic translation and proof-carrying checking. V4-R2 concerns actual source-to-Lean certificate export. Exact records, source hashes and later accepted declaration readbacks are in `inputs/OBLIGATION_CONFIRMATIONS.json` and `inputs/ACCEPTED_SCOPED_READBACKS.json`.

Historical catalogue/header phrases such as “uncompiled” remain verbatim evidence. They do **not** revoke the subsequently accepted mapped-native Lean 4.19.0 declarations at the identical preserved source tree. Conversely, those accepted declarations do not prove the Python parser or every exporter call. The immutable original strict-wrapper FAIL is a third, separate status, not a missing-compiler result. No part of this P03 work changes any of those statuses.

The controlling source identities are the seven U03 bindings in the unmodified `OBLIGATIONS.json`, preserved inside the included original ZIP. In particular:

| Source | SHA-256 |
|---|---|
| `reference.py` | `398fdecf3c125f29fbbf7d242327cae0c5044440d58d5d8cdad9297b6e76ea77` |
| `boundaries.py` | `a4382218253e193d7caafa5f164c9aed1d1b0e79754ba0041164383356dc3210` |
| `proof_export.py` | `4971f828be8d21d7d5a20226e166c21e92d361ac1a53afee094f3a34e2364ad3` |
| `lean/FiniteBridge.lean` | `f75306d1a29cd76385058ca1a819910b1f635a63369d807d484ab6db981a0042` |

## 2. Negative evidence accounted for before any proposed completion

Eight generated examples and finite test censuses establish their checked instances, not universal JSON/Python correctness. `FiniteBridge.check` consumes an inductive `Cert`, whereas Python first handles raw bytes, arbitrary native objects, shape validation and bounded construction. Python reduction traces carry data which the exporter erases after validation. Budget refusals, serialisation canonicalisation, unexpected exceptions and the host's mutable objects are not present in the old `Cert → Option Checked` model.

No contradiction in a mapped-native soundness theorem was found. The countermodels below refute explicitly stated **interface extrapolations** one might otherwise use in the missing refinement proof. They are not new diagnoses of the old strict-wrapper failure.

## 3. Countermodel P03-U03-CE01: encoder success outside decoder domain

Property tested:

> For a stable native value x, if `dump_json(x)` returns bytes b, then `load_json(b)` returns the corresponding JSON value.

The unchanged source has the following exact witness:

```python
value = []
for _ in range(100):
    value = [value]

bound_tree(value)      # succeeds: 101 native nodes
raw = dump_json(value) # succeeds: 202 bytes, 101 '[' and 101 ']'
load_json(raw)         # Rejection: resource: JSON depth
```

`bound_tree` counts the root at depth zero and accepts the empty container at native depth 100. The lexical JSON scanner counts open containers from one and rejects the 101st opening bracket. Thus the encoder's successful range is not included in the decoder's domain. This witness is not a well-formed proof certificate; it concerns the shared transport layer, not a false mathematical theorem admitted by the checker.

The proposal keeps the decoder's ceiling at 100 and adds a container-nesting check to the encoder. It does **not** globally lower native depth to 99: a scalar leaf at native depth 100 still fits exactly 100 JSON container levels and must remain supported. This explicitly narrows successful encoder output at the mismatched boundary; it is a proposed interface repair requiring later review, not an invisible policy change. Exact preimage, postimage and unified diff are in `proposal/`.

The test first failed on the original source (`evidence/red-original`, exit 1), then passed on the proposal. Positive controls retain both a scalar at the final native depth and an empty container at the final allowed JSON level.

## 4. Countermodel P03-U03-CE02: malformed exporter rows escape the refusal language

Property tested:

> A finite native input to `proof_export.module` either emits the bounded module text or raises the declared `Rejection`, rather than failing during unchecked tuple unpacking.

The exact source validates the outer list/tuple and count but executes `for name, raw in examples` before validating a row. Consequently:

```python
module([None])                     # TypeError
module([[]])                       # ValueError
module([['name']])                 # ValueError
module([['name', b'{}', 'extra']])   # ValueError
```

These are ordinary deterministic host exceptions, not resource exhaustion. The raw red run records four failing subtests under one test method; the valid-row positive test passes. No emitted certificate is involved, so this again does not refute logical soundness.

The proposed change requires an exact list/tuple row of length two before unpacking. It preserves valid list and tuple rows, name validation, proof checking, duplicate-name refusal and all export budgets. Previously tolerated arbitrary two-item iterables (for example a two-item generator row) would now be refused; this is an explicit proposed native input-domain restriction requiring later review, not an extensional-equivalence claim for every formerly accepted object. It does not purport to make arbitrarily concurrently mutated native module inputs safe: the stable-input ownership hypothesis below remains explicit.

## 5. A precise simulation interface, not a silently strengthened theorem

Use four result classes: `Success(v)`, `Reject(r)`, `FuelExhausted`, and `HostFault(e)`. Do not erase the last three into logical falsity. For a proposed resource-aware abstract machine, rejection is an observable outcome with a reason category and unchanged logical state; it is not a failed `Derives` judgement.

Let J map a supported native value to its JSON value: tuples become lists; dictionary order is forgotten; exact integers, Booleans, strings and null retain their values. J does not preserve object identity or aliasing. Let E_T and E_M map validated finite type/program tuples to `TypeCode` and `Term` constructors. Let E_C map a **validated** certificate to `Cert`: `reduce(p,[t0,…,tn])` becomes n nested `Cert.step` constructors around E_C(p).

The required end-to-end success square is:

```text
raw bytes --strict decoding--> proof data --Python checking--> (term, type)
                                   |                              |
                         validated E_C                     E_M × E_T
                                   |                              |
                                   v                              v
                                  Cert --Lean check d--> Checked projection
```

The right-hand equality must cover **both** term and type. The theorem must be about a successful concrete checking derivation, not merely matching example strings. The export square then connects E_C to emitted Lean syntax and a real, pinned kernel run. Producing that syntax alone does not supply its final edge.

### Explicit hypotheses of the proposed ordinary source comparison

The executed modules are the bound source bytes; built-in Python operations follow their declared semantics; input graphs are finite and remain stable for the duration of native traversal; no malicious monkeypatching, private-state mutation or callbacks replace code; enough host memory/stack is available for operations within the stated resource contract. For concurrency-safe ingress, bytes or an owned validated snapshot must replace that stable-native-input assumption. The current patch only supplies the flat observation snapshot described under U04, not a universal native-object snapshotter.

These are proposed refinement hypotheses, **not** newly added premises in any accepted theorem. The operational semantics of CPython and the JSON library have not been verified in Lean here. That remaining gap is recorded, not hidden behind the induction below.

## 6. Ordinary mathematical bridge for cutoff substitution

Define R(s,c)(n)=n when n<c, and n+s otherwise, for nonnegative s,c. Define `rename` by the exact `FiniteBridge` equations, lifting R under `all` by `liftRen`. The lift equation is

```text
liftRen(R(s,c)) = R(s,c+1).
```

At zero, both sides return zero. At n+1, the test n<c is equivalent to n+1<c+1 and both branches agree. Structural induction on a finite type therefore proves that the mathematical cutoff traversal used by `shift_type` agrees with `rename R(s,c)`, whenever the concrete call succeeds. Input/output budgets only add refusal branches. Negative shifts exposed by the public helper have separate underflow behaviour; the instantiation bridge uses only nonnegative shifts and does not claim a total negative-shift renaming theorem.

For fixed argument A, define the simultaneous substitution at binder depth b:

```text
Sigma_b(n) = var n                         when n < b
           = rename (n ↦ n+b) A           when n = b
           = var (n-1)                    when n > b.
```

`Sigma_0 = singleSub A`. Also `Sigma_(b+1) = upSub Sigma_b`: at zero the result is `var 0`; at n+1, the three cases n<b, n=b and n>b give respectively the retained bound variable, the one-further-shifted argument, and the lowered free variable. The middle case uses the structural renaming-composition law, proved by induction with the corresponding lifted functions.

Induct on the body B. The variable, bottom and arrow cases follow their constructor equations. Under `all`, the concrete traversal raises b to b+1, exactly as `substitute` lifts Sigma_b to `upSub Sigma_b`. Therefore the mathematical traversal yields

```text
E_T(instantiate_type(B,A)) = instantiateType(E_T(B),E_T(A))
```

for successful concrete calls under the stated operational hypotheses. This is an **ordinary source-correspondence argument**, not a new kernel-verified statement. The already accepted `instantiate_sem` can be used only after this bridge and its runtime premises are discharged; it does not itself prove the Python implementation.

### Bounded falsification evidence

An independently structured Python specification uses simultaneous substitutions rather than cutoff traversal. The experiment enumerates all 308 type trees of constructor size at most five over `bottom,var 0,var 1,var 2`; it compares 4,928 shifts and all 94,864 body/argument pairs. A separate application-spine specification compares 3,405 terms of constructor size at most seven with the concrete head-step function. All comparisons pass. The corpus and deterministic generation code are included; the corpus SHA-256 is `376d15bdee09dc1b7765f95cef82c54af992061ea5e9ff7b0a841800277bbf59`.

The explicit capture-sensitivity witness is `B=all(var 1), A=var 0`. Correct instantiation is `all(var 1)`; forgetting the lifted shift gives the different `all(var 0)`. This is a specification-mutation witness, not a mutation or requalification of historical source. Counts supply bounded differential evidence only.

## 7. Checker and exporter correspondence by constructors

| Concrete branch | Abstract correspondence | Remaining boundary |
|---|---|---|
| I/K/S | Same finite term and arrow-type constructors after exact scoped-type validation | Native parsing, finite-tree encoding and budgets |
| application | Induction hypotheses plus exact equality of function domain and argument type | No semantic subtyping or extensional equality is substituted |
| universal introduction | One body certificate checked at d+1; same erased term; `all` type | No infinitary family of supplied premises |
| universal elimination | Polymorphic-type check plus the substitution bridge above | Concrete cutoff/refusal semantics |
| reduction | Exact first term and every adjacent deterministic head step; n steps map to n `Cert.step`s | Invalid traces cannot be erased first and then accepted |
| JSON entry | Exact strict decode then check | Duplicate keys, UTF-8, integers, depth, byte and native-type refusals |
| text export | Fully checked input, restricted identifier, constructor-only emission; separate erasure/type theorems | Actual Lean parsing, elaboration, kernel execution and declaration audit |

An induction over a **successful checking derivation** establishes the mathematical constructor square subject to the explicit runtime hypotheses. It is intentionally one-way. Malformed proof data may have an erasure whose underlying term is derivable; that does not make the malformed concrete input admissible. Likewise abstract acceptance does not entail available concrete resources.

`_head_step` is deterministic weak-head reduction. None means no available weak-head step, not a full-normalisation theorem. `FuelExhausted` is a resource result, not proof of divergence.

## 8. Budget and rejection accounting

The transport layer has 524,288 input/output bytes, native depth 100, 20,000 counted tree nodes, 256-bit integers and 4,096-character strings. The proof traversal also limits height and certificate nodes and charges aggregate returned term/type work. Substitution charges each inserted argument copy **before** allocating it and validates the result. The exporter has its own 512-constructor accounting, one-MiB source cap and 16-example module cap. Its charge for a `reduce` wrapper is conservative relative to the erased Cert tree: the wrapper itself and each retained step are charged. These different budgets must not be identified by assertion.

The reverse transport implication is legitimately false even after CE01 is repaired. Thirty strings of 4,096 copies of “é” fit below the input-byte cap in direct UTF-8, yet ASCII-escaped serialisation exceeds the output cap and is refused. `test_decoder_success_does_not_promise_encoder_budget_success` preserves that refusal. The repair does not weaken output budgeting to manufacture round-trip totality.

The library is not an operating-system allocation or CPU sandbox. Final module assembly and other bounded local objects are not a proof of peak physical memory usage. Resource accounting is to be represented at its actual abstract-machine granularity.

## 9. Result and remaining work

The two transport/export counterexamples are complete at their explicitly stated scopes. The mathematical substitution argument and constructor correspondence are supplied as ordinary arguments with a bounded differential probe. Proposed changes to `boundaries.py` and `proof_export.py` have exact preimages and pass the final regression runs.

U03 remains PARTIAL because there is no mechanised semantics or extraction proof for the deployed parser, no universal host-exception analysis, no proof of native mutable-object ownership for the entire API, and no new pinned kernel execution of arbitrary exported certificates. The later Codex handoff lists these obligations separately from the already-tested source patches. No accepted theorem was weakened to remove them.
