# Eighth semantic controls

Read RESULT_INTERPRETATION.md for the exact distinction between concrete cost proof rejection, runtime semantic counterexample, and unchanged historical resource outcomes. Fresh author evidence is included, and the separately bound independent review passes both core results and the literal addendum. See INDEPENDENT_REVIEW_BINDING.json and the separate review archive; auxiliary resource limits remain explicitly uncredited.

## Source-only replay

The packet contains all 146 custom imports of the exact positive cost target, all 162 custom imports of the accepted runtime target, and five new runtime proof modules. Source bytes are frozen in SOURCE_MANIFEST.json. The two inherited mutants are preserved byte-for-byte. No custom compiled objects or historical plans are included.

First validate the complete Lean source census and both exact mutation derivations:

    python3 replay.py --verify-only

For fresh proof replay, provide official Lean 4.19.0 and the pinned Mathlib revision c44e0c8ee63ca166450922a373c7409c5d26b00b with its official dependency caches. Use a new absent output directory outside the packet and dependency roots:

    python3 replay.py --lean-bin /path/to/lean-4.19.0-linux/bin \
      --mathlib /path/to/mathlib4 \
      --mathlib-archive /path/to/mathlib-c44e0c8.tar.gz \
      --out /path/to/new-output --mode all

Omit --mathlib-archive for a clean exact Git checkout. The archive route verifies the pinned compressed archive and its complete 6,816-file extracted inventory; the eight package Git revisions and clean source states are checked separately. No downloads or dependency edits occur.

--mode cost freshly builds the complete positive cost target and audits selected endpoint axioms, then runs its unchanged mutant once. Concrete type mismatch and resource failure are separately recorded. The unchanged positive theorem is not declared false.

--mode runtime freshly builds 167 modules and audits the new endpoints, including the nontrivial positive control and exact positive-measure counterexample. It does not rerun the old timeout-only runtime mutant. Its preserved source and receipt remain available for custody and comparison.

All compilation is sequential with -j1 and a 180-second wall-clock ceiling per module. No heartbeat flags are added. A positive closure failure stops its dependent test; a timeout is never promoted to semantic rejection. Accepted axiom readbacks must contain only propext, Classical.choice and Quot.sound.

## Meaning of the selector witness

The runtime counterexample uses an exact classical finite-table existence construction. This fully discharges the source Certificate, including off-path cells. It does not claim that hidden classical choice values were evaluated to native literal tables, or that this counterexample was run empirically. The checked theorem is an existential mathematical refutation of the exact universal mixed-program/decoder claim.
