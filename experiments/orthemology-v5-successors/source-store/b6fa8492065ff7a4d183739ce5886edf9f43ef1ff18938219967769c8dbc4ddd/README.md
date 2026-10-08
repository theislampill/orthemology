# P1 expression algorithm: source and acceptance

This is a source-neutral public projection of the accepted P1_v3 expression-only result. It preserves all scientific Lean source, the inherited Python source, original controls, reviewer controls and the original accepted manifest/receipt identities. It contains no compiled proof objects or dependency binaries.

Accepted source manifest: `d0177de1ebeb8de4ff71898dbccc729ca420c70a50c307f1bacccd6d2c38d43d`.

Original independent acceptance receipt: `c55e4f5ae6dba9ce0f517c2b6ab242fdfbad7e4f8951e856cb7487e7fd1c15a0`.

## Result and limits

The model captures the iterative `(expression, ready)` work stack, value-stack orientation, finite dictionary store and the exact meter/check ordering of the bound Python expression evaluator.

On successful evaluation, it returns the corresponding `ObserverCore.evalExpr` value and consumes exactly the expression's syntax-derived work-pop/tick cost. On failure, it short-circuits at the same modeled error category and visible count as the recursive reference. It does not execute remaining work after a fault. The local result permits arbitrary pending work and preexisting values. Explicit input-dependent finite bounds suffice in the ideal mathematical model.

Read `spec/P1_SCOPE.md`, `spec/SOURCE_CORRESPONDENCE.md`, `acceptance/ACCEPTANCE.md`, and the explicit success/failure wording clarification in `acceptance/WORDING_CLARIFICATION.md`.

Theorems assume well-formed finite expression trees, natural exact built-in integer values/keys, optional natural exact-integer budgets and a natural exact-integer starting count. Those are preconditions, not runtime validation supplied by Meter or eval_expr. Missing variables are zero; variable reads are not width-checked. Power uses its distinct pre-shift exponent guard, while other arithmetic is checked after computation.

This is an accepted mathematical algorithm-model result plus independently reviewed, hash/AST-bound source correspondence. It is not a verified Python frontend or CPython theorem. Primitive Python semantics, allocation/time/OS failures, malformed direct tuples, parsing/serialization, statements/repeat tasks, complete run/trace/wrapper behavior, and a fixed finite all-input budget remain outside the result. No continued-success monotonicity theorem is asserted. P2/P3 work is unfinished and is not included here.

## Custody

- `bindings/ACCEPTED_SOURCE_MANIFEST.json` is the exact original manifest; it has not been edited to describe this projection.
- `bindings/ACCEPTED_REVIEW_MANIFEST.json` and `acceptance/ORIGINAL_REVIEW_RECEIPT.json` preserve the original review bindings.
- `CUSTODY_MAP.json` accounts for every original source payload and every original review payload: preserved, explicitly derived, or omitted with a reason. The public scope replaces a private approval paragraph; this is identified as a derived document.
- Private planning material, local execution paths, transient development snapshots/logs, compiled objects and toolchain/cache binaries are not bundled.
- Original historical receipts retain original relative artifact identifiers. Consult the custody map for relocated or omitted artifacts. They are historical qualification evidence, not a claim that every referenced file is present here.
- `PUBLIC_MANIFEST.json` binds the public payload. Its sidecar and the separately supplied ZIP digest provide transport-integrity checks, not a cryptographic authorship attestation.

The inherited `source/prcodec.py` is exact input source with SHA-256 `dd79f63f5af91bbe1c3695fa401a41a726b224fa5e3d80aa9c589de95949da6c`. Its inclusion does not broaden the accepted expression-only theorem scope.

## External prerequisites

Supply an already provisioned Lean 4.19.0 distribution and the exact accepted Mathlib source/precompiled cache. The full dependency manifests are included under `dependencies/`. The launcher hash is `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023` and the Mathlib revision is `c44e0c8ee63ca166450922a373c7409c5d26b00b`.

The wrapper verifies the full 5,065-entry compiler distribution, 6,816 source records and 34,230 cache entries before compilation. Official precompiled proof dependencies remain trusted. This packet does not download, install, repair, bootstrap or rebuild official Mathlib. Missing or mismatching prerequisites are a refusal, not a silently substituted toolchain.

`spec/DEPENDENCY_PINS.json` retains historical revision/clean-state metadata. It is not a live Git-clean claim about an archive-restored environment. Current verification is byte-based.

### Five trace-path relocations

Exactly five cache-utility `.trace` paths may be compared after one prefix replacement per file; all scientific `.olean`/`.ilean` and all other cache entries must match exactly. The replacement must yield the original pinned size and SHA-256. No normalized trace is saved and no dependency file is modified.

For an exact original cache, omit the trace-prefix options. For a relocated cache, supply its existing prefix and the reference snapshot prefix as external environment values, including trailing separators. Prefixes alone authorize nothing: the original hash/size checks must still pass. Absolute host-specific prefixes are intentionally not bundled. `dependencies/TRACE_PATH_DELTAS.json` lists the allowed paths and bound original identities.

## Portable replay

Use Python 3.12 or a compatible Python 3 implementation. Set the following shell variables to the externally supplied input locations and a new output location. Output must be nonexistent and outside the packet, compiler and Mathlib trees.

```sh
python3 replay.py \
  --lean-root "$LEAN_ROOT" \
  --mathlib-root "$MATHLIB_ROOT" \
  --output "$NEW_OUTPUT"
```

For a relocated cache, additionally pass:

```sh
  --trace-prefix "$RESTORED_TRACE_PREFIX" \
  --pinned-trace-prefix "$REFERENCE_TRACE_PREFIX"
```

Append `--verify-only` to validate custody and all prerequisites without compilation. No shell script is sourced automatically and no existing LEAN_PATH is trusted.

Full replay cold-builds the local ObserverCore copy, four scientific modules, required checks, 21 author controls, 37 public theorem axiom readbacks, four reviewer universal consumer theorems and 28 reviewer examples. It also checks the four expected machine-mutant rejections and bounded Python/source controls, including the exact independent control script.

The independent script is executed unchanged in an output-only compatibility layout. Its two literal-source paths are populated with byte-identical copies of the bound input. This reproduces the behavioral controls; it does not create a new claim of independently sourced provenance. The original accepted custody evidence retains that historical role.

Each Lean invocation uses `-j1`, default heartbeats and a 180-second wall limit. Commands run sequentially. A timeout is a failure with no semantic or mutant-rejection credit. No historical whole-program timeout probe is retried.

Outputs, including custom `.olean` files and logs, stay beneath the new output directory. Logs replace only machine-specific packet/output/dependency/interpreter path prefixes with logical names; receipts retain raw diagnostic hashes and the normalized log hashes. No input file is changed. Successful replay ends with `REPLAY_RECEIPT.json`; absent receipt or nonzero exit is not successful completion.
