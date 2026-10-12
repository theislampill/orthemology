# Cumulative and sharp partial damping: intermediate evidence

10 October 2026 UTC. Additive preservation of two accepted ordinary mathematical results. T20 remains ACTIVE. Packaging and re-executing finite controls provide no new research-time credit. This archive does not replace earlier evidence.

## Start here

The two final proofs and their complete independent reviews are in `evidence/`:

- `cumulative-square-positivity-20261010/RESULT.md`, SHA-256 `a530a5341497e3416345a7ec325e986a7e54f2c254954f80fd32f1f596e6244f`
- `cumulative-square-positivity-independent-review-20261010/REVIEW.md` and `REVIEW_RECEIPT.json`: `PASS_EXACT_HYPOTHESES`, no unresolved defects
- `partial-quadratic-rank-classification-20261010/RESULT.md`, SHA-256 `d940d080eea86c0486e81219898c343c4e4c025f86e00cda209df3a3266a3288`
- `partial-quadratic-rank-independent-review-20261010/REVIEW.md` and `REVIEW_RECEIPT.json`: `PASS_NO_BLOCKING_FINDINGS`

The author-side contributions of the parent and investigators remain attributed in their unchanged proofs. The independent reviews are separate ordinary mathematical assessments, not blind reviews. Their receipts accept exact frozen bytes. Historical author receipts still have their original author-only or review-pending wording; the later review receipts establish acceptance without rewriting history.

## Accepted results and their distinct boundaries

The cumulative theorem V_c assumes a supplied continuous, locally bounded-degree polynomial energy schedule, a continuous scalar shift making each rate SOS, and a radial SOS certificate for the accumulated shifted energy from time zero to **every** positive time. Full polynomial-square positivity, normalization and coordinatewise C¹ regularity through time zero then yield a unique whole-path probability lift and positive-time determinacy. No initial representing measure is assumed. The finite backward Volterra expansion and cumulative certificate permit rank-one rates that fail instantaneous radial coercivity. No certificate regularity, common SOS-factor selection, or all-interior-window coercivity is added. A certificate only at a single terminal time is not sufficient for the stated theorem and is not claimed. The supplied polynomial-coordinate transfer is inherited and applies conditionally under the cumulative hypotheses; no general polynomial-flow completeness claim is made.

For fixed quadratic damping of rank r in dimension d, write k=d−r. The sharp rank theorem separates three questions:

- Automatic whole-path law existence for **every** admissible full-square-positive hierarchy holds exactly when k≤1. In that range, moment-coordinate continuation is unique in the admissible class.
- Universal identification of the law lifting an already specified path holds exactly when k=0. For k≥1, distinct full-support probabilities can have the same entire tilted moment record.
- For k≥2 there are global full-square-positive paths with no representing law at any time. The obstruction can be strictly square-positive at every finite time, and nonstationary when r≥1. Rank zero necessarily gives stationary paths.

These universal thresholds do not assert that every partially damped individual path is ambiguous. Failure of law identification is distinct from failure of moment-coordinate continuation uniqueness. General lower-bounded quadratics are treated by the stated invertible affine reduction, with a nonzero linear term in a null direction explicitly excluded.

The classical d−1 marginal Carleman existence theorem, all-marginal determinacy, one-dimensional Hamburger theorem, and the full infinite-dimensional square-positive nonmoment functional remain imported ordinary mathematical inputs. Finite algebraic scripts do not construct that infinite functional or prove the classical representation or analytic exhaustion theorems.

## Evidence retained without rewriting

All authored files from the four current packets are copied exactly, including duplicate reviewer snapshots, original controls, logs, receipts, bound inputs, source/reading records, and historical exclusions. Six source-body paths are represented by three explicit external artifacts, described below. `COPY_MANIFEST.json` records every copied file's original relative path, size, hash and role.

The cumulative review retains the original draft `inputs/candidate-RESULT.md`, SHA-256 `468dac5cdd3c4368c12cb7db2bb6cc7f5267b7dee8035d65911962e40042950d`, and `FINAL_DELTA.patch`. The final correction explicitly requires compact smooth spatial time derivatives for the generic family-test lemma and pins the source URL to v1. The application already satisfied the stronger test condition. Replay checks the exact draft-to-final unified diff; it does not hide or overwrite the draft.

All files of the small inherited V, polynomial-transport, tensor-realizability and fixed-coercive author/review packets are retained, along with the earlier moment-evolution comparison's result and input/source/reading manifests. Their earlier mathematical controls are **not** rerun or added to fresh counts. Their exact input snapshots preserve the inherited proof chain without rebuilding transitive campaigns. `HISTORICAL_RECEIPT_REFERENCES.json` classifies included members, required external source aliases, and any historical references outside this archive. This is bounded evidence preservation, not a promise that every source body or transitive campaign named in an old document is bundled.

The rank review's historical truncated-functional exclusion retains the old `Controls.lean`, result, independent review and seal. The zero continuation has Λ((x³−x)²)=−96. It is an exclusion guard, not the rank theorem's full-functional counterexample. It does not say every extension of the old truncated record fails. No Lean compilation is rerun; no archived Lean file becomes a new kernel claim here.

