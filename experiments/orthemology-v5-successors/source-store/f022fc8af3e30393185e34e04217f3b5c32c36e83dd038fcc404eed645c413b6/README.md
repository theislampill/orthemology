# Lean project: exact source integration

## Prepare dependencies

Install/select official Lean `leanprover/lean4:v4.19.0`. Keep `lean-toolchain`, `lakefile.lean`, and `lake-manifest.json` unchanged. The manifest fixes all nine repositories; `DEPENDENCY_PROVENANCE.json` gives their URLs, exact commits and replay provenance.

For a prepared, clean Mathlib checkout at the pinned commit, with its eight pinned packages and compatible compiled cache already available:

    python3 verification/reuse_dependencies.py /path/to/prepared/mathlib
    python3 verification/verify_dependencies.py

The helper verifies the nine Git heads and clean tracked trees before creating local `.lake/packages/` symlinks. It refuses conflicting links. It copies no compiled project output. A compatible existing dependency cache may be reused; project modules must be compiled freshly in this package.

Alternatively, Lake can obtain the manifest-pinned repositories in a network-enabled environment. After that, request the official selective cache for the imported Mathlib roots:

    lake exe cache get Mathlib/Data/Bool/Basic.lean Mathlib/Algebra/MvPolynomial/Funext.lean Mathlib/Algebra/BigOperators/Fin.lean Mathlib/Algebra/Order/BigOperators/Group/Finset.lean
    python3 verification/verify_dependencies.py

The network-bootstrap route is guidance, not a claim that a clean network bootstrap or full external dependency rebuild was performed for this release. The recorded replay reused exact existing clean source checkouts and caches, including the restricted extension's documented official selective cache acquisition. This integration performed no new download. Do not update dependency revisions.

## Build and verify

The outer `replay.sh` is the complete fresh-extraction entry point. Individually:

    python3 verification/verify_sources.py
    lake build
    bash verification/run_checks.sh

All 88 root modules are default targets. `verification.KernelAudit` is a separately registered supporting module imported by the audits. Verification scripts run inherited interface/audit suites, Raw and Boolean rejection suites, gate controls, restricted compiler/checker controls, nine root polynomial-test controls, executable-closure checks, all-project proof closure, and declaration export. New logs and outputs are local replay products.

`verification/AllProjectProofAudit.lean` selects every theorem originating in the 88 modules, collects its axioms independently, and traverses checked declaration types/values, constructors and recursor rules. It rejects unapproved axioms, unchecked dependencies, unsafe/partial dependencies and incomplete traversal. The only permitted standard axioms are `propext`, `Quot.sound`, `Classical.choice`. Generated runtime auxiliaries are not proof roots and cannot occur in accepted proof closure. `verification/RestrictedComputationalAudit.lean` additionally excludes classical choice and abstract-polynomial interpretation from the three executable checker/certificate roots.

## Source identity and declarations

`MODULES.json` lists all 88 root modules. `verification/preserved-module-lock.json` binds every root to its accepted source stage. `verification/source-lock.json` binds current source, configuration and replay scripts. `DECLARATION_CLAIM_MAP.md` and the machine-readable declaration inventory identify checked declarations and their exact boundary; the Lean statements themselves are authoritative.

The original 76 source modules are byte-identical to the accepted unified v3 archive. The two gate modules, restricted v1 compiler and seven restricted v2 modules are also unchanged. Thus all 86 v4 root modules retain their exact bytes. The separately accepted PolynomialTestBoundary and PolynomialTestAudit modules are included unchanged as two additional default roots. Integration edits only configuration, supporting replay harnesses, locks and release metadata. There is no namespace rewrite or semantic transport in this integration.

## Historical receipts

- `verification/historical/raw-v2-receipt.json`: exact original Raw receipt, SHA-256 `24db3eb238d712fa242cb5c71a5c074d70a4a52434d34b41ada2f3d731327082`.
- `verification/historical/unified-v3-receipt.json`: exact original 76-module receipt, SHA-256 `53cd30a370c0f94db9fc211d2005637af204cc5197e88f30c7edcbfed6a52a27`.
- `verification/historical/unified-v4-receipt.json`: exact 86-module integration receipt, SHA-256 `3ab3b08b87aef587b2b6dd3964f6a884fb90c3b547511157b73275ebe4f7d637`.
- `verification/receipt.json`: distinct v5 replay record, never a replacement for the historical receipts.

Historical receipts and source locks refer to their historical package-relative files/logs, some deliberately not repeated here. They are custody evidence, not claims that old relative paths resolve in this successor or that historical replay equals current replay.

Negative fixtures intentionally contain false statements, missing premises, axioms, admitted proofs or unsafe/partial definitions to test rejection. They are excluded from the library proof roots, and successful infrastructure compilation is required before an intended rejection counts.
