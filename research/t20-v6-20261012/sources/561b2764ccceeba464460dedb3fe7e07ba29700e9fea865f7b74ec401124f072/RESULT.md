# Occurrence, source-owned content, and operation-relative retention

11 October 2026. Additive active-T20 reassessment. No protected changes or adoption. Source bindings and actual reading scopes are in `READING_RECEIPT.json`; executable controls are in `controls/`.

## Result

A bounded source-record application survives the admission test. The actual T16 Quran 48:9 fixture supplies seven interpreted claim occurrences, including their commentary, reported/direct voice, qualifications, and complete or partial antecedent rows. Applying the inherited T20 finite-contract theorem to those supplied records gives an exact, small result:

- Preserving just the antecedent row needs no sidecar beyond that row.
- Also preserving the fixture's direct-exposition versus reporting distinction requires a two-value sidecar, or one fixed-width bit.
- Additionally supporting exclusion of a named commentary from the selected record view requires a three-value sidecar, or two fixed-width bits.

The minimum concerns this declared record-view service, with the antecedent row retained. It is **not** a minimum memory for linguistic understanding or human warrant. The new work is a concrete crosswalk and finite application of already-owned D1/D2, not a new general theorem. The relevant record, not a hypothetical Arabic reading class, supplies the distinction.

A second result is a coverage refinement: the separate commissioned-content `SOURCE_RETURN.md` contains an affirmative source-owned distinction absent as a separately bound source in the current foundational source register. Qualified inquiry may impose a real circumstance-relative duty even where the inquirer lacks knowledge of the actual source ruling. That does not imply every warranted route is unavailable, and it does not undermine the source's truthful original guidance. The return also explicitly limits a universal demand for maximal disclosure. Those are inherited substantive results deserving preservation, not discoveries of a new philosophical gap.

Several more ambitious transports were rejected as already owned or unsupported. In particular, neither the T16 source rows nor a successful sidecar computation identifies a commissioned assertion, authenticates its source, proves its truth, or supplies a recipient's actual uptake.

## 1. The old stopping decision and its actual successor

T15's occurrence passage (derived report lines 275–283) records a justified stop. H-ICS already supplied the compatible-relation/natural-join/parity mathematics, and the then-inspected occurrence packet did not supply the proposed complete joint reading class. Naming a made-up relation after Quran 61:5:4 would not have supplied the missing input. This stop remains correct at its date and target.

T16 then supplies a **different selected source-relative fixture** for Quran 48:9. Its report at lines 183–195 and its seven-record JSON are substantive owners. They do not claim an exhaustive class of admissible Arabic interpretations. Six claim occurrences supply complete rows, and one supplies `(M,M,null)`. The complete selected relation is `{(M,M,G),(G,G,G)}`. Here M and G name the grammatical antecedent proposals Messenger and God, respectively. They are not assertion-owner labels.

The record's null means unspecified in that particular claim. It is not a wildcard authorizing completion. The existing checker already demonstrates that taking coordinate marginals produces unsupported `(G,M,G)` and `(M,G,G)` rows. It already preserves copied claim identity and the distinction between Ibn Ashur's direct exposition and his partial report attributed to Ibn Abbas. These are inherited positive applications, not an unperformed T15 task.

Consequently the present investigation may use the supplied T16 records for a new declared record query. It may not promote them to all admissible readings, choose the correct theological interpretation, independently count the reported majority, or identify the unresolved al-Qushayri from his name. The fourth commentary discussed in the report is not a machine-input record.

## 2. Exact new application and proof

### 2.1 State and operations

The represented state is one selected T16 claim record, or an absorbing state `excluded-from-view`. There are eight states. The retained coarse record r is its three-coordinate antecedent tuple, including the explicit null where present; the excluded state has its own distinct coarse value.

The narrow voice label v has two values: the JSON's `direct_exposition` / `direct_exposition_with_reasons` records count as direct exposition; its other records count as reporting. This is only a grouping of the frozen record descriptors. Direct exposition is not a claim of exclusive final preference, personal inner belief, or commissioned assertoric ownership.

