# Unbuilt development intermediates

These files are excluded from every successful compiled module list.

- Probe.lean.unbuilt: temporary checks of possible lemma names; it intentionally contains unsuccessful checks.
- MeasureBridge.lean.unbuilt: exploratory direct MeasureTheory statement. Compilation stopped at an unavailable Bochner.Basic import before checking this file. The needed dependency closure has 648 missing Mathlib modules, and no rebuild was attempted.

Only the seven modules enumerated in RESULT.md carry a trust=0 replay claim. The measure-nonrepresentation conclusion is documented as a mathematical corollary of the checked polynomial positivity obstruction, not as a separately checked MeasureTheory theorem.
