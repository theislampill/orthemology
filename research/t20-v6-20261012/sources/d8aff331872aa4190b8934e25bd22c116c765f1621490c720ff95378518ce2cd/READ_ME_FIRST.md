# T20 Hessian Admissibility: consolidated research checkpoint

9 October 2026. **Intermediate research; T20 remains active.** Start here. The compact [integration index](../../PUBLIC_BOUNDARIES.md#recovered-reference-128) lists the exact result, proof and review files and hashes. The large historical source map is retained provenance and does not need to be read for initial review.

## Newly established, at the stated mathematical scope

For the inherited canonical field V_i(b)=(1−z)/f_i''(b_i) on the open cube, with z=Σ_i b_i:

1. **All-start interior safety, n≥3:** every interior starting forecast stays inside the cube for every finite forward time if and only if each lower derivative endpoint f_i′(0+) is −∞. Under this condition every start converges to an interior coherent point. For n=2 all admissible score families are safe, so the n≥3 restriction is essential.
2. **Safety and scalar closure together, n≥3:** all-start safety plus original-clock autonomy of the coherence sum holds exactly for q_i(t)=1/f_i''(t)=a t with a common a>0. Equivalently f_i(t)=t log(t)/a+β_i t+γ_i: scaled convex negative-Shannon generators up to coordinate-affine terms. Then z′=a z(1−z), the ratios b_i/z are conserved, and the limit is b⁰/z(0).
3. **Exact individual-start lifetime:** a shared dual-coordinate interval gives an exact interior-root criterion and, when necessary, a one-dimensional improper travel-time integral. A coherent boundary can be reached in finite time under the actual inherited Score assumptions; an explicit cubic/quadratic example arrives at (0,1/2,1/2) at log(3/2). Normalizing the field changes that arrival to infinite normalized time.
4. **Preserved clock-dependent predictive memory:** for the binary-log canonical field on the specified open incoherent chamber, exact original-clock coherence prediction requires n continuous real coordinates. The inherited normalized field needs only the coherence sum for that different clock. These are exact continuous-coordinate results, not bit, runtime or robust estimation bounds.

Here “scalar” means the coherence sum z, equivalently the signed defect z−1. It does **not** mean the squared objective (z−1)²/2 alone, which loses the sign. The joint result classifies the specified field and observable; it does not make convex negative Shannon entropy the unique safe metric, nor supply an operational noetic adapter.

All-start safety concerns this chosen correction field and domain; it is not a claim of geodesic completeness of the Riemannian metric.

## Reading and evidence

- [General admissibility proof](../2a180efeea5844c25c63a6b59e14ac9808a5cb9b7f01f26b05a04d2f9419c86f/GENERAL_ADMISSIBILITY_REVIEWED.md), especially §§6–7
- [Independent general review](../ab8a1741404fc0b59dd211257fe595ba6dd395824308748f6b93b68a0b75638a/REVIEW.md) and [frozen receipt](../../PUBLIC_BOUNDARIES.md#recovered-reference-131)
- [Prior integrated result](../abf6c6fede6b7f9e08ba3d469a9b0a0f97ec5b9d2ad12197d6383f226e912a94/combined-result.md), [scalar iff proof](../5ce54702491ebc4568841d8e198b0db2cd0fcc9f5b14b785e7be8a5a656a1624/scalar-projectability.md), [binary-log memory proof](../e82a8b652f32e79de65c7423eefa6dd0c1e96493818aeb0fefc0f8d4760b7d51/binary-log-memory.md), and [dual-flow/boundary report](../679e3049b498c19a0d9982ef30dc7a34483871dfdf21178dad1b45004485bb58/dual-flow-and-boundary.md)
- [Source-linked noetic interface](../4ab67c31065de47787a47b1864b941cc8dd824478a62285f651a28016b776be8/noetic-interface.md) and [external-access ledger](../d0d1089f41194f9c0dbe10a8b7e552d0cee6c924cff8909a775853e057364445/SOURCE_ACCESS_LEDGER.md)
- [Original frozen review](../../PUBLIC_BOUNDARIES.md#recovered-reference-130), [general root replay](../../PUBLIC_BOUNDARIES.md#recovered-reference-132), and [six-suite packaging replay](../../PUBLIC_BOUNDARIES.md#recovered-reference-129)

The new universal claims are ordinary written proofs with independent internal mathematical review. Exact finite controls corroborate particular identities; they do not prove the full analytic/topological claims. No fresh Lean/kernel replay, empirical cognitive validation, source authentication, new philosophical warrant, repository integration, owner acceptance, final T20 closure or historical six-hour duration certification is asserted. Packaging/checking does not count as new research time. The root prospective-operation record is retained at its stated precision and does not certify earlier duration.

## Integrity verification, entirely offline

First compare the ZIP's SHA-256 with the independently delivered short guide. After extraction, from this directory run:

```sh
python3 -B replay/verify_admissibility.py --output ../hessian-admissibility-integrity
```

Python 3.8+ standard library is sufficient. The output directory must be new and outside the package. The verifier checks every payload hash and byte count, exact file/directory inventory, strict JSON, declared source/review bindings, and safe paths. Changed, missing or extra files, extra directories, symlinks and invalid manifest paths are rejected. No source research code is executed and the package is not changed.

To compare the ZIP with the extracted bytes too:

```sh
python3 -B replay/verify_admissibility.py --output ../hessian-admissibility-archive --archive ../T20_Hessian_Admissibility_Research_Checkpoint_20261009.zip
```

Optionally add `--archive-sha256 HASH_FROM_THE_SHORT_GUIDE`. ZIP duplicates, traversal, absolute/backslash paths, special members, wrong roots and unexpected members are rejected. The ZIP contains regular file entries only, and a 256 MiB uncompressed safety bound applies. A self-contained manifest cannot authenticate a replaced verifier; the independent ZIP hash is the trust anchor.

Run the bounded verifier-control suite with:

```sh
python3 -B replay/test_admissibility_verifier.py replay/verify_admissibility.py
```

It checks two valid-input cases and 18 rejection/refusal cases on temporary fixtures outside the package. It is a bounded implementation check, not a general security proof.

## Exact finite-control replay

Tested dependencies: Python 3.12.14, SymPy 1.14.0 and mpmath 1.3.0. The pinned requirements are in `replay/requirements-replay.txt`; install through your normal trusted package process if needed. Integrity verification requires none of those external packages. No toolchain binaries are bundled.

Run copies because some original scripts write results next to themselves. From this package root, these POSIX-shell commands preserve all sealed files:

```sh
mkdir ../hessian-admissibility-controls
cp hessian-frontier-recovery-20261009/scalar_closure_controls.py ../hessian-admissibility-controls/
cp hessian-flow-memory-boundary-20261009/check_controls.py ../hessian-admissibility-controls/
cp hessian-flow-continuation-20261009/check_dual_controls.py ../hessian-admissibility-controls/
cp hessian-continuation-independent-review-20261009/independent_controls.py ../hessian-admissibility-controls/
cp hessian-general-admissibility-20261009/controls.py ../hessian-admissibility-controls/
cp hessian-general-admissibility-review-20261009/independent_power_controls.py ../hessian-admissibility-controls/
python3 -B ../hessian-admissibility-controls/scalar_closure_controls.py > ../hessian-admissibility-controls/scalar.stdout.json
python3 -B ../hessian-admissibility-controls/check_controls.py > ../hessian-admissibility-controls/memory.stdout.json
python3 -B ../hessian-admissibility-controls/check_dual_controls.py > ../hessian-admissibility-controls/dual.stdout.json
python3 -B ../hessian-admissibility-controls/independent_controls.py > ../hessian-admissibility-controls/independent.stdout.json
python3 -B ../hessian-admissibility-controls/controls.py > ../hessian-admissibility-controls/general.stdout.json
python3 -B ../hessian-admissibility-controls/independent_power_controls.py > ../hessian-admissibility-controls/general-independent.stdout.json
```

Expected: every process exits zero and reports PASS. Counts are 66 memory assertion groups, 46 dual assertions, 29 earlier independent checks, 353 general fixture cases (32+32+1+288), and 13 additional independent symbolic checks; the scalar suite reports its exact finite algebra controls. These are different kinds of counts and must not be presented as a count of theorems. The six captured JSON outputs were compared exactly with the frozen component result objects; see `consolidated-verification/CONTROL_REPLAY.json`.

## Preservation and source boundaries

The predecessor ZIP remains byte-identical:

- `T20_Hessian_Continuation_Research_Checkpoint_20261009.zip`
- 1,190,627 bytes
- SHA-256 `20a63a419322e5cb85461324b88c440872800e1b39a3e792c2aa69ada04de85c`

All 115 files from its extracted payload are retained byte-for-byte; the predecessor ZIP itself is not embedded. `BASE_PAYLOAD_MAP.json` records the mapping. A few original root metadata files were renamed with `BASE_` so this consolidated package can have its own manifest and guide. Scientific component paths and their relative source layout remain unchanged. The base's `replay/verify_portable.py` and `replay/test_portable_verifier.py` are historical preserved bytes; use the new admissibility verifier above on this consolidated directory. The retained `BASE_READ_ME_FIRST.md` describes the earlier packet at its original boundary.

All 16 files in the three new frozen components are retained without edits. Earlier checkpoint ZIPs, including the new base ZIP, were inventoried and rehashed. The separate final validation receipt records that comparison. The historical source map is retained in full for provenance, but `INTEGRATION_INDEX.json` is the small practical entry point.

All local source files directly used by these arguments are present. The new source ledger's original absolute workspace locators are mapped to archive-relative paths in `provenance/GENERAL_SOURCE_PATH_REMAP.json`. External academic PDFs and Lean/Mathlib transitive build dependencies are not distributed. The external-access ledger precisely limits reading credit; this packet is self-contained for the retained reports, scoped local sources and Python controls once the stated dependencies are available, not for a whole historical programme or a new Lean build. Philosophical continuity remains inherited at its original defeasible warrant level.
