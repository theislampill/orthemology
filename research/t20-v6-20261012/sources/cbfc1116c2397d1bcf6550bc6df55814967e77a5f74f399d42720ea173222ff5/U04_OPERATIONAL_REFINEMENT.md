# U04 / CV-O — complete-state, concurrent, refusal and failure refinement

## Disposition

**REFUTED / REFORMULATED — unconditional failure-atomic refinement of the deployed mutable registry is false under host exceptions. A resource-aware sequential/concurrent refinement survives under explicit no-interrupted-write conditions; the separate owned-ingress/copy-on-write proposal removes that condition for precommit faults. Postcommit response loss is a committed/pending outcome, never unconditional rollback.**

This is an ordinary source-level proof and counterhistory result, not a verified Python interpreter or a new kernel proof of the full registry. The inherited U04/CV-O record and V4-O1–O4/CV-O predecessors remain unchanged. The existing mapped `OperationalKernel.Plan` theorem is not silently extended to mutable records, arbitrary probabilities or new operation constructors.

The exact source and proposal identities are in `inputs/SOURCE_BINDINGS.json` and `proposal/PATCH_AND_STATEMENT_MAP.json`. Attempt1's mutation counterexample and snapshot patch are preserved in its ZIP. The new tests are not another replay of the old acceptance censuses.

## 1. Abstract state and observations

Let an abstract committed state be

    A = (issuer, rules, observations, probability_models,
         probability_requirements, issued, epoch).

`rules` is a finite map to `(natural version, enabled)`; observations are finite natural-number tuples; probability models are canonical immutable byte specifications; requirements map operation-rule names to `(model name, rational tolerance)`. Each issued record contains immutable canonical candidate bytes, a finite checked operation tree, its exact dependency/stamp vector and canonical probability evidence. The issuer is a process-local identity, not a cryptographic assertion about a remote principal. `issued` is an insertion-ordered finite map: insertion order matters to paginated `project`, so it is not erased from the abstraction.

An abstract handle is `(issuer identity, fresh ticket)`. The permitted ticket alphabet consists of 48-character lowercase hexadecimal strings returned by the declared entropy primitive. Freshness is checked against **all** prior issued records, including stale ones. A bounded sequence of eight colliding entropy results causes refusal; there is no probabilistic premise that collisions never occur.

Define the completed operation alphabet by the fourteen public methods of the new adapter: rule revision; finite observation set/remove; probability model set/refine/coarsen; requirement set/remove; admission from native or bytes; revalidation; description; dispatch; projection. Native admission and byte admission share one logical issuance rule but have different ingress phases. The constructor is trusted host initialisation, not an untrusted candidate instruction.

The abstract transition rules are mathematical operations on these finite maps, not calls back into the concrete implementation:

* A revision validates its request and bounds, changes the named finite map and the specified stamps, and increases `epoch` by one. An absent requirement reads stamp `(0,true)`; absent ordinary dependencies read `None`. Removal retains the version tombstone.
* Admission parses a finite operation derivation, checks every required enabled stamp and probability condition in the current state, then either refuses without changing the registry or appends a fresh immutable record and returns its handle. Revalidation uses the old record's source only; it performs a new admission against the current state and produces a new record/handle.
* Dispatch checks issuer membership, exact stamp equality and input membership, then follows the finite operation semantics below, including all intermediate and output resource/type guards. It returns a fresh JSON value and makes no logical registry change.
* Description and projection produce the stated copies of metadata, currentness and insertion-ordered pages. They confer no authority beyond the same current-state predicates.

Observable histories include invocation, **captured request**, successful/refused response, and a host-fault/no-response phase when visible. The captured-request coordinate is necessary for mutable native inputs: a bounded deep copy can observe a hybrid of concurrent caller updates. It does not promise the value at the invocation instant. Clients requiring that promise must provide immutable bytes or a cooperatively locked/frozen graph.

Physical heap addresses other than issuer identity, lock ownership, private workspaces, interpreter frames, entropy consumption and wall-clock time are hidden from the logical registry observation. Entropy and allocation are nevertheless real external effects and are not described as rolled back.

## 2. Concrete relation and invariants

