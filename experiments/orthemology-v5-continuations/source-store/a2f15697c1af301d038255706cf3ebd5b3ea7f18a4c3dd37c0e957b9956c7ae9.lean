import CanonicalHistoryPMF

noncomputable section
set_option linter.unusedSectionVars false
open MeasureTheory ProbabilityTheory Finset Filter
open scoped BigOperators ENNReal
attribute [local instance] Classical.propDecidable
namespace Orthemology.Tranche3.CanonicalMicro
open Orthemology.Tranche2.PolicyEmbedding
universe u v
variable {A Y : Type u} [Fintype A] [Fintype Y] [DecidableEq A]

/-- Accumulated cost of the literally acquired actions, newest first. -/
def historyCost (c : A → ℝ≥0∞) (h : History A Y) : ℝ≥0∞ := (h.map (fun ay => c ay.1)).sum

omit [Fintype A] in
lemma historyPMF_invariant (π : History A Y → A) (P : A → Y → ℝ)
    (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1)
    (I : History A Y → Prop) (hI : I [])
    (hnext : ∀ h y, I h → 0 < P (π h) y → I ((π h,y)::h))
    (n : ℕ) (h : History A Y) (hp : historyPMF π P hP hN n h ≠ 0) : I h := by
  induction n generalizing h with
  | zero =>
    have he : h = [] := by
      by_contra he
      simp [historyPMF,PMF.pure_apply,he] at hp
    simpa only [he] using hI
  | succ n ih =>
    cases h with
    | nil => exact (hp (historyPMF_succ_nil π P hP hN n)).elim
    | cons ay h =>
      rcases ay with ⟨a,y⟩
      rw [historyPMF_succ_cons] at hp
      split_ifs at hp with he
      · have hp' := mul_ne_zero_iff.mp hp
        have hy : 0 < P a y := ENNReal.ofReal_pos.mp (pos_iff_ne_zero.mpr hp'.2)
        subst a
        exact hnext h y (ih h hp'.1) hy
      · exact (hp rfl).elim

omit [Fintype A] [DecidableEq A] in
lemma pmfMean_nextHistory (π : History A Y → A) (P : A → Y → ℝ)
    (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1)
    (h : History A Y) (f : History A Y → ℝ≥0∞) :
    pmfMean (nextHistoryPMF π P hP hN h) f =
      ∑ y, ENNReal.ofReal (P (π h) y) * f ((π h,y)::h) := by
  rw [nextHistoryPMF,pmfMean_map,pmfMean,tsum_fintype]
  rfl

omit [Fintype A] in
/-- A nonnegative one-step potential pays for every deterministic history
horizon under the actual finite controlled-iid experiment. -/
theorem historyPMF_cost_potential_bound (π : History A Y → A) (P : A → Y → ℝ)
    (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1)
    (c : A → ℝ≥0∞) (V : History A Y → ℝ≥0∞)
    (I : History A Y → Prop) (hI : I [])
    (hnext : ∀ h y, I h → 0 < P (π h) y → I ((π h,y)::h))
    (hstep : ∀ h, I h → c (π h) + ∑ y, ENNReal.ofReal (P (π h) y) * V ((π h,y)::h) ≤ V h)
    (n : ℕ) :
    pmfMean (historyPMF π P hP hN n) (fun h => historyCost c h + V h) ≤ V [] := by
  induction n with
  | zero => simp [historyPMF,pmfMean_pure,historyCost]
  | succ n ih =>
    rw [historyPMF,pmfMean_bind]
    apply le_trans (pmfMean_mono_on_support _ _ _ ?_) ih
    intro h hh
    have hi := historyPMF_invariant π P hP hN I hI hnext n h hh
    have hc : pmfMean (nextHistoryPMF π P hP hN h) (fun k => historyCost c k + V k) =
        historyCost c h + c (π h) + ∑ y, ENNReal.ofReal (P (π h) y) * V ((π h,y)::h) := by
      rw [nextHistoryPMF,pmfMean_map]
      have he : (fun y => historyCost c ((π h,y)::h) + V ((π h,y)::h)) =
          fun y => (historyCost c h + c (π h)) + V ((π h,y)::h) := by
        funext y
        simp only [historyCost,List.map_cons,List.sum_cons,Prod.fst]
        simp only [add_assoc,add_comm,add_left_comm]
      rw [he,pmfMean_add,pmfMean_const]
      congr 1
      rw [pmfMean,tsum_fintype]
      rfl
    rw [hc,add_assoc]
    exact add_le_add_left (hstep h hi) _

section CanonicalLaw
variable {R : Type v} [Inhabited Y] [MeasurableSpace R]
    [MeasurableSpace A] [MeasurableSingletonClass A]
    [MeasurableSpace Y] [MeasurableSingletonClass Y]

def ignoreSeed (π : History A Y → A) (_ : R) (h : History A Y) : A := π h

omit [DecidableEq A] [Inhabited Y] [MeasurableSingletonClass A] [MeasurableSpace Y] [MeasurableSingletonClass Y] in
lemma ignoreSeed_measurable (π : History A Y → A) :
    Measurable (fun z : R × History A Y => ignoreSeed π z.1 z.2) :=
  (measurable_of_countable π).comp measurable_snd

omit [Fintype A] [Fintype Y] [DecidableEq A] [Inhabited Y] [MeasurableSpace R]
    [MeasurableSpace A] [MeasurableSingletonClass A] [MeasurableSpace Y] [MeasurableSingletonClass Y] in
lemma actionCompatible_ignoreSeed (π : History A Y → A) (r : R) (h : History A Y) :
    ActionCompatible (ignoreSeed π) r h ↔ ActionCompatible (fun (_ : Unit) h => π h) () h := by
  induction h with
  | nil => rfl
  | cons ay h ih => simp only [ActionCompatible,ignoreSeed,ih]

/-- Exact finite-law identification with the pre-existing canonical fresh-row
experiment, for any common private-seed law. The constructed policy ignores the
seed, but its law is literally the original actionLaw interface. -/
theorem historyPMF_eq_canonical_marginal (π : History A Y → A)
    (ρ : Measure R) [IsProbabilityMeasure ρ] (P : A → Y → ℝ)
    (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1) (n : ℕ) :
    (historyPMF π P hP hN n).toMeasure =
      (ρ.prod (feedbackLaw P P hP hN hP hN)).map
        (fun z => historyTrajectory ∅ (ignoreSeed π) z n) := by
  apply Measure.ext_of_singleton
  intro h
  rw [PMF.toMeasure_apply_singleton _ h (measurableSet_singleton h),historyPMF_apply,
    history_marginal_formula ∅ (ignoreSeed π) (ignoreSeed_measurable π) ρ P P hP hN hP hN
      (fun a ha => (Finset.not_mem_empty a ha).elim)]
  have he : {r : R | ActionCompatible (ignoreSeed π) r h} =
      if ActionCompatible (fun (_ : Unit) h => π h) () h then Set.univ else ∅ := by
    ext r
    simp only [Set.mem_setOf_eq,actionCompatible_ignoreSeed]
    split_ifs <;> simp_all
  rw [he]
  by_cases hn : n = h.length <;> by_cases hc : ActionCompatible (fun (_ : Unit) h => π h) () h <;>
    simp [hn,hc]

lemma pmf_lintegral_eq_mean {α : Type*} [Countable α] [MeasurableSpace α] [MeasurableSingletonClass α]
    (p : PMF α) (f : α → ℝ≥0∞) : (∫⁻ a, f a ∂p.toMeasure) = pmfMean p f := by
  rw [lintegral_countable']
  simp only [PMF.toMeasure_apply_singleton _ _ (measurableSet_singleton _),pmfMean,mul_comm]

omit [Fintype A] [Fintype Y] [Inhabited Y] [MeasurableSpace R]
    [MeasurableSpace A] [MeasurableSingletonClass A] [MeasurableSpace Y] [MeasurableSingletonClass Y] in
lemma acquired_history_cost (π : R → History A Y → A) (U : Finset A)
    (oracle : ℕ → A → Y) (r : R) (X : Stack A Y) (c : A → ℝ≥0∞) (n : ℕ) :
    (∑ t ∈ Finset.range n, c (π r (observedHistory U π oracle r X t))) =
      historyCost c (observedHistory U π oracle r X n) := by
  induction n with
  | zero => simp [observedHistory,historyCost]
  | succ n ih =>
    rw [Finset.sum_range_succ,ih]
    simp only [observedHistory,historyCost,List.map_cons,List.sum_cons,Prod.fst]
    exact add_comm _ _

/-- Literal physical prefix-cost equality in the canonical action law. -/
theorem canonical_prefix_cost_eq_historyPMF (π : History A Y → A)
    (ρ : Measure R) [IsProbabilityMeasure ρ] (P : A → Y → ℝ)
    (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1)
    (c : A → ℝ≥0∞) (d : A) (n : ℕ) :
    (∫⁻ x, ∑ t ∈ Finset.range n, c (x t) ∂actionLaw (ignoreSeed π) ρ P hP hN d) =
      pmfMean (historyPMF π P hP hN n) (historyCost c) := by
  have hf : Measurable (fun x : ℕ → A => ∑ t ∈ Finset.range n, c (x t)) := by fun_prop
  have hh := historyTrajectory_measurable (∅ : Finset A) (ignoreSeed (R := R) π) (ignoreSeed_measurable π)
  have hfH : Measurable (fun H : ℕ → History A Y => ∑ t ∈ Finset.range n, c (historyAction d H t)) :=
    hf.comp (historyAction_measurable d)
  rw [actionLaw,lintegral_map hf (historyAction_measurable d),observedTraceLaw,
    lintegral_map hfH hh]
  have he : (fun z : Input R A Y => ∑ t ∈ Finset.range n,
      c (historyAction d (historyTrajectory ∅ (ignoreSeed π) z) t)) =
      fun z => historyCost c (historyTrajectory ∅ (ignoreSeed π) z n) := by
    funext z
    change (∑ t ∈ Finset.range n, c (((observedHistory ∅ (ignoreSeed π) z.2.2 z.1
      (fun a k => z.2.1 (a,k)) (t+1)).headD (d,default)).1)) = _
    simp only [observedHistory,List.headD_cons,Prod.fst]
    exact acquired_history_cost (ignoreSeed π) ∅ z.2.2 z.1 (fun a k => z.2.1 (a,k)) c n
  rw [he,← lintegral_map (measurable_of_countable (historyCost c))
    (historyTrajectory_coordinate_measurable ∅ (ignoreSeed π) (ignoreSeed_measurable π) n),
    ← historyPMF_eq_canonical_marginal π ρ P hP hN n,pmf_lintegral_eq_mean]

/-- End-to-end canonical-law drift principle. It assumes only a one-step
algebraic potential certificate on positive reachable histories. -/
theorem canonical_total_cost_of_drift (π : History A Y → A)
    (ρ : Measure R) [IsProbabilityMeasure ρ] (P : A → Y → ℝ)
    (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1)
    (c : A → ℝ≥0∞) (V : History A Y → ℝ≥0∞)
    (I : History A Y → Prop) (hI : I [])
    (hnext : ∀ h y, I h → 0 < P (π h) y → I ((π h,y)::h))
    (hstep : ∀ h, I h → c (π h) + ∑ y, ENNReal.ofReal (P (π h) y) * V ((π h,y)::h) ≤ V h)
    (d : A) :
    (∫⁻ x, ∑' t, c (x t) ∂actionLaw (ignoreSeed π) ρ P hP hN d) ≤ V [] := by
  rw [lintegral_tsum (fun t : ℕ => (show Measurable (fun x : ℕ → A => c (x t)) from by fun_prop).aemeasurable)]
  apply ENNReal.tsum_le_of_sum_range_le
  intro n
  rw [← lintegral_finset_sum (Finset.range n) (fun i _ => by fun_prop),
    canonical_prefix_cost_eq_historyPMF π ρ P hP hN c d n]
  exact (pmfMean_mono_on_support _ _ _ (fun h _ => le_self_add)).trans
    (historyPMF_cost_potential_bound π P hP hN c V I hI hnext hstep n)
end CanonicalLaw
end Orthemology.Tranche3.CanonicalMicro
