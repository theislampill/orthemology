import CalibratedPanels
import Mathlib.Algebra.BigOperators.Ring.Finset

namespace RouteProbability

open scoped BigOperators

inductive Kind
  | a | b | c | d | e
  deriving DecidableEq, Repr

instance : Fintype Kind where
  elems := {Kind.a, Kind.b, Kind.c, Kind.d, Kind.e}
  complete := by intro k; cases k <;> simp

lemma univ_kind : (Finset.univ : Finset Kind) = {Kind.a, Kind.b, Kind.c, Kind.d, Kind.e} := rfl

/-- The three nonempty issued-root profiles. -/
inductive Profile
  | A | B | AB
  deriving DecidableEq, Repr

/-- Guards are evaluated on the issued profile, before success is sampled. -/
def enabled : Profile → Kind → Bool
  | .A, .a | .A, .d | .B, .b | .B, .e | .AB, .a | .AB, .b | .AB, .c => true
  | _, _ => false

/-- Support-calibrated independent route-failure probabilities. -/
def failure : Kind → ℚ
  | .a | .d => 1 / 2
  | .b | .e => 2 / 3
  | .c => 5 / 6

lemma failure_nonneg (k : Kind) : 0 ≤ failure k := by cases k <;> norm_num [failure]
lemma failure_le_one (k : Kind) : failure k ≤ 1 := by cases k <;> norm_num [failure]

/-- R indexes actual independent route occurrences; aliases are not new indices. -/
structure Model (R E : Type*) [DecidableEq E] where
  kind : R → Kind
  outputs : R → Finset E
  outputs_nonempty : ∀ r, (outputs r).Nonempty

variable {R E : Type*} [Fintype R] [DecidableEq E]

/-- A successful enabled occurrence emits its entire output bundle at once. -/
def endpoint (M : Model R E) (S : Profile) (ω : R → Bool) : Finset E :=
  Finset.univ.biUnion fun r => if enabled S (M.kind r) ∧ ω r = true then M.outputs r else ∅

/-- Exactly those enabled route occurrences capable of hitting the query. -/
def relevant (M : Model R E) (S : Profile) (U : Finset E) : Finset R :=
  Finset.univ.filter fun r => enabled S (M.kind r) ∧ (M.outputs r ∩ U).Nonempty

/-- The observed endpoint misses U exactly when every relevant route fails. -/
theorem endpoint_absent_iff (M : Model R E) (S : Profile) (U : Finset E) (ω : R → Bool) :
    ¬(endpoint M S ω ∩ U).Nonempty ↔ ∀ r ∈ relevant M S U, ω r = false := by
  constructor
  · intro h r hr
    have hr' := (Finset.mem_filter.mp hr).2
    cases hω : ω r with
    | false => rfl
    | true =>
      exfalso
      apply h
      obtain ⟨x, hx⟩ := hr'.2
      refine ⟨x, Finset.mem_inter.mpr ⟨?_, (Finset.mem_inter.mp hx).2⟩⟩
      apply Finset.mem_biUnion.mpr
      refine ⟨r, Finset.mem_univ r, ?_⟩
      simpa [hr'.1, hω] using (Finset.mem_inter.mp hx).1
  · intro h hn
    obtain ⟨x, hx⟩ := hn
    have hx' := Finset.mem_inter.mp hx
    obtain ⟨r, _, hr⟩ := Finset.mem_biUnion.mp hx'.1
    by_cases he : enabled S (M.kind r) ∧ ω r = true
    · have hrout : x ∈ M.outputs r := by simpa [he] using hr
      have hrel : r ∈ relevant M S U := by
        apply Finset.mem_filter.mpr
        exact ⟨Finset.mem_univ r, he.1, ⟨x, Finset.mem_inter.mpr ⟨hrout, hx'.2⟩⟩⟩
      have hf := h r hrel
      simp [hf] at he
    · simp [he] at hr

end RouteProbability