The first contract retains r only and has a copy operation which preserves the source-record identity. The second also retains v. The third additionally permits `exclude_work(w)` for each of the three named commentary IDs. Applied to a record from w, that operation moves to the excluded state; otherwise it leaves the record unchanged. Copy and exclusion leave an already excluded state excluded. Costs are zero and all operations are enabled in all represented states.

These are explicit operations on a selected view of records. No source is deleted, falsified, declared unreliable, or treated as an independent evidence root. The one-way view is deliberately bounded: reinclusion, restoration from the absorbing state, token-level correction, and changes to the linguistic interpretation are outside its operation menu. Nothing in this calculation proves a minimum for those richer contracts.

### 2.2 Why the coarsest partition is exactly (row, voice, work)

If two live records have the same antecedent row, voice, and work, their required outputs agree. For any named-work exclusion they either both remain or both enter the excluded state. Copy also agrees. Thus this grouping, with the excluded state separate, is contract-preserving.

Conversely, different antecedent rows cannot be merged because r is retained. Different voice values cannot be merged because v is required. If the rows and voice agree but the works differ, exclude the first work: one record is excluded while the other remains live. The distinct retained coarse outputs make the merge invalid. Therefore every contract-preserving partition refines `(row, voice, work)`.

This proves the coarsest partition directly for this deterministic service. It is an instance of inherited D1's branch-labelled refinement, not a new bisimulation theorem.

### 2.3 The actual collision

The fixture contains these two exact records:

1. `qurtubi-48-9-attributed-split`: al-Qurtubi's report attributed to al-Dahhak, row `(M,M,G)`, reporting voice, work `QURTUBI_JAMI`.
2. `ibn-atiyya-48-9-reported-split`: Ibn Atiyya's report attributed to “majority,” row `(M,M,G)`, reporting voice, work `IBN_ATIYYA_MUHARRAR`.

They have identical r and v. Excluding `QURTUBI_JAMI` removes only the first from this view. Retaining both the antecedent proposal and whether it is reported therefore still loses a declared future response if the work is erased.

The direct al-Qurtubi split exposition supplies a third block in the same MMG fibre. The GGG fibre likewise has three blocks: al-Qurtubi's reported unified selection attributed to al-Qushayri, Ibn Atiyya's reported unified variant, and Ibn Ashur's direct unified exposition. The partial row and excluded state each have one block.

### 2.4 The exact sidecar bound

A deterministic sidecar paired with r must give different labels to the three blocks in either complete-row fibre. Hence its common alphabet has at least three values. Three suffice: enumerate the three blocks separately in each fibre and reuse those labels across different r-values. This is precisely inherited D2's within-fibre pigeonhole/label-reuse proof.

Thus the third contract needs alphabet size 3 and fixed-width length ceil(log2(3)) = 2. For the second contract, each complete-row fibre contains two voice blocks, so alphabet 2 and one bit suffice and are necessary. The first contract needs alphabet 1 and zero bits. These are three nested **declared** contracts; moving between them does not make the earlier representation defective for its earlier task.

For this particular fixture the third partition happens to distinguish every record. That accidental fact does not make a claim-ID sidecar universally minimal, imply that any future additional fields are unnecessary, or establish that all seven records are independent grounds. A new record set or operation menu requires recomputation.

### 2.5 Executable checks

`controls/contract_check.py` checks the exact SHA-256 of the unchanged seven-record source, then enumerates all 4,140 partitions of the eight represented states. The number of admissible partitions is 25, 4, and 1 for the three contracts, respectively. Their unique coarsest partitions have 4, 6, and 8 blocks.

An independent encoder enumeration examines all assignments from smaller candidate sidecar alphabets to the seven active records (the excluded state has its own coarse key, so its sidecar is fixed). For the strongest contract no one-value or two-value assignment works; exactly 108 three-value assignments work. The one-bit voice contract has eight valid binary assignments. This enumeration corroborates the direct written proof; it does not establish the truth of the manual source interpretation.

