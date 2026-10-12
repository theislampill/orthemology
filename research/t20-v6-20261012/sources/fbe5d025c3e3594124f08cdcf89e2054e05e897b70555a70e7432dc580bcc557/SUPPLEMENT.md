# Telescope code transport and final selected replay

The original pinned source set and first replay remain unchanged. That replay freshly checked all twelve positive modules and all eight axiom audits, but its direct `decide` negative control could not reduce the well-founded evaluator. That reduction failure was not treated as a successful semantic rejection. Corrected negative files first rewrite using the already kernel-proved rejection equations, then attempt `decide` on the false boolean equality. They must fail specifically because that proposition is false. `verify_supplement.py` retains the original pins, adds the new modules and corrected controls, replays the full selected proof chain afresh, and requires these corrected failures.

The immutable core module `TelescopeCodeValidity.lean` is not modified by this supplement.

`TelescopeNatTransport.lean`, namespace `TelescopeCodeValidity`, exposes:

- `encode_map_encode_tel (Γ : P01AC.Tel)`: `Encodable.encode (Γ.map (fun A : P01AC.Ty => Encodable.encode A)) = Encodable.encode Γ`.
- `telNatDecode : Nat → List Nat`: ordinary standard `Encodable.decode (α := List Nat)` followed by `getD []`.
- `primrec_telNatDecode : Primrec telNatDecode`.
- `telNatDecode_encode (Γ : P01AC.Tel)`: `telNatDecode (Encodable.encode Γ) = Γ.map (fun A : P01AC.Ty => Encodable.encode A)`.

This makes the list-of-head-codes transport explicit for natural-code mixed substitutions and weakenings. It does not replace the telescope codec by a tree codec or silently identify structured telescopes with natural lists. The only `Primcodable` instances needed for this transport are the standard natural-number and list instances. No source `Primcodable Ty` or `Primcodable Tel` premise is introduced.

Replay command: `python hase-telescope-code-validity-20261010/verify_supplement.py`. Final receipt: `validation/SUPPLEMENT_REPLAY.json`. Supplement pins: `validation/SUPPLEMENT_PINS.json`. Fresh selected replay still leaves the protected baseline unchanged.
