# POST-SUBSTITUTION OPUS 4.8 CANDIDATE STATE
# NOT INDEPENDENTLY SIGNED OFF
# NOT APPROVED FOR MERGE

**Interruption record — PR #3 model-substitution containment**
**Date:** 2026-07-20 · **Containment model:** `claude-opus-4.8`

---

## 1. Provenance (two attributed observations, not adjudicated)

```text
present_thread_initial_internal_harness_claim:
  claude-fable-5

owner_observed_ui_substitution:
  claude-opus-4.8

current_containment_model:
  claude-opus-4.8
```

Neither observation is asserted over the other. This session has no access to platform routing state and makes **no adjudication** about which observation better reflects it. Work performed after the owner-observed substitution is **not** relabelled as Fable work; it is labelled post-substitution Opus 4.8 candidate work throughout.

A separate, older disagreement about the *implementing* R4 run (`implementing_run_internal_harness_claim` vs `owner_observed_ui_substitution`, recorded in `AUTONOMOUS-R4-STATE.json`) is untouched by this record.

## 2. What this record covers

The independent-review session was ordered to halt mid-flight. It had completed Phases A–F (committed and pushed) and was partway through Phase G/H (whole-corpus consistency and PDF rebuild, uncommitted) when containment was ordered. No sign-off was issued, no merge was attempted, and `main` was never touched.

## 3. Repository state at containment

