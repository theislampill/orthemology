# Replay

Authoritative modules, in order:

1. P01DependentModel
2. P01DependentSubstitution
3. P01DependentFundamental
4. P01DependentControls
5. P01DependentRepresentation

The three `*Contract.lean` files assert promised target availability and are compiled after these modules. `DependentAudit.lean` is generated from all top-level declarations in the five main sources, with exact type and axiom readbacks.

Run `python qualify.py qualification-replay-UNUSED-NAME` from this directory. The destination must not already exist. Defaults match the pinned research workspace. Supported overrides are P01_PARENT_PROJECT, P01_PARENT_PACKET, P01_PARENT_RECEIPT, P01_SUCCESSOR, P01_LEAN and P01_CANONICAL; changing a path does not waive any inventory, digest, version, commit, clean-status, or declaration check.

The driver verifies the repaired parent source inventory and receipt, the original sealed recursive successor digest/source bytes, dependency revisions, compiler identity, and canonical checkout. It discovers local import closure, copies each source into a fresh source directory, and rebuilds all local modules with `lean -j1` into a fresh artifact directory. Parent and successor local object directories are excluded from LEAN_PATH. Pinned package caches are reused read-only; copying enormous caches is unnecessary.

`qualification-final/QUALIFICATION.json` is the primary receipt. Source bindings, compiler outputs, command records and all checked artifacts are retained beneath that directory. `RESULT_MANIFEST.json` binds the sealed deliverable. Failed developmental probes and the earlier first-order checkpoint are excluded from the authoritative ZIP and receive no proof credit. Independent audit material is a separate artifact/report.

The trust base includes Lean's kernel/compiler, the pinned compiled library dependencies, and the operating system. Hygiene scans and contract checks supplement kernel checking; they do not replace it.
