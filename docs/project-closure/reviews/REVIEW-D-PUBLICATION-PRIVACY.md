# Review D — publication and privacy reviewer

**Date:** 2026-07-20 · **Stance:** assume something private, fake, or overclaimed slipped through.

| # | Check | Result |
|---|---|---|
| D-1 | No private material | Git-grep sweeps + `validate_repo.py` banned-pattern checks: no absolute local paths, no session identifiers, no temp-session paths, no credentials/keys, no raw transcripts, no screenshots or images at all (binary-free tree except generated PDFs), no research-output dumps (`.output`/`.jsonl` filename ban). The private casebook and longitudinal record remain unpublished and are described as not independently auditable everywhere they are mentioned |
| D-2 | No internal model-process language in paper bodies | The four current paper bodies (manuscript, core, note, two companions) carry neutral provenance pointers; original headers preserved verbatim in `docs/provenance/document-history.md`. **Deliberate exceptions, by the immutability rule:** the two companion supporting-history files and the frozen terminology v0 spec retain their original headers (rewriting them would falsify hashes/history); each is labeled as history where indexed. Decision records and closure docs name the implementing model on purpose — that is provenance honesty, not process leakage |
| D-3 | No inaccessible evidence treated as public | Abstract, §1.4, §11.4, §13.4, §15.2, and the availability statement all mark the casebook/longitudinal record internal, private, non-auditable, motivation-not-validation; no quantitative claim rests on them |
| D-4 | No fake experiment | Corpus-wide: every study is READY TO RUN, NOT RUN; validators print non-empirical disclaimers; the terminology report and STATUS say so; power parameters are marked synthetic placeholders; deviation ledger empty with "no run has occurred" |
| D-5 | No license invention | No LICENSE file; STATUS/OPEN-DECISIONS state the open decision and default copyright |
| D-6 | No citation identity invention | No CITATION.cff; no author names, affiliations, or ORCID anywhere; `docs/CITING.md` gives commit-based interim guidance only |
| D-7 | No release-readiness overclaim | VERSION file: "Not a numbered stable release"; PDFs carry DRAFT status pages; STATUS keeps "not peer reviewed / draft" |
| D-8 | No broken build or links | CI nine-check suite green at this revision (hygiene, verdict semantics, notation, schemas, sources, cross-document, packet hash, manifest, PDF-source consistency); internal-link resolution is part of `validate_repo.py` |
| D-9 | Third-party rights | No copyrighted third-party text is reproduced beyond short attributed quotations rendered as "interpretation of the meaning" (Qurʾānic renderings) and standard bibliographic data; the embedded PDF fonts (DejaVu via matplotlib) are under an embedding-permissive free license; no private fonts embedded |
| D-10 | Fresh diff review against R1 | The full `git diff 5fdd526..HEAD` was reviewed commit-by-commit during construction; every changed public file is either a current-corpus normalization, a new R2 artifact, or an untouched historical record — no archive file, R1 decision record, R1 patch, or frozen v0 spec was modified (verified: `git diff 5fdd526..HEAD --stat -- archive/ docs/decisions/0001* docs/decisions/0002* docs/decisions/0003* terminology/orthemic-terminology-evaluation-spec.md` is empty) |

**Verdict:** publishable as a research-stage draft state; no blocking finding. Open publication burdens (license, identity, external submission) are owner-only and recorded in `OPEN-DECISIONS.md` / `UNAVOIDABLE-OWNER-ACTIONS.md`.
