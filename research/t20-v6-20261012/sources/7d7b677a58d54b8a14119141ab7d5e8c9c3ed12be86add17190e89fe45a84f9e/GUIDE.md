# Additive broad-correction research archive

11 October 2026 UTC. This is a small, additive preservation packet within active T20. It is not a consolidation of all T20, replacement of earlier packets/checkpoints, protected-repository integration, programme closure, or a field-priority certificate. Original source files were copied without rewriting their contents. The external preservation receipt records the archive hash, fresh extraction, replay results, and final unchanged-originals check.

## Read in this order

1. `matrix-rank-gaussian-entrance-20261011/RESULT.md`, then `matrix-rank-independent-review-20261011/REVIEW.md`.
2. `conditional-entropy-control-20261011/RESULT.md`, then `conditional-entropy-independent-review-20261011/REVIEW.md`.
3. `conditional-entropy-root-controls-20261011/CONTROL.md` for the sharp broad-class coefficient and the positive-probability fibrewise nonmonotonicity example.
4. `cumulative-warrant-primary-check-20261011/REPORT.md` for the bounded primary-source finding. Its `SOURCE_READS.json` states precisely what was visually read and which original sources are deliberately omitted.

## What is genuinely added, inherited, or corrected

### Matrix-rank entrance

The inherited full-law observed-marginal projection, its observed transport-flux correction, and the scalar Gaussian entrance are dependencies, not newly discovered results. This packet extends them to finite-dimensional centred Gaussian matrix data with fixed observed law N(0,I), a supplied positive-definite conditional target covariance, noncommuting matrices, and arbitrary conditional rank deficiency r. It proves strictly positive inflow on every initial null direction, unique global entrance within that Gaussian class, convergence to the supplied target, and the rank-dependent asymptotics det S ~ d0 t^r, KL = -(r/2) log t + C0 + O(t), and D = r/(2t) + O(1).

The curve length and time-changed finite-action statements are for this particular curve. They do not establish geodesic minimality or an endpoint-distance identity. The theorem does not claim all-law weak-PDE existence or uniqueness, a transfer under arbitrary whitening that preserves the Euclidean metric, or external authentication of the supplied target. The 15 root isotropic controls are supplementary scalar/product witnesses; they are separate from the noncommuting author and reviewer checks.

The review retains a source-attribution qualification: the compared Liero et al. paper discusses semidefinite precision matrices in Appendix B. Its positive-definite Gaussian-domain comparison must not be paraphrased as a claim that the paper never treats any semidefinite matrix.

### Conditional entropy

The product-target coercivity transfer and the dependent-target observed-score multiplier were already present in the two bound predecessors. The bounded addition combines these for a nonproduct, non-Gaussian conditional-coercivity theorem and identifies the exact nonnegative remainder: latent Fisher information, conditional reaction variance, observed-gradient remainder, and a coarse variance remainder. A uniform conditional KL ≤ C I/2 gives D ≥ 2E/C. Exponential decay follows only for an existing admissible projected-flow solution with the stated entropy chain rule or energy inequality. General-law existence, uniqueness, and singular entrance are not proved.

The dependent quartic and Cauchy-observed examples establish genuinely non-Gaussian functional-inequality scope without hidden joint coercivity. The logistic-tilt example retains both transport and reaction in a bounded-entropy obstruction while its target variance varies; it does not refute a fixed-target inequality. Target-marginal mismatch leaves a fixed coarse KL residual, so the decay is of excess conditional entropy; identifying projected fields additionally requires the coarse log-ratio domain assumption. The independent review is bound to the final author digest and found no blocking mathematical defect within that scope. Classical LSI and unconstrained SHK decay remain explicitly credited ancestry.

The separate root controls distinguish the broad smooth-law coefficient from a stronger coefficient on an inherited centred Gaussian subfamily. For the supplied scalar target N(0,T), independent observed and latent coordinates, and latent law N(m,s), the sequence m=n, s=1/n gives D/E -> 2/T. This is an instantaneous dissipation sharpness test, not a trajectory's asymptotic exponent. The root fibre example has positive conditional KL derivative near y=0 on a set of positive observed probability while integrated KL decreases. Global entropy descent does not imply descent on every fibre.

### Cumulative warrant primary check

The actual increment is fresh print-edition identity, exact printed-line locator, and continuous-context verification of previously recorded content in Darʾ 8:16–25, especially 8:20–21 and the first six lines of printed p. 21. It is not a newly discovered primary position, an additional philosophical warrant, a new joint-sufficiency criterion, or an evidential-independence condition. The valid content of alternative acquisition routes and the rejection of compulsory universal sequencing remain as previously recorded. The corroborative tawātur analogy remains El-Tobgui's interpretation. Existing affirmative warrant, operative-basing, and attribution distinctions are preserved.

