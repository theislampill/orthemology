# O2 VALIDATION REPORT

**Date:** 2026-07-19 · Claude Fable 5 (`claude-fable-5`). No deep-research, no subagents, no sourcing, no experiments in this gate. The deterministic validator below is a consistency check over declared fixture data — **not an empirical experiment**.

## Hash table

| Role | File | SHA-256 |
|---|---|---|
| pre-O2 stage | `candidates\d1-m1-stage\` core / draft / note | `dab3a21b860a483adc3226690cdefd081c1cf95aca9e3465cf2a029f2b8cfdc9` / `1a46764c1afcb75188de363fac6316af4d3561a292c9294b60276e6eb39f8d08` / `41111140184c6dbe0a7153bc08ebc93c897659c286462755757ea6c330f78adf` |
| D1+M1+O2 candidates | core / draft / note | `e22e2c51d22258baef634f21af8d9d6b560953456c891ddd362a5dd8f22300ca` / `a96c3541b3d3b575b1cfd324e6d18132073304c86cdb68f00dd5e21ae7679e39` / `41111140…` (unchanged) |
| canonical parents (pre-promotion, re-verified) | core / draft / note | `18a693c54a87bcd818480c014a818642aa7b30c741c965241bc8557e1edddb5d` / `7ac99acb22d805edcdcb725dffcd1f82d90c5979af43c68cb43bab191c1ea964` / `53d347c8dcbe061aa1cc863f3fead8cde84fa2a458d42ee27384b406c454e40b` |
| patches | incremental / cumulative | `a82e71837fb43a11072904ff0a2cdaedb767f659b8953a7f1905adacdf8e3771` / `9033da7e8222224985123f552881f03d18e45b88e19fb15efe4f0220e3a154a3` |

## Machine-checkable validation

`scripts\validate_verdict_semantics.py --fixtures tests\verdict-fixtures.json --hash-manifest tests\pre-promotion-hashes.json` → **29 checks, 0 failures**, covering all 14 mandated items:
1 V1 ∉ CorePath ✓ · 2 V2b^tok ∉ CorePath ✓ · 3 V4b ∉ CorePath ✓ · 4 V3c required iff MetaTok≠∅ ✓ · 5 V2b^tok_q → V1_q on every fixture claim ✓ · 6 V2b^proc non-factivity witnessed (F3) ✓ · 7 all four resolved cells satisfiable ✓ (F1 correct+adequate, F2 correct+defective, F3 incorrect+adequate, F4 correct+defective-via-V3c; compound incorrect+defective verified on the deterministic F2 variant with V1=fail) · 8 undetermined required verdict ⇒ not adequate (F5) ✓ · 9 every N/A has a recorded reason ✓ · 10 unevaluated = undetermined, never N/A ✓ · 11 F2 = correct+defective ✓ · 12 F3 = incorrect+adequate ✓ · 13 F4 = correct+defective through V3c alone ✓ · 14 canonical parents match recorded pre-promotion hashes ✓.

## Declared implications (exact, complete)

`V2b^tok_q(e) → V1_q(e)` (definitional, factive, claim-wise) — the ONLY entailment introduced. Explicit non-entailments: V2b^proc ↛ V1; V3d ↛ V1; PathwayAdequate ↛ V1; V1 ↛ PathwayAdequate; V6 ↮ V2b^proc; PathwayAdequate ↮ ¬PathwayDefective (undetermined third state). The full verdict vector was inspected: no other definitional implication is introduced; pairwise independence is nowhere claimed.

## Scope audit

All 8 incremental hunks map to the O2 clauses (ledger map); zero unrelated fixes; D3/D4/O3/terminology/companion/citation content untouched; note candidate byte-identical to stage. Whole-corpus scan for bare `V2b` (excluding `^proc`/`^tok`): remaining live-candidate occurrences are only the deliberate historical/supersession references (Gate-B provenance blockquote; the "supersedes the earlier parenthetical" note) — 5 residuals were updated (core trace sentence, core V3d, core status ledger, draft V3d; draft §8.5 rewritten).

## Structure checks

All edited tables retain column counts; code fences balanced in edited regions; banners intact; candidate completeness: every §7 fixture present in both the core §4.2 table and the machine fixtures; §5/§6 predicates (`AdequatePathError`, `JustifiedMiss`) defined exactly once.

## Files changed in this gate (O2 phase)

`candidates\` core + draft (O2 edits), `candidates\d1-m1-stage\` (frozen copies, new), both patches, `tests\verdict-fixtures.json`, `tests\pre-promotion-hashes.json`, `scripts\validate_verdict_semantics.py`, this report, the O2 ledger, the O2 owner packet.

## Disclaimer

Candidates claim no empirical validation and no terminology adoption; the fixtures are definitional satisfiability witnesses, not measurements. Promotion (below, same gate) is governed by the owner's conditional authorization; publication honesty statements live in the public STATUS.md.
