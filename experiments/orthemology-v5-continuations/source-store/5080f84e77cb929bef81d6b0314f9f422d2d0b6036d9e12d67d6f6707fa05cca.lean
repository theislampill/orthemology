import ConcreteSparsePrior

namespace IndependentConcreteContract
noncomputable section
open MeasureTheory ProbabilityTheory
open scoped ENNReal
open SparsePriorBayes SparsePriorProcess ConcreteSparsePrior

/- The coherent-output helper bodies are reused from the separately accepted
independent process contract probe, without changing that frozen source. -/
theorem accepted_is_coherent (a e q : ℝ) (ha : 0 ≤ a) (ha1 : a ≤ 1)
    (he : 0 < e) (he4 : e ≤ (1/4 : ℝ))
    (h : SparsePriorGeometry.Accepted a e q) : 0 ≤ q ∧ q ≤ 1 := by
  rcases h with ⟨h0,h1⟩
  have ht1 : 0 ≤ a*e*(1-e) :=
    mul_nonneg (mul_nonneg ha he.le) (by linarith)
  have ht0' : a*(e*(1+e)) ≤ e*(1+e) := by
    have h := mul_le_mul_of_nonneg_right ha1
      (show 0 ≤ e*(1+e) by positivity)
    simpa using h
  have heq : e*(1+e) ≤ (5/16 : ℝ) := by
    nlinarith [mul_nonneg he.le (show 0 ≤ (1/4 : ℝ)-e by linarith)]
  have ht0 : a*e*(1+e) ≤ (5/16 : ℝ) := by nlinarith
  constructor
  · nlinarith [sq_nonneg (q-(1/2 : ℝ))]
  · nlinarith [sq_nonneg (q-1)]

def clipReport (q : ℝ) : ℝ := max 0 (min 1 q)

lemma clipReport_coherent (q : ℝ) : 0 ≤ clipReport q ∧ clipReport q ≤ 1 := by
  exact ⟨le_max_left _ _, max_le (by norm_num) (min_le_left _ _)⟩

lemma clipReport_eq {q : ℝ} (hq0 : 0 ≤ q) (hq1 : q ≤ 1) : clipReport q = q := by
  simp only [clipReport, min_eq_right hq1, max_eq_right hq0]

lemma clipped_failure_le (a e q : ℝ) (ha : 0 ≤ a) (ha1 : a ≤ 1)
    (he : 0 < e) (he4 : e ≤ (1/4 : ℝ)) :
    literalFailure a e (clipReport q) ≤ literalFailure a e q := by
  classical
  by_cases h : SparsePriorGeometry.Accepted a e q
  · have hc := accepted_is_coherent a e q ha ha1 he he4 h
    rw [clipReport_eq hc.1 hc.2]
  · unfold literalFailure
    simp only [h, if_false]
    split_ifs <;> simp

/-- Restricting every output to a coherent binary report preserves the sharp iff. -/
theorem coherent_policy_finite_iff {Z : Type*} [MeasurableSpace Z] (eta : Measure Z)
    [IsProbabilityMeasure eta] (a : ℕ → ℝ) (p e : ℝ) (hp : 0 < p)
    (ha : ∀ i, 0 < a i) (hh : ∀ i, a i ≤ (1/2 : ℝ))
    (hs : ∀ i, a (i+1) ≤ a i/2) (he : 0 < e) (he4 : e ≤ (1/4 : ℝ)) :
    (∃ pi : Z → Policy, (∀ n S, Measurable (fun z => pi z n S)) ∧
      (∀ z n S, 0 ≤ pi z n S ∧ pi z n S ≤ 1) ∧
      (∫⁻ omega, totalFailures a e pi omega ∂experimentLaw eta a p hp ha hh hs) < ⊤) ↔
    Summable (fun i : ℕ => ((a (i+1))^p/a i)*Real.log (a i/a (i+1))) := by
  constructor
  · rintro ⟨pi,hmeas,_hcoherent,hfin⟩
    exact (exists_finite_actual_expectation_iff eta a p e hp ha hh hs he he4).mp
      ⟨pi,hmeas,hfin⟩
  · intro hsum
    obtain ⟨pi,hmeas,hfin⟩ :=
      (exists_finite_actual_expectation_iff eta a p e hp ha hh hs he he4).mpr hsum
    let pi' : Z → Policy := fun z n S => clipReport (pi z n S)
    refine ⟨pi',?_,?_,?_⟩
    · intro n S
      exact measurable_const.max (measurable_const.min (hmeas n S))
    · intro z n S
      exact clipReport_coherent _
    · have hcount (omega : Z × (ℕ × Receipts)) :
          totalFailures a e pi' omega ≤ totalFailures a e pi omega := by
        unfold totalFailures
        apply ENNReal.tsum_le_tsum
        intro n
        exact clipped_failure_le (a omega.2.1) e
          (pi omega.1 (n+1) (prefixSet (n+1) omega.2.2))
          (ha omega.2.1).le (by have h := hh omega.2.1; linarith) he he4
      exact lt_of_le_of_lt (lintegral_mono hcount) hfin

abbrev fullLaw {Z : Type*} [MeasurableSpace Z] (eta : Measure Z) :=
  experimentLaw eta quadraticSupport 1 (by norm_num) quadraticSupport_pos
    quadraticSupport_half quadraticSupport_sep

