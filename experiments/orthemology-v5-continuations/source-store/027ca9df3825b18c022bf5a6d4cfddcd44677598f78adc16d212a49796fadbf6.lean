import ProcessExpectation

namespace IndependentProcessContract
noncomputable section
open MeasureTheory ProbabilityTheory Finset
open scoped ENNReal BigOperators
open SparsePriorBayes SparsePriorProcess

/-- This report function has no latent-index argument and only reads positions < n. -/
def observedReport {Z : Type*} (pi : Z → Policy) (n : ℕ) (z : Z) (y : ℕ → Bool) : ℝ :=
  pi z n ((range n).filter (fun k => y k = true))

def rawCount {Z : Type*} (a : ℕ → ℝ) (e : ℝ) (pi : Z → Policy)
    (omega : Z × (ℕ × (ℕ → Bool))) : ℝ≥0∞ := by
  classical
  exact ∑' n : ℕ,
    if (observedReport pi (n+1) omega.1 omega.2.2)^2 - (1/4 : ℝ) -
          a omega.2.1 * e * (1+e) ≤ 0 ∧
       (1-observedReport pi (n+1) omega.1 omega.2.2)^2 - (1/4 : ℝ) +
          a omega.2.1 * e * (1-e) ≤ 0
    then (0 : ℝ≥0∞) else (1 : ℝ≥0∞)

theorem rawCount_eq {Z : Type*} (a : ℕ → ℝ) (e : ℝ) (pi : Z → Policy) :
    rawCount a e pi = totalFailures a e pi := by
  funext omega
  unfold rawCount totalFailures
  apply tsum_congr
  intro n
  unfold stageFailure literalFailure SparsePriorGeometry.Accepted observedReport prefixSet
  split_ifs <;> rfl

