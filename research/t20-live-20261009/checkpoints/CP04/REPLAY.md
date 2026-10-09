# Replay and evidence boundaries

## Verify the extracted payload

Extract the ZIP with any normal ZIP reader, then run from its top directory:

```sh
python3 PACKING/check_manifest.py
sha256sum --check MANIFEST.sha256
```

The root manifest enumerates actual payloads. Original nested manifests remain unchanged and can name omitted source bodies or compiled objects. Their exclusions are explicit in `OMISSIONS_AND_SOURCE_LINKS.json`; they are not unexplained archive corruption.

## Reproduce the scoped Python controls

Recorded environment: Python 3.12.14, mpmath 1.3.0 and SymPy 1.14.0. Ten scripts use the standard library; only the adaptive-count numerical diagnostic needs mpmath, and only the crossed interior symbolic diagnostic needs SymPy. The versions are pinned in `PACKING/requirements-controls.txt`; dependencies are not installed or bundled by the harness.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONOPTIMIZE=0 python3 PACKING/replay_python.py --output ../fresh-scope-calibration-replay
```

The harness copies the checkpoint into a disposable directory before invoking unchanged scripts. All writes and regenerated scientific outputs occur there. It compares the deterministic JSON results to frozen values and checks that the delivered checkpoint stays byte-identical. Logs and its new receipt go to the requested output directory outside this checkpoint.

The twelve commands cover acquisition recruitment, calibration-frontier author controls, crossed independent/incorporation/symbolic controls, arbitrary adaptive pure-count review, multi-root author and review controls, and global calibration main/efficiency author and review controls. Exact paths and comparisons are in `PACKING/REPLAY_RECEIPT.json`. High-precision numerical diagnostics are not exact real-arithmetic proofs. Finite controls do not replace the general written arguments or test physical applicability.

## Existing Lean record and minimal dependencies

No fresh Lean invocation, kernel replay or environmental rebuild was performed for this checkpoint. The productive-sufficiency author and reviewer logs retain their historical identity and declared scope. Cached `.olean` files, all mathlib files, toolchains and giant rebuild outputs are intentionally omitted.

The compact archive includes all local Lean source modules needed for the reported productive-sufficiency dependency graph:

- The three `formal-identification` modules: Calibration, HitTransform and CalibratedPanels
- Five probability modules preserved in `productive-sufficiency-scope/review/replay`: Model, BernoulliAssignments, HistogramGrouping, GenerativePanels and EndpointLaw
- The three unchanged inherited bridge modules under `productive-sufficiency-scope/inherited`
- ScopeTest, ReviewerChecks and the three false-strengthening source probes

`PACKING/LEAN_DEPENDENCIES.json` lists the source compile order, exact Lean 4.19.0 release/archive SHA-256, mathlib commit and dependency lockfile. These are sufficient local project sources and external pins, not a prebuilt portable environment. The original bootstrap script is included unchanged as a historical official-source retrieval recipe. It installs/downloads tools if executed and may require connectivity or permission; it was not executed by packaging.

For a future replay in an already prepared pinned Lean/mathlib environment, compile these source modules in the listed order, making the preceding modules' output directories available through LEAN_PATH and using the historical flags `-DwarningAsError=true --trust=0`. The original `verify.sh` and `negative_controls.py` additionally expect sibling `formal-identification` and `formal-route-probability` directories with the earlier layout. Probability sources in this ZIP are deliberately preserved at their reviewer snapshot paths rather than silently rewriting that historical verifier. Arrange a disposable replay layout first, or use the first identified checkpoint's documented original layout. The verifier alone is not advertised as a complete one-command replay from this compact ZIP.

No build recipe above is represented as newly tested. The current delivery checks byte identity and Python controls only.

## Preservation rules

Earlier checkpoints are identified by exact hashes rather than copied wholesale. Root candidate notes remain dated history; the final reviewed successors govern their claims. Source omissions retain original source locators and available hashes, with fresh local exclusion hashes distinguished from inherited receipts. No new historical reading, empirical evidence, research-time credit, owner acceptance, final integration or T20 closure follows from packaging or replay.
