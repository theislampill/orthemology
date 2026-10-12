# P02 research checkpoint index

Start with `REPORT.md`, `RECEIPT.json` and `OBLIGATION_RESULTS.json`. Broader obligations U05, U08, CV-R, CV-C and Q1c are PARTIAL; ordinary work, finite execution and unexecuted Lean candidates are distinguished.

For mathematical content read `analysis/U05_MEASURE_SEMANTICS.md`, `analysis/U08_CORRESPONDENCE.md`, `analysis/CV_R_REFINEMENT.md`, `analysis/CV_C_COMPUTABILITY.md` and `analysis/Q1c_FINITE_PROBABILITY.md`. Primary comparisons and formal targets are in the remaining two analysis notes.

For boundaries read `NEGATIVE_FINDINGS.json`, `UNRESOLVED_DEPENDENCIES.json` and `provenance/PATCH_MAPPING.json`. Exact unchanged input records are in `inputs/packet/`; the original received ZIP is retained alongside that directory.

For later execution read `implementation_handoff/CODEX_HANDOFF.md`. The shell helper is NOT EXECUTED here and never automatically grants theorem or obligation PASS. Scripts under provenance describing this run are provenance, not permission to execute historical private paths or to modify canonical source.

For transport verification use `provenance/reopen_verify.py` with the delivered ZIP and detached seal. All archive members are checked, including the manifest's detached hash. The post-seal verification report is external to avoid circularly changing the archive it verifies.
