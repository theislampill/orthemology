import Mathlib

open Filter
open scoped BigOperators

namespace Orthemology.Tranche2.PhysicalFlattening

variable {A : Type*}

def prefixLength (blocks : ℕ → List A) (n : ℕ) : ℕ :=
  ∑ k ∈ Finset.range n, (blocks k).length

@[simp] lemma prefixLength_zero (blocks : ℕ → List A) : prefixLength blocks 0 = 0 := by
  simp [prefixLength]

@[simp] lemma prefixLength_succ (blocks : ℕ → List A) (n : ℕ) :
    prefixLength blocks (n+1) = prefixLength blocks n + (blocks n).length := by
  simp [prefixLength,Finset.sum_range_succ]

lemma prefixLength_mono (blocks : ℕ → List A) : Monotone (prefixLength blocks) := by
  apply monotone_nat_of_le_succ
  intro n
  simp

def Unbounded (blocks : ℕ → List A) : Prop :=
  ∀ t, ∃ n, t < prefixLength blocks (n+1)

noncomputable def blockIndex (blocks : ℕ → List A) (hu : Unbounded blocks) (t : ℕ) : ℕ :=
  Nat.find (hu t)

lemma blockIndex_upper (blocks : ℕ → List A) (hu : Unbounded blocks) (t : ℕ) :
    t < prefixLength blocks (blockIndex blocks hu t + 1) :=
  Nat.find_spec (hu t)

lemma blockIndex_lower (blocks : ℕ → List A) (hu : Unbounded blocks) (t : ℕ) :
    prefixLength blocks (blockIndex blocks hu t) ≤ t := by
  by_cases h : blockIndex blocks hu t = 0
  · simp [h]
  · have hn : blockIndex blocks hu t - 1 < blockIndex blocks hu t := by omega
    have hnot := Nat.find_min (hu t) hn
    have heq : blockIndex blocks hu t - 1 + 1 = blockIndex blocks hu t := by omega
    rw [heq] at hnot
    exact le_of_not_gt hnot

lemma offset_lt_length (blocks : ℕ → List A) (hu : Unbounded blocks) (t : ℕ) :
    t - prefixLength blocks (blockIndex blocks hu t) <
      (blocks (blockIndex blocks hu t)).length := by
  have h := blockIndex_upper blocks hu t
  rw [prefixLength_succ] at h
  have hl := blockIndex_lower blocks hu t
  omega

/-- Concatenate the actual finite execution blocks, not their unexecuted plans. -/
noncomputable def flatten (blocks : ℕ → List A) (hu : Unbounded blocks) (t : ℕ) : A :=
  (blocks (blockIndex blocks hu t)).get
    ⟨t-prefixLength blocks (blockIndex blocks hu t),offset_lt_length blocks hu t⟩

lemma flatten_mem_block (blocks : ℕ → List A) (hu : Unbounded blocks) (t : ℕ) :
    flatten blocks hu t ∈ blocks (blockIndex blocks hu t) :=
  List.get_mem _ _

lemma late_index (blocks : ℕ → List A) (hu : Unbounded blocks) (N t : ℕ)
    (ht : prefixLength blocks N ≤ t) : N ≤ blockIndex blocks hu t := by
  by_contra h
  have hn : blockIndex blocks hu t+1 ≤ N := by omega
  have hm := prefixLength_mono blocks hn
  have hupp := blockIndex_upper blocks hu t
  omega

/-- A literal action-time cutoff is the cumulative length of the finite prefix
of possibly bad executed blocks. No bound on their individual lengths is needed. -/
theorem eventually_flatten_good (blocks : ℕ → List A) (hu : Unbounded blocks)
    (Good : A → Prop)
    (hgood : ∀ᶠ n in atTop, ∀ a ∈ blocks n, Good a) :
    ∀ᶠ t in atTop, Good (flatten blocks hu t) := by
  obtain ⟨N,hN⟩ := eventually_atTop.mp hgood
  apply eventually_atTop.mpr
  refine ⟨prefixLength blocks N,fun t ht => ?_⟩
  exact hN _ (late_index blocks hu N t ht) _ (flatten_mem_block blocks hu t)