For the ordinary deployed engine, the relation maps its five private mutable maps, `_epoch` and `_issuer` to A by the value interpretation above. For `AtomicEngine`, A is the image of **only** the currently published `_engine` pointer. A provisional engine may differ and is deliberately excluded from committed A.

The full machine additionally contains the shared reentrant mutex, the public-transaction-active flag, pending calls with owned arguments, private map copies, local resource counters and response objects. A call may be in `capture`, `waiting`, `private`, `published`, `responded` or `aborted` phase. These components are not omitted from the simulation; they are related to pending abstract invocations and stuttering steps.

The inductive invariants are:

1. The published five maps have no mutable aliases exposed by the supported API. Map values are recursively immutable: stamps/observations/requirements are tuples; model/source/evidence bytes are immutable; checked operation/sampler records are frozen records whose payloads are tuples, bytes, integers, fractions or other such records. Host reflection that writes frozen/private fields is excluded by H.
2. Every issued record has a successful derivation at its issuance state and binds the complete recorded read set. Issued records remain present and immutable thereafter, even when not current. Issuer identity remains unchanged across private copies.
3. Versions never decrease or reset at a key; tombstones and virtual absence stamps prevent ABA. The finite revision cap is 10,000, not modular arithmetic. A failed proposed transaction leaves both content and versions unchanged.
4. All code that can inspect or publish committed state uses the same mutex. A new public transaction during same-thread reentry is refused; internal calls of the base engine continue within the same private transaction and reentrant lock.
5. No provisional state or returned mutable value aliases a map of a previous or next committed state. The only publication is the `_engine = private` reference store after the result object has been constructed.

Initial construction establishes these invariants. Map copying preserves all immutable values and insertion order. The branch analysis below preserves them at every normal publication. Failure before publication cannot break them because the only modified maps belong to an unpublished object.

## 3. Successful operation semantics: all compiled tags

Use the independently specified finite interfaces: bounded natural numbers; booleans; unit; binary products; finite indices; bounded literal bit arrays; checked source-proof values; and a tagged `Pending`/`Done` sampler output. This is an explicit extension of the ordinary finite operational model, not a claim that all constructors already occur in the old Lean `Plan`.

| Concrete tag | Abstract successful meaning and proof obligation |
|---|---|
| `primitive` | `succ(n)=n+1`, `iszero(n)=(n=0)`, Boolean negation. Literal type tests prevent Python's Bool-as-Int identification. Output membership is checked, so the maximum 256-bit natural may be refused by `succ`. |
| `id`, `copy` | Identity and diagonal of the declared finite interface. Returned sharing is later erased into owned JSON copies; semantic values, not object identity, are preserved. |
| `first`, `second` | Product projection, only after exact input-interface membership. |
| `compose` | Domain/codomain equality is checked at admission. Evaluate first, validate its result, then evaluate second. A later projection cannot hide an invalid intermediate. Induction on the two operation trees proves the value equation. |
| `parallel` | Evaluate each child on its declared coordinate and form the pair, retaining both child read sets and resource charges. |
| `core` | Admission checks a source certificate of arrow type A→B. A runtime input is itself a checked proof of A. The returned certificate is the application of those two proofs. U03's successful checker correspondence supplies its term/type meaning. No untyped host function is called. |
| `selector` | A marker-free checked polymorphic selector has an exact weak-head trace from application to two fresh markers to one marker. Substitute arbitrary values for the two fresh markers in every trace term: each head-step equation commutes with that substitution until the terminal marker. Thus the selected projection is sound; the stored overhead is trace length, not a general cost theorem. |
| `observer` | Admission validates a finite nonhalting control invariant for the declared binary-tape source. Every control state in that invariant has both possible symbol successors inside it and nonhalting. Induction on source steps gives nonhalting from the initial state; the observer's defined prefixes are all zero. This is a strong sufficient certificate, not a decision procedure for arbitrary observers or P02's distinct finite-Mealy hitting algorithm. |
| `sampler` | Both leaf proofs are checked at the same type. The integer cell update `(k,d)→(2k+b,2d)` represents the next dyadic cylinder. For q(x)=x²+2x−1, q is strictly increasing on [0,1]; endpoint signs decide whether a cell lies entirely below or above its unique root. A `Done` value contains the corresponding checked leaf; an unsettled prefix is `Pending`, not a returned program. |
| `sampler_budgeted` | The guarded finite-cap machine uses the same cell equations and leaf checks. The declared residual calculation is checked before admission. Its probability interpretation is conditional on the specified fair-bit law, not produced by a dispatch that merely receives a caller's bits. |
| `edge` | The operation maps source s to target t and fixes all other finite indices. Admission checks every active observation has the carrier size and equal values at s,t. Thus the edge preserves every currently bound observation. The vocabulary stamp additionally detects newly introduced observations. |

