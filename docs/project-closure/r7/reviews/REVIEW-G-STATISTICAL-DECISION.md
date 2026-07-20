# R7 Review G — statistical / decision-rule audit

Surfaced model: `claude-opus-4-8`. Posture: declared endpoint not computed; p without multiplicity; null rescued by observed power; failed run dropped; manual outcome despite frozen rules; synthetic mistaken for evidence.

- AURC removed from the FCSP-2 analysis (declared-not-computed) — **DEFEATED** (smoke test asserts every declared endpoint appears). Holm multiplicity over the two primaries is present in both packets; there is NO observed-power computation anywhere (pre-run fixed sensitivity only); failed item-repeats are recorded and gated, never dropped; `decide()` executes the frozen rules mechanically and is unit-tested (supports / does-not-yet / harm / named-inconclusive); synthetic runs adjudicate nothing (unit-tested). No blocking findings.
