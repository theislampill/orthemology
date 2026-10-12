# Replaying this independent review

The review uses Lean 4.19.0, commit 6caaee842e94, and Mathlib commit c44e0c8ee63ca166450922a373c7409c5d26b00b with its official dependency cache. No custom `.olean` is an input to the rebuild. The recorded `lib/` directories are outputs and are omitted from the portable archive.

From this directory, replace the three environment paths as appropriate:

```
python verify.py \
  --source-root /path/to/p02-qualification \
  --mathlib-root /path/to/mathlib4 \
  --lean-bin /path/to/lean-4.19.0-linux/bin \
  --entry UniformComputabilityAudit \
  --entry EndpointChecks \
  --author-seal /path/to/p02-qualification/UNIFORM_COMPUTABILITY_SEAL.json
```

The verifier copies and independently compiles the full custom closure into a new receipt directory. It validates the exact Lean version, Mathlib pin and clean pinned official dependency checkouts, then reads every public `Uniform*` and auditor control declaration's full type and axiom footprint. It rejects unexpected axioms, build failures, source drift and seal drift. Re-run the expected-failure controls against the resulting independent library:

```
python run_negative_controls.py receipts/TIMESTAMP/RESULT.json
python compare_bindings.py receipts/TIMESTAMP/RESULT.json \
  /path/to/p02-qualification \
  /path/to/prior-operational-independent-receipt/RESULT.json
```

`compare_bindings.py` verifies all author seal files, all 35 declared source hashes, all 119 theorem targets and axiom sets, the generated author audit, and every shared source from the earlier operational independent review. The author receipt and older operational receipt remain separate evidence, not substitutes for the independent build.
