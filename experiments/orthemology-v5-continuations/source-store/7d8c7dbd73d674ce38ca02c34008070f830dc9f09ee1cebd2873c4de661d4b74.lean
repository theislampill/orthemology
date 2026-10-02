import SubprobHellinger
import BlockKernel

/-!
# A genuinely interruptible observation block

A left outcome exits immediately after the current observation. A right outcome
records a support-preserving observation and continues. No later old-menu action
is executed after an exit. Completed-outcome affinity is computed without
conditioning on completion.
-/

noncomputable section
open scoped BigOperators
open Finset

namespace Orthemology.Tranche2

universe u

/-- n remaining active observation steps; no opaque continuation after exit. -/

def StopObs (Y : Type u) : ℕ → Type u
  | 0 => PUnit
  | n+1 => Y ⊕ (Y × StopObs Y n)

instance stopObsFintype {Y : Type*} [Fintype Y] : (n : ℕ) → Fintype (StopObs Y n)
  | 0 => inferInstanceAs (Fintype PUnit)
  | n+1 => @instFintypeSum Y (Y × StopObs Y n) inferInstance
      (@instFintypeProd Y (StopObs Y n) inferInstance (stopObsFintype n))

def stopCompleted {Y : Type*} : {n : ℕ} → StopObs Y n → Bool
  | 0, _ => true
  | _+1, Sum.inl _ => false
  | _+1, Sum.inr (_,w) => stopCompleted w

def stoppedMass {A Y : Type*} (p : A → Y → ℝ) (stay : A → Y → Bool) :
    (acts : List A) → StopObs Y acts.length → ℝ
  | [], _ => 1
  | a::_as, Sum.inl y => if stay a y then 0 else p a y
  | a::as, Sum.inr (y,w) => if stay a y then p a y * stoppedMass p stay as w else 0

variable {A Y : Type*} [Fintype Y]

omit [Fintype Y] in
lemma stoppedMass_nonneg (p : A → Y → ℝ) (stay : A → Y → Bool)
    (hp : ∀ a y, 0 ≤ p a y) (acts : List A) :
    ∀ w, 0 ≤ stoppedMass p stay acts w := by
  induction acts with
  | nil => intro w; norm_num [stoppedMass]
  | cons a as ih =>
    intro w
    rcases w with y | ⟨y,w⟩
    · simp only [stoppedMass]
      split_ifs <;> first | exact le_rfl | exact hp a y
    · simp only [stoppedMass]
      split_ifs <;> first | exact mul_nonneg (hp a y) (ih w) | exact le_rfl

theorem stoppedMass_normalized (p : A → Y → ℝ) (stay : A → Y → Bool)
    (hNorm : ∀ a, ∑ y, p a y = 1) (acts : List A) :
    ∑ w, stoppedMass p stay acts w = 1 := by
  induction acts with
  | nil => simp [stoppedMass, StopObs]
  | cons a as ih =>
    change (∑ w : Y ⊕ (Y × StopObs Y as.length), stoppedMass p stay (a::as) w) = 1
    rw [Fintype.sum_sum_type, Fintype.sum_prod_type, ← Finset.sum_add_distrib]
    calc
      (∑ y, (stoppedMass p stay (a::as) (Sum.inl y) +
        ∑ w, stoppedMass p stay (a::as) (Sum.inr (y,w)))) = ∑ y, p a y := by
        apply Finset.sum_congr rfl
        intro y _
        cases hs : stay a y <;> simp [stoppedMass, hs, ← Finset.mul_sum, ih]
      _ = 1 := hNorm a

def survivalMass (p : A → Y → ℝ) (stay : A → Y → Bool) (acts : List A) : ℝ :=
  ∑ w, if stopCompleted w then stoppedMass p stay acts w else 0

def survivalAffinity (p q : A → Y → ℝ) (stay : A → Y → Bool) (acts : List A) : ℝ :=
  ∑ w, if stopCompleted w then
    Real.sqrt (stoppedMass p stay acts w) * Real.sqrt (stoppedMass q stay acts w) else 0

def residualActionAffinity (p q : A → Y → ℝ) (stay : A → Y → Bool) (a : A) : ℝ :=
  ∑ y, if stay a y then Real.sqrt (p a y) * Real.sqrt (q a y) else 0

