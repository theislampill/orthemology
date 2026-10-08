# Independent cold source review of A1

Reviewed immutable manifest: `923206fcb0d870806b6e77ca259f99e0604876ac872d97c0bf70c100fb460bd3`.
Status: independent source replay and all 49 A1 plus 15 reviewer axiom checks passed. See REVIEW_RECEIPT.json and ACCEPTANCE.md.

## Unchanged contract

The delivered `FiniteSelectorSource.Certificate` requires raw natural-number digit equality in all three fields. Its cycle and target fields each quantify over four finite supports and two Boolean arguments twice. The stage field quantifies over the four supports. No decoding quotient replaces the equality, and neither reachability nor an observed-history restriction weakens it.

The inherited `cellIndex` has value `4 * supportCode B + 2 * bitNat first + bitNat second`. The new reverse roundtrip reaches every index in `Fin 16`; the inherited forward roundtrip gives the semantic inverse. The new support roundtrip similarly reaches all four stage cells. Therefore residue equality is not assumed from incomplete observations. It is derived from exhaustive digits using the generic radix theorem.

## Arithmetic reconstruction

`digit_mod_pow` uses divisibility of the smaller radix power into the truncation power. `residue_eq_iff_digits` then inducts on the width using the quotient/remainder recurrence. It has no hidden positive-base premise; base zero and base one are covered by the underlying natural division/remainder identities. The application uses ordinary bases 2, 32 and 16.

The target conversion is exactly `2^(5*i) = 32^i`, hence sixteen target cells occupy 80 bits. Four stage cells of four bits occupy 16 bits. All sixteen cycle cells occupy 16 bits. The proof of `sameCells_iff_normalize_eq` explicitly converts every direction; no boundedness is silently applied to unbounded data.

## Payload and orientation

`bit_encoding_injective`, inherited `support_code_injective`, `target_encoding_injective`, and `retained_encoding_injective` cover their finite carriers. `retained_encoding_le_sixteen` excludes raw payloads 17 through 31 from the image. Presence is not erased: none is zero; some empty is one. A separately compiled reviewer control explicitly derives rejection of the original Certificate from a raw payload greater than 16.

The sparse fixture fixes target and stage choices on every support. Its target digits are four zeros, four sixes, four elevens, then six, six, eleven, eleven. Its stage digits are zero, five, ten, fifteen. The cycle differs between orientations only on the four full-support cells. Full support, fallback false, residue false is cell 12; its raw bit is the opaque retained initial candidate. Thus a certificate for one fixed literal record supplies exactly the corresponding orientation equality.

`literal_certificate_iff` extracts that bit from the original cycle field, without evaluating the retained choice. `certificate_iff_exact_normalForm` compares arbitrary certified data with the already proved conditional literal at `initialCandidate`. The reverse direction uses generic normalization invariance of the same Certificate. The target remains the delivered sparse kernel/menu/priority.

## What uniqueness does and does not mean

`bounded_certificate_iff` yields the unique used-width record. `certificate_iff_literal_plus_high` gives the full unbounded equivalence class by three arbitrary natural high-digit coefficients. The nonuniqueness witness adds one high cycle bit. Consequently full numeral identity is neither asserted nor needed.

The generalized unique bounded existence theorem uses inherited classical `certifiedData`; it does not compute tables from a kernel. `normalizeCertified` truncates supplied data, and `extractCertifiedLiteral` reads a finite bit from supplied already-certified data. Their value equations do not provide the closed orientation or eliminate the premise that a Certificate has been supplied.

## Boundary controls

The malformed support input 4 reads cycle bit 16, so the high-bit witness produces raw component outputs zero and one despite equality of every semantic certificate cell. This directly blocks unrestricted extensional equality of the raw natural-input component functions. Future program transport must establish bounds at the actual call sites. No equality of serialized bytes, arithmetic costs, resource meters or finite-fuel success follows from the present quotient.

No all-history, physical-frame, or measure transport theorem is present in A1. No universal Python-to-Lean refinement claim is present. The Eighth mathematical task-stack and callFuel soundness/completeness results remain inherited, not a newly closed implementation correspondence.

## Evidence custody

The source census independently matches 7 definitions and 42 theorems. The snapshot hashes, all manifest files, absence of extra Lean sources, and approved specification hash were independently checked. Both known author development proof-script failures were copied with unchanged source/log/receipt bytes. All historical resource-inconclusive probes retain their dispositions and are not rerun.
