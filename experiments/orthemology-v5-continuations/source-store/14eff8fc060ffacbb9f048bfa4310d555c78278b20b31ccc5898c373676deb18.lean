import RecursivePhysicalBudget

namespace IndependentPhysicalCostControls
open Orthemology.Tranche2 Orthemology.Tranche2.PhysicalFlattening
open Orthemology.Tranche3 Orthemology.Tranche3.PhysicalCost
open scoped ENNReal BigOperators

theorem boundary_01 : listCost (fun a : ℕ => (a : ℝ≥0∞)) [2,2,3] = 7 := by norm_num [listCost]
theorem boundary_02 : listCost (badActionCost ({0} : Finset ℕ)) [1,1,0,2] = 3 := by norm_num [listCost,badActionCost]
theorem boundary_03 : plannedBadCount ({0} : Finset ℕ) [1,1,0,2] = 3 := by decide
theorem boundary_04 : listCost (fun _ : ℕ => (⊤ : ℝ≥0∞)) [] = 0 := rfl
theorem boundary_05 : listCost (fun _ : ℕ => (⊤ : ℝ≥0∞)) [0] = ⊤ := by simp [listCost]
theorem boundary_06 : listCost (badActionCost ({0} : Finset ℕ)) [1,1] = 2 ∧
    ([1,1] : List ℕ).toFinset.card = 1 := by norm_num [listCost,badActionCost]

-- A complete block has two bad actions; an immediate exit has only one.
def firstExit : StopObs Bool 3 := Sum.inl true
theorem boundary_07 : stoppedActions [1,0,2] firstExit = [1] := rfl
theorem boundary_08 : plannedBadCount ({0} : Finset ℕ) (stoppedActions [1,0,2] firstExit) = 1 := by decide
theorem boundary_09 : plannedBadCount ({0} : Finset ℕ) [1,0,2] = 2 := by decide
theorem boundary_10 : stopped_bad_count_le_planned ({0} : Finset ℕ) [1,0,2] firstExit =
    stopped_bad_count_le_planned ({0} : Finset ℕ) [1,0,2] firstExit := rfl

-- Initial placeholders must be skipped by the fixed-prefix decoder.
def initialEmpty : ℕ → List ℕ | 0 => [] | _+1 => [0]
theorem boundary_11 : decode 9 initialEmpty 0 = 9 := rfl
theorem boundary_12 : decode 9 (fun n => initialEmpty (n+1)) 0 = 0 := rfl
theorem boundary_13 : decode 9 (fun n => initialEmpty (n+1)) 3 = 0 := rfl

-- An unbounded stream may have an early empty block; total decoder conservation
-- requires the stronger all-nonempty premise used by the actual recorded law.
def intermittent : ℕ → List ℕ | 0 => [0] | 1 => [] | _+2 => [1]
theorem boundary_14 : decode 9 intermittent 1 = 9 := rfl
theorem boundary_15 : (prefixActions intermittent 3).getD 1 9 = 1 := rfl
theorem boundary_16 : ∀ n, (fun _ : ℕ => ([] : List ℕ)) n = [] := fun _ => rfl
theorem boundary_17 : ¬ Unbounded (fun _ : ℕ => ([] : List ℕ)) := by
  intro h
  obtain ⟨n,hn⟩ := h 0
  simp [prefixLength] at hn

-- Repeated labels are distinct physical positions.
def repeated : ℕ → List ℕ := fun _ => [7,7]
lemma repeated_nonempty : ∀ n, repeated n ≠ [] := by intro n; simp [repeated]
theorem boundary_18 : decode 0 repeated 0 = 7 := rfl
theorem boundary_19 : decode 0 repeated 1 = 7 := rfl
theorem boundary_20 : decode 0 repeated 2 = 7 := rfl
theorem boundary_21 : Function.Bijective (fun ni : Σ n, Fin (repeated n).length =>
    prefixLength repeated ni.1 + ni.2.val) :=
  physicalPosition_bijective repeated (unbounded_of_nonempty repeated repeated_nonempty)
theorem boundary_22 (c : ℕ → ℝ≥0∞) :
    (∑' t, c (decode 0 repeated t)) = ∑' n, listCost c (repeated n) :=
  decode_total_cost c 0 repeated repeated_nonempty

-- The general flatten theorem permits earlier empty blocks as soon as length is unbounded.
theorem boundary_23 (blocks : ℕ → List ℕ) (hu : Unbounded blocks) (n : ℕ)
    (i : Fin (blocks n).length) :
    flatten blocks hu (prefixLength blocks n + i.val) = (blocks n).get i :=
  flatten_at_offset blocks hu n i

end IndependentPhysicalCostControls
