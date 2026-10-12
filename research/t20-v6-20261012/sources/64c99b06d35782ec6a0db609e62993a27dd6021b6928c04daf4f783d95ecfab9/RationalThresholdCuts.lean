import MembershipMatrixComputable

/-! Exact rational cuts of the unchanged numeric observer's atomic mass.
These are upper normal forms, not new lower reductions or a library hierarchy
completeness theorem. All original definitions and source bytes are retained. -/
open Set MeasureTheory
open scoped ENNReal NNReal
namespace AtomicMembership.RationalThreshold
open P02A2 P02A2.Q8Measure P02A2.FiniteOutputTable P02.Codec
open P02.Codec.UniformComputability

theorem exists_nnrat_between {a b : ℝ≥0∞} (h : a < b) :
    ∃ q : ℚ≥0, a < (q : ℝ≥0∞) ∧ (q : ℝ≥0∞) < b := by
  obtain ⟨q,hq,ha,hb⟩ := ENNReal.lt_iff_exists_rat_btwn.mp h
  refine ⟨q.toNNRat, ?_, ?_⟩
  · simpa only [nnrat_cast_real, Rat.coe_toNNRat q hq] using ha
  · simpa only [nnrat_cast_real, Rat.coe_toNNRat q hq] using hb

theorem table_mass_bound (e i k : ℕ) (hi : rationalOfCode i < 1)
    (h : ∀ n, membershipMatrix e i k n) :
    (rationalOfCode i : ℝ≥0∞) ≤ mass (outputLaw (evaluateIndex e)) := by
  rw [atomic_mass_formula]
  apply le_trans (le_iInf (fun n => ?_)) (le_iSup (fun k => ⨅ n,
    outputLaw (evaluateIndex e) (heavy (outputLaw (evaluateIndex e)) k n)) k)
  rw [← rational_heavy_mass _ (indexTable e) (indexTable_exact e), nnrat_le_cast]
  exact h n hi

/-- Strict lower cut: one positive rational margin must hold for every horizon. -/
def lowerCutMatrix (q : ℚ≥0) (e i k n : ℕ) : Prop :=
  q < rationalOfCode i ∧ rationalOfCode i < 1 ∧ membershipMatrix e i k n

/-- Closed lower cut: every strictly smaller rational receives a witness. -/
def upperCutMatrix (q : ℚ≥0) (e i k n : ℕ) : Prop :=
  rationalOfCode i < q → membershipMatrix e i k n

instance (q : ℚ≥0) (e i k n : ℕ) : Decidable (lowerCutMatrix q e i k n) :=
  inferInstanceAs (Decidable (_ ∧ _ ∧ _))
instance (q : ℚ≥0) (e i k n : ℕ) : Decidable (upperCutMatrix q e i k n) :=
  inferInstanceAs (Decidable (_ → _))

theorem numeric_mass_gt (e : ℕ) (q : ℚ≥0) :
    (q : ℝ≥0∞) < mass (outputLaw (evaluateIndex e)) ↔
      ∃ i k, ∀ n, lowerCutMatrix q e i k n := by
  constructor
  · intro h
    obtain ⟨r,hqr,hrm⟩ := exists_nnrat_between h
    have hm1 : mass (outputLaw (evaluateIndex e)) ≤ 1 := by
      simpa using positive_le_total (outputLaw (evaluateIndex e))
    have hr1 : r < 1 := (nnrat_lt_cast r 1).mp (by simpa using hrm.trans_le hm1)
    obtain ⟨i,hi⟩ := rationalOfCode_surjective r
    have hs : (r : ℝ≥0∞) < ⨆ k, ⨅ n,
        outputLaw (evaluateIndex e) (heavy (outputLaw (evaluateIndex e)) k n) := by
      rwa [← atomic_mass_formula]
    obtain ⟨k,hk⟩ := lt_iSup_iff.mp hs
    refine ⟨i,k,fun n => ?_⟩
    refine ⟨by simpa [hi] using (nnrat_lt_cast q r).mp hqr, by simpa [hi] using hr1, ?_⟩
    intro _
    change rationalOfCode i ≤ rationalHeavyMass (indexTable e) k n
    rw [hi, ← nnrat_le_cast, rational_heavy_mass _ _ (indexTable_exact e)]
    exact hk.le.trans (iInf_le _ n)
  · rintro ⟨i,k,h⟩
    exact ((nnrat_lt_cast q _).mpr (h 0).1).trans_le
      (table_mass_bound e i k (h 0).2.1 (fun n => (h n).2.2))

theorem numeric_mass_ge (e : ℕ) (q : ℚ≥0) (hq : q ≤ 1) :
    (q : ℝ≥0∞) ≤ mass (outputLaw (evaluateIndex e)) ↔
      ∀ i, ∃ k, ∀ n, upperCutMatrix q e i k n := by
  constructor
  · intro h i
    by_cases hi : rationalOfCode i < q
    · have hs : (rationalOfCode i : ℝ≥0∞) < ⨆ k, ⨅ n,
          outputLaw (evaluateIndex e) (heavy (outputLaw (evaluateIndex e)) k n) := by
        rw [← atomic_mass_formula]
        exact ((nnrat_lt_cast _ _).mpr hi).trans_le h
      obtain ⟨k,hk⟩ := lt_iSup_iff.mp hs
      refine ⟨k,fun n _ _ => ?_⟩
      change rationalOfCode i ≤ rationalHeavyMass (indexTable e) k n
      rw [← nnrat_le_cast, rational_heavy_mass _ _ (indexTable_exact e)]
      exact hk.le.trans (iInf_le _ n)
    · exact ⟨0,fun _ h => (hi h).elim⟩
  · intro h
    by_contra hn
    obtain ⟨r,hmr,hrq⟩ := exists_nnrat_between (lt_of_not_ge hn)
    obtain ⟨i,hi⟩ := rationalOfCode_surjective r
    have hrq' : rationalOfCode i < q := by
      simpa [hi] using (nnrat_lt_cast r q).mp hrq
    obtain ⟨k,hk⟩ := h i
    have hb := table_mass_bound e i k (hrq'.trans_le hq) (fun n => hk n hrq')
    rw [hi] at hb
    exact (not_le_of_gt hmr) hb

theorem numeric_mass_lt (e : ℕ) (q : ℚ≥0) (hq : q ≤ 1) :
    mass (outputLaw (evaluateIndex e)) < (q : ℝ≥0∞) ↔
      ∃ i, ∀ k, ∃ n, ¬ upperCutMatrix q e i k n := by
  rw [← not_le, numeric_mass_ge e q hq]
  push_neg
  rfl

theorem numeric_mass_le (e : ℕ) (q : ℚ≥0) :
    mass (outputLaw (evaluateIndex e)) ≤ (q : ℝ≥0∞) ↔
      ∀ i k, ∃ n, ¬ lowerCutMatrix q e i k n := by
  rw [← not_lt, numeric_mass_gt]
  push_neg
  rfl

end AtomicMembership.RationalThreshold
