# AR8R V11 campaign reconciliation and publication-boundary proposal

**Date:** 2026-08-03 · **Authority:** V11 repository-reconciliation proposal ·
**Status:** owner adoption pending · **Preserves:** Decisions 0001–0036 and the
V8 recovery packet.

This is not a numbered repository decision. A future numbered decision requires
a real pull-request allocation and owner review.

## Proposed rule

Campaign closure is a derived cross-ledger judgment. A terminal campaign summary
may not override unresolved, partial, contradictory, pending, blocked, or
unaudited records retained by its theorem, burden, candidate, premise, rival,
audit, repair, source, dependency, or admission owners.

A zero-open-burden claim is valid only when:

1. the set of controlling lower-level records is declared;
2. every declared record is parsed and reconciled;
3. every burden has an explicit terminal transfer or disposition;
4. duplicate bytes and renamed theorem-family instances receive no independent
   evidential or novelty credit;
5. blocking findings and superseded versions remain visible;
6. the computed open count is zero; and
7. any owner-gated acceptance has actually occurred.

A self-authored summary, validator, or archive may establish structural
consistency. It cannot establish philosophical validity, historical originality,
source fidelity, external peer review, empirical validation, terminology
adoption, natural closure, or owner acceptance.

## Relation to Definition 13

Definition 13 remains the episode-level rule: an episode record cannot assert
closure over an unresolved residual unless the same bundle explicitly represents
and convicts the false closure.

This proposal adds a distinct campaign-level rule. Even if each individual
record is locally well formed, a campaign summary is invalid when it suppresses
contradictory states distributed across separate authoritative ledgers. Local
schema validity therefore does not imply global campaign reconciliation.

## Public status classes

V11 uses these proposal outcomes:

- `PUBLIC_INTEGRATE`: exact or sufficiently audited bounded material proposed
  for a public packet;
- `PUBLIC_SUMMARY`: non-verbatim status or custody information proposed for
  public research memory;
- `DEFERRED_INSUFFICIENT_AUDIT` and `DEFERRED_OWNER_ADOPTION`;
- `BLOCKED_FORMAL_DEFECT`;
- `SUPERSEDED_EXACT_VERSION` and `DUPLICATE_EXACT_BYTES`;
- `PRIVATE_LOCAL_EVIDENCE`;
- `UNAVAILABLE_CONTEXT_ONLY`.

A hash proves byte custody only. Reconstruction, replacement, and historical
recovery remain separate provenance classes.

## Implementation boundary

The V11 validator checks reconciliation arithmetic, terminal dispositions,
publication/privacy compatibility, supersession, and duplicate-credit
constraints. It does not adjudicate the truth or originality of the research.
No historical AR8R duration, segment, theorem identity, or natural-closure
status is changed by this proposal.
