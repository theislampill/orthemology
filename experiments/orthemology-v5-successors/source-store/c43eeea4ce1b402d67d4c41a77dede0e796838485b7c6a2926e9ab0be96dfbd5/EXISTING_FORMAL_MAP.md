# Existing formal coverage and common-source map

Read-only source audit, 7 October 2026. This report adds no Lean source, theorem, philosophical warrant, replay result, or repository edit.

## Result first

The strongest exact retained mathematical core for T19 P00092–P00097 is Sixth `Orthemology.Tranche6.ConnectedUnity`, especially `common_cover_of_connected_local`, `local_connected_iff_least`, and `unique_root_of_connected_local`. It proves a conditional local-to-global result for an inhabited strict transitive relation. The local premise already says that **every node has one bearer covering its entire reflexive ancestor cone**. Connectedness propagates identities of those covers; it does not establish their existence or interpretation.

An independent reviewer source proves the forward result constructively without invoking the author's unity theorems or using choice. The same packet proves the exact missing-support condition for a single target and supplies a genuine infinite connected graph with one root but no complete cover. Thus the source already anticipates precisely the unsupported-derivative-branch warning in T19 P00096.

The graph proof has no primitive act, productive-mode, bearer-qualification, source-perfection, mediate-attribution, CND or modal predicate. Its application to T19 needs separate, relation-faithful warrant for those matters. In particular, the graph's `LocalCover` is not a Lean consequence of T19's CND and source-mode appraisals. No later Lean extension connecting those predicates was located in the inspected successor source store.

## 1. Snapshot, status and source notation

Repository root R = `predecessor repository`.

Read-only Git identity observed:
- HEAD `fd0903d99d657c35e32fddcc8864d2a77930cf40`
- Tree `e7b47c7e3dc18685c33904181d9d31d7cd75495f`

This is the through-T16 candidate snapshot. T19 report P00010 separately records adopted main `19de267c`, tree `08a6452e`, through final Sixth, and PR30 open/unmerged at this candidate. This audit did not query the live remote or claim a later adoption state.

Short source labels below expand to exact repository-relative paths:

- CU = `experiments/orthemology-v5-continuations/source-store/261ba4fbf10ee9d8baf1e4330bd9e842b23a0ffcbcadf3f3338cc2f47e240eea.lean` (`ConnectedUnity.lean`)
- IR = `experiments/orthemology-v5-continuations/source-store/b47fc7376e7ec701edabd721775d45db944d6ee2c312273dadf61559fa897988.lean` (`InfiniteRootlessBranch.lean`)
- RP = `experiments/orthemology-v5-continuations/source-store/db96ef53e43355b052b9305011e5e8c0f3987b7ad12345a46564e0b5c3f94ad6.lean` (`ReviewerProbes.lean`)
- UG = `experiments/orthemology-v5-continuations/source-store/ed447b67a6cd54b901384cca59eb94cd339d6a2f6c5cd2dbe3a77803c0b0ddd3.lean` (`UpstreamGround.lean`)
- SI = `experiments/orthemology-v5-continuations/source-store/45ab18f7305033091f8fc31bb906d4c87866de47138df76637c6937440064503.lean` (`SourceIdentity.lean`)
- PC = `experiments/orthemology-v5-continuations/source-store/8765c137491f2f5e2cd9e0c699987c53fcbb00b9cc9e90b49712ec124e97906a.lean` (`ProductiveCompleteness.lean`)
- CR = `docs/provenance/v5-research-continuations/notes/06a096f0844f48eac253a26b455ea7f995385b4d5f1743eb0306d61c206f9292.md` (full independent Sixth connected-source review)
- UR = `docs/provenance/v5-research-continuations/notes/934cc5b7ce40fe8b2b426374cf484b5ea67eff4c8bf53bdab027f69fd741a141.md` (full independent upstream review; same body also retained as `25c6c5ef…md`)
- UP = `docs/provenance/v5-research-continuations/notes/77c25b97efa8b1d0cd61e815cf154faee5b3d0dcc6c9f72faedfb8e0a6b87265.md` (upstream premise/rival map)

All six Lean sources above were read directly. The quoted definitions and stated proof dependencies below come from source, not merely the review summaries.

