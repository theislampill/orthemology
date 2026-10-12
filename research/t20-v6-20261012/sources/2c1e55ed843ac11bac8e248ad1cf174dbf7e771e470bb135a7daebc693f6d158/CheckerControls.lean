import HonestCheckerStep

namespace PDChecker.Controls
noncomputable section
open PDChecker
open scoped ENNReal

abbrev CState := State 2 Unit Bool

def tape : Fin 2 → Bool := fun _ => false
def checker0 : CState := initialAt tape () 0 0
def checker1 : CState := initialAt tape () 0 1
def written0 : CState := .live 0 true () 0

def forkMachine : Machine Unit Bool where
  universal _ := true
  step _ _ b := ⟨b,.running (),0⟩

def acceptingMachine (shift : ℤ) : Machine Unit Bool where
  universal _ := true
  step _ _ _ := ⟨false,.accept,shift⟩

lemma checked_write : advance forkMachine checker0 (false,false) true=written0 := by decide
lemma unchecked_symbol_retained : advance forkMachine checker1 (false,false) true=checker1 := by decide
lemma false_read_rejected : advance forkMachine checker0 (true,false) true=.bottom := by decide
lemma accepting_outside_rejected :
    advance (acceptingMachine 1) (.live 1 false () 1 : CState) (false,false) true=.bottom := by decide
lemma accepting_inside_succeeds :
    advance (acceptingMachine 0) (.live 1 false () 1 : CState) (false,false) true=.top := by decide
lemma negative_head_rejected :
    advance (acceptingMachine (-1)) checker0 (false,false) true=.bottom := by decide

lemma fork_false_output : branchOutput forkMachine checker0 (false,false) false=(.universal false,checker0) := by decide
lemma fork_true_output : branchOutput forkMachine checker0 (false,false) true=(.universal true,written0) := by decide

lemma fork_false_mass : kernel forkMachine checker0 (false,false) (.universal false,checker0)=(2:ℝ≥0∞)⁻¹ := by
  rw [kernel_universal_row _ _ _ (by rfl),fork_false_output,fork_true_output]
  simp

lemma fork_true_mass : kernel forkMachine checker0 (false,false) (.universal true,written0)=(2:ℝ≥0∞)⁻¹ := by
  rw [kernel_universal_row _ _ _ (by rfl),fork_false_output,fork_true_output]
  simp

lemma failed_read_point_mass : kernel forkMachine checker0 (true,false)=PMF.pure (.reject,State.bottom) := by
  exact kernel_failed_read forkMachine 0 false () 0 (true,false) rfl (by decide)

lemma terminal_branches_merge :
    kernel (acceptingMachine 0) checker0 (false,false)=PMF.pure (.accept,State.top) := by
  have hb : branchOutput (acceptingMachine 0) checker0 (false,false)=
      Function.const Bool (.accept,State.top) := by
    funext b
    cases b <;> decide
  rw [kernel,if_pos (by rfl),hb]
  exact PMF.map_const _ _

lemma initial_checker0_mass : initialBelief tape () 0 checker0=(2:ℝ≥0∞)⁻¹ :=
  initialBelief_apply tape () 0 0
lemma initial_checker1_mass : initialBelief tape () 0 checker1=(2:ℝ≥0∞)⁻¹ :=
  initialBelief_apply tape () 0 1
lemma initial_checkers_different : checker0≠checker1 := by decide

/-- The tempting known-state boot implementation chooses a hidden checker under
one receipt. It is a genuine normalized PMF kernel and fails posterior determinism. -/
def badBootKernel : Option CState → Unit → PMF (Receipt × Option CState)
  | none,_ => PMF.map (fun b : Bool => (.ordinary,some (if b then checker1 else checker0))) fairBit
  | some s,_ => PMF.pure (.ordinary,some s)

def badBootInitial : PMF (Option CState) := PMF.pure none

lemma boot_is_known : badBootInitial none=1 := by simp [badBootInitial,PMF.pure_apply]