A separate direct-signature oracle recovers the same 1/2/3 minima without partition refinement. Deliberately erasing named-work operations or erasing the voice distinction is rejected by the boundary controls in both normal and optimized modes. This is a separate code path by the same author, not independent review.

The own checker uses explicit exception-raising requirements rather than Python `assert`; normal and optimized runs produced identical JSON. The inherited T16 checker was separately copied unchanged and replayed in normal mode only. Its original assert-based scope is not upgraded by running Python with optimization. The inherited replay retains two complete rows, one partial record, and seven source/voice contract checks.

## 3. The precise join to source-owned veracity

### 3.1 Four source relations cannot be collapsed

The held owners distinguish at least four relations:

- A grammatical expression refers, under an interpretation, to a particular antecedent.
- A commentary records, expounds, or attributes that interpretation.
- An original communicative source owns an assertion with exact contextual content at an occasion.
- A present recipient has and actually exercises, or suitably retains, a warranted route to that source-owned content.

The T16 rows address the first relation and retain important parts of the second. They do not supply the third or fourth. A G in `(G,G,G)` names a grammatical antecedent proposal; it cannot be inserted as the g argument of `m.asserts c g t q`. Likewise the `attributed_holder` and `attributed_selector` fields are reports by the commentary, not independently acquired statements from those people. Copying a report does not add an independent acquisition.

### 3.2 The older occurrence algebra preserves the correct smaller target

T10's actual `ARTICLE.md` and `EXACT_EFFECT_ALGEBRA.md` compute selected output-to-context references by stack effects and compose them through source-bound substitutions. Their origin keys include snapshot and source-context occurrence, not just equal strings. Multiple emitted outputs sharing a context require one missing role observation for the **all-author** query, while their output occurrence IDs remain distinct and their full propositions remain separate data.

Its correction `ORACLE_AND_FORCE_PRECISIONS.md` explicitly preserves original-source role and current-carrier force as two relations. A present quotation can faithfully carry an old assertion without becoming a new assertion or authorization. Boundary identity acquisition is separate from the later role-only cover problem; the corrected lower bound requires locality of complete observable responses, not merely independent target labels.

Thus three tempting shortcuts were already rejected by the older owner: deduplicating equal words as equal sources; treating a context-origin quotient as identity of all emitted tokens; and transporting old source force into current carrier force. The present application does not rediscover them.

### 3.3 The actual veracity theorem has the missing types in its signature

The inspected unchanged `VeracityBoundary.lean` defines `asserts : Occasion → Source → Token → Content → Prop` and contextual `trueAt`. Its local theorem consumes exact owned-token assertion, local awareness and control, plus K/D/N/P and the same-source exercise bridge. It concludes truth at that occasion for that content. It does not conclude recipient warrant.

A justified semantic adapter could use the occurrence record to retain a source/token/content/occasion identification and the separately warranted assertoric ownership needed by this theorem. T10's context role alone does not supply all those terms and premises; T16's antecedent row plainly does not. This is an interface comparison, not a missing premise in the established positive philosophical argument. T17's affirmative exceptionless source-owned veracity appraisal remains intact, including its distinction between exceptionless scope and defeasible warrant.

The current commissioned-content report supplies the positive recipient route: reliably transmitted C, its warranted source attribution, truthfulness in the relevant reporting domain, and appropriate actual uptake or retention can warrant assent even if two original wordings express C. Exact wording stays part of the target when prescribed. The proof that C is true and the warranted claim that this source communicated C remain different.

The finite application therefore contributes **preservation of already supplied source-relative distinctions**, not a new way to create those grounds. It shows exactly where row-only and row-plus-voice summaries are inadequate for a chosen future source-selection operation.

## 4. A source-owned correction about later practical duty

The separate `commissioned-content-access-test-20261009/SOURCE_RETURN.md`, SHA-256 `52fbe080e7bd57f6c06e695a28428052463702d3ccce72bf2c7ba6ad493250d0`, was read in full. The current foundational register binds the earlier REPORT for FND-031 but does not separately list this source-return hash among its 49 source entries. The earlier manifest explicitly retains both. This is a bounded coverage finding; the register never claimed exhaustive fresh reading.

