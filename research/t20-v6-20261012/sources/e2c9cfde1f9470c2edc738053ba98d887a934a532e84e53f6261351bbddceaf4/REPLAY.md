# Replay and evidence

Run `python qualify.py qualification-replay-UNUSED-NAME` from this directory. The destination must be new. The qualification recipe rebuilds every local imported module from source with Lean 4.19.0 `-j1`; only pinned standard-library/Mathlib package caches are reused read-only. It never imports prior P01 local object files.

The sole new implementation module is `P01CanonicalCarrierProjection.lean`. `ProjectionContract.lean` checks the promised targets. The audit reads every new top-level declaration's exact type and axiom list. `qualification-final/QUALIFICATION.json` is authoritative; `RESULT_MANIFEST.json` binds the final ZIP.

Prerequisites and environment overrides are inherited from the raw-index successor: P01_PARENT_PROJECT, P01_PARENT_PACKET, P01_PARENT_RECEIPT, P01_SUCCESSOR, P01_LEAN and P01_CANONICAL. P01_DEPENDENT selects the already-sealed raw-index successor directory. Its exact ZIP hash and all imported source bytes are checked. Relocating inputs never relaxes hash/version/clean-status requirements.

The two canonical constructor-owning source files are byte-compared with canonical commit 03e2604dfcef278b01c60d19b05370fcec4194b6. Their source paths and hashes are recorded in `canonical_constructor_sources`. This is the exact source-projection binding, while canonical adoption remains false.
