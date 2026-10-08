import Mathlib.Algebra.Order.Field.Defs
import Mathlib.Data.Fintype.BigOperators
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.FinCases

/-!
Exact finite application controls. The information principle is inherited from
H-ICS and T9; finite TV/data-processing are established statistical principles.
No upstream OpenAI math implementation is imported. Probability scalars range
over any linearly ordered field, so decisions are not restricted to rationals.
-/
namespace TraceControls
open scoped BigOperators

abbrev Trace := Fin 7
abbrev Word := Bool × Bool
abbrev Mask := Bool × Bool
-- Complete trace encoding: 0=[], 1=[0], 2=[1], 3=[0,0], 4=[0,1],
-- 5=[1,0], 6=[1,1].
def empty : Trace := 0
def zero : Trace := 1
def one : Trace := 2
def word00 : Word := (false, false)
def word01 : Word := (false, true)

def emit (w : Word) (a : Mask) : Trace :=
  if a.1 then
    if a.2 then
      if w.1 then (if w.2 then 6 else 5) else (if w.2 then 4 else 3)
    else if w.1 then 2 else 1
  else if a.2 then (if w.2 then 2 else 1) else 0

variable {K : Type*} [Field K] [LinearOrder K] [IsStrictOrderedRing K]

def retention : K := 1 / 4

def maskWeight (a : Mask) : K :=
  (if a.1 then retention else 1 - retention) *
  (if a.2 then retention else 1 - retention)

def mass (w : Word) (t : Trace) : K :=
  ∑ a : Mask, if (emit w a).val = t.val then maskWeight a else 0

theorem mask_sum : (∑ a : Mask, (maskWeight a : K)) = 1 := by
  norm_num [maskWeight, retention, Fintype.sum_prod_type, Fintype.sum_bool, Fin.coe_ofNat_eq_mod]

theorem trace_total (w : Word) : (∑ t : Trace, (mass w t : K)) = 1 := by
  classical
  unfold mass
  rw [Finset.sum_comm]
  simp only [← Fin.ext_iff]
  simpa using (mask_sum (K := K))

theorem mass_nonneg (w : Word) (t : Trace) : (0 : K) ≤ mass w t := by
  apply Finset.sum_nonneg
  intro a _
  split_ifs
  · rcases a with ⟨a,b⟩
    cases a <;> cases b <;> norm_num [maskWeight, retention]
  · exact le_rfl

def law00 (t : Trace) : K :=
  if t.val = 0 then 9/16 else if t.val = 1 then 6/16 else if t.val = 3 then 1/16 else 0

def law01 (t : Trace) : K :=
  if t.val = 0 then 9/16 else if t.val = 1 then 3/16 else
  if t.val = 2 then 3/16 else if t.val = 4 then 1/16 else 0

theorem complete_law00 (t : Trace) : (mass word00 t : K) = law00 t := by
  fin_cases t <;> norm_num [mass, word00, emit, maskWeight, retention,
    law00, (by decide : (3:Trace) ≠ 0), Fintype.sum_prod_type, Fintype.sum_bool, Fin.coe_ofNat_eq_mod]

theorem complete_law01 (t : Trace) : (mass word01 t : K) = law01 t := by
  fin_cases t <;> norm_num [mass, word01, emit, maskWeight, retention,
    law01, (by decide : (4:Trace) ≠ 0), (by decide : (2:Trace) ≠ 0), Fintype.sum_prod_type, Fintype.sum_bool, Fin.coe_ofNat_eq_mod]

def tv (P Q : Trace → K) : K := (1/2) * ∑ t, |P t - Q t|

theorem one_trace_tv : tv (mass word00) (mass word01) = (1/4 : K) := by
  simp only [tv, complete_law00, complete_law01]
  norm_num [Fin.sum_univ_succ, law00, law01, Fin.coe_ofNat_eq_mod, Fin.succ]
  rw [abs_of_nonneg (by norm_num : (0:K) ≤ 3/16), abs_of_nonneg (by norm_num : (0:K) ≤ 1/16)]
  norm_num

def copies (m : ℕ) (t : Trace) : Fin m → Trace := fun _ => t

def copyMass (m : ℕ) (w : Word) (z : Fin m → Trace) : K :=
  ∑ t : Trace, if copies m t = z then mass w t else 0

def copySupport (m : ℕ) : Finset (Fin m → Trace) :=
  Finset.univ.image (copies m)

def copiedTV (m : ℕ) : K :=
  (1/2) * ∑ z ∈ copySupport m,
    |(copyMass m word00 z : K) - copyMass m word01 z|

theorem copies_injective (m : ℕ) (hm : 0 < m) : Function.Injective (copies m) := by
  intro s t h
  exact congrFun h ⟨0, hm⟩

