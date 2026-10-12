import Schur

open Matrix
namespace FullFunctionalRecurrence
open FullFunctionalSchur

def Index : ℕ → Type
  | 0 => Fin 4
  | n+1 => Index n ⊕ Unit

instance indexFintype : (n : ℕ) → Fintype (Index n)
  | 0 => inferInstanceAs (Fintype (Fin 4))
  | n+1 => @instFintypeSum (Index n) Unit (indexFintype n) inferInstance

instance indexDecidableEq : (n : ℕ) → DecidableEq (Index n)
  | 0 => inferInstanceAs (DecidableEq (Fin 4))
  | n+1 => @Sum.instDecidableEq (Index n) Unit (indexDecidableEq n) inferInstance

def position : {n : ℕ} → Index n → ℕ
  | 0, i => i.val
  | _+1, Sum.inl i => position i
  | n+1, Sum.inr _ => n+4

theorem position_lt : ∀ {n : ℕ} (i : Index n), position i < n+4
  | 0, i => i.isLt
  | n+1, Sum.inl i => by simpa only [position] using Nat.lt.step (position_lt i)
  | n+1, Sum.inr _ => by simp [position]

theorem position_injective : ∀ n, Function.Injective (@position n)
  | 0 => fun _ _ h => Fin.ext h
  | n+1 => by
    intro i j h
    cases i with
    | inl i => cases j with
      | inl j => exact congrArg Sum.inl (position_injective n h)
      | inr j => have hi := position_lt i; simp only [position] at h; omega
    | inr i => cases j with
      | inl j => have hj := position_lt j; simp only [position] at h; omega
      | inr j => cases i; cases j; rfl

theorem position_surjective : ∀ n k, k < n+4 → ∃ i : Index n, position i = k
  | 0, k, h => ⟨⟨k,h⟩,rfl⟩
  | n+1, k, h => by
    by_cases hk : k < n+4
    · obtain ⟨i,hi⟩ := position_surjective n k hk
      exact ⟨Sum.inl i,hi⟩
    · have he : k = n+4 := by omega
      exact ⟨Sum.inr (),he.symm⟩

noncomputable def initialA : Matrix (Index 0) (Index 0) ℝ :=
  diagonal (fun i : Fin 4 => if i.val = 3 then 4 else 1)
noncomputable def initialB : Matrix (Index 0) (Index 0) ℝ :=
  diagonal (fun i : Fin 4 => if i.val = 3 then 1/4 else 1)

theorem initialA_symmetric : initialAᵀ = initialA := by simp [initialA]
theorem initialB_symmetric : initialBᵀ = initialB := by simp [initialB]

theorem initial_inverse : initialA * initialB = 1 := by
  rw [initialA, initialB, diagonal_mul_diagonal]
  convert (diagonal_one : (diagonal (fun _ : Fin 4 => (1 : ℝ))) = 1) using 1
  ext i j
  congr 2
  funext k
  split_ifs <;> norm_num

theorem initial_positive : Positive initialA := by
  intro u hu
  classical
  have hn : ∃ i, u i ≠ 0 := by
    by_contra h
    push_neg at h
    exact hu (funext h)
  obtain ⟨i,hi⟩ := hn
  change 0 < ∑ j, u j * (initialA *ᵥ u) j
  apply Finset.sum_pos'
  · intro j hj
    simp only [initialA, mulVec_diagonal]
    split_ifs <;> nlinarith [sq_nonneg (u j)]
  · refine ⟨i, Finset.mem_univ i, ?_⟩
    simp only [initialA, mulVec_diagonal]
    split_ifs <;> nlinarith [sq_pos_of_ne_zero hi]

structure Data (n : ℕ) where
  A : Matrix (Index n) (Index n) ℝ
  B : Matrix (Index n) (Index n) ℝ

noncomputable def initial : Data 0 := ⟨initialA,initialB⟩

noncomputable def extend {n : ℕ} (s : Data n) (v : Index n → ℝ) : Data (n+1) :=
  ⟨extendA s.A v (1 + v ⬝ᵥ s.B *ᵥ v), extendB s.B (s.B *ᵥ v)⟩

def Invariant {n : ℕ} (s : Data n) : Prop :=
  s.Aᵀ = s.A ∧ s.Bᵀ = s.B ∧ s.A * s.B = 1 ∧ Positive s.A

theorem initial_invariant : Invariant initial :=
  ⟨initialA_symmetric,initialB_symmetric,initial_inverse,initial_positive⟩

theorem extend_invariant {n : ℕ} (s : Data n) (hs : Invariant s) (v : Index n → ℝ) :
    Invariant (extend s v) := by
  rcases hs with ⟨hAs,hBs,hAB,hAp⟩
  refine ⟨extendA_symmetric s.A hAs _ _, extendB_symmetric s.B hBs _,
    extend_inverse s.A s.B hBs hAB v, ?_⟩
  apply extend_positive s.A hAs hAp
  rw [mulVec_mulVec,hAB,one_mulVec]

/-- Every sequence of causally selected off-diagonal vectors gives a total
unbounded recursion. No positivity or invertibility assumption is made about it. -/
noncomputable def stages (choose : ∀ n, Data n → Index n → ℝ) : (n : ℕ) → Data n
  | 0 => initial
  | n+1 => extend (stages choose n) (choose n (stages choose n))

theorem stages_invariant (choose : ∀ n, Data n → Index n → ℝ) (n : ℕ) :
    Invariant (stages choose n) := by
  induction n with
  | zero => exact initial_invariant
  | succ n ih => exact extend_invariant _ ih _

theorem stages_positive (choose : ∀ n, Data n → Index n → ℝ) (n : ℕ)
    (u : Index n → ℝ) (hu : u ≠ 0) :
    0 < u ⬝ᵥ (stages choose n).A *ᵥ u :=
  (stages_invariant choose n).2.2.2 u hu

#print axioms stages_invariant
#print axioms stages_positive
end FullFunctionalRecurrence
