# Trace reconstruction: bounded application result

## Result

At retention probability 1/4, a deletion trace of 00 and a deletion trace of 01 have total-variation distance 1/4. Repeating the same realised trace any positive number of times preserves that distance. Every randomized decision based on those copies has equal-prior success at most 5/8. With no data, the distance is zero and equal-prior success is 1/2.

These facts have now been freshly checked in the existing Lean 4.19 environment. The general statements use a linearly ordered field, and exact rational fixtures instantiate them. They are finite statements. No real-analysis import, convergence theorem, general trace decoder, or upstream 4.34.1 library was replayed.

Two separate controls also passed: identical encoded content with different source labels has the same stipulated content-only channel law; for the known word 00, an observed single zero is compatible with two distinct masks, each of conditional weight 1/2. Content recovery and source/occurrence attribution are different targets.

The general information principle is inherited from H-ICS and T9. The new contribution is this selected application and its verification, not a new general statistical or information theorem. Sharing one latent word with independent fresh masks is legitimate sampling. Copies can improve availability and fault tolerance; the negative result concerns ideal repeated access to the same already realised observation.

## Verified scope

- `formal/TraceControls.lean`: 19 theorem declarations, about 200 lines
- `formal/RationalFixtures.lean`: 13 exact application fixtures
- All positive declarations compile under `--trust=0`
- Full type and axiom readbacks use only propext, Quot.sound and Classical.choice
- Four false promotions are rejected at their intended mathematical targets
- 2,157 actual imported objects, including the two fresh local modules, are hash-bound
- Official cached dependencies are trusted and were not rebuilt; no network, installation or Lake command was used
- `formal/verification-run03/VERIFICATION.json`: author PASS, awaiting independent review

The earlier proof-engineering failures and both failed replay-harness runs are retained. The initial empty-module contract failed on missing theorem names as intended. Its later GREEN result is a development check, not additional mathematical evidence. Failed `decide` reductions on rational expressions were corrected and are not counted as valid negative controls.

## Positive contrast and application conditions

For fresh independent traces of the same word, the written two-word calculation gives TV = 1-(1-p)^M and optimal equal-prior success 1-(1-p)^M/2. The all-M general formula remains written mathematics; exact finite enumerations were performed independently by the root and author. They are not counted as general proofs. Convergence statements concern ordinary real probability, not an arbitrary ordered field.

`MODEL_DERIVATION_AND_PROPOSAL.md` gives the exact derivation and eight still-required application conditions: faithful encoding/known length; actual deletion-only observation model; known channel parameter; correct joint mask law; actual sampling resources and support; an appropriately checked selected theorem; separate source/occurrence/truth/authority evidence; and a correctly stated probabilistic service. No real-world authentication, permission, truthfulness or normative conclusion is established here.

## Research-source boundary

The 29-page October 5 uniform-decoder paper was read in full, with selected visual checks on pp. 1 and 23. Its formal family scope document covers only the separate September 24 lower-bound manuscript. The new decoder is not kernel-checked merely because its family has a Comparator link. Neither novel upstream upper nor lower bound is needed for this finite application.

## Replay and review

This is the selected public SOURCE projection. Run from any directory:

    python3 formal/replay.py --lean "$LEAN419" --cache "$EXISTING_PREPARATION" --output ../fresh-math122-output

Only an existing pinned official Lean 4.19.0 compiler and the already prepared official cache are used. No Lake, installation or upstream 4.34.1 build is required. Output must be fresh and outside the packet, compiler and cache. See BUILD.md and PROJECTION_NOTES.md. The frozen author record's pending-review status is historical; review/REVIEW.md and review/REVIEW.json carry the later scoped PASS. No new proof replay occurred during this public curation.
