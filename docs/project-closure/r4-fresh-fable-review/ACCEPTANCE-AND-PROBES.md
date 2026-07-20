# R4 PR #3 — Fresh Fable Full Acceptance Testing and Adversarial Probes (Phase E)

Session surfaced model at this phase boundary: `claude-fable-5`; no
substitution observed.

## Full workflow suite

Every step of the review branch's `.github/workflows/validate.yml` (26 steps,
the quarantine workflow including the internal-reference step) was executed
in order from the working tree with Python 3.11.9 and the pinned dependency
line: **0 failing steps**. The suite is re-run against the exact final commit
before sign-off; no "all green" claim is made for any earlier tree than the
one recorded in FABLE-REVIEW-SIGNOFF.md.

## Tracked-cache check

Added as `validate_repo.py` check 0 (`git ls-files` free of
`__pycache__`/`.pyc`/`.pyo`), probed below (P10).

## Adversarial probes beyond the committed fixtures

Each probe mutates the tree, requires the responsible check to FAIL, then
restores and requires green. "PROBE-OK" = the check failed as required.

| # | Probe | Responsible check | Result |
|---|---|---|---|
| P1 | README state-marker tamper (decision-range) | validate_current_state | PROBE-OK |
| P2 | file added into frozen pilot0 packet | freeze_pilot0 --check | PROBE-OK |
| P3 | citation of a nonexistent script in docs | validate_internal_references | PROBE-OK |
| P4 | external exemption shadowing a local path | validate_internal_references (new hardening) | PROBE-OK |
| P5 | manifest hash flip | validate_repo | PROBE-OK |
| P6 | superseded strict-soundness formula reintroduced in a NEW yaml, ASCII-paraphrased | validate_decision_dependencies (Phase B hardening) | PROBE-OK |
| P7 | timezone-naive `decision_time` in a committed example | validate_cross_record_semantics | **initially PROBE-BAD → repaired → PROBE-OK** (see below) |
| P8 | source-status row outside declared families | validate_source_status | PROBE-OK |
| P9 | committed PDF byte tamper | build_pdfs --check | PROBE-OK |
| P10 | force-added `.pyc` under scripts/ | validate_repo check 0 | PROBE-OK |

## P7 finding and repair

A naive `decision_time` (time-of-day, no offset) on a verdict record's
objectivity index passed both layers: the schemas declare no `date-time`
format (and the JSON Schema library does not enforce formats by default), and
the semantic layer parsed only the fields its orderings currently consume.

Repair: `validate_cross_record_semantics.py` now sweeps every bundle
recursively — any string value under a timestamp-named key (`*_time`,
`effective_from`, `declared_at`, `expiry`, `calibration_expiry`) that carries
a time-of-day must parse as a timezone-aware ISO-8601 instant. Pure dates
(no clock time) remain legitimate coarser-granularity values, and
prose-valued keys (e.g. `recovered_from`) are deliberately outside the key
set. The sweep lives in `collect_issues`, so the negative-fixture harness
inherits it.

Pinned by standing fixture `tests/invalid/I45-naive-decision-time.json`
(schema-valid by design; flagged by cross-record semantics). Post-repair:
examples green, I42/I45 both rejected at the semantic layer, mutation suite
green (0 unjustified survivors), full suite green.
