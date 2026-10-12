import Recurrence
import Indexing

open Matrix
namespace FullFunctionalMoment
open FullFunctionalSchur FullFunctionalRecurrence FullFunctionalIndexing
noncomputable section

instance compatibleDecidable (p q : Exponent) : Decidable (Compatible p q) :=
  inferInstanceAs (Decidable ((p.1+q.1)%2=0 ∧ (p.2+q.2)%2=0))

/-- A finite-prefix moment assignment, with harmless arbitrary values beyond it. -/
def initialJ (k : ℕ) : ℝ := if k = 4 then 4 else 1

def entry (J : ℕ → ℝ) (p q : Exponent) : ℝ :=
  if Compatible p q then J (index (midpoint p q)) else 0

theorem entry_symmetric (J : ℕ → ℝ) (p q : Exponent) : entry J p q = entry J q p := by
  classical
  unfold entry
  have h : Compatible p q ↔ Compatible q p := ⟨compatible_symm,compatible_symm⟩
  simp only [h,midpoint_comm p q]

@[simp] theorem entry_self (J : ℕ → ℝ) (p : Exponent) : entry J p p = J (index p) := by
  simp [entry]

structure State (n : ℕ) where
  core : Data n
  J : ℕ → ℝ

def first : State 0 := ⟨initial,initialJ⟩

def column {n : ℕ} (s : State n) : Index n → ℝ :=
  fun i => entry s.J (exponentAt (position i)) (exponentAt (n+4))

def nextDiagonal {n : ℕ} (s : State n) : ℝ := 1 + column s ⬝ᵥ s.core.B *ᵥ column s

def next {n : ℕ} (s : State n) : State (n+1) :=
  ⟨extend s.core (column s), fun k => if k = n+5 then nextDiagonal s else s.J k⟩

def state : (n : ℕ) → State n
  | 0 => first
  | n+1 => next (state n)

@[simp] theorem next_J_new {n : ℕ} (s : State n) : (next s).J (n+5) = nextDiagonal s := by
  simp [next]

theorem next_J_old {n : ℕ} (s : State n) (k : ℕ) (hk : k ≤ n+4) :
    (next s).J k = s.J k := by
  simp [next, show k ≠ n+5 by omega]

theorem entry_next_old {n : ℕ} (s : State n) (p q : Exponent)
    (hp : index p ≤ n+4) (hq : index q ≤ n+4) :
    entry (next s).J p q = entry s.J p q := by
  classical
  unfold entry
  split_ifs with h
  · exact next_J_old s _ (le_trans (midpoint_index_le h) (max_le hp hq))
  · rfl

theorem column_precedes {n : ℕ} (i : Index n)
    (h : Compatible (exponentAt (position i)) (exponentAt (n+4))) :
    index (midpoint (exponentAt (position i)) (exponentAt (n+4))) ≤ n+4 := by
  have hi := position_lt i
  have hm := midpoint_precedes_of_index_lt
    (show index (exponentAt (position i)) < index (exponentAt (n+4)) by simp; omega) h
  simp only [index_exponentAt] at hm
  omega

theorem entry_next_column {n : ℕ} (s : State n) (i : Index n) :
    entry (next s).J (exponentAt (position i)) (exponentAt (n+4)) = column s i := by
  classical
  unfold column entry
  split_ifs with h
  · exact next_J_old s _ (column_precedes i h)
  · rfl

def GramInvariant {n : ℕ} (s : State n) : Prop :=
  ∀ i j, s.core.A i j = entry s.J (exponentAt (position i)) (exponentAt (position j))

theorem first_gram : GramInvariant first := by
  classical
  intro i j
  change diagonal (fun i : Fin 4 => if i.val = 3 then (4 : ℝ) else 1) i j =
    entry initialJ (exponentAt i.val) (exponentAt j.val)
  by_cases hij : i = j
  · subst j
    simp only [diagonal_apply_eq,entry_self,index_exponentAt,initialJ]
    have he : (i.val+1=4) ↔ (i.val=3) := by omega
    simp only [he]
  · rw [diagonal_apply_ne _ hij]
    have hp : index (exponentAt i.val) ≤ 4 := by simp; omega
    have hq : index (exponentAt j.val) ≤ 4 := by simp; omega
    have hn : exponentAt i.val ≠ exponentAt j.val := by
      intro he
      exact hij (Fin.ext (exponentAt_injective he))
    simp [entry,seed_parity_separated hp hq hn]

