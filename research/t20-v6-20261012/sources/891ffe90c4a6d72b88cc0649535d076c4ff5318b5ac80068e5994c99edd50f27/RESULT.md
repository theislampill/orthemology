# Exact canonical telescope-code validation

Additive evidence for the existing `Encodable P01AC.Tel`, definitionally `List P01AC.Ty`. The retained list instance has `encode [] = 0` and `encode (a :: xs) = Nat.pair (encode a) (encode xs) + 1`. No source encoding, decoder, datatype, or instance is changed.

## Interfaces

Import `TelescopeCodeValidity`, namespace `TelescopeCodeValidity`:

- `validTel : Nat → Bool`
- `primrec_validTel : Primrec validTel`
- `validTel_exact (c : Nat) : validTel c = true ↔ ∃ xs : List Ty, Encodable.encode xs = c`
- `validTel_encode (xs : Tel) : validTel (encode xs) = true`
- `telHead`, `telTail` are the first and second projections of `Nat.unpair (c - 1)`.

Import `TelescopeDecoderBridge`:

- `normalizeTel : Nat → Option Nat`
- `primrec_normalizeTel`
- `normalizeTel_decode₂ (c) : normalizeTel c = (Encodable.decode₂ Tel c).map Encodable.encode`
- `primrec_tel_decode₂_reencode : Primrec (fun c => Encodable.encode (Encodable.decode₂ Tel c))`

The bridge concerns canonical `decode₂`; it does not claim ordinary source-decoder equivalence.

## Proof

`ExactSyntaxValidity.evaluate` is instantiated at state `(unused sort, list code)`. At zero, the shape accepts with no children. At a successor, the head is validated by the retained exact Ty validator and the sole child is the tail. The actual numeric tail is strictly smaller than the successor code by `Nat.unpair_right_le`. `tel_rule` proves the source-list image decomposition, using the unchanged `Encodable.encode_list_cons` and pair/unpair laws. `evaluate_exact` then proves the all-input image theorem. The shape and child operations are primitive recursive; the retained evaluator theorem yields `primrec_validTel`.

No `Primcodable Ty`/`Primcodable Tel`, arbitrary-Encodable primitive-recursion theorem, computability premise, admission, or extra axiom is used.

## Controls and replay

`TelescopeValidityControls` proves an all-natural-number raw-cons equation exposing both head and tail validation. It includes all-input malformed-head, malformed-tail and nested-malformed-head rejection theorems; positive image controls; six positive runtime checks and four negative runtime checks. Rejected negative Lean modules try accepting a bad head, accepting a bad tail, and replacing the list codec with the tree codec.

Run `python hase-telescope-code-validity-20261010/verify.py` after initialization. The runner checks all pinned upstream and local inputs before and after, freshly compiles selected required upstream modules plus all telescope modules with Lean 4.19.0 `--trust=0`, audits the listed theorem axioms, checks runtime outputs, and requires each negative module to fail for its expected reason. It writes `validation/AUTHOR_REPLAY.json` with hashes, logs, and fresh-output paths. `validation/INPUT_PINS.json` is immutable after initialization. The baseline is not rebuilt, and protected inputs are never written.

This proves telescope canonical-image recognition and its canonical decoder bridge only. Whole certificate validity, checker computability, source derivability enumeration, and T20 closure remain outside this artifact's claim.
