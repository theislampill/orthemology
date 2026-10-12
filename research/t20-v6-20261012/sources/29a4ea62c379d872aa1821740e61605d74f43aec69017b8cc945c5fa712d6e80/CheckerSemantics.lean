import CheckerKernel

namespace PDChecker
noncomputable section
open scoped ENNReal

variable {m : ℕ} {Q Γ : Type*} [DecidableEq Γ]

lemma advance_failed_read (M : Machine Q Γ) (i : Fin m) (sigma : Γ) (q : Q)
    (h : Fin m) (a : Action Γ) (b : Bool) (hi : i=h) (hg : sigma≠a.1) :
    advance M (.live i sigma q h) a b=.bottom := by simp [advance,hi,hg]

lemma advance_outside (M : Machine Q Γ) (i : Fin m) (sigma : Γ) (q : Q)
    (h : Fin m) (a : Action Γ) (b : Bool)
    (hout : checkedHead m ((h:ℕ)+(M.step q a.1 b).shift)=none) :
    advance M (.live i sigma q h) a b=.bottom := by simp [advance,hout]

lemma advance_running (M : Machine Q Γ) (i : Fin m) (sigma : Γ) (q : Q)
    (h h' : Fin m) (a : Action Γ) (b : Bool) (q' : Q)
    (hread : i=h → sigma=a.1)
    (hin : checkedHead m ((h:ℕ)+(M.step q a.1 b).shift)=some h')
    (hnext : (M.step q a.1 b).next=.running q') :
    advance M (.live i sigma q h) a b=
      .live i (if i=h then (M.step q a.1 b).write else sigma) q' h' := by
  have hcheck : ¬(i=h ∧ sigma≠a.1) := by tauto
  simp [advance,hcheck,hin,hnext]

lemma advance_accept_inside (M : Machine Q Γ) (i : Fin m) (sigma : Γ) (q : Q)
    (h h' : Fin m) (a : Action Γ) (b : Bool)
    (hread : i=h → sigma=a.1)
    (hin : checkedHead m ((h:ℕ)+(M.step q a.1 b).shift)=some h')
    (hnext : (M.step q a.1 b).next=.accept) :
    advance M (.live i sigma q h) a b=.top := by
  have hcheck : ¬(i=h ∧ sigma≠a.1) := by tauto
  simp [advance,hcheck,hin,hnext]

@[simp] lemma kernel_top (M : Machine Q Γ) (a : Action Γ) :
    kernel (m:=m) M .top a=PMF.pure (.accept,.top) := by
  simp [kernel,isUniversal,branchOutput,advance,emit]

@[simp] lemma kernel_bottom (M : Machine Q Γ) (a : Action Γ) :
    kernel (m:=m) M .bottom a=PMF.pure (.reject,.bottom) := by
  simp [kernel,isUniversal,branchOutput,advance,emit]

lemma kernel_failed_read (M : Machine Q Γ) (i : Fin m) (sigma : Γ) (q : Q)
    (h : Fin m) (a : Action Γ) (hi : i=h) (hg : sigma≠a.1) :
    kernel M (.live i sigma q h) a=PMF.pure (.reject,.bottom) := by
  have hb : branchOutput M (.live i sigma q h) a =
      Function.const Bool (.reject,State.bottom) := by
    funext b
    simp [branchOutput,advance_failed_read M i sigma q h a b hi hg,emit]
  unfold kernel
  rw [hb]
  split
  · exact PMF.map_const _ _
  · rfl

lemma kernel_universal_row [DecidableEq Q] (M : Machine Q Γ) (s : State m Q Γ) (a : Action Γ)
    (hu : isUniversal M s=true) (out : Receipt × State m Q Γ) :
    kernel M s a out =
      (if out=branchOutput M s a false then (2:ℝ≥0∞)⁻¹ else 0) +
      (if out=branchOutput M s a true then (2:ℝ≥0∞)⁻¹ else 0) := by
  classical
  rw [kernel,if_pos hu,PMF.map_apply,tsum_fintype]
  simp [add_comm]

lemma kernel_existential_row [DecidableEq Q] (M : Machine Q Γ) (s : State m Q Γ) (a : Action Γ)
    (hu : isUniversal M s≠true) (out : Receipt × State m Q Γ) :
    kernel M s a out = if out=branchOutput M s a a.2 then 1 else 0 := by
  classical
  rw [kernel,if_neg hu,PMF.pure_apply]
  split_ifs <;> rfl

lemma kernel_entry_values [DecidableEq Q] (M : Machine Q Γ) (s : State m Q Γ)
    (a : Action Γ) (out : Receipt × State m Q Γ) :
    kernel M s a out=0 ∨ kernel M s a out=(2:ℝ≥0∞)⁻¹ ∨ kernel M s a out=1 := by
  classical
  by_cases hu : isUniversal M s=true
  · rw [kernel_universal_row M s a hu out]
    split_ifs <;> simp [ENNReal.inv_two_add_inv_two]
  · rw [kernel_existential_row M s a hu out]
    split_ifs <;> simp

/-- A literal finite-state cardinality calculation, distinct from any complexity theorem. -/
def stateEquiv (m : ℕ) (Q Γ : Type*) : State m Q Γ ≃ (Fin m × Γ × Q × Fin m) ⊕ Bool where
  toFun s := match s with
    | .live i sigma q h => .inl (i,sigma,q,h)
    | .top => .inr true
    | .bottom => .inr false
  invFun x := match x with
    | .inl (i,sigma,q,h) => .live i sigma q h
    | .inr true => .top
    | .inr false => .bottom
  left_inv s := by cases s <;> rfl
  right_inv x := by rcases x with ⟨i,sigma,q,h⟩|b <;> first | rfl | cases b <;> rfl

omit [DecidableEq Γ] in
lemma card_state [Fintype Q] [Fintype Γ] :
    Fintype.card (State m Q Γ)=m^2*Fintype.card Γ*Fintype.card Q+2 := by
  rw [Fintype.card_congr (stateEquiv m Q Γ)]
  simp
  ring

lemma card_receipt : Fintype.card Receipt=5 := by decide

end
end PDChecker
