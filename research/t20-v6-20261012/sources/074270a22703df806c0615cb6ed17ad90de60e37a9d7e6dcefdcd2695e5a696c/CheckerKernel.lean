import Mathlib

namespace PDChecker
noncomputable section
open scoped ENNReal

inductive Control (Q : Type*)
  | running (q : Q)
  | accept
  | reject
  deriving DecidableEq, Fintype

structure Instruction (Q Γ : Type*) where
  write : Γ
  next : Control Q
  shift : ℤ

structure Machine (Q Γ : Type*) where
  universal : Q → Bool
  step : Q → Γ → Bool → Instruction Q Γ

inductive State (m : ℕ) (Q Γ : Type*)
  | live (index : Fin m) (symbol : Γ) (control : Q) (head : Fin m)
  | top
  | bottom
  deriving DecidableEq, Fintype

inductive Receipt
  | ordinary
  | universal (branch : Bool)
  | accept
  | reject
  deriving DecidableEq, Fintype

abbrev Action (Γ : Type*) := Γ × Bool

/-- Bounds are checked before the destination control, including accepting controls. -/
def checkedHead (m : ℕ) (z : ℤ) : Option (Fin m) :=
  if h : 0 ≤ z ∧ z<(m:ℤ) then some ⟨z.toNat,(Int.toNat_lt h.1).mpr h.2⟩ else none

def isUniversal {m : ℕ} {Q Γ : Type*} (M : Machine Q Γ) : State m Q Γ → Bool
  | .live _ _ q _ => M.universal q
  | .top => false
  | .bottom => false

/-- Actual single-cell validation, checked write, shared control/head update and terminal handling. -/
def advance {m : ℕ} {Q Γ : Type*} [DecidableEq Γ] (M : Machine Q Γ)
    (s : State m Q Γ) (a : Action Γ) (branch : Bool) : State m Q Γ :=
  match s with
  | .top => .top
  | .bottom => .bottom
  | .live i sigma q h =>
    if i=h ∧ sigma≠a.1 then .bottom
    else
      let ins := M.step q a.1 branch
      match checkedHead m ((h:ℕ)+ins.shift) with
      | none => .bottom
      | some h' =>
        match ins.next with
        | .accept => .top
        | .reject => .bottom
        | .running q' => .live i (if i=h then ins.write else sigma) q' h'

/-- Only nonterminal outcomes use the selected public step tag. -/
def emit {m : ℕ} {Q Γ : Type*} (tag : Receipt) (s : State m Q Γ) : Receipt × State m Q Γ :=
  match s with
  | .top => (.accept,.top)
  | .bottom => (.reject,.bottom)
  | .live i sigma q h => (tag,.live i sigma q h)

@[simp] lemma emit_snd {m : ℕ} {Q Γ : Type*} (tag : Receipt) (s : State m Q Γ) :
    (emit tag s).2=s := by cases s <;> rfl

lemma separated_emit {m : ℕ} {Q Γ : Type*} {b c : Bool} (hbc : b≠c)
    (s t : State m Q Γ)
    (h : (emit (.universal b) s).1=(emit (.universal c) t).1) : s=t := by
  cases s <;> cases t <;> simp_all [emit]

def branchOutput {m : ℕ} {Q Γ : Type*} [DecidableEq Γ] (M : Machine Q Γ)
    (s : State m Q Γ) (a : Action Γ) (branch : Bool) : Receipt × State m Q Γ :=
  emit (if isUniversal M s=true then .universal branch else .ordinary) (advance M s a branch)

/-- A normalized exact fair bit, not an abstract distribution premise. -/
def fairBit : PMF Bool := PMF.uniformOfFintype Bool

@[simp] lemma fairBit_apply (b : Bool) : fairBit b=(2:ℝ≥0∞)⁻¹ := by
  simp [fairBit,PMF.uniformOfFintype_apply]

/-- The actual joint receipt/successor kernel: a point mass at existential states,
and the pushforward of one exact fair bit at universal states. -/
def kernel {m : ℕ} {Q Γ : Type*} [DecidableEq Γ] (M : Machine Q Γ)
    (s : State m Q Γ) (a : Action Γ) : PMF (Receipt × State m Q Γ) :=
  if isUniversal M s=true then PMF.map (branchOutput M s a) fairBit
  else PMF.pure (branchOutput M s a a.2)

def PosteriorDeterministic {S A O : Type*} (K : S → A → PMF (O × S)) : Prop :=
  ∀ s a o q r, 0 < K s a (o,q) → 0 < K s a (o,r) → q=r

/-- Posterior determinism is derived from the constructed kernel, with no PD premise. -/
theorem kernel_posterior_deterministic {m : ℕ} {Q Γ : Type*} [DecidableEq Γ]
    (M : Machine Q Γ) : PosteriorDeterministic (kernel (m:=m) M) := by
  intro s a o q r hq hr
  have hqs : (o,q) ∈ (kernel M s a).support := (PMF.mem_support_iff _ _).mpr (ne_of_gt hq)
  have hrs : (o,r) ∈ (kernel M s a).support := (PMF.mem_support_iff _ _).mpr (ne_of_gt hr)
  by_cases hu : isUniversal M s=true
  · rw [kernel,if_pos hu] at hqs hrs
    obtain ⟨b,hb,hbq⟩ := (PMF.mem_support_map_iff _ _ _).mp hqs
    obtain ⟨c,hc,hcr⟩ := (PMF.mem_support_map_iff _ _ _).mp hrs
    by_cases hbc : b=c
    · subst c
      exact congrArg Prod.snd (hbq.symm.trans hcr)
    · have hobs := (congrArg Prod.fst hbq).trans (congrArg Prod.fst hcr).symm
      simp only [branchOutput,if_pos hu] at hobs
      have hs := separated_emit hbc (advance M s a b) (advance M s a c) hobs
      have hqb := congrArg Prod.snd hbq
      have hrc := congrArg Prod.snd hcr
      simp only [branchOutput,emit_snd] at hqb hrc
      exact hqb.symm.trans (hs.trans hrc)
  · rw [kernel,if_neg hu] at hqs hrs
    have hqeq := (PMF.mem_support_pure_iff _ _).mp hqs
    have hreq := (PMF.mem_support_pure_iff _ _).mp hrs
    exact congrArg Prod.snd (hqeq.trans hreq.symm)

end
end PDChecker
