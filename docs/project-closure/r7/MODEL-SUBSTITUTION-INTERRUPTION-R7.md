# R7 — MODEL SUBSTITUTION INTERRUPTION RECORD

**POST-SUBSTITUTION OPUS 4.8 CANDIDATE STATE**
**NOT INDEPENDENTLY SIGNED OFF**
**NOT APPROVED FOR MERGE — LEFT AS A DRAFT PR FOR GENUINE-FABLE / OWNER REVIEW**

Date: 2026-07-20.

## What happened

The R7 pass began under the controlling instruction
`fable-r7-orthemology-noetic-application-and-experiment-validity-tieoff.md`,
which requests model **Fable 5** and carries a MODEL_PROVENANCE_CHECKPOINT:
if substitution away from Fable 5 appears, stop before the next
merge/push/PR-state-mutation, preserve the exact state, create a durable
interruption record, and do not merge.

Mid-pass the owner surfaced, in chat, an observed substitution to
**Opus 4.8** ("you switched from Fable to Opus"). The current session's
environment independently surfaces `claude-opus-4-8`. This session therefore
attests its **own current surfaced identity as `claude-opus-4-8`** and stops
attesting Fable 5.

## Attributed observations (preserved, not adjudicated)

```text
present_session_surfaced_harness_identity (after owner override): claude-opus-4-8
earlier_in_this_thread_this_session_attested:                     claude-fable-5
owner_observed_substitution:                                      claude-opus-4-8 (Fable -> Opus)
```

Earlier R4–R6 passes in this project self-attested `claude-fable-5` and were
merged to `main`. This record does **not** adjudicate or rewrite those
historical attestations; it only records the owner's current observation and
this session's honest current identity. The recurring
"self-identified-as-Fable-while-running-as-Opus" provenance question is a
standing project concern (see the R4 interruption record and the recovery
memory); this record adds one more attributed observation to that lineage
without resolving it.

## Owner authorization for continuation under the substitute

The owner explicitly authorized continued work under the substitute, bounded:

```text
"continue; you switched from Fable to Opus; so you do NOT have permission to
Merge; any work MUST be in a branch/PR and CANNOT push to main"
```

Adopted constraints for the remainder of R7 under Opus 4.8:

1. all work stays on branch `closure/r7-noetic-application-experiment-validity`;
2. the branch may be pushed and a **DRAFT** PR opened (the owner-designated vehicle);
3. **no merge**, **no push to `main`**, **no ready-for-merge / auto-merge state change**;
4. commit trailers switch to `Co-Authored-By: Claude Opus 4.8` (avoid a false-Fable record);
5. no subagents / background workflows (controlling instruction; sequential only);
6. no empirical run, no external model call, no registration, no term adoption (unchanged).

## Disposition

R7 engineering (DAEE typed noetic-application crosswalk + notation firewall +
fixtures; FCSP-2 / ER-2 methodologically valid packet rebuilds; methods gate;
document/state reconciliation; adversarial reviews) is completed under Opus
4.8 and delivered as a **draft PR**. Final sign-off and the protected merge
are **left to a genuine-Fable session or the owner**, who should re-verify
from a clean clone before merging. Nothing in R7 reaches `main` under this
substituted session.
