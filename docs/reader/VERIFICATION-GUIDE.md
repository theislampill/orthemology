# Verification, source inspection and maintenance

> **C02 reader-design preview — partial coverage.** This branch tests the representative works mapped for Issue 35. It is not the completed C03 catalogue, a new scientific assessment, or the replacement for the current root guide. [Coverage and qualification](../project-closure/reader-refactor-issue-35/PILOT-QUALIFICATION.md).

[Atlas](RESEARCH-ATLAS.md) · [Works](PAPER-CATALOGUE.md) · [Results](RESULT-INDEX.md) · [Frontiers](CURRENT-FRONTIERS.md) · [Applications](APPLICATIONS.md) · [Verification](VERIFICATION-GUIDE.md)

## Choose the claim before choosing the check

A claim that a PDF matches its source, a theorem follows from stated assumptions, a finite test passes, and a philosophical interpretation is warranted needs different evidence. The repository preserves those distinctions in its publication, source, result and review owners.

| Evidence | What it can establish at its declared scope | What it does not establish by itself |
|---|---|---|
| Source identity / content hash | Which exact bytes were retained or compared. | Correctness, novelty, source reliability or semantic equivalence of different editions. |
| Written mathematical argument | A stated reasoning route under its assumptions, available for scrutiny. | Fresh kernel checking or empirical applicability. |
| Recorded formal compilation | The formal declarations and imports checked in the named environment. | Every surrounding prose claim, proposed application or metaphysical premise. |
| Finite controls | Observed behaviour for the actual tested cases. | A universal theorem or empirical validation of an unrun study. |
| Existing review | What the named reviewer/session examined and concluded at that time. | A fresh independent review of changed prose or this refactor. |
| Owner acceptance / repository merge | The applicable decision or integration event. | Automatic research closure, external peer review or validation of every component. |

The [result/evidence owners][evidence] and [T20 source recovery guide][recovery] supply the scope for concrete results. Do not replace that scope with one badge for an entire page.

## Inspecting a selected mathematical result

For the [finite-mediator bound](RESULT-INDEX.md#finite-mediator), read the statement, the complete-mediation assumption and the ordinary proof in the linked paper. A small controller program is not automatically the mediator that the theorem assumes.

For [tensor Theorem G](RESULT-INDEX.md#tensor-moments), distinguish the all-polynomial path assumptions from finite moment truncations, and the law determined by a complete path from the potentially nonunique paths of an initial record. The source's ordinary written theorem is not a Lean proof merely because the repository also contains Lean files.

For [the Fisher corollary](RESULT-INDEX.md#fisher-geometry), check the ambient norm identity in the controlling source as well as the corollary and its existing review. The fixed-fibre dimension result does not assert a globally minimal chart or that every posterior task needs the same information.

## Reading and editing a publication

Start with the [publication profile][profile]. It identifies the substantive sources, generated LaTeX and governed rendering relationships. The formal-reference PDF combines the core and multi-actor note; the notation gallery is a diagnostic reference.

Edit the substantive Markdown owner, not its generated LaTeX or PDF. This refactor does not authorise manuscript revision. The [publication-source review][publication-review] and artifact sidecars identify the existing source pin; do not repin a publication to the navigation commit merely to make it look newer.

The repository's existing full PDF check is:

```sh
python scripts/build_pdfs.py --check
```

It requires the declared publication toolchain and infrastructure; the command's presence here is not a claim that it ran in this authoring environment. It checks governed artifacts, not the differently qualified preserved lineage PDFs. The [lineage note][lineage] explicitly leaves the decisive-revision PDF's exact TeX build relationship unresolved.

For citation identity and commit-specific references, follow [Citing this repository][citing]. A reader page must not invent a DOI, author identity or publication acceptance.

## Inspecting or exporting repaired T20 sources

The [source recovery guide][recovery] documents the maintained resolver:

```sh
python -B scripts/resolve_t20_v6_source.py find tensor-realizability
python -B scripts/resolve_t20_v6_source.py resolve 449a28007af5a4d372d95be4d8f961a3ac577e723760f7a352327a05d4b6e17a
```

These find and resolve the exact declared public source. They do not execute its proof or confer new scientific evidence. The guide also documents isolated formal-suite export and its pinned Lean/Mathlib requirements. Follow that actual source-recovery contract, rather than assuming a historical relative command refers to the current checkout.

Held or unavailable identities remain held or unavailable. A public manifest row, transformed locator or archived command is not permission to reconstruct private research or pretend a missing historical execution was observed.

## Checking this reader pilot

From the repository root, with the existing locked Python dependencies:

```sh
python -B tests/test_reader_census.py
python -B -O tests/test_reader_census.py
python -B tests/test_reader_pilot.py
python -B -O tests/test_reader_pilot.py
python -B scripts/check_reader_pilot.py
```

These checks compare the representative crosswalk with its bounded candidate/owner population, bind exact sources, preserve composite and edition relationships, and reject specified omissions and mutations. **They do not establish complete work coverage or semantic fidelity.** A misleading explanation with valid source links can still pass mechanical checks; source-based reader review is therefore required.

The optimisation runs above apply to these new validator tests. They are not an instruction to run historical scientific scripts under optimisation: assertion-based controls can lose checks in that mode, as the source recovery guide warns.

The [pilot qualification record][qualification] separates actually observed runs, local rendering, existing evidence, remaining review and the complete RLGWO acceptance predicates.

## Maintaining the reader layer

The work catalogue is the primary editorial home for a work's description and edition presentation. The atlas explains subject relationships; the result index locates claims; frontiers discuss the relevant open question; applications explain a use and its additional assumptions. They should not independently maintain competing status or edition lists.

For a new rendering, update the actual publication/edition owner and the corresponding catalogue route. For a changed statement supporting a synopsis, review that synopsis and its exact source binding. A source change must not silently leave an old interpretation labelled current; an unrelated change need not rewrite every page.

Stage admitted new files before running the existing generation owners:

```sh
python scripts/generate_current_state.py
python scripts/make_manifest.py
python scripts/generate_current_state.py --check
python scripts/validate_current_state.py
python scripts/validate_review_state.py
python scripts/validate_internal_references.py
```

These are selected integration checks, not a substitute for the complete [.github/workflows/validate.yml][ci] contract. Preserve the authored state, existing scientific owners and all required gates. [Decision 0014][decision14] explains the source-digest and convergence rules. A passing pilot or a populated set of headings is not the final refactor.

[profile]: ../publication-profile.yaml
[lineage]: ../../theory/lineages/h-ics-v5/README.md
[evidence]: ../provenance/v5-successors/EVIDENCE_BINDINGS.json
[recovery]: ../../research/t20-v6-20261012/SOURCE_RECOVERY.md
[publication-review]: ../provenance/v5-consolidation/PUBLICATION_SOURCE_REVIEW.json
[citing]: ../CITING.md
[qualification]: ../project-closure/reader-refactor-issue-35/PILOT-QUALIFICATION.md
[ci]: ../../.github/workflows/validate.yml
[decision14]: ../decisions/0014-generated-project-state-and-whole-state-reread.md
