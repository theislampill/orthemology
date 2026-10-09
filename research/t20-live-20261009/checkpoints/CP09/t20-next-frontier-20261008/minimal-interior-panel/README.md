# Portable controls and provenance

This packet is scratch-only. RESULT.md contains written proofs, not kernel-checked formalizations. Existing historical event/source records are preserved without certifying prior activity durations.

Run with Python 3.10 or later, standard library only:

    python controls.py

Or, from the enclosing workspace:

    python t20-next-frontier-20261008/minimal-interior-panel/controls.py

The script asserts exact comparisons and writes CONTROL_RESULTS.json beside itself. A rerun changes recorded timestamps but should reproduce all panel counts, histograms, minimum sizes, and the source digest. The retained CONTROL_RUN.log is stdout from the executed command, redirected when originally run. Runtime used: Python 3.12.14, Clang 22.1.3. No downloads, network access, external dependencies, randomized sampling, or solver are required.

The finite-grid comparator independently constructs all endpoint hit masks reachable by OR-ing route rectangles, assigning exact minimum route counts by breadth-first search. It compares those counts against exhaustive cut-set enumeration. Separately, greedy interval stabbing is compared against exhaustive cut-set enumeration for every interval family through five minimal positives. Three-dimensional enumeration does not use the two-dimensional formula.

Assurance boundaries:
- The deterministic finite controls verify their finite grids only.
- The general formula, robust open-set construction, measurable adaptive transport, and 3D counterexample are written proofs.
- No new proof-assistant run, statistical experiment, physical feasibility test, or performance benchmark was conducted.
- The finite-support and measurability conclusions do not supply numerical likelihood, KL, sample-rate, or stopping-time bounds.

Source inspection in this continuation: retained-interior-certificate/RESULT.md and full-face-threshold-kl-rate/RESULT.md were read in full. Their bytes are bound in CURRENT_SOURCE_BINDINGS.json. The predecessor's theorem and assurance descriptions are inherited, not independently recompiled in this packet. The separately assigned reviewer lane is minimal-interior-panel-review; its own report states its inspection and controls.
