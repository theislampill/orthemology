# Replaying the separate matrix review

Use Lean 4.19.0, commit 6caaee842e94, and the official Mathlib cache at c44e0c8ee63ca166450922a373c7409c5d26b00b with its locked dependencies. No custom object files are build inputs. The portable archive omits generated custom `.olean` files.

From this directory, adjust the source/environment locations:

```
python verify.py \
  --source-root /path/to/p02-qualification \
  --source-root /path/to/atomic-membership-frontier \
  --source-root /path/to/measure-frontier \
  --source-root /path/to/tagged-row-measure \
  --mathlib-root /path/to/mathlib4 \
  --lean-bin /path/to/lean-4.19.0-linux/bin \
  --entry ComputableMatrixAudit \
  --entry MatrixVectors \
  --author-seal /path/to/p02-qualification/COMPUTABLE_MATRIX_SEAL.json
```

The verifier snapshots and rebuilds the full custom closure into a new isolated library, checks exact official pins, then reads explicit types and axioms for the matrix, arithmetic, original predicate/table, inherited Uniform, and independent control declarations. Source/author-seal drift is rejected. Each run records commands, output hashes and logs.

After a successful rebuild, run:

```
python compare_bindings.py receipts/TIMESTAMP/RESULT.json \
  /path/to/p02-qualification \
  /path/to/uniform-evaluator-independent-receipt/RESULT.json \
  /path/to/atomic-membership-independent-receipt/RESULT.json
python run_negative_controls.py receipts/TIMESTAMP/RESULT.json
python check_vectors.py receipts/TIMESTAMP/RESULT.json
python scan_sources.py receipts/TIMESTAMP/RESULT.json
```

Binding checks include the complete new 77-source seal, all 35 author theorem targets, the root arithmetic digest and six arithmetic targets, and unchanged overlapping source bytes from both prior independently reviewed subjects (35 evaluator and 51 original atomic-membership modules). Two prior supplemental modules, FixedIndexPrimrec and FiniteTableWitnesses, are not imported by the new subject. These prior receipts supply identity baselines, not a replacement for the new complete rebuild.

The 480 compiled vector rows each contain three values: the new heavy integer count, the new integer Boolean gate, and the original rational membership decision. A separate exact-Fraction/counting oracle checks all 1,440 values over three qualitatively different observer laws, depths/thresholds 0–3, and ten rational encodings. Finite vectors remain supplemental regression evidence; the uniform equality and computability claims are the kernel theorems.

The separately supplied diagonal sharpness control is optional to the matrix award and has its own receipt:

```
python run_sharpness.py receipts/TIMESTAMP/RESULT.json
```

It compiles the exact digest-bound NonPRBoundary source against the fresh closure and audits its two declarations. It proves non-primitive-recursiveness of the exact universal evaluator, not of the membership matrix. It neither alters the frozen matrix sources nor rewrites the earlier evaluator award.
