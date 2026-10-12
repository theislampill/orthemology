# Exact proof-system separation: participating root contributions

10 October 2026. These are successor consequences of the new concrete model, not replacements for any frozen result.

1. NoInternalNegation.lean uses the unchanged full-PER model's positive semantic interpretation of the actual W(originalQ) and its actual HasE soundness theorem. It proves that no source proof polynomial inhabits W(originalQ) → Bottom. With the new homogeneous-model noninhabitation theorem, the exact W is independent of the current source proof rules in the sense that neither it nor its internal negation is derivable. It remains true in the intended full-PER interpretation. This is not an assertion that a mathematical truth has become false or that the two interpretations are identical.

2. CertificateSeparation.lean recompiles the exact inherited T16 UnaryCertificateSyntax, verified against its source-store SHA-256. Its positive HasC witness of the literal compiler identity is reconstructed using the existing certified constructor, certificate generator and checker theorem. That positive result is inherited. The new consequence combines it with fresh HasE noninhabitation: there cannot be a translation of every closed HasC proof to some HasE proof of the SAME type, even if the proof polynomial changes. This does not exclude translations changing types, relative semantic translations, restricted fragments, or the uninvestigated reverse direction. It does not introduce or adopt a new calculus.

Both new root modules compiled with Lean 4.19.0 --trust=0; only propext, Classical.choice and Quot.sound appear. The source grammar and inherited objects were not modified. Independent reviewer was asked to replay these contributions and literal endpoint alignment separately.

The old phrase 'HasC has no HasE coercion' must not be treated as an inherited mathematical proof of the new impossibility result. Conversely, the inherited positive HasC theorem is not new credit merely because it was recompiled in this comparison.

Source recovery: exact pinned repository file fetched through GitHub; original content hash 5f80f464475cb12a6ad90fc89c3540912322f31470be86e26072a990222115c4. Source acquisition and local hashes are in ROOT_SOURCE_BINDINGS.json. The full inherited HasC soundness file was not recompiled; its opening 42 lines were inspected only to identify its original semantic scope. The positive proof here uses the unchanged syntax/certificate rule directly and claims no fresh all-context HasC semantic theorem.

T20 remains active. This settles these exact source-strength questions, not unrestricted type-theoretic completion, philosophical warrant, repository integration or owner acceptance.