For the sampler arithmetic, induction gives `0≤k<d=2^n`. The irrational root cannot equal a dyadic boundary: a rational root of the monic polynomial would be an integer, and neither endpoint is a root. Therefore exactly one dyadic cell contains it at each depth, all other cells are decided, and under independent fair bits that residual cylinder has mass `2^-n`. This is a scoped ordinary interpretation of the existing finite sampler branch, not P04's general sampler extraction/cost work or an empirical random-source assertion.

The compile recursion checks exact fields, operation height≤60, at most 1,000 visited operation constructors and aggregate type work. Each constructed dependency set includes its own rule and every child's dependencies. An induction over successful compilation followed by successful execution establishes both interface membership and the equations in the table. Each local work/type check adds a refusal branch; it does not change a returned value's mathematical meaning. The execution work budget is 200,000 structural visits, distinct from transport/export bounds.

## 4. Complete reads, absence, revisions and ABA

At admission the read set is obtained from the compiled tree, not a caller's declared list. It always contains `schema`. Structural, primitive and wrapper nodes add their rule keys. Edge compilation additionally reads `vocabulary` and every current `obs:name`; the dependency closure includes those keys even when the edge happens to be an identity.

For each eligible operation-rule dependency, admission binds `need:<rule>` **even when no probability requirement exists**. If a requirement exists, it binds the required probability model's `probobs:<name>` stamp and computes the exact model certificate. Multiple references to one rule/model are not different authorities; the set of keys is deduplicated and the evidence is stored immutably.

For any unchanged dependency set K and states A,A′ with identical stamps at K, `Current(A,record)` iff `Current(A′,record)`. This follows componentwise from exact equality and enabled bits, not from the coarse epoch number. Conversely, changing a bound key's stamp invalidates that record; a subsequent re-enable at a larger version cannot restore equality. Requiring a formerly absent model changes virtual need stamp 0 to 1; removing/readding changes it again. Finite observation removal retains its own stamp and changes `vocabulary`; reintroduction cannot reuse a former version. Probability coarsening may make the semantic tolerance easier but still changes the version, so it cannot revive old authority.

Read stability is guaranteed only within the same lock-held transaction. Canonical bytes checked before locking are independent of registry state. Any model/refinement comparison using current Gamma occurs under the lock. Caller-owned native structures are copied before that interval and never become a competing registry writer.

## 5. Phase, linearisation and refusal table

All mutation entries in the proposed adapter linearise at its **single reference publication**, after the base method's private effect and result construction. An unchanged private copy published by a read-only operation is a stutter; choose the successful lock-held observation point for that read. Calls that fail before publication have no registry step.

