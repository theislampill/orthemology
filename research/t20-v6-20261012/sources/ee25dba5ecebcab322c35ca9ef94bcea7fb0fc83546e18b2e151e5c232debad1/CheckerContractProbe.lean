import CheckerControls

namespace PDCheckerIndependentReview
noncomputable section
open PDChecker
open scoped ENNReal

/-- Changing the action's requested branch at a universal control cannot change
the actual PMF. The machine chooses its own fair branch. -/
theorem universal_ignores_action_branch {m : ℕ} {Q Γ : Type*} [DecidableEq Γ]
    (M : Machine Q Γ) (s : State m Q Γ) (g : Γ) (b c : Bool)
    (hu : isUniversal M s=true) : kernel M s (g,b)=kernel M s (g,c) := by
  have hadv (d : Bool) : advance M s (g,b) d=advance M s (g,c) d := by
    cases s <;> rfl
  have hout : branchOutput M s (g,b)=branchOutput M s (g,c) := by
    funext d
    simp only [branchOutput,hadv]
  simp only [kernel,hu,↓reduceIte,hout]

/-- The lift adds an observation copy only; its old last label does not alter
the underlying control transition. -/
theorem old_copy_label_irrelevant {m : ℕ} {Q Γ : Type*} [DecidableEq Γ]
    (M : Machine Q Γ) (i : Fin m) (g : Γ) (q : Q) (h : Fin m)
    (x y : LastReceipt) (a : Action Γ) :
    liftedKernel M (.live i g q h x) a=liftedKernel M (.live i g q h y) a := rfl

theorem rejecting_target_visible {m : ℕ} {Q Γ : Type*} (s : LiftState m Q Γ) :
    observe s=.reject ↔ s=.bottom := by
  cases s with
  | live i g q h last => cases last <;> simp [observe,LastReceipt.observe]
  | top => simp [observe]
  | bottom => simp [observe]

theorem rejecting_target_absorbing {m : ℕ} {Q Γ : Type*} [DecidableEq Γ]
    (M : Machine Q Γ) (a : Action Γ) :
    liftedKernel (m:=m) M .bottom a=PMF.pure .bottom := by
  simp [liftedKernel,erase,kernel_bottom,PMF.pure_map,copyOutcome]

/-- Pointwise contract readback of the joint-row reconstruction. The initial
belief and the machine are the only construction data; no PD premise is used. -/
theorem raw_lifted_joint_entry {m : ℕ} {Q Γ : Type*} [DecidableEq Γ]
    (M : Machine Q Γ) (s : LiftState m Q Γ) (a : Action Γ)
    (o : Receipt) (t : State m Q Γ) :
    (PMF.map (fun q => (observe q,erase q)) (liftedKernel M s a)) (o,t)=
      kernel M (erase s) a (o,t) := by
  rw [lifted_joint_row_exact]

/-- Hidden mixing gives positive mass to all checker indices while revealing
only the same common initial label. -/
theorem initial_hidden_mixing_contract {m : ℕ} {Q Γ : Type*} [Nonempty (Fin m)]
    (tape : Fin m → Γ) (q0 : Q) (h0 : Fin m) :
    (∀ i : Fin m, 0 < initialBelief tape q0 h0 (initialAt tape q0 h0 i)) ∧
    PMF.map erase (initialLiftBelief tape q0 h0)=initialBelief tape q0 h0 ∧
    PMF.map observe (initialLiftBelief tape q0 h0)=PMF.pure .ordinary :=
  ⟨initialBelief_positive tape q0 h0,initial_lift_erases tape q0 h0,initial_lift_common_label tape q0 h0⟩

/-- ValidOutput really is necessary for reading the copied observation: the
total fallback must not be used to justify arbitrary inconsistent pairs. -/
theorem invalid_copy_does_not_preserve_receipt :
    observe (copyOutcome (.accept,PDChecker.Controls.checker0)) ≠ Receipt.accept := by decide

def mixedTerminalMachine : Machine Unit Bool where
  universal _ := true
  step _ _ b := ⟨false,(if b then .accept else .reject),0⟩

theorem distinct_terminal_half_masses :
    kernel mixedTerminalMachine PDChecker.Controls.checker0 (false,false) (.accept,.top)=(2:ℝ≥0∞)⁻¹ ∧
    kernel mixedTerminalMachine PDChecker.Controls.checker0 (false,false) (.reject,.bottom)=(2:ℝ≥0∞)⁻¹ := by
  have h0 : branchOutput mixedTerminalMachine PDChecker.Controls.checker0 (false,false) false=(.reject,State.bottom) := by decide
  have h1 : branchOutput mixedTerminalMachine PDChecker.Controls.checker0 (false,false) true=(.accept,State.top) := by decide
  constructor <;> rw [kernel_universal_row _ _ _ (by rfl),h0,h1] <;> simp

/-- An unchecked wrong symbol is not locally detected. Detection belongs to
the retained checker at the actual head, not every private checker. -/
theorem unchecked_false_read_not_rejected :
    advance PDChecker.Controls.forkMachine PDChecker.Controls.checker1 (true,false) false=
      PDChecker.Controls.checker1 := by decide

/-- Signed bounds reject moves far beyond either boundary, even on acceptance. -/
example : advance (PDChecker.Controls.acceptingMachine 100) PDChecker.Controls.checker0
    (false,false) false=.bottom := by decide
example : advance (PDChecker.Controls.acceptingMachine (-100)) PDChecker.Controls.checker0
    (false,false) false=.bottom := by decide

#print axioms universal_ignores_action_branch
#print axioms old_copy_label_irrelevant
#print axioms rejecting_target_visible
#print axioms rejecting_target_absorbing
#print axioms raw_lifted_joint_entry
#print axioms initial_hidden_mixing_contract
#print axioms invalid_copy_does_not_preserve_receipt
#print axioms distinct_terminal_half_masses
#print axioms unchecked_false_read_not_rejected

end
end PDCheckerIndependentReview
