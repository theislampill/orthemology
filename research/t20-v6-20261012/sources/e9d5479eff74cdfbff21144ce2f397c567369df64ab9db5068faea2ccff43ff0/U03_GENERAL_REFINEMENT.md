# U03 — general partial/refusal refinement, with owned ingress

## Disposition and exact object of the result

**REFUTED / REFORMULATED — total native/JSON round-trip and unconditional borrowed-input refinement are false. The strongest surviving result is an ordinary, resource-aware partial refinement for exact byte inputs and owned/stable native values, with explicit host outcomes.** It is not an extraction or kernel proof of CPython, JSON, or arbitrary generated Lean text.

The exact U03 record, predecessor IDs, source hashes and original criteria are retained in `inputs/P03_OBLIGATION_CONFIRMATIONS.json`; the entire original packet and attempt1 remain inside the unchanged predecessor ZIP. U03 still denotes the original whole deployed parser/checker/exporter research obligation. This disposition is a new research result, not a canonical ledger edit or a relabelling of an accepted theorem.

Attempt1 already supplies the depth counterexample, malformed-row counterexample, ordinary shift/substitution argument, constructor mapping and their finite evidence. Those are premises of this continuation, not newly counted experiments. In particular the 4,928/94,864/3,405 comparison populations were not regenerated.

New source proposals are separately named `proposal/safe_frontend.py` and the ingress of `proposal/atomic_engine.py`. Existing canonical APIs are not overwritten. The three attempt1 patch pre/postimages remain exact predecessor evidence.

## 1. Concrete domains, not “all JSON” or “all Python values”

Let N be finite acyclic graphs of **exact** Python builtin values: `dict` with exact string keys, `list`, `tuple`, exact `str`, exact `int`, exact `bool`, and `None`. Subclasses, floats, bytes nested as values, arbitrary iterables, dataclasses, fractions at the ordinary JSON interface, custom protocols and foreign objects are outside N. Repeated aliases are permitted but each traversal occurrence is charged separately. Object identity, aliasing and dictionary insertion order are not semantic coordinates of JSON.

The supplied structural contract counts the root at depth 0, all container/value nodes and dictionary keys, with at most 20,000 visits, depth 100, 256-bit integer magnitude and 4,096-character nonsurrogate strings. Container length must not exceed the node limit. The separate JSON lexical depth counts containers beginning with depth 1. These are different counters; attempt1's empty-container chain shows why both are needed.

Let J erase Python presentation: tuples and lists become JSON arrays, dictionary key order is forgotten, and primitive values keep their exact values. J neither preserves sharing nor establishes a single-instant snapshot of a concurrently mutated object.

Let B be exact immutable `bytes`, at most 524,288 bytes, whose strict UTF-8 decode is valid JSON with unique object keys, no floats/exponent notation/non-finite constants, integral lexemes of at most 78 digits and magnitude at most 256 bits, lexical container depth at most 100, and whose parsed value satisfies the structural contract. JSON whitespace and escape alternatives are allowed; byte identity is not required. An exact `bytes` subclass, `str`, `bytearray` or `memoryview` is refused by `load_json` rather than coerced.

For a stable x, define E(x) as canonical compact sorted-key ASCII-escaped JSON, **only if** the structural and lexical-depth guards and output byte limit all hold and the host successfully completes the primitive operations. The extra output-domain condition is substantive: a decoded direct-UTF-8 value may require too many ASCII-escaped output bytes. The preserved attempt1 reverse-direction witness remains binding.

B and N do not assert that every syntactically valid JSON document is a valid certificate. Certificate D is a further exact grammar: seven rules (`i`, `k`, `s`, `app`, `all_i`, `all_e`, `reduce`), exact field sets, scoped finite type trees, finite terms and checked reduction traces. A successful parse without a successful checker is not a proof.

## 2. Host semantics and result algebra

The ordinary argument uses a small explicit host contract H, not a claim that H was verified in Lean:

