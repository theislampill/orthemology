import ExecutablePruning

/-! Kernel-checked finite controls. `decide` is ordinary proof reduction; no
`native_decide` or custom trusted computation axiom is used. -/
namespace HiddenParity.Controls

set_option maxRecDepth 100000
set_option maxHeartbeats 8000000

abbrev One := Fin 1
abbrev Two := Fin 2
abbrev Three := Fin 3
abbrev Four := Fin 4

/-- Explicit reduced rational avoids opacity of the library inverse under decide. -/
def half : ℚ := ⟨1, 2, by decide, by decide⟩
theorem half_eq : half = (1 / 2 : ℚ) := by rw [half, Rat.mk'_eq_divInt, Rat.divInt_eq_div]; norm_num

def sourceOne (_ : Three) : One := 0
def succOne (_ : Three) : Finset One := {0}
def sameRow (_ : Two) (_ : Three) : ℚ := 1

def cascadePriority (m : Two) (e : Three) : ℕ :=
  if m = 0 then 2 else if e = 0 then 1 else if e = 1 then 3 else 4

/-- One deleting round removes only priority 1, so priority 3 still needs recomputation. -/
theorem cascade_first_round :
    executableStep sourceOne succOne Finset.univ sameRow cascadePriority 0 Finset.univ =
      ({1, 2} : Finset Three) := by decide

theorem cascade_second_round :
    executableStep sourceOne succOne Finset.univ sameRow cascadePriority 0 {1, 2} =
      ({2} : Finset Three) := by decide

theorem cascade_output :
    executableOutput sourceOne succOne Finset.univ sameRow cascadePriority 0 Finset.univ =
      ({({2} : Finset Three)} : Finset (Finset Three)) := by decide

-- Full rows over two observed outcomes. The candidate never exits state 0.
def zeroSource (_ : Three) : Two := 0
def zeroSucc (_ : Three) : Finset Two := {0}
def revealRow (m : Three) (e : Three) (y : Two) : ℚ :=
  if m = 2 ∧ e = 0 then half else if y = 0 then 1 else 0

def revealPriority (m : Three) (e : Three) : ℕ :=
  if m = 0 then 2 else if m = 1 ∧ e = 0 then 1
  else if m = 2 ∧ e = 1 then 1 else 4

/-- Rival 2 is initially distinguishable by pair 0. -/
theorem rival_initially_unmatched :
    ¬ Match revealRow (0 : Three) 2 (Finset.univ : Finset Three) := by decide

/-- Deleting the discriminating row makes rival 2 match. -/
theorem rival_newly_matches :
    Match revealRow (0 : Three) 2 ({1, 2} : Finset Three) := by decide

theorem rival_first_round :
    executableStep zeroSource zeroSucc Finset.univ revealRow revealPriority 0 Finset.univ =
      ({1, 2} : Finset Three) := by decide

theorem rival_second_round :
    executableStep zeroSource zeroSucc Finset.univ revealRow revealPriority 0 {1, 2} =
      ({2} : Finset Three) := by decide

theorem rival_output :
    executableOutput zeroSource zeroSucc Finset.univ revealRow revealPriority 0 Finset.univ =
      ({({2} : Finset Three)} : Finset (Finset Three)) := by decide

-- Forced two-state cycle: both used pairs are needed for closure and recurrence.
def cycleSource (e : Two) : Two := e
def cycleSucc (e : Two) : Finset Two := if e = 0 then {1} else {0}
def cycleRow (_ : One) (e y : Two) : ℚ := if y = (if e = 0 then 1 else 0) then 1 else 0
def cycle23 (_ : One) (e : Two) : ℕ := if e = 0 then 2 else 3
def cycle21 (_ : One) (e : Two) : ℕ := if e = 0 then 2 else 1
def cycle01 (_ : One) (e : Two) : ℕ := if e = 0 then 0 else 1

/-- Higher odd priorities are retained when below them a recurrent even minimum exists. -/
theorem higher_odd_cycle_retained :
    executableOutput cycleSource cycleSucc Finset.univ cycleRow cycle23 0 Finset.univ =
      ({(Finset.univ : Finset Two)} : Finset (Finset Two)) := by decide

/-- CoBüchi's bad=1/good=2 encoding rejects the forced alternating cycle. -/
theorem cobuchi_21_cycle_rejected :
    executableOutput cycleSource cycleSucc Finset.univ cycleRow cycle21 0 Finset.univ =
      (∅ : Finset (Finset Two)) := by decide

/-- 0/1 instead accepts it, so it cannot be the coBüchi specialization. -/
theorem wrong_01_encoding_distinguished :
    executableOutput cycleSource cycleSucc Finset.univ cycleRow cycle01 0 Finset.univ =
      ({(Finset.univ : Finset Two)} : Finset (Finset Two)) := by decide

-- Compare full rows, not rows conditioned on the common no-exit successor.
def singleSource (_ : One) : Two := 0
def singleSucc (_ : One) : Finset Two := {0}
def exitRow (m : Two) (_ : One) (y : Two) : ℚ :=
  if m = 0 then if y = 0 then 1 else 0 else half

def oppositePriority (m : Two) (_ : One) : ℕ := if m = 0 then 2 else 1

def sameSingleRow (_ : Two) (_ : One) (y : Two) : ℚ := if y = 0 then 1 else 0

/-- A rival with a positive exit has a different full row and is not a matching rival. -/
theorem full_row_difference_retains_target :
    executableOutput singleSource singleSucc Finset.univ exitRow oppositePriority 0 Finset.univ =
      ({(Finset.univ : Finset One)} : Finset (Finset One)) := by decide

/-- Candidate-only parity checking would incorrectly accept this component. -/
theorem equal_row_odd_rival_rejects :
    executableOutput singleSource singleSucc Finset.univ sameSingleRow oppositePriority 0 Finset.univ =
      (∅ : Finset (Finset One)) := by decide

-- Deletion of a cross edge splits components; pair 2 is then in no MEC.
def splitSource (e : Four) : Two := if e < 2 then 0 else 1
def splitSucc (e : Four) : Finset Two := if e = 0 ∨ e = 2 then {0} else {1}
def splitRow (_ : One) (e : Four) (y : Two) : ℚ :=
  if y = (if e = 0 ∨ e = 2 then 0 else 1) then 1 else 0

def splitPriority (_ : One) (e : Four) : ℕ :=
  if e = 0 then 4 else if e = 1 then 1 else if e = 2 then 2 else 3

theorem split_first_round :
    executableStep splitSource splitSucc Finset.univ splitRow splitPriority 0 Finset.univ =
      ({0, 2, 3} : Finset Four) := by decide

theorem split_recomputed_components :
    executableMECs splitSource splitSucc ({0, 2, 3} : Finset Four) =
      ({({0} : Finset Four), {3}} : Finset (Finset Four)) := by decide

theorem split_output :
    executableOutput splitSource splitSucc Finset.univ splitRow splitPriority 0 Finset.univ =
      ({({0} : Finset Four)} : Finset (Finset Four)) := by decide

theorem empty_input :
    executableOutput sourceOne succOne Finset.univ sameRow cascadePriority 0 ∅ =
      (∅ : Finset (Finset Three)) := by decide

def emptySucc (_ : One) : Finset Two := ∅
def openSucc (_ : One) : Finset Two := {1}

theorem empty_successors_rejected :
    executableMECs singleSource emptySucc Finset.univ =
      (∅ : Finset (Finset One)) := by decide

theorem no_closed_component_rejected :
    executableMECs singleSource openSucc Finset.univ =
      (∅ : Finset (Finset One)) := by decide

end HiddenParity.Controls
