# T20 tensor realizability: accepted ordinary-proof evidence

Preserved additively on 10 October 2026 UTC. This compact packet binds the accepted tensor continuation and its independent ordinary mathematical review. It is an evidence preservation, not final integration or a T20 closure decision.

## Exact accepted object

- Candidate: `evidence/tensor-realizability-extension-20261010/RESULT.md`
- Candidate SHA-256: `449a28007af5a4d372d95be4d8f961a3ac577e723760f7a352327a05d4b6e17a`
- Review: `evidence/tensor-realizability-independent-review-20261010/REVIEW.md`
- Review SHA-256: `448ace340a04d56aaa26b1cab0d7f720dcda56c3fe1a37bdff76c8375c30ad07`
- Recorded verdict: `PASS_ORDINARY_INDEPENDENT_REVIEW`.
- Finite exact evidence: 332 author controls and 147 separately authored independent controls. These counts are not a proof by finite sampling.

The complete author and reviewer directories are retained byte-for-byte, including the reviewer's author snapshot and original receipts. Seven additional single-file source anchors at their original relative paths make the unmodified independent checker replayable without the whole project baseline. They duplicate the inherited source bytes already bound inside the author packet. No other baseline files are included.

## Preserved conclusions and limits

For a finite-dimensional numerical vector with the full commutative-polynomial moment record:

1. Lower-bounded polynomial damping plus all-time representability exhausts admissible paths by fixed initial-law exponential tilts. Without coercivity, the underlying law need not be unique; the stated quotient records the exact ambiguity.
2. Coercivity gives full-vector positive-time determinacy and the initial-moment-fibre/path classification under the candidate's representability premises.
3. For quadratic damping, all-time positivity on every polynomial square dynamically forces realizability. The accepted sufficient extensions are the explicit sum-of-squares coercive certificate and polynomial-coordinate automorphisms with polynomial inverses.

The general-coercive extension was active, separate research at this preservation cut. It is excluded and unaccepted in this packet. The accepted theorem does not silently upgrade square positivity to realizability for every coercive polynomial. Its all-time-representability coercive theorem is a separate claim with different premises.

### Conditional negative-square semidecision

The candidate proves a conditional semidecision consequence under a known positive rational horizon (or infinity), promised exact quadratic hierarchy/normalization/regularity, and uniformly certified coordinate evaluation at rational times. A nonrealizable path then has a strict rational-time rational-polynomial negative-square witness, which a dovetailed certified search could detect.

This packet does **not** implement a generic detector. The two executable programs replay only their specified finite symbolic/rational controls. There is no total validity decision, witness-degree or detection-time bound, generic isolated-multisequence test, effective measure-reconstruction guarantee, or empirical claim. The predecessor's particular scalar counterexample search is not repackaged as such a generic implementation.

No Lean or other formal-kernel certification, field-novelty certification, noetic realization, metaphysical uniqueness, final integration, or T20 closure is claimed. Finite controls supplement the ordinary proof and review. The original sources credit the classical existence/determinacy input and specify that primary-PDF parsed text was inspected; no local source-PDF hash or screenshot verification is added here.

## Contents and provenance

- `evidence/`: the two original evidence directories and seven source-anchor files only.
- `SOURCE_BINDINGS.json`: source-relative paths, exact byte lengths and SHA-256 digests of every copied evidence file.
- `SCOPE.json`: machine-readable scope and exclusions.
- `replay.py`: integrity/receipt verification and fresh-copy finite replay.
- `INTEGRITY.json`: every other package file's size and SHA-256 digest. The archive and this manifest are externally bound by the preservation receipt; the manifest does not hash itself.

The archive is self-contained for these checks. Source anchors retain their original project-relative locations under `evidence/` specifically because the original independent checker expects them as siblings of its own directory. They are retained evidence copies, not writable links to the working project.

## Replay

Requirements: Python 3.12 and SymPy 1.14.0. Reference replay uses Python 3.12.14. No network, Lean toolchain, full baseline, or new research is required. The replay does not install dependencies.

1. Extract the archive into a new empty directory.
2. From the extracted package root, run:

   `python3 replay.py --verify-only`

3. To replay both exact-control suites in a new external output directory, run:

   `python3 replay.py --output-dir /absolute/path/to/new-empty-replay-directory`

   With no `--output-dir`, the script creates and reports a fresh temporary directory.

The script verifies the full file set and per-file hashes, both original receipts, the accepted candidate/review binding, all seven source anchors against both inherited copies, and every reviewer-snapshot file against the author directory. It executes the unmodified author and independent checkers in a fresh evidence copy, requires exit zero, exactly 332 and 147 checks, and byte-identical generated result JSON. It re-verifies that the extracted package remained unchanged. The output directory retains logs and `REPLAY_RECEIPT.json`.

Expected status: `PASS_SOURCE_BOUND_FINITE_CONTROL_REPLAY`.

## Custody and additive handling

Original accepted files, the seven inherited originals, and all preexisting archives are only read. Fresh copies receive generated replay outputs. The companion preservation receipt binds the archive, manifest, fresh replay receipt, and before/after custody record. Later research is neither awaited nor incorporated. No upload or publication is performed by this preservation task.
