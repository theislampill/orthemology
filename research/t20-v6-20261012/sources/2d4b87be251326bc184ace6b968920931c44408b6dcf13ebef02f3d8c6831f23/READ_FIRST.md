# Fixed bundle overlap information

`RESULT.md` is the bounded written derivation. It applies inherited contractions, parity, fibre sufficiency, and Boolean-lattice inversion to the once-per-node cost of a supplied compatible proof bundle. The concrete addition is a common-grammar cost-3/cost-4 witness with equal individual and pairwise costs, together with its general parity realization. It is not a new optimization theorem.

Run `python shared-proof-overlap-information-20261009/check_overlap.py` from the workspace root. The script imports the unchanged predecessor compiler without writing bytecode into its directory. `CHECK_RESULTS.json` records 369 exact assertions: five parity sizes, actual admitted proof DAGs and branch sub-DAGs, diagonal contractions, inverse histogram maps, and weighted/empty/repeated/identity controls. Six input hashes are rechecked.

No independent review or Lean formalization is claimed. Existing inputs, protected material, and T20 status were not modified. The work stops at this information-interface discriminator.
