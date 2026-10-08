# Source/version verification

Checked 3 October 2026 UTC, approximately 12:30–12:35. Read-only; no external contact, access workaround, or publication.

## Disposition

**The bibliographic identity is verified; the finality/currentness of the inspected PROOF PDF is not.** No correction or erratum was located in the bounded checks below. This is not evidence that none exists. Retain the description **publisher-hosted, proof-marked witness**, rather than “verified final version” or “uncorrected publication.” No changed domain qualification was verified in a final text.

## Identified records and copies

- [Crossref work record](https://api.crossref.org/works/10.48106/dial.v77.i4.04), raw JSON retrieved at 12:31:50–12:31:55 UTC: Alexandre Billon; *Dialectica* 77(4), 459–504; publication year 2023; DOI 10.48106/dial.v77.i4.04. The DOI record was created on 2 October 2025 at 12:26:32 UTC and deposited at 12:26:48 UTC. Its primary resource remains https://www.philosophie.ch/billon-2023. Empty `relation`; no correction/update notice in the retrieved record. Registration/deposit dates are not publication or PDF revision dates.
- [Inspected asset URL](https://assets.philosophie.ch/dialectica/billon_a-2023.pdf): the web tool supplies a **cached text extraction**, 47 PDF pages, cover plus printed 459–504, with PROOF markings and CC-BY 4.0 notice. Requested printed locators correspond to zero-based PDF pages **16 / 24 / 41 / 42** for 474 / 482 / 499 / 500. This check did not obtain raw bytes or a successful screenshot; no PDF hash is available.
- [Alternative former-publisher attachment](https://www.philosophie.ch/attachment/1263/download/billon_a-2023): cached extraction identifies a **different 45-page copy**, with title capitalization differences, a cover DOI ending at `dial.v77.i4`, cover pagination `1–1`, and a `MISSING` placeholder at the opening. It must not be substituted for the 47-page witness. These are draft-status indicators, not a verified revision chronology. Raw retrieval returned 403 and a screenshot attempt returned Cache miss.
- [Former-publisher journal page](https://www.philosophie.ch/dialectica): the retrieved web view says affiliation ended in early 2026 and links its open-access back issues. The [77(4) issue page](https://www.philosophie.ch/dialectica-77-4-2023) links https://assets.philosophie.ch/dialectica/dial.v77.i4.pdf; that target returned 403. Search-index and opened views of the issue/article pages differ; the opened article URL reported 404. Consequently this check cannot establish which article PDF is presently offered as final.
- [PhilArchive version record](https://philarchive.org/versions/BILARF-3): search-indexed repository metadata identifies version 1, uploaded **24 November 2025, 17:21:16 GMT**, under the complete DOI and pagination. The record's direct view and PDF at https://philarchive.org/archive/BILARF-3 were unavailable (403/cache errors). Its content, uploader, and identity relative to either publisher copy are unverified. This is a lead, not a recovered final version.

## Bounded correction/version checks

1. Raw Crossref [journal query](https://api.crossref.org/journals/0012-2017/works?filter=from-pub-date%3A2023-01-01&rows=1000): **47 of 47 returned records**, all dated 2023 or 2024. No title containing erratum/corrigendum/correction and no nonempty update/relation field. This does not cover an unregistered or unlinked correction.
2. Former-publisher article index and issue/DOI pages; exact-title/DOI searches with correction, erratum, and corrigendum terms. No relevant correction found. The article index is visibly incomplete for 77(4), so its absence carries little weight.
3. [Université de Lille publications](https://pro.univ-lille.fr/alexandre-billon/publications), institution-linked HAL and Academia pages, and author-site searches: no verified replacement for this article. The institutional list returned 30 records but did not list this title; linked views were partly unavailable. This is not an exhaustive author bibliography.

## Evidence limits and files

No target page was visually verified. Formula typography, footnote placement, and visual domain qualifications therefore remain open. Existing mathematical review locators are not promoted to visually checked text. No prior missing capture has been recovered or relabeled.

`crossref.json` and `crossref_journal_2023_onward.json` are genuine raw HTTP response bodies; their retrieval logs include exact URLs, headers, times, sizes, and hashes. `WEB_RECORDS_CAPTURED.json` contains selected tool-returned cached/search text, **not** downloaded HTML/PDF bytes. `WEB_OBSERVATIONS.json` records additional observations and query limits. Local SHA-256 identities are in `MANIFEST.sha256`; none is represented as a hash of an unacquired PDF.
