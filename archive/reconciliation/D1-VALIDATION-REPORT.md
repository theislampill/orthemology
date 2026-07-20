# D1 VALIDATION REPORT

**Date:** 2026-07-19 · **Validator:** Claude Fable 5 (`claude-fable-5`), Thread A, resumed gate.
**No-research statement:** `/deep-research` was NOT invoked in this gate; no subagents or background workflows were launched; no external research was performed. The previously launched research task's partial artifact exists at `<private-temp>\tasks\<private-task>.output` (+ per-agent journal under `…\subagents\workflows\<private-task>\`) and is classified **INCOMPLETE / UNADJUDICATED** — interrupted by a rate limit (12 verifier/synthesis agents failed; synthesis never ran); no result was accepted or synthesized into any D1 artifact; not a D1 dependency; the Hume/metaortheme scholarship question is deferred to a future companion-research thread.

## 1. Source/candidate hash table

| Role | File | SHA-256 |
|---|---|---|
| canonical parent | `<workspace>\orthemic-core-formalization.md` | `18a693c54a87bcd818480c014a818642aa7b30c741c965241bc8557e1edddb5d` |
| canonical parent | `<workspace>\orthemma-ortheme-systems-revised-draft.md` | `7ac99acb22d805edcdcb725dffcd1f82d90c5979af43c68cb43bab191c1ea964` |
| canonical parent | `<workspace>\orthemic-multi-actor-conflict-note.md` | `53d347c8dcbe061aa1cc863f3fead8cde84fa2a458d42ee27384b406c454e40b` |
| candidate | `candidates\orthemic-core-formalization-v2-candidate.md` | `6e1238210da5426f8efd0cc6ddb87a0b29ec01cf62e895f1d1201b05aa22be4d` |
| candidate | `candidates\orthemma-ortheme-systems-revised-draft-v2-candidate.md` | `82321a312418d0f78448765ca1b3e6b599d443cd04b4402ea0b1b8d5d9713895` |
| candidate | `candidates\orthemic-multi-actor-conflict-note-v2-candidate.md` | `41111140184c6dbe0a7153bc08ebc93c897659c286462755757ea6c330f78adf` |
| patch | `D1-COMPLETE-DIFFS.patch` (28 hunks: 9/14/5) | `b8b73c048ca3466af3eb00c99c4adf0404a0bfc0cd8b3da6e9c33291ace25db8` |

**Canonical-unchanged proof:** all three parent hashes re-computed at gate start and gate end; both times identical to the Gate-H `CANONICAL-MANIFEST.json` rows (which this program verified against live files at Gate A). No canonical, state, index, manifest, or seal file was written in this gate.

**Independent diff regeneration:** before corrections, a freshly regenerated `git diff --no-index` of parents vs the interrupted candidates was **byte-identical** to the stored pre-interruption patch (`b25311539194eb5b0ac45eb62f7b23d1a83ae9cef41ed7c2848766c70cd6ace6`, 23 hunks — matching the expected 8/12/3). After corrections, the stored patch was regenerated from disk (never hand-edited); its hunk counts (9/14/5) were recomputed, not carried forward.

## 2. D1 scope classification

Per-hunk classification is in `D1-GROUND-TRUTH-CHANGE-LEDGER.md` §"D1 scope classification". Summary: all 28 hunks are D1-required, D1-forced, or declared status hygiene (banners); **one** pre-existing-issue bundle (the M1 `Π` content definition) was found and **removed** to `M1-PROFILE-SPACE-DEFINITION-OPTIONAL.md`; **zero** accidental scope expansions remain.

## 3. Residual-notation scan

**Before correction** (resumed-gate entry state), violations present: draft §9.3 "one case, one task"; draft §10.1 "actor/task indices"; draft §10.2 "actor/task index"; draft §10.3 `G(White, T)/G(Black, T)`; draft §10.4 `p̂_{A,White,t}/p̂_{A,Black,t}`, `G(White, T)/G(Black, T)`, "actor/task-indexed"; note header "actor/task indices"; note C4 `Ω_A/Ω_B` (×2 lines); note C5 `G(A), G(B)`; note C6 `T_A`, "A-indexed"; note §3 "task T; placements are task-indexed". **Total: 13 residual inconsistencies found.**

