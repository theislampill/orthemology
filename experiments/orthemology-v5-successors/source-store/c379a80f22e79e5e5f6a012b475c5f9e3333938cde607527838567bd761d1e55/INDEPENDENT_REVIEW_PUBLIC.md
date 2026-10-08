# Independent review: original-ground extension and witness robustness

**Verdict: PASS within the expressly bounded structural and philosophical scope. No blocking finding.**

Reviewer: separate AI-conducted review, 7 October 2026 UTC. This is not external human-specialist validation or acceptance of new metaphysical premises. The candidate remains an isolated research result; no canonical repository adoption, public source selection, or later comprehensive dependency audit is authorized by this review.

## 1. Exact object reviewed

The author-confirmed fixed private candidate is `CANDIDATE_MANIFEST_v1.json`, SHA-256 `50c787b40cf0afa51f39bcba5a520a7718a48daeabc3fe495fafc1d610a4fee6`. All 47 entries match their recorded byte lengths and hashes. The approved design remains unchanged from the temporary approved copy, SHA-256 `06fef5c14ced11aa33da42d2e6e014b882cb8715cd824cad3c45f5341cb6535f`.

The decisive current appraisal is `PHILOSOPHICAL_APPRAISAL_v2.md`, SHA-256 `f56432bc48e2b5aa8394754d521e60f1bf266e17c7fa710ff3367196075e6a47`; the proof map is `PROOF_MAP_v1.md`, SHA-256 `577bc52cad53b2b1b56ce75c2b47ae9fc16d463939d98851b922ffb3162e8625`. The earlier design's open philosophical verdict is historical, explicitly superseded by the current appraisal. Its mathematical construction remains the implementation target. The historical source-binding record's awaiting-approval field is not the current candidate status.

Read in full: all three research modules, the author audit, replay script, exact theorem inventory, proof map, revised appraisal, approved design, README, custody record, and source-binding record. Targeted inherited report passages and fourteen retained primary-page images were also checked as detailed below.

## 2. Fresh mechanical verification

- Compiled `GroundExtension`, `GroundExtensionControls`, `ModalCapacityControl`, and `AxiomAudit` in a new reviewer-owned output directory. The replay copied source inputs and built its own dependency objects. `LEAN_PATH` contained only the reviewer object directory. No author `.olean` and no old-suite build object was used for the new modules.
- Toolchain: official Lean 4.19.0, commit `6caaee842e94`, binary SHA-256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`. Its identity matches the retained official-acquisition receipt. The toolchain was not reacquired and no package was installed.
- All 77 author theorems compiled and received fresh transitive `#print axioms` checks. Exact declarations match both the JSON inventory and the audit output. Seventy-three are axiom-free; four use standard axioms. The exact union is `propext` and `Quot.sound`; no `Classical.choice`, `sorryAx`, custom axiom, admitted proof, `native_decide`, or other scanned trust escape occurs.
- Fresh explicit/universe-enabled type readbacks were recorded for all 77 declarations in `TypeReadback.stdout.log`.
- Five separate reviewer boundary theorems compile without axioms: exact positive-length old-path preservation, no positive return to the added root, preservation of production's inclusion in support, a simultaneous nonempty/well-founded/covered/necessitating powerless finite control, and the real nonactual capacity witness with existing endpoints.
- Independent Python interpretation exhaustively checked 4,165 arbitrary relation/root-set combinations on 0–3 old nodes, including exact reflexive and positive-length old paths and acyclicity. It also checked all 4,165 relation/existence combinations for new-root uniqueness, 1,116 covered inputs for coverage preservation, and 592 endpoint-typed inputs for endpoint preservation. This is executable corroboration; the arbitrary-structure result is established by Lean, not by extrapolation from enumeration.
- Independently evaluated all stated finite countercontrols and the four-node capacity model. The capacity model is endpoint-typed, acyclic and covered at both supplied indices; old existence, productive/support arrows, capacity, and old support paths agree with the specified two-node base.

The principal replay is `replay-v1/REPLAY_RECEIPT.json`. The separate identity/executable audit is `INDEPENDENT_CHECKS_RECEIPT_v1.json`. No compiler or checker failure occurred in this review. All created sources, objects and logs remain preserved here. No broad inherited-suite replay or source cleanup occurred.

