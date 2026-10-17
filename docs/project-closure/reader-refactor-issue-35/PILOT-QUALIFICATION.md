# Issue 35 — pilot qualification and preview boundary

**IN PROGRESS. This record does not declare the full refactor, C02 independent acceptance or C03 complete.**

## Ruling: test the selected page structure before bulk curation

C01's complete tracked denominator has now been routed through the scoped discovery owners in [OWNER-MAP.json](OWNER-MAP.json). The map covers every baseline path, including earlier continuations and AR8R; it does not claim that every contained scholarly work has been semantically classified. The representative [CROSSWALK.json](CROSSWALK.json) binds the work/edition cases and intellectual routes already read in [PILOT.md](PILOT.md).

Ruling: author a **representative six-page reading preview** at the agreed reader paths to exercise C02's actual design. This is the small pilot before C03 bulk curation, not a claim to have completed the comprehensive mapping or a waiver of it. Every page must carry an explicit partial-preview boundary. The root README, STATUS and other current entrances remain unchanged; they must not present the preview as the complete new default. No new per-work directories, website platform or scientific IDs are introduced.

If a separate reviewer rejects this design, revise the small sample before extending it. Do not discard the existing source reading or rewrite original arguments. The final promotion and complete coverage remain C03/C05 obligations.

## Exact additional admitted paths

| Path | Pilot purpose |
|---|---|
| `docs/reader/RESEARCH-ATLAS.md` | Subject-oriented routes through the source-read sample, with the twelve-avenue owner preserved and incomplete breadth explicit. |
| `docs/reader/PAPER-CATALOGUE.md` | Representative works, all six governed rendering relationships and preserved-edition distinctions. |
| `docs/reader/RESULT-INDEX.md` | Selected result-level routes plus declared collection owners; no automatic theorem extraction. |
| `docs/reader/CURRENT-FRONTIERS.md` | Source-bound sample of unresolved questions and already advanced historical frontiers. |
| `docs/reader/APPLICATIONS.md` | Explain the sample's uses and required interpretation, not inferred human-cognition validation. |
| `docs/reader/VERIFICATION-GUIDE.md` | Inspection/replay routes and editing ownership; commands and claims must match available tools. |
| `docs/project-closure/HISTORICAL-STATUS-INDEX.yaml` | Add only the missing Issue-35 candidate-record classification required by the existing review-state gate; preserve all prior rules and vocabulary. |

These paths extend the existing allowlist only for this sample and its necessary integration. Scientific payloads, original proof code, historical reviews, governed PDFs and permanent CI remain protected.

## Observed integration defect and repair

The original PR checkpoint's full CI run `38316950544` completed with failure at the existing review-state gate; later checks were skipped. It had passed provisioning and earlier checks, but was not full-CI success. Local reproduction identified the actual defect: the new files under the Issue-35 closure directory had no classification in the historical-status index.

The bounded repair adds that exact directory prefix with the existing `current-candidate` status and a note excluding independent sign-off, complete corpus coverage, merged current state and scientific acceptance. It does not alter the review-state validator, a historical body, any previous classification or the global review-state wording.

Observed local control: the original index fails; the added rule passes; removing only that rule reproduces the same classification failure; restoring it passes. These are Python 3.13.5 author-environment observations, not the eventual pinned-interpreter full CI result. The failing earlier run remains in history.

## Qualification to record

Record the exact candidate and source bindings; positive and negative mechanical controls; paired source-based intellectual answers; local rendered-page and navigation observations; unresolved review/coverage limitations; and the observed generator/CI results. A mechanically passing crosswalk can still have a misleading explanation. The later record must demonstrate that limitation rather than claiming that hashes or keywords establish scholarly fidelity.

## Recovery 03 — tested reader candidate, not whole-corpus completion

