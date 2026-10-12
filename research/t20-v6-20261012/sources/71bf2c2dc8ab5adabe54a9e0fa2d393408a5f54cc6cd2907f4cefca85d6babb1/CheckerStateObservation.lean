import InitialCheckerBelief

namespace PDChecker
noncomputable section
open scoped ENNReal

inductive LastReceipt
  | ordinary
  | universal (branch : Bool)
  deriving DecidableEq, Fintype

def LastReceipt.observe : LastReceipt → Receipt
  | .ordinary => .ordinary
  | .universal b => .universal b

inductive LiftState (m : ℕ) (Q Γ : Type*)
  | live (index : Fin m) (symbol : Γ) (control : Q) (head : Fin m) (last : LastReceipt)
  | top
  | bottom
  deriving DecidableEq, Fintype

def erase {m : ℕ} {Q Γ : Type*} : LiftState m Q Γ → State m Q Γ
  | .live i sigma q h _ => .live i sigma q h
  | .top => .top
  | .bottom => .bottom

def observe {m : ℕ} {Q Γ : Type*} : LiftState m Q Γ → Receipt
  | .live _ _ _ _ last => last.observe
  | .top => .accept
  | .bottom => .reject

/-- The fallback for an inconsistent nonterminal terminal-label pair is unreachable
under the actual kernel, as proved below. It is not a false observation on a real run. -/
def copyOutcome {m : ℕ} {Q Γ : Type*} (out : Receipt × State m Q Γ) : LiftState m Q Γ :=
  match out.2 with
  | .top => .top
  | .bottom => .bottom
  | .live i sigma q h => .live i sigma q h
    (match out.1 with | .universal b => .universal b | _ => .ordinary)

def ValidOutput {m : ℕ} {Q Γ : Type*} (out : Receipt × State m Q Γ) : Prop :=
  match out.2 with
  | .top => out.1=.accept
  | .bottom => out.1=.reject
  | .live _ _ _ _ => out.1=.ordinary ∨ ∃ b, out.1=.universal b

lemma branchOutput_valid {m : ℕ} {Q Γ : Type*} [DecidableEq Γ]
    (M : Machine Q Γ) (s : State m Q Γ) (a : Action Γ) (b : Bool) :
    ValidOutput (branchOutput M s a b) := by
  cases h : advance M s a b <;> simp [branchOutput,h,emit,ValidOutput]
  split <;> simp_all

lemma kernel_support_valid {m : ℕ} {Q Γ : Type*} [DecidableEq Γ]
    (M : Machine Q Γ) (s : State m Q Γ) (a : Action Γ)
    (out : Receipt × State m Q Γ) (hout : out ∈ (kernel M s a).support) : ValidOutput out := by
  by_cases hu : isUniversal M s=true
  · rw [kernel,if_pos hu] at hout
    obtain ⟨b,hb,hout⟩ := (PMF.mem_support_map_iff _ _ _).mp hout
    rw [← hout]
    exact branchOutput_valid M s a b
  · rw [kernel,if_neg hu] at hout
    rw [(PMF.mem_support_pure_iff _ _).mp hout]
    exact branchOutput_valid M s a a.2

@[simp] lemma erase_copy {m : ℕ} {Q Γ : Type*} (out : Receipt × State m Q Γ) :
    erase (copyOutcome out)=out.2 := by rcases out with ⟨o,s⟩;cases s <;> rfl

lemma observe_copy {m : ℕ} {Q Γ : Type*} (out : Receipt × State m Q Γ)
    (hv : ValidOutput out) : observe (copyOutcome out)=out.1 := by
  rcases out with ⟨o,s⟩
  cases s <;> cases o <;> simp_all [ValidOutput,copyOutcome,observe,LastReceipt.observe]

/-- A normalized transition PMF whose observation is a deterministic label of its next state. -/
def liftedKernel {m : ℕ} {Q Γ : Type*} [DecidableEq Γ] (M : Machine Q Γ)
    (s : LiftState m Q Γ) (a : Action Γ) : PMF (LiftState m Q Γ) :=
  PMF.map copyOutcome (kernel M (erase s) a)

def StateObservationPD {S A O : Type*} (K : S → A → PMF S) (obs : S → O) : Prop :=
  ∀ s a q r, 0 < K s a q → 0 < K s a r → obs q=obs r → q=r

/-- The state-observation lift preserves the required restriction for every actual row. -/
theorem lifted_kernel_posterior_deterministic {m : ℕ} {Q Γ : Type*} [DecidableEq Γ]
    (M : Machine Q Γ) : StateObservationPD (liftedKernel (m:=m) M) observe := by
  intro s a q r hq hr hobs
  have hqs : q ∈ (liftedKernel M s a).support := (PMF.mem_support_iff _ _).mpr (ne_of_gt hq)
  have hrs : r ∈ (liftedKernel M s a).support := (PMF.mem_support_iff _ _).mpr (ne_of_gt hr)
  obtain ⟨x,hx,hxq⟩ := (PMF.mem_support_map_iff _ _ _).mp hqs
  obtain ⟨y,hy,hyr⟩ := (PMF.mem_support_map_iff _ _ _).mp hrs
  have hxy : x.1=y.1 := by
    rw [← observe_copy x (kernel_support_valid M (erase s) a x hx),
      ← observe_copy y (kernel_support_valid M (erase s) a y hy),hxq,hyr]
    exact hobs
  have hxp : 0 < kernel M (erase s) a (x.1,x.2) :=
    pos_iff_ne_zero.mpr ((PMF.mem_support_iff _ _).mp hx)
  have hyp : 0 < kernel M (erase s) a (x.1,y.2) := by
    rw [hxy]
    exact pos_iff_ne_zero.mpr ((PMF.mem_support_iff _ _).mp hy)
  have hstates := kernel_posterior_deterministic M (erase s) a x.1 x.2 y.2 hxp hyp
  have heq : x=y := Prod.ext hxy hstates
  exact hxq.symm.trans ((congrArg copyOutcome heq).trans hyr)

