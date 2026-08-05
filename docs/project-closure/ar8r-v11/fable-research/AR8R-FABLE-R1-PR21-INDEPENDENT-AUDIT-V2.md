# AR8R Fable — PR #21 independent audit V2 (pre-repair reproduction)

Fable's independent reproduction of the Codex owner audit of PR #21, performed
before any repair edit, in a clean isolated worktree at the exact audited head.

```text
repository:        theislampill/orthemology
pull request:      #21
audited base:      7b05340e6fdb03a5f2700d05e385268acbc2fdfa (origin/main)
audited head:      defe5487ec454a6fda1b767591823f90b10a66a9
PR state at check: OPEN, draft, MERGEABLE, mergeStateStatus CLEAN
worktree:          fresh git worktree at the audited head, clean
changed files:     21 (all reviewed in the two-pass review that produced them)
```

## Reviewer identity and transport state

Reviewing model: Claude Fable 5 (`claude-fable-5`), pinned in client settings
during this audit. Earlier in the same working session the client's
safeguard-fallback feature (`switchModelsOnFlag`) switched individual turns to
Opus when flagged content was touched; each switch was owner-visible and
owner-reverted. Per the owner steer, any such fallback is classified as a
transport/reviewer-integrity interruption, not as a continuing or independent
reviewer. The Codex audit and the distinct fresh-context subagent review of
`c2ee904` were separate reviewers from this one.

## Mechanical reproduction at the audited head

```text
t299_finite_check.py:  361164 cases, 0 mismatches, exit 0,
                       result digest 462cd40854b9830e47c2c4da7ddc5a695735898f005626f30001adefd76d65a5
                       (byte-identical to the digest in the Codex receipt)
n1_transversal_packing_check.py: 7/7 checks true, exit 0
validate_repo.py:      exit 0
generate_current_state.py --check: exit 0
```

Lean: sources at this head are hash-identical to those rebuilt three times
already (Fable clean scratch build, distinct-reviewer rebuild in a second
scratch, Codex build): exit 0, `Build completed successfully (636 jobs).`,
14 declarations, 7 axiom-free / 7 standard-axioms.

## Visual PDF review — 61/61 pages independently inspected

Method: every page of every committed PDF rendered and visually inspected
(6 PDFs; 26 + 14 + 8 + 6 + 5 + 2 = 61 pages).

Agreement with the Codex page ledger: **complete**. Every enumerated defect was
independently confirmed:

- `orthemma-ortheme-systems-draft.pdf` p1 stranded "causes."; p2 isolated §1.5
  heading with dead space; p3 fragmented narrow two-column table with raw
  `O*(m; A)` syntax; pp4–5 ASCII flow diagram and raw `Succ_a`/profile blocks;
  p6 shattered four-column table; p11 and p13 raw status blocks; pp14–26 dense
  but no further clipping.
- `orthemic-core-reference-draft.pdf` p12 companion title beginning mid-column;
  pp13–14 large raw monospaced blocks.
- `orthability-divine-speech-athari-draft.pdf` p5 stranded route-specificity
  bullet with a large empty area before §7.
- `dynamic-orthing…`, `orthability-ground-of-intelligibility…`,
  `notation-gallery` — dense in places, no comparable structural breaks.

Additional Fable findings beyond the Codex ledger (same defect classes):

1. `orthemma…` p7: the typed-candidate-families table is fragmented in the same
   way as p6, and p7 carries two further raw blocks (`h = ⟨channel k; …⟩`,
   `mis-scoped pass ≡ …`).
2. `orthemic-core…` pp1, 8, 11 carry further raw monospaced blocks
   (`ι_n` embedding, `CorePath`/`ReqPath`/`Status_i`, `Compat_m`) — same class
   as the pp13–14 finding.
3. `notation-gallery` p2: the episode-signature display equation's last line
   (`Succ⟩`) is ragged far right; cosmetic only, recorded not repaired.

Accessibility: concur that none of the six PDFs carries a structure tree
(untagged); the pinned latexmk/pdflatex pipeline does not load a tagging
package. Disposition recorded in the layout repair report as an explicit
bounded deferral.

## Adjudication of the four Codex blocking findings

All four are **agreed** as merge-blocking on the audited head:

1. Unqualified proved/verified language inside `DERIVED_BUT_UNVERIFIED` packets
   — confirmed at the cited lines; a top-banner disclaimer does not bind
   quotable local claims.
2. Factual identity relations over `UNVERIFIED` source rows — confirmed;
   "Identical/Equivalent … inherits" is asserted while every row is
   `UNVERIFIED`.
3. Source-specific descriptions under a `SOURCE_LEVEL_UNVERIFIED` banner —
   confirmed; the banner quarantines the gate verdict but the descriptive
   sections still read as current authority.
4. PDF visual publication QA — confirmed page by page, with the additional
   instances above.

No disagreement with any Codex finding. Repairs proceed on the existing PR
branch with no force-push.
