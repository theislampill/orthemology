# Recovered core111: additional dependency-source assurance

PASS, with independent detached acceptance. The exact 1,369-module required third-party Lean import closure was rebuilt from pinned sources in an isolated, initially proof-object-free tree. The unchanged recovered core then passed fresh compilation of all 111 mathematical modules, its complete control/audit suite, and 22 Python reference tests.

The source build completed on 5 October 2026 at 17:23:21 UTC; the complete core replay finished at 17:30:19 UTC. All 376 archive entries and 7,507 tracked files in both the original and isolated dependency trees rechecked unchanged. No dependency source trees, proof-object binaries, widget assets, npm resources, or compiler binaries are included in this evidence package.

Start with PUBLIC_ASSURANCE_v1.json. The detailed author receipt is evidence/DETACHED_SOURCE_REBUILD_REPLAY_RECEIPT.json; independent acceptance is independent-review/DETACHED_ACCEPTANCE.json. Both original receipts are preserved byte-for-byte. PACKAGE_INDEX.json binds every packaged evidence file.

The required source and object inventories, pinned revisions, compiler options and effective paths appear in evidence/. DEPENDENCY_COLD_BUILD.log records every fresh compiler invocation. fresh-core-replay/ preserves the complete immutable replay receipts, audit inventories and logs. tools/ and the independent verifier scripts document the executed checks. accepted-core-source-locks/ contains only the accepted archive's identity/coverage manifests and toolchain pin.

The immutable replay wrapper retains static cache-oriented provenance strings. Its dependency hashes are instead bound by the detached source-build evidence to the new objects. No accepted source ZIP or earlier result was changed.

The comparison against the earlier official-cache replay found 1,355 byte-identical dependency objects and 14 different Mathlib objects. All five resulting project inventories are byte-identical, including 8,289 declarations and 3,485 theorem roots, and all 226 control/audit contract results and metadata agree. No general dependency-byte reproducibility or semantic-equivalence claim is made, and the specific cause of the 14 byte differences was not established.

Official Lean 4.19.0 and Init/Lean/Std/Lake infrastructure, the operating system/runtime, and registry JavaScript build-tool distributions remain trusted. This was not a full-Mathlib rebuild, a compiler bootstrap, or native compiler/FFI verification. This supplement concerns core111 only; the separate signed116 replay retains its previously reported dependency-cache scope.

Process samples contain only explicitly selected Lean/Lake build/import variables; the public projection adds each selected value's hash. Technical workspace paths are retained solely as historical execution provenance. Other environment values are not included.
