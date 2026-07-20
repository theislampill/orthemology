# R6 — Read-Only Reproduction Report (Phase A)

Date: 2026-07-20. Session surfaced model: `claude-fable-5`; no substitution
observed. Historical model observations preserved, unadjudicated.

## A1. Topology

Live `main` = `6df15cbd3c2ce851de3d968207212ead86ecbf25` — equals the supplied
archive's recorded revision; archive SHA-256 `581a693c…b3002` matches the
audit record. 298 tracked files. Branch protection: required `validate`,
strict, no force-push/deletion. Latest main Actions run 29768058419: success.
Decision range 0001–0017.

## A2. Complete current suite

Every step of `.github/workflows/validate.yml` run in order from the fresh
clone (Python 3.11.9, CI dependency line): **28 scripted steps, 0 failures**
(the audit's count of 29 includes the pip-install command), including the
mutation suite (1,813 mutants / 27 families / 0 unjustified survivors) and
the deterministic PDF byte-equality rebuild.

## A3. Finding matrix (audit `orthemology-r5-independent-audit-and-r6-findings.md`)

| # | Finding | Classification | Evidence |
|---|---|---|---|
| 1 | no false-closure benchmark packet | **reproduced** | `experiments/` contains only `README.md` |
| 2 | no episode-reification E1–E5 packet | **reproduced** | same |
| 3 | OPEN-DECISIONS says every packet instrument-ready | **reproduced** | burden 3: "Every packet is INSTRUMENT-READY, NOT RUN" |
| 4 | manuscript §13.1 calls the unbuilt design preregistered | **reproduced** | "the preregistered false-closure / selective-prediction benchmark"; "Decision rule — three outcomes, preregistered"; "as preregistered" (§16); no registry record exists |
| 5 | Pilot-0 v1 = feasibility only, no adoption/retirement | **reproduced** | v1 protocol: feasibility/instrumentation pilot |
| 6 | Pilot-0 v2 gives adopt-candidate/reject/undetermined | **reproduced** | EXECUTION-SPEC.md three-outcome rule |
| 7 | v2 calls margins pre-registered without stating them there | **reproduced** | "pre-registered margins" phrasing; numeric margins absent from that spec |
| 8 | STATUS points current readers at R2 sourcing ledgers | **reproduced** | STATUS bullet names `docs/sourcing/SOURCING-LEDGER.md` + companion ledger as the broader sourcing surface |
| 9 | R3 ledgers state they supersede the R2 statuses | **reproduced** | R3 ledger headers |
| 10 | neither companion has a References section | **reproduced** | zero `## References` headings in both papers |
| 11 | CI labels partially unconstrained deps "pinned" | **reproduced** | step installs unpinned pyyaml/jsonschema and a pypdf range |
| 12 | residual "internally consistent specification" wording | **reproduced** | manuscript §15.1 (with the correct no-proof disclaimer elsewhere) |

M1–M4 (closed readiness vocabulary; distinct packet identities; the same
§15.1 wording; the record-N-attests-merge-N−1 pattern needing one
documentation note) — all **reproduced** by inspection.

No repair was begun before this report was written.
