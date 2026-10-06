import FiniteMemoryLaw

noncomputable section
open MeasureTheory
open scoped ENNReal BigOperators
open Orthemology.Tranche2.PolicyEmbedding
namespace HiddenParity.Cost.HistoryPMF
attribute [local instance] Classical.propDecidable
universe u v
variable {A Y : Type u} {Q : Type v}
variable [Fintype A] [Fintype Y] [DecidableEq A] [Inhabited Y]
variable [MeasurableSpace A] [MeasurableSingletonClass A]
variable [MeasurableSpace Y] [MeasurableSingletonClass Y]
variable [DecidableEq Q]

/-- Track a fixed finite controller while allowing arbitrary additional
history-dependent stopping. A disagreement of the actual policy's action is
also killed. This makes the eventual comparison theorem honest for any policy;
a source-specific interval adapter must prove agreement before its own stop. -/
def monitor (choose : Q → A) (update : Q → Y → Q) (kill : Q)
    (halt : History A Y → Prop) (q₀ : Q) : History A Y → Q
  | [] => q₀
  | (a,y)::h =>
      let q := monitor choose update kill halt q₀ h
      if q=kill ∨ a≠choose q ∨ halt ((a,y)::h) then kill else update q y

variable (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y=1)
variable (π : History A Y → A) (choose : Q → A) (update : Q → Y → Q) (kill : Q)
variable (halt : History A Y → Prop) (q₀ : Q)

/-- The actual one-step row, monitored with extra killing, is dominated at
every surviving state by the frozen transition. This derives the inequality
from action agreement and the literal normalized row probabilities. -/
theorem monitored_step_le (h : History A Y) (q' : Q) (hq' : q'≠kill) :
    ((step P hP hN π h).map (monitor choose update kill halt q₀)) q' ≤
      transition P hP hN choose update (monitor choose update kill halt q₀ h) q' := by
  classical
  simp only [step,PMF.map_comp,transition,PMF.map_apply,symbolPMF_apply]
  apply ENNReal.tsum_le_tsum
  intro y
  by_cases hk : monitor choose update kill halt q₀ h=kill
  · simp [Function.comp_def,monitor,hk,hq']
  · by_cases ha : π h=choose (monitor choose update kill halt q₀ h)
    · by_cases hh : halt ((choose (monitor choose update kill halt q₀ h),y)::h)
      · simp [Function.comp_def,monitor,hk,ha,hh,hq']
      · simp [Function.comp_def,monitor,hk,ha,hh]
    · simp [Function.comp_def,monitor,hk,ha,hq']

/-- Arbitrary adapted extra stopping and policy disagreement cannot increase
the probability mass of any surviving finite-state readout. There is no
independence or stopping-time distribution assumption in this theorem. -/
theorem monitored_marginal_le
    (habs : ∀ y, update kill y=kill) (n : ℕ) (q' : Q) (hq' : q'≠kill) :
    ((historyPMF P hP hN π n).map (monitor choose update kill halt q₀)) q' ≤
      iteratePMF (transition P hP hN choose update) n q₀ q' := by
  classical
  let K := transition P hP hN choose update
  let f := monitor choose update kill halt q₀
  have hKkill : K kill=PMF.pure kill := by
    change (symbolPMF P hP hN (choose kill)).map (update kill)=_
    rw [show update kill=Function.const Y kill from funext habs,PMF.map_const]
  induction n generalizing q' with
  | zero => simp [historyPMF,PMF.pure_map,monitor,iteratePMF]
  | succ n ih =>
      rw [historyPMF,PMF.map_bind,PMF.bind_apply]
      have hStep : (∑' h, historyPMF P hP hN π n h * ((step P hP hN π h).map f) q') ≤
          ∑' h, historyPMF P hP hN π n h * K (f h) q' := by
        apply ENNReal.tsum_le_tsum
        intro h
        exact mul_le_mul_left' (monitored_step_le P hP hN π choose update kill halt q₀ h q' hq') _
      apply hStep.trans
      change ((historyPMF P hP hN π n).bind (K ∘ f)) q' ≤ _
      rw [← PMF.bind_map,iteratePMF,PMF.bind_apply,PMF.bind_apply]
      apply ENNReal.tsum_le_tsum
      intro q
      by_cases hq : q=kill
      · subst q
        rw [hKkill,PMF.pure_apply,if_neg hq']
        simp
      · exact mul_le_mul_right' (ih q hq) (K q q')

variable [Fintype Q] [MeasurableSpace Q] [MeasurableSingletonClass Q]

/-- The probability statement concerns the actual original canonical history
law, not merely a recurrence or assumed finite distribution. -/
theorem actual_monitored_survival_le
    (habs : ∀ y, update kill y=kill) (n : ℕ) :
    (observedTraceLaw ∅ (fun (_ : Unit) h => π h) (Measure.dirac ()) P P hP hN hP hN)
      {H | monitor choose update kill halt q₀ (H n)≠kill} ≤
    (iteratePMF (transition P hP hN choose update) n q₀).toMeasure {q | q≠kill} := by
  classical
  let f := monitor choose update kill halt q₀
  let μ := observedTraceLaw ∅ (fun (_ : Unit) h => π h) (Measure.dirac ()) P P hP hN hP hN
  have hf : Measurable f := measurable_of_countable _
  have hs : MeasurableSet {q : Q | q≠kill} := (Set.toFinite _).measurableSet
  have hmap : μ.map (f ∘ (fun H : ℕ → History A Y => H n)) =
      ((historyPMF P hP hN π n).map f).toMeasure := by
    rw [← Measure.map_map hf (measurable_pi_apply n),actual_history_marginal_eq_pmf,PMF.toMeasure_map _ _ hf]
  change μ ((f ∘ (fun H : ℕ → History A Y => H n)) ⁻¹' {q | q≠kill}) ≤ _
  rw [← Measure.map_apply (hf.comp (measurable_pi_apply n)) hs,hmap,
    PMF.toMeasure_apply_fintype,PMF.toMeasure_apply_fintype]
  apply Finset.sum_le_sum
  intro q _
  by_cases hq : q≠kill
  · simp only [Set.indicator_apply,Set.mem_setOf_eq,if_pos hq]
    exact monitored_marginal_le P hP hN π choose update kill halt q₀ habs n q hq
  · simp only [Set.indicator_apply,Set.mem_setOf_eq,if_neg hq]
    exact le_rfl

end HiddenParity.Cost.HistoryPMF
