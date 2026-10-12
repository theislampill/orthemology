# Verified release replay entrypoint

Use `python hase-telescope-code-validity-20261010/verify_release.py`.

The release receipt is `validation/RELEASE_REPLAY.json` and the immutable pin set is `validation/RELEASE_PINS.json`. `CURRENT.md` gives the theorem inventory and diagnostic history. Its earlier final-runner path is superseded here: that runner accidentally selected the generic proof module for axiom-audit parsing, causing a Python KeyError after the Lean module compiled successfully. The release runner's audit selection is restricted to the three actual audit modules. This harness-only correction preserves all earlier files and pins, and does not change any Lean source.

The selected release replay compiles sixteen modules with Lean 4.19.0 `--trust=0`, validates fifteen theorem axiom audits, six positive/four negative runtime controls, and three expected semantic diagnostic rejections. Pinned retained inputs are checked before and after; the protected baseline is not rebuilt or modified.
