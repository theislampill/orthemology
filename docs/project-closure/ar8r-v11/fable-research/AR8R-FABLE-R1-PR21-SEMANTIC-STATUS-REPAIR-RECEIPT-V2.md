# PR #21 — semantic-status repair receipt V2 (Codex finding 1)

Repairs the merge-blocking finding that unverified research was locally written
as proved or verified inside packets whose top banner says
`DERIVED_BUT_UNVERIFIED`.

## Status vocabulary (one vocabulary across prose, YAML, and validators)

```text
LEAN_FORMALIZED_SCOPED_RESULT   kernel-checked in the committed scoped Lean
                                development, with a receipt entry
CHECKED_FINITE_INSTANCE_ONLY    reproduced by a committed checker on the
                                stated finite domain only
DERIVED_BUT_UNVERIFIED          the author's derivation; checked by no one;
                                not citable as established
SOURCE_LEVEL_UNVERIFIED         a reading of an external source checked by
                                no reviewer
UNREPRODUCED_FROM_COMMITTED_ARTIFACTS
                                a reported number no committed artifact can
                                reproduce; no evidential weight
CONJECTURE                      not even derived; a lead
```

## What changed

`AR8R-FABLE-R1-TYPED-CORE-CANDIDATES.md`:

- both "**Proved.**" headings replaced by "**Derived properties**" with an
  explicit per-item status; every Core A and Core B property, and the battery
  bullets that state theorem-like consequences, now carry
  `DERIVED_BUT_UNVERIFIED` locally except the fibre-constancy characterization,
  which carries `LEAN_FORMALIZED_SCOPED_RESULT` (a residual "provably" in the
  partial-observation bullet was caught by the distinct rereview and fixed);
- "a proved tight bound" is now "a derived, unverified bound
  (`DERIVED_BUT_UNVERIFIED`) suggests";
- the transport hypotheses no longer claim countermodels "prove" necessity;
- the discriminator section no longer presents its tabulated verdicts as
  established: the tabulation was never committed, and the section now says so
  where it is quoted from, not only in the banner;
- the Core B judgment gloss no longer uses bare "establishes" for the
  object-language reading.

`AR8R-FABLE-R1-SEPARATION-INDEX-AND-INTERPRETATION-MAPS.md`:

- Lemma 1, Lemma 2, and Theorem R each carry a local status; "Theorem" is
  marked as the author's label, not a verification status;
- "Proved properties" → "Derived properties (all `DERIVED_BUT_UNVERIFIED`)";
- "Proved here", "proved necessary", the exponential-gap claim, and the
  categorical "no bridging theorem exists" conclusion are all rewritten as
  derived-unverified, with the absence of any committed instance stated inline;
- "three verified interpretation maps" → "three *recorded* interpretation
  maps" with the per-domain statuses spelled out; the weak typed-model pass is
  explicitly "author-recorded only, with no verification status".

Top-level banners were not weakened; local wording was brought down to them.

## Fail-closed enforcement

`scripts/validate_fable_r1_claim_language.py` (new, wired into
`.github/workflows/validate.yml`):

- rejects any line of a candidate packet carrying bare
  proved/proven/verified/establishes language without an admissible local
  status, negation/withdrawal context, or evidence owner on the same line;
- the candidate-packet set is explicit; receipts and audit records, whose
  "verified" words report performed checks, are documented as out of scope;
- after the distinct rereview: also gates the prior-art correspondence table's
  Relation column, the zero-novelty ceiling headline's presence, and the
  sourcing table's claim-supported column; token set extended
  (provably/prove(s)/established) and exemptions narrowed. The gate remains a
  lexical tripwire, not a prover — adversarial paraphrase can evade it, and
  human review stays the outer gate;
- exit 1 on any failure; current state: PASS with 0 failures.
