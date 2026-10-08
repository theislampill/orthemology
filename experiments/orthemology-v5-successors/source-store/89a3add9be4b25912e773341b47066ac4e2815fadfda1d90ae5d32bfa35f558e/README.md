# Four-state structured stress control

This small source-only supplement qualifies one structural family against the
unchanged public efficient implementation and independent exhaustive oracles.
It is **bounded implementation evidence**, not a new theorem or a broader
four-state census. It leaves the existing Eighteenth release files unchanged.

## Why this family

The positive anchor has four states and two actions at every state. Internal
action 0 mixes equally within `{0,1}` or `{2,3}`. Low-odd action 1 goes from 0
to 2 and from 2 to 0, with self-loops at 1 and 3. Before filtering, both modes
have one eight-pair maximal end component (MEC). Removing priority-1 actions at
the attained-even threshold exposes **two disjoint, nontrivial two-state MECs
simultaneously**. A three-state instance cannot have that particular shape.

The internal priorities in modes 0 and 1 are respectively `(2,3,4,5)` and
`(3,2,5,4)`. Each block therefore attains its own and rival even minima at
different pairs. Both blocks survive threshold 2; only the second survives
threshold 4. The anchor's rows are numerically equal across modes. Hard checks
require the exact two components, separate witnesses, exact representative
sets and target unions, and a winning region containing all four states.

## Exact admitted population

Eight labelled templates each use all four initial states, giving 32 distinct
complete input instances. All templates retain four states, two actions per
state, and exact rational probabilities. There is no random sampling, seed,
state/action relabelling, or claim that initial-state changes are new graph
structures. No isomorphism-class census is claimed.

1. `equal_row_anchor`: the anchor above.
2. `first_block_rival_even_removed`: change mode 1's internal priority at state
   1 from 2 to 3, destroying the first block's rival-even qualification.
3. `second_block_rival_even_removed`: change mode 1's internal priority at
   state 3 from 4 to 5, destroying the second block's rival-even qualification.
4. `first_block_numerically_distinguished`: retain template 2's odd rival
   minimum and change mode 1's state-0 internal row to `(1/3,2/3,0,0)`. Support
   is unchanged but numerical equality fails. The first block qualifies under
   uncertain mode 0 (Case A), but not under uncertain mode 1.
5. `both_blocks_numerically_distinguished`: start from the anchor and change
   mode 1's internal rows at states 0 and 2 to `(1/3,2/3,0,0)` and
   `(0,0,2/3,1/3)`. Each component has its own numerical distinction.
6. `forward_bridge_removed_bad_first_block`: retain template 2's odd rival
   minimum and replace the 0-to-2 bridge with a self-loop at 0 in both modes.
   Hard checks require `K=W={2,3}`; initial states 0 and 1 must lose. This
   prevents another component's even witness from rescuing the bad block.
7. `matched_exiting_internal_successor`: change the state-0 internal row to
   `(1/3,1/3,1/3,0)` in both modes. Its matched successor exits the first block;
   whole-action closure must reject that block after bridge filtering.
8. `revealing_exiting_internal_successor`: make that exiting-row change only
   in mode 1. The successor at state 2 is revealing relative to mode 0, and
   the first block is neither closed nor a qualifying uncertain-mode-1 block.

`INPUTS.json` preserves all 32 exact raw inputs and their canonical SHA-256
digests. Canonical input JSON sorts object keys and uses separators `,` and
`:` with no added spaces. Probabilities use canonical rational strings.

## Replay

Use Python 3.10 or later and the standard library only. No installation,
network access, Lean environment, or external cache is required:

```
python -E -S -B run_control.py --check
python -E -S -B run_control.py --output ../fresh-four-state-run
```

The output directory must not exist and must be outside this supplement.
`--check` verifies source hashes and structural assertions but does not call
the census. The ordinary command launches exactly one census process, capped
at 180 seconds, with Python environment variables removed and site startup
disabled. Do not use `-O` or `-OO`: the unchanged census uses assertions, and
the harness refuses optimized Python. The interpreter and standard library
are trusted.

The unchanged `run_campaign.census` checks, for each input:

- both modes' exact MEC sets for every one of 256 allowed-pair subsets, and
  containment of every exhaustive end component within a returned MEC;
- known and both uncertain target unions and representative soundness for
  every allowed-pair subset;
- every known region and all 256 combinations of candidate `K` and `W`;
- the final region classification and the submitted positive or negative body.

The process stops at the first assertion discrepancy. Exact input data and
available census locals (including mode, allowed subset, and actual output)
are retained in `FAILURE.json`. Timeout, incomplete coverage, malformed input,
source mismatch, or execution failure is an execution/coverage limit, never
negative mathematical evidence. Output logs may include local runtime paths;
only the path-free summary records are distributed here.

## Evidence and limits

`RESULT.json`, `EXECUTION.json`, and `FEATURE_COVERAGE.json` record the single
qualification run. `SOURCE_BINDINGS.json` binds 12 byte-identical files copied
from the existing public code-evidence package, including production, both
independent oracles, and the census. The copied relative layout is preserved
because the original imports rely on it. `MANIFEST.json` inventories all
other distributed files by byte count and SHA-256; it is an integrity record,
not a signature or publisher-authentication mechanism.

There are no production edits, new dependencies, compiled objects, raw
internal reviews, private notes, or absolute host paths in this supplement.
Run counts and timing are not an algorithmic complexity proof. The
arbitrary-finite scope continues to rest on the source argument and stated
mathematical results. This supplement establishes neither Python/Lean
correspondence nor a physical deployment guarantee.