1. Exact builtin integer/string/container, UTF-8, JSON and hashing primitives have their specified mathematical behavior when they return normally. The selected source bytes, functions and constants are not monkeypatched by the input.
2. Immutable bytes and validated immutable leaves do not change during use. A borrowed native-tree theorem additionally requires stability for that traversal; the owned adapter replaces this with an explicit capture transcript.
3. Memory/stack/entropy/runtime operations may fail. Such events are observable `HostFault`/`Abort` outcomes, not proofs of invalidity. Resource bounds in this program are logical work/data bounds, not an operating-system CPU/heap sandbox.
4. No external actor mutates private registry state or forges supposedly immutable internal dataclass fields with host reflection. Such host compromise is outside the admission-byte threat model.

Use outcomes `Success(v)`, `Refusal(category)`, `FuelExhausted`, `HostFault(exception, phase)` and `AbortOrNoResponse(phase)`. An internal invariant failure is a refusal/error report, never permission to accept a false certificate. Exception classes alone do not prove rollback for an effectful method: U04 distinguishes precommit from postcommit histories.

### Complete treatment of exception-producing boundaries

| Operation class | Existing behavior / proposed interpretation |
|---|---|
| UTF-8 and JSON grammar | Unicode failures, JSON parse/value failures, duplicate keys and forbidden numeric tokens become `Rejection`; strict bytes and size guards precede parsing. |
| Structural validation and reference checking | Declared grammar, scope, trace and numeric/work limits produce `Rejection`; normalisation fuel exhaustion is the distinct `FuelExhausted`. A caller-supplied `work` list is intentionally decremented, including on refusal. It is not covered by an “all native state unchanged” assertion. |
| Legacy row unpacking | Malformed/custom rows may raise `TypeError`, `ValueError`, arbitrary user iterator exceptions, or diverge. No total legacy-iterator theorem is asserted. |
| Owned native capture | Exact-type inspection occurs before protocol use. Captured lists use builtin indexed reads with a fixed initial length; dictionaries use builtin item traversal. Shrink/iteration invalidation yields a structured unstable-capture refusal. Recursion exhaustion is a resource refusal. `MemoryError` and asynchronous exceptions propagate; no engine state has been accessed. |
| Canonical encoding | The existing encoder translates its documented value/type/recursion failures into rejection. Allocation failure, final byte joining and other host failures may escape. The owned adapter does not fabricate a success in any such branch. |
| Hashing, regular expressions, exact rationals, locks, allocation and entropy | Successful primitives obey H; otherwise record the actual host outcome. Entropy consumption, CPU time and allocation are not rolled back by a logical registry transaction. `KeyboardInterrupt`/`SystemExit` are not swallowed as invalid-proof decisions. |
| Internal helper parameters | Native `nodes`, `depth`, `work`, fuel and helper metadata are not all untrusted-JSON-addressable. The natural-budget theorem requires natural limits and an owned integer work cell. Nonconforming direct host calls may raise or exhibit behavior outside that helper theorem; they are not promoted into the byte API domain. |

This classifies host exceptions rather than leaving a blanket “exception handling later” requirement. H remains an explicit external VM contract; no finite Python execution establishes H universally.

## 3. General transport theorems and proofs

### U03-A2-T1 — stable accepted encode implies decode, preserving J

For stable x in N, under successful H primitives and all E guards, `load_json(dump_json_attempt1(x)) = J(x)`. For `encode_owned`, successful return itself additionally executes `load_json` on the immutable returned bytes before exposing them; hence successful return always belongs to B under H.

Proof for the value equation: structural induction on the finite traversal tree. Scalars are represented by the matching JSON literal or escaped string; exact integer and nonsurrogate/string bounds ensure the parser's corresponding scalar guards. Boolean exact-type handling prevents its interpretation as an integer index. Arrays preserve order and recursively encoded elements. Objects contain unique exact string keys; sorted emission changes only order, and the duplicate-key hook reconstructs the same map. The native and lexical depth counters and all node/string/numeric limits remain checked, not inferred from byte length. Chunk accumulation either refuses before returning over-budget bytes or returns the exact concatenation. Parsing the complete returned bytes follows the same constructor decomposition, yielding J(x). The extra final decode in the owned adapter is a checked postcondition, not the sole proof of value preservation.

