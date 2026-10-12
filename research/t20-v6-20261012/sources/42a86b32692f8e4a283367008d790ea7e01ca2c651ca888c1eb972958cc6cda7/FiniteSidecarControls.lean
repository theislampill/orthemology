import SourceCorrectionHistories
import Mathlib.Tactic.FinCases

namespace FiniteSidecar.Controls
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive
open JointCompletion (HasJ)
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

/-- Accepted coarse state 0 has four support/price classes; rejected state 1 has two.
This is a declared finite operational example, not an actual-warrant assignment. -/
def withdrawA : Tables :=
  ⟨[[0,0,1,1],[0,0,0,0]], [[1,1,0,0],[1,1,1,1]], [[0,1,2,3],[0,1,0,1]]⟩
def costRows : List (List Nat) := [[1,9,1,9],[1,9,0,0]]
def currentRows : List (List Nat) := [[1,1,1,1],[0,0,0,0]]

theorem table_separates {z i j : Nat} (rows : List (List Nat))
    (h : tableValue rows 0 z i ≠ tableValue rows 0 z j) :
    ObservablyDifferent (encodeState z i) (encodeState z j) :=
  ⟨tableObserver rows, tableValue rows 0 z i, tableValue rows 0 z j,
    oldJ (tableObserver_has rows 0), tableObserver_observes rows 0 (encoded_represents z i),
    tableObserver_observes rows 0 (encoded_represents z j), h⟩

/-- Current accepted verdict alone does not distinguish the four classes. -/
theorem current_same (i : Fin 4) :
    NatObs (eval (.app (tableObserver currentRows) (encodeState 0 i.val)) zeroEnv) 1 := by
  have h := tableObserver_observes currentRows 0 (encoded_represents 0 i.val)
  fin_cases i <;> exact h

/-- The specified cost and withdrawal observers jointly require all four classes. -/
theorem four_required (i j : Fin 4) (hij : i ≠ j) :
    ObservablyDifferent (encodeState 0 i.val) (encodeState 0 j.val) := by
  fin_cases i <;> fin_cases j
  all_goals first
    | exact (hij rfl).elim
    | exact table_separates costRows (by decide)
    | exact table_separates withdrawA.branch (by decide)

/-- First two supporting classes are withdrawn; the other two retain accepted status. -/
example : (runCodes [withdrawA] 0 0) = ([0], (1,0)) := rfl
example : (runCodes [withdrawA] 0 1) = ([0], (1,1)) := rfl
example : (runCodes [withdrawA] 0 2) = ([1], (0,2)) := rfl
example : (runCodes [withdrawA] 0 3) = ([1], (0,3)) := rfl
example : (runCodes [withdrawA,withdrawA] 0 0) = ([0,0], (1,0)) := rfl

/-- These are literal source outputs, with source identities for each branch. -/
example : List.Forall₂ (fun b n => HasJ [] (.atom .i) (.identity N b (inputNumeral n)))
    (runSource [withdrawA,withdrawA] (encodeState 0 0)).1 [0,0] :=
  runSource_branch_identities [withdrawA,withdrawA] (encodeState_has 0 0) (encoded_represents 0 0)

/-- Reusing tag 0 across different retained coarse values remains distinguishable. -/
example : ¬ ∃ e, HasJ [] e (.identity State (encodeState 0 0) (encodeState 1 0)) := by
  rw [encoded_identity_iff]
  decide

/-- Two ordinary tags cannot encode four source-observable required states,
even if the proof terms are all chosen differently. -/
theorem two_tags_cannot_hide_four (tag : Fin 4 → Fin 2) (evidence : Fin 4 → Poly)
    (he : ∀ i, HasJ [] (evidence i) Evidence) :
    ¬ (∀ i j, i ≠ j → ObservablyDifferent
      (withEvidence 0 (tag i).val (evidence i))
      (withEvidence 0 (tag j).val (evidence j))) := by
  intro h
  have impossible := finite_fibre_lower_bound 0 tag evidence he h
  omega

example : (∀ z : Fin 2, ([4,2][z.val]?.getD 0) ≤ 4) := by decide
example : (∃ tags : (z : Fin 2) → Fin ([4,2][z.val]?.getD 0) → Fin 4,
    ∃ evidence : (z : Fin 2) → Fin ([4,2][z.val]?.getD 0) → Poly,
      (∀ z i, HasJ [] (evidence z i) Evidence) ∧
      (∀ z i j, i ≠ j → ObservablyDifferent
        (withEvidence z.val (tags z i).val (evidence z i))
        (withEvidence z.val (tags z j).val (evidence z j)))) := by
  apply (common_alphabet_exact (fun z : Fin 2 => [4,2][z.val]?.getD 0)).mpr
  decide

/-- Empty and out-of-range tables follow their declared default, not an invented Fin typing. -/
example : tableValue [] 73 0 0 = 73 := rfl
example : tableValue [[5]] 73 4 0 = 73 := rfl
example : tableValue [[5]] 73 0 4 = 73 := rfl
example : tableValue (tabulate 0 0 (fun _ _ => 7)) 0 0 0 = 0 := rfl
example : (runCodes [] 9 11) = ([], (9,11)) := rfl

/-- Failure of rectangle closure is visible: the source type alone does not block it. -/
def escaping : Tables := ⟨[[0]], [[7]], [[0]]⟩
example : ¬ ClosedRectangle 1 1 escaping := by
  intro h
  have bad := (h 0 0 (by decide) (by decide)).1
  change 7 < 1 at bad
  omega
example : Has [] (controller escaping) (arr State Reply) := controller_has escaping
example : (runCodes [escaping,escaping] 0 0) = ([0,0], (0,0)) := rfl

#print axioms four_required
#print axioms two_tags_cannot_hide_four
end FiniteSidecar.Controls