def stayMass (p : A → Y → ℝ) (stay : A → Y → Bool) (a : A) : ℝ :=
  ∑ y, if stay a y then p a y else 0

lemma survivalAffinity_cons (p q : A → Y → ℝ) (stay : A → Y → Bool)
    (hp : ∀ a y, 0 ≤ p a y) (hq : ∀ a y, 0 ≤ q a y) (a : A) (as : List A) :
    survivalAffinity p q stay (a::as) =
      residualActionAffinity p q stay a * survivalAffinity p q stay as := by
  unfold survivalAffinity
  change (∑ w : Y ⊕ (Y × StopObs Y as.length), _) = _
  rw [Fintype.sum_sum_type, Fintype.sum_prod_type]
  simp only [stopCompleted, Bool.false_eq_true, ↓reduceIte, Finset.sum_const_zero, zero_add]
  rw [residualActionAffinity, Finset.sum_mul]
  apply Finset.sum_congr rfl
  intro y _
  cases hs : stay a y
  · simp [stoppedMass, hs]
  · simp only [stoppedMass, hs, ↓reduceIte]
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro w _
    cases hc : stopCompleted w
    · simp [hc]
    · simp only [hc, ↓reduceIte]
      rw [Real.sqrt_mul (hp a y), Real.sqrt_mul (hq a y)]
      ring

theorem survivalAffinity_product (p q : A → Y → ℝ) (stay : A → Y → Bool)
    (hp : ∀ a y, 0 ≤ p a y) (hq : ∀ a y, 0 ≤ q a y) (acts : List A) :
    survivalAffinity p q stay acts = (acts.map (residualActionAffinity p q stay)).prod := by
  induction acts with
  | nil => simp [survivalAffinity, StopObs, stopCompleted, stoppedMass]
  | cons a as ih => rw [survivalAffinity_cons p q stay hp hq, ih]; rfl

lemma survivalMass_cons (p : A → Y → ℝ) (stay : A → Y → Bool) (a : A) (as : List A) :
    survivalMass p stay (a::as) = stayMass p stay a * survivalMass p stay as := by
  unfold survivalMass
  change (∑ w : Y ⊕ (Y × StopObs Y as.length), _) = _
  rw [Fintype.sum_sum_type, Fintype.sum_prod_type]
  simp only [stopCompleted, Bool.false_eq_true, ↓reduceIte, Finset.sum_const_zero, zero_add]
  rw [stayMass, Finset.sum_mul]
  apply Finset.sum_congr rfl
  intro y _
  cases hs : stay a y
  · simp [stoppedMass, hs]
  · simp only [stoppedMass, hs, ↓reduceIte]
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro w _
    cases hc : stopCompleted w <;> simp [hc]

theorem survivalMass_product (p : A → Y → ℝ) (stay : A → Y → Bool) (acts : List A) :
    survivalMass p stay acts = (acts.map (stayMass p stay)).prod := by
  induction acts with
  | nil => simp [survivalMass, StopObs, stopCompleted, stoppedMass]
  | cons a as ih => rw [survivalMass_cons, ih]; rfl

theorem survivalMass_le_one (p : A → Y → ℝ) (stay : A → Y → Bool)
    (hp : ∀ a y, 0 ≤ p a y) (hNorm : ∀ a, ∑ y, p a y = 1) (acts : List A) :
    survivalMass p stay acts ≤ 1 := by
  calc
    _ ≤ ∑ w, stoppedMass p stay acts w := by
      apply Finset.sum_le_sum
      intro w _
      split_ifs <;> first | exact le_rfl | exact stoppedMass_nonneg p stay hp acts w
    _ = 1 := stoppedMass_normalized p stay hNorm acts

lemma survivalAffinity_eq_killed (p q : A → Y → ℝ) (stay : A → Y → Bool) (acts : List A) :
    survivalAffinity p q stay acts =
      affinity (killedLaw (stoppedMass p stay acts) stopCompleted)
        (killedLaw (stoppedMass q stay acts) stopCompleted) := by
  exact (killedLaw_affinity_formula _ _ _).symm

end Orthemology.Tranche2
