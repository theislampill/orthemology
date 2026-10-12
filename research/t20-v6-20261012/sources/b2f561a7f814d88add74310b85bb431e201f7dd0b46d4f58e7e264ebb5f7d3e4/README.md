# Channel-natural repair: compact intermediate research archive

Date: 2026-10-09 UTC.

This archive contains the frozen channel-natural mathematical result, its source ledger, six exact predecessor inputs, the parent candidate derivation (one of those six), the author control suite, and the complete independent-review artifacts. Original bytes and relative paths are preserved. No upload is part of this archive operation.

## Start here

- `channel-natural-repair-20261009/RESULT.md`: the mathematical result and exact hypotheses.
- `channel-natural-repair-review-20261009/FINAL_REVIEW.md`: the independent assessment.
- `channel-natural-repair-review-20261009/INDEPENDENT_ANALYSIS.md`: proof, scope controls, and source-reading limits.
- `INPUT_PROVENANCE.json`: the six inputs, original source links/pins where available, reading scopes, and byte-preservation map.
- `BUNDLE_MANIFEST.json`: every packaged payload file's length and SHA-256 digest. The manifest does not recursively hash itself.

## Replay from a fresh extraction

Requirements: Python 3 and SymPy. The packaging receipt records the exact Python and SymPy versions used. No network access, repository checkout, secrets, original PDFs, or data download is needed for replay. This is self-contained for the two current control suites, not a bundled Python distribution or a reproduction of all upstream repositories.

From the extracted archive's top directory, run:

```sh
python replay.py > ../channel-natural-replay-receipt.json
```

The helper verifies all bundle digests, the author manifest, every independent-review seal binding, and original-input preservation. It executes the author suite and the independently written suite, checks the expected counts (61 and 43), requires their generated JSON to remain byte-identical to the frozen records, and verifies all packaged bytes again. Success is reported as JSON on standard output; any failure returns a nonzero exit code. The command puts its receipt outside the payload directory.

The underlying commands, if desired, are:

```sh
python channel-natural-repair-20261009/verify.py
python channel-natural-repair-review-20261009/independent_controls.py
```

Each writes its own deterministic result JSON, with the same bytes as the frozen result. Neither script validates the universal mathematical theorem: the ordinary proof is in the documents. The helper uses standard-library integrity checks and invokes these unchanged scripts.

## Scope

This is an intermediate research handoff. The mathematical conclusion depends on its stated all-dimension, all-channel, interior-domain, and normalization-repair hypotheses. No formal-kernel certification or field-novelty claim is made. Chentsov's original book was not read during this task, and Campbell's original full PDF was unavailable; precise reading limits are preserved in the source ledger and review.

The two predecessor source ledgers are included unchanged. Their external and local citations preserve provenance, but files needed only by older predecessor replay suites or unrelated research are deliberately omitted. Both suites specified above require only the files supplied here. No lifecycle state or adoption decision is issued by packaging.
