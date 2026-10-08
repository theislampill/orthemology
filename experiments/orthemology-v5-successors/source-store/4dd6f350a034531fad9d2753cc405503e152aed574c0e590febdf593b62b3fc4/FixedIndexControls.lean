import HiddenChangeFixedIndex
import HiddenChangeContamination
open HiddenChange MeasureTheory
open Orthemology.Tranche2.PolicyEmbedding
namespace HiddenChangeLawTests
example : fixedMode none 200 = 0 := by decide +kernel
example : fixedMode (some 0) 0 = 1 := by decide +kernel
example : fixedMode (some 1) 0 = 0 := by decide +kernel
example : fixedMode (some 1) 1 = 1 := by decide +kernel
example : fixedMode (some 1) 200 = 1 := by decide +kernel
example (s : State 1) (π : Policy Unit 1 2) (α : Adversary Unit 1 2)
    (z : (Unit × Unit) × FlatStack (TaggedPair 1 2) (State 1)) :
    stackHistoryTrajectory (adaptivePolicy s π α) z =
      stackHistoryTrajectory (fixedPolicy (firstOne (adaptiveMode s π α z)) s π) (z.1.1,z.2) :=
  actual_eq_selected_fixed s π α z
#check winsAll_iff_fixed_indices
#print axioms actual_eq_selected_fixed
#print axioms adaptive_wins_of_fixed_indices
#print axioms fixed_adversary_law
#print axioms winsAll_iff_fixed_indices
end HiddenChangeLawTests

-- Exact deterministic two-state separator on the actual stack evaluator.
open HiddenChange HiddenParity MeasureTheory Filter
open Orthemology.Tranche2.PolicyEmbedding Orthemology.Tranche2.RecurrentSupport
open HiddenParity.Stochastic HiddenParity.Adaptive
namespace HiddenChangeSeparator
noncomputable section

def policy : Policy Unit 2 1 := fun _ _ => 0
def tape : FlatStack (TaggedPair 2 1) (State 2) := fun z =>
  if z.1.1 = 0 then (if z.1.2.1 = 0 then 1 else 0) else z.1.2.1
def run (κ : ChangeIndex) := stackActionTrajectory (fixedPolicy κ 0 policy) ((),tape)
def hist (κ : ChangeIndex) := stackHistoryTrajectory (fixedPolicy κ 0 policy) ((),tape)
def fixture : HiddenChange.Input 2 1 where
  rows := #[0,1,1,0,1,0,0,1]
  priorities := #[0,1,0,1]
  menus := [⟨[0,1],0,[0]⟩,⟨[0,1],1,[0]⟩]
  interpretation := ⟨["zero","one"],["q","r"],["a"],"v1","state","exact","common"⟩

example : Admissible fixture := by decide +kernel

lemma tag (κ : ChangeIndex) (t : ℕ) : (run κ t).1 = fixedMode κ t :=
  fixed_stack_tag κ 0 policy ((),tape) t
lemma act (κ : ChangeIndex) (t : ℕ) : (run κ t).2.2 = 0 := rfl
lemma source_step (κ : ChangeIndex) (t : ℕ) :
    (run κ (t+1)).2.1 = if fixedMode κ t = 0 then
      (if (run κ t).2.1 = 0 then 1 else 0) else (run κ t).2.1 := by
  rw [show (run κ (t+1)).2.1 = stackReceipt (fixedPolicy κ 0 policy) ((),tape) t from
    fixed_stack_source_next κ 0 policy ((),tape) t]
  change (if (run κ t).1 = 0 then (if (run κ t).2.1 = 0 then 1 else 0) else (run κ t).2.1) = _
  rw [tag]

lemma immediate_source (t : ℕ) : (run (some 0) t).2.1 = 0 := by
  induction t with
  | zero => rfl
  | succ t ih => simpa [fixedMode, ih] using source_step (some 0) t
