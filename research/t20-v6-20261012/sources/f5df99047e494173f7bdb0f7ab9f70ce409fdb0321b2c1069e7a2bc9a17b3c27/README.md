# Reproducible exact diagnostics

## What is actually implemented

The code uses Python's standard library only. It contains exact rational probability calculations, finite modal and causal-support controls, a 15-fact Boolean explanation interpretation, compatibility-graph enumeration, and offline package-integrity checks. It does not contact external services, install tools, modify a repository, or run any inherited Lean suite.

`diagnostics.py` implements the mathematical controls. `tests/` contains 56 unit/finite-control tests, including explicit negative cases. `replay.py` recomputes the canonical result, compares it to the delivered record, runs all tests, and checks that the input research tree is unchanged.

## One-command replay

From the extracted package root:

```sh
python3 -B engineering/replay.py --output /absolute/path/to/new-t20-review-output
```

Python 3.10 or later is recommended; the producing environment was Python 3.13. The output parent must already exist, the output itself must not exist, and it must be outside the research tree. The command normally takes seconds to tens of seconds depending on the machine. Its child-test timeout is 120 seconds.

Results are written only to the new output:

- `DIAGNOSTIC_RESULTS.json` — deterministic exact results;
- `TESTS.log` — unittest output;
- `REPLAY_RECEIPT.json` — environment, exit status, result identity and before/after integrity.

A successful replay is not an independent philosophical review. Hashes protect byte identity against the supplied manifest; without a separately trusted archive digest they do not authenticate the author.

## Safe ZIP inspection

The included `inspect_archive.py` validates and stages a file-only, single-root archive before committing it to a new directory. It refuses paths containing traversal, backslashes, absolute names or colons; duplicate names; symbolic links and special-file modes; encrypted members; oversized packages; and existing destinations. It then checks the staged manifest. No research code in the inspected archive is executed.

```sh
python3 -B engineering/inspect_archive.py /path/to/delivery.zip /path/to/new-destination
```

The utility itself must come from a trusted/read copy. No self-checking script can establish its own integrity from nothing.

## Mathematical scope

The Boolean interpretation exhausts 32,767 nonempty pluralities of 15 facts. Full and partial transitivity over every target are checked by exact integer bit-set inclusion. This is not a Monte Carlo approximation.

The covariance obstruction for finite exchangeability and the common-requisite/graph lemmas have written general proofs. Finite enumeration is corroborating execution, not a proof that the general theorem is true merely because tested cases passed.

The causal tables identify minimal positive sufficient sets under a declared monotone Boolean response law. They do not implement Schaffer's complete theory of actual causation. The modal tables are interpretations of restricted signatures, not authenticated metaphysical possibilities.

## Lean boundary

`formal/BridgeDiagnostics.lean` is an optional **uncompiled candidate**, not a successful execution result. It is not invoked by replay. The seven inherited Lean files were inspected and hashed, not freshly compiled. No toolchain is bundled.

## Development evidence

The first diagnostic implementation was preceded by failing tests. Compatibility-graph and package-integrity additions have separately preserved RED records. The GREEN logs and the final fresh-extraction receipt identify which tests actually ran. A failing test caused by an intentionally absent implementation is development evidence, not a philosophical counterexample.
