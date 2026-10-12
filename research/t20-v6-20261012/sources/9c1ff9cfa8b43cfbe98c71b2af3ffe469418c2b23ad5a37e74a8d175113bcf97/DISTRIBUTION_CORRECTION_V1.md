# Distribution-only correction

Scientific artifact revision 6 and all accepted sources/review bytes are unchanged.
The first public wrapper stopped before output creation because it unnecessarily
required a compiled cache for every package named by the pinned Lake manifest.
The official prepared dependency tree has no cache for the inherited Cli package,
which these proofs do not import.

This wrapper-only successor requires the exact seven cache-bearing packages used
by this proof import closure: LeanSearchClient, Qq, aesop, batteries, importGraph,
plausible and proofwidgets. Their names are checked against the pinned Lake
manifest; missing any required cache is a preflight failure. Cli is explicitly
classified as unused and excluded from LEAN_PATH; its absence in the supplied
prepared installation is recorded rather than silently tolerated as an arbitrary
missing dependency. Unlisted directories never enter LEAN_PATH. A missing required
transitive object still fails compilation. No dependency is downloaded or rebuilt.
The source-only proof scope and trusted-cache boundary are unchanged.

Predecessor archive SHA-256:
375bf13ad4e1b2301620af8cdbfe4cc049c0b8d69242b769f2026c43d63c3cba