lemma map_congr_on_support {A B : Type*} (p : PMF A) (f g : A → B)
    (h : ∀ a ∈ p.support, f a=g a) : PMF.map f p=PMF.map g p := by
  classical
  ext b
  rw [PMF.map_apply,PMF.map_apply]
  apply tsum_congr
  intro a
  by_cases ha : p a=0
  · simp [ha]
  · rw [h a ((PMF.mem_support_iff _ _).mpr ha)]

/-- Erasing the lifted state while reading its label recovers the original joint row exactly. -/
theorem lifted_joint_row_exact {m : ℕ} {Q Γ : Type*} [DecidableEq Γ]
    (M : Machine Q Γ) (s : LiftState m Q Γ) (a : Action Γ) :
    PMF.map (fun q => (observe q,erase q)) (liftedKernel M s a)=kernel M (erase s) a := by
  rw [liftedKernel,PMF.map_comp]
  have h := map_congr_on_support (kernel M (erase s) a)
    ((fun q => (observe q,erase q)) ∘ copyOutcome) id (by
      intro out hout
      apply Prod.ext
      · exact observe_copy out (kernel_support_valid M (erase s) a out hout)
      · exact erase_copy out)
  exact h.trans (PMF.map_id _)

@[simp] lemma observe_accept_iff {m : ℕ} {Q Γ : Type*} (s : LiftState m Q Γ) :
    observe s=.accept ↔ s=.top := by
  cases s with
  | live i sigma q h last => cases last <;> simp [observe,LastReceipt.observe]
  | top => simp [observe]
  | bottom => simp [observe]

@[simp] lemma lifted_top_absorbing {m : ℕ} {Q Γ : Type*} [DecidableEq Γ]
    (M : Machine Q Γ) (a : Action Γ) : liftedKernel (m:=m) M .top a=PMF.pure .top := by
  simp [liftedKernel,erase,kernel_top,PMF.pure_map,copyOutcome]

def initialLiftAt {m : ℕ} {Q Γ : Type*} (tape : Fin m → Γ) (q0 : Q) (h0 : Fin m) (i : Fin m) :
    LiftState m Q Γ := .live i (tape i) q0 h0 .ordinary

def initialLiftBelief {m : ℕ} {Q Γ : Type*} [Nonempty (Fin m)]
    (tape : Fin m → Γ) (q0 : Q) (h0 : Fin m) : PMF (LiftState m Q Γ) :=
  PMF.map (initialLiftAt tape q0 h0) (PMF.uniformOfFintype (Fin m))

lemma initial_lift_erases {m : ℕ} {Q Γ : Type*} [Nonempty (Fin m)]
    (tape : Fin m → Γ) (q0 : Q) (h0 : Fin m) :
    PMF.map erase (initialLiftBelief tape q0 h0)=initialBelief tape q0 h0 := by
  rw [initialLiftBelief,PMF.map_comp]
  rfl

/-- Every possible checker has the same initial deterministic label; no index is exposed. -/
lemma initial_lift_common_label {m : ℕ} {Q Γ : Type*} [Nonempty (Fin m)]
    (tape : Fin m → Γ) (q0 : Q) (h0 : Fin m) :
    PMF.map observe (initialLiftBelief tape q0 h0)=PMF.pure .ordinary := by
  rw [initialLiftBelief,PMF.map_comp]
  exact PMF.map_const _ _

def liftStateEquiv (m : ℕ) (Q Γ : Type*) :
    LiftState m Q Γ ≃ ((Fin m × Γ × Q × Fin m) × LastReceipt) ⊕ Bool where
  toFun s := match s with
    | .live i sigma q h last => .inl ((i,sigma,q,h),last)
    | .top => .inr true
    | .bottom => .inr false
  invFun x := match x with
    | .inl ((i,sigma,q,h),last) => .live i sigma q h last
    | .inr true => .top
    | .inr false => .bottom
  left_inv s := by cases s <;> rfl
  right_inv x := by rcases x with ⟨⟨i,sigma,q,h⟩,last⟩|b <;> first | rfl | cases b <;> rfl

lemma card_lastReceipt : Fintype.card LastReceipt=3 := by decide

lemma card_liftState {m : ℕ} {Q Γ : Type*} [Fintype Q] [Fintype Γ] :
    Fintype.card (LiftState m Q Γ)=3*(m^2*Fintype.card Γ*Fintype.card Q)+2 := by
  rw [Fintype.card_congr (liftStateEquiv m Q Γ)]
  simp [card_lastReceipt]
  ring

lemma lift_cardinality_bound {m : ℕ} {Q Γ : Type*} [Fintype Q] [Fintype Γ] :
    Fintype.card (LiftState m Q Γ)≤5*Fintype.card (State m Q Γ) := by
  rw [card_liftState,card_state]
  omega

end
end PDChecker
