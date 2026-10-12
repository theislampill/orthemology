# Final telescope and list-code transport artifact

## Current replay entrypoint

Run `python hase-telescope-code-validity-20261010/verify_final.py`.

Read `validation/FINAL_REPLAY.json` for the final selected Lean 4.19.0 trust-zero receipt and `validation/FINAL_PINS.json` for all preserved upstream, original, supplement, and final inputs. This entrypoint supersedes the earlier runners; their sources and failed-attempt logs remain immutable evidence.

## Current interfaces

- `TelescopeCodeValidity.lean`: exact primitive-recursive canonical-image validator for the unchanged `P01AC.Tel = List P01AC.Ty` encoding.
- `TelescopeDecoderBridge.lean`: primitive-recursive canonical `decode₂`/re-encode bridge for `Tel`.
- `TelescopeNatTransport.lean`: explicit telescope-to-list-of-natural-head-codes transport.
- `ListNatCodeTransport.lean`: algebraic generic `encode_map_encode {α} [Encodable α]` and `listNatDecode_encode`, with the standard primitive-recursive `listNatDecode : Nat → List Nat` decoder/getD. No `Primcodable α` premise is used or inferred.
- Control and audit modules verify genuine/malformed codes and the precise theorem axiom dependencies.

The generic algebraic list identity is not a blanket claim that arbitrary Encodable source functions are primitive recursive. Source datatypes, encoders, and existing instances remain unchanged.

## Preserved diagnostic development

The first selected replay passed its twelve positive modules and eight axiom checks, but direct `decide` could not reduce the well-founded validator in its attempted rejection test. Corrected tests rewrite by kernel-proved rejection lemmas before trying to prove the false equality. The second replay passed all fourteen positive modules, all eleven axiom checks, and both corrected rejection tests; it then exposed an incorrect namespace in the old wrong-codec diagnostic. The final, independently checked negative file names the actual `SourceFamilyComputability.node`, and its false codec equality fails specifically by a definitional mismatch. No source theorem was changed by either diagnostic correction.

The final runner recompiles sixteen selected modules, checks fifteen axiom-audit entries, checks six positive and four negative runtime outputs, and requires three diagnostic rejections for the expected semantic reasons. All pinned inputs are rechecked before and after. The protected baseline is not rebuilt or mutated. Whole checker computability, ordinary Tel decoder equivalence, source derivability enumeration, and T20 closure are not claimed by this artifact.
