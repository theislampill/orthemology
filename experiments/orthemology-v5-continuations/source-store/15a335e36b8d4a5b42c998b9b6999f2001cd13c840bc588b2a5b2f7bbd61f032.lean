import PositiveAtomMass

namespace Orthemology.Frontier.MealyMeasure
open Set MeasureTheory
open scoped ENNReal

variable {S : Type*}

/-- A countable, concrete candidate family for all positive atoms. -/
def atomCandidate (M : Mealy S) (s : S) (u : List Bool) : Cantor := output M s (extend u)

def atomCandidateMassQ [Fintype S] [DecidableEq S] (M : Mealy S) (s : S) (u : List Bool) : ℚ :=
  targetMassQ M (drivenGenerator M (prefixDriver u)) s (s,0)

theorem atomCandidateMassQ_correct [Fintype S] [DecidableEq S] (M : Mealy S) (s : S)
    (u : List Bool) :
    (atomCandidateMassQ M s u : ℝ) = (law M s {atomCandidate M s u}).toReal := by
  simpa only [atomCandidateMassQ, drivenGenerator_stream, prefixDriver_stream, atomCandidate] using
    targetMassQ_correct M (drivenGenerator M (prefixDriver u)) s (s,0)

/-- Positive rational candidate mass is equivalent to being a genuine atom. -/
theorem atomCandidate_positive_iff [Fintype S] [DecidableEq S] (M : Mealy S) (s : S)
    (u : List Bool) :
    0 < atomCandidateMassQ M s u ↔ atomCandidate M s u ∈ P02A2.positive (law M s) := by
  have hreal : 0 < atomCandidateMassQ M s u ↔
      0 < (atomCandidateMassQ M s u : ℝ) := by exact_mod_cast Iff.rfl
  rw [hreal, atomCandidateMassQ_correct, ENNReal.toReal_pos_iff]
  change (0 < law M s {atomCandidate M s u} ∧ law M s {atomCandidate M s u} < ⊤) ↔
    0 < law M s {atomCandidate M s u}
  exact and_iff_left (measure_lt_top _ _)

/-- Filtering the explicit finite-word candidate family by its computed positive rational mass
    gives exactly the positive singleton support. Repetitions are not hidden. -/
theorem positive_iff_candidate [Fintype S] [DecidableEq S] [Nonempty S]
    (M : Mealy S) (s : S) (y : Cantor) :
    y ∈ P02A2.positive (law M s) ↔
      ∃ u : List Bool, atomCandidate M s u = y ∧ 0 < atomCandidateMassQ M s u := by
  constructor
  · intro hy
    obtain ⟨u, hu⟩ := positive_atom_finite_generator M s y hy
    have he : atomCandidate M s u = y := by
      simpa only [drivenGenerator_stream, prefixDriver_stream, atomCandidate] using hu
    exact ⟨u, he, (atomCandidate_positive_iff M s u).mpr (he.symm ▸ hy)⟩
  · rintro ⟨u, rfl, hu⟩
    exact (atomCandidate_positive_iff M s u).mp hu

end Orthemology.Frontier.MealyMeasure