### Ownership and evidence layers

1. `SI` and `PC` own retained Third-tranche implications. SI explicitly identifies its actual-root necessity core as prior canonical h-modal Theorem 1 (SI:4–9,39–40). Neither is a Sixth novelty.
2. `UG` owns Sixth complete-coverage-to-predecessor-freedom without global well-foundedness and its composition with unchanged SI.
3. `CU` and `IR` own Sixth local-cover/connectedness factorisation and genuine infinite support controls. `RP` owns independent constructive proofs and additional adversarial controls.
4. `SIXTH_FINAL_OVERLAY.json`, `current_selections`, maps `T6-UPSTREAM` to `S6F-02` as `SCOPED_SUCCESSOR`, specifically: coverage implies independence without global well-foundedness; local covers plus connectedness factorise a least ancestor; a connected one-root infinite fork can lack complete coverage.
5. `RESULT_STATUS.json`, rows `T6-UPSTREAM` and `S6F-02`, reports `VERIFIED_DERIVED`, inherited `CONDITIONAL_PHILOSOPHY_WITH_FORMAL_MODELS`, fresh `FRESH_COMPONENTS`, adoption `CANDIDATE`; empirical, normative, external-peer-review and novelty warrants remain `NOT_ESTABLISHED`. The research-status field must not be confused with whether the Sixth registry itself landed on main.
6. Stored component receipts `checks/549ba6a7f094-connected-author.json`, `checks/549ba6a7f094-connected-review.json`, and `checks/eff5fada59f4-upstream-author.json` report `FRESH_KERNEL_COMPONENTS`, exit 0, kernel verification and exact source hashes. These are retained historical evidence, **not fresh execution in this T20 audit**. They trust pinned official Lean 4.19.0 and official dependency caches.
7. The connected receipts say `original_controls: NOT_RUN` for that component execution and explicitly defer separate native/positive/mutation-control associations to the overlay. They must not be described as independently rerunning the entire original driver. The full original CR:59–77 reports its separate broader replay, readbacks and tamper checks. The UG component receipt records original controls PASS.

### Exact text custody gap

The connected author's actual prose files are registered but not distributed in this checkout:
- `SOURCE_MAP.json` id `src-549ba6a7f0941c36-ef0541a8983592e3`: `projections/connected-author/CONNECTED_SOURCE_UNITY.md`, original SHA256 `a5d4a68b6e3b9c874a7855385bc28180b9a83951f34c9700015b2e00b9e2ecb7`, 16527 bytes; `path:null`, `CUSTODY_ONLY`.
- id `src-549ba6a7f0941c36-67555c1eb5ca5f1a`: `projections/connected-author/PREMISE_AND_RIVAL_MAP.md`, original SHA256 `7dbdfaa708f5d3fcb091ba01748a13758172bf973e5404b19e88404b78b62201`, 7544 bytes; `path:null`, `CUSTODY_ONLY`.

CR:11 identifies the author archive as `Sixth_Connected_Source_Unity_Author_v1_20261001.zip`, 373480 bytes, SHA256 `7bfe5cb1dd028c93c311f0ee8d14348e6b45796fb1f6a75e246edea72b83e7a4`. Therefore the P0–P4 application map in section 3 is a source-supported reconstruction from the directly read formal files, full review and T19 P00094, **not a verbatim quotation of the unavailable original numbered premise table**.

## 2. Exact graph definitions

Strict ancestry `r : D → D → Prop` is a parameter, not a separately defined transitive closure. Core theorem hypotheses supply:
- irreflexivity `∀ y, ¬ r y y`
- transitivity `∀ a b c, r a b → r b c → r a c`

The philosophical productive reading is outside those formal hypotheses. CU:3–5 explicitly marks productive reading, local-completion existence and full field scope substantive. CR:37–43 distinguishes strict efficient ancestry in one fixed respect from generic causation, intrinsic inherence, spatial/epistemic association and proper productive acts.

Exact definitions (CU:10–25):

