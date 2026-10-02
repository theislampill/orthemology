import EndpointMoment

namespace AnnularLiteral
noncomputable section
open MeasureTheory Set
open scoped ENNReal

def D0 (a e q : ℝ) : ℝ := q^2 - 1/4 - a*e*(1+e)
def D1 (a e q : ℝ) : ℝ := (1-q)^2 - 1/4 + a*e*(1-e)
def Accepted (a e q : ℝ) : Prop := D0 a e q ≤ 0 ∧ D1 a e q ≤ 0

def lower (e q : ℝ) : ℝ := (q^2-1/4)/(e*(1+e))
def upper (e q : ℝ) : ℝ := (1/4-(1-q)^2)/(e*(1-e))

lemma accepted_range {a e q : ℝ} (ha : 0 ≤ a) (ha1 : a ≤ 1)
    (he : 0 < e) (he4 : e ≤ 1/4) (h : Accepted a e q) :
    1/2 ≤ q ∧ q ≤ 1/2+e := by
  have h1e : 0 < 1-e := by linarith
  obtain ⟨h0,h1⟩ := h
  dsimp [D0,D1] at h0 h1
  have hp : 0 ≤ a*e*(1-e) := by positivity
  have hq : 1/2 ≤ q := by
    nlinarith [sq_nonneg (q-1/2)]
  constructor
  · exact hq
  · have hpa : a*e*(1+e) ≤ e*(1+e) := by
      nlinarith [mul_nonneg (show 0 ≤ 1-a by linarith) (show 0 ≤ e*(1+e) by positivity)]
    nlinarith

lemma accepted_iff_bounds {a e q : ℝ} (he : 0 < e) (he4 : e ≤ 1/4) :
    Accepted a e q ↔ lower e q ≤ a ∧ a ≤ upper e q := by
  have h1e : 0 < 1-e := by linarith
  have h0 : 0 < e*(1+e) := by positivity
  have h1 : 0 < e*(1-e) := by positivity
  unfold Accepted D0 D1 lower upper
  rw [div_le_iff₀ h0, le_div_iff₀ h1]
  constructor <;> intro h <;> constructor <;> nlinarith [h.1,h.2]

/-- Left multiplicative width, uniformly bounded by 5/3. -/
lemma left_width {e q : ℝ} (he : 0 < e) (he4 : e ≤ 1/4) (hq : 1/2 ≤ q) :
    upper e q ≤ (5/3)*lower e q := by
  have h1e : 0 < 1-e := by linarith
  let t := q-1/2
  have ht : 0 ≤ t := by dsimp [t];linarith
  have hnum : 3*(t-t^2)*(1+e) ≤ 5*(t+t^2)*(1-e) := by
    have hA := mul_nonneg ht (show 0 ≤ 1-4*e by linarith)
    have hB := mul_nonneg (sq_nonneg t) (show 0 ≤ 4-e by linarith)
    nlinarith
  have hu : 1/4-(1-q)^2 = t-t^2 := by dsimp [t];ring
  have hl : q^2-1/4 = t+t^2 := by dsimp [t];ring
  unfold upper lower
  rw [hu,hl,← mul_div_assoc]
  apply (div_le_div_iff₀ (by positivity : 0<e*(1-e)) (by positivity : 0<e*(1+e))).2
  have hs := mul_le_mul_of_nonneg_left hnum he.le
  convert div_le_div_of_nonneg_right hs (show 0 ≤ (3:ℝ) by norm_num) using 1 <;> ring

