import Mathlib

/-! Least surviving candidates for the exact Σ2 normal form ∃s ∀t R s t.
The search at stage n tests s,t ≤ n and returns n+1 when no candidate passes.
The first predecessor convention is zero, matching compile_sigma2. -/
namespace P02A2.SurvivorCandidates

variable (R : ℕ → ℕ → Prop) [DecidableRel R]

def passes (s n : ℕ) : Prop := ∀ t ∈ Finset.range (n+1), R s t

instance passes_decidable (s n : ℕ) : Decidable (passes R s n) := by
  unfold passes
  infer_instance

def available (n s : ℕ) : Prop := (s ≤ n ∧ passes R s n) ∨ s = n+1

instance available_decidable (n s : ℕ) : Decidable (available R n s) := by
  unfold available passes
  infer_instance

def candidate (n : ℕ) : ℕ := Nat.find (show ∃ s, available R n s from ⟨n+1, Or.inr rfl⟩)

theorem candidate_spec (n : ℕ) : available R n (candidate R n) := Nat.find_spec _

theorem candidate_le_default (n : ℕ) : candidate R n ≤ n+1 :=
  Nat.find_min' _ (Or.inr rfl)

theorem candidate_le_passing {n s : ℕ} (hs : s ≤ n) (hp : passes R s n) :
    candidate R n ≤ s := Nat.find_min' _ (Or.inl ⟨hs,hp⟩)

theorem candidate_passes {n : ℕ} (h : candidate R n ≤ n) :
    passes R (candidate R n) n := by
  rcases candidate_spec R n with hs | hs
  · exact hs.2
  · omega

theorem passes_mono {s n m : ℕ} (h : n ≤ m) (hp : passes R s m) : passes R s n := by
  intro t ht
  exact hp t (Finset.mem_range.mpr (by have := Finset.mem_range.mp ht; omega))

theorem candidate_step (n : ℕ) : candidate R n ≤ candidate R (n+1) := by
  by_cases h : candidate R (n+1) ≤ n
  · apply candidate_le_passing R h
    exact passes_mono R (Nat.le_succ n) (candidate_passes R (by omega))
  · have hd := candidate_le_default R n
    omega

theorem candidate_monotone : Monotone (candidate R) := monotone_nat_of_le_succ (candidate_step R)

theorem candidate_bounded_by_witness {s : ℕ} (hs : ∀ t, R s t) :
    ∀ n, candidate R n ≤ s := by
  intro n
  by_cases hsn : s ≤ n
  · exact candidate_le_passing R hsn (fun t _ => hs t)
  · have hd := candidate_le_default R n
    omega

theorem monotone_nat_bounded_eventually_constant (f : ℕ → ℕ) (hf : Monotone f)
    (B : ℕ) (hB : ∀ n, f n ≤ B) : ∃ N, ∀ n, N ≤ n → f n = f N := by
  induction B with
  | zero => exact ⟨0, fun n _ => by have h0 := hB 0; have hn := hB n; omega⟩
  | succ B ih =>
      by_cases he : ∃ N, f N = B+1
      · rcases he with ⟨N,hN⟩
        refine ⟨N, fun n hn => ?_⟩
        have hm := hf hn
        have hb := hB n
        omega
      · apply ih
        intro n
        have hb := hB n
        have hn : f n ≠ B+1 := fun h => he ⟨n,h⟩
        omega

theorem witness_implies_stabilization (h : ∃ s, ∀ t, R s t) :
    ∃ N, ∀ n, N ≤ n → candidate R n = candidate R N := by
  rcases h with ⟨s,hs⟩
  exact monotone_nat_bounded_eventually_constant (candidate R) (candidate_monotone R) s
    (candidate_bounded_by_witness R hs)

theorem stabilization_implies_witness
    (h : ∃ N, ∀ n, N ≤ n → candidate R n = candidate R N) : ∃ s, ∀ t, R s t := by
  rcases h with ⟨N,hN⟩
  refine ⟨candidate R N, fun t => ?_⟩
  let n := max N (max t (candidate R N))
  have hNn : N ≤ n := by dsimp [n]; omega
  have htn : t ≤ n := by dsimp [n]; omega
  have hcn : candidate R N ≤ n := by dsimp [n]; omega
  have he := hN n hNn
  have hp := candidate_passes R (n := n) (by omega)
  rw [he] at hp
  exact hp t (Finset.mem_range.mpr (by omega))

def previous (n : ℕ) : ℕ := if n = 0 then 0 else candidate R (n-1)
def innovation (n : ℕ) : Bool := decide (candidate R n ≠ previous R n)

theorem innovation_successor (n : ℕ) :
    innovation R (n+1) = decide (candidate R (n+1) ≠ candidate R n) := by
  simp [innovation, previous]

theorem stabilization_implies_eventually_no_innovation
    (h : ∃ N, ∀ n, N ≤ n → candidate R n = candidate R N) :
    ∃ N, ∀ n, N ≤ n → innovation R n = false := by
  rcases h with ⟨N,hN⟩
  refine ⟨N+1, fun n hn => ?_⟩
  have h0 : n ≠ 0 := by omega
  have hprev := hN (n-1) (by omega)
  have hnow := hN n (by omega)
  simp [innovation, previous, h0, hprev, hnow]

theorem eventually_no_innovation_implies_stabilization
    (h : ∃ N, ∀ n, N ≤ n → innovation R n = false) :
    ∃ N, ∀ n, N ≤ n → candidate R n = candidate R N := by
  rcases h with ⟨N,hN⟩
  refine ⟨N, fun n hn => ?_⟩
  induction n, hn using Nat.le_induction with
  | base => rfl
  | succ n hn ih =>
      have he := hN (n+1) (by omega)
      rw [innovation_successor] at he
      have hsame : candidate R (n+1) = candidate R n := by simpa using he
      exact hsame.trans ih

theorem witness_iff_eventually_no_innovation :
    (∃ s, ∀ t, R s t) ↔ ∃ N, ∀ n, N ≤ n → innovation R n = false := by
  constructor
  · exact fun h => stabilization_implies_eventually_no_innovation R (witness_implies_stabilization R h)
  · exact fun h => stabilization_implies_witness R (eventually_no_innovation_implies_stabilization R h)

end P02A2.SurvivorCandidates