For a mutable x, let `Capture(x,c)` mean the actual finite sequence of exact builtin reads produced the fresh value c. The general owned theorem is instead:

    encode_owned(x)=Success(b) implies
      there exists c, Capture(x,c) and D(b)=J(c).

It does **not** assert c=x at invocation or at one common instant. The new mutation countermodel changes an input integer to a float after validation but before the predecessor encoder begins. The predecessor returns bytes its decoder refuses. Owned capture prevents the original borrowed object from being accessed by the encoder; this is a strictly stronger ingress guarantee with an explicitly different ownership boundary.

### U03-A2-T2 — strongest reverse relation

For b in B, D(b) is owned data. Encoding that value may still refuse due to canonical output length or host failure. Wherever the encoding is defined:

    D(E(D(b))) = D(b),
    E(D(E(D(b)))) = E(D(b)).

Proof: D(b) is structurally valid, contains no cycles or caller aliases, and scalar decode followed by encode preserves each value. Apply T1. Canonical key ordering/escaping and fixed separators make the second normal form unique, giving idempotence. Byte equality b=E(D(b)) holds only when b already has that canonical representation. Total two-sided round-trip is therefore false, not unfinished research.

### U03-A2-T3 — resource monotonicity, at its exact direction

Fix a stable traversal/derivation, successful host primitives and the same semantic grammar. In the mathematical resource-parameterised machine, componentwise larger natural budgets cannot turn that success into a semantic rejection; they return the same value. If a fixed traversal exceeds a particular smaller budget, tightening that budget cannot make it pass. Raising budgets can turn a resource rejection into success. The **first error label** may change when different guards are reached; no monotonicity of literal error strings is claimed.

Proof: each charged prefix has a nonnegative visit/work total independent of the remaining budget until it refuses. A successful traversal has every such prefix within its respective cap. Increasing the cap preserves each inequality. Each semantic check is unchanged. For the converse refusal direction use the exceeded prefix. This is a theorem of the explicit counters, not an inference that increasing available physical memory always preserves host scheduling behavior.

Malformed grammar/type/trace conditions cannot be made valid merely by raising resource caps; a smaller cap can mask their later detection. “Every rejection persists when budgets rise” is false. Hash equality, a caught exception or a smaller output is not substituted for an acceptance guard.

## 4. Structural, substitution and checker refinement

The reference grammar validates before the semantic bridge is applied. `_freeze` by itself is not a theorem that arbitrary Python values become immutable; its general fallback can retain a nonsequence object. For a subsequently well-formed type/program, however, its recursively nested representation contains only exact tuples, known tag strings and natural indices, so the typed result is immutable and has the unique constructor encoding.

Use the unchanged attempt1 maps E_T, E_M and E_C into `FiniteBridge.TypeCode`, `Term` and `Cert`. All constructor equations and the actual Lean `check` definition were read. We reuse, rather than re-census, the cutoff-renaming and simultaneous-substitution proof. In particular at binder depth b:

    Sigma_b(n) = var n                       if n<b;
               = rename (n |-> n+b) A       if n=b;
               = var(n-1)                   if n>b.

`Sigma_(b+1)=upSub Sigma_b` follows from the three variable cases. Structural induction proves the concrete successful `instantiate_type(B,A)` encodes as `instantiateType(E_T B,E_T A)`. Negative shifts are a separate checked native helper behavior; the universal-instantiation bridge uses nonnegative lifts. Each inserted argument copy is charged before its allocation, and final output validation can still refuse an oversized result.

### U03-A2-T4 — full successful checker square