/-- Right width is9/5, proved separately rather than by an invalid symmetry. -/
lemma right_width {e q : ℝ} (he : 0 < e) (he4 : e ≤ 1/4) (hq : q ≤ 1/2+e) :
    1-lower e q ≤ (9/5)*(1-upper e q) := by
  have h1e : 0 < 1-e := by linarith
  let t := 1/2+e-q
  have ht : 0 ≤ t := by dsimp [t];linarith
  have hbase : 0 ≤ 4-14*e-8*e^2 := by
    have h := mul_nonneg (show 0 ≤ 1-4*e by linarith) (show 0 ≤ 2+e by linarith)
    nlinarith
  have hnum : 5*t*(1+2*e-t)*(1-e) ≤ 9*t*(1-2*e+t)*(1+e) := by
    have hA := mul_nonneg ht hbase
    have hB := mul_nonneg (sq_nonneg t) (show 0 ≤ 14+4*e by linarith)
    nlinarith
  have hne0 : e*(1+e) ≠ 0 := by positivity
  have hne1 : e*(1-e) ≠ 0 := by positivity
  have hu : 1-lower e q = t*(1+2*e-t)/(e*(1+e)) := by
    unfold lower
    field_simp
    dsimp [t]
    ring
  have hl : 1-upper e q = t*(1-2*e+t)/(e*(1-e)) := by
    unfold upper
    field_simp
    dsimp [t]
    ring
  rw [hu,hl,← mul_div_assoc]
  apply (div_le_div_iff₀ (by positivity : 0<e*(1+e)) (by positivity : 0<e*(1-e))).2
  have hs := mul_le_mul_of_nonneg_left hnum he.le
  convert div_le_div_of_nonneg_right hs (show 0 ≤ (5:ℝ) by norm_num) using 1 <;> ring

lemma not_accepted_both_left {a b e q : ℝ} (ha : 0<a) (ha1 : a≤1)
    (hab : 2*a≤b) (he : 0<e) (he4 : e≤1/4) :
    ¬ (Accepted a e q ∧ Accepted b e q) := by
  intro h
  have hq := accepted_range ha.le ha1 he he4 h.1
  have ha' := (accepted_iff_bounds he he4).1 h.1
  have hb' := (accepted_iff_bounds he he4).1 h.2
  have hw := left_width he he4 hq.1
  nlinarith

lemma not_accepted_both_right {a b e q : ℝ} (ha : 0<a) (ha1 : a≤1)
    (hab : 2*a≤b) (he : 0<e) (he4 : e≤1/4) :
    ¬ (Accepted (1-a) e q ∧ Accepted (1-b) e q) := by
  intro h
  have hq := accepted_range (by linarith : 0≤1-a) (by linarith : 1-a≤1) he he4 h.1
  have ha' := (accepted_iff_bounds he he4).1 h.1
  have hb' := (accepted_iff_bounds he he4).1 h.2
  have hw := right_width he he4 hq.2
  nlinarith

lemma measurableSet_accepted (e q : ℝ) : MeasurableSet {a : ℝ | Accepted a e q} := by
  change MeasurableSet ({a : ℝ | D0 a e q ≤ 0} ∩ {a : ℝ | D1 a e q ≤ 0})
  apply MeasurableSet.inter
  · exact measurableSet_le (by unfold D0; fun_prop) measurable_const
  · exact measurableSet_le (by unfold D1; fun_prop) measurable_const

def failureIndicator (e q a : ℝ) : ℝ≥0∞ := by
  classical
  exact if Accepted a e q then 0 else 1

def weightedFailure (μ : Measure ℝ) (w : ℝ → ℝ≥0∞) (e q : ℝ) : ℝ≥0∞ :=
  ∫⁻ a, w a * failureIndicator e q a ∂μ

lemma misses_one_of_pairwise_separation (C D : Set ℝ) (e q : ℝ)
    (hsep : ∀ a ∈ C, ∀ b ∈ D, ¬ (Accepted a e q ∧ Accepted b e q)) :
    (∀ a ∈ C, ¬ Accepted a e q) ∨ (∀ b ∈ D, ¬ Accepted b e q) := by
  classical
  by_cases h : ∃ a ∈ C, Accepted a e q
  · obtain ⟨a,ha,hacc⟩ := h
    right
    intro b hb hbacc
    exact hsep a ha b hb ⟨hacc,hbacc⟩
  · left
    intro a ha hacc
    exact h ⟨a,ha,hacc⟩

lemma weightedFailure_lower_of_missed_set (μ : Measure ℝ) (w : ℝ → ℝ≥0∞)
    (e q : ℝ) (c : ℝ≥0∞) (C : Set ℝ) (hC : MeasurableSet C)
    (hmiss : ∀ a ∈ C, ¬ Accepted a e q) (hw : ∀ a ∈ C, c ≤ w a) :
    c * μ C ≤ weightedFailure μ w e q := by
  calc
    c * μ C = ∫⁻ a, C.indicator (fun _ => c) a ∂μ := by
      rw [lintegral_indicator hC]
      simp
    _ ≤ weightedFailure μ w e q := by
      apply lintegral_mono
      intro a
      by_cases ha : a ∈ C
      · simpa [Set.indicator_of_mem ha, failureIndicator, hmiss a ha] using hw a ha
      · simp [Set.indicator_of_not_mem ha]