theorem next_gram {n : ℕ} (s : State n) (hs : GramInvariant s) : GramInvariant (next s) := by
  classical
  intro i j
  cases i with
  | inl i => cases j with
    | inl j =>
      change s.core.A i j = entry (next s).J (exponentAt (position i)) (exponentAt (position j))
      rw [hs,entry_next_old]
      · simp only [index_exponentAt]; have hi := position_lt i; omega
      · simp only [index_exponentAt]; have hj := position_lt j; omega
    | inr j =>
      change column s i = entry (next s).J (exponentAt (position i)) (exponentAt (n+4))
      exact (entry_next_column s i).symm
  | inr i => cases j with
    | inl j =>
      change column s j = entry (next s).J (exponentAt (n+4)) (exponentAt (position j))
      rw [entry_symmetric]
      exact (entry_next_column s j).symm
    | inr j =>
      change nextDiagonal s = entry (next s).J (exponentAt (n+4)) (exponentAt (n+4))
      simp only [entry_self,index_exponentAt]
      exact (next_J_new s).symm

theorem state_core_invariant (n : ℕ) : Invariant (state n).core := by
  induction n with
  | zero => exact initial_invariant
  | succ n ih => exact extend_invariant _ ih _

theorem state_gram (n : ℕ) : GramInvariant (state n) := by
  induction n with
  | zero => exact first_gram
  | succ n ih => exact next_gram _ ih

theorem state_J_stable {m n k : ℕ} (hmn : m ≤ n) (hk : k ≤ m+4) :
    (state n).J k = (state m).J k := by
  induction n, hmn using Nat.le_induction with
  | base => rfl
  | succ n hmn ih =>
    change (next (state n)).J k = (state m).J k
    rw [next_J_old _ _ (by omega),ih]

theorem state_J_compatible {m n k : ℕ} (hm : k ≤ m+4) (hn : k ≤ n+4) :
    (state m).J k = (state n).J k := by
  rcases le_total m n with h | h
  · exact (state_J_stable h hm).symm
  · exact state_J_stable h hn

/-- One infinite sequence, defined by a fixed finite stage for each index. -/
def J (k : ℕ) : ℝ := (state k).J k

theorem J_eq_state {n k : ℕ} (hk : k ≤ n+4) : J k = (state n).J k :=
  state_J_compatible (by omega) hk

theorem entry_J_eq_state {n : ℕ} (p q : Exponent)
    (hp : index p ≤ n+4) (hq : index q ≤ n+4) :
    entry J p q = entry (state n).J p q := by
  classical
  unfold entry
  split_ifs with h
  · exact J_eq_state (le_trans (midpoint_index_le h) (max_le hp hq))
  · rfl

def moment (e : Exponent) : ℝ :=
  if e.1 % 2 = 0 ∧ e.2 % 2 = 0 then J (index (e.1/2,e.2/2)) else 0

theorem moment_add (p q : Exponent) : moment (p+q) = entry J p q := by
  rfl

def gram (n : ℕ) : Matrix (Index n) (Index n) ℝ :=
  fun i j => moment (exponentAt (position i) + exponentAt (position j))

theorem gram_eq_state (n : ℕ) : gram n = (state n).core.A := by
  ext i j
  rw [gram,moment_add,entry_J_eq_state,← state_gram]
  · simp only [index_exponentAt]; have hi := position_lt i; omega
  · simp only [index_exponentAt]; have hj := position_lt j; omega

/-- The actual recurrence has positive Gram matrices at every natural size.
No degree bound and no positivity assumption on the moment sequence occur. -/
theorem gram_positive (n : ℕ) : Positive (gram n) := by
  rw [gram_eq_state]
  exact (state_core_invariant n).2.2.2

theorem J_seed (k : ℕ) (hk : k ≤ 4) : J k = initialJ k :=
  J_eq_state (n := 0) hk

@[simp] theorem moment_zero : moment (0,0) = 1 := by
  change J 1 = 1
  rw [J_seed 1 (by omega)]
  norm_num [initialJ]

@[simp] theorem moment_four_two : moment (4,2) = 1 := by
  norm_num [moment,show index (2,1) = 2 from rfl,J_seed 2 (by omega),initialJ]

@[simp] theorem moment_two_four : moment (2,4) = 1 := by
  norm_num [moment,show index (1,2) = 3 from rfl,J_seed 3 (by omega),initialJ]

@[simp] theorem moment_two_two : moment (2,2) = 4 := by
  change J 4 = 4
  rw [J_seed 4 (by omega)]
  norm_num [initialJ]

#print axioms state_gram
#print axioms gram_positive
end
end FullFunctionalMoment
