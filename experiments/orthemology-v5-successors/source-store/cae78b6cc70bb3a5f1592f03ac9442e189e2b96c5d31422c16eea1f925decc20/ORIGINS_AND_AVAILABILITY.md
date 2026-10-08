# External dependency origins and availability

The evidence package includes exact custom sources and portable replay orchestration. It does not distribute the external Lean dependency objects. The source revisions, object names, byte counts and SHA-256 digests are bindings for separately prepared environments, not an installer.

## Two historical origins

- Hidden-change expects 6,646 objects from the retained official-cache environment, including locally compiled cache-client tooling. This exact external inventory is used by the hidden-change replay lane.
- HasE expects 1,369 objects originating in an earlier limited build from pinned dependency sources. The present package consumes that result as a prepared environment. Recompiling its 84 custom modules does not itself rebuild those external dependencies.

All 1,369 HasE object names are also present in the broad hidden-change set. Of these, 1,355 SHA-256 identities agree and 14 Mathlib identities differ. The complete comparison is in INVENTORY_COMPARISON.json. No cause or general byte-reproducibility conclusion is inferred from the difference alone.

## What is qualified here

The recorded replay starts with the separately prepared matching environments and verifies their exact inventories before compiling the included custom sources. It does not establish a clean-Linux provisioning recipe. This package contains neither the snapshots nor a supported acquisition/source-build procedure shown to reproduce these exact bytes on a new host. Its checker intentionally rejects missing and extra .olean objects as well as hash mismatches.

A reader without matching snapshots can run the manifest verification, Python suites and finite campaigns using the Python standard library. For Lean replay, the reader first needs a separately provided verified environment. No download is claimed to be published by this tree. A generic Mathlib cache retrieval or broad installation must not be assumed to produce the HasE pins.

A source rebuild may yield sound proof objects with different bytes, but such objects are outside this exact-snapshot qualification. They require their own explicit source-to-object evidence and review. Do not overwrite or silently relax these inventory pins to make a differing environment pass.
