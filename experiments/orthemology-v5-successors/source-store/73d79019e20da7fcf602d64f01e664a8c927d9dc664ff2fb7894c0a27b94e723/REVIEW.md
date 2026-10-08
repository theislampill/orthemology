# Independent review: finite deletion-trace application

Disposition: PASS for the frozen, bounded application. No mathematical or model-scope defect requiring a source revision was found. This is an independent claim-level review, not authority to integrate, release, adopt an upstream theorem, or close the wider T20 programme.

## Identity and independence

The reviewed packet is `../122/FROZEN_HANDOFF.json`, SHA-256 `5754d2e4f04d42c1ea1af67c0a10a304271a54e2b1974851240cd7437348b83d`. Its 16 listed files matched both hashes and byte lengths before replay and matched hashes afterward. The bound author receipt is `../122/formal/verification-run03/VERIFICATION.json`, SHA-256 `068bb6132923f0916f65f52116fa9e96ee7c50f88a03e0de41eafc1c31101c3f`; the main source is SHA-256 `0df33942b13f157d7952adb89c43d6f9934892c52af8c5d511973945e2b2dea2`.

The reviewer was newly dispatched with the frozen task description, not the author's execution context. This review read the model, ownership plan, exact sources, tests, readbacks and receipts. A separately written replay harness compiled fresh local objects instead of calling the author's replay harness or loading the author's local objects. Separately written enumeration uses retained index subsets, not the author/coordinating enumeration implementations. Coordinating and author receipts were inspected as prior evidence and are not counted as new reviewer checks.

All review writes are inside this review directory. The frozen scientific source, repository, integration candidate, original receipts and upstream source were not edited.

## Fresh replay result

