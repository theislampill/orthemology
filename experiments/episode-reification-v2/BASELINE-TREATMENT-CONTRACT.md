# ER-2 baseline/treatment contract (information-matched, label-free)

- One canonical fact-atom list per case (`fixtures/<case>/facts.json`, stable
  IDs F01…). The **baseline** renders the atoms as a chronological audit log
  (`baseline-record.md`); the **treatment** renders the SAME atoms as an
  explicit sectioned/linked record (`treatment-record.json`).
- **Information match (audit B8/H2 repair):** the treatment adds *organization
  and typed links only*. It contains **no** diagnostic case title, **no**
  `binding_defect`/interpretation-bearing `reliability_note`, **no** field
  that states a keyed failure class. `tests/test_smoke.py` proves both
  renderings carry exactly the same fact atoms and that neither runner-visible
  arm contains any KEYS token, archetype label, or diagnostic conclusion.
- Both arms receive the same frozen probes, the same budget, and the same
  closed answer schema. Coined vocabulary appears in neither arm.
- Time/cost measured in both arms (answer tokens); the cost ratio feeds the
  harm rule only.
- Unit of inference: the **case**, paired across arms; the five archetypes are
  strata with four neutral surface variants each (20 cases). Repeats are
  within-case replicates (temperature-0 default 1); deterministic reruns are
  never independent evidence (Decision 0020).
