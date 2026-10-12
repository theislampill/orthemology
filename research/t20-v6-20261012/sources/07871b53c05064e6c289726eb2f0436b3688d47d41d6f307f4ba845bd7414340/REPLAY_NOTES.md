# Replay and generator notes

Run `python verify.py` from this directory (or use its absolute path). The input pin manifest already exists; do not invoke `--init` again or overwrite it. The verifier uses retained Lean 4.19.0, trust level zero, a 65,536 KB thread stack, a fresh output directory, and the exact pinned retained import closure. Author and independent reviewer receipts remain separate.

For optional regeneration in a disposable copy, copy SCHEMA.json and run, in order:

1. generate_rules.py
2. generate_image.py
3. generate_rule_parts.py
4. generate_controls_release.py

This reproduces all 21 generated image-rule, bound, global image, and control modules byte-for-byte; see validation/GENERATOR_REPLAY.json. The source schema and frozen constructor-description generator are separately covered by the earlier descriptor freeze and independent schema review.

The older generate_controls.py is a preserved diagnostic draft. Its last printer-option insertion left an unterminated Python string. It is not invoked by verification or the Lean proof chain. The working additive replacement generate_controls_release.py corrects only that string escaping. It was added after the immutable proof input pins were created and is separately included in the final freeze. No selected Lean source, frozen input pin, or previous freeze was changed to repair that utility.

Optional exploratory modules under diagnostics, including stack/reduction probes and the superseded monolithic Rule proof, are not part of the selected theorem closure. A retained failed attempt is not a passing control. Only explicitly successful entries in AUTHOR_REPLAY.json are accepted; the five semantic negative controls must fail with their specified false-proposition diagnostic.
