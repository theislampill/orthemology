# Read first

Result: exact `(judgement, support)` earliest-occurrence normalization preserves guarded DAG validity and exact root support without increasing nonnegative once-per-node cost. Finite state/rule refinement therefore yields an attained minimum via whole-graph enumeration.

Credit: this explicitly combines the already stated guarded refined-label construction and the already proved unguarded earliest-DAG theorem. It is not a new general finiteness method, scalable optimizer, or kernel-certified DAG result.

- `RESULT.md`: contract, full proof, finite-catalogue transport, limitations
- `guarded_dag.py`: supplied-witness normalizer and admission-aware checker
- `test_guarded_dag.py`: 13 discriminating deterministic tests
- `INPUT_HASHES.json` and `INPUT_UNCHANGED.json`: read-only predecessor bindings
- `MANIFEST.json`: author-packet byte bindings

From this directory, run `PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -v`.

The scripts import the two predecessor Python modules from their existing sibling directories. They do not modify them. No external packages, browser, network or installation are needed.

Independent review is separate from the author's assertions; no independent review is implied merely by these files being present.
