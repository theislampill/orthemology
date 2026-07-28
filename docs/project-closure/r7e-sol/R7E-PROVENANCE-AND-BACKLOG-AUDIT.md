# R7E provenance and backlog audit

**Status:** SOL INDEPENDENT REVIEW CANDIDATE — NO SIGNOFF OR MERGE READINESS.

This record supersedes the R7E workflow and backlog claims for current review
purposes without rewriting either historical input. The preserved R7E state is
an implementing-run account. The preserved backlog is a lossy historical
candidate list. Their bytes remain unchanged.

## Repository reconstruction

The preserved Markdown contains exactly 221 legacy rows, but only 172 unique legacy IDs.
There are 49 reused occurrences across 19 duplicate legacy IDs. The attributed
implementing run reports sixteen rejections, while the repository preserves
only eight rejection records, all truncated.

`ORTHING-CANDIDATE-LEDGER.json` therefore assigns every parseable survivor-row
occurrence one immutable ID derived from its stable source line. It retains the
legacy ID separately, so duplicate history is visible rather than normalized
away. Each row preserves its legacy target text as truncated and unresolved.
The ledger does not reconstruct missing proposal prose, exact loci, sources,
agent reports, reviewer rationales, or rejection text.

The repository does not contain the workflow journal, per-agent reports, or
full candidate drafts. Those artifacts remain `missing`. The reported 36
agents, 12 + 12 + 12 phase shape, zero errors, 4.9M subagent tokens, 237
candidates, 221 survivors, 99 keep, 122 bound, and 16 rejected remain
`implementing-run-attributed`; they are not independently reconstructed.

## Supplied attachments

The supplied REBAKE and maximal-trajectory files were read entirely and their
hashes are recorded in `R7E-INPUT-PROVENANCE.json` as
`attachment-observed`. Their identity as the exact artifacts available to the
original R7E run is `unresolved`: no independently checkable binding connects
the observed files to that run. They are not copied into the repository and
are not promoted to repository-verified sources.

## Evidence and review boundaries

Repository verification establishes file identity, parseable row occurrence,
and the eight preserved rejection bullets. It does not establish the truth of
agent-generated candidate prose or screening outcomes. Agent-generated prose
is not scholarship. An agent-claimed sourcing label is not source verification.
A survivor or backlog row is not correctness, is not approval, is not
independent review, and is not merge readiness.

The immutable ledger is complete only with respect to the 221 parseable
survivor-row occurrences in the preserved Markdown. Overall R7E provenance is
explicitly incomplete because the journal, reports, drafts, eight rejection
records, and original-run attachment bindings remain missing or unresolved.

Later-crosswalk unknowns remain explicit:

- Turn identity is not orthing identity, and session identity is not episode identity.
- Episode IDs do not prove independent observations.
- Retrospective reconstruction is not live capture.
- No missing rejection record is inferred.
- Current Sol evidence is not inserted into the original R7E t1 evidence state.
- No single sound/unsound field replaces defect-locus accounting.
- No recurrence is claimed without a controlled fingerprint or distinct-source accounting.

## Disposition

R7E-SOL-F002 is resolved only as a truthful current-state qualification: the
statistics are durably retained as implementing-run attribution and cannot be
promoted by the validator. R7E-SOL-F003 is resolved only as occurrence-level
accounting: all parseable rows map exactly once, while truncation and absent
records remain explicit. Neither resolution establishes source verification,
semantic correctness, independent signoff, or readiness to merge PR #12 or
any parent PR.
