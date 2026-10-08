# Aggregate cancellation: a separate bounded successor

## Relation to the accepted lifecycle model

The accepted v4 source and LIFECYCLE_ARGUMENT.md are preserved unchanged. This addendum extends its known-root runtime class with the exact existing cancelWith function. The new RuntimeWithCancellationTrace embeds every old RuntimeTrace and adds cancellation calls. It does not add runBatch, progress, clock advancement, a fault-discovery strategy, unknown-label transport or a new physical implementation claim.

## Exact operational translation

For a valid outer guard, the runtime counts the supplied distinct selected acknowledgement addresses that satisfy either of two conditions: the address is tainted, or the requester field equals the full envelope's original actor. These are the exact responders used by the simulation.

Each responder contributes one common cancelAck event. An intact responder records the complete envelope tombstone before contributing the reply. Tainted responders may contribute a reply while retaining no tombstone. Nonresponding intact addresses contribute no event. The function has no cancellation-specific badSign or badOpen argument, and this extension invents none. The existing preparation and attempted-landing flags retain their previous meaning.

The path, acknowledgement distinctness and selected-address guards are consumed explicitly. Invalid outer guards return the original World and false. A false threshold result after a valid outer guard may still retain partial tombstones; it is never treated as identity merely because the Boolean is false.

The simulation preserves full alignment: root and threshold fields, plant, complete effective Policy, continuing fault set, local policies, revocations, commitment/tombstone membership and the authenticated certificate history. Cleanup does not require the original action still to be permitted. It does not modify the plant and cannot roll back an earlier lawful landing.

## The crucial one-way Boolean statement

A true cancelWith result proves that this call contains at least B+1 distinct selected responders. Under the continuing fault bound, at least one is intact. It has stored the exact full-command tombstone, and the common accumulated cancellation certificate follows. A separate theorem also derives equality of the model's requester field and the original actor; this is not a proof that a real authentication service correctly bound a human identity to that string.

The converse is false and is not claimed. The common cancelAcks field accumulates distinct replies across the whole history. The runtime Boolean counts only the current call's responders. Two individually false one-root calls can produce an accumulated common certificate, while repeating the same root twice does not increase the distinct count. The fixture proves this at genuine aligned, reachable common states, rather than by manually inserting a desired certificate.

A true current-call result may be represented by an additional close event. False returns do not force absence of a previously accumulated certificate and do not produce a false equivalence between the two interfaces.

## Durable actual-runtime exclusion

After a true actual cancelWith result, the same full envelope cannot land after any finite continuation of the enlarged actual-operation class, regardless of the later requester or shared badOpen value. The proof first derives the actual response events and their accumulated certificate, then applies the common arbitrary-continuation tombstone theorem, then uses the proved live runtime gate correspondence. The classifier does not veto the runtime as an additional hidden gate.

The scope is the exact full Envelope. An altered ordered path, action, successor or nonce is a different command. The controls deliberately show that reusing the same numerical nonce with a different ordered path can remain admissible if separately valid. That witness violates a correct actor's fresh-nonce discipline and is not offered as a recommended strategy. No global nonce ban or cancellation of every related future operation is inferred.

## Exact-source controls

The controls use the accepted raw2-to3 fixture and its full 3,013-byte source. They establish:

- B replies from the bad root alone are insufficient; a still-valid prepared operation can still land.
- B+1 replies comprising one bad and one intact selected root block an unlanded, still-version-current operation.
- A wrong requester cannot obtain closure from the available bad replies.
- False calls retain partial tombstones, distinct replies accumulate, and repeating one root is deduplicated.
- Duplicate or unselected acknowledgement addresses trigger full identity before mutation.
- Cleanup after revocation still stores the tombstone.
- Cleanup after a lawful landing leaves that complete plant unchanged.
- A delayed preparation cannot erase an existing tombstone.
- Cancellation is scoped to the complete command rather than only its nonce.
- The durable exclusion theorem applies to every later trace of the enlarged runtime class.

## Retained limits

World.now remains constant across this bounded operation language; the successor explicitly proves that fact. There is no theorem of clock authenticity, real-time service, stable authorisation windows or residual-work feasibility. Cancellation's cleanup entitlement, source/Policy authenticity, actual reservation and real authentication remain external institutional premises. The same continuing lifetime fault union, coherent root-wide memory and same-command physical mediation are required.

The result advances the operational join. It does not prove N2, T0, R5 defeat or a common metaphysical bearer.
