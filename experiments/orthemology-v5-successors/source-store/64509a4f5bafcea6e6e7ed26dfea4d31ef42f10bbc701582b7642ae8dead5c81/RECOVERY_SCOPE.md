# Recovery and verification status at package freeze

This is a new recovered-v1 integration, not an identical restoration of the interrupted wrapper. All 111 mathematical modules match their historical source digests and have been freshly compiled after the reset.

All 220 designated historical fixture slots now have actual files. Of these, 167 match independently retained historical digests, 52 were restored from complete original write/patch payloads without retained old digests, and one deterministic finite regression fixture was regenerated from the retained generator. This does not claim byte-identical restoration of all 220 historical files. The regenerated fixture has repeat-generation evidence and is explicitly subject to current independent review. Four additional integration-auditor controls are new.

The staged author verification covers all 220 main fixture contracts, four new integration controls, 22 Python tests, all 3,485 theorem roots and explicit declaration/auxiliary/opaque inventories. Historical and staged receipts are not substitutes for the separate full fresh-extraction author and independent archive-replay receipts required before delivery. Restoration labels describe provenance at freeze; later archive acceptance is conveyed by those separate exact-digest receipts.

ACCEPTANCE_MAP.json maps every source root to its bounded historical scientific acceptance, distinguishing exact recovered record bodies from digest-only anchors. No unavailable review body or digest is fabricated. Written-only exclusions and computational trust boundaries are stated in SCOPE.md.
