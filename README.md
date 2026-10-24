# Orthemology

Orthemology investigates the conditions of correct judgement, adequate reasoning and production, warranted recognition, objective standards, and source-grounded correction. Its philosophical arguments, mathematical results, formal proofs and applications retain their own premises and evidence scopes.

## Read the research

| Question | Start with the primary source |
|---|---|
| How do correctness, evidence and correction fit together? | [The main paper](papers/correctness-reasoning-and-systems.md) |
| What makes things intelligible and genuinely evaluable? | [Orthability and the ground of intelligibility](foundations/orthability-and-the-ground-of-intelligibility.md) · [current foundational arguments](foundations/current-arguments.md) |
| What follows about necessary being, productive adequacy and divine attributes? | [Modal grounding](foundations/modal-grounding/orthability-and-modal-grounding.md) · [attributes and speech](foundations/orthability-divine-attributes-and-speech-athari.md) |
| How do proper function, recognition, warrant and correction relate? | [Concrete and sound reason](foundations/concrete-and-sound-reason.md) · [dynamic orthing and noetic learning](foundations/dynamic-orthing-noetic-learning-and-orthability.md) |
| What must representations retain for future inquiry? | [Continuation-complete inquiry](mathematics/continuation/continuation-complete-inquiry.md) · [information, composition and revision](mathematics/information-and-revision/information-composition-and-self-revision.pdf) |
| How are collective judgement and formal reasoning governed? | [Formal core](mathematics/formal-foundations/core-formalization.md) · [collective inquiry](mathematics/collective-inquiry/conflict-and-shared-standards.md) |
| What are the substantive applications? | [DAEE epistemics](applications/daee-epistemics/README.md) |

The [reading guide](docs/reader/START_HERE.md) covers the programme's twelve avenues. [Current science](docs/reader/CURRENT_SCIENCE.md) presents affirmative arguments with their premises and qualifications; [research frontiers](docs/reader/RESEARCH_FRONTIERS.md) distinguishes established results from genuine open questions.

These guides are generated from existing scientific owners. A preserved source, a correct file hash, an ordinary mathematical argument, a finite control, a kernel-checked theorem and a scientific adoption decision are different forms of evidence. See [status](STATUS.md).

## Find a complete work and its review

Python 3.11 or later is sufficient for ordinary source reading; no proof toolchain is needed.

```sh
python tools/corpus.py list --subject geometry
python tools/corpus.py search "necessary being"
python tools/corpus.py show --work "Finite-audit Fisher descent: exact criterion and sharp cardinality threshold" --include-status
```

The last command reads the complete selected primary texts and identified review, with the source-owned status. Use `--role reading` for the scholarly selection or `--output NEW_DIRECTORY` to save complete reading forms, including PDFs. Historical source-fidelity reports are available explicitly with `--role historical` or `--role all`. A missing controlling review is disclosed; it does not confer acceptance.

Source access verifies the exact edition against SHA-256 and Git blob identities. It can read retained Git history, an explicitly supplied verified cache, or the existing public source at its pinned commit. Reading does not silently reconstruct the old repository.

For deliberate offline reading, cache a named work:

```sh
python tools/corpus.py --cache ../research-cache fetch --work "Finite-audit Fisher descent: exact criterion and sharp cardinality threshold"
python tools/corpus.py --cache ../research-cache --offline show --work "Finite-audit Fisher descent: exact criterion and sharp cardinality threshold" --include-status
```

`search --full-text` reports the actual searched and unavailable populations. `fetch --all` deliberately caches the full public baseline (310,686,293 logical bytes); it is separate from an ordinary reading session. Source caches and restored proof environments live outside the ordinary checkout. Named `materialise` requires `--context reading` for a reading bundle or `--context replay` plus an explicit verified history source for a complete historical source workspace; neither choice executes a proof.

## Edit, reproduce and preserve

[Contributing](CONTRIBUTING.md) explains source ownership, new editions and review. The [reproducibility guide](docs/reader/REPRODUCIBILITY.md) separates reading, exact restoration, actual proof/experiment execution and publication.

```sh
python tools/corpus.py --help
python tools/replay.py --help
python tools/authority.py validate --root .
```

Historic paths and research labels remain resolvable as exact citations and replay inputs. Ordinary navigation uses the subject and argument. Original manuscripts, proofs, reviews, negative findings and historical source identities remain preserved.

The repository consolidation is being implemented and qualified through [R-0002](https://github.com/theislampill/orthemology/issues/38) and its [draft implementation PR](https://github.com/theislampill/orthemology/pull/39). That work reuses the completed reader refactor; it does not change scientific acceptance.
