# Aggregate cancellation successor: independent review

## Verdict and lineage

PASS for immutable runtime-cancellation-v5, manifest SHA-256 `bc52d02249a41172488dc7caa34844802eeec4df811f644e4888ad2f412792d5`.

The successor simulates the actual accepted `cancelWith` state transition, preserves partial effects, and proves that a true current-call reply establishes a cumulative common cancellation certificate and durable exclusion of that complete envelope through every later finite trace of the enlarged runtime class. Its statements remain one-way at the Boolean/certificate boundary.

All files inherited from the v4 scientific manifest are byte-identical. The copied predecessor manifest is exact. The v4 source argument remains historical; the separate cancellation addendum and `CURRENT_CLAIM_MAP.md` correctly identify the enlarged trace type. The v4 scientific verdict is inherited only at its original scope. Its current reporting identity is the separately corrected v4 receipt, with the original receipt and exact correction retained for provenance.

No frozen scientific-source correction is required. Public distribution-wrapper acceptance, `runBatch`, progress, arbitrary clock updates, fault discovery, alias transport and external warrants remain separate.

## Verification

The four added modules were freshly compiled, sequentially, with official Lean 4.19.0 and the disclosed 65,536 KiB thread stack. The previously independently cold-built v4 objects were consumed read-only after exact source comparison; no new full rebuild of those 34 unchanged modules is claimed. Their object identities were recorded and checked again after replay.

Comment-aware enumeration found 45 added theorem declarations and 289 combined declarations. A separate axiom audit covered all 289. Every closure is contained in `propext`, `Classical.choice` and `Quot.sound`. No custom axiom, proof hole, unsafe declaration or native truth oracle appears in the scientific sources. All candidate and inherited source identities remained stable.

The accepted full native fixture and its 3,013-byte source remain unchanged. Eight additional independent challenge theorems also compiled with standard logical axioms only. Commands, source identities, inherited object identities and logs are bound by the incremental replay receipt.

## Operational translation

`cancelResponders` is the exact bounded-root representation of the current call's filtered acknowledgement list. The actual predicate is the disjunction of taint and requester equality to the full envelope's actor. Its order, length and distinctness are proved against the unchanged runtime list. No cancellation-specific faulty-signing or faulty-opening parameter is added.

For a valid outer guard, the simulation emits one common `cancelAck` event per actual responder. Each intact responder stores the complete envelope tombstone. Bad responders may add acknowledgements without storing a tombstone, exactly as the accepted function specifies. Nonresponding intact roots contribute neither acknowledgement nor mutation.

`cancelWith_preserves_alignment` preserves the entire existing relation: root count, budget, both thresholds, plant, complete effective policy, continuing taint set, root policy/revocation/commitment/tombstone membership, idle boundary and the authenticated certificate stream. It requires no current permission to execute the original action. Actual cleanup rights and authentication remain external premises.

Invalid path, duplicate-address or unselected-address guards produce exact full-world identity and false. A false threshold result after valid guards is treated separately: actual partial tombstones and their primitive acknowledgement events remain. The proof never substitutes identity merely because the return Boolean is false.

## The Boolean and accumulated-certificate distinction

`true_cancel_implies_certificate` first uses the current call's distinct responder count, the equality of runtime and authority budgets, and finite-set cardinality. It then embeds that current set into the union with existing acknowledgements. Thus a true call establishes the accumulated common B+1 certificate.

The converse is false. The included two-call fixture proves that two one-root calls, each returning false, produce a genuinely aligned and reachable common state with an accumulated certificate. Repeating the same root leaves the distinct certificate set at one root. No desired certificate is manually inserted into an assumed state.

`true_cancel_requester_matches` also derives model requester equality from the fault bound: B+1 distinct responders contain an intact root, whose reply requires that equality. This is a theorem about the input field and model predicate, not evidence of real-world identity authentication.

