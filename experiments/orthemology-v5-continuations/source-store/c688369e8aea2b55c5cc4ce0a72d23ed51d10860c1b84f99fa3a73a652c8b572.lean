import GeneratorEquality

namespace Orthemology.Frontier.MealyMeasure
open Set MeasureTheory
open scoped ENNReal

variable {S : Type*}

/-- A total computable enumeration of finite binary words; unused codes return the empty word. -/
def wordAt (n : ℕ) : List Bool := (Encodable.decode (α := List Bool) n).getD []

theorem wordAt_encode (u : List Bool) : wordAt (Encodable.encode u) = u := by
  simp [wordAt, Encodable.encodek]

/-- Enumerate exactly positive-mass candidates, retaining only their first occurrence.
    The finite duplicate test compares infinite outputs by the proved finite-state bound. -/
def enumerateAtoms [Fintype S] [DecidableEq S] (M : Mealy S) (s : S) (n : ℕ) :
    Option (List Bool × ℚ) :=
  if 0 < atomCandidateMassQ M s (wordAt n) ∧
      ∀ k : Fin n, atomCandidatesEqual M s (wordAt k) (wordAt n) = false then
    some (wordAt n, atomCandidateMassQ M s (wordAt n)) else none

theorem enumerateAtoms_spec [Fintype S] [DecidableEq S] (M : Mealy S) (s : S)
    (n : ℕ) (u : List Bool) (r : ℚ) :
    enumerateAtoms M s n = some (u,r) ↔
      (0 < atomCandidateMassQ M s (wordAt n) ∧
        ∀ k : Fin n, atomCandidatesEqual M s (wordAt k) (wordAt n) = false) ∧
      (wordAt n = u ∧ atomCandidateMassQ M s (wordAt n) = r) := by
  simp [enumerateAtoms, Option.ite_none_right_eq_some]

/-- Every returned entry is a genuine positive atom with its exact rational mass. -/
theorem enumerateAtoms_sound [Fintype S] [DecidableEq S] (M : Mealy S) (s : S)
    (n : ℕ) (u : List Bool) (r : ℚ) (h : enumerateAtoms M s n = some (u,r)) :
    atomCandidate M s u ∈ P02A2.positive (law M s) ∧
      (r : ℝ) = (law M s {atomCandidate M s u}).toReal := by
  obtain ⟨⟨hp, _⟩, rfl, rfl⟩ := (enumerateAtoms_spec M s n u r).mp h
  exact ⟨(atomCandidate_positive_iff M s _).mp hp, atomCandidateMassQ_correct M s _⟩

/-- Every positive singleton eventually appears in the computable enumeration. -/
theorem enumerateAtoms_complete [Fintype S] [DecidableEq S] [Nonempty S]
    (M : Mealy S) (s : S) (y : Cantor) (hy : y ∈ P02A2.positive (law M s)) :
    ∃ n u r, enumerateAtoms M s n = some (u,r) ∧ atomCandidate M s u = y := by
  classical
  obtain ⟨u, hu, hp⟩ := (positive_iff_candidate M s y).mp hy
  have hex : ∃ n, atomCandidate M s (wordAt n) = y :=
    ⟨Encodable.encode u, by simpa only [wordAt_encode] using hu⟩
  let n := Nat.find hex
  have hn : atomCandidate M s (wordAt n) = y := Nat.find_spec hex
  have hpos : 0 < atomCandidateMassQ M s (wordAt n) :=
    (atomCandidate_positive_iff M s _).mpr (hn.symm ▸ hy)
  have hfresh : ∀ k : Fin n, atomCandidatesEqual M s (wordAt k) (wordAt n) = false := by
    intro k
    simp only [Bool.eq_false_iff, ne_eq, atomCandidatesEqual_spec]
    intro he
    exact Nat.find_min hex k.isLt (he.trans hn)
  refine ⟨n, wordAt n, atomCandidateMassQ M s (wordAt n), ?_, hn⟩
  exact (enumerateAtoms_spec M s _ _ _).mpr ⟨⟨hpos, hfresh⟩, rfl, rfl⟩

/-- Distinct returned entries denote distinct infinite output streams, not just distinct words. -/
theorem enumerateAtoms_no_duplicates [Fintype S] [DecidableEq S]
    (M : Mealy S) (s : S) (n m : ℕ) (u v : List Bool) (r z : ℚ)
    (hn : enumerateAtoms M s n = some (u,r))
    (hm : enumerateAtoms M s m = some (v,z)) (hne : n ≠ m) :
    atomCandidate M s u ≠ atomCandidate M s v := by
  obtain ⟨⟨_, hnf⟩, hnu, _⟩ := (enumerateAtoms_spec M s n u r).mp hn
  obtain ⟨⟨_, hmf⟩, hmv, _⟩ := (enumerateAtoms_spec M s m v z).mp hm
  intro he
  rcases lt_or_gt_of_ne hne with hlt | hlt
  · have hf := hmf ⟨n, hlt⟩
    simp only [Bool.eq_false_iff, ne_eq, atomCandidatesEqual_spec] at hf
    exact hf (by simpa only [hnu, hmv] using he)
  · have hf := hnf ⟨m, hlt⟩
    simp only [Bool.eq_false_iff, ne_eq, atomCandidatesEqual_spec] at hf
    exact hf (by simpa only [hnu, hmv] using he.symm)

end Orthemology.Frontier.MealyMeasure