The failed response left a real saved head, `a3290bb16d68e3b8c6f5764e83f8679001bf4e81`, tree `355b080ae21e186272e08de849a2c2840777d647`, containing the six previews and the additional maps/checks. Recovery reproduced that exact tree from the preserved baseline and a hash-checked patch; all 31 recovery members and 26 commit bodies matched. The [recovery run](https://github.com/theislampill/orthemology/actions/runs/38324978431) transports public Git objects only. The earlier input archives were not changed.

The saved full PR run `38322079165` failed at hygiene and skipped subsequent gates. Local reproduction identified a stale release-manifest hash for the historical-status index changed in the preceding continuation. This is a missing generation step, not an exception to the manifest or review-state requirements. The first current recovery runs reproduced ten census tests and twenty-eight pilot tests successfully; they did not retroactively turn the failed PR run into a pass.

### Mechanical controls and maintenance finding

Four added negative controls exposed actual false passes: modifying a scientific source and updating its local crosswalk hash together; changing its executable mode; naming an unknown reading form; and pointing one work's governed rendering to another work's PDF. The repaired checker compares science against the independently pinned Git object and mode, as well as the editorial hash, and reads rendering ownership from the existing publication profile.

Actual section-to-source routes are now checked for all seven journeys. Wrong or absent source fragments, a valid but different source, a source link moved outside the promised section, missing/duplicate journeys, symlinked targets, and a fenced link decoy are exercised with real Markdown parsing. The corpus contains no fake replacement science; all mutations use temporary fixtures. A source hash or HTTP-like successful target does not establish a correct reading route.

The initial route/source regression run had seventeen expected failures among forty-six tests. After repair, forty-seven passed normally and with optimisation. A test setup initially expected an active error for a `file:` link; CommonMark suppresses that link. The corrected control tests both the resolver's rejection and the lost promised source route. This does not weaken the source requirement.

M01 then found a genuine design defect: a second properly governed PDF was rejected unless it became another work. Three maintenance controls brought the suite to fifty tests, with one observed failure before repair. The checker now allows additional `reading_forms` to name their existing publication `artifact_id` while retaining a single scholarly work. Each edition must target its own PDF; the union of its profile-owned components remains discoverable. The legacy work-level artifact ID is still supported. Missing editions and wrong PDF targets still fail.

After this change all **50 pilot tests passed normally and under optimisation**, and the actual representative crosswalk plus six-page route check passed. The corresponding ten census tests are separate. These are author-environment Python 3.13.5 observations, not the pinned CI run. An unrelated terminal/startup message after some invocations is not clean-room evidence. Recorded execution of these tests is not all eighteen RLGWO controls or independent review.

**Maintenance footprint:** M01's fixture changes its actual publication owner, adds the synthetic rendering and attaches a reading form to the existing work; it does not add a work or rewrite atlas/frontier/application prose. M03 and M05 have bounded discovery/source-drift controls. Full M01–M05 contributor exercises, especially repeated-checkpoint work equivalence and scientific-owner update impacts, remain to be qualified against the eventual complete catalogue.

### Source-based answers and paired adverse readings

The paths and exact hashes below are the existing keys in [CROSSWALK.json](CROSSWALK.json), not new source acquisitions or scientific IDs. The earlier reading record remains intact. This continuation examined the named passages to check and improve the reader explanations; it did not authenticate every quoted primary volume or rerun research scripts.

| Route | Source passages examined and answer retained | Adverse reading rejected by those sources |
|---|---|---|
| J01–J03 | Existing manuscript/component and publication-profile bindings; the complete lineage relationship note. The formal PDF has two components; the decisive PDF and differently titled TeX remain related without an established exact build. The current main exposition does not automatically incorporate later work. | Counting Markdown, generated TeX and PDF as separate discoveries; silently dropping a composite component; claiming exact edition equivalence from title or abstract similarity. |
| J04 | `coordination` section 5 and its `twelfth` collection statement retain a sharp fixed-horizon bound under complete mediation. The source is readable as mathematics without a PDF. | Treating short program text as the entire mediator or interpreting a retrospective fixed-horizon construction as an already realised forward-causal controller. |
| J05 | `sound` sections 1–2, 4.1–4.2 and 5; relevant concrete/sound distinction passages; `retained` sections 1–5 and 7. Recognition can be basic in the account, reasoning can clarify/remind/remove obstacles, and wider non-collusive concordance has a cognitive-vindication role beyond report counting. | Reducing the account to transmission metadata, requiring an endless prior proof for every recognition, turning source assertions into a fresh cross-cultural survey, or inferring impaired cognition from disagreement. |
| J05 foundational step | `retained` section 2: a wholly received productive field is not supplied with an unreceived productive basis merely by collecting received members, even without a first temporal member. Actual cooperation is not denied. The report distinguishes a bare Necessary Being route from identification of the actual common Creator while retaining its later affirmative appraisals at their recorded scopes. | A weak-parts/weak-whole fallacy, a generic ban on every infinite sequence, automatic world-identification from a mathematical model, or erasure of the later positive appraisals under a blanket unresolved label. |
| J06 tensor | `tensor` statement/conventions and start of its hierarchy; `coercive` Theorem G and sections 5–7. The coercive successor supplies ordinary conditional mathematics beyond the predecessor's older quadratic/SOS bridge. Complete-path uniqueness is distinct from initial-moment ambiguity. | Calling the stronger coercive result still merely proposed, claiming finitely many positive-semidefinite checks satisfy every-polynomial positivity, or equating the moments with measured human cognition. |
| J06 Fisher | `fisher` sections 1–3 and 9–11; the complete `sidecar` corollary. The full-source Fisher metric and discarded weights affect gradient dynamics. The two weight vectors in the result entry preserve the same mixture but give different velocities. The fixed-fibre corollary preserves selected ambient norms, not a gradient intrinsic to a fibre with fixed conditionals. | Treating a fixed-fibre coordinate count as a global changing-rank chart theorem, replacing full-source preservation with a weaker posterior-only contract, or interpreting numerical decrease as epistemic warrant. |
| J07 | Complete `join`, `missing` report and `occurrences` JSON. Two complete occurrence tuples do not license their Cartesian marginal combinations; incomplete rows are not wildcards. Sharp missing-outcome extremes require joint feasible completions. | A generic twelve-avenue link without an actual contribution; treating source-relative tuples as new Arabic authentication or as evidence of actual statistical dependence; assuming coordinatewise possible endpoints are jointly attainable. |

The affirmative foundational explanation was added because the recovered preview named that route without adequately explaining its productive-adeququacy step. The Fisher entry now includes its actual metric, numerical counterexample and precise meaning of a flow projecting consistently. These are source-bound reader repairs, not new scientific conclusions.

**Semantic countercontrol:** the temporary page fixture was changed from a conditional construction to a claim proving all real human cognition correct. It still passes the mechanical links/bindings check. That deliberately observed false friend demonstrates why T16–T18 and A06/A13 require source-based adjudication. The author's adverse-reading analysis above is not the independent review still owed under C05.

### Rendered presentation and route observations

Chromium rendered all six pages at 1440×1080 and 390×844 in an offline CommonMark/table preview. The resulting desktop/mobile contact sheets were visually inspected. The old mobile evidence table placed its qualifications outside the visible column; it was replaced with paragraphs. Wide collection tables became sectioned reading routes, and the mathematical display lines were shortened without changing their meaning. All twelve rendered page/viewport combinations had document width equal to viewport width. The result equations and collection qualifications no longer require horizontal scrolling; two long verification command blocks remain intentional scroll regions.

The seven declared journeys had eighteen source endpoints checked in the rendered DOM and against local target bytes/anchors. Non-PDF targets were rendered locally; PDF targets received identity checks only. This is not a PDF visual review or a scientific replay.

The original attempt to navigate localhost was blocked by browser policy before the first page. The offline renderer did **not** bypass that policy. Its `set_content` observations are therefore **not hosted HTTP navigation, GitHub pixel parity, independent reader comprehension or C06 public readback**. Those remain explicit checks for the subsequent reviewer.

### Bounded CI admission and remaining gates

Ruling: add one read-only reader-pilot step to `.github/workflows/validate.yml`, using the existing dependency lock and interpreter. Its commands run the census/pilot suites normally and under optimisation plus actual source/reader binding validation. The existing scientific, privacy, source, current-state and PDF steps remain unchanged and required. This is the narrowly necessary C04 integration already within the RLGWO scope, not a new workflow platform or a semantic-acceptance badge.

The local existing dependency suite ran fifteen cases: fourteen passed and `test_python311_transitive_backport_is_exactly_pinned` failed because the author interpreter is Python 3.13.5 and the test requires a version below 3.13. That test and the pinned CI interpreter remain unchanged. This environment failure is reported, not relabelled as a successful full local run.

The temporary recovery workflow remains admitted only for transport, existing-generator reconciliation and its own removal. Exact-head pinned-environment/full CI outcomes must be recorded from observed GitHub runs; the local results above do not predict them.

C01's exact object population and discovery-owner routing are available. The 19-work/33-source crosswalk is still a representative slice, not all substantive work dispositions. C02 has an author-tested bibliographic/intellectual design with recorded limitations; independent journey acceptance is outstanding. C03's full semantic crosswalk, broader avenue treatment and root/navigation consolidation remain unfinished. C04 has these specific tests and M01 repair, not complete maintenance qualification. C05 and C06 remain unexecuted. The next implementation should reuse these source readings and resolve the remaining coverage, not restart the mathematical programme or mark the RLGWO closed.