| Public entry | Pre-lock or private validation | State read/effect | Refusal/no-effect point |
|---|---|---|---|
| `revise_rule` | Exact immutable key/Bool; reserved names; revision cap | Update one stamp and epoch | Any failed guard before publication |
| `set_observation` | Owned bounded integer tuple; name/size | Observation plus vocabulary/name stamps, epoch | Bad values, vocabulary/cap failure, or private host exception |
| `remove_observation` | Exact string | Delete existing observation; retain/increase stamps | Missing name/cap refusal |
| `set_probability_observation` | Owned spec, strict encode/decode and exact model check | Store bytes; model stamp; epoch | Invalid/rational/resource/model refusal |
| `refine_probability_observation` | Owned fine spec; lock-held old/new comparison | Store checked finer model with one revision; return report | Missing model/factorisation/budget refusal |
| `coarsen_probability_observation` | Owned coarse spec; reversed lock-held comparison | Store checked coarser model; return directional report | Same; report allocation failures remain private |
| `require_probability` | Exact rule/model names; owned rational pair | Requirement plus need stamp and epoch | Unknown rule/model, malformed epsilon, revision cap |
| `remove_probability_requirement` | Exact rule name | Delete requirement; need stamp and epoch | Missing requirement/cap refusal |
| `admit` | Own/canonicalise native candidate | Same as byte admission | Capture/transport failure before lock |
| `admit_json` | Immutable raw bytes; fresh parse and canonical source | Compile, certify, bind, bounded fresh-ticket search, append record | Grammar/disabled/epsilon/cap/collision/host failure |
| `revalidate` | Opaque exact handle | Locate old immutable source; perform new admission within same transaction | Bad handle or any new-admission refusal |
| `describe` | Exact issuer-bound handle | Currentness, source digest and copied evidence | Invalid/unissued handle; host fault before response |
| `dispatch` | Owned input; opaque handle | Currentness, input check, pure finite evaluation, copied output | Stale/typing/work/output/host refusal; no logical writes |
| `project` | Exact bounded pagination | Copy insertion-ordered current-record page | Pagination/resource/host failure |

The table contains all fourteen public methods, counting `admit` and `admit_json` separately. Construction is a separate initialisation event. No supported state-reading or state-changing method is omitted by the phase proof.

## 6. Newly executed counterhistories and their exact scope

### CE-HOST-REVISION — partial contents with unchanged version

In the exact attempt1 engine, start with observation `[0,0]` and a current admitted edge 0→1. During `set_observation('v',[0,1])`, inject a synchronous `MemoryError` after `_observations` has changed but before the version-loop executes. The method fails with unchanged dependency versions. Dispatch through the old handle returns 1, which violates the now-stored observation. The raw test observes the stale-admission hazard. The proof is a concrete instruction-prefix counterhistory, not a claim that all normal locked revisions fail.

### CE-HOST-ISSUANCE — failure after record insertion

Admission inserts an `Issued` record before constructing the returned `Licence`. A host exception at the latter statement leaves the new record in the registry. An abstract model treating **every failed call** as a no-effect step is false even without another thread. It could instead include a committed/pending issuance, but cannot both hide the append from later `project` and claim rollback.

### CE-REENTRY — rejected first proposal

The first private-copy adapter allowed same-thread public reentry while an outer private copy was pending. A nested rule revision could publish successfully and then be overwritten by the outer copy. The two completed independent revisions had no serial explanation. The rejected source preimage and RED test remain in the packet. The repaired `_active` guard refuses a new public transaction until the outer one leaves; base-engine nested calls still share the private state and do not fork another transaction.

### CE-POSTCOMMIT — cancellation is not rollback

Inject `KeyboardInterrupt` immediately after reference publication and before delivery of the result. The revision is committed even though no normal response reaches the caller. This is not repaired by copying: any real commit must have a boundary after which a response can be lost. Treat the operation as committed/pending, include an indeterminate observation, or add a separately designed durable idempotent protocol. This packet does not invent such a protocol or claim process-crash persistence.

## 7. Ordinary theorem family and proofs

### CV-O-A2-SEQ — sequential successful-step refinement

Assume H, a related initial state, immutable/owned request meaning, the bound source bytes, and a normally completed method whose outcome is not a host interruption between writes. Then each successful deployed method matches exactly one abstract finite transition, and each ordinary rejection matches a refusal with unchanged logical registry state where the source has not yet written.

Proof: parse and native-capture correspondence is U03. For admission, structural induction gives the checked tree and complete dependency set; the loop adds need-absence and model dependencies and stores their exact current stamps; fresh-ticket membership prevents overwrite. The revision branches perform exactly the listed finite updates. Dispatch uses the invariant's checked tree and lock-stable current bindings, so the operation-table induction supplies the result; copying only erases aliases. Read-only methods merely compute the stated views. The instruction order in the counterhistories proves why arbitrary host failures cannot be added to this theorem unchanged.

### CV-O-A2-ATOMIC — proposed precommit failure refinement

Assume H's all-or-none ordinary reference-store semantics, supported API access only, and the proposed adapter invariants. A prepublication exception/refusal has no committed registry effect, regardless of how many provisional map writes occurred. A successful publication yields precisely the abstract transition established by CV-O-A2-SEQ.

