# D1 GROUND-TRUTH RECONCILIATION — EXACT CHANGE LEDGER (v2, post-interruption)

**Date:** 2026-07-19 · **Author:** Claude Fable 5 (`claude-fable-5`), Thread A · **Supersedes** the pre-interruption ledger version (which carried stale 7/13/5 conceptual hunk groupings; all counts below are recomputed from the regenerated machine diff).
**Governing decision:** owner **D1 = (d)** — analysis-relative primitive with strictly scoped task-relative abbreviation, under the owner's eight-point interpretation.
**Status:** PROPOSED. Canonical files untouched (re-verified this gate). All changes live in `candidates\`. Complete machine diff: **`D1-COMPLETE-DIFFS.patch`** (git unified diff, canonical → candidate). Nothing is promoted without owner approval.

## File identities and counts (recomputed after all corrections)

| File | Parent SHA-256 (= Gate-H manifest, re-verified) | Candidate SHA-256 | Lines (parent→cand) | Bytes (parent→cand) | Hunks | +/− lines |
|---|---|---|---|---|---|---|
| core → `orthemic-core-formalization-v2-candidate.md` | `18a693c54a87bcd818480c014a818642aa7b30c741c965241bc8557e1edddb5d` | `6e1238210da5426f8efd0cc6ddb87a0b29ec01cf62e895f1d1201b05aa22be4d` | 594→625 | 37,123→39,860 | 9 | +68/−37 |
| draft → `orthemma-ortheme-systems-revised-draft-v2-candidate.md` | `7ac99acb22d805edcdcb725dffcd1f82d90c5979af43c68cb43bab191c1ea964` | `82321a312418d0f78448765ca1b3e6b599d443cd04b4402ea0b1b8d5d9713895` | 869→883 | 81,934→86,455 | 14 | +45/−31 |
| note → `orthemic-multi-actor-conflict-note-v2-candidate.md` | `53d347c8dcbe061aa1cc863f3fead8cde84fa2a458d42ee27384b406c454e40b` | `41111140184c6dbe0a7153bc08ebc93c897659c286462755757ea6c330f78adf` | 166→185 | 9,611→11,156 | 5 | +46/−27 |
| **Total** | | | | | **28** | +159/−95 |

Patch: `D1-COMPLETE-DIFFS.patch`, SHA-256 `b8b73c048ca3466af3eb00c99c4adf0404a0bfc0cd8b3da6e9c33291ace25db8`, 49,409 bytes. (The pre-correction patch `b2531153…`, 23 hunks, was byte-identically reproduced by independent regeneration before being superseded.)

## Owner-clause → hunk map

| Owner clause | Hunks implementing it |
|---|---|
| 1. Primitive `Inst_A(m,o)`; profile `O*(m; A)` | draft Def 3; draft §2.6; draft Defs 8/9, aliasing row, §7 bullet, V1 row, glossary; core notation block; core `⊨_μ`; core V1 |
| 2. `A` explicit + versionable (component list) | draft §2.6 (`ver(A)`); core notation block; episode-record `A` rows |
| 3. Realism / four distinctions | draft Def 3 realism paragraph |
| 4. `O*_T(m)` local scoped shorthand only, extended to `Inst_T, Π_T, K_T, R_T, W_T` | draft Def 3 convention paragraph + §2.6 closing sentence; core convention block; core `Π_A`-shorthand gloss; glossary |
| 5. Shorthand forbidden in multi-analysis contexts | forbidden-context lists (draft Def 3; core block); draft §9.3 "one case, one analysis"; draft §10.1/§10.2/§10.3/§10.4; core §5.2 condition 1; core §5.3; note §1.2/§C4/§C5/§C6/§3 |
| 6. Episode record carries analysis identity + version; V1 against `A(e)` | core §2.2 signature + `A` table row + `T = task(A)` row; draft §8.2 signature + prose; core V1 + `⊨_μ`; draft §8.3 V1 row |
| 7. Task-relative readability preserved; abbreviation not a second ontology | deliberate no-changes list below |
| 8. No bridging law | none introduced; stated explicitly in draft Def 3 |
| (status hygiene) | 3 banner hunks (one per candidate) |

## D1 scope classification — every hunk

**Directly required by D1(d):** draft Def 3; draft §2.6; core notation block; episode-record `A` additions (core §2.2, draft §8.2); V1 restatements (core §4.1, draft §8.3); core `⊨_μ`; glossary `Inst_A` entry; `O*(m; A)` normalizations (draft Defs 8/9, aliasing row, §7 bullet); draft §2.7 `≢_A` (Def 7 subscript unification — the definition explicitly fixes `A`).
**Mechanically forced by D1(d):** actor rename `A/B → α/β` in every multi-actor formal passage (core §5.3; note §§1–3; draft §10.3/§10.4 role-label convention) — forced because `A` now formally names the analysis, making `φ(A→B)`, `G(A, T_A)`, `Ω_A`, `p̂_{A,White,t}` ambiguous; documented, revisable under D4. Also: core §5.2 and draft §9.3 composite condition ("one case, one analysis") — forced because task-sharing no longer individuates a single ground truth; multi-analysis declarations in §10.1/§5.3; core `Π_T`→`Π_A`-with-shorthand index change.
**Adjacent editorial correction (kept, flagged):** the three candidate-status banners (Phase-4 requirement); the core notation block's alignment of `p̂`/`Ô` with the core's own §2.2 (stale-block repair is inseparable from rewriting the block D1 must rewrite).
**Independent pre-existing issue (REMOVED from D1):** the full content definition of the profile space (M1) — split out to `M1-PROFILE-SPACE-DEFINITION-OPTIONAL.md`; the candidate retains only the D1-required index change.
**Accidental scope expansion:** none found after audit. (The pre-interruption candidate had bundled the M1 definition; corrected this gate.)

## Deliberate retained shorthand (licensed; complete list from the post-correction scan)

| Locus | Symbols | License |
|---|---|---|
| Core L46/51, L169; draft L114–121, L188, L865 | `Inst_T, O*_T, Π_T, K_T, R_T, W_T` | Definitional mentions inside the convention text itself |
| Core §2.2 table (L159–160) | `Π_T, K_T, R_T, W_T` | Episode-internal scope: the record now carries `A`; single analysis fixed by the episode itself |
| Draft §2.2/§2.3 (L138, L148) | `O*_T(m)` | Def 3's standing scope (single fixed `A`, §§2–9) |
| Draft §5 table (L303–306) | `Π_T, K_T, R_T, W_T` | Same standing scope |
| Draft §2.6 (L185) | `p̂_{A,α,t}(m)` | Explicit-`A` form — not shorthand |
| Note C5 | `U_A + U_B` | Declared prose player labels (in-text note maps A/B → α/β); utility is task apparatus, not a profile symbol |

## D1-forced renames (complete)

`I_T`→`Inst_A` (primitive), `O*_T`-as-primitive→`O*(m; A)`, `O*_A(m)`→`O*(m; A)` (single written form), `≢_T`→`≢_A` (Def 7), actors `A,B`→`α,β` (formal passages), `Ω_A/Ω_B`→`Ω_α/Ω_β`, `W(A)/W(B)`→`W(α)/W(β)` (schema `W(·)`), `G(A,T_A)`→`G(α,T_α)`, `φ(A→B)`→`φ(α→β)`, `Conflict_m/Compat_m(G_A,G_B)`→`(G_α,G_β)`, `p̂_{A,White,t}`→`p̂_{A_α,α,t}` (with declared White=α, Black=β), `p̂(e,α,T)`→`p̂(e,α,T_α)`, "one case, one task"→"one case, one analysis" (both files), "actor/task ind…"→"actor/analysis ind…" (draft §10.1/§10.2, note ×3).

## Residual issues intentionally deferred (NOT in this package)

O2 `PathwayAdequate` + "none entails another" (next-question material — adjacent text untouched); D3 verdict-index scheme (V4a/V4b, V3c); D4 full symbol table (`W(α)`→`Sch`, `Γ`, `Rep`, `θ`, `st`, `Ω` superscripts); O3 compaction example; E1 §1.5 fix and all H1 editorial batch items; Def 7 dangling `λ` weights (m1) and E14 minors; B4 citations; M1 optional patch (separate file); metaorthemma proposal (separate assessment; **no metaorthemma text in these candidates**).

## Acceptance checks

See `D1-VALIDATION-REPORT.md` — all eight mandated validation tests pass on the corrected candidates.