lemma weightedFailure_lower_two_sets (μ : Measure ℝ) (w : ℝ → ℝ≥0∞)
    (e q : ℝ) (c : ℝ≥0∞) (C D : Set ℝ)
    (hC : MeasurableSet C) (hD : MeasurableSet D)
    (hsep : ∀ a ∈ C, ∀ b ∈ D, ¬ (Accepted a e q ∧ Accepted b e q))
    (hw : ∀ a ∈ C ∪ D, c ≤ w a) :
    c * min (μ C) (μ D) ≤ weightedFailure μ w e q := by
  rcases misses_one_of_pairwise_separation C D e q hsep with hmiss | hmiss
  · exact (mul_le_mul_left' (min_le_left _ _) c).trans
      (weightedFailure_lower_of_missed_set μ w e q c C hC hmiss
        (fun a ha => hw a (Or.inl ha)))
  · exact (mul_le_mul_left' (min_le_right _ _) c).trans
      (weightedFailure_lower_of_missed_set μ w e q c D hD hmiss
        (fun a ha => hw a (Or.inr ha)))

/-- Every real report incurs missing mass on one full left annulus. -/
theorem left_annular_lower (μ : Measure ℝ) (w : ℝ → ℝ≥0∞) (e q x : ℝ)
    (c : ℝ≥0∞) (he : 0<e) (he4 : e≤1/4) (hx : 0<x) (hx8 : 8*x≤1)
    (hw : ∀ a ∈ Ioc x (2*x) ∪ Ioc (4*x) (8*x), c ≤ w a) :
    c * min (μ (Ioc x (2*x))) (μ (Ioc (4*x) (8*x))) ≤ weightedFailure μ w e q := by
  apply weightedFailure_lower_two_sets μ w e q c _ _ measurableSet_Ioc measurableSet_Ioc _ hw
  intro a ha b hb
  apply not_accepted_both_left (by linarith [ha.1]) (by linarith [ha.2])
    (by linarith [ha.2,hb.1]) he he4

/-- The reflected annuli have independently checked 9/5 geometry. -/
theorem right_annular_lower (μ : Measure ℝ) (w : ℝ → ℝ≥0∞) (e q x : ℝ)
    (c : ℝ≥0∞) (he : 0<e) (he4 : e≤1/4) (hx : 0<x) (hx8 : 8*x≤1)
    (hw : ∀ a ∈ Ico (1-2*x) (1-x) ∪ Ico (1-8*x) (1-4*x), c ≤ w a) :
    c * min (μ (Ico (1-2*x) (1-x))) (μ (Ico (1-8*x) (1-4*x))) ≤
      weightedFailure μ w e q := by
  apply weightedFailure_lower_two_sets μ w e q c _ _ measurableSet_Ico measurableSet_Ico _ hw
  intro a ha b hb
  have h := not_accepted_both_right (a:=1-a) (b:=1-b)
    (by linarith [ha.2]) (by linarith [ha.1]) (by linarith [ha.1,hb.2]) he he4 (q:=q)
  simpa using h

/-- Independent seed mixing preserves the same unnormalized annular lower bound.
This is an iterated integral inequality, not an assumed all-policy risk theorem. -/
theorem seed_averaged_left_annular_lower {Z : Type*} [MeasurableSpace Z]
    (η : Measure Z) [IsProbabilityMeasure η] (report : Z → ℝ)
    (μ : Measure ℝ) (w : ℝ → ℝ≥0∞) (e x : ℝ) (c : ℝ≥0∞)
    (he : 0<e) (he4 : e≤1/4) (hx : 0<x) (hx8 : 8*x≤1)
    (hw : ∀ a ∈ Ioc x (2*x) ∪ Ioc (4*x) (8*x), c ≤ w a) :
    c * min (μ (Ioc x (2*x))) (μ (Ioc (4*x) (8*x))) ≤
      ∫⁻ z, weightedFailure μ w e (report z) ∂η := by
  calc
    _ = ∫⁻ _z : Z, c * min (μ (Ioc x (2*x))) (μ (Ioc (4*x) (8*x))) ∂η := by simp
    _ ≤ _ := lintegral_mono (fun z => left_annular_lower μ w e (report z) x c he he4 hx hx8 hw)

lemma growth_left_annulus (μ : Measure ℝ) [IsFiniteMeasure μ] (x : ℝ) (hx : 0<x)
    (η : ℝ≥0∞) (hg : (1+η)*μ (Ioc 0 x) ≤ μ (Ioc 0 (2*x))) :
    η*μ (Ioc 0 x) ≤ μ (Ioc x (2*x)) := by
  have hd : Disjoint (Ioc (0:ℝ) x) (Ioc x (2*x)) := by
    apply Set.disjoint_left.mpr
    intro a ha hb
    exact (not_lt_of_ge ha.2) hb.1
  have hμ := measure_union (μ:=μ) hd measurableSet_Ioc
  rw [Ioc_union_Ioc_eq_Ioc hx.le (by linarith)] at hμ
  rw [hμ,add_mul,one_mul] at hg
  exact ENNReal.le_of_add_le_add_left (ne_of_lt (measure_lt_top μ _)) hg

lemma growth_right_annulus (μ : Measure ℝ) [IsFiniteMeasure μ] (x : ℝ) (hx : 0<x)
    (η : ℝ≥0∞) (hg : (1+η)*μ (Ico (1-x) 1) ≤ μ (Ico (1-2*x) 1)) :
    η*μ (Ico (1-x) 1) ≤ μ (Ico (1-2*x) (1-x)) := by
  have hd : Disjoint (Ico (1-2*x) (1-x)) (Ico (1-x) (1:ℝ)) := by
    apply Set.disjoint_left.mpr
    intro a ha hb
    exact (not_lt_of_ge hb.1) ha.2
  have hμ := measure_union (μ:=μ) hd measurableSet_Ico
  rw [Ico_union_Ico_eq_Ico (by linarith) (by linarith)] at hμ
  rw [hμ,add_mul,one_mul,add_comm (μ (Ico (1-2*x) (1-x)))] at hg
  exact ENNReal.le_of_add_le_add_left (ne_of_lt (measure_lt_top μ _)) hg

/-- Lower growth at two separated scales supplies the actual left cumulative mass. -/
theorem left_growth_weighted_lower (μ : Measure ℝ) [IsFiniteMeasure μ]
    (w : ℝ → ℝ≥0∞) (e q x : ℝ) (c η : ℝ≥0∞)
    (he : 0<e) (he4 : e≤1/4) (hx : 0<x) (hx8 : 8*x≤1)
    (hg : (1+η)*μ (Ioc 0 x) ≤ μ (Ioc 0 (2*x)))
    (hg4 : (1+η)*μ (Ioc 0 (4*x)) ≤ μ (Ioc 0 (8*x)))
    (hw : ∀ a ∈ Ioc x (2*x) ∪ Ioc (4*x) (8*x), c ≤ w a) :
    c*(η*μ (Ioc 0 x)) ≤ weightedFailure μ w e q := by
  have h24 : 2*(4*x) = 8*x := by ring
  have hI := growth_left_annulus μ x hx η hg
  have hJ := growth_left_annulus μ (4*x) (by positivity) η (by simpa only [h24] using hg4)
  have hmono : μ (Ioc (0:ℝ) x) ≤ μ (Ioc 0 (4*x)) := by
    apply measure_mono
    intro a ha
    exact ⟨ha.1, by linarith [ha.2]⟩
  have hmin : η*μ (Ioc 0 x) ≤ min (μ (Ioc x (2*x))) (μ (Ioc (4*x) (8*x))) := by
    apply le_min hI
    exact (mul_le_mul_left' hmono η).trans (by simpa only [h24] using hJ)
  exact (mul_le_mul_left' hmin c).trans (left_annular_lower μ w e q x c he he4 hx hx8 hw)

/-- Right lower growth uses the reflected intervals and its separate 9/5 proof. -/
theorem right_growth_weighted_lower (μ : Measure ℝ) [IsFiniteMeasure μ]
    (w : ℝ → ℝ≥0∞) (e q x : ℝ) (c η : ℝ≥0∞)
    (he : 0<e) (he4 : e≤1/4) (hx : 0<x) (hx8 : 8*x≤1)
    (hg : (1+η)*μ (Ico (1-x) 1) ≤ μ (Ico (1-2*x) 1))
    (hg4 : (1+η)*μ (Ico (1-4*x) 1) ≤ μ (Ico (1-8*x) 1))
    (hw : ∀ a ∈ Ico (1-2*x) (1-x) ∪ Ico (1-8*x) (1-4*x), c ≤ w a) :
    c*(η*μ (Ico (1-x) 1)) ≤ weightedFailure μ w e q := by
  have h24 : 2*(4*x) = 8*x := by ring
  have hI := growth_right_annulus μ x hx η hg
  have hJ := growth_right_annulus μ (4*x) (by positivity) η (by simpa only [h24] using hg4)
  have hmono : μ (Ico (1-x) (1:ℝ)) ≤ μ (Ico (1-4*x) 1) := by
    apply measure_mono
    intro a ha
    exact ⟨by linarith [ha.1],ha.2⟩
  have hmin : η*μ (Ico (1-x) 1) ≤
      min (μ (Ico (1-2*x) (1-x))) (μ (Ico (1-8*x) (1-4*x))) := by
    apply le_min hI
    exact (mul_le_mul_left' hmono η).trans (by simpa only [h24] using hJ)
  exact (mul_le_mul_left' hmin c).trans (right_annular_lower μ w e q x c he he4 hx hx8 hw)

lemma log_one_sub_lower {a : ℝ} (ha : 0≤a) (ha2 : a≤1/2) :
    -2*a ≤ Real.log (1-a) := by
  have hp : 0<1-a := by linarith
  have hl := Real.one_sub_inv_le_log_of_pos hp
  have haux : -2*a ≤ 1-(1-a)⁻¹ := by
    apply (mul_le_mul_right hp).mp
    rw [sub_mul,one_mul,inv_mul_cancel₀ (ne_of_gt hp)]
    nlinarith [mul_nonneg ha (show 0≤1-2*a by linarith)]
  exact haux.trans hl

/-- A genuine Bernoulli extreme-prefix likelihood inequality at deterministic n. -/
lemma zero_prefix_lower {a : ℝ} (ha : 0≤a) (ha2 : a≤1/2) (n : ℕ)
    (hna : (n:ℝ)*a≤8) : Real.exp (-16) ≤ (1-a)^n := by
  have hp : 0<1-a := by linarith
  have hexp : (1-a)^n = Real.exp ((n:ℝ)*Real.log (1-a)) := by
    rw [Real.exp_nat_mul,Real.exp_log hp]
  rw [hexp]
  apply Real.exp_le_exp.mpr
  have h := mul_le_mul_of_nonneg_left (log_one_sub_lower ha ha2)
    (Nat.cast_nonneg n : (0:ℝ)≤n)
  nlinarith

/-- Lower-growth mass forces error on the all-zero prefix, for every report. -/
theorem zero_prefix_growth_lower (μ : Measure ℝ) [IsFiniteMeasure μ]
    (e q x : ℝ) (η : ℝ≥0∞) (n : ℕ)
    (he : 0<e) (he4 : e≤1/4) (hx : 0<x) (hx16 : x≤1/16)
    (hnx : (n:ℝ)*x≤1)
    (hg : (1+η)*μ (Ioc 0 x) ≤ μ (Ioc 0 (2*x)))
    (hg4 : (1+η)*μ (Ioc 0 (4*x)) ≤ μ (Ioc 0 (8*x))) :
    ENNReal.ofReal (Real.exp (-16))*(η*μ (Ioc 0 x)) ≤
      weightedFailure μ (fun a => ENNReal.ofReal ((1-a)^n)) e q := by
  apply left_growth_weighted_lower μ _ e q x _ η he he4 hx (by linarith) hg hg4
  intro a ha
  have ha0 : 0≤a := by rcases ha with h|h <;> linarith [h.1]
  have ha8 : a≤8*x := by rcases ha with h|h <;> linarith [h.2]
  have hna := mul_le_mul_of_nonneg_left ha8 (Nat.cast_nonneg n : (0:ℝ)≤n)
  exact ENNReal.ofReal_le_ofReal (zero_prefix_lower ha0 (by linarith) n (by nlinarith))

/-- The all-one prefix has the reflected lower bound with the independent right geometry. -/
theorem one_prefix_growth_lower (μ : Measure ℝ) [IsFiniteMeasure μ]
    (e q x : ℝ) (η : ℝ≥0∞) (n : ℕ)
    (he : 0<e) (he4 : e≤1/4) (hx : 0<x) (hx16 : x≤1/16)
    (hnx : (n:ℝ)*x≤1)
    (hg : (1+η)*μ (Ico (1-x) 1) ≤ μ (Ico (1-2*x) 1))
    (hg4 : (1+η)*μ (Ico (1-4*x) 1) ≤ μ (Ico (1-8*x) 1)) :
    ENNReal.ofReal (Real.exp (-16))*(η*μ (Ico (1-x) 1)) ≤
      weightedFailure μ (fun a => ENNReal.ofReal (a^n)) e q := by
  apply right_growth_weighted_lower μ _ e q x _ η he he4 hx (by linarith) hg hg4
  intro a ha
  have ha0 : 0≤1-a := by rcases ha with h|h <;> linarith [h.2]
  have ha8 : 1-a≤8*x := by rcases ha with h|h <;> linarith [h.1]
  have hna := mul_le_mul_of_nonneg_left ha8 (Nat.cast_nonneg n : (0:ℝ)≤n)
  have h := zero_prefix_lower ha0 (by linarith) n (by nlinarith)
  apply ENNReal.ofReal_le_ofReal
  simpa using h

/-- Arbitrary randomized reports preserve both extreme-prefix lower bounds.
The seed law is a probability measure independent of the parameter in this explicit
iterated-integral formulation. No report measurability is needed for this inequality. -/
theorem seed_averaged_two_prefix_growth_lower {Z : Type*} [MeasurableSpace Z]
    (ν : Measure Z) [IsProbabilityMeasure ν] (report0 report1 : Z → ℝ)
    (μ : Measure ℝ) [IsFiniteMeasure μ] (e x : ℝ) (η0 η1 : ℝ≥0∞) (n : ℕ)
    (he : 0<e) (he4 : e≤1/4) (hx : 0<x) (hx16 : x≤1/16)
    (hnx : (n:ℝ)*x≤1)
    (hg0 : (1+η0)*μ (Ioc 0 x) ≤ μ (Ioc 0 (2*x)))
    (hg04 : (1+η0)*μ (Ioc 0 (4*x)) ≤ μ (Ioc 0 (8*x)))
    (hg1 : (1+η1)*μ (Ico (1-x) 1) ≤ μ (Ico (1-2*x) 1))
    (hg14 : (1+η1)*μ (Ico (1-4*x) 1) ≤ μ (Ico (1-8*x) 1)) :
    ENNReal.ofReal (Real.exp (-16)) *
      (η0*μ (Ioc 0 x) + η1*μ (Ico (1-x) 1)) ≤
    (∫⁻ z, weightedFailure μ (fun a => ENNReal.ofReal ((1-a)^n)) e (report0 z) ∂ν) +
    (∫⁻ z, weightedFailure μ (fun a => ENNReal.ofReal (a^n)) e (report1 z) ∂ν) := by
  have h0 : ENNReal.ofReal (Real.exp (-16))*(η0*μ (Ioc 0 x)) ≤
      ∫⁻ z, weightedFailure μ (fun a => ENNReal.ofReal ((1-a)^n)) e (report0 z) ∂ν := by
    calc
      _ = ∫⁻ _z : Z, ENNReal.ofReal (Real.exp (-16))*(η0*μ (Ioc 0 x)) ∂ν := by simp
      _ ≤ _ := lintegral_mono (fun z => zero_prefix_growth_lower μ e (report0 z) x η0 n
        he he4 hx hx16 hnx hg0 hg04)
  have h1 : ENNReal.ofReal (Real.exp (-16))*(η1*μ (Ico (1-x) 1)) ≤
      ∫⁻ z, weightedFailure μ (fun a => ENNReal.ofReal (a^n)) e (report1 z) ∂ν := by
    calc
      _ = ∫⁻ _z : Z, ENNReal.ofReal (Real.exp (-16))*(η1*μ (Ico (1-x) 1)) ∂ν := by simp
      _ ≤ _ := lintegral_mono (fun z => one_prefix_growth_lower μ e (report1 z) x η1 n
        he he4 hx hx16 hnx hg1 hg14)
  simpa only [mul_add] using add_le_add h0 h1

end
end AnnularLiteral