- `Below r a b := a = b ∨ r a b`
- `Root r g := ¬ ∃ y, r y g`
- `LocalCover r g x := Below r g x ∧ ∀ y, Below r y x → Below r g y`
- `LocallyComplete r := ∀ x, ∃ g, LocalCover r g x`
- `LeastAncestor r g := ∀ x, Below r g x`
- `Path r x x` by `refl`; a `step` accepts `r x y ∨ r y x` followed by `Path r y z`
- `Connected r := ∀ x y, Path r x y`
- `RootAncestor r g x := Root r g ∧ Below r g x` (CU:147)

Consequences of exact typing:
- `Below` is equality plus the already-transitive relation; equality is not a productive self-loop.
- Connectedness is finite undirected path connectedness; the domain itself need not be finite, temporally well ordered or globally well founded.
- `Root` here contains no existence predicate. In an actual-world application, actual existence and predecessor-closed scope have to be supplied by the domain interpretation.
- `LocalCover` includes g's membership in x's reflexive ancestral cone. It also covers **every** member of that cone, including actual contributors dispensable for a coarse endpoint if these belong to the chosen history-inclusive relation.
- `LocallyComplete` ranges over all D, including ancestral nodes and a root itself. It is not merely a cover of the selected output, every visible endpoint, every qualified source's selected act, or one supported branch.
- A root covers itself by equality (CU:60–64), so an actual productive act cannot be read off reflexive coverage.

### Strict versus reflexive coverage

UG:15–16 uses the earlier strict-target predicate:
`Coverage r g x := r g x ∧ ∀ y, r y x → y = g ∨ r g y`.

It requires an actual strict edge `r g x` under the intended interpretation, unlike CU's reflexive `LocalCover`. By elementary unpacking, strict `Coverage r g x` corresponds to `LocalCover r g x` together with `r g x`; this comparison is an audit observation, not a newly claimed retained theorem. Do not silently exchange the two predicates in an application.

## 3. P0–P4 application premises: exact role and outstanding bridge

The P-label allocation is explicit in T19 P00094; supporting exact requirements are in CU and CR. These are application conditions, not a Lean structure named P0P4.

| Premise | Required role | Exact formal/source boundary |
|---|---|---|
| Sixth P0 | Actual field and adequate scope: inhabited domain of actually relevant candidates; all real predecessors capable of altering root/coverage classification retained in the declared respect | `base : D` supplies only formal nonemptiness (CU:92,106,129,140). Actuality/predecessor closure are interpretation burdens (CR:35–39). RP:148–154 proves omitted predecessor can manufacture roothood. Empty-domain control CU:260–271 blocks existential inference from vacuous universals. |
| Sixth P1 | Faithful strict productive ancestry in one fixed respect, including the appropriate mediate contributions | `irrefl` and `trans` are explicit (CU:89–93). r is assumed, not manufactured. CR:39 denies generic causal transitivity and conflation with attributes/other causal respects. T19 P00082–91 supplies occurrence-sensitive mediate-attribution argument, not a graph-definition theorem. |
| Sixth P2 | Complete local coverage for every node: `∀ x, ∃ g, LocalCover r g x` | CU:14–17. This is the substantive singular-completion premise. CR:17–21 expressly says an irreducibly plural original joint account can deny P2; connectedness does not refute it. T19 P00093–95 assesses CND, source-mode perfection and mediate attribution as new philosophical support. The existing math does not derive P2 from those notions. |
| Sixth P3 | Genuine productive connectivity of that same declared field | `Connected r` via finite undirected `Path` (CU:21–25). One connected field does not absorb other independent domains (CR:37). Graph connectivity must use the same interpreted productive relation as P1/P2. |
| Sixth P4 | Act/source interpretation connecting graph coverage to actual productive sourcehood; reflexive coverage is not an act | Nontrivial strict ancestry can yield a strict descendant (CU:198–206), but not a proper unborrowed act. CR:41 expressly keeps `HistoryComplete`, `UnborrowedActs`, `ProductiveWitness` separate. RP:197–210 proves a least-source graph alone does not force `HistoryComplete` for an independently assigned act interpretation. |

Important namespace collision: later foundational P1 = whole productive/original completion and later P2 = particular bearer identification, e.g. Eleventh assembly ARTICLE:17. They are not Sixth graph P1 = ancestry and graph P2 = universal LocalCover. T19 P00094 specifically warns about this. The reconstructed DAG should use qualified identifiers such as `S6.P2.local_complete` and `upstream.P1.original_completion`, not a single node called P1.