omit [LinearOrder K] [IsStrictOrderedRing K] in
theorem copyMass_at (m : ℕ) (hm : 0 < m) (w : Word) (t : Trace) :
    (copyMass m w (copies m t) : K) = mass w t := by
  classical
  unfold copyMass
  rw [Finset.sum_eq_single t]
  · simp
  · intro b _ hbt
    have hne : copies m b ≠ copies m t := fun h => hbt (copies_injective m hm h)
    simp [hne]
  · simp

theorem duplicate_tv (m : ℕ) (hm : 0 < m) : (copiedTV m : K) = 1/4 := by
  classical
  unfold copiedTV copySupport
  rw [Finset.sum_image]
  · simp_rw [copyMass_at m hm]
    exact one_trace_tv
  · intro a _ b _ h
    exact copies_injective m hm h

theorem copies_zero_const : copies 0 = fun _ _ => empty := by
  funext t i
  exact Fin.elim0 i

theorem copyMass_zero (w : Word) (z : Fin 0 → Trace) : (copyMass 0 w z : K) = 1 := by
  unfold copyMass
  have h : ∀ t, copies 0 t = z := fun _ => Subsingleton.elim _ _
  simp only [h, if_true]
  exact trace_total w

theorem zero_data_tv : (copiedTV 0 : K) = 0 := by
  simp [copiedTV, copyMass_zero]

-- h(t) is the conditional probability of reporting 01, with arbitrary field values.
def success (h : Trace → K) : K :=
  ((∑ t, mass word00 t * (1 - h t)) + (∑ t, mass word01 t * h t)) / 2

theorem success_formula (h : Trace → K) :
    success h = 1/2 + (-3*h 1 + 3*h 2 - h 3 + h 4)/32 := by
  simp only [success, complete_law00, complete_law01]
  norm_num [Fin.sum_univ_succ, law00, law01, Fin.coe_ofNat_eq_mod, Fin.succ]
  change ((9/16 * (1-h 0) + (3/8 * (1-h 1) + 1/16 * (1-h 3))) +
    (9/16 * h 0 + (3/16 * h 1 + (3/16 * h 2 + 1/16 * h 4)))) / 2 = _
  ring

theorem randomized_success_bound (h : Trace → K)
    (hh : ∀ t, 0 ≤ h t ∧ h t ≤ 1) : success h ≤ 5/8 := by
  rw [success_formula]
  have h1 := (hh 1).1
  have h2 := (hh 2).2
  have h3 := (hh 3).1
  have h4 := (hh 4).2
  linarith

-- This expectation samples a single mask then repeats its realised output.
-- It is exactly the operational pushforward experiment, not iid fresh masks.
def duplicateSuccess (m : ℕ) (h : (Fin m → Trace) → K) : K :=
  success (fun t => h (copies m t))

theorem duplicate_randomized_success_bound (m : ℕ) (h : (Fin m → Trace) → K)
    (hh : ∀ z, 0 ≤ h z ∧ h z ≤ 1) : duplicateSuccess m h ≤ 5/8 := by
  exact randomized_success_bound _ (fun t => hh (copies m t))

theorem zero_data_success (h : (Fin 0 → Trace) → K) : duplicateSuccess 0 h = 1/2 := by
  unfold duplicateSuccess
  rw [success_formula]
  simp only [copies_zero_const]
  ring

abbrev World := Bool × Word

def worldMass (w : World) (t : Trace) : K := mass w.2 t

omit [LinearOrder K] [IsStrictOrderedRing K] in
theorem same_content_source_law (source₁ source₂ : Bool) (w : Word) :
    (worldMass (source₁,w) : Trace → K) = worldMass (source₂,w) := rfl

omit [LinearOrder K] [IsStrictOrderedRing K] in
theorem distinct_sources_same_law :
    (false : Bool) ≠ true ∧
    (worldMass (false,word00) : Trace → K) = worldMass (true,word00) := by
  exact ⟨Bool.false_ne_true, rfl⟩

def conditionalMaskMass (a : Mask) : K :=
  if (emit word00 a).val = zero.val then maskWeight a / mass word00 zero else 0

theorem known_word_mask_ambiguity :
    (true,false) ≠ (false,true) ∧
    emit word00 (true,false) = zero ∧
    emit word00 (false,true) = zero ∧
    (conditionalMaskMass (true,false) : K) = 1/2 ∧
    (conditionalMaskMass (false,true) : K) = 1/2 := by
  norm_num [conditionalMaskMass, mass, emit, word00, zero,
    maskWeight, retention, Fintype.sum_prod_type, Fintype.sum_bool, Fin.coe_ofNat_eq_mod]

end TraceControls