lemma index_le_prefixLength (blocks : ℕ → List A) (hne : ∀ n, blocks n ≠ []) (n : ℕ) :
    n ≤ prefixLength blocks n := by
  induction n with
  | zero => simp
  | succ n ih =>
    have hl : 0 < (blocks n).length := List.length_pos_iff.mpr (hne n)
    rw [prefixLength_succ]
    omega

/-- Nonempty executed blocks ensure infinitely many actual action steps. -/
theorem unbounded_of_nonempty (blocks : ℕ → List A) (hne : ∀ n, blocks n ≠ []) :
    Unbounded blocks := by
  intro t
  exact ⟨t,lt_of_lt_of_le (Nat.lt_succ_self t) (index_le_prefixLength blocks hne (t+1))⟩

/-- With nonempty blocks, physical action t occurs within the first t+1 blocks. -/
theorem blockIndex_le_time (blocks : ℕ → List A) (hne : ∀ n, blocks n ≠ []) (t : ℕ) :
    blockIndex blocks (unbounded_of_nonempty blocks hne) t ≤ t := by
  exact (index_le_prefixLength blocks hne _).trans
    (blockIndex_lower blocks (unbounded_of_nonempty blocks hne) t)

end Orthemology.Tranche2.PhysicalFlattening

#print axioms Orthemology.Tranche2.PhysicalFlattening.eventually_flatten_good
#print axioms Orthemology.Tranche2.PhysicalFlattening.unbounded_of_nonempty
#print axioms Orthemology.Tranche2.PhysicalFlattening.blockIndex_le_time

namespace Orthemology.Tranche2.PhysicalFlattening
variable {A : Type*}

lemma tail_prefix_lower (blocks : ℕ → List A) (N : ℕ)
    (hne : ∀ n ≥ N, blocks n ≠ []) (k : ℕ) :
    k ≤ prefixLength blocks (N+k) := by
  induction k with
  | zero => simp
  | succ k ih =>
    have hl : 0 < (blocks (N+k)).length :=
      List.length_pos_iff.mpr (hne (N+k) (Nat.le_add_right N k))
    change k+1 ≤ prefixLength blocks (N+(k+1))
    rw [← Nat.add_assoc,prefixLength_succ]
    omega

theorem unbounded_of_eventually_nonempty (blocks : ℕ → List A)
    (hne : ∀ᶠ n in atTop, blocks n ≠ []) : Unbounded blocks := by
  obtain ⟨N,hN⟩ := eventually_atTop.mp hne
  intro t
  refine ⟨N+t,?_⟩
  have h := tail_prefix_lower blocks N hN (t+1)
  simpa only [Nat.add_assoc] using lt_of_lt_of_le (Nat.lt_succ_self t) h

lemma prefixLength_congr (blocks other : ℕ → List A) (N : ℕ)
    (h : ∀ k < N, blocks k = other k) :
    prefixLength blocks N = prefixLength other N := by
  apply Finset.sum_congr rfl
  intro k hk
  rw [h k (Finset.mem_range.mp hk)]

/-- The least crossing depends only on the first t+1 nonempty blocks. -/
theorem blockIndex_prefix_local (blocks other : ℕ → List A)
    (hb : ∀ n, blocks n ≠ []) (ho : ∀ n, other n ≠ []) (t : ℕ)
    (heq : ∀ k ≤ t, blocks k = other k) :
    blockIndex blocks (unbounded_of_nonempty blocks hb) t =
      blockIndex other (unbounded_of_nonempty other ho) t := by
  apply le_antisymm
  · apply Nat.find_min'
    have h := blockIndex_upper other (unbounded_of_nonempty other ho) t
    have hi := blockIndex_le_time other ho t
    rw [prefixLength_congr blocks other _ (fun k hk => heq k (by omega))]
    exact h
  · apply Nat.find_min'
    have h := blockIndex_upper blocks (unbounded_of_nonempty blocks hb) t
    have hi := blockIndex_le_time blocks hb t
    rw [prefixLength_congr other blocks _ (fun k hk => (heq k (by omega)).symm)]
    exact h

end Orthemology.Tranche2.PhysicalFlattening

#print axioms Orthemology.Tranche2.PhysicalFlattening.unbounded_of_eventually_nonempty
#print axioms Orthemology.Tranche2.PhysicalFlattening.blockIndex_prefix_local