For a stable/owned certificate p and valid depth d, if concrete checking succeeds with (m,A), then the **mathematical evaluation of the bound finite Lean checker definition** on E_C(p) at d returns a Checked object whose erased term is E_M(m) and type is E_T(A).

Proof by induction on the successful checking derivation:

- I/K/S: exact field/type validation establishes scoped type codes. The two implementations construct identical term/type trees.
- Application: both recursive checks succeed. Concrete equality of the function domain and argument type becomes equality of the injectively encoded TypeCodes. Both construct the same application and codomain.
- Universal introduction: the induction hypothesis is at d+1. Both erase the type abstraction and wrap the type in `all`.
- Universal elimination: the polymorphic check exposes `all B`; the argument is valid at d. The substitution result above yields the same instantiated type and unchanged erased term.
- Reduction: the checked initial certificate fixes both term and type. The concrete trace must start at that term; every following term is the deterministic head successor. Induct on trace length and use the head-step constructor equations to produce exactly one `Cert.step` per retained step. The type stays unchanged. Empty, wrong-start or invalid-step traces cannot be erased into an accepted certificate.

The head-step comparison covers I, K, S, left-spine congruence and absence of a weak-head successor. It is not full normalisation or a proof that fuel exhaustion means divergence. Work/depth/node guards may prevent any recursive case from returning; T4 concerns successful derivations and never removes those refusal branches.

T4 is an ordinary source-correspondence proof. It does not claim this conversation executed Lean, extracted Python from Lean, proved the JSON library in Lean or kernel-checked arbitrary emitted certificates. Accepted `checked_sound` applies to the mathematical Checked witness only after the constructor bridge, not directly to arbitrary raw bytes.

## 5. Export syntax and the native row compatibility decision

### U03-A2-T5 — constructor-only syntax, conditional elaboration

For a successful validated export, `_ty` and `_term` emit the corresponding finite constructors. `_cert` emits the corresponding certificate, with a reduction trace expanded to repeated `Cert.step`. Induction on constructors proves that the emitted expressions denote E_T, E_M and E_C under the fixed imported declarations and namespace. The name grammar starts with a letter, contains only letters/digits/underscore, and is at most 80 characters; generated names append fixed suffixes. No user string is injected as Lean syntax. Distinct accepted base names yield disjoint generated names because the five suffixes are pairwise suffix-incomparable. Duplicate base names are explicitly refused.

The exporter independently bounds certificate expansion at 512 counted constructors, a module at 16 rows and UTF-8 text at 1 MiB. The charge for a reduction wrapper is conservative relative to its expanded certificate tree. Type/term arguments additionally retain reference structural bounds. These are not the transport byte bound or a bound on the Lean kernel's physical working memory.

Under the exact imported constructor/checker definitions, a fresh namespace and enough host evaluator resources, T4 supplies the mathematical proposition evaluated by each emitted `by decide`. **Actual parsing/elaboration/kernel execution is not established here.** It is an exact external execution target, not a mathematical premise secretly assumed proved. The original strict-wrapper FAIL is not replaced by a promised clean build. The formal handoff identifies the accepted mapped-native preparation path separately from the new core-only Q1f packet.

### Arbitrary two-item iterable rows

The canonical `proof_export.module` accepts some generator/custom two-item rows by ordinary Python unpacking. The included documentation and tests contain no promise of arbitrary-iterator support, but that observable deployed behavior cannot simply be called accidental and removed without acknowledging the change. The attempt1 strict-row patch remains an unadopted **proposed restriction**, not full legacy extensional equivalence.

This continuation resolves the compatibility choice without guessing owner policy: add the separately named `export_module_owned` entrypoint and leave the legacy entrypoint available. It accepts only exact list/tuple rows with exact immutable name/bytes leaves, captures each bounded row, then calls the existing exporter. On that domain the original and attempt1 guarded exporter branches coincide. Adopting the strict behavior under the old name would still be a separate API decision, not needed for the new refinement theorem.