## 4. Positive proof dependency DAG already present

All the following are exact retained results, with namespace prefix `Orthemology.Tranche6.ConnectedUnity` unless otherwise stated.

1. `below_transitive` CU:27–35: r transitive → Below transitive.
2. `root_of_local_cover` CU:43–52: strict transitive r + LocalCover(g,x) → Root(g). No WellFounded hypothesis.
3. `local_cover_unique` CU:54–58: two local covers of one target coincide.
4. `roots_agree_on_edge` CU:66–73: LocalCover(g,x), LocalCover(h,y), r(x,y), strictness and transitivity → g=h.
5. `roots_agree_on_path` CU:75–87: a locally covering source selection has the same value along every undirected path.
6. `common_cover_of_connected_local` CU:89–101: strict transitive r + base:D + LocallyComplete + Connected → ∃g ∀x LocalCover(g,x).
7. `least_of_connected_local` CU:103–109: same hypotheses → ∃g LeastAncestor(g).
8. `least_implies_local_and_connected` CU:111–125: a least ancestor gives local completion and connectedness; this reverse direction needs neither strictness nor transitivity.
9. `local_connected_iff_least` CU:127–135: for inhabited strict transitive r, (LocallyComplete ∧ Connected) ↔ ∃g LeastAncestor(g).
10. `unique_root_of_connected_local` CU:137–145: same main hypotheses → one root exists and every root equals it.
11. `strict_descendant_of_nontrivial_field` CU:198–206: transitive r + LeastAncestor(g) + ∃a b r(a,b) → ∃x r(g,x). This is a non-reflexive graph consequence, not an interpretation into proper acts.

Dependency spine:
`P1 strict/transitive + P2 LocalCover → local roots → equality on edges → equality along P3 paths; P0 base picks an actual-domain witness → common cover/least ancestor/unique root`.

The author's field-existence proof chooses a source function using `Classical.choose` (CU:94–96). Its stored receipt lists `Classical.choice` for the common-cover/least/iff/unique-root theorems; the elementary root/edge/path results have empty axiom lists. The independent proof below removes even that choice dependency.

### Independent reviewer proof and a stronger alternate formulation

Namespace `ConnectedReview`:
- `reviewer_root_of_cover` RP:9–20
- `reviewer_edge_cover_eq` RP:22–33
- `reviewer_path_cover` RP:35–49: propagates a supplied single cover by induction, using local completion at the next node
- `reviewer_constructive_local_to_least` RP:51–57: obtains one cover at base, transports it to every x; no global selected source function
- `reviewer_least_unique` RP:59–67: two least ancestors coincide under strict/transitive r
- `reviewer_global_unique_supported_to_least` RP:69–80: ∃! root plus root ancestry of **every** node → least ancestor; no separate connectivity assumption needed

The stored reviewer receipt gives empty axiom lists for these core proofs. This is prior independent formal work, not a T20 discovery or implementation.

## 5. Exact ancestral-support characterisations

`local_cover_iff_unique_root_and_ancestral_support` CU:149–175 states for a fixed x, under strict transitive r:

`(∃g LocalCover r g x) ↔ ((∃!g RootAncestor r g x) ∧ ∀y, Below r y x → ∃h RootAncestor r h y)`.

The second conjunct cannot be omitted. Unique root ancestry of x does not guarantee that every other ancestor of x has any root ancestor. The reverse proof explicitly chooses a root h of each y and uses uniqueness at x to identify h with g (CU:167–175).

`local_iff_unique_root_ancestors` CU:177–196 states:

`LocallyComplete r ↔ ∀x, ∃!g RootAncestor r g x`.

This universally quantified equivalence can omit an explicit support conjunct because the same hypothesis applies to every ancestral y. Confusing the universal theorem with the pointwise theorem would recreate the precise already-repaired error. RP:82–114 independently proves the two pointwise directions.

## 6. Existing countercontrols and their exact force

