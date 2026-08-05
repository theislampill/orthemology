# PR #21 — source-verification receipt V2 (Codex findings 2 and 3)

## Finding 2 — literature identity over unverified rows

**Option taken: (2), retain rows as `UNVERIFIED` and rewrite the relations.**
Option (1) — verifying each cited work against an exact accessible text — was
not taken, because this correction cycle had no access to the cited editions
and the steer forbids inventing bibliographic metadata. Verification remains an
open burden, not a completed act.

Relationship vocabulary, now fail-closed while a row is `UNVERIFIED`:

```text
AUTHOR_ASSESSED_UNVERIFIED   the author's assessment of the relation; no text
                             was consulted; never quotable as a factual identity
POSSIBLE_ANALOGUE            a resemblance worth checking; weaker than assessed
                             identity
SEARCH_LEAD                  a place to look; asserts no relation
```

Changes:

- `AR8R-FABLE-R1-SOURCING.md`: every relation cell rewritten into the vocabulary
  above; the fail-closed rule is stated in the packet itself.
- `AR8R-FABLE-R1-PRIOR-ART-AND-NOVELTY-CEILING.md`: the correspondence table's
  bolded **Identical** / **Equivalent** / "inherits" cells are now "Assessed
  identical (unverified)" etc.; the headline no longer asserts that objects
  "already exist in the literature" as fact, and the closing consequence
  paragraph is likewise author-assessed.
- The **zero-novelty ceiling is preserved unchanged**. It is a refusal to claim
  novelty, which needs no source verification and is unaffected by downgrading
  the positive identity claims.

Enforcement: `scripts/validate_fable_r1_claim_language.py` check 2 fails the
build if any `UNVERIFIED` row carries `IDENTICAL`, `EQUIVALENT`, `INHERITS`, or
`ALREADY_EXISTS`, or bare identity wording outside an assessed/analogue wrapper.

## Finding 3 — OSM source-specific claims under a source-unverified banner

**Option taken: quarantine.** Verification against the exact source bytes was
not performed. The owner steer of this cycle additionally directed that
source-level OSM analysis stop; the source is outside this correction's
boundary.

- `AR8R-FABLE-R1-OSM-TYPED-EXTRACTION.md`: the typed-extraction section and the
  per-result classification table are explicitly quarantined as **unverified
  notes that are not current research authority**, retained as leads for a
  future verification pass that must cite exact source locations for anything it
  keeps.
- Mathematical deductions are kept separate from descriptions of what the source
  reports: the four countermodel classes are marked as round-1 constructions
  independent of the source's content (`DERIVED_BUT_UNVERIFIED`).
- The unqualified "admits no global section by construction" claim was already
  removed in the previous cycle and remains removed everywhere, including the
  failed-candidate ledger row; the supported limitation is the absence of a
  canonical, transition-compatible section plus latent-state nonidentifiability.
- Reviewing model and transport state are recorded in
  `AR8R-FABLE-R1-PR21-INDEPENDENT-AUDIT-V2.md`: a client safeguard fallback that
  silently switches models is classified as a transport/reviewer-integrity
  interruption and never counted as an independent reviewer.

## Remaining burden

`FABLE-R1-B07` (new): verify each prior-art attribution against an exact
accessible text, recording identifier, location, and proposition context, or
retire the row. `FABLE-R1-B08` (new): verify or retire the quarantined OSM
typed-extraction notes against exact source locations, in a stable recorded
review context. Both are `closable_by: EXTERNAL_SPECIALIST_OR_DEDICATED_SEARCH`.
