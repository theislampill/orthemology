# Polynomial proof extensions: intermediate evidence archive

10 October 2026 UTC. Additive preservation of two independently accepted, explicitly bounded results. This archive neither supersedes earlier evidence nor closes T20.

## Contents and accepted scope

- `sources/lean-truncated-moment-obstruction-20261010/` preserves the exact author sources, five compiler-negative controls, successful and historical logs, manifests, receipts, and excluded exploratory source. The proof uses actual `MvPolynomial (Fin 3) ℝ`, ordinary multiplication, coefficients, total degree and evaluation. Every nonzero degree-at-most-two polynomial has strictly positive Λ(p²), while a globally nonnegative degree-four polynomial F has Λ(F)=−2. All 35 moments and the ten-coefficient parameterization are checked.
- `sources/polynomial-moment-certificate-independent-review-20261010/` preserves the sealed independent source review, all 72 production axiom closures, two additional probes, exact symbolic checks and complete review logs. Its seal accepts only the stated truncated polynomial scope.
- `sources/polynomial-transport-continuation-20261010/` and its independent review preserve the ordinary written proof for supplied bounded-degree C1 polynomial automorphism paths satisfying transformed Theorem V hypotheses. The nonlinear shear example has joint determinacy even though one coordinate's Carleman series converges. This does not assert marginal indeterminacy, arbitrary polynomial-vector-field completeness, or a universal formal kernel proof. All 36 exact symbolic controls are retained.
- `inherited/` contains the small dependency proof/provenance set: accepted V with its review, the fixed-coordinate ancestor, source-comparison note, and rational truncated diagnostic with its review. Small V control inputs are retained so its existing 23 checks can also run. Ancestor receipts may refer to wider earlier packets or external publications not copied here; their presence does not claim those wider artifacts are bundled or newly reviewed.
- `prerequisites/` pins the external Lean distribution and package source revisions and records all 2,447 retained dependency source/object SHA-256 pairs. No external `.olean` files, Mathlib tree, toolchain, modern full-source book or PDF is bundled.
- `INPUT_PROVENANCE.json` binds every preserved input to its original byte hash. `MANIFEST.json` covers every payload file except itself. Original historical scripts are preserved unchanged for provenance, including their original absolute paths. Use the root `replay.py` for relocation-safe replay; do not run those historical scripts in place.

## Essential boundaries

The actual zero continuation to higher monomial coefficients fails full square positivity: Λ((x³−x)²)=−96. Both that degree-three counterexample and the degree restriction are kernel-checked. It does not prove that every possible extension of the 35 moments fails.

The five deliberately false claims must fail at the Lean compiler with logical/arithmetic `False` goals: Λ(F)=−1; Λ(xyz)=0; 0≤Λ(F); 0≤Λ((x³−x)²); 0<−Λ(1). Missing imports or identifiers are not acceptable negative-control results.

General positive-measure nonrepresentation is a written corollary, with integrability explained in the independent review. No MeasureTheory/Bochner theorem or heat theorem was compiled. The `.lean.unbuilt` attempts have no verification status. The heat value −3797/2500 and inverse-heat controls remain exact symbolic mathematics only. The active diffusion theorem is excluded. No integration, protected-source change, upload, field-priority conclusion, empirical/noetic application or T20 closure is included.

## External prerequisites and exact replay

1. Python 3.10+ is required. The executed environment is recorded in `prerequisites/RUNTIME_PINS.json` (Python 3.12.14). Supply SymPy 1.14.0 and mpmath 1.3.0, pinned in `requirements.txt`. Installation, if needed, is a separate environment-preparation step; this replay does not install anything.
2. Supply the retained Lean 4.19.0 x86_64 Linux distribution (reported commit `6caaee842e94`, original toolchain spec `leanprover/lean4:v4.19.0`). `--lean-home` is its root, with `bin/lean`, `lib/lean`, and `src/lean`. The replay verifies the executable and three Lean runtime shared-library hashes, plus every imported Lean source/object pair. The Linux host's compatible C runtime and loader remain external prerequisites.
3. Supply the pinned package checkouts and retained compiled objects. `--packages-dir` contains the named `mathlib`, `aesop`, `batteries`, `Qq`, `plausible`, `proofwidgets`, `LeanSearchClient`, and `importGraph` directories with their standard `.lake/build/lib/lean` layout. `Cli` remains recorded in the upstream package lock, but contributes no imported object and needs no built output. The exact package repository URLs and full commit hashes are in `RUNTIME_PINS.json` and the original `lake-manifest.json`. Mathlib is `c44e0c8ee63ca166450922a373c7409c5d26b00b`.
4. This compact archive does not promise those binaries can be regenerated bit-identically merely from source commit hashes. Exact replay requires objects matching `EXTERNAL_DEPENDENCIES.json`; independently building/fetching different objects would be a separate validation exercise. The retained dependency tree can be relocated or copied to another compatible host without rewriting any archived file. All paths in the replay manifest are relative to the two supplied roots.

From the extracted packet directory:

    python3 replay.py --lean-home /absolute/path/to/lean-4.19.0-linux --packages-dir /absolute/path/to/packages --output /absolute/path/to/new-replay-output

The output directory must not exist and must be outside the immutable packet. The command verifies all payload hashes and all 2,447 external source/object pairs before compiling the seven own production modules and two independent review modules with `--trust=0`. It checks fresh local import resolution, exact production object hashes, 72 production plus two additional axiom closures (only standard `propext`, `Classical.choice`, `Quot.sound`), all five expected failures, and the 36 transport controls. It also replays the rational diagnostic, independent symbolic moment check and inherited V controls in separate output copies; their result bytes must match the archived results. No original is overwritten.

The command never calls Lake, rebuilds Mathlib, downloads dependencies, or uses a bundled old local object. Imported retained `.olean` files are identity-verified, not freshly rebuilt. `--trust=0` applies to the newly compiled sources; it is not a claim that the entire dependency library was recompiled or independently re-proved here. Fresh receipts, full logs and objects go only to the supplied output directory.

## Integrity and preservation receipts

`preservation-evidence/` includes the successful preliminary fresh-extract logs and receipt, plus fail-closed integrity guard tests. An initial wrapper-only preflight overrequired a built output for unused Cli; the correction and preflight failure are retained explicitly. No proof module had run in that failed preflight, and no author or dependency file was changed.

The final archive's SHA-256, byte size, fresh-extract replay receipt, and original/earlier-archive nonmutation checks are delivered in an external preservation receipt to avoid a circular archive hash. The payload retains the original accepted author/reviewer receipts as immutable historical records. Author receipts that predate review remain unchanged; the later independent review seals establish their accepted status.