lemma late_source (t : ℕ) : (run (some 1) (t+1)).2.1 = 1 := by
  induction t with
  | zero => decide +kernel
  | succ t ih => simpa [fixedMode, ih] using source_step (some 1) (t+1)
lemma never_two (t : ℕ) : (run none (t+2)).2.1 = (run none t).2.1 := by
  rw [show t+2 = (t+1)+1 by omega, source_step, source_step]
  simp only [fixedMode, if_true]
  generalize hh : (run none t).2.1 = x
  fin_cases x <;> decide +kernel
lemma never_even (t : ℕ) : (run none (2*t)).2.1 = 0 := by
  induction t with
  | zero => rfl
  | succ t ih => rw [show 2*(t+1)=2*t+2 by omega, never_two, ih]
lemma never_even_action (t : ℕ) : run none (2*t) = (0,(0,0)) := by
  apply Prod.ext
  · exact tag none _
  · exact Prod.ext (never_even t) (act none _)
lemma immediate_action (t : ℕ) : run (some 0) t = (1,(0,0)) := by
  apply Prod.ext
  · simpa [fixedMode] using tag (some 0) t
  · exact Prod.ext (immediate_source t) (act (some 0) t)
lemma late_action (t : ℕ) : run (some 1) (t+1) = (1,(1,0)) := by
  apply Prod.ext
  · simpa [fixedMode] using tag (some 1) (t+1)
  · exact Prod.ext (late_source t) (act (some 1) (t+1))

lemma priority_source (g : TaggedPair 2 1) : fixture.priority g.1 g.2 = g.2.1.val := by
  rcases g with ⟨m,x,a⟩
  fin_cases m <;> fin_cases x <;> fin_cases a <;> decide +kernel

example : TaggedParity fixture (0,0) (hist none) := by
  unfold TaggedParity hist
  rw [← stackActionTrajectory_eq_historyAction]
  change ParitySuccess (fun g => fixture.priority g.1 g.2) (run none)
  refine ⟨0, ⟨⟨(0,(0,0)), ?_, rfl⟩, ?_⟩, rfl⟩
  · rw [mem_recurrentSet]
    simp only [Recurs, frequently_atTop]
    intro N
    exact ⟨2*N, by omega, never_even_action N⟩
  · intro _ _; exact Nat.zero_le _
example : TaggedParity fixture (0,0) (hist (some 0)) := by
  unfold TaggedParity hist
  rw [← stackActionTrajectory_eq_historyAction]
  change ParitySuccess (fun g => fixture.priority g.1 g.2) (run (some 0))
  refine ⟨0, ⟨⟨(1,(0,0)), ?_, rfl⟩, ?_⟩, rfl⟩
  · rw [mem_recurrentSet]
    simp only [Recurs, frequently_atTop]
    intro N
    exact ⟨N, le_rfl, immediate_action N⟩
  · intro _ _; exact Nat.zero_le _
example : ¬ TaggedParity fixture (0,0) (hist (some 1)) := by
  unfold TaggedParity hist
  rw [← stackActionTrajectory_eq_historyAction]
  change ¬ ParitySuccess (fun g => fixture.priority g.1 g.2) (run (some 1))
  intro ⟨d,⟨⟨e,he,hed⟩,_⟩,heven⟩
  have hsub := recurrentSet_subset_of_eventually_mem (run (some 1)) {(1,(1,0))}
    (show ∀ᶠ t in atTop, run (some 1) t ∈ ({(1,(1,0))} : Finset (TaggedPair 2 1)) from by
      rw [eventually_atTop]
      refine ⟨1,fun t ht => ?_⟩
      obtain ⟨j,rfl⟩ := Nat.exists_eq_succ_of_ne_zero (by omega : t ≠ 0)
      simpa only [late_action, Finset.mem_singleton])
  have heq := Finset.mem_singleton.mp (hsub he)
  subst e
  have hd : d = 1 := hed.symm
  subst d
  contradiction
end
end HiddenChangeSeparator