def parameter {Z : Type*} (omega : Z × (ℕ × Receipts)) : ℝ :=
  quadraticSupport omega.2.1

example : quadraticSupport 0 = Real.exp (-1) := by norm_num [quadraticSupport]
example : quadraticSupport 1 = Real.exp (-4) := by norm_num [quadraticSupport]
example : quadraticSupport 1 / quadraticSupport 0 = Real.exp (-3) := by
  simpa using quadraticSupport_ratio 0

theorem parameter_strictly_interior {Z : Type*} (omega : Z × (ℕ × Receipts)) :
    0 < parameter omega ∧ parameter omega < 1 := by
  constructor
  · exact quadraticSupport_pos _
  · have h := quadraticSupport_half omega.2.1
    change quadraticSupport omega.2.1 < 1
    linarith

/-- Functions of the parameter have the same integral after adding the independent seed. -/
theorem seed_product_integral {Z : Type*} [MeasurableSpace Z] (eta : Measure Z)
    [IsProbabilityMeasure eta] (f : ℕ → ℝ≥0∞) :
    (∫⁻ omega, f omega.2.1 ∂fullLaw eta) =
      ∫⁻ iy : ℕ × Receipts, f iy.1
        ∂latentLaw quadraticSupport 1 (by norm_num) quadraticSupport_pos
          quadraticSupport_half quadraticSupport_sep := by
  have hf : Measurable (fun omega : Z × (ℕ × Receipts) => f omega.2.1) :=
    (measurable_of_countable f).comp (measurable_snd.fst)
  unfold fullLaw experimentLaw
  rw [lintegral_prod _ hf.aemeasurable]
  simp only [lintegral_const, measure_univ, mul_one]

theorem full_inverse_moment {Z : Type*} [MeasurableSpace Z] (eta : Measure Z)
    [IsProbabilityMeasure eta] :
    (∫⁻ omega, ENNReal.ofReal (1/parameter omega) ∂fullLaw eta) = ⊤ := by
  unfold parameter
  rw [seed_product_integral eta (fun i : ℕ => ENNReal.ofReal (1/quadraticSupport i))]
  exact quadraticSupport_inverse_moment_infinite

theorem full_inverse_variance {Z : Type*} [MeasurableSpace Z] (eta : Measure Z)
    [IsProbabilityMeasure eta] :
    (∫⁻ omega, ENNReal.ofReal (1/(parameter omega*(1-parameter omega))) ∂fullLaw eta) = ⊤ := by
  unfold parameter
  rw [seed_product_integral eta (fun i : ℕ =>
    ENNReal.ofReal (1/(quadraticSupport i*(1-quadraticSupport i))))]
  exact quadraticSupport_inverse_variance_infinite

theorem full_no_endpoint_atoms {Z : Type*} [MeasurableSpace Z] (eta : Measure Z) :
    fullLaw eta {omega | parameter omega = 0 ∨ parameter omega = 1} = 0 := by
  have he : {omega : Z × (ℕ × Receipts) | parameter omega = 0 ∨ parameter omega = 1} = ∅ := by
    apply Set.eq_empty_iff_forall_not_mem.mpr
    intro omega h
    have hi := parameter_strictly_interior omega
    rcases h with h | h <;> linarith
  rw [he, measure_empty]

/-- All properties hold under one and the same complete seeded experiment,
and the finite-count witness can be required to issue coherent reports. -/
theorem coherent_counterexample_same_law {Z : Type*} [MeasurableSpace Z] (eta : Measure Z)
    [IsProbabilityMeasure eta] (e : ℝ) (he : 0 < e) (he4 : e ≤ (1/4 : ℝ)) :
    ∃ pi : Z → Policy, (∀ n S, Measurable (fun z => pi z n S)) ∧
      (∀ z n S, 0 ≤ pi z n S ∧ pi z n S ≤ 1) ∧
      (∫⁻ omega, totalFailures quadraticSupport e pi omega ∂fullLaw eta) < ⊤ ∧
      (∫⁻ omega, ENNReal.ofReal (1/parameter omega) ∂fullLaw eta) = ⊤ ∧
      (∫⁻ omega, ENNReal.ofReal (1/(parameter omega*(1-parameter omega))) ∂fullLaw eta) = ⊤ ∧
      fullLaw eta {omega | parameter omega = 0 ∨ parameter omega = 1} = 0 := by
  obtain ⟨pi,hmeas,hcoherent,hfin⟩ :=
    (coherent_policy_finite_iff eta quadraticSupport 1 e (by norm_num)
      quadraticSupport_pos quadraticSupport_half quadraticSupport_sep he he4).mpr
        quadraticSupport_spacing_summable
  exact ⟨pi,hmeas,hcoherent,hfin,full_inverse_moment eta,
    full_inverse_variance eta,full_no_endpoint_atoms eta⟩

#print axioms parameter_strictly_interior
#print axioms seed_product_integral
#print axioms full_inverse_moment
#print axioms full_inverse_variance
#print axioms full_no_endpoint_atoms
#print axioms coherent_counterexample_same_law
end
end IndependentConcreteContract