| Fact | Value |
|---|---|
| Repository | `theislampill/orthemology` |
| PR | [#3](https://github.com/theislampill/orthemology/pull/3), **OPEN, still draft** |
| PR base | `main` @ `63d15ecfa` (`63d15ecf4aa50672265100b7d5620af764421862`) — **unchanged** |
| Remote `main` | `63d15ecf4aa50672265100b7d5620af764421862` — **never modified** |
| PR branch | `closure/r4-semantic-contract-source-integrity` |
| PR head at containment | `de19ccf4b3525ae536bb9bc163aefcd9f4bfedf8` |
| Merge state | `BLOCKED` (required check failing) |
| Required check `validate` at head | **FAILURE** |
| Quarantine branch | `quarantine/r4-pr3-post-substitution` |
| Force-push / history rewrite / squash / reset | **none performed** |
| Merge | **none performed** |

## 4. Work boundary

The boundary rests on the owner's contextual clue mapped onto commit timestamps. Repository evidence contains no model-routing record; see `interruption/commit-boundary.txt` for the method and its limit.

- **Last definitely completed pre-substitution phase:** **Phase D** — commit `00cf05d6` (2026-07-20T12:00:46-04:00), *and this is also the last commit whose CI was green*.
- **First definitely post-substitution action:** the Phase E integration work leading to commit `b2742d1` (12:06:22-04:00).
- **Uncertain material:** the precise instant within the 12:00:46 → 12:06:22 window. Nothing finer is claimed.
- **No file was begun before and completed after** the boundary.

### Exact command running when containment was ordered

```text
python - <<'PYEOF'   # sidecar source/PDF hash verification over artifacts/*.sources.json
```

It **completed**, printing `ALL SIDECARS CONSISTENT`. No follow-up command was launched. The next intended action — writing `PDF-AND-ARTIFACT-VERIFICATION.md` and committing Phase G+H — was **not** performed.

## 5. Post-substitution commits already pushed (preserved, not rewritten)

| Commit | Phase | Status |
|---|---|---|
| `b2742d172f69f15b8859a1a6395e2eae115cb236` | E — latent related-work integration; Decision 0015 amendment | pushed; **requires fresh Fable review** |
| `de19ccf4b3525ae536bb9bc163aefcd9f4bfedf8` | F — registry scope, CIR-1 split, ATH-3 downgrade | pushed; **requires fresh Fable review** |

Neither is rewritten or removed. **The entire range `00cf05d6..de19ccf4` is labelled as requiring fresh Fable reproduction and review before any merge.** PR #3 stays in draft.

## 6. Changed material at containment (uncommitted → quarantined)

| File | Boundary classification |
|---|---|
| `.github/workflows/validate.yml` | created after substitution (adds an internal-reference CI step) |
| `docs/reference-exemptions.yaml` | created after substitution (new) |
| `scripts/validate_internal_references.py` | created after substitution (new; **never run in CI, never run at any commit**) |
| `docs/current-state.yaml` | modified after substitution (regenerated) |
| `artifacts/orthemma-ortheme-systems-draft.pdf` + `.sources.json` | rebuilt after substitution |
| `artifacts/orthemic-core-reference-draft.pdf` + `.sources.json` | rebuilt after substitution |
| `artifacts/orthability-ground-of-intelligibility-draft.pdf` + `.sources.json` | rebuilt after substitution |
| `artifacts/orthability-divine-speech-athari-draft.pdf` + `.sources.json` | rebuilt after substitution |

Preserved artifacts under `docs/project-closure/r4/interruption/`:

| File | Purpose |
|---|---|
| `git-status-porcelain-v2.txt` | machine-readable status at containment |
| `git-diff-stat.txt` | 12 files, 8,797 insertions, 8,518 deletions |
| `git-diff.patch` | binary-capable patch (`--binary`), sha256 `38c7f7e20c033eb78111734725e6ac869f3d15c5fc83205154b94c83719f3cf7` |
| `changed-files.txt` | changed path list |
| `untracked-files.txt` | untracked path list |
| `commit-boundary.txt` | boundary reconstruction and its stated limits |
| `validator-results-known-at-interruption.md` | every validator claim with the state it ran against |

## 7. Validation state — no "all green" claim

**The pushed PR head is RED.** CI at `de19ccf4` fails the PDF byte-equality step because the Phase E commit edited the manuscript (§12.1) and the formal core (latent cross-reference) without rebuilding the committed PDFs. The rebuild that would fix it was performed locally but **never committed to the PR branch**; it survives only on the quarantine branch.

Green CI exists only at `00cf05d6` (Phase D, pre-substitution). Every other validator result in this session was observed locally against working trees that have since changed and **was not rerun during containment**. Per-test detail, with invalidation risk stated per row, is in `interruption/validator-results-known-at-interruption.md`.

## 8. Unfinished work

**Phase underway:** G (whole-corpus consistency) and H (PDF/artifact rebuild).

**Completed but uncommitted:** corpus scan for the superseded strict-soundness formula (none found in current normative prose); ghost-reference scan; the new internal-reference validator with its exemption registry (both tamper-probed locally); privacy/overclaim scans (clean); the four-PDF rebuild with sidecar consistency verified.

**Not started:** the `PDF-AND-ARTIFACT-VERIFICATION.md` report; Phase I (six adversarial passes); Phase J (sign-off, merge, fresh-clone verification). **No sign-off document was written and none is authorized by this state.**

**Known failure carried forward:** CI red at the PR head, as in §7.

**Source-status contradiction that was under investigation:** `ATH-3` (Ibn Taymiyyah, *Majmūʿ al-Fatāwā* vol. 12, "the words are the words of the Creator, and the voice is the voice of the reciter"). The R4 candidate registry recorded it `PRIMARY_TEXT_EXACT` with `wording_directly_checked: true`, while the companion prose labels the same locus `[via compilation]`. The post-substitution Phase F commit downgraded it to `COMPILATION_MEDIATED` on the conservative principle of taking the weaker of two conflicting evidence-access claims, and added a guard forbidding that contradiction class. **The adopted Atharī doctrine was not altered.** A fresh Fable session should re-adjudicate both the downgrade and the guard rather than inherit them.

**Next read-only action for a fresh Fable reviewer:** fetch the live PR, confirm head `de19ccf4` and base `63d15ecf`, read the failing CI run for that head (the PDF byte-equality step), then diff `00cf05d6..de19ccf4` and this quarantine commit before running any validator — i.e. reproduce the red state and the post-substitution range independently before trusting any claim in this record.

---

    THIS STATE IS PRESERVED AS A POST-SUBSTITUTION CANDIDATE.
    PR #3 REMAINS UNMERGED.
    A FRESH FABLE 5 SESSION MUST REPRODUCE, REVIEW, REPAIR, AND SIGN OFF
    BEFORE MERGE.
