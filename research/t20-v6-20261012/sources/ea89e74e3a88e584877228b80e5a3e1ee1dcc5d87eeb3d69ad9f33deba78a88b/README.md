# Orthemology Seventh research evidence collection

Start with report.docx and EVIDENCE_LEDGER.json. MANIFEST.json maps the report’s original filenames and input identities to short component ZIP names and embedded paths. Exact accepted ZIP bytes are preserved. Later acceptance records control current status; historical pending labels remain unchanged inside frozen inputs.

Source interpretation, general conditional proofs, finite/reference execution and actual applicability remain distinct. N2, essential T0 and fixed R5 remain open. Both inherited Sixth semantic mutants remain INCONCLUSIVE. No physical deployment or external specialist certification is claimed.

## Verify and extract

Collection verification needs Python 3.10 or later and its standard library. It executes no component code and makes no network request.

    python verify.py
    python verify.py --manifest-sha256 THE_INDEPENDENTLY_RECEIVED_SHA256

A checksum inside the same untrusted download cannot authenticate its own origin. Preserve the outer ZIP digest supplied with delivery.

Extract components to a new, absent directory with a short path:

    python verify.py --extract-to private-locator:f9ef82fa38a17584e821

Each component receives its short identifier as a directory. Only the explicitly recorded common ZIP wrapper prefix is removed; file bytes and scientific layouts are unchanged. The report and loose baseline/addendum files remain at collection level.

The verifier checks exact inventories, hashes and ZIP CRCs. It rejects traversal, absolute/backslash paths, symlinks, nonregular or encrypted members, filename collisions, Windows reserved names/characters and excessive paths. Fresh staged extraction rechecks written bytes and refuses existing destinations. Both staging and final paths must fit a conservative 240 UTF-16-unit ceiling.

Run the 44 positive/negative controls without changing collection bytes:

    python test_verifier.py
    python -O test_verifier.py

## Run component checks

Packaging-only validators use two absent destinations:

    python verify.py --extract-to private-locator:b22079622d6d0185af9b --validate-components all --out private-locator:549456322a848bdff68e

A component without a separate validator is still covered by the collection’s complete inventory, member hashes and CRC checks.

Proof/reference replay needs official Linux x86_64 Lean 4.19.0; native composition also needs its leanc compiler. Mathlib-dependent components require commit c44e0c8ee63ca166450922a373c7409c5d26b00b, the exact dependency revisions listed in the manifest, and official compiled caches. Preserved shell drivers require Bash. External caches remain trusted inputs; they are not rebuilt or bundled. Windows-safe filenames do not establish native Windows proof replay; use the documented Linux environment or WSL.

Example selective replay:

    python verify.py --extract-to private-locator:a494c4386c143f0123ce --replay attribution covering --lean-bin /path/to/lean-4.19.0-linux/bin --mathlib /path/to/mathlib-c44e0c8 --out private-locator:1662f64dde838969d847

Use component IDs from the manifest, or all. Recipes, timeouts and terminal expectations are explicit there. Both destinations must be absent; outputs stay outside immutable inputs. Replay rechecks every extracted component and the collection after each command. Declared terminal evidence must be newly generated regular files under the anchored output area. Failed commands, altered inputs, wrong terminal results and resource limits prevent a successful receipt; partial timeout diagnostics are retained. Replay executes accepted component code under the caller’s permissions and is not a general code sandbox.

For controls with archive-extracted Mathlib, also supply --mathlib-archive /path/to/mathlib-c44e0c8.tar.gz, SHA256 9fce64f31ba5612df46871eee8b4581c81c120604deb08cc35fa9f0fb543a425. Omit it for a clean exact Git checkout. The separately accepted control-support wrapper supplies this route without changing controls.zip. It requires completed bounded revalidation while preserving both INCONCLUSIVE scientific outcomes. The full original cost-mutant closure is intentionally absent; its scalar probe is a narrower check. Long runtime replays can take substantially longer than packaging validation.

## Source and evidence handling

Read scope-addenda/F3_SCOPE_CLARIFICATION.md with the source-scope baseline. F3 is an unresolved reading issue, not established textual corruption. baseline/infinity preserves a small inherited formal closure and scope clarification, with no new Seventh proof credit. Historical review bodies omitted to avoid extra exposition retain exact hash/locator references.

Modern-source exposition is kept only in its accepted curated locations; the final report’s rebound ledger controls combined accounting. Exact custom sources recur only where immutable accepted packets retain their dependency closures. The manifest identifies these inherited copies and the optional unpinned NumPy/SciPy discovery script, which supported replay does not invoke. Full supplied PDFs, raw captures, process notes, credentials, external tools/caches and generated compiled objects are excluded.

The baseline verification is a field-preserving public projection of an earlier read-only record. REMOTE_RECHECK.json separately records a later branch lookup. Neither is a fresh proof replay. No GitHub write is part of this collection.
