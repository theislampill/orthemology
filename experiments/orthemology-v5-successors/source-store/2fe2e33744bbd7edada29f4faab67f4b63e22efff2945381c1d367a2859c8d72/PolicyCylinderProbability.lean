import FeedbackFiberProbability

noncomputable section
open MeasureTheory ProbabilityTheory Set Finset
open scoped BigOperators ENNReal

namespace Orthemology.Tranche2.PolicyEmbedding
universe u v
variable {R : Type v} {A Y : Type u} [Fintype A] [Fintype Y] [DecidableEq A] [Inhabited Y]
    [MeasurableSpace R] [MeasurableSpace A] [MeasurableSingletonClass A]
    [MeasurableSpace Y] [MeasurableSingletonClass Y]

abbrev Input (R : Type v) (A Y : Type u) := R × (FlatStack A Y × RowOracle A Y)

def historyTrajectory (U : Finset A) (π : R → History A Y → A) (z : Input R A Y) : ℕ → History A Y :=
  observedHistory U π z.2.2 z.1 (fun a n => z.2.1 (a,n))

omit [MeasurableSpace A] [MeasurableSingletonClass A] in
omit [Inhabited Y] in
/-- Actual finite-history probability, including the arbitrary private seed.
The private compatible-seed factor and all feedback factors are derived from
the deterministic fiber identity and actual independent product measures. -/
theorem private_transcript_cylinder_probability
    (U : Finset A) (π : R → History A Y → A) (ρ : Measure R) [IsProbabilityMeasure ρ]
    (base P : A → Y → ℝ)
    (hb : ∀ a y, 0 ≤ base a y) (hbn : ∀ a, ∑ y, base a y = 1)
    (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1)
    (hagree : ∀ a ∈ U, base a = P a) (D : Set R) (h : History A Y) :
    (ρ.prod (feedbackLaw base P hb hbn hP hN))
      {z | z.1 ∈ D ∧ historyTrajectory U π z h.length = h} =
      ρ (D ∩ {r | ActionCompatible π r h}) * ∏ i : Fin h.length, ENNReal.ofReal (P h[i].1 h[i].2) := by
  have he : {z : Input R A Y | z.1 ∈ D ∧ historyTrajectory U π z h.length = h} =
      (D ∩ {r | ActionCompatible π r h}) ×ˢ
        {ω | FeedbackCompatible U (fun a n => ω.1 (a,n)) ω.2 h} := by
    ext z
    simp only [Set.mem_setOf_eq,Set.mem_prod,Set.mem_inter_iff,historyTrajectory,observedHistory_fiber]
    tauto
  rw [he,Measure.prod_prod,feedbackCompatible_probability U h base P hb hbn hP hN hagree]

/-- The observed history coordinate is measurable despite the arbitrary
private seed space and countably infinite feedback stacks. -/
theorem historyTrajectory_coordinate_measurable
    (U : Finset A) (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2)) (n : ℕ) :
    Measurable (fun z : Input R A Y => historyTrajectory U π z n) := by
  have hX : Measurable (fun z : Input R A Y => fun a k => z.2.1 (a,k)) :=
    measurable_pi_lambda _ (fun a => measurable_pi_lambda _ (fun k =>
      (measurable_pi_apply (a,k)).comp measurable_snd.fst))
  have hi : Measurable (fun z : Input R A Y =>
      ((z.1,((fun a k => z.2.1 (a,k)),([] : History A Y))),z.2.2)) :=
    (measurable_fst.prodMk (hX.prodMk measurable_const)).prodMk measurable_snd.snd
  have hr := (FiniteAlphabetQuery.measurable_run (query U π) (step U π)
    (query_measurable U π hπ) (step_measurable U π hπ) n).comp hi
  have he : (fun z : Input R A Y => historyTrajectory U π z n) =
      fun z => (FiniteAlphabetQuery.run (query U π) (step U π) z.2.2
        (z.1,((fun a k => z.2.1 (a,k)),[])) n).1.2.2 := by
    funext z
    exact (congrArg (fun s => s.1.2.2) (policyRun_eq_observedHistory U π z.2.2 z.1 (fun a k => z.2.1 (a,k)) n)).symm
  rw [he]
  exact hr.fst.snd.snd

theorem historyTrajectory_measurable
    (U : Finset A) (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2)) :
    Measurable (historyTrajectory U π) :=
  measurable_pi_lambda _ (historyTrajectory_coordinate_measurable U π hπ)

def observedTraceLaw (U : Finset A) (π : R → History A Y → A) (ρ : Measure R)
    (base P : A → Y → ℝ)
    (hb : ∀ a y, 0 ≤ base a y) (hbn : ∀ a, ∑ y, base a y = 1)
    (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1) : Measure (ℕ → History A Y) :=
  (ρ.prod (feedbackLaw base P hb hbn hP hN)).map (historyTrajectory U π)

/- Equality with the canonical all-query model is pursued in the successor;
this file proves the exact finite-history probability without assuming it. -/
end Orthemology.Tranche2.PolicyEmbedding
