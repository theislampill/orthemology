# Tenth research evidence

This evidence package accompanies the separate native Tenth research report. It preserves the accepted component papers, independent review receipts, exact input identities and reproducibility limits.

## Report and evidence

The accepted native report is a separate DOCX. This evidence directory contains its exact identity and claim map in `tranche10/report/public/REPORT_BINDING.json` and `REPORT_CLAIM_MAP.json`. It contains no report-prose copy, authoring Markdown, report render, prior native candidate or full-prose author binding.

Start with `COMPONENT_ACCEPTANCE.json` for controlling component dispositions, the report claim map for report/evidence links, and `REPRODUCIBILITY.md` for scientific replay boundaries. Accepted author packets can retain historical pending-review labels; their exact later independent receipts govern the stated acceptance scope. The dated integration and ownership reviews are historical companions.

## Payload-only check

With Python 3.12 or later, from the extracted evidence directory:

    python3 verify_selection.py . --expected-manifest-sha256 MANIFEST_HASH
    python3 -O verify_selection.py . --expected-manifest-sha256 MANIFEST_HASH

Use the manifest digest supplied separately with this package. This command checks exact file membership, regular-file status, duplicate and unsafe paths, symlinks, sizes, hashes and the declared report/claim-map binding. It needs no private directory or network. Its output explicitly says the external report was **NOT_CHECKED** when no report is supplied.

A self-consistent manifest is not an independent authenticity proof. Run on a quiescent directory; the checker does not defend against concurrent hostile filesystem writers. The manifest excludes only itself. Save verification output outside this directory, because an extra file correctly fails its strict membership check.

## Combined report and evidence check

Supply the separate report explicitly:

    python3 verify_selection.py . --expected-manifest-sha256 MANIFEST_HASH --report "/path/to/Orthemology_Tenth_Research_Report_v1_20261003.docx" --require-report
    python3 -O verify_selection.py . --expected-manifest-sha256 MANIFEST_HASH --report "/path/to/Orthemology_Tenth_Research_Report_v1_20261003.docx" --require-report

The checker reads only the report path supplied by the caller and compares its size and SHA-256 with the binding. A byte-identical renamed download, including a filename with a download suffix, is accepted. A substituted file fails even if its filename matches. The checker never searches for files named in historical metadata. A missing `--report` fails when `--require-report` is set.

This is combined byte verification, not a native-document rendering check, scientific review, source authentication, signature check or release authorisation. The independent native, reference, source-distribution and visual receipts state their separate scopes. The detached independent outer-archive receipt identifies the exact checked ZIP, manifest and separate report; its scope is distinct from this directory check.

## Historical receipts and public projections

`SELECTION_MANIFEST.json` is the sole current byte inventory. Original inner manifests and input inventories remain historical identity receipts. Some record omitted captures, compiled products, superseded drafts or predecessor bytes. They are not a second current-payload checker.

`PROVENANCE_MAP.json` maps every selected source, approved replacement and historical inventory member to its current representation or explicit omission. Accepted originals remain unchanged. Selected projections preserve predecessor identities while distributing only their approved replacement bodies. Local projection companions resolve to the controlling included receipts. `PUBLIC_SELECTION_PREDECESSOR.json` retains previous public-selection identities without copying their prose.

Ninth is represented by exact identities, never by its full report, archive or source-access prose. Raw primary captures, copied reviewer input trees, private working records, binaries, compiled modules and caches are excluded. Ordinary historical workspace/source-custody locators can remain as provenance; they are not public runtime requirements.

## Reproducibility and limits

The occurrence commands in `REPRODUCIBILITY.md` replay supplied Python models and the unchanged fixture. The full historical wrapper additionally requires excluded original source captures and is not publicly replayable from this directory. Its projected execution receipt remains historical evidence, not a claim that its source stage was repeated publicly.

The public Lean replay receipt records a fresh run from selected public inputs under the declared external Lean 4.19.0/Mathlib environment. It covers eight compiled modules and 99 axiom readbacks. The receipt preserves its exact tested predecessor selection, input identities and trust limits. It does not claim hermetic bootstrap, independent dependency certification or new mathematical acceptance. Runtime binaries and dependency caches are not bundled.

Finite-limit material is ordinary mathematics and review, with inherited ownership stated. It contains no new checker. Component/control counts overlap and are not independent evidence totals. No accepted component acquires conclusions beyond its explicit premises through packaging, source hashes or successful execution.

## Source use and currentness

The current source reconciliation and exact native-report distribution receipt govern the selected evidence, separate report and already delivered source-derived chat together. Public projections do not renew source allowances. No added source synopsis is supplied here. Older totals and draft-status remarks are historical where a later exact receipt supersedes them.

The read-only canonical boundary receipt describes its stated observation time. It does not claim that later repository states have been inspected.
