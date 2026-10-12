# Repeating the final replay

Use `python hase-coded-rule-templates-20261010/verify_final.py`.

This checked wrapper runs the unchanged source-fresh verifier and additionally
checks the frozen TelescopeNatTransport and ListNatCodeTransport handoff objects.
These objects are not used as a substitute for source replay: both modules are
freshly compiled before RuleCodeBasics is compiled. The supplemental pins record
the initial object identities exposed to downstream workers. Each invocation
writes its own `validation/final-replay-*` receipt directory, preserving the first
author receipt, original 3,032-input manifest and core source freeze.

The original `verify.py` remains a valid full source-fresh replay entry point;
its telescope source pins are sufficient for the freshly rebuilt modules.
