# Portable source-only boundary package

The mathematical sources, scientific reviews, source manifests and final verification logs are unchanged. All 50 author sources and the full 51-source independent review closure are included, so source-manifest paths resolve without a new reconstruction contract. Reproduction uses the clean root scripts with an explicit trusted TOOLCHAIN_ENV and the hash-verified Lean 4.19.0 binary.

Two historical independent-review shell wrappers are intentionally not distributed: the historical verification receipt still records their identities, but those script bindings are historical evidence, not portable entry points. They embedded internal execution coordination and a machine-specific environment-file pin. No scientific source or acceptance finding depends on distributing them. Original hashes and origins remain in separate custody. The current root scripts have no such coordination variable or environment-file-content pin; they verify the actual compiler binary.

The independent source tree may be rebuilt with a copy of the root scripts/reproduce-module.sh placed under independent-review/scripts and its dependency-order.txt, or reviewed against the unchanged full author replay and independent evidence. The root scripts/reproduce-all.sh is the primary portable reproduction entry point.

Original initial-elaboration output, its exact failing source snapshot, and the post-compile shell-error transcript were recovered byte-for-byte from retained captures. Consult evidence/HISTORICAL_DIAGNOSTIC_CUSTODY.json for hashes and limitations. The numeric historical exit 127 was observed in the original tool return, not in the retained stdout/stderr file; the claimed edit-race cause remains an author explanation rather than an independently established fact. No historical failure was reconstructed.

The additional portability smoke uses a relocated trusted environment file and a real dependency-using proof module. It reuses only previously rebuilt dependency objects temporarily, is not described as a new full clean build, and contributes no objects to this archive. Fresh reproduction logs remain separate from immutable acceptance evidence.