| Control | Exact result and locator | What it blocks |
|---|---|---|
| Two-root merge | CU:210–230: strict transitive Merge on Fin3, connected, roots 0 and 1, no local cover of 2; all nodes can be labelled necessary CU:248–252 | Connectedness, activity, strictness and necessary-existence labels do not imply P2 or unity. |
| Split components | CU:232–246: LocallyComplete Split, no least ancestor, disconnected | P2 alone does not reach a common source across disconnected domains. |
| Singleton | CU:254–258: LocalCover of () by itself under false relation, no strict descendant | Reflexive self-cover is not self-production or actual productive participation. |
| Empty field | CU:260–271: vacuous LocallyComplete and Connected with no least witness | Nonemptiness cannot be dropped. |
| Infinite Fork | IR:10–23: ground→target; each branch n→target; branch m→branch n iff n<m | Genuine countable unsupported branch, not finite truncation. |
| Fork's one root | IR:41–61: only ground is root; target has unique root ancestor | Even these can coexist with incomplete target ancestry. |
| Fork's missing cover | IR:63–91: target has no local cover; connected field with unique root has no least ancestor | Unique root plus connectedness is weaker than complete coverage. RP:189–195 locates missing support inside target's own cone. |
| Nontransitive chain | RP:116–138: irreflexive 0→1→2, locally complete and connected but no least ancestor | Omitting transitive ancestry changes the theorem. |
| Non-strict relation | RP:140–146: universal Bool relation has two distinct covers and no root | Irreflexivity is material to roothood/uniqueness. |
| Dropped predecessor | RP:148–154 | A root in an induced/truncated field is not necessarily a root in the actual relevant field. |
| Rooted non-well-founded ancestry | UG:107–141 and RP:156–187: none precedes all some n; subordinate reversed-natural chain; least/covering root exists, global WellFounded fails | P00096 is correct: no global well-foundedness/temporal first event is required. |
| Bare graph versus act bridge | RP:197–210 | LeastAncestor does not establish a separately interpreted HistoryComplete predicate. |

These are implication counterinterpretations. The source explicitly declines to certify their metaphysical realisability (IR:3–6; UG:3–6; CR:75,85).

## 7. Actual participation and the retained act-accounting theorem

The mathematically precise actual-productive-witness layer predates Sixth and is imported unchanged as PC. It has distinct types S (source), M (mode), X (target), unlike the single-node-type graph.

PC:19–33:
- `HistoryComplete complete modeOf accounts := ∀s x m, complete s x → modeOf x m → accounts s m`
- `UnborrowedActs proper accounts := ∀s t m, proper t m → accounts s m → s=t`
- `ProductiveWitness complete modeOf proper := ∀s x, complete s x → ∃m, modeOf x m ∧ proper s m`

`proper s m` means this source's particular unborrowed proper exercise (PC:6–9); `accounts` means ultimate productive accounting, not merely an intentional owner, thought ownership or propositional entailment.

`uniqueness_of_history_complete` PC:35–43 proves complete(s,x) and complete(t,x) imply s=t under those three displayed hypotheses. The proof takes t's actual proper mode, includes it in s's account by history closure, and applies UnborrowedActs. Actual participation is doing work; two merely counterfactually sufficient conditions are not enough.

`uniqueness_of_universal_activity_scope` PC:45–56 proves uniqueness under universal accounting of all proper modes and an actual exercise for each source. Connectedness is unnecessary when that stronger universal scope is already independently granted. It must not be imported into a local-field argument without its additional universal premise.

`endpoint_sufficiency_does_not_give_history_closure` PC:60–76 supplies actual witnesses and unborrowed mode accounting for two endpoint-sufficient candidates while HistoryComplete fails. Mere ability to reproduce the endpoint cannot replace complete actual-history accounting.

**Critical boundary for the T19 DAG:** CU does not instantiate PC's predicates; importing PC does not prove such an interpretation. CR:41 and RP:197–210 explicitly preserve this boundary. Neither an actual strict productive edge nor a generic act owner is automatically a `proper` unborrowed original exercise.

## 8. Prior necessity and essential reception results relevant to bearer qualification