lemma boot_mass0 : badBootKernel none () (.ordinary,some checker0)=(2:ℝ≥0∞)⁻¹ := by
  simp [badBootKernel,PMF.map_apply,tsum_fintype,fairBit_apply,checker0,checker1,initialAt]

lemma boot_mass1 : badBootKernel none () (.ordinary,some checker1)=(2:ℝ≥0∞)⁻¹ := by
  simp [badBootKernel,PMF.map_apply,tsum_fintype,fairBit_apply,checker0,checker1,initialAt]

theorem known_state_hidden_selection_not_pd : ¬ PosteriorDeterministic badBootKernel := by
  intro h
  have heq := h none () .ordinary (some checker0) (some checker1)
    (by rw [boot_mass0];simp) (by rw [boot_mass1];simp)
  exact initial_checkers_different (Option.some.inj heq)

/-- Suppressing the fair branch receipt also breaks PD without changing the physical updates. -/
def badHiddenBranchKernel (s : CState) (a : Action Bool) : PMF (Receipt × CState) :=
  PMF.map (fun b : Bool => (.ordinary,advance forkMachine s a b)) fairBit

lemma hidden_mass0 : badHiddenBranchKernel checker0 (false,false) (.ordinary,checker0)=(2:ℝ≥0∞)⁻¹ := by
  simp [badHiddenBranchKernel,PMF.map_apply,tsum_fintype,fairBit_apply,
    checker0,initialAt,tape,advance,forkMachine,checkedHead,emit]

lemma hidden_mass1 : badHiddenBranchKernel checker0 (false,false) (.ordinary,written0)=(2:ℝ≥0∞)⁻¹ := by
  simp [badHiddenBranchKernel,PMF.map_apply,tsum_fintype,fairBit_apply,
    checker0,written0,initialAt,tape,advance,forkMachine,checkedHead,emit]

theorem suppressed_branch_receipt_not_pd : ¬ PosteriorDeterministic badHiddenBranchKernel := by
  intro h
  have heq := h checker0 (false,false) .ordinary checker0 written0
    (by rw [hidden_mass0];simp) (by rw [hidden_mass1];simp)
  exact (by decide : checker0≠written0) heq

example : Fintype.card (State 2 Bool Bool)=18 := by rw [card_state];decide
example : Fintype.card (LiftState 2 Bool Bool)=50 := by rw [card_liftState];decide
example : Fintype.card Receipt=5 := card_receipt

#print axioms PDChecker.kernel_posterior_deterministic
#print axioms PDChecker.advance_failed_read
#print axioms PDChecker.advance_outside
#print axioms PDChecker.advance_running
#print axioms PDChecker.kernel_failed_read
#print axioms PDChecker.kernel_universal_row
#print axioms PDChecker.kernel_entry_values
#print axioms PDChecker.card_state
#print axioms PDChecker.initialBelief_support
#print axioms PDChecker.initialBelief_apply
#print axioms PDChecker.initialBelief_positive
#print axioms PDChecker.initialBelief_normalized
#print axioms PDChecker.lifted_kernel_posterior_deterministic
#print axioms PDChecker.lifted_joint_row_exact
#print axioms PDChecker.observe_accept_iff
#print axioms PDChecker.lifted_top_absorbing
#print axioms PDChecker.initial_lift_erases
#print axioms PDChecker.initial_lift_common_label
#print axioms PDChecker.lift_cardinality_bound
#print axioms PDChecker.honest_running_step
#print axioms PDChecker.honest_branch_receipt
#print axioms PDChecker.honest_receipt_law
#print axioms PDChecker.Controls.known_state_hidden_selection_not_pd
#print axioms PDChecker.Controls.suppressed_branch_receipt_not_pd
#check PDChecker.kernel_posterior_deterministic
#check PDChecker.lifted_kernel_posterior_deterministic
#check PDChecker.lifted_joint_row_exact
#check PDChecker.honest_receipt_law

end
end PDChecker.Controls
