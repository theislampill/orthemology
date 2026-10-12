# Portable Gaussian SHK comparison replay

This derivative contains our comparison, derivation, accepted mathematical input snapshot and replay controls. RESULT.md is identical to the locally retained audit report.

Run `python3 verify.py`. SymPy is required; NumPy and SciPy enable optional numerical controls. The all-dimension proof is in RESULT.md. Finite tests are corroboration, not a formal proof.

The third-party primary PDF, extracted text, HTML and page images are deliberately omitted. No redistribution licence was established. Their exact source URLs, hashes and inspected regions remain in SOURCE_READING.json. Source-custody checks report `unavailable` when these originals are absent; that is not a successful custody verification. Mathematical controls remain executable.

To require a source-custody check, independently obtain the WIAS PDF from its recorded official URL, place it as `wias_preprints_3198.pdf` beside the verifier, and run `python3 verify.py --require-source-custody`. A different source hash fails.

The earlier accepted Gaussian input is included unchanged. If its original sibling folder is also present, the verifier checks it; otherwise it verifies the included hash-bound snapshot. No protected sources or earlier frozen artifacts were changed.
