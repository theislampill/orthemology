# Additive archive-portability supplement

This supplement fixes dependency preflight for the preserved Sixth controls
packet. It does not change any Lean theorem, mutant, proof loop, heartbeat
setting, or scientific disposition. Both original controls remain INCONCLUSIVE;
the cost scalar obstruction remains a separately scoped result.

Required original ZIP:

- Sixth_Control_Followup_20261002.zip
- SHA256: 6d4ff83d02763b4c11a5e2de3538e05cb827eda619930471e55d5c80ef758934
- Extracted manifest SHA256:
  f2eae35e8dfc35f630f1ef8228700517520b777aa451ad47fa2ec7e8c4198064

The original ZIP is unchanged and is not duplicated in this small supplement.
Its Git-only replay entrypoint remains as delivered. Use this supplement's
entrypoint for an exact official source-archive dependency tree.

## Identity routes

The wrapper requires the original compiler byte/version pins and eight official
dependency Git revisions. Dependency checkouts must be clean, with no untracked
or ignored extra Lean source. Tracked Git symlinks are bound by the tracked-clean
check and are not followed by the additional source census.

For Mathlib, choose one route:

1. A clean exact Git checkout at c44e0c8ee63ca166450922a373c7409c5d26b00b.
   Omit --mathlib-archive.
2. The exact official source archive plus its extracted source tree. Supply
   --mathlib-archive. The wrapper checks the complete compressed archive digest,
   every archived file, and all 6,816 extracted source files against the pinned
   inventory. It rejects missing, changed, unexpected, or symlinked source files.
   Only root .git and .lake metadata/build products are excluded from that source
   census. The eight .lake/packages dependencies are verified separately.

Pinned official archive:

- https://github.com/leanprover-community/mathlib4/archive/c44e0c8ee63ca166450922a373c7409c5d26b00b.tar.gz
- 17,774,877 bytes
- SHA256: 9fce64f31ba5612df46871eee8b4581c81c120604deb08cc35fa9f0fb543a425

The full archive digest is fixed in code. The inventory is independently checked
against the actual archive bytes, so an inventory alone cannot substitute for
the pinned archive. No Git metadata is created or fabricated. The supplement
contains inventory metadata only, not Mathlib source bodies or binaries.

## Run after extraction

All files may have mode 0644. Invoke Python explicitly; executable bits are not
required. Official Lean/Mathlib dependency caches must already exist. This
wrapper neither downloads nor modifies dependencies.

    python3 /path/to/supplement/replay_with_archive.py \
      --packet /path/to/extracted/Sixth_Control_Followup_20261002 \
      --lean-bin /path/to/lean-4.19.0-linux/bin \
      --mathlib /path/to/mathlib-source \
      --mathlib-archive /path/to/pinned-mathlib.tar.gz \
      --out /path/to/absent-output --mode all

--mode all performs the scoped cost scalar controls, fresh 162-module runtime
closure, selected positive type/axiom readbacks, and unchanged runtime mutant.
There is no additional full cost-mutant replay. --mode cost and --mode runtime
retain their original narrower meanings. Never infer semantic rejection from a
timeout or from the fact that an attempt completed.

Use --verify-dependencies-only with the same explicit paths and an absent output
path to check packet and dependency identities without proofs. --verify-only
checks only the original packet. Optimized Python (-O) is deliberately refused,
so source/outcome assertions cannot be disabled.

The output must be absent and outside the original packet, this wrapper, Mathlib,
and the Lean installation. A rejected preflight never rewrites a preexisting
RESULT.json. Terminal receipt updates occur only after this invocation created
the output directory. Python bytecode-cache writes are disabled.

## Validation and provenance

WRAPPER.diff shows the complete derivation from the original replay.py.
WRAPPER_BINDING.json pins both driver versions, the helper, and the inventory.
The scientific proof loops are unchanged. A prior preflight-only compatibility
failure is not reclassified as a proof or mutant failure.

validate_wrapper_guards.py exercises read-only preflight, -O refusal, preservation
of existing output evidence, forbidden dependency outputs, wrong archive digest,
changed source byte, and wrong dependency revision. Negative source-byte checks
use a separate copied fixture; the actual dependency tree remains read-only.

The evidence directory records the completed fresh-extraction replay and guard
controls. Public receipts normalize local filesystem roots and retain original
hashes. No official caches, custom .olean files, large source-copy fixtures,
service captures, or private download links are included.
