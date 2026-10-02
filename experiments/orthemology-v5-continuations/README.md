# v5 continuation sources and replay

Start with the [claim boundaries](../../docs/architecture/V5-RESEARCH-CONTINUATIONS.md)
and [source/review index](../../docs/provenance/v5-research-continuations/README.md).
This continues through the final sixth return, preserving the checkpoint-3
registry and its receipts. Research adoption remains candidate-scoped.

Run deterministic source/status validation and rejection controls with Python
3.11.9 and the repository's existing dependency lock:

```sh
python -B scripts/validate_research_continuations.py
python -B tests/test_research_continuations.py
python -B -O tests/test_research_continuations.py
python -B tests/test_research_continuation_replay.py
python -B -O tests/test_research_continuation_replay.py
python -B tests/test_research_continuation_successors.py
python -B -O tests/test_research_continuation_successors.py
python -B tests/test_continuation_controls.py
python -B -O tests/test_continuation_controls.py
```

Choose a suite ID from `registry.json`. For example, using explicit locations for
the official Linux x86-64 Lean 4.19.0 bin directory and pinned Mathlib checkout:

```sh
python -B scripts/replay_research_continuations.py \
  --suite 0a74eb642cc6-integer-budget-v3 \
  --lean-bin "$LEAN_BIN" --mathlib "$MATHLIB" --out "$ABSENT_EXTERNAL_OUTPUT"
```

The output must be absent and outside the checkout. Exit 0 means scoped fresh
custom compilation and exact type/axiom readbacks; exit 1 is failure and exit 2
is a missing prerequisite. The receipt does not claim original mutation controls,
whole-family mathematical adoption or external warrants. Do not copy generated
objects or logs into Git. Official cached dependencies are trusted; all custom
objects in this interface are freshly built. No shared custom import directory
or fallback to an author build is allowed.

`source-store` deduplicates equal bytes, while `suites` preserves independent
module namespaces and import closures. The stored driver identities describe the
original packet's argument contract. Some original `--lean-bin` options actually
take an executable: the normalized descriptor records the inspected meaning,
not an inference from the option name. The public interface above always takes
a bin directory.

`reference/rational-v3` and `reference/integer-v3` preserve exact selected Python
sources and their local test layout. Their original complete packet verifiers
also inspect private archive dependencies and are retained in private custody.
The selected public tests can be run directly in normal Python; they contain
original assertions and must not be credited under optimized Python. Only the
new fail-closed validation tests above claim optimized-mode protection.

The final-sixth kernel closures are
`7cbe94fa76f6-actual-finite-model-common-exponential-range` (153 modules) and
`b5be7775f6d0-runtime-v8` (179 modules), plus the connected-author,
connected-review and zero-error-disclosure suites. Their component receipts do
not certify the whole original control contract. The successor overlay separately
binds native checks and supplied semantic probes/mutations to exact fresh kernel
receipts. Resource-limit results remain inconclusive, even when another diagnostic
appears in the same log.

The standard-library controls have their own isolated public interface:

```sh
python -B scripts/replay_continuation_controls.py \
  --suite sixth-foundations --out "$ABSENT_EXTERNAL_OUTPUT"
```

Also available are `sixth-foundations-addenda` and `sixth-cost-controls`; each
needs a different absent output directory. These replay exact original inputs
with Python assertions enabled, even if the parent runs with optimization.
Source files cannot be overwritten, and undeclared output files fail the replay.
The returned `PASS_NATIVE_CONTROLS` means finite controls only. It does not
formalize the ordinary continuum proofs or establish world-directed warrant.