The return reads Majmūʿ 14:142–167, with the decisive legal-relief discussion at 149–155 and immediate continuation at 159–160. Its actual substantive distinction is stronger than a bare later-loss possibility:

- The original source has genuinely permitted something or removed a burden.
- A later recipient or intermediary does not know the relief, lacks suitable advice, or follows mistaken mediation.
- The qualified inquirer can nonetheless be obligated to state the result of their actual inquiry.
- That circumstance-relative duty does not transform the original permission into an original prohibition.

The report explicitly separates `O_inquiry ⇒ knowledge-of-the-actual-source-ruling`, which the source case does not support, from `O_inquiry ⇒ adequate opportunity`, which absent knowledge alone does not refute. It also separates these from an independently established unexcused duty whose required performance is warranted uptake of this actual source teaching. The latter needs its own appropriate opportunity bridge.

This matters for semantic correction. Replacing an intermediary's mistaken attribution can restore access to an already-valid permission without positing a newly changed original law. Conversely, a representation preserving only a practical verdict such as “must state restriction” cannot silently identify that verdict with “the original source prohibited it.” This is an actual source-owned separation; no invented psychological episode is needed.

The immediate continuation's beneficial-obscurity examples further block a universal move from greater information to lower practical burden or universally required disclosure. They do not license inventing messages, hiding relevant evidence, or dismissing a specific promised access undertaking. The source still affirms one actual truth and the positive original guidance. The report expressly withholds any inference that all routes were unavailable or that a specific present person's ignorance proves culpability.

Suggested additive synthesis wording:

> The separate later-obligation source return supplies a positive source-owned instance of original permission coexisting with mistaken mediation and a real duty to state the result of qualified inquiry. That duty neither changes the original ruling nor entails knowledge of it; absence of knowledge also does not establish absence of every adequate opportunity. The immediate continuation admits purpose-sensitive beneficial obscurity. These findings sharpen the target of a continuing obligation-to-access bridge while preserving truthful original guidance.

This source paragraph and the T16 record-view result are distinct contributions. Neither mathematically certifies the other.

## 5. Overlap, rejected transports, and stopping decision

1. **A new join/parity theorem:** rejected. T15 identifies H-ICS ownership; T16's exact row/marginal contrast is already implemented. The present increment uses named-work filtering and a specified output label, with an exact inherited-theorem application.
2. **Proposition preservation implies attributed-content preservation:** rejected as already owned. T10, the commissioned-content REPORT, and the later cumulative-content note expressly separate these.
3. **Commission plus general trust fixes a particular report:** rejected as already owned. The current source-content owners require actual attribution, content and reporting scope. The Tibyan note explicitly says it found no new missing distinction.
4. **Source role is the current carrier's assertion:** rejected by the actual T10 correction, not newly discovered here.
5. **A formal sidecar is human warrant:** rejected. D1/D2 and the support-scope report already require independently justified meanings and actual basing; this application deliberately represents records rather than people.
6. **Later loss contradicts original veracity:** rejected as already owned. The original-content report and the substantive SOURCE_RETURN preserve the relevant temporal, audience and normative distinctions.
7. **FND-031 has a newly refuted philosophical conclusion:** rejected. Its existing scope is compatible with the source return. The gain is explicit preservation of a less visible positive source application.
8. **A new empirical or Arabic certification problem must now be solved:** rejected. The held record's manual interpretation remains bounded; no empirical study, historical adjudication or broad new source campaign was needed or initiated.

The useful outcome is therefore an exact source-bound record contract plus an inherited philosophical coverage refinement. No further general proof or human-warrant application is justified merely by inventing more labels. A richer correction operation should be investigated only if a concrete task supplies its actual semantics and evidence. This pass stops at the verified application and precise source return, while retaining all affirmative source-owned grounds.
