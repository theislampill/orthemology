# Orthemology Seventeenth supporting evidence

This directory contains finite-arithmetic checks, synthetic controls, selected historical aggregate certificates and bounded source-reading metadata. The three companion documents are distributed separately; their exact filenames, byte counts and SHA-256 digests are in `RELATED_ARTIFACTS.json`.

## Replaying the calculations and metadata checks

With Python 3.11 or newer and its standard library, run from this directory:

```sh
python -B run_checks.py
```

This runs the retained calculation and tail-predicate tests, synthetic block-orbit controls, aggregate-certificate arithmetic and source-metadata consistency checks. It uses no participant dataset, writes no research data and makes no network acquisition call. Metadata and portability tests are packaging controls, not new mathematical results. Metadata readers explicitly use UTF-8. A regression runs them under a strictly non-UTF-8 C locale on Linux; this is not a claim of Windows execution.

A successful run verifies those calculations and metadata assertions. It does not prove historical reading, independently authenticate source captures, verify every file's integrity, or verify the bytes of the separately supplied DOCX files. For example, the source-scope tests validate some digest shapes and relationships; a syntactically valid but substituted capture digest may still pass them.

## Separately verifying the exact directory

Obtain the trusted SHA-256 digest of `MANIFEST.json` independently of this directory, such as from the accompanying verification record. Then run:

```sh
python -B verify_manifest.py --expected-manifest-sha256 TRUSTED_MANIFEST_SHA256
```

Replace `TRUSTED_MANIFEST_SHA256` with that exact 64-character digest. This separate check compares the manifest to the supplied trusted digest, checks the complete file and directory allowlist, and verifies every nonmanifest member's byte count and SHA-256. The manifest's digest is external to avoid circular self-hashing. For an adversarially altered package, use a trusted verifier rather than relying on its included executable. A matching directory does not verify a later ZIP container, historical reading, source accuracy or external companion documents. Hash those DOCX files separately against `RELATED_ARTIFACTS.json`.

## Contents

- `calculation/`: exact decimal parsing, generic CSV reading and validation, the frozen fixed-opportunity statistic, rational exponential enclosures, independent arithmetic controls and fabricated fixtures.
- `tail/`: the two strict rational predicates and independent cross-product checks, with endpoint and malformed-input controls. The certificate retains its explicitly post-inspection status.
- `aggregates/`: previously recorded aggregate outputs and independent aggregate checks, in exact rational form. No participant records or coefficient arrays are included.
- `synthetic/check_orbits.py`: finite synthetic examples supporting the block-orbit discussion. These neither select nor execute a test on real observations.
- `sources/six_source_coverage.json`: the unchanged record for six supplied PDFs totaling 1,393 pages, including its targeted-visual snapshot and repaired cover gap. It contains metadata rather than book text or images.
- `sources/additional_arabic_source_scope.json`: the unchanged, separate record for the 938-page Arabic edition scan, covering 78 distinct main-text pages plus 17 separately bounded context pages. The scan's full length is not reading credit or an addition to the six-PDF total.
- `sources/minhaj_electronic_read_scope.json`: the unchanged bounded electronic-body reading record. It distinguishes successful retrieved line ranges, citation/search-derived printed references, and tool/cache retrieval failures. Repeated electronic texts are not independent witnesses; no printed-edition or manuscript collation is claimed.
- `companion/Mathematical_Companion_Content_v2.md`: the preserved original text-and-mathematics source. The final mathematical DOCX adds only two disclosed AI-authorship/date paragraphs. All 398 native mathematical objects and the preceding substantive content are unchanged. The Markdown lacks those two added paragraphs and does not promise identical pagination.

`FINITE_MATH_SCOPE.md` states the targets, assumptions, theorem dependency and the post-inspection lower-certificate argument. The separate mathematical companion supplies the underlying probability contracts; it does not contain that later certificate argument. `ADAPTATION_LOG.json` records copying and packaging changes. Historical certificates, source-scope records and adaptation entries retain their original version/status wording as historical snapshots; current companion-document identities are in `RELATED_ARTIFACTS.json`. The manifest, test receipt and bounded privacy report describe this exact directory and their respective verification limits.

## Aggregate replay and inferential scope

Actual-data inputs and execution orchestration are omitted. Generic CSV readers, validators and aggregate-calculation functions remain; the documented checks use fabricated fixtures and supplied aggregate certificates. The original archive and projection are identified by hashes only. Running this package cannot establish that their rows produce the recorded aggregates. The historical independent reconstruction used the same archive and was computational replication, not an independent experiment.

The empirical target remains all 75 exported games, all exported rosters and 48 scheduled opportunities per member, with weight `1/(75 × roster size × 48)`. It is not normalized by responder or disagreement counts. The companion's separate generic eligibility-normalized target must not be substituted for this frozen application.

All eight original finite sensitivity rows and the unrestricted endpoint are retained. The finite upper bounds are one. The separately labelled post-inspection lower certificate gives a strict lower bound `167/1500 > 1/20` for the same robust family suprema, conditional on the maintained model. It is neither the exact robust tail nor a lower bound for every individual assignment law. No historical randomization mechanism is recovered. No new empirical statistic, simulation, subgroup analysis or raw-data execution is included.

## Source, privacy and proof boundaries

No participant records, correspondence, private contacts, conversation logs, primary PDFs, extracted source bodies, source screenshots, page images, caches, private working reports or private filesystem paths are included. Original Drive links retain their access controls and do not grant public access or redistribution permission. Reading-coverage metadata does not establish the truth of the sources' arguments.

The mathematical material consists of ordinary finite computation and written argument. It does not add Lean files, claim kernel-checked proofs, reproduce the external Tyurin theorem's proof or alter the canonical programme. Attribution and theorem dependence remain explicit. Package verification does not itself establish programme closure, source-release permission or successful delivery.
