import PhysicalFlattening
open Filter
open scoped BigOperators
open Orthemology.Tranche2.PhysicalFlattening
namespace IndependentFlattening

def unitBlocks (n : ℕ) : List ℕ := [n]
lemma unit_nonempty (n : ℕ) : unitBlocks n ≠ [] := by simp [unitBlocks]
lemma unit_prefix (n : ℕ) : prefixLength unitBlocks n = n := by
  simp [prefixLength, unitBlocks]
lemma unit_index (t : ℕ) : blockIndex unitBlocks (unbounded_of_nonempty unitBlocks unit_nonempty) t = t := by
  have hl := blockIndex_lower unitBlocks (unbounded_of_nonempty unitBlocks unit_nonempty) t
  have hu := blockIndex_upper unitBlocks (unbounded_of_nonempty unitBlocks unit_nonempty) t
  rw [unit_prefix] at hl hu
  omega
lemma unit_flatten (t : ℕ) : flatten unitBlocks (unbounded_of_nonempty unitBlocks unit_nonempty) t = t := by
  simp [flatten, unit_index, unitBlocks]

def sparse (n : ℕ) : List Bool := if n % 2 = 0 then [true] else []
lemma sparse_prefix (k : ℕ) : prefixLength sparse (2*k) = k := by
  induction k with
  | zero => simp
  | succ k ih =>
    rw [show 2*(k+1) = 2*k+1+1 by omega, prefixLength_succ, prefixLength_succ, ih]
    simp [sparse, Nat.add_mod, Nat.mul_mod]
lemma sparse_unbounded : Unbounded sparse := by
  intro t
  refine ⟨2*t+1, ?_⟩
  rw [show 2*t+1+1 = 2*(t+1) by omega, sparse_prefix]
  omega
lemma sparse_not_eventually_nonempty : ¬ (∀ᶠ n in atTop, sparse n ≠ []) := by
  intro hh
  obtain ⟨N,hN⟩ := eventually_atTop.mp hh
  have h := hN (2*N+1) (by omega)
  simpa [sparse, Nat.add_mod, Nat.mul_mod] using h
lemma sparse_flatten_true (t : ℕ) : flatten sparse sparse_unbounded t = true := by
  have hm : ∀ n b, b ∈ sparse n → b = true := by
    intro n b hb
    unfold sparse at hb
    split_ifs at hb <;> simp_all
  exact hm _ _ (flatten_mem_block sparse sparse_unbounded t)

def delayed (n : ℕ) : List Bool := if n < 3 then [] else [true]
lemma delayed_eventually_nonempty : ∀ᶠ n in atTop, delayed n ≠ [] := by
  apply eventually_atTop.mpr
  exact ⟨3,fun n hn => by simp [delayed, not_lt.mpr hn]⟩
lemma delayed_unbounded : Unbounded delayed :=
  unbounded_of_eventually_nonempty delayed delayed_eventually_nonempty
lemma delayed_eventually_good : ∀ᶠ t in atTop, flatten delayed delayed_unbounded t = true := by
  apply eventually_flatten_good delayed delayed_unbounded (fun b => b = true)
  apply Filter.Eventually.of_forall
  intro n b hb
  unfold delayed at hb
  split_ifs at hb <;> simp_all

lemma all_empty_not_unbounded : ¬ Unbounded (fun _ : ℕ => ([] : List ℕ)) := by
  intro h
  obtain ⟨n,hn⟩ := h 0
  simpa [prefixLength] using hn
lemma all_empty_vacuously_good : ∀ᶠ n : ℕ in atTop, ∀ a ∈ ([] : List ℕ), False := by
  exact Filter.Eventually.of_forall (fun _ a ha => by simpa using ha)

end IndependentFlattening
#print axioms IndependentFlattening.unit_flatten
#print axioms IndependentFlattening.sparse_prefix
#print axioms IndependentFlattening.sparse_unbounded
#print axioms IndependentFlattening.sparse_not_eventually_nonempty
#print axioms IndependentFlattening.sparse_flatten_true
#print axioms IndependentFlattening.delayed_unbounded
#print axioms IndependentFlattening.delayed_eventually_good
#print axioms IndependentFlattening.all_empty_not_unbounded
#print axioms IndependentFlattening.all_empty_vacuously_good
