import SCCParity

namespace IndependentMECReview
open HiddenParity
set_option maxHeartbeats 8000000
set_option maxRecDepth 100000
abbrev V := Fin 4
abbrev E := Fin 5

def src (e : E) : V := if e=0 ∨ e=1 then 0 else if e=2 then 1 else 2
def nxt (e : E) : Finset V :=
  if e=0 then {0} else if e=1 then {1} else if e=2 then {2} else if e=3 then {1} else {0,3}

theorem first_cleanup : SCCPruning.step src nxt Finset.univ = ({0,1,2,3} : Finset E) := by decide
theorem reverse_path_cleanup : SCCPruning.step src nxt ({0,1,2,3} : Finset E) = {0,2,3} := by decide
theorem two_final_components : SCCPruning.mecs src nxt Finset.univ =
    ({({0} : Finset E),{2,3}} : Finset (Finset E)) := by decide

def onePass : Finset (Finset E) :=
  let K := SCCPruning.step src nxt Finset.univ
  K.image (fun e => SCCPruning.cluster src nxt K (src e))
theorem one_pass_is_wrong : onePass ≠ SCCPruning.mecs src nxt Finset.univ := by decide
theorem one_pass_retains_nonclosed_cluster : ({0,1} : Finset E) ∈ onePass ∧
    ¬ IsEndComponent src nxt ({0,1} : Finset E) := by decide

abbrev One := Fin 1
abbrev Two := Fin 2
abbrev Three := Fin 3
abbrev Four := Fin 4

def selfSource (_e : Four) : One := 0
def selfSucc (_e : Four) : Finset One := {0}
def sameRow (_m : One) (_e : Four) : Nat := 0
def allOdd (_m : One) (e : Four) : Nat := 2*e.val+1

theorem too_little_parity_fuel_retains_odd_pair :
    SCCPruning.parityIterate selfSource selfSucc Finset.univ sameRow allOdd 0 3 Finset.univ =
      ({3} : Finset Four) := by decide
theorem exact_pair_fuel_eliminates_all_odd :
    SCCPruning.parityOutput selfSource selfSucc Finset.univ sameRow allOdd 0 Finset.univ = ∅ := by decide

def cycleSource (e : Two) : Two := e
def cycleSucc (e : Two) : Finset Two := if e=0 then {1} else {0}
def cycleRow (_m : One) (_e : Two) : Nat := 0
def cyclePriority (_m : One) (e : Two) : Nat := if e=0 then 2 else 101

theorem higher_odd_is_retained :
    SCCPruning.parityOutput cycleSource cycleSucc Finset.univ cycleRow cyclePriority 0 Finset.univ =
      ({(Finset.univ : Finset Two)} : Finset (Finset Two)) := by decide

def rematchSource (_e : Three) : One := 0
def rematchSucc (_e : Three) : Finset One := {0}
def rematchRows (m : Two) (e : Three) : Nat := if m=1 ∧ e=0 then 1 else 0
def rematchPriority (m : Two) (e : Three) : Nat :=
  if m=0 then (if e=0 then 1 else if e=1 then 2 else 4)
  else (if e=1 then 1 else 2)

theorem newly_matching_rival_is_rechecked :
    SCCPruning.parityOutput rematchSource rematchSucc Finset.univ rematchRows rematchPriority 0 Finset.univ =
      ({({2} : Finset Three)} : Finset (Finset Three)) := by decide

def third : ℚ := ⟨1, 3, by decide, by decide⟩
def twoThirds : ℚ := ⟨2, 3, by decide, by decide⟩
theorem third_eq : third = (1/3 : ℚ) := by rw [third, Rat.mk'_eq_divInt, Rat.divInt_eq_div]; norm_num
theorem twoThirds_eq : twoThirds = (2/3 : ℚ) := by rw [twoThirds, Rat.mk'_eq_divInt, Rat.divInt_eq_div]; norm_num

def fullRows (m : Two) (_e : One) (s : Two) : ℚ :=
  if m=0 then (if s=0 then 1 else 0) else (if s=0 then third else twoThirds)
def kernel : RationalKernel Two One Two where
  row := fullRows
  nonnegative := by intro m e s; fin_cases m <;> fin_cases e <;> fin_cases s <;> norm_num [fullRows, third_eq, twoThirds_eq]
  normalized := by intro m e; fin_cases m <;> fin_cases e <;> norm_num [fullRows, third_eq, twoThirds_eq, Fin.sum_univ_two]
def pairSource (_e : One) : Two := 0
def priorities (m : Two) (_e : One) : Nat := if m=0 then 2 else 1

theorem full_rows_do_not_match : ¬ Match kernel.row (0:Two) (1:Two) (Finset.univ : Finset One) := by decide
theorem candidate_zero_exit_target :
    SCCPruning.markovTarget kernel pairSource Finset.univ priorities 0 Finset.univ = ({0} : Finset Two) := by decide
theorem rival_positive_exit_rejected :
    SCCPruning.markovTarget kernel pairSource Finset.univ priorities 1 Finset.univ = (∅ : Finset Two) := by decide

def oneKernel : RationalKernel One One One where
  row := fun _ _ _ => 1
  nonnegative := by intros; norm_num
  normalized := by intros; simp
def oneSource (_e : One) : One := 0
def oddPriority (_m : One) (_e : One) : Nat := 1
/-- Exact predicate semantics do not manufacture a live-candidate premise. -/
theorem empty_live_set_scope_boundary :
    SCCPruning.markovTarget oneKernel oneSource ∅ oddPriority 0 Finset.univ = ({0} : Finset One) := by decide

set_option pp.explicit true in
#check @SCCPruning.mecs_eq_executable
set_option pp.explicit true in
#check @SCCPruning.parityOutput_exact
set_option pp.explicit true in
#check @SCCPruning.markovTarget_exact
#print axioms one_pass_is_wrong
#print axioms one_pass_retains_nonclosed_cluster
#print axioms exact_pair_fuel_eliminates_all_odd
#print axioms higher_odd_is_retained
#print axioms newly_matching_rival_is_rechecked
#print axioms full_rows_do_not_match
#print axioms candidate_zero_exit_target
#print axioms rival_positive_exit_rejected
#print axioms empty_live_set_scope_boundary
end IndependentMECReview