Only the 10 files explicitly named in that packet's shareable `MANIFEST.json`, plus the manifest itself, are included. Its unlisted `VERIFICATION.json`, private source PDF/HTML/text bodies, page images, and full books are excluded. `SOURCE_READS.json` retains their hashes and exact reading boundaries as provenance; those omitted bytes and visual readings cannot be reverified from this archive alone. The retained prior-note and attribution snapshots are inherited evidence, not a fresh whole-volume reading.

## Evidence levels and count boundaries

- Analytic reports: ordinary mathematical derivations and stated functional-analytic assumptions, with source-bound independent review. These are not formal-kernel certificates.
- Mathematical controls: finite symbolic/rational corroboration and explicitly labelled high-precision numerical checks, including deliberately incorrect multiplier controls. They do not replace the general-dimensional proof or establish an all-law existence theorem.
- Source-reading records: bounded primary/contextual interpretation and attribution records. File hashes authenticate bytes, not the correctness of historical or philosophical interpretation.
- Preservation checks: archive file-set checks, hashes, freeze bindings, and replay equality. These are not new mathematical controls or source readings.

Matrix author: 31 reported checks = 27 mathematical controls + 4 predecessor-snapshot bindings. Matrix independent reviewer: 51 = 42 mathematical controls + 9 author-freeze/predecessor bindings. Matrix root: 15 mathematical controls. Conditional root: 9 mathematical controls. Counts are per execution, not added again for optimized runs. Duplicated predecessor snapshots and author replays are not independent results.

Conditional author portable replay: 42 checks = 28 author-labelled exact controls + 9 high-precision numerical controls + 5 copied-input bindings. The frozen 47-check author and reviewer-author-replay records additionally checked 5 external original paths; those 5 checks are intentionally excluded from fresh-extract credit. Conditional independent review: 30 separately authored exact controls, with no embedded input-binding count. The parent-supplied sharpness, per-fibre and logistic controls are participating contributions, not independent certification.

The full Bakry–Émery paper, full text extraction and page render are also deliberately omitted from the conditional author packet. No redistribution licence was verified. The unchanged original author manifest lists 18 files, of which 15 are delivered and 3 source bodies are not. `OMITTED_SOURCE_BODIES.json` lists these exact hashes and the 17 excluded source-check bodies/images. This delivery restriction does not erase or rewrite the original source reading, freeze, or review records. The reviewer’s earlier 18-file verification is historical evidence, not a claim that all 18 files are in this archive. Source URLs and reading boundaries remain available; archive replay does not repeat the visual source examination.

## Replay from a fresh extraction

Requires Python 3, SymPy, and mpmath. The recorded replay environment was Python 3.12.14, SymPy 1.14.0, and mpmath 1.3.0. The archive itself does not install software or access the network. In a shell, from the directory containing the archive:

```sh
ARCHIVE="$PWD/broad-correction-research-preservation-20261011.zip"
EXTRACT="$(mktemp -d)"
OUTPUT="$(mktemp -d)"
python3 -m zipfile -e "$ARCHIVE" "$EXTRACT"
ROOT="$EXTRACT/broad-correction-research-preservation-20261011"
PYTHONDONTWRITEBYTECODE=1 python3 "$ROOT/verify_archive.py" --output "$OUTPUT/manifest-before.json"
PYTHONDONTWRITEBYTECODE=1 python3 "$ROOT/replay_controls.py" --output-dir "$OUTPUT/controls"
PYTHONDONTWRITEBYTECODE=1 python3 "$ROOT/verify_archive.py" --output "$OUTPUT/manifest-after.json"
```

`replay_controls.py` uses normal and optimized Python subprocesses, puts all logs and generated outputs in the external output directory, verifies the recorded control counts, and compares normal/optimized outputs. Scripts that write beside themselves are run only from disposable external copies. The frozen archive payload is not a replay workspace. The runner's receipt lists the exact subprocess commands and classifies mathematical controls separately from source bindings. Both replay counts and limitations should be read before quoting a pass.

`MANIFEST.json` authenticates every included file except itself; its SHA-256 and the ZIP hash are bound by the external preservation receipt. `SOURCE_BINDINGS.json` additionally binds every copied payload file to its original workspace bytes. Nested author/reviewer freezes and the source packet's shareable manifest remain unchanged.
