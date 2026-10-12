# Independent telescope/list transport review

Verdict: PASS for the frozen telescope layer only.

Frozen candidate: `hase-telescope-code-validity-20261010/validation/RELEASE_FREEZE.json`. The current release entrypoint is `verify_release.py`, as explicitly recorded by `REPLAY.md`; `CURRENT.md` retains the superseded final-runner entrypoint for diagnostic history.

Independent replay: `TELESCOPE_REVIEW_RECEIPT.json`. All sixteen selected modules compiled in a separate review output directory with Lean 4.19.0 `--trust=0`; fifteen theorem axiom audits were restricted to propext, Classical.choice, and Quot.sound. Six genuine and four malformed runtime controls matched. Three false propositions were rejected for their expected semantic reasons. All 2,944 release pins and all 35 frozen file entries matched both before and after. The protected baseline was neither rebuilt nor edited; the author's frozen receipt was not overwritten.

The accepted claims are:
- `validTel` is primitive recursive and recognizes exactly the image of the unchanged `Encodable (List P01AC.Ty)` encoding, for every natural input.
- The head is checked against the actual Ty canonical validator; the tail is recursively checked. Nil is exactly zero, and the successor pair format is retained. The tail strictly decreases, including on malformed positive codes.
- `normalizeTel_decode₂` and `primrec_tel_decode₂_reencode` concern the canonical decoder `decode₂`, not equivalence to the original decoder on all inputs.
- `encode_map_encode` is a generic algebraic theorem for every `Encodable α`, using the retained standard list encoding. Its exact source-list transport is not a new flattened codec.
- `listNatDecode` is the standard `List Nat` decoder with empty default and is primitive recursive. On genuine encoded lists, it produces exactly their element-code list. No `Primcodable α` premise is used or inferred.

No source Primcodable instance, original-decoder/all-input equivalence, whole-checker computability, derivability enumeration, global certificate canonical validity, or T20 closure is accepted by this review.