## 3. Formal boundary assessment

### Uniformity and what is preserved

`GroundExtension.lean` is universe-polymorphic over arbitrary node and modal-index types. A distinguished actual index supplies nonemptiness of the indices where required; no finiteness of the old node collection is assumed. The new individual is `none : Option A`; old identities are embedded by `some`. Old existence, old productive edges and old necessary-existence predicates are unchanged by definition. The nonempty finite fixture prevents the separation from relying solely on an empty productive field.

`old_profile_iff` (lines 71–86) preserves arbitrary supplied profile predicates on tuples of old individuals. It is not a formal syntax/semantics theorem for all modal formulas and does not establish an elementary or unrestricted theory-conservative extension. Quantification over the expanded metaphysical domain, newly permitted interventions on the ground, and the broad `Root` predicate may change. Profiles must not already encode the disputed whole-originality conclusion or silently quantify over the enlarged ontology. The design, current proof map and appraisal acknowledge this restriction. The supported description is **old-field/profile preservation**, not unrestricted conservative extension.

### Direction, paths, roots and coverage

An edge `S a b` runs from supporting source to recipient. `Path` is finite reflexive-transitive reachability. `Acc S b` inducts over incoming sources, so the well-foundedness theorem has the intended ancestry orientation. The independent positive-length check additionally establishes exact preservation when a strictly positive path is required, including potentially cyclic old relations; no reflexive zero-length path is being counted as a productive act.

The generic `old_path_iff` proves both directions, and there is no path from an old node into the new one. `Acyclic` excludes an edge followed by a reflexive return path, thereby excluding self-loops as well as longer cycles. Well-foundedness is preserved when supplied, not inferred from coverage. The infinite control has a root supporting every natural-number node and the strict descending edge orientation `a → b` when `b < a`. Each chain node has a larger predecessor indefinitely; coverage and acyclicity coexist with failure of ancestry well-foundedness. Its Lean proof correctly establishes this general infinite case.

`Root` means existence plus no incoming represented support edge. It does not, without a faithful exhaustive representation premise, prove absolute existential nonreceipt. `Coverage` means every existing individual has a finite support path from an existing root. This is an explicit inherited premise, not local causality proving original completion.

The new root is original at every index, but uniqueness and transferred coverage are claimed at the distinguished actual index only. The all-world countercontrol correctly supplies a second old root elsewhere. The code does not equate actual originality with essential independence by bare modal logic.

### Grounding and modal scope

The added targets are the **fixed old actual roots**, at every index. The necessary-root hypothesis is essential for the intended all-index endpoint typing and grounding necessitation. It is visibly assumed by `ground_necessitation_preserved` and `support_endpoints_preserved`, not proved as metaphysics. The missing-necessity fixture appropriately violates this hypothesis; it is not a model of the full accepted philosophical package.

`GroundNecessitates` composes along grounding paths. It is not imposed on mixed support or productive ancestry. The finite necessary-agent/contingent-effect example is a real countercontrol: mixed support from the new necessary root reaches an effect missing nonactually. Therefore no whole-history necessitation or contingent-effect necessity has been obtained.

`Necessary` means existence of the same supplied individual at every supplied modal index. It neither introduces a modal accessibility theory nor certifies that these indices exhaust metaphysical possibility. `none` is mathematically constructed; the code does not discover an actual entity.

### Power and actual provision

The powerless extension leaves genuine old productivity intact while the unique actual root has `liftHolder H none = False`. The conclusion is non-entailment from the weaker structural/profile premises. It is not a countermodel to a stronger applicable perfection premise that requires power.

The uniform parameterized-holder variant makes the limit exact: an actual original standing holder exists iff the new root's holder proposition holds. This alone is a predicate-level interpretation. The separate finite capacity module goes beyond a label: `modalAble ground` has the explicit witness `modalP true ground extra`, with both endpoints existing at that nonactual index and the extra effect absent actually. Actual productive arrows still run from the old holder to the old effect, and no actual productive path runs from the ground to that field. A mixed support path does run there.

