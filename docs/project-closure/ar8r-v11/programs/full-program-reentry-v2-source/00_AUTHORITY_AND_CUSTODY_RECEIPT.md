# 00 — Authority and Custody Receipt

Generated: `2026-08-02T16:49:12Z`

## Operation boundary

This was a **read-only continuity, custody, and program-reentry operation**. It did not modify GitHub, `main`, the authorized T354 branch name, any pull request, any historical payload, any owner-adoption field, or the historical research ledger. It did not resume AR8R research or adopt a theorem.

## Live Git authority observed read-only

| Field | Observed value |
|---|---|
| Repository | `theislampill/orthemology` |
| `origin/main` | `cc91f41fec364ea3910b80d57252bb1e0a050278` |
| PR #15 | `MERGED` |
| Audited PR head | `b758c92d579772c10b793d380c6e4f347c2ca688` |
| Merge parents | `6273605aca275039fcc62f221bc49ec7205093b6`, `b758c92d579772c10b793d380c6e4f347c2ca688` |
| Observed branches | `main`, `codex/ar8r-recovery-integration-v8` |
| T354 branch | `NOT PRESENT` |
| Open pull requests | `0` |
| T354 pull request | `NONE` |
| GitHub mutation by this operation | `false` |

The attached repository snapshot has no `.git` directory. Therefore, the local checked-out branch, local HEAD, index, and working-tree status are **not observable from that archive**. Public read-only GitHub observation is recorded separately from archive custody.

## Bounded T354 result preserved exactly

| Field | Result |
|---|---|
| Terminal result | `BLOCKED_FOR_OWNER` |
| Blocking reason | `GITHUB_MUTATION_CHANNEL_UNAVAILABLE` |
| Authorized branch | `codex/ar8r-post-merge-owner-decisions-t354-repair-v1` — not created |
| Head SHA | none |
| Draft PR | none |
| Exact-head CI | not run |

No part of the bounded T354 task was rerun or modified here.

## Historical research authority

```text
historical substantive duration: 09:41:25.405101139
historical substantive seconds: 34885.405101139
latest historically closed segment: 357
theorem-origin authority: V5
historical checkpoint SHA-256: 660231b1d5a60f41ac1b5e6d0e2d9f79717e26bd79d6352bb92de0ad7f5b33e5
natural campaign closure: NOT_REACHED
```

No segment 358 was opened. Continuity time was not added to historical research time.

## Verified input custody

- `AR8R_POST_MERGE_VERIFIED_HANDOFF_V9.zip`: SHA-256 `7dcef75c2764442c383cc9f6abf971332d2d1d1a68183fdb009098967f3ebce3`; 154 entries; CRC/path-safety pass; internal `SHA256SUMS` pass.
- `orthemology-main(7).zip`: SHA-256 `ec5314442cc6212cad0cd5cd9fcdfb835567f4847830445c8f7529ea8422a04e`; 872 archive entries; 735 files; 9,866,333 uncompressed file bytes; CRC/path-safety pass; no `.git` metadata.
- `ten-proofs-main(1).zip`: SHA-256 `abdd3cabdf687bf493da2df85d6f7c77387ec56bef9a4d9d6b2c342505c7f09f`; 45 entries; CRC/path-safety pass.
- All 13 present attachments are byte-hashed and content-assessed. Twelve referenced inputs were not present and are explicitly marked unavailable; none was silently replaced.

## Current-main findings

- Current generated state is `R6` and retains the repository honesty boundary: research-stage draft; no external human peer review; no empirical validation; candidate terminology not community-adopted.
- Decisions `0001` through `0036` are present. Decisions `0037` and `0038` are absent.
- The AR8R V8 historical-status rule still says `current-candidate` on the old recovery branch despite PR #15 being merged. This reproduced defect is **not repaired here**.
- T150 proposal owner-adoption remains `PENDING`; T366 reconstruction owner-adoption remains `PENDING`.
- Historical T354 remains `BLOCKED_FORMAL_DEFECT` and byte-identical.
- The unresolved set remains exactly 22 identities and all remain insufficient-evidence blocks.

## Protected hashes

```text
T150 proposal:
9116750ee674d509e68941a8ff15ef1e2f792b9cfbb2df3e4dece9f67b3f4e29

T366 reconstruction proposal:
e5d374af56925e338df66a62f7ac08d0515689c0b068d61935d1e003c937f55a

historical T354 payload:
4ae7fe4807de3b961dc8fbec464d23738dc4fb58b94ca4af4f758aed316fd264
```

## Validation reproduced

The seven required repository validators were run against a disposable Git-index copy containing the exact archived files and passed. Direct execution from the extracted archive failed only where scripts required Git metadata. This is an engineering-conformance result, not mathematical consistency, source truth, empirical validation, external review, or theory adoption.

## Provenance firewall

Replacement is not exact recovery; reconstruction is not exact recovery; a repair theorem is not the historical theorem; owner adoption is not historical identity; Git merge is not theory adoption; static Lean inspection is not kernel verification; source presence is not source truth; formal nonentailment is not world-level falsity; profile blindness is not target nonexistence; and this continuity map is not a research result.
