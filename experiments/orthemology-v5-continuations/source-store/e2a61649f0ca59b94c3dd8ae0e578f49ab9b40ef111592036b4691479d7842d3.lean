import Mathlib

/-! Real measures, exact reciprocal counts, and the punctured-endpoint moment hinge.
This is a new author extension, separate from the frozen ordinary review.
-/
namespace EndpointMoment
noncomputable section
open MeasureTheory Set Filter
open scoped ENNReal

lemma reciprocal_threshold_iff {a : ℝ} (ha : 0 < a) (n : ℕ) :
    a ≤ ((n + 1 : ℕ) : ℝ)⁻¹ ↔ n < Nat.floor a⁻¹ := by
  have hn : (0 : ℝ) < ((n + 1 : ℕ) : ℝ) := by positivity
  have h : a ≤ ((n + 1 : ℕ) : ℝ)⁻¹ ↔ ((n + 1 : ℕ) : ℝ) ≤ a⁻¹ := by
    simpa only [inv_inv] using (inv_le_inv₀ (inv_pos.mpr ha) hn)
  rw [h, ← Nat.le_floor_iff (inv_nonneg.mpr ha.le)]
  omega

lemma count_reciprocal_thresholds {a : ℝ} (ha : 0 < a) :
    (∑' n : ℕ, (if a ≤ ((n + 1 : ℕ) : ℝ)⁻¹ then (1 : ℝ≥0∞) else 0)) =
      (Nat.floor a⁻¹ : ℝ≥0∞) := by
  simp_rw [reciprocal_threshold_iff ha]
  rw [tsum_eq_sum (s := Finset.range (Nat.floor a⁻¹))]
  · have he : (∑ n ∈ Finset.range (Nat.floor a⁻¹),
          (if n < Nat.floor a⁻¹ then (1 : ℝ≥0∞) else 0)) =
          ∑ _n ∈ Finset.range (Nat.floor a⁻¹), (1 : ℝ≥0∞) := by
      apply Finset.sum_congr rfl
      intro n hn
      simp [Finset.mem_range.mp hn]
    rw [he]
    simp
  · intro n hn
    simp only [Finset.mem_range, not_lt] at hn
    simp [not_lt.mpr hn]

/-- Exact count after any deterministic index offset. Natural subtraction records
that there are no qualifying integers when the reciprocal is below the cutoff. -/
lemma count_reciprocal_thresholds_tail {a : ℝ} (ha : 0 < a) (N : ℕ) :
    (∑' n : ℕ, (if a ≤ ((n + N + 1 : ℕ) : ℝ)⁻¹ then (1 : ℝ≥0∞) else 0)) =
      (Nat.floor a⁻¹ - N : ℕ) := by
  have hc (n : ℕ) : a ≤ ((n + N + 1 : ℕ) : ℝ)⁻¹ ↔ n < Nat.floor a⁻¹ - N := by
    rw [reciprocal_threshold_iff ha]
    omega
  simp_rw [hc]
  rw [tsum_eq_sum (s := Finset.range (Nat.floor a⁻¹ - N))]
  · have he : (∑ n ∈ Finset.range (Nat.floor a⁻¹ - N),
          (if n < Nat.floor a⁻¹ - N then (1 : ℝ≥0∞) else 0)) =
          ∑ _n ∈ Finset.range (Nat.floor a⁻¹ - N), (1 : ℝ≥0∞) := by
      apply Finset.sum_congr rfl
      intro n hn
      simp [Finset.mem_range.mp hn]
    rw [he]
    simp
  · intro n hn
    simp only [Finset.mem_range, not_lt] at hn
    simp [not_lt.mpr hn]

lemma floor_reciprocal_le {a : ℝ} (ha : 0 < a) :
    (Nat.floor a⁻¹ : ℝ≥0∞) ≤ ENNReal.ofReal a⁻¹ := by
  simpa using ENNReal.ofReal_le_ofReal (Nat.floor_le (inv_nonneg.mpr ha.le))

lemma reciprocal_le_twice_floor {a : ℝ} (ha : 0 < a) (ha1 : a ≤ 1) :
    ENNReal.ofReal a⁻¹ ≤ 2 * (Nat.floor a⁻¹ : ℝ≥0∞) := by
  have hOne : (1 : ℝ) ≤ a⁻¹ := (one_le_inv₀ ha).2 ha1
  have hNat : 1 ≤ Nat.floor a⁻¹ := (Nat.one_le_floor_iff _).2 hOne
  have hCast : (1 : ℝ) ≤ (Nat.floor a⁻¹ : ℝ) := by exact_mod_cast hNat
  have hlt := Nat.lt_floor_add_one (a⁻¹)
  have hle : a⁻¹ ≤ 2 * (Nat.floor a⁻¹ : ℝ) := by linarith
  have h := ENNReal.ofReal_le_ofReal hle
  simpa [ENNReal.ofReal_mul] using h

/-- Reciprocal profile for an arbitrary measurable positive distance. -/
def profile {X : Type*} [MeasurableSpace X] (μ : Measure X) (d : X → ℝ) (n : ℕ) : ℝ≥0∞ :=
  μ {x | d x ≤ ((n + 1 : ℕ) : ℝ)⁻¹}

/-- Exact count/integral identity. No density or finiteness of the measure is assumed. -/
theorem tsum_profile_eq_lintegral_floor {X : Type*} [MeasurableSpace X]
    (μ : Measure X) (d : X → ℝ) (hd : Measurable d)
    (hpos : ∀ᵐ x ∂μ, 0 < d x) :
    (∑' n, profile μ d n) = ∫⁻ x, (Nat.floor (d x)⁻¹ : ℝ≥0∞) ∂μ := by
  let f : ℕ → X → ℝ≥0∞ := fun n =>
    {x | d x ≤ ((n + 1 : ℕ) : ℝ)⁻¹}.indicator 1
  have hm (n : ℕ) : MeasurableSet {x | d x ≤ ((n + 1 : ℕ) : ℝ)⁻¹} :=
    measurableSet_le hd measurable_const
  have hf (n : ℕ) : AEMeasurable (f n) μ :=
    (measurable_const.indicator (hm n)).aemeasurable
  calc
    (∑' n, profile μ d n) = ∑' n, ∫⁻ x, f n x ∂μ := by
      apply tsum_congr
      intro n
      exact (lintegral_indicator_one (hm n)).symm
    _ = ∫⁻ x, ∑' n, f n x ∂μ := (lintegral_tsum hf).symm
    _ = ∫⁻ x, (Nat.floor (d x)⁻¹ : ℝ≥0∞) ∂μ := by
      apply lintegral_congr_ae
      filter_upwards [hpos] with x hx
      simpa [f, Set.indicator_apply] using count_reciprocal_thresholds hx

/-- Exact Tonelli identity for the deterministic tail, with no measure-finiteness assumption. -/
theorem tsum_profile_tail_eq_lintegral_floor {X : Type*} [MeasurableSpace X]
    (μ : Measure X) (d : X → ℝ) (hd : Measurable d)
    (hpos : ∀ᵐ x ∂μ, 0 < d x) (N : ℕ) :
    (∑' n, profile μ d (n+N)) =
      ∫⁻ x, ((Nat.floor (d x)⁻¹ - N : ℕ) : ℝ≥0∞) ∂μ := by
  let f : ℕ → X → ℝ≥0∞ := fun n =>
    {x | d x ≤ ((n + N + 1 : ℕ) : ℝ)⁻¹}.indicator 1
  have hm (n : ℕ) : MeasurableSet {x | d x ≤ ((n + N + 1 : ℕ) : ℝ)⁻¹} :=
    measurableSet_le hd measurable_const
  have hf (n : ℕ) : AEMeasurable (f n) μ :=
    (measurable_const.indicator (hm n)).aemeasurable
  calc
    (∑' n, profile μ d (n+N)) = ∑' n, ∫⁻ x, f n x ∂μ := by
      apply tsum_congr
      intro n
      exact (lintegral_indicator_one (hm n)).symm
    _ = ∫⁻ x, ∑' n, f n x ∂μ := (lintegral_tsum hf).symm
    _ = _ := by
      apply lintegral_congr_ae
      filter_upwards [hpos] with x hx
      simpa [f, Set.indicator_apply] using count_reciprocal_thresholds_tail hx N

/-- The moment is bounded by twice the exact reciprocal count integral. -/
theorem reciprocal_moment_le_twice_profile {X : Type*} [MeasurableSpace X]
    (μ : Measure X) (d : X → ℝ) (hd : Measurable d)
    (hpos : ∀ᵐ x ∂μ, 0 < d x ∧ d x ≤ 1) :
    (∫⁻ x, ENNReal.ofReal (d x)⁻¹ ∂μ) ≤ 2 * ∑' n, profile μ d n := by
  rw [tsum_profile_eq_lintegral_floor μ d hd (hpos.mono fun _ h => h.1)]
  calc
    (∫⁻ x, ENNReal.ofReal (d x)⁻¹ ∂μ) ≤
        ∫⁻ x, 2 * (Nat.floor (d x)⁻¹ : ℝ≥0∞) ∂μ := by
      apply lintegral_mono_ae
      filter_upwards [hpos] with x hx
      exact reciprocal_le_twice_floor hx.1 hx.2
    _ = 2 * ∫⁻ x, (Nat.floor (d x)⁻¹ : ℝ≥0∞) ∂μ :=
      lintegral_const_mul' _ _ (by norm_num)

/-- Genuine measure-theoretic inverse-moment finiteness equivalence. -/
theorem tsum_profile_lt_top_iff {X : Type*} [MeasurableSpace X]
    (μ : Measure X) (d : X → ℝ) (hd : Measurable d)
    (hpos : ∀ᵐ x ∂μ, 0 < d x ∧ d x ≤ 1) :
    (∑' n, profile μ d n) < ⊤ ↔ (∫⁻ x, ENNReal.ofReal (d x)⁻¹ ∂μ) < ⊤ := by
  constructor
  · intro h
    exact lt_of_le_of_lt (reciprocal_moment_le_twice_profile μ d hd hpos)
      (ENNReal.mul_lt_top (by norm_num) h)
  · intro h
    rw [tsum_profile_eq_lintegral_floor μ d hd (hpos.mono fun _ h => h.1)]
    apply lt_of_le_of_lt _ h
    apply lintegral_mono_ae
    filter_upwards [hpos] with x hx
    exact floor_reciprocal_le hx.1

/-- Removing finitely many initial indices preserves profile-series finiteness
for finite measures. This uses the actual ENNReal series decomposition. -/
theorem tsum_profile_tail_lt_top_iff {X : Type*} [MeasurableSpace X]
    (μ : Measure X) [IsFiniteMeasure μ] (d : X → ℝ) (hd : Measurable d)
    (hpos : ∀ᵐ x ∂μ, 0 < d x ∧ d x ≤ 1) (N : ℕ) :
    (∑' n, profile μ d (n + N)) < ⊤ ↔
      (∫⁻ x, ENNReal.ofReal (d x)⁻¹ ∂μ) < ⊤ := by
  have he : (∑ n ∈ Finset.range N, profile μ d n) +
      (∑' n, profile μ d (n + N)) = ∑' n, profile μ d n :=
    ENNReal.summable.sum_add_tsum_nat_add'
  have hf : (∑ n ∈ Finset.range N, profile μ d n) < ⊤ := by
    apply ENNReal.sum_lt_top.mpr
    intro n _
    exact measure_lt_top _ _
  rw [← tsum_profile_lt_top_iff μ d hd hpos, ← he, ENNReal.add_lt_top]
  exact ⟨fun h => ⟨hf, h⟩, fun h => h.2⟩

/-- Restricting to the open unit interval excludes both endpoint atoms. -/
def interior (μ : Measure ℝ) : Measure ℝ := μ.restrict (Ioo 0 1)

instance interior_isFiniteMeasure (μ : Measure ℝ) [IsFiniteMeasure μ] :
    IsFiniteMeasure (interior μ) := by
  unfold interior
  infer_instance

def leftMass (μ : Measure ℝ) (n : ℕ) : ℝ≥0∞ := profile (interior μ) id n
def rightMass (μ : Measure ℝ) (n : ℕ) : ℝ≥0∞ :=
  profile (interior μ) (fun x => 1-x) n

/-- At n>=1 (physical denominator n+1>=2), this is the literal punctured
left cumulative mass, including a possible atom exactly at the cutoff. -/
theorem leftMass_eq_Ioc (μ : Measure ℝ) (n : ℕ) (hn : 1 ≤ n) :
    leftMass μ n = μ (Ioc 0 (((n+1 : ℕ) : ℝ)⁻¹)) := by
  change (μ.restrict (Ioo 0 1)) (Iic (((n+1 : ℕ) : ℝ)⁻¹)) = _
  rw [Measure.restrict_apply measurableSet_Iic]
  congr 1
  ext x
  have hc : (((n+1 : ℕ) : ℝ)⁻¹) < 1 := by
    apply (inv_lt_one₀ (by positivity : (0:ℝ) < ((n+1 : ℕ):ℝ))).2
    exact_mod_cast (show 1 < n+1 by omega)
  simp only [mem_inter_iff, mem_Iic, mem_Ioo, mem_Ioc]
  constructor
  · intro h
    exact ⟨h.2.1,h.1⟩
  · intro h
    exact ⟨h.2,h.1,h.2.trans_lt hc⟩

/-- The reflected cumulative mass has its own correctly oriented half-open interval. -/
theorem rightMass_eq_Ico (μ : Measure ℝ) (n : ℕ) (hn : 1 ≤ n) :
    rightMass μ n = μ (Ico (1-(((n+1 : ℕ) : ℝ)⁻¹)) 1) := by
  unfold rightMass profile interior
  rw [Measure.restrict_apply (measurableSet_le (by fun_prop) measurable_const)]
  congr 1
  ext x
  have hc : (((n+1 : ℕ) : ℝ)⁻¹) < 1 := by
    apply (inv_lt_one₀ (by positivity : (0:ℝ) < ((n+1 : ℕ):ℝ))).2
    exact_mod_cast (show 1 < n+1 by omega)
  simp only [mem_inter_iff, mem_setOf_eq, mem_Ioo, mem_Ico]
  constructor <;> intro h
  · exact ⟨by linarith [h.1],h.2.2⟩
  · exact ⟨by linarith [h.1],by linarith [h.1],h.2⟩

def leftMoment (μ : Measure ℝ) : ℝ≥0∞ :=
  ∫⁻ x, ENNReal.ofReal x⁻¹ ∂interior μ
def rightMoment (μ : Measure ℝ) : ℝ≥0∞ :=
  ∫⁻ x, ENNReal.ofReal (1-x)⁻¹ ∂interior μ
def inverseVarianceMoment (μ : Measure ℝ) : ℝ≥0∞ :=
  ∫⁻ x, ENNReal.ofReal (x*(1-x))⁻¹ ∂interior μ

lemma ae_interior (μ : Measure ℝ) : ∀ᵐ x ∂interior μ, 0 < x ∧ x < 1 :=
  ae_restrict_mem measurableSet_Ioo

lemma ae_left_distance (μ : Measure ℝ) : ∀ᵐ x ∂interior μ, 0 < x ∧ x ≤ 1 :=
  (ae_interior μ).mono fun _ h => ⟨h.1, h.2.le⟩

lemma ae_right_distance (μ : Measure ℝ) :
    ∀ᵐ x ∂interior μ, 0 < 1-x ∧ 1-x ≤ 1 := by
  filter_upwards [ae_interior μ] with x hx
  constructor <;> linarith [hx.1,hx.2]

/-- Both endpoint count identities use the same arbitrary Borel measure. -/
theorem left_count_integral (μ : Measure ℝ) :
    (∑' n, leftMass μ n) = ∫⁻ x, (Nat.floor x⁻¹ : ℝ≥0∞) ∂interior μ :=
  tsum_profile_eq_lintegral_floor _ _ measurable_id ((ae_interior μ).mono fun _ h => h.1)

theorem right_count_integral (μ : Measure ℝ) :
    (∑' n, rightMass μ n) = ∫⁻ x, (Nat.floor (1-x)⁻¹ : ℝ≥0∞) ∂interior μ :=
  tsum_profile_eq_lintegral_floor _ _ (by fun_prop) ((ae_right_distance μ).mono fun _ h => h.1)

theorem inverseVarianceMoment_eq (μ : Measure ℝ) :
    inverseVarianceMoment μ = leftMoment μ + rightMoment μ := by
  unfold inverseVarianceMoment leftMoment rightMoment
  calc
    (∫⁻ x, ENNReal.ofReal (x*(1-x))⁻¹ ∂interior μ) =
        ∫⁻ x, ENNReal.ofReal x⁻¹ + ENNReal.ofReal (1-x)⁻¹ ∂interior μ := by
      apply lintegral_congr_ae
      filter_upwards [ae_interior μ] with x hx
      have hp : 0 < 1-x := by linarith [hx.2]
      have he : (x*(1-x))⁻¹ = x⁻¹ + (1-x)⁻¹ := by
        field_simp [ne_of_gt hx.1, ne_of_gt hp]
      rw [he, ENNReal.ofReal_add (inv_nonneg.mpr hx.1.le) (inv_nonneg.mpr hp.le)]
    _ = _ := lintegral_add_left (by fun_prop) _

/-- The full two-sided moment hinge, with endpoint atoms excluded by restriction. -/
theorem endpoint_series_lt_top_iff (μ : Measure ℝ) :
    (∑' n, (leftMass μ n + rightMass μ n)) < ⊤ ↔
      inverseVarianceMoment μ < ⊤ := by
  rw [ENNReal.tsum_add, ENNReal.add_lt_top, inverseVarianceMoment_eq, ENNReal.add_lt_top]
  exact and_congr
    (tsum_profile_lt_top_iff _ _ measurable_id (ae_left_distance μ))
    (tsum_profile_lt_top_iff _ _ (by fun_prop) (ae_right_distance μ))

/-- Arbitrary deterministic finite cutoffs are harmless for a finite prior. -/
theorem endpoint_tail_series_lt_top_iff (μ : Measure ℝ) [IsFiniteMeasure μ] (N : ℕ) :
    (∑' n, (leftMass μ (n+N) + rightMass μ (n+N))) < ⊤ ↔
      inverseVarianceMoment μ < ⊤ := by
  rw [ENNReal.tsum_add, ENNReal.add_lt_top, inverseVarianceMoment_eq, ENNReal.add_lt_top]
  exact and_congr
    (tsum_profile_tail_lt_top_iff _ _ measurable_id (ae_left_distance μ) N)
    (tsum_profile_tail_lt_top_iff _ _ (by fun_prop) (ae_right_distance μ) N)

/-- Adding arbitrary endpoint atoms does not change the restricted measure. -/
theorem interior_add_endpoint_atoms (μ : Measure ℝ) (a b : ℝ≥0∞) :
    interior (μ + a • Measure.dirac 0 + b • Measure.dirac 1) = interior μ := by
  simp [interior, Measure.restrict_add, Measure.restrict_smul, restrict_dirac]

end
end EndpointMoment