/-- The index is mixed once, while each summand contains an entire iid stream. -/
def rawLaw {Z : Type*} [MeasurableSpace Z] (eta : Measure Z)
    (a : ℕ → ℝ) (p : ℝ) (_hp : 0 < p) (ha : ∀ i, 0 < a i)
    (hh : ∀ i, a i ≤ (1/2 : ℝ)) (_hs : ∀ i, a (i+1) ≤ a i/2) :
    Measure (Z × (ℕ × (ℕ → Bool))) :=
  eta.prod (Measure.sum (fun i =>
    ENNReal.ofReal ((a i)^p / (∑' j : ℕ, (a j)^p)) •
      (Measure.dirac i).prod
        (Measure.infinitePi (fun _ : ℕ =>
          sourceCoinMeasure (a i) (ha i).le (by have h := hh i; linarith)))))

theorem rawLaw_eq {Z : Type*} [MeasurableSpace Z] (eta : Measure Z)
    (a : ℕ → ℝ) (p : ℝ) (hp : 0 < p) (ha : ∀ i, 0 < a i)
    (hh : ∀ i, a i ≤ (1/2 : ℝ)) (hs : ∀ i, a (i+1) ≤ a i/2) :
    rawLaw eta a p hp ha hh hs = experimentLaw eta a p hp ha hh hs := by rfl

theorem rawLaw_probability {Z : Type*} [MeasurableSpace Z] (eta : Measure Z)
    [IsProbabilityMeasure eta] (a : ℕ → ℝ) (p : ℝ) (hp : 0 < p)
    (ha : ∀ i, 0 < a i) (hh : ∀ i, a i ≤ (1/2 : ℝ))
    (hs : ∀ i, a (i+1) ≤ a i/2) :
    IsProbabilityMeasure (rawLaw eta a p hp ha hh hs) := by
  rw [rawLaw_eq]
  infer_instance

/-- Independent expanded experiment/literal-count target type. -/
theorem expanded_process_iff {Z : Type*} [MeasurableSpace Z] (eta : Measure Z)
    [IsProbabilityMeasure eta] (a : ℕ → ℝ) (p e : ℝ) (hp : 0 < p)
    (ha : ∀ i, 0 < a i) (hh : ∀ i, a i ≤ (1/2 : ℝ))
    (hs : ∀ i, a (i+1) ≤ a i/2) (he : 0 < e) (he4 : e ≤ (1/4 : ℝ)) :
    (∃ pi : Z → (ℕ → Finset ℕ → ℝ),
      (∀ n S, Measurable (fun z => pi z n S)) ∧
      (∫⁻ omega, rawCount a e pi omega ∂rawLaw eta a p hp ha hh hs) < ⊤) ↔
    Summable (fun i : ℕ => ((a (i+1))^p/a i)*Real.log (a i/a (i+1))) := by
  simpa only [rawCount_eq, rawLaw_eq] using
    exists_finite_actual_expectation_iff eta a p e hp ha hh hs he he4

theorem all_half_from_initial (a : ℕ → ℝ) (h0 : a 0 ≤ (1/2 : ℝ))
    (hs : ∀ i, a (i+1) ≤ a i/2) : ∀ i, a i ≤ (1/2 : ℝ) := by
  intro i
  induction i with
  | zero => exact h0
  | succ i ih => have h := hs i; linarith

/-- The original p=1 problem with just the initial upper bound is a specialization. -/
theorem initial_bound_p_one_iff {Z : Type*} [MeasurableSpace Z] (eta : Measure Z)
    [IsProbabilityMeasure eta] (a : ℕ → ℝ) (e : ℝ)
    (ha : ∀ i, 0 < a i) (h0 : a 0 ≤ (1/2 : ℝ))
    (hs : ∀ i, a (i+1) ≤ a i/2) (he : 0 < e) (he4 : e ≤ (1/4 : ℝ)) :
    (∃ pi : Z → Policy, (∀ n S, Measurable (fun z => pi z n S)) ∧
      (∫⁻ omega, rawCount a e pi omega
        ∂rawLaw eta a 1 (by norm_num) ha (all_half_from_initial a h0 hs) hs) < ⊤) ↔
      Summable (fun i : ℕ => (a (i+1)/a i)*Real.log (a i/a (i+1))) := by
  simpa only [Real.rpow_one] using
    expanded_process_iff eta a 1 e (by norm_num) ha
      (all_half_from_initial a h0 hs) hs he he4

theorem prefix_eq_of_agree (n : ℕ) (y y' : Receipts)
    (h : ∀ k, k<n → y k = y' k) : prefixSet n y = prefixSet n y' := by
  ext k
  by_cases hk : k<n
  · simp [prefixSet, hk, h k hk]
  · simp [prefixSet, hk]

theorem no_future_receipt {Z : Type*} (pi : Z → Policy) (n : ℕ) (z : Z)
    (y y' : Receipts) (h : ∀ k, k<n → y k = y' k) :
    observedReport pi n z y = observedReport pi n z y' := by
  change pi z n (prefixSet n y) = pi z n (prefixSet n y')
  rw [prefix_eq_of_agree n y y' h]

/-- Full words retain order information even when their cardinalities agree. -/
def orderSensitive : Policy := fun _ S => if 0 ∈ S then (3/4 : ℝ) else (1/2 : ℝ)

example : ({0} : Finset ℕ).card = ({1} : Finset ℕ).card ∧
    orderSensitive 2 {0} ≠ orderSensitive 2 {1} := by
  norm_num [orderSensitive]

/-- A fixed latent index and prefix have exactly the advertised joint mass. -/
theorem latent_cylinder (a : ℕ → ℝ) (p : ℝ) (hp : 0 < p)
    (ha : ∀ i, 0 < a i) (hh : ∀ i, a i ≤ (1/2 : ℝ))
    (hs : ∀ i, a (i+1) ≤ a i/2) (i n : ℕ) (S : Finset ℕ)
    (hS : S ⊆ range n) :
    latentLaw a p hp ha hh hs (({i} : Set ℕ) ×ˢ prefixEvent n S) =
      ENNReal.ofReal (priorWeight a p i) *
        ENNReal.ofReal ((a i)^S.card*(1-a i)^(n-S.card)) := by
  unfold latentLaw
  rw [Measure.sum_apply _ ((measurableSet_singleton i).prod (prefixEvent_measurable n S hS))]
  simp only [Measure.smul_apply, smul_eq_mul, Measure.prod_prod]
  rw [tsum_eq_single i]
  · simp [Measure.dirac_apply, receiptLaw_prefix_mass (a i) (ha i).le
      (show a i ≤ 1 by have h := hh i; linarith) n S hS]
  · intro j hji
    simp [Measure.dirac_apply, hji]

theorem independent_seed_cylinder {Z : Type*} [MeasurableSpace Z]
    (eta : Measure Z) [IsProbabilityMeasure eta]
    (a : ℕ → ℝ) (p : ℝ) (hp : 0 < p)
    (ha : ∀ i, 0 < a i) (hh : ∀ i, a i ≤ (1/2 : ℝ))
    (hs : ∀ i, a (i+1) ≤ a i/2) (U : Set Z) (i n : ℕ) (S : Finset ℕ)
    (hS : S ⊆ range n) :
    experimentLaw eta a p hp ha hh hs (U ×ˢ (({i} : Set ℕ) ×ˢ prefixEvent n S)) =
      eta U * ENNReal.ofReal (priorWeight a p i) *
        ENNReal.ofReal ((a i)^S.card*(1-a i)^(n-S.card)) := by
  rw [experimentLaw, Measure.prod_prod, latent_cylinder a p hp ha hh hs i n S hS]
  ring

/-- Accepted real outputs are automatically coherent under the loss contract. -/
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

/-- Charging the optional empty-prefix report adds expected cost at most one. -/
theorem initial_expected_cost_le_one {Z : Type*} [MeasurableSpace Z] (eta : Measure Z)
    [IsProbabilityMeasure eta] (a : ℕ → ℝ) (p e : ℝ) (hp : 0 < p)
    (ha : ∀ i, 0 < a i) (hh : ∀ i, a i ≤ (1/2 : ℝ))
    (hs : ∀ i, a (i+1) ≤ a i/2) (pi : Z → Policy) :
    (∫⁻ omega, stageFailure a e pi 0 omega ∂experimentLaw eta a p hp ha hh hs) ≤ 1 := by
  have hpoint (omega : Z × (ℕ × Receipts)) : stageFailure a e pi 0 omega ≤ 1 := by
    classical
    unfold stageFailure literalFailure
    split_ifs <;> simp
  calc
    _ ≤ ∫⁻ _omega, (1 : ℝ≥0∞) ∂experimentLaw eta a p hp ha hh hs :=
      lintegral_mono hpoint
    _ = 1 := by simp

#print axioms expanded_process_iff
#print axioms initial_bound_p_one_iff
#print axioms rawLaw_probability
#print axioms no_future_receipt
#print axioms latent_cylinder
#print axioms independent_seed_cylinder
#print axioms accepted_is_coherent
#print axioms coherent_policy_finite_iff
#print axioms initial_expected_cost_le_one
end
end IndependentProcessContract
