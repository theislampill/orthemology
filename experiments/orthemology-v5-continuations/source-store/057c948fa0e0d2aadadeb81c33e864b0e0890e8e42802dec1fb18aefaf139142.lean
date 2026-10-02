import CoBuchiTargetCost

noncomputable section
open MeasureTheory Filter
open scoped ENNReal
open HiddenParity.Stochastic
open Orthemology.Tranche2.RecurrentSupport
open Orthemology.Tranche2.PolicyEmbedding
namespace HiddenParity.Cost
variable {Pair : Type*}

/-- Count the actual pairs at t=0,1,...; there is no synthetic initial visit. -/
def badCount (bad : Pair → Prop) [DecidablePred bad] (x : ℕ → Pair) : ℝ≥0∞ :=
  ∑' n, if bad (x n) then 1 else 0

theorem badCount_eq_encard (bad : Pair → Prop) [DecidablePred bad] (x : ℕ → Pair) :
    badCount bad x = ({n | bad (x n)} : Set ℕ).encard := by
  rw [← ENNReal.tsum_set_one]
  have h := tsum_subtype ({n | bad (x n)} : Set ℕ) (fun _ => (1 : ℝ≥0∞))
  rw [h]
  apply tsum_congr
  intro n
  simp only [Set.indicator_apply,Set.mem_setOf_eq]

theorem badCount_lt_top_iff_eventually (bad : Pair → Prop) [DecidablePred bad] (x : ℕ → Pair) :
    badCount bad x < ⊤ ↔ ∀ᶠ n in atTop, ¬ bad (x n) := by
  rw [badCount_eq_encard,ENat.toENNReal_lt_top,Set.encard_lt_top_iff]
  constructor
  · intro h
    obtain ⟨N,hN⟩ := h.bddAbove
    refine eventually_atTop.mpr ⟨N+1,?_⟩
    intro n hn hbad
    have := hN hbad
    omega
  · intro h
    obtain ⟨N,hN⟩ := eventually_atTop.mp h
    apply (Set.finite_lt_nat N).subset
    intro n hn
    by_contra hge
    exact hN n (by simpa using hge) hn

/-- Exact finite-state parity/count correspondence at the coBüchi encoding. -/
theorem cobuchi_parity_iff_badCount_finite [Fintype Pair]
    (bad : Pair → Prop) [DecidablePred bad] (x : ℕ → Pair) :
    ParitySuccess (coBuchiPriority bad) x ↔ badCount bad x < ⊤ := by
  rw [ParitySuccess,cobuchi_minimum_even_iff bad _ (recurrentSet_nonempty x),
    badCount_lt_top_iff_eventually]
  constructor
  · intro h
    filter_upwards [eventually_mem_recurrentSet x] with n hn
    exact h (x n) hn
  · intro h e he hbad
    obtain ⟨n,hn,hgood⟩ := ((mem_recurrentSet x e).mp he |>.and_eventually h).exists
    exact hgood (hn.symm ▸ hbad)

theorem badCount_measurable [Fintype Pair] [MeasurableSpace Pair] [MeasurableSingletonClass Pair]
    (bad : Pair → Prop) [DecidablePred bad] : Measurable (badCount bad) := by
  apply Measurable.ennreal_tsum
  intro n
  exact (measurable_of_finite (fun p : Pair => if bad p then (1 : ℝ≥0∞) else 0)).comp
    (measurable_pi_apply n)

/-- Quantitative success always implies a.s. coBüchi. The converse for the
specific generated controller requires the new stopped-cost analysis. -/
theorem finite_expected_badCount_implies_ae_parity
    [Fintype Pair] [MeasurableSpace Pair] [MeasurableSingletonClass Pair]
    (μ : Measure (ℕ → Pair)) (bad : Pair → Prop) [DecidablePred bad]
    (hfinite : (∫⁻ x, badCount bad x ∂μ) < ⊤) :
    ∀ᵐ x ∂μ, ParitySuccess (coBuchiPriority bad) x := by
  filter_upwards [ae_lt_top (badCount_measurable bad) hfinite.ne] with x hx
  exact (cobuchi_parity_iff_badCount_finite bad x).mpr hx

end HiddenParity.Cost
