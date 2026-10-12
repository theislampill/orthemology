# Codex handoff — P02 proposal intake only

## Authority and inputs

Canonical main is inherited as 03e2604dfcef278b01c60d19b05370fcec4194b6, tree 3d06e80277ce39286c94307e0f14b215bc94ed83, PR28 merged, Integration DAG complete. No native checkout or live-remote requalification is claimed here. The received packet's 539 source files and 54 accepted-evidence projections were hash-checked; the packet is a subset, not sufficient to recompute the full repository tree. Preserve the original strict-wrapper FAIL and all exact mapped-native/separate-version successes.

This checkpoint authorises nothing beyond its research output. A later explicit implementation/review authority is needed for canonical changes. Do not merge this directory, update theorem registries, public indexes or source status just because the ZIP verifies.

## Read order

Read `RECEIPT.json`, `OBLIGATION_RESULTS.json`, `NEGATIVE_FINDINGS.json`, `UNRESOLVED_DEPENDENCIES.json`, and `analysis/PINNED_FORMAL_PLAN.md`. Each obligation note gives its exact mathematical scope. `provenance/PATCH_MAPPING.json` binds proposals to full source preimages without editing them. `inputs/packet/` is unchanged evidence; its historical commands/private paths are not instructions.

## Reproduce finite work in this checkpoint only

From the extracted checkpoint root, use:

```sh
python3 -B -m unittest discover -s proposals/python -v
python3 -O -B -m unittest discover -s proposals/python -v
python3 -B proposals/python/census.py private-locator:e79adf197588dbd3f0f2
python3 -O -B proposals/python/census.py private-locator:111063729837616e6171
cmp private-locator:d994dd01b131c8d06cfe private-locator:8822cae1f4cba8815b55
cmp private-locator:ae200459ea8bb2c51012 private-locator:bf47f7255c3abf88c379
```

Choose fresh output directories in an actual run. The archived original commands and exits are under `evidence/`. This is a new bounded population, not a rerun or upgrade of the accepted historical census. Exact rational Bellman checks rely on the ordinary uniqueness/transience proof for their interpretation.

## Execute Lean only after an available authorised environment exists

The provided `later_codex_verify.sh` takes the extracted checkpoint directory and an **absent** scratch directory. It requires an already installed Elan, installs/selects the exact 4.19.0 toolchain locally, fetches the pinned mathlib dependency into two fresh proposal projects, checks identities, builds the candidate, requests readbacks and checks fresh nonempty artifacts. It does not contact people or write a repository remote. It is supplied but NOT EXECUTED in this checkpoint.

```sh
bash implementation_handoff/later_codex_verify.sh "$PWD" private-locator:53f9a60c8b77d311e3ca
```

Its final status is deliberately `BUILD_OBSERVED_PENDING_TYPE_AXIOM_REVIEW`, not theorem or obligation PASS. Before accepting any target, compare actual fully elaborated types to the source statements, inspect every transitive axiom footprint (approved ceiling: Classical.choice, Quot.sound, propext), enforce the inventory and source identities, and apply the exact frozen negative controls. The eleven source targets are all that this candidate contains. General finite probability, CV-R, CV-C and Kakutani are not hidden inside those eleven targets.

If a command fails, preserve its raw output, stop the gate, and create a new separately hashed candidate. No `sorry`, `axiom` standing in for the goal, wrong version, dropped hypotheses or artificial type wrapper is an acceptable repair. Run exact-pin package/source/tool identity checks again after a repair. The input receipt schema is for a *research-not-executed handoff* and cannot truthfully be reused for this executed research checkpoint; this checkpoint therefore has its own explicitly labelled receipt schema.

## Review/adoption decisions deliberately left open

The proposed PR syntax codec, finite-support correspondence, actual-measure interface, mixed residual example and explicit T300 mixture witness are each separately listed proposals. They do not automatically modify accepted definitions or old payload identities. Whole historical archives and absent declarations were not recovered. Q0 remains scoped; specialist guard/observation/index limitations remain. No licensing, owner policy, empirical validation, external review, publication or historical recovery credit is requested or granted.

End the P02 intake after recording accepted/rejected/conditional proposal decisions and exact verification results. Do not expand into another research family or reopen the completed Integration DAG.