SI owns the exact definitions (SI:16–37):
- `Received dep w x := ∃y, dep w y x`
- `Root ex dep w x := ex w x ∧ ¬ Received dep w x`
- `Necessary ex x := ∀w, ex w x`
- `UniformRoot ex dep x := ∀w, Root ex dep w x`
- `GenericReception ex dep := ∀x, (∃w, Received dep w x) → ∀v, ex v x → Received dep v x`
- `ActualReceptionPreservation ex dep actual := ∀x, Received dep actual x → ∀w, ex w x → Received dep w x`

This modal Root is not definitionally the graph Root: it additionally demands actual existence, and its relation is world-indexed.

Exact implications:
1. `necessary_of_actual_root`, SI:39–48: actual Root(x) plus `∀y, ex actual y → ¬Necessary ex y → Received dep actual y` yields Necessary(x).
2. `uniform_of_necessary_actual_root`, SI:50–59: same actual Root(x), Necessary(x), GenericReception → UniformRoot(x).
3. `uniform_of_contingent_reception`, SI:61–67 composes the two for the same x.
4. `local_transfer_iff_uniform`, SI:69–82: given actual roothood and necessary existence, object-specific backwards reception transfer is equivalent to the uniform conclusion. This is an explicit warning against treating a restatement as independent warrant.
5. `generic_of_fixed_origin`, SI:84–92: stronger fixed-parent origin transport, with existing dependency targets, entails generic reception. The converse is false.
6. `predecessor_free_of_coverage`, UG:20–29: strict Coverage plus irreflexive/transitive r gives predecessor freedom without WellFounded.
7. `uniform_of_complete_coverage`, UG:31–44: actual presence of g, strict complete coverage at actual, strict/transitive actual relation, contingent reception and GenericReception produce UniformRoot of that same g.

Controls:
- SI:98–111: actual-only reception preservation is too weak for an actually unreceived root; the root can receive at another world while necessary existence remains.
- SI:113–123: GenericReception allows parent identity to vary. It is **not** general transworld origin-essentiality.
- SI:125–137: generic reception allows a cycle in the union of possible dependencies despite per-world acyclic examples.
- SI:139–149: reception doctrine alone does not make an actually unreceived bearer necessarily existent.
- UG:49–105: genuinely infinite rootless contingent chain can satisfy contingent reception and GenericReception; alternatively every node can necessarily exist and still receive. Neither reception premise supplies foundation or independence by itself.

Written prior owner: `theory/lineages/h-modal/orthability_modal_grounding.md` Theorem 1 at 177–192 gives necessary actuality in a complete well-founded actual ancestor cone; 210–220 explicitly says a root is enough and global well-foundedness is only one sufficient source of one. Its Proposition 2 at 761–765 proves a universal unique root under well-founded upstream-directedness and credits the prior finite-DAG version to Deep J. Sixth's exact gain is the distinct local-complete/connected factorisation without global well-foundedness, not discovery of every common-root argument.

The formal modal conclusion is source-independent logic conditional on the represented alternatives. It does not itself establish the metaphysical domain, actual contingent reception, essential reception, relevant attributes or qualified-perfect-source status in T19 P00097.

## 9. Sixth onward written refinements directly relevant to the join

No matching later Lean modules using `HistoryComplete`, `UnborrowedActs`, `GenericReception`, `LocallyComplete`, `ConnectedUnity` or `RootAncestor` were found in `experiments/orthemology-v5-successors/source-store/**/*.lean`. This is a bounded search result, not a claim to have read every unrelated successor Lean source.

Two later full papers were directly read because they sharpen the needed productive interpretation:

### Eleventh: original provision and constitutive possession

`experiments/orthemology-v5-successors/source-store/bef95a0a2b0774ad36c8e42d9070968a95b14811434bc0c6affa3ec3eeff7532/ARTICLE.md`

- 13–23: if a covered actual receiving mode consists in reception through b's exercise, that indispensable efficacy belongs in a complete original account. This is neither logical entailment nor identity of receiving mode with intrinsic act. It does not establish that a bearer satisfies the standard or every history has singular completion.
- 27–40: exclusion of donated unborrowed efficacy does not, without more, establish exclusive subjecthood for every proposed constitutive co-possession. A proper source-intrinsic exercise's subject-indexing has substantive positive rationale.
- 52–70: distinguish source bearer, power, manifestation, common event and proper source-intrinsic act; sharing an event or power does not establish one shared original exercise. Required tests include distinct bearers, same token proper exercise, original possession, full-origin accounting and one fixed identity relation.
- 82–88: warranted local original-supply reason retained; no actual P1/P2 closure, necessary participant or certified original co-owner.
- 94–96 credits prior dependent-mode and whole-token work (original SHA256 `c40202c1…` and `5f98f3dd…`). The paper explicitly adds no code/formal model at 102.