- Official existing Lean 4.19.0 compiler, SHA-256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`, with `-j1 --trust=0`.
- Fresh compilation of `TraceControls.lean` and all 13 examples in `RationalFixtures.lean`, plus the existing contract.
- All 19 theorem names were independently extracted from source and matched the declared inventory. Full explicit universe/type and axiom readbacks exactly matched the frozen author readbacks.
- The observed axiom union is precisely `Classical.choice`, `Quot.sound`, and `propext`. No authored `sorryAx` or additional axioms were admitted.
- 2,157 imported objects were independently resolved and hash-bound: two newly compiled local objects and 2,155 existing cached imports. All cached hashes match the author receipt. The cache is trusted, not rebuilt.
- No OAI upstream module or Real module occurs in the actual import closure. No Lake, install, download, upstream 4.34 build, or Comparator execution occurred.
- All four false-scope controls failed at their intended propositions: reversed retention/deletion value, extending positive-copy TV to zero data, uniqueness of the first retained position, and different source labels forcing different observation laws. There were exactly three `False` goals and one explicit `decide` refutation, with no syntax/import failure substituted for the test.

Evidence: `replay/INDEPENDENT_REPLAY.json`, `replay/READBACKS.json`, `replay/IMPORT_BINDINGS.json`, and replay logs. The earlier author's empty-module RED contract is a development check only, not independent mathematical evidence.

## Claim-level review

| Claim | Finding and exact ceiling |
| --- | --- |
| Complete channel | PASS. `Fin 7` encodes all seven binary words of length at most two. `true` retains a position; retention is 1/4, deletion 3/4. Emission preserves order and includes empty output and its length. Normalization and nonnegativity are proved for all four two-bit words. |
| Exact pair law | PASS. For 00 the masses on empty, 0, 00 are 9/16, 6/16, 1/16. For 01 the masses on empty, 0, 1, 01 are 9/16, 3/16, 3/16, 1/16. Other outputs have mass zero. One-trace TV is 1/4. |
| Positive copied counts | PASS. `copies_injective` quantifies over every natural M with an explicit proof of `0 < M`. `copyMass_at` and `duplicate_tv` use that hypothesis. The result is not inferred from a bounded M enumeration. |
| M=0 | PASS. All input traces map to the unique empty function; total mass is 1, TV is 0, and equal-prior decision success is exactly 1/2. The all-M upper bound of 5/8 remains valid but is deliberately weaker at M=0. |
| Arbitrary randomized policies | PASS. The theorem quantifies over arbitrary `K`, `[Field K] [LinearOrder K] [IsStrictOrderedRing K]`, and every function `h : Trace → K` satisfying the stated bounds. It is not restricted to rational policies or deterministic policies. The finite calculation is specialized to this channel pair, not a newly implemented generic TV theorem for arbitrary laws. |
| Sharp 5/8 optimum | PASS. The frozen source proves the upper bound via the exact signed mass vector. Reviewer-only kernel checks give a bounded likelihood-sign policy attaining 5/8 in any such K, and a first-coordinate policy attaining it for every positive M. Thus “optimal” has a checked attainability witness as well as an upper bound. |
| Pushforward correspondence | PASS. The source's `duplicateSuccess` correctly samples one realized trace and then repeats it. Reviewer-only kernel checks prove full-space normalization, zero off the diagonal support, equality between full-space TV and `copiedTV`, and the pushforward expectation identity. This closes the possible gap between operational pullback notation and the explicit copied law. |
| Source labels | PASS, conditional on the stated model. `worldMass` discards the first component of `Bool × Word`, so changing the label at fixed word preserves the law by definition. It does not prove actual historical sameness or authenticity. An all-M source-label decision obstruction is written mathematics, not a separate endpoint in this 19-theorem module. |
| Known-word position ambiguity | PASS. For known 00, masks retaining only position one and only position two are distinct and both emit 0; each conditional mass is 1/2. Reviewer checks verify the conditioning mass is positive and the two other masks have conditional mass zero. This target is original-position attribution, not the historical source/utterance-event target or a programme-specific occurrence predicate. |
| Fresh independent traces | PASS as a written finite derivation with bounded enumerative checks. Sharing a fixed latent word is intended; masks must be independent conditional on it. For this pair, common product mass is `(1-p)^M`, hence TV `1-(1-p)^M` and equal-prior optimum `1-(1-p)^M/2`. No general fresh-product theorem is promoted to a kernel result. |

## Additional independent counterchecks

Twelve reviewer-only theorems compiled under the same trust setting, with their explicit types and allowed axioms recorded in `EXTRA_READBACKS.json`. They establish the support/expectation checks, sharp attainment, failure of zero-count injectivity, complete mask conditioning, impossibility of a simultaneous 2/3 guarantee, and counterexamples when either the lower or upper decision-probability constraint is dropped.

The separate exact-rational enumeration in `COUNTERCHECKS.json` covers:

- All four length-two words and retention endpoints/interiors 0, 1/4, 1/2, 3/4, 1.
- Copied and directly mask-generated fresh laws for M=0 through 4 at those five parameters; normalization and exact predicted TV/optimal-success values.
- All 128 deterministic rules on the complete seven-symbol trace alphabet, and 2,187 randomized rules taking values 0, 1/3, 1. These finite checks support, but do not replace, the universal ordered-field theorem.
- Removing empty outputs and conditioning on being nonempty changes the pair's TV from 1/4 to 4/7. This checks that empty traces are a material observation-contract condition.
- At two observations, copied joint-empty probability is 9/16 versus 81/256 for fresh masks. The mixed empty/zero event has probability zero for copies and 27/128 for fresh masks, while both coordinate marginals agree.
- With known 00 and first trace 0, each possible positive-probability second fresh trace leaves that first trace's position posterior at 1/2. Exposing the actual mask would instead change the attribution service, even though this particular binary pair's TV happens to remain 1/4.

The review test's first compile had local test-authoring errors in type inference, closed `Fin.val` reduction, and a missing pair of parentheses around a negated conjunction. Its failed source and log are retained. The reviewer-only test file was corrected and then compiled cleanly. These failures are not findings against the frozen source and are not counted as semantic negative controls.

## Source, ownership and semantic scope

`SOURCE_SCOPE.json` independently verifies 38 selected upstream source blobs against both SHA-256 and the recorded Git blob identity at commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. The family scope page links only the September 24 lower-bound manuscript. The three Comparator names are `quantitative_sample_lower_bound`, `superpolynomial_one_trace`, and `superpolynomial_sample_complexity`. The October 5 decoder remains a manuscript claim. The challenge `.lean` file deliberately contains statement placeholders; its existence is not proof evidence. No upstream novel lower or upper bound is needed for the application or receives fresh kernel credit from this review.

This reviewer read the selected opening channel, theorem and resource statements for both manuscripts, not both full proofs. The author's broader reported reading is not silently relabelled independent review.

The H-ICS record-fibre criterion, feasible-support output determination and observation congruence, and T9's explicitly inherited observation-limited separation and copied-root/occurrence distinctions, support the ownership map. The new credit is a selected elementary application and its checks, not a general information theorem, new reconstruction algorithm, or upstream theorem adoption.

“Content” must mean the encoded word at the channel boundary. Binary-word recovery does not by itself recover a contextual proposition, intended meaning, illocutionary force, source-owned assertion, truth or authority. The proposal explicitly requires a lossless encoding, decoding, and the content equivalence it preserves. That interpretation bridge needs independent warrant in a real application. Two situations with equal word bytes may differ in contextual meaning; the source-label control remains valid for the declared word-only channel without erasing that distinction.

The eight application conditions in the proposal remain obligations. This is a two-word equal-prior discrimination control, not a general decoder guarantee, per-instance authenticity certificate, actual transmission study, participant/statistical result, or authorization. Copies can retain availability, durability and fault-tolerance value. The information bound assumes ideal repeated access to the same already-realized trace.

The ordered-field formalization is finite algebra. Ordinary real-probability interpretations are included, but no asymptotic convergence claim is made for arbitrary non-Archimedean ordered fields.

## Minor documentation note

The frozen design document's opening status still says “No Lean implementation” and its proposal section says approval is pending. The ownership execution ledger and README clearly give the later implemented status. Treat the design status as historical, and label it as such if it is excerpted or republished. This does not change or block the scientific verdict; the frozen packet was preserved without editing it.

## Review disposition

The coordinator can use this PASS only for the digest-bound elementary application and the evidence classes distinguished above. Integration, acceptance and wider programme disposition remain owner decisions. No claim in this review supplies a new source-authentication, normative, general convergence or whole-family Lean result.
