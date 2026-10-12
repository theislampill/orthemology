import MeasurablePhysicalFlattening
open Filter MeasureTheory
open Orthemology.Tranche2.PhysicalFlattening
namespace IndependentDecoder

theorem empty_decode (d t : ℕ) : decode d (fun _ => []) t = d := by
  have hh : ∀ N, prefixActions (fun _ : ℕ => ([] : List ℕ)) N = [] := by
    intro N
    induction N with
    | zero => rfl
    | succ N ih => rw [prefixActions_succ,ih]; rfl
  unfold decode
  rw [hh]
  rfl

theorem finite_prefix_values : prefixActions (fun n => if n=0 then [0,1] else if n=1 then [] else [2]) 3 = [0,1,2] := by decide

theorem nonempty_default_independent (d e : A) (blocks : ℕ → List A)
    (hn : ∀ n, blocks n ≠ []) (t : ℕ) : decode d blocks t = decode e blocks t := by
  rw [decode_eq_flatten d blocks hn t,decode_eq_flatten e blocks hn t]

def sparse (n : ℕ) : List ℕ := if n%2=0 then [n/2] else []
lemma sparse_prefix (k : ℕ) : prefixLength sparse (2*k) = k := by
  induction k with
  | zero => simp
  | succ k ih =>
    rw [show 2*(k+1) = 2*k+1+1 by omega,prefixLength_succ,prefixLength_succ,ih]
    simp [sparse,Nat.add_mod,Nat.mul_mod]
lemma sparse_unbounded : Unbounded sparse := by
  intro t
  refine ⟨2*t+1,?_⟩
  rw [show 2*t+1+1 = 2*(t+1) by omega,sparse_prefix]
  omega
lemma sparse_fallback : decode 99 sparse 1 = 99 := by decide
lemma sparse_actual_value : flatten sparse sparse_unbounded 1 = 1 := by
  have h := prefix_getD_eq_flatten sparse sparse_unbounded 99 3 1 (by decide)
  have hv : (prefixActions sparse 3).getD 1 99 = 1 := by decide
  rw [hv] at h
  exact h.symm
lemma unbounded_does_not_suffice_for_decoder_identity : decode 99 sparse 1 ≠ flatten sparse sparse_unbounded 1 := by
  rw [sparse_fallback,sparse_actual_value]
  decide

section MeasurableMixed
local instance : MeasurableSpace (List ℕ) := ⊤
local instance : MeasurableSingletonClass (List ℕ) := ⟨fun _ => trivial⟩
def mixed (n ω : ℕ) : List ℕ := if ω=0 then [] else [n]
theorem mixed_decode_measurable (d t : ℕ) :
    Measurable (fun ω => decode d (fun n => mixed n ω) t) :=
  decode_measurable d mixed (fun _ => measurable_of_countable _) t
lemma mixed_invalid_fallback : decode 99 (fun n => mixed n 0) 1 = 99 := by decide
lemma mixed_valid_action : decode 99 (fun n => mixed n 1) 1 = 1 := by decide
end MeasurableMixed

end IndependentDecoder
#print axioms IndependentDecoder.empty_decode
#print axioms IndependentDecoder.finite_prefix_values
#print axioms IndependentDecoder.nonempty_default_independent
#print axioms IndependentDecoder.sparse_unbounded
#print axioms IndependentDecoder.sparse_fallback
#print axioms IndependentDecoder.sparse_actual_value
#print axioms IndependentDecoder.unbounded_does_not_suffice_for_decoder_identity
#print axioms IndependentDecoder.mixed_decode_measurable
#print axioms IndependentDecoder.mixed_invalid_fallback
#print axioms IndependentDecoder.mixed_valid_action
