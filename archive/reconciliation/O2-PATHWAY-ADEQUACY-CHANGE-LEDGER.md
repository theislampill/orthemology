# O2 PATHWAY ADEQUACY — CHANGE LEDGER

**Date:** 2026-07-19 · Claude Fable 5 (`claude-fable-5`), Thread A.
**Governing decision:** owner **O2 = (a)** — result-free pathway core with a non-factive procedure/reference-class truth-conduciveness verdict — under the owner's controlling interpretation (§1–§8 of the decision message).
**Layering:** applied on top of the frozen D1+M1 stage (`candidates\d1-m1-stage\`: core `dab3a21b…`, draft `1a46764c…`, note `41111140…`). D1 and M1 patches/ledgers preserved unchanged.

## Identities

| Artifact | SHA-256 | Lines / bytes |
|---|---|---|
| core candidate (D1+M1+O2) | `e22e2c51d22258baef634f21af8d9d6b560953456c891ddd362a5dd8f22300ca` | 776 / 51,939 |
| draft candidate (D1+M1+O2) | `a96c3541b3d3b575b1cfd324e6d18132073304c86cdb68f00dd5e21ae7679e39` | 887 / 91,521 |
| note candidate | `41111140184c6dbe0a7153bc08ebc93c897659c286462755757ea6c330f78adf` — **unchanged** (scanned; no O2 reference found) | 185 / 11,156 |
| `O2-PATHWAY-ADEQUACY-INCREMENTAL-DIFFS.patch` (D1+M1 → D1+M1+O2; 2 files, 8 hunks; core +142/−35, draft +13/−11) | `a82e71837fb43a11072904ff0a2cdaedb767f659b8953a7f1905adacdf8e3771` | — / 31,724 |
| `CUMULATIVE-D1-M1-O2-DIFFS.patch` (canonical → D1+M1+O2; 3 files, 36 hunks) | `9033da7e8222224985123f552881f03d18e45b88e19fb15efe4f0220e3a154a3` | — / 85,803 |
| `tests\verdict-fixtures.json` + `scripts\validate_verdict_semantics.py` | hashed in the validation report | — |

## Owner-clause → hunk map

| Owner clause | Implemented by |
|---|---|
| §1.1 V1 result-side, never a conjunct | Core V1 bullet sentence; draft V1 row sentence; CorePath exclusion |
| §1.2 V2b^proc (non-factive, RelSpec_q, no post-hoc reference class, one result insufficient) | Core V2b^proc bullet (full RelSpec list); draft V2b^proc row (compressed) |
| §1.2 V2b^tok (factive claim-wise, aggregation caveat, excluded from core, not sole carrier of token-local procedural defects) | Core V2b^tok bullet; draft V2b^tok row |
| §2 independence-claim correction + implication table | Core §4.1 header rewrite + declared implication/dependency table (9 rows); draft §8.3 header (points to core table); residual bare-"V2b" mentions updated (core trace sentence, V3d bullets ×2, status-ledger line) |
| §3 result-free CorePath incl. V3c; V4b advisory | Core §4.1 CorePath block; draft §8.3 header |
| §4 governed applicability (ReqPath derived; minimum rules; N/A reasons; "not tested" ≠ "not applicable") | Core §4.1 ReqPath block; core §2.2a applicability paragraph rewrite |
| §5 four-valued Status + Adequate/Defective/Undetermined; matrix applies only after resolution | Core §4.1 status block; core/draft §-matrix preambles |
| §6 corrected four cells; `AdequatePathError`; `JustifiedMiss` non-redundancy note; no formal "blameless" | Core §4.2 matrix; draft §8.4 matrix |
| §7 fixtures F1–F5 | Core §4.2 fixtures table; draft §8.4 pointer; `tests\verdict-fixtures.json` |
| §8 V6 vs V2b^proc distinction, no blanket independence | Core V6 bullet addition; implication-table row |

## Deliberate no-changes / deferrals

Note candidate untouched (no O2 content). D3 renumbering NOT performed (V2b^proc/V2b^tok labels provisional; V3c lettering note stands). D4 symbol normalization untouched. O3 compaction placement untouched. Terminology, companion, citations, experiments untouched. Stage archives (`d1-stage\`, `d1-m1-stage\`) frozen with their historical text. The core Gate-B provenance blockquote (historical) retains its original verdict-vector list per the standing no-rewrite rule.

## Remaining open issues

D3 (verdict-index scheme/lettering: V4a/V4b naming in draft §8.3 still "V4" with parenthetical; V3c/V2b^proc/V2b^tok final labels); D4 (symbol table); O3 (compaction example); E1/H1 editorial batch; B4 citations; M1-optional Π_A definition patch (separate authorization); terminology/companion/publication gates.
