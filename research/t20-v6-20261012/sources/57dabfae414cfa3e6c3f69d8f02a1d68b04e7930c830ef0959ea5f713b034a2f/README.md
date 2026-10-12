# Orthemology consolidation — recovered stage-two work and continuation supplement

**Overall status: PARTIAL — NOT APPROVED against the original exhaustive source-reading and repeated two-pass gate.**

Start with `REPORT.md` or `REPORT.html`. The report distinguishes the preserved interrupted work from the new continuation-information supplement. `CONTINUE.md` states the remaining work without narrowing the original request.

The package retains the available stage-one packet and interrupted stage-two working files under `preserved/`. Original files are not edited. `ledgers/preservation_inventory.json` records source and destination paths, hashes and handling. `ledgers/distribution_exclusions.json` identifies every packaging exclusion encountered. Font files and detected credential-bearing files are not distributed.

`research/continuation_information.md` develops and proves a bounded distinction relevant to apoautosis: retaining the ability to answer each future query using a query-specific observation is not the same as recovering a complete future-answer vector within one observation budget. It supplies a relation-valued covering formulation, a necessary fixed-target memory/probe bound, explicit counterexamples and a destructive-inquiry account.

`verification/verify_continuation_information.py` is a standalone ordinary-Python finite checker. Its output is in `verification/continuation_information_results.json` when execution completes. The checker has no network or source-repository writes. It refuses optimized Python. A passing run concerns only the enumerated synthetic models.

`verification/acquire_public_snapshot.py` records attempted public-byte acquisition, separately from connector observations. A failed request is retained as a failure. A historical pin is not silently labelled a newly verified current pin. A successful byte acquisition still earns no semantic-reading credit.

`audits/` contains two new coverage/adversarial cycles for this recovery candidate. Neither cycle approves the full consolidation. The earlier audit files remain preserved, not rewritten.

Integrity instructions:

    python verification/verify_package.py
    python verification/verify_continuation_information.py

Do not execute unrelated preserved source scripts without reading them and checking their stated scope. Do not infer full source reading, physical validity, independent novelty, empirical advantage, adoption or meniscus attainment from any generated inventory or test receipt.