The nonvacuous capacity interpretation is a bounded finite control, not an arbitrary-base theorem realizing every proposed power semantics. In particular, arbitrary modal-index types need not supply a nonactual index. The current candidate correctly does not claim otherwise. Nor is one witnessed ability a semantics of unrestricted power, wisdom or volition.

No hidden agency premise, efficient-grounding identification, full-field creatorhood, or all-originals-are-powerful assumption was found in the general theorem. Production's inclusion in support, if assumed of the old field, is preserved; the reviewer separately checked that elementary connection rather than confusing the two relations.

## 4. Source and philosophical assessment

All eleven recorded inherited document/text/PDF identities were rehashed successfully. Targeted report checks covered T17 paragraphs 40–68 (especially 44, 48–61 and 65–68), T18 paragraphs 5–18 and source guide paragraph 24, and T19 paragraphs 67–85. Those passages support the appraisal's ownership and premise distinctions:

- T17 already accepts actual original completion and its qualified-bearer realization account. The same-witness contingency-as-need inference is substantively warranted there, not newly earned by the structural extension.
- T17 paragraphs 56–61 separately warrant essential independence. Necessary existence and actual nonreceipt alone do not supply it.
- T17 paragraphs 65–68 affirm a separate pure-perfection ascent beyond gifts already manifested in creatures, retain eligibility/cost/contradiction conditions, and distinguish standing power from exclusive actual production.
- T18 paragraph 15 closes the unrestricted claim that every autonomous obtaining fact automatically supplies the required power-bearing subject. It does not retract T17's affirmative baseline.
- T19 paragraphs 77 and 81–85 require typed, genuine productive attribution. They do not turn noncausal grounding or capacity into actual efficient ancestry, and they keep assertion ownership distinct.

The reviewer also inspected fourteen already owned Asbahani page images: one-based PDF positions 155–157, 499–503, 508, 551–552 and 559–561, corresponding to printed main pages 55–57, 399–403, 408, 451–452 and 459–461. This is selected prior-source verification, not new acquisition, full-volume reading, manuscript collation or historical discovery. Detailed primary-text/apparatus observations are omitted from this projection for separate source selection. No raw source images or body are included, and the reader does not inherit other roles' broader source coverage.

The revised appraisal gives the affirmative bypass its proper force. If Φ is genuinely an actual individuated necessary reality with complete existential nonreceipt, merely describing its grounding as noncausal does not defeat T17's independently accepted positive pure-perfection comparison. Applying that defeasible rationale to Φ is warranted at the inherited standard, absent a specific incompatible constitution, need or defect. This is a reasoned new application of an inherited judgement, not modal necessity alone entailing power and not absence of a defeater serving as the entire positive argument.

The remaining limitations are correctly retained: an obtaining proposition need not furnish an individuated reality by notation; actual individuation/independence and eligibility remain substantive application premises; standing power does not by itself yield actual efficient provision of the observed field. The powerless model therefore neither refutes T17 nor establishes a possible rival ground, while the capable model prevents the discussion from ignoring the accepted perfection route.

## 5. Integration disposition

Accept the frozen candidate as a **kernel-checked uniform structural extension**, with **finite nonvacuity and scope controls** and the **bounded affirmative philosophical appraisal** above. Preserve the current appraisal's supersession of the earlier open assessment, its T17–T19 ownership statements, and the profile-language restriction.

Do not project it as:

1. a proof of metaphysical possibility or actual existence of a noncausal ground;
2. a refutation, downgrading, or machine reproof of T17's actual warranted conclusion;
3. an unrestricted necessity-to-agency theorem;
4. all-world uniqueness, universal well-foundedness, or mixed-support necessitation;
5. a full-domain conservative extension or a complete formal semantics of every pure perfection;
6. proof of actual efficient authorship, common Creatorhood or revelation attribution.

No author revision is required for this scoped acceptance. The later full premise/dependency-DAG campaign remains separate and was not begun here.

Projection note: This public report is derived from the independently reviewed original at SHA-256 4682ac642288b8b58d025c5b7d68063f0db452445e4b750b6aeb9a2840f0215d. Only the primary-reading paragraph projection and candidate locator change above were made; the formal findings and verdict are preserved. The private candidate manifest and raw execution receipts are digest-referenced, not selected for redistribution.
