import Calibration
import HitTransform

/-!
# Exact calibrated histogram identification

The three rational panels are defined directly from five nonnegative finite-set
histograms and the calibrated factors 1/2, 2/3, and 5/6.  The main theorem proves
injectivity for every finite effect type, without a bound on the multiplicities.

The interpretation of these expressions as observable absence probabilities is
external: no stochastic independence or physical actuator is asserted here.
-/

namespace CalibratedIdentification

variable {E : Type*} [Fintype E] [DecidableEq E]

/-- The five support/guard classes, normalized to exclude empty output bundles. -/
structure Histogram (E : Type*) [DecidableEq E] where
  a : Finset E → ℕ
  b : Finset E → ℕ
  c : Finset E → ℕ
  d : Finset E → ℕ
  e : Finset E → ℕ
  a_empty : a ∅ = 0
  b_empty : b ∅ = 0
  c_empty : c ∅ = 0
  d_empty : d ∅ = 0
  e_empty : e ∅ = 0

/-- Issued A: the A-only and A-with-absence-of-B classes are enabled. -/
def panelA (H : Histogram E) (U : Finset E) : ℚ :=
  (1 / 2 : ℚ) ^ (hit H.a U + hit H.d U)

/-- Issued B: the B-only and B-with-absence-of-A classes are enabled. -/
def panelB (H : Histogram E) (U : Finset E) : ℚ :=
  (2 / 3 : ℚ) ^ (hit H.b U + hit H.e U)

/-- Issued AB: only the three unguarded classes are enabled. -/
def panelAB (H : Histogram E) (U : Finset E) : ℚ :=
  jointCode (hit H.a U) (hit H.b U) (hit H.c U)

/-- Exactly the equality of the three specified rational observation families. -/
def SamePanels (H K : Histogram E) : Prop :=
  ∀ U : Finset E, U.Nonempty →
    panelAB H U = panelAB K U ∧ panelA H U = panelA K U ∧ panelB H U = panelB K U

/-- The rational prime code identifies all five hit counts at every queried set. -/
theorem samePanels_hit_eq (H K : Histogram E) (h : SamePanels H K)
    (U : Finset E) (hU : U.Nonempty) :
    hit H.a U = hit K.a U ∧ hit H.b U = hit K.b U ∧
    hit H.c U = hit K.c U ∧ hit H.d U = hit K.d U ∧ hit H.e U = hit K.e U := by
  obtain ⟨hAB, hA, hB⟩ := h U hU
  exact calibrated_five_counts_injective hAB hA hB

/-- Main identification theorem: three exact calibrated panels determine the
entire anonymous histogram on an arbitrary finite effect type. -/
theorem calibrated_panels_identify (H K : Histogram E) (h : SamePanels H K) : H = K := by
  have ha : H.a = K.a := hit_injective_of_empty_zero H.a_empty K.a_empty
    (fun U hU => (samePanels_hit_eq H K h U hU).1)
  have hb : H.b = K.b := hit_injective_of_empty_zero H.b_empty K.b_empty
    (fun U hU => (samePanels_hit_eq H K h U hU).2.1)
  have hc : H.c = K.c := hit_injective_of_empty_zero H.c_empty K.c_empty
    (fun U hU => (samePanels_hit_eq H K h U hU).2.2.1)
  have hd : H.d = K.d := hit_injective_of_empty_zero H.d_empty K.d_empty
    (fun U hU => (samePanels_hit_eq H K h U hU).2.2.2.1)
  have he : H.e = K.e := hit_injective_of_empty_zero H.e_empty K.e_empty
    (fun U hU => (samePanels_hit_eq H K h U hU).2.2.2.2)
  cases H
  cases K
  cases ha
  cases hb
  cases hc
  cases hd
  cases he
  rfl

/-- Explicit coefficientwise form, including every effect bundle. -/
theorem calibrated_panels_identify_coefficients (H K : Histogram E) (h : SamePanels H K)
    (T : Finset E) :
    H.a T = K.a T ∧ H.b T = K.b T ∧ H.c T = K.c T ∧
    H.d T = K.d T ∧ H.e T = K.e T := by
  rw [calibrated_panels_identify H K h]
  exact ⟨rfl, rfl, rfl, rfl, rfl⟩

end CalibratedIdentification
