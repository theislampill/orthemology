# Fixed channels, positive instruments, and tensor-likelihood closure

Portable, additive research evidence, 10 October 2026. Author and independent-review packets are preserved byte for byte. These are ordinary mathematical proofs and finite exact controls, not a formal audit or proof-assistant certificate.

## Results preserved

- Fixed finite passive channel: a nonempty closed convex law family is stable under every defined outcome exactly when its extreme laws are supported within equal-outcome-column blocks. The packet also gives the minimal stable hull and the repeatable-observable crosswalk. This is a global outcome-wise condition; one-prior feasibility and finite posterior reachability are different contracts.
- Proper finite cones: identity-summing positive instruments act by scalar reweighting on canonical indecomposable summands. The cone/instrument transport keeps admissible operations explicit: an intrinsic positive feasible-cone map need not lift to one fixed passive diagonal likelihood about the original target.
- Proper interaction-moment hierarchies: exact passive probability-plus-retained-posterior update on the full law simplex permits only constant likelihoods, for both binary and nondegenerate finite product alphabets. Strictly positive posterior-only updates have the same obstruction; zero-supported likelihoods have the stated support-rank exception. The associated proper-order moment cone is indecomposable; full order recovers the orthant structure.

Independent reviews report no blocking defect under the stated hypotheses. The preserved author controls have 9, 16, and 13 groups; the respective independent controls have 7, 7, and 12 groups. Finite computations corroborate examples and boundaries, not universal theorems by enumeration.

## Provenance and the two cone versions

The current reviewed cone RESULT has SHA-256 `5c74c7086c038dce1be0e9098b42fce9cc4c7aee8670fe0ba682b50d780af5c0`. The unchanged tensor author instead binds `e9f9a5465aa9f6f03f789f852e87a9847f4aa8b5641866b8c293ad2c9a1bb086`. Running its verifier against the current cone therefore correctly fails the input guard.

Both byte sequences are retained. The earlier result is a hash-matching reconstruction by exact reversal of two recorded precision edits, not an independently retained historical snapshot. The delta packet preserves the reconstruction provenance and exact diff. Replay creates separate current-cone and historical-cone workspace trees and never overwrites either preserved evidence version. The frozen tensor author report is not edited. Its review clarifies “first-slot” to “first-order” and that the displayed six-dimensional closure presumes a nonconstant first-slot likelihood, for its multiplication operator or the binary channel {L,1−L}. An otherwise unspecified larger channel need not have that closure. “First-order” includes observables across all slots.

Established ancestry remains explicit: Bayes-plausibility/splitting and compact convex extreme-point arguments; the inherited H-Continuation invariant-observable/intertwining theorem; Loewy–Schneider's cone identity-extremality theorem and the Barnum–Wilce / Heinosaari–Leppäjärvi–Plávala componentwise results; Walsh/Fourier and stabilizing-algebra machinery. These are bounded new-to-packet deductions and applications, with no field-wide novelty claim. The underlying source-read scopes and accessible external source URLs are preserved; no unretained external PDF bytes or exhaustive literature search are implied.

## Files and replay

- `workspace/`: the seven named packets at their original workspace-relative paths, plus every direct local input required by their verifiers and declared source bindings. The historical replay workspace contains only the tensor author and its nine bound inputs, not a conjectural earlier full cone packet. Required reviewer snapshot trees remain intact.
- `SCOPED_INPUTS.json`: input roles, exact sizes/digests, read scopes, and historical substitution provenance.
- `ORIGINALS_BEFORE_AFTER.json`: source-file before/after hash evidence from preservation.
- `METADATA.json`, `MANIFEST.json`: precise scope, runtime, original package identities and every preserved file's size/digest. The outer archive receipt separately binds the ZIP and manifest, avoiding a self-hash claim.
- `replay.py`: integrity checks, three author verifiers, three independent-review control programs, the cone review's author snapshot, the tensor review's portable snapshot replay, and an expected-failure check for current-path cone drift. It compares recorded outputs byte for byte and verifies the preserved bundle is unchanged afterward.

Extract the ZIP into a new directory. From the extracted bundle, run:

    python3 replay.py --verify-only
    python3 replay.py --work-dir /path/to/new-empty-replay-destination

The destination must not yet exist and must be outside the extracted bundle. All writes are confined there. Python 3.10 or later and its standard library are sufficient; tested runtime details are in the outer receipt. No network, Git checkout, compiler, Lean build, or third-party package is required. `REPLAY_RECEIPT.json` and logs are written to the new destination. Fresh-extract replay evidence supplied with this archive records the exact archive hash it tested.

Older source-binding files are retained as bounded ancestry records; this package does not recursively preserve or rerun their historical dependency closures. No protected repository file is changed. The archive adds no empirical/actual warrant, physical realizability, epistemic or normative authority, metaphysical conclusion, integration approval, or T20 closure. Separately ongoing leafwise-geometry and source research are outside this frozen archive.