**After correction:** full-corpus scan for `O*_A | O*_T | I_T | Inst_T | Π_T | K_T | R_T | W_T | φ(A→B) | Ω_A | Ω_B | G(A | G(B | p̂_{A, | task-indexed | actor/task | one case, one task` returns **only** (a) definitional mentions inside the abbreviation-convention text itself, and (b) licensed single-analysis shorthand under an explicitly fixed `A` (complete table in the ledger §"Deliberate retained shorthand"). The note candidate returns zero hits. **13/13 corrected.**

## 4. Mandated validation tests

| # | Test | Result |
|---|---|---|
| 1 | One primitive; no dual-ground-truth equivocation | **PASS** — `Inst_A` / `O*(m; A)` is the only primitive form; `O*_A(m)` subscript form retired; every `O*_T` occurrence is convention text or licensed scope; §2.6 states "no second, task-only ground truth" |
| 2 | Task shorthand never used in a live multi-analysis context | **PASS** — §5.2/§9.3 composites, §5.3/§10 multi-actor, and the note all use full `O*(m; A)` / `A_α` forms and declare the prohibition locally |
| 3 | `A` always means analysis in formal notation | **PASS** — actors renamed `α, β` in all formal passages; prose "Player A/B" and `U_A+U_B` mapped by declared in-text conventions |
| 4 | Formal actors are `α, β` | **PASS** — verified by scan (no formal `Ω_A`, `G(A,…`, `φ(A→B)`, `W(A)` remain) |
| 5 | Every episode used for V1 has an analysis identity/version | **PASS** — `A` (identifier + version) added to both episode signatures; V1 and `⊨_μ` written against `O*(m; A(e))` |
| 6 | Multi-actor target sets inhabit analysis-indexed profile spaces | **PASS** — `G(α, T_α) ⊆ Π_{A_α}` in draft Def 13, core §5.3, note §3; `φ(α→β)` between `Π_{A_α}` and `Π_{A_β}` |
| 7 | No task-to-analysis bridging law introduced | **PASS** — none exists; draft Def 3 states the abbreviation-only rule explicitly |
| 8 | No canonical source file changed | **PASS** — hash proof above |

## 5. Cross-document consistency and structure

- Def 3 (draft), notation block (core), and glossary state the **same** convention (same licensed symbol list, same forbidden-context list drawn from the owner's clause 5).
- Episode signatures agree across core §2.2 and draft §8.2 (`α, w, A, T, t`), with `T = task(A)` glossed identically.
- Multi-actor notation agrees across core §5.3, draft §10, and the note (`α/β`, `A_α`, `G(α,T_α)`, `φ(α→β)`, `W(·)`).
- Markdown structure: banner blockquotes render standalone; all edited tables keep column counts; code fences balanced (verified by scan of edited regions); no heading levels changed.
- Completeness: every locus named in the resumed-gate instruction list was corrected or justified; every symbol in the owner's Phase-3 scan list was scanned corpus-wide.

## 6. Bundled fixes: accepted / rejected / deferred

- **Accepted (in D1):** stale core notation block repair (inseparable from clause-1 rewrite); actor renames (forced); banners (mandated).
- **Rejected from D1 (split out):** M1 profile-space content definition → `M1-PROFILE-SPACE-DEFINITION-OPTIONAL.md`.
- **Deferred:** O2/D3/D4/O3 edits, E1, E14 minors (incl. Def 7 `λ` weights), B4 citations, all H1 editorial items, metaorthemma (assessed separately; zero metaorthemma text in candidates).

## 7. Files changed during this resumed gate

`candidates\*.md` (3 — residual fixes, Π split-back, banners), `D1-COMPLETE-DIFFS.patch` (regenerated), `D1-GROUND-TRUTH-CHANGE-LEDGER.md` (rewritten), plus new: this report, `M1-PROFILE-SPACE-DEFINITION-OPTIONAL.md`, `D1-OWNER-REVIEW-PACKET.md`, `OWNER-METAORTHEMMA-PROPOSAL.md`, `METAORTHEMMA-DISTINCTION-ASSESSMENT.md`. Nothing else.

## 8. Disclaimer

These candidates are **not canonical, not publication artifacts, and claim no empirical validation and no terminology adoption**. Promotion requires owner approval of the diff, followed by the standing promotion procedure (apply → re-hash → index/manifest regeneration under a new seal — none of which occurred here).
