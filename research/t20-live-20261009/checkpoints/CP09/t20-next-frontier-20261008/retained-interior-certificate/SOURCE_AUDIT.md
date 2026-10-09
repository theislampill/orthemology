# Source and dependency audit

This packet is a bounded scratch-only mathematical continuation. All dependency reads were read-only; no upstream source was edited, installed or rebuilt. SOURCE_BINDINGS.json records exact RESULT.md hashes for the four predecessors requested in the assignment. Their complete result texts were inspected, with split reads where a combined tool response had been truncated. Other local reads were limited to the existing formal-identification toolchain, verification scripts and mathlib metadata needed to reuse the already installed tools.

## Imported mathematical content

- dependent-gate-transport/RESULT.md: the F_c=H_c(ab) route CDF, density, Joe interpretation, common endpoint law, and its stated independent-route semantics.
- same-threshold-replay/RESULT.md: retained/nonlatched observation contract, all-command scope, and the exact n=1,m=2 heterogeneous-copula t=3/4 three-bit alias. No re-proof of its all-command identification or finite-grid perturbation theorem is claimed.
- arbitrary-face-replay-design/RESULT.md: the hard pair, all-rate two-face bound, cost conventions and exclusion of longer retained words. Its quantitative bound is not rederived here.
- full-face-threshold-kl-rate/RESULT.md: full face-minimum channel and its explicit exclusion of retained interior AB queries. Its KL asymptotic proof was read for boundary comparison, not re-proved by this packet.

## External primary source

Dirk Oliver Theis, On some lower bounds on the number of bicliques needed to cover a bipartite graph, arXiv:0708.1174v4, 2011, https://arxiv.org/pdf/0708.1174.

Inspection: web PDF text, introduction on pp. 1-2 (lines 18-39 in the returned extraction), for rectangle covering and the familiar fooling-set cardinality lower bound. The reference list entry to Dietzfelbinger, Hromkovic and Schnitger was visible. This is a targeted primary-source check of attribution, not an exhaustive literature review, priority search, or verification of the paper's subsequent rank/tensor results. Search discovery also surfaced the 1996 paper's publisher abstract, but no theorem is imported from that abstract. The relevant combinatorial proof is supplied directly and independently in RESULT.md and Lean.

## Kernel assurance and exact provenance

Lean: 4.19.0, commit 6caaee842e94. Existing mathlib checkout: c44e0c8ee63ca166450922a373c7409c5d26b00b. KERNEL_DEPENDENCIES.json binds lean/lake executables, available Lean shared runtimes, package manifest, toolchain file, accepted source and verification script. IMPORTED_MODULE_BINDINGS.json binds both the .olean and .lean file of each of the 1,798 transitive imported modules. ImportInventory.lean lists the environment's actual imported module names; it does not add a theorem or axiom to the accepted proof.

verify_kernel.sh copies the source into an isolated output directory and checks with -t 0 and warnings-as-errors. It does not modify the predecessor or its modules. The trust-zero option verifies imported module declarations according to Lean's tool semantics; it is not a from-source rebuild of the toolchain or all upstream dependencies. The accepted source's printed axioms are exactly the standard propext, Classical.choice and Quot.sound, with the latter two absent when unused. No bundle-wide kernel claim is made.

The probability formulas, full-support argument, KL consequence, low-arity interpretation and sampling discussion have written proofs and deterministic controls only. Neither code nor mathematical proof establishes that real-world route semantics or threshold retention hold. The package supplies no empirical data and no physical intervention warrant.