Proof: under the mutex, `_fork` obtains private copies of every mutable map. The only shared reachable values are immutable; issuer identity is intentionally shared. No base method has a reference back to an older map and no provisional result is returned early. Thus every provisional write and exception changes only hidden call-local state. The sole store changes the entire related committed state at once; before it A is old, after it A is the completed next state. Internal nested calls remain on the same private engine. Public reentry is rejected, excluding the lost-update counterhistory. `finally` clears the busy flag; repeated asynchronous interruption can impair progress but does not create an accepted stale transition.

### CV-O-A2-CONCURRENT — forward stuttering simulation and linearisation

Under the same hypotheses, every finite concrete concurrent history of the proposed adapter has a resource-aware abstract history with the same completed observations after projecting hidden implementation steps. Order successful mutating operations by publication, read-only successes by their lock-held observation, ordinary rejections by their failing check, and handle postpublication no-response calls as committed pending operations.

Proof: capture/wait/private steps stutter on A. The shared mutex and reentry guard ensure at most one public state transaction can publish from a given committed interval; each next transaction forks the most recently published state. CV-O-A2-ATOMIC handles each publication and prepublication failure. The chosen points lie within their calls; hence nonoverlapping calls preserve real-time precedence. Induction on the finite instruction history constructs the abstract sequence. Pending calls without publication can be omitted; pending calls with a publication are completed abstractly when needed to explain later observations. No fairness, bounded response time or termination under unending cancellation is inferred.

This is **forward stuttering refinement / trace inclusion**, not a backward simulation or unconditional bisimulation against the old ideal `Plan`. A mathematical natural-number successor may be ideal-total while the concrete bounded successor refuses; resource exhaustion, failed entropy and stale versions also add outcomes. Conversely, for a fixed admissible input/entropy/fault/scheduler transcript satisfying the abstract machine's matching concrete work rules, the constructed replay has exactly the same observations. That equality is a coupled-history statement, not equality between every arbitrary nondeterministic abstract behavior and a concrete run.

### CV-O-A2-FAIL — complete failure split

Structured syntax/type/policy/resource rejection before publication is a no-effect logical refusal. A synchronous host failure before publication is a no-effect **host failure**, not logical invalidity. A postpublication exception or lost reply is an indeterminate committed call, not a refusal rolled back. Lock-acquisition/capture failure is prepublication. Entropy/CPU/memory consumption are not logical registry coordinates and need not be restored. Process death, storage durability, arbitrary private-state mutation and hostile interpreter replacement are outside H, rather than silently modelled as successful rollback.

This partition resolves failure refinement without assuming host exceptions never occur. Full transparent retry would require a new external or durable idempotence contract, not another ordinary proof about this in-memory adapter.

## 8. Probability-carrying refinement after consuming P02

`P02_OPERATIONAL_INSTANTIATION.md` proves the exact declared finite/interval measure interpretation, fibre defect, threshold and finite debt formulas, then the probability-lifting theorem under an explicit joint environment law. P02's U05 M01/M03/M04, CV-R R02/R07 and Q1c's section-2 finite probability interface are reused at ordinary scope. No new P02 kernel declaration exists or is imported.

P02 U08 fixed-point/sampler gaps, its general PR-codec gap, its T300 parity example and P12's optional TRC application are not prerequisites of the deployed finite operational transition theorem. The infinite-history extension retains J and measurable-history hypotheses; it is never derived by dropping the residual from finite engine tests.

## 9. Executed scope and terminal boundary

The new suite includes 4,680 bounded serial histories with 18,056 checked transitions, 534 injected line-prefix fault points and six forced actual-thread schedules, plus the unit regressions and probability instantiations. These finite checks are differential/falsification evidence for the proposed code. The universal claims above are ordinary proofs over explicit H and the finite algorithms; no count is described as a kernel proof.

The false unconditional deployed-failure claim is terminally refuted. The revised theorem family is supplied in full at ordinary research scope, with exact counterhistories and a separate implementation proposal. Native full-stack mechanisation and deployment adoption remain separate effects; current mathematical conclusions are not waiting for an unread P02 packet.