Negative mathematical controls remain in the unchanged current scripts and reviews: earliest-time versus latest-time Volterra order, instantaneous rank-one null directions, post-stop rank-one windows, wrong Gaussian killing scale, too-large mixture weight, two hidden directions outside the existence threshold, hidden-law ambiguity, and the separate full-functional nonmoment obstruction. Exact finite controls supplement the written proofs.

## External sources and runtime prerequisites

Complete modern primary PDF bodies, extracted source text bodies and full-page images are not redistributed. `EXTERNAL_PREREQUISITES.json` records the exact three excluded artifacts and six original author/reviewer paths:

1. Putinar–Schmüdgen, *Multivariate Determinateness*, arXiv:0810.0840v1, PDF SHA-256 `9e551b5856cdf1065f1170641bed91a1d0f40c1d19368c9187f0c3d16661ac94`
2. The original printed-p.24 PNG rendering, SHA-256 `03b3c10d228266fee98b8deb069527d5c3123d6beb4952dbc87b129f79c80424`
3. Its original extracted text, SHA-256 `5099deaec23494bfc716da1a416d06b3285127ab5494950edb351298c8c0003b`

The primary URL is https://arxiv.org/pdf/0810.0840v1 . Supply these exact files under `partial-quadratic-rank-classification-20261010/sources/` relative to an explicit external root. The wrapper reads them without modification and copies them only to disposable replay work. The three original derivative bytes must be supplied or reproduced exactly; a different rendering or extraction can legitimately fail the hash check. No retrieval, fresh reading or literature-priority research is performed here.

The classical textbook URL and precise historical reading limitations are preserved. No retained full-book byte hash or successful textbook screenshot is invented. The comparison's other primary source bodies remain outside this compact archive and are not executable dependencies of the four current scripts.

Runtime: CPython 3.12.14, SymPy 1.14.0, mpmath 1.3.0. These versions and the two package entrypoint hashes are enforced by `prerequisites/RUNTIME_PINS.json`; requirements are recorded separately. Python, packages and compatible OS libraries remain external. This checks versions and package entrypoints, not the entire interpreter/package distribution byte-for-byte. No automatic installation, network retrieval, dependency rebuild or Lean toolchain is used.

## Fresh portable replay

Extract the ZIP into a new directory, then run from its top-level folder:

    python3 -B replay.py --external-root /absolute/path/to/exact-source-root --output-dir /absolute/path/to/new-output

The output must be new and outside the immutable package. The wrapper rejects missing/corrupt sources, missing runtime packages, mismatched runtime versions, changed payload bytes, unexpected payload files, symlinks, an existing output directory, an output inside the package, and optimized Python assertion disabling. It does not silently skip missing provenance prerequisites.

The unchanged current programs execute in a fresh copied evidence workspace. Four regenerated JSON files must match the preserved originals byte-for-byte:

- Cumulative author: 118 checks, comprising 89 algebraic and 29 integrity checks
- Cumulative independent: 55 checks, comprising 54 algebraic and 1 integrity check
- Rank author: 1,232 checks, comprising 1,223 algebraic and 9 integrity checks
- Rank independent: 1,605 checks, comprising 1,591 algebraic and 14 snapshot-integrity checks; the algebraic checks include 1,309 Gaussian recursion cases

These are counts of executed finite checks, not counts of distinct theorems or disjoint discoveries. The rank review's sealed-file verifier also runs, separately classified as integrity work. Wrapper input, receipt, snapshot, source and correction checks are separately recorded. `EXECUTION_SCOPE.json` enumerates all archived Python programs and expressly marks inherited copies as historical, not rerun.

The replay writes full logs, copied work, regenerated outputs and `REPLAY_RECEIPT.json` only under the requested output. It rechecks packet and external-source hashes afterward. A failed or blocked run cannot report a successful result.

## Preservation receipts and limits

`MANIFEST.json` covers every payload file except itself; the archive SHA-256 covers it too. `preservation-evidence/` preserves a successful preliminary fresh-extraction replay and adversarial guard-test records. The initial receipt classifier mistakenly treated copied predecessor receipt member paths as relative to their copy placement. The recorded metadata-only correction resolves these via byte-identical canonical receipt origins. The initial classification is retained; all four mathematical control results were already correct and unchanged. `test_guards.py` reproducibly exercises missing/corrupt source, tampered packet, missing runtime, optimized-assertion, reused-output and inside-packet-output refusals without altering originals. The final external preservation receipt binds the finished ZIP hash/size, ZIP CRC check, fresh final extraction/replay, guard-test results, and before/after byte identity of the listed original files and earlier diffusion/polynomial archives and receipts. The external receipt avoids a circular archive hash.

No preservation step modifies original packets or protected repository files, integrates results, uploads material, closes T20, certifies field priority, supplies finite-degree realizability certification, or creates empirical/noetic conclusions. Source and proof checks here establish artifact identity and reproducible bounded execution; the accepted ordinary written proofs and reviews retain their exact mathematical status.
