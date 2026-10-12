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
