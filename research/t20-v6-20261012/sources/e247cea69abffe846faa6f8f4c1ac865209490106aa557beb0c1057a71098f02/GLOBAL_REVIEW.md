# Independent global certificate-domain review

Verdict: PASS for primitive-recursive canonical image membership of the exact retained certificate encodings. This verdict is separate from the earlier telescope and descriptor verdicts.

## Bound candidate and fresh verification

Candidate: `hase-certificate-code-validity-20261010/validation/FINAL_FREEZE.json`, SHA256 `139a358aaa6d0ff56f28e80d2393c3671c4605eaf5892248d5de0febcc69db67`.

The independent replay freshly compiled all 41 selected additive modules with Lean 4.19.0, `--trust=0`, and the recorded `-s 65536` thread-stack setting. It verified 145 theorem axiom audits, allowing only propext, Classical.choice, and Quot.sound. All 96 certificate/payload constructor witnesses evaluated true, all eight malformed witnesses evaluated false, and five deliberately false semantic claims failed for the expected false-proposition diagnostic. Including retained core and Tel controls, 141 runtime outputs matched exactly.

All 2,993 input pins, 236 final-freeze entries, the earlier descriptor freeze, and the exact ordered inventory of 2,813 retained imported objects matched before and after replay. Four independently inspected declaration-source identities were additionally checked. The protected baseline was neither rebuilt nor edited. All 41 newly produced objects are byte-identical to the frozen author replay's corresponding objects.

Main receipt: GLOBAL_CANDIDATE_REPLAY_RECEIPT.json. Its selected source/object/log records are authoritative. Its fresh output is `global-replay-5pov3oas/`. Earlier development objects in the candidate's top-level validation directory are not interchangeable with this coherent replay.

## Semantic findings

The accepted `certValid_exact` theorem holds for every natural sort and code. Its explicit expected-sort language is:

0 Term; 1 TypeCode; 2 Poly; 3 Ty; 4 Nat; 5 Tel; 6 StepCert; 7 RedCert; 8 FiniteCert; 9 PolyCert; 10 LookupCert; 11 Claim; 12 Rule; 13 SerialCert; 14 SerialCertList. Unsupported sorts reject.

The 96 descriptor equations retain the original constructor tags, arities, payload order, external-field leaf wrappers, and final zero terminators. They correspond to 5 StepCert, 2 RedCert, 7 FiniteCert, 8 PolyCert, 2 LookupCert, 6 Claim, 63 Rule, 1 SerialCert, and 2 SerialCertList constructors. The direct declaration coverage check and exact encoding equations were reviewed independently in the earlier descriptor verdict; the final freeze preserves those identities.

Local reconstruction shape is explicitly insufficient for canonical validity. Every field is checked at its expected sort, with genuine Tel validation where required. The global theorem combines all local image equivalences, including all 63 Rule cases, with the generic bounded evaluator. Mutual SerialCert/SerialCertList recursion checks both the cons head and tail. Decrease bounds hold for every dependency of a canonical parent; for arbitrary malformed inputs, the evaluator itself rejects a dependency unless its numeric code is strictly smaller. It does not silently skip oversized children.

The primitive-recursiveness proof covers the parameterized descriptor interpreter, shape, child extraction, and the bounded global evaluator. The descriptors use only standard primitive-codable finite data. No source Primcodable instance or source-operation computability premise is assumed.

Canonical images overlap numerically. The preserved codec legitimately gives Term.zero, TypeCode.bottom, and Ty.raw the same natural code; further source/certificate overlaps are tested. Correctness therefore uses expected-sort membership, never a global numeric-sort-disjointness assumption.

## Additional independent controls

GlobalReviewControls.lean compiled against the fresh independent objects. Eleven named theorems passed allowed-axiom audits, and four additional kernel examples passed. These establish:
- Equal-size and larger-size dependencies reject in the generic evaluator.
- Any rejected child forces its parent to reject.
- SerialCertList cons rejects either an invalid head or an invalid tail, for arbitrary natural payloads, even though the outer cons shape is valid.
- A locally well-formed Claim with invalid telescope code one rejects globally.
- Every code at unsupported sort 15 rejects.
- The same natural code can be accepted at multiple legitimate source sorts.

Receipt: GLOBAL_REVIEW_CONTROLS_RECEIPT.json. Source, object, and audit log identities are included there.

## Generator and history qualification

Independent isolated regeneration reproduced all 21 generated image-rule, bounds, grammar, image, and control Lean modules byte-for-byte. The eight retained source identities and their existing reference manifests also matched. See GENERATOR_REVIEW_RECEIPT.json.

The authoritative entrypoints are the frozen verify.py and the four generator scripts named in REPLAY_NOTES.md, including generate_controls_release.py. The older generate_controls.py is a preserved defective convenience draft and is not executed by verification. Failed author elaboration/stack attempts and the independent descriptor-control reduction overflow remain diagnostic history. They are not passing checks and do not enlarge the accepted theorem scope. A freeze is an integrity envelope, not acceptance of every historical file as valid proof code.

## Explicit boundary

This is syntax/certificate canonical encoded-image validation. It is not a proof of whole semantic checker computability, equivalence of the original decoder on arbitrary malformed/noncanonical inputs, source derivability being recursively enumerable, source adoption, or T20 closure. The 96 certificate/payload constructors are not 96 logical rules or 15 judgment families; the retained six judgment families remain unchanged.

No blocking finding remains for this narrow layer. No candidate source or frozen author receipt was modified during the review.
