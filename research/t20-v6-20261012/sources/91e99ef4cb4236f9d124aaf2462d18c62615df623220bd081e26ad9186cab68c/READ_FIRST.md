# Read first

`RESULT.md` gives two exact Set Cover transports at the current proof-compiler interface:

1. With empty support and identical acyclic branching rules, minimum occurrence-tree cost is easy, while minimum once-per-node DAG cost is NP-complete to budget.
2. With exact target support, even unary acyclic take/skip chains encode Set Cover; tree and DAG cost coincide. Explicit support-state expansion must not be mistaken for a polynomial algorithm in the compact grammar size.

This is classical complexity, particularly Sahni's shared AND/OR ancestry and Karp's Set Cover. The older RP-T7 recheck-hardness summary is credited; its full source was not located. The packet makes no general historical novelty or programme-wide novelty claim.

Verification:

    python shared-proof-cost-boundary-20261009/check_transport.py

Run relative to the parent workspace, or use the script's absolute path. Python 3 standard library only. The script reads the two sibling predecessor compilers and writes `CHECK_RESULTS.json` in this directory. It does not alter either compiler or create bytecode caches there. All 689 small incidence systems and targeted controls passed; these checks corroborate the written reductions, not prove them universally.

`SOURCE_LEDGER.json` records actual reading depth and access limits. `OPERATIONS.jsonl` records prospective operations and later observed evidence without retrospective duration credit. `INPUT_BINDINGS.json` and `INPUT_UNCHANGED.json` bind the local inputs. `MANIFEST.json` binds this additive packet's other files.

No solver/performance campaign, approximation claims, Lean certification, predecessor edits, protected-state writes, repository integration, scientific adoption or T20 closure.