There is no total safe coercion for all arbitrary Python iterables that also preserves their operational behavior: a user-defined iterator can diverge before yielding its first item or run arbitrary host code. Rejecting such objects before calling their protocol is an explicit domain boundary. A caller-controlled conversion outside this interface does not become a verified or time-bounded operation by assertion.

## 6. Ownership classification over the complete relevant API

| Data/entry | Owner during proof-relevant use | Consequence |
|---|---|---|
| `load_json` raw | Exact immutable bytes | Stable syntax; fresh private decoded containers. |
| `dump_json`, `check`, shifting/substitution/normalisation helpers called natively | Caller may own a mutable graph | Stable-native theorem only, or use owned ingress. `_freeze` alone does not establish arbitrary-data ownership. |
| `snapshot_native` | Caller graph during capture; newly allocated private tree afterwards | Bounded read transcript, no foreign iteration callbacks; no claim of invocation-atomic deep snapshot. |
| `encode_owned` / `owned_json` | Private captured tree and immutable bytes | Encoding and decoding cannot see later caller edits. |
| Export module | Legacy rows may be arbitrary producer objects; new entry captures exact bounded rows | New strict domain has immutable name/bytes leaves; legacy behavior is retained separately. |
| `admit_json` | Immutable candidate bytes | Parsed and canonical source is privately held and stored as immutable bytes. |
| Native admission, dispatch and probability setters in the adapter | Captured before entering the state transaction | Source/value meaning is the captured request; caller's unrelated later edits have no registry authority. |
| Flat observation | Copied exact integer tuple | No post-validation list mutation; the predecessor repair is preserved. |
| Compiled nodes, checked sampler records, issued records | Fixed frozen records with recursively immutable payloads | Safe to share between private state copies under the stated no-reflection host contract. |
| Rule/observation/issuer/requirement maps | Engine-private mutable maps; adapter clones them | No borrower can obtain a mutable registry alias through the supported API. |
| Descriptions, projections, dispatch outputs | Fresh caller-owned copies, or immutable opaque Licence | Client edits cannot change committed metadata; issuer object is an identity token, not transferable authority. |
| Work counters, entropy requests, interpreter stack | Call-local or external host state | Charged/consumed even on refusal; not falsely included in registry rollback. |

## 7. End-to-end theorem and exact evidence ceiling

Combining T1–T5 gives the strongest surviving general statement:

> For the exact source bytes, H, a strict byte request or a completed owned capture, and a successful resource-bounded concrete decode/validate/substitute/check/export execution, the output has the same constructor-level term/type/certificate meaning in the finite mathematical checker. Every declared grammar/resource failure remains a refusal; host failures remain separately classified. No malformed input or budget exception is converted into an accepted certificate. Generated source has the proven constructor meaning, while actual Lean kernel acceptance requires its separate exact-pin execution.

For the broader legacy APIs the source relation includes borrowed mutable inputs, arbitrary host protocols and host faults. The countermodels show why the total/value-at-invocation version is false. This is a reformulated theorem, not an incomplete attempt to prove that false claim.

Research results are complete at this ordinary source/host-contract scope. Repository adoption, a mechanised semantics/extraction for the deployed Python interpreter, and native exact-pin elaboration remain unclaimed; none is quietly replaced by finite counts. New executed evidence is listed in `evidence/EVIDENCE_SUMMARY.json` and the associated raw commands/streams. The unchanged legacy tests, source hashes and original strict failure retain their own prior scopes.

### Final proposal self-review and verification

A new count-capture control exposed an initial exporter-adapter draft that validated one length read and traversed a second length read. A caller update could turn an allowed single row into seventeen traversed rows. The final adapter captures the length once, validates that same count and traverses exactly those rows; the rejected preimage and red-to-green evidence are retained. This is a new proposal correction, not a modification of predecessor evidence. The final fifteen-method adapter suite passes in normal and optimised Python against both canonical and attempt-0001 source copies. New named strict ingress therefore does not require silently adopting the predecessor's legacy-row restriction.
