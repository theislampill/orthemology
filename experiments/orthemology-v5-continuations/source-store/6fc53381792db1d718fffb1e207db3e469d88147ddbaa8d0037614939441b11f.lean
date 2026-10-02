import Mathlib

/-! UNEXECUTED. Small finite rational law layer and general pivot completion.
The fully permutation-invariant all-proper-marginal theorem is separately a
statement contract, not falsely counted among the proved declarations here. -/
namespace P02A2.FiniteLaw
open scoped BigOperators

structure Law (X : Type*) [Fintype X] where
  weight : X → ℚ
  nonneg : ∀ x, 0 ≤ weight x
  total : ∑ x, weight x = 1

variable {X Y : Type*} [Fintype X] [Fintype Y]

noncomputable def event (p : Law X) (A : X → Prop) : ℚ := by
  classical
  exact ∑ x, if A x then p.weight x else 0

noncomputable def mix (p q : Law X) (a : ℚ) (ha : 0 ≤ a) (ha1 : a ≤ 1) : Law X where
  weight x := (1-a)*p.weight x+a*q.weight x
  nonneg x := add_nonneg (mul_nonneg (by linarith) (p.nonneg x)) (mul_nonneg ha (q.nonneg x))
  total := by rw [Finset.sum_add_distrib, ← Finset.mul_sum, ← Finset.mul_sum, p.total, q.total]; ring

theorem mix_event (p q : Law X) (a : ℚ) (ha : 0 ≤ a) (ha1 : a ≤ 1) (A : X → Prop) :
    event (mix p q a ha ha1) A = (1-a)*event p A+a*event q A := by
  classical
  unfold event
  simp only [mix]
  rw [Finset.mul_sum, Finset.mul_sum, ← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro x hx
  split_ifs <;> ring

noncomputable def push (p : Law X) (f : X → Y) : Law Y := by
  classical
  refine ⟨fun y => ∑ x, if f x=y then p.weight x else 0, ?_, ?_⟩
  · intro y
    apply Finset.sum_nonneg
    intro x hx
    split_ifs
    · exact p.nonneg x
    · exact le_rfl
  · rw [Finset.sum_comm]
    simpa using p.total

theorem push_event (p : Law X) (f : X → Y) (A : Y → Prop) :
    event (push p f) A = event p (fun x => A (f x)) := by
  classical
  unfold event push
  have hswap : (∑ y : Y, if A y then ∑ x : X,
      if f x = y then p.weight x else 0 else 0) =
      ∑ y : Y, ∑ x : X, if A y then (if f x = y then p.weight x else 0) else 0 := by
    apply Finset.sum_congr rfl
    intro y hy
    by_cases h : A y <;> simp [h]
  rw [hswap, Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro x hx
  rw [Finset.sum_eq_single (f x)]
  · simp
  · intro y hy hne
    simp [Ne.symm hne]
  · simp

-- General parity completion: a free word determines its unique pivot bit.
def parity : List Bool → Bool
  | [] => false
  | x::xs => Bool.xor x (parity xs)

def complete (b : Bool) (xs : List Bool) : List Bool := Bool.xor b (parity xs) :: xs

theorem complete_parity (b : Bool) (xs : List Bool) : parity (complete b xs)=b := by
  simp only [complete,parity]
  cases b <;> cases parity xs <;> rfl

theorem complete_length (b : Bool) (xs : List Bool) : (complete b xs).length=xs.length+1 := by
  simp [complete]

theorem complete_injective (b : Bool) : Function.Injective (complete b) := by
  intro x y h
  exact List.cons.inj h |>.2

theorem complete_unique (b a : Bool) (xs : List Bool) (h : parity (a::xs)=b) :
    a::xs=complete b xs := by
  cases a <;> cases hp : parity xs <;> cases b <;> simp_all [parity,complete]

noncomputable def completionEquiv (b : Bool) (n : ℕ) :
    {xs : List Bool // xs.length=n} ≃ {ys : List Bool // ys.length=n+1 ∧ parity ys=b} where
  toFun xs := ⟨complete b xs.val, by rw [complete_length,xs.property]; exact And.intro rfl (complete_parity b xs.val)⟩
  invFun ys := ⟨ys.val.tail, by cases h : ys.val with
    | nil => have hp := ys.property.1; simp [h] at hp
    | cons a xs => simpa [h] using ys.property.1⟩
  left_inv xs := by apply Subtype.ext; rfl
  right_inv ys := by
    apply Subtype.ext
    cases h : ys.val with
    | nil => have hp := ys.property.1; simp [h] at hp
    | cons a xs =>
      have hp : parity (a::xs)=b := by simpa [h] using ys.property.2
      simpa [h] using (complete_unique b a xs hp).symm

-- Exact all-n targets: these are definitions of propositions, NOT theorem proofs.
def cubeParity {n : ℕ} (x : Fin n → Bool) : Bool := parity (List.ofFn x)
noncomputable def parityWeight (n : ℕ) (b : Bool) (x : Fin n → Bool) : ℚ :=
  if cubeParity x=b then (2:ℚ)/(2:ℚ)^n else 0

noncomputable def properMarginalTarget : Prop :=
  ∀ n : ℕ, 1≤n → ∀ J : Finset (Fin n), J ≠ Finset.univ →
    ∀ u : Fin n → Bool, ∀ b : Bool,
      (∑ x : Fin n → Bool, if ∀ j∈J, x j=u j then parityWeight n b x else 0)
        = (1:ℚ)/(2:ℚ)^J.card
end P02A2.FiniteLaw