The reply threshold is a sufficient epistemic guarantee of an intact response, rather than a necessary condition for physical/model veto in every individual case. Independent checks show that one intact reply can already block the otherwise valid unlanded operation while the Boolean is false and the common B+1 certificate is absent. This reinforces, rather than contradicts, the candidate's one-way claim.

Distinct-root deduplication likewise concerns the certificate set. The actual runtime tombstone list appends again on a repeated valid call. Independent checks verify list length grows from one to two while the common distinct acknowledgement set remains `{1}`. The representation correctly uses membership and does not claim whole-runtime idempotence for repeated cleanup calls.

## Expanded trace and durable exclusion

`RuntimeWithCancellationTrace` embeds every old `RuntimeTrace` without extra side conditions and adds actual cancellation calls. Each new step is simulated using its real outer guard and outcome. A true call may append a justified common close event; a false call still retains its real response events and may leave a previously accumulated certificate intact.

`runtime_cancel_trace_refines_history` derives the common history inductively for arbitrary finite enlarged traces, preserving alignment and reachability at every boundary. Current full-policy admission remains available after such traces.

`true_runtime_cancel_blocks_all_continuations` derives the cancellation state and certificate from the actual call, derives the common continuation using the expanded simulation, applies durable tombstone persistence, and then uses the established live runtime gate correspondence. It quantifies over every later requester and existing shared `badOpen` value. No global classifier is inserted as an extra runtime veto.

The conclusion is scoped to the exact full envelope. Ordered path, action, successor and nonce remain part of identity. A control deliberately reuses the nonce with a separately valid reversed ordered path and shows that it may land. That does not satisfy a correct actor's fresh-nonce discipline and does not justify a broader nonce ban.

## Controls assessed

The retained native-source controls substantiate the stated boundaries:

- B replies from the bad root alone return false and leave an otherwise legitimate prepared action able to land.
- B+1 replies containing one bad and one intact selected root close a still-unlanded, version-current operation, so prior execution cannot mask the cancellation veto.
- A wrong requester gets insufficient bad replies and cannot create the intact tombstone needed for this closure.
- Distinct partial replies accumulate across false calls, while repeated roots are deduplicated for certificate counting.
- Duplicate and unselected acknowledgement addresses fail before mutation.
- Cleanup after certified revocation still stores the tombstone.
- Cleanup after lawful execution preserves the complete landed plant.
- Delayed preparation does not erase the tombstone.
- Same nonce does not identify different complete envelopes.
- The native closed-before-prepare example instantiates exclusion after every later enlarged trace.

## Independent challenges

`CancellationV5Challenges.lean` establishes eight additional checks:

1. One intact reply can return false yet veto a later attempt.
2. That one-root state lacks a B+1 common certificate.
3. Repeating that root appends a second runtime tombstone while the certificate set remains `{1}`.
4. The repeated-call common state is itself aligned and reachable through actual calls.
5. Every actual cancellation call preserves the complete plant, without any action-validity premise.
6. A wrong requester causes full runtime-state identity, independently of its modeled reply count.
7. Cancellation preserves every root's commitment list; veto does not rely on deleting earlier preparation evidence.
8. Every old runtime trace embeds unchanged into the successor language.

The wrong-requester identity statement is unconditional state behavior. A claim that its Boolean must be false additionally needs the aligned fault-budget assumptions, as supplied by the main source theorem.

## Retained ceilings

The runtime language still has no clock-update event, and the successor proves constant `World.now` by induction. The common timestamp mechanism remains distinct from a warranted physical clock or elapsed service time.

The fixed fault set bounds the lifetime union of relevant failed duties. Coherent root-wide memory, same-command non-bypassable mediation, atomic complete-plant/time observations, authentic source and policy custody, legitimate grants, retained cleanup entitlement, actual reservation/consent and real authentication remain substantive external premises.

The expanded class remains bounded by the original operation-language restrictions, including its envelope subtype and authentic successful certification constructor. It proves neither arbitrary physical fault behavior nor unrestricted whole-program refinement. No progress, capacity, discovery, unknown-root alias, N2, T0 or R5 conclusion follows.