Review owner: `experiments/orthemology-v5-successors/source-store/4ebbfc029eed5f74f529092cff8648fe7c6ce8bbdda0446e4ae84f1ec7102e9a/ACCEPTANCE_v1.md`; registry entry `D15-T11-ACCOUNTING-BRIDGE` retains candidate-specific warrant-assessment scope. This is historical philosophical/interpretive credit, not a new kernel bridge to CU.

### Eleventh: composition and the original productive bearer

`experiments/orthemology-v5-successors/source-store/270004e117a99a58d7619ec25b372c0a4652070ee2c8e2b3c27d44c4e6e4fe16/ARTICLE.md`

- 17 separates later upstream P1 whole-origin completion, P2 particular bearer, N2/N3 same-bearer existential explanation/necessity.
- 49–72 applies the retained PC theorem: an original member's mode cannot remain proper and unborrowed while a distinct whole is assigned full ultimate accounting for it under the same relation. One member suffices; no finite cardinality or temporal first-member premise.
- 76–100 preserves four alternatives: genuinely original whole with derivative members; narrower whole joint role; intrinsic aspects rather than separate source-bearers; or a newly defended accounting relation.
- 124–132 says actual singular identification requires no extra personal name, but a singular noun cannot convert plural productive contribution into one bearer.

Review owner: `…/243bd1ee52efbac0b7c0637eadf6dd2f1d6a0a7d1a8e8babc73461f1a8455ffc/ACCEPTANCE_v1.md`; `D15-T11-ACTUAL-BEARER` is a conditional attribution/assembly limitation, not a general impossibility proof for composite sources. T19 P00097's statement that a holistic original does not make every component original is consistent with this boundary.

The through-T16 candidate registry continues to distinguish argument custody from actual-world closure. `docs/decisions/0039-v5-tranches-07-15-successor-layer.md`:18–29 preserves original statement/obligation owners; 64–69 retains source-specific philosophical premises. `groups/t16-successor/CLAIM_MAP.json`, row `T16-SOURCE-ASSESSMENT`, explicitly withholds independently warranted world-directed unity/necessary-being deduction and fresh T16 kernel qualification. T19's later affirmative defeasible appraisal must be represented as its own philosophical judgement, not retroactively relabelled Sixth/T16 formal proof.

## 10. Recommended dependency-node boundaries for the overall reconstruction

Keep these nodes separate:

1. Actual admitted productive occurrence / actual field inhabitants.
2. Complete actual-origin account, including relevant branches and historical contributors.
3. Original-bearer existence and qualifications; each candidate must meet the same conditions.
4. Faithful occurrence- and respect-indexed strict ancestry; explicit transitivity/irreflexivity.
5. CND appraisal against primitive duplicate entire original production.
6. Strong actual-source-mode/perfection norm against differentiated foreign completion.
7. Faithful mediate attribution preserving original contributions through derivative action.
8. **Application bridge:** items 1–7 really provide `∀x∃g LocalCover(g,x)` on the same domain.
9. Productive connectedness of that domain.
10. Existing Sixth local-to-common mathematical theorem.
11. Actual productive/act interpretation, not reflexive coverage alone.
12. Modal continuation: actual presence, contingent-reception and essential-reception premises for the same identified bearer, separately from field unity.

Existing formal work warrants arrows from explicit P0–P3 graph premises to common cover/unique graph root, and from explicit PC/SI premises to their own identity/modal conclusions. It does **not** warrant an unlabelled arrow from CND, bare necessity, source perfection or connectedness alone to P2. The T19 join must explain why the metaphysical premises cover all relevant ancestors at every node, preserve the same productive relation and bearer identity, and supply actual sourcehood. These are the precise application obligations to audit, not reasons to rerun already-owned elementary graph proofs as if new.
