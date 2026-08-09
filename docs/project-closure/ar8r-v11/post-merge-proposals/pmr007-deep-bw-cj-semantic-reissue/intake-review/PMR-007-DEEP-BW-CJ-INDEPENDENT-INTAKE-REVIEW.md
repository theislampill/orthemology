# Independent intake review — PMR-007 Deep BW–CJ V1

**Verdict:** `BLOCK_V1_AND_V2_REPAIRED_TO_BOUNDED_V3_GAP`

The V1 semantic reissue truthfully records that its original ephemeral files
were lost. Its 40-file public archive is byte-intact. Its consolidated checker,
however, contains two load-bearing false-pass paths:

- Deep CI initializes `matched_twins: 20000` and `twin_failures: 0` but never
  constructs or checks a twin;
- Deep CJ does the same for `personal_impersonal_twins`.

Running V1 on Windows also rewrites its result file with CRLF bytes, so a
cross-platform rerun does not preserve the archived LF result hash even though
the parsed JSON object is unchanged. This is a checker-output portability
defect, not a defect in the frozen archive's original byte custody.

The repository-created V2 attempt:

1. executes 20,000 exact-profile/different-target fibre collisions for CI;
2. executes 20,000 fittingness-sensitive, payoff-independent
   personal/impersonal target-expansion collisions for CJ;
3. executes a profile-perturbation negative control for every twin;
4. executes a same-target negative control for every twin;
5. requires every load-bearing counter to be observed rather than prefilled;
6. serializes its result as UTF-8 with LF newlines.

An independent rereviewer correctly rejected this as tautological repetition:
the constructed twins satisfy the checked predicates by definition, and
repeating them 20,000 times is not independent corroboration.

V3 preserves that failed attempt, retains BW–CH's bounded results, and replaces
CI/CJ with exhaustive declared-signature enumeration. It independently checks
target-leak, profile-change, and same-target controls; rechecks both CJ
eligibility predicates on every twin; and kills OR, ignored-target, and
identity-only predicate mutants. Its authority ceiling remains narrow:

```text
BW–CH: GAP — bounded proposal candidates; no adequate per-result independent rereview
CI: GAP — conditional target-fibre countermodel repaired; architecture implementation unverified
CJ: GAP — conditional target-fibre countermodel repaired; architecture implementation unverified
historical identity: NONE
owner adoption: PENDING
external review: OPEN
repository scientific adoption: NONE
general novelty: 0
integrated champion: NONE
meniscus: MENISCUS_NOT_REACHED
natural closure: NOT_REACHED
```

V3 is a constructed finite-signature witness, not an architecture experiment,
an empirical replication, or an independent proof of the surrounding proposal.

The original V1 audit and rereview files are summary-level regenerated custody
copies, not recovered per-result review packets. No top-line `ADMITTED_*` token
inside frozen V1 source bytes overrides this outer disposition.
