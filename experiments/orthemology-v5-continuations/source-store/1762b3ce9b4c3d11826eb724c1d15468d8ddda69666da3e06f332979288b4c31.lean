import Mathlib.Tactic

namespace Orthemology.Tranche3
noncomputable section

/-- Excess loss at the first truth vertex, in fixed score units. -/
def excessZero (a e q : ℝ) : ℝ := q^2 - (a*(1/2+e)^2+(1-a)*(1/2)^2)
/-- Excess loss at the second truth vertex. -/
def excessOne (a e q : ℝ) : ℝ := (1-q)^2 - (a*(1/2-e)^2+(1-a)*(1/2)^2)
/-- The same coherent report must work for every supplied possible standard. -/
def RobustGood (l u e eta q : ℝ) : Prop :=
  0 ≤ q ∧ q ≤ 1 ∧ ∀ a, l ≤ a → a ≤ u → excessZero a e q ≤ eta ∧ excessOne a e q ≤ eta

def robustReport (l u e : ℝ) : ℝ := 1/2 + (l+u)/2*e - (u-l)/2*e^2
def robustValue (l u e : ℝ) : ℝ := excessZero l e (robustReport l u e)

lemma excessZero_expand (a e q : ℝ) :
    excessZero a e q = q^2-1/4-a*e*(1+e) := by unfold excessZero; ring
lemma excessOne_expand (a e q : ℝ) :
    excessOne a e q = (1-q)^2-1/4+a*e*(1-e) := by unfold excessOne; ring

/-- Endpoint verification suffices for the entire uncertainty interval. -/
theorem robustGood_iff_endpoints (l u e eta q : ℝ)
    (hlu : l ≤ u) (he0 : 0 ≤ e) (he1 : e ≤ 1) :
    RobustGood l u e eta q ↔
      0 ≤ q ∧ q ≤ 1 ∧ excessZero l e q ≤ eta ∧ excessOne u e q ≤ eta := by
  constructor
  · rintro ⟨hq0,hq1,h⟩
    exact ⟨hq0,hq1,(h l le_rfl hlu).1,(h u hlu le_rfl).2⟩
  · rintro ⟨hq0,hq1,hz,ho⟩
    refine ⟨hq0,hq1,?_⟩
    intro a hla hau
    rw [excessZero_expand] at hz ⊢
    rw [excessOne_expand] at ho ⊢
    have hz' := mul_nonneg (sub_nonneg.mpr hla) (mul_nonneg he0 (by linarith : 0 ≤ 1+e))
    have ho' := mul_nonneg (sub_nonneg.mpr hau) (mul_nonneg he0 (by linarith : 0 ≤ 1-e))
    constructor <;> nlinarith

lemma robustReport_mem (l u e : ℝ) (hl0 : 0 ≤ l) (hlu : l ≤ u)
    (hu1 : u ≤ 1) (he0 : 0 ≤ e) (he1 : e ≤ 1/4) :
    0 < robustReport l u e ∧ robustReport l u e < 1 := by
  have hu0 : 0 ≤ u := hl0.trans hlu
  have hl1 : l ≤ 1 := hlu.trans hu1
  have he : e ≤ 1 := by linarith
  have h1 := mul_nonneg hl0 (mul_nonneg he0 (by linarith : 0 ≤ 1+e))
  have h2 := mul_nonneg hu0 (mul_nonneg he0 (by linarith : 0 ≤ 1-e))
  have h3 := mul_nonneg (sub_nonneg.mpr hl1) he0
  have h4 := mul_nonneg (sub_nonneg.mpr hu1) he0
  have h5 := mul_nonneg (sub_nonneg.mpr hlu) (sq_nonneg e)
  dsimp [robustReport]
  constructor <;> nlinarith

lemma robust_crossing (l u e : ℝ) :
    excessOne u e (robustReport l u e) = robustValue l u e := by
  unfold robustValue excessOne excessZero robustReport
  ring

/-- Exact minimax lower bound, with coherent admissibility explicit. -/
theorem robustValue_le_max (l u e q : ℝ) (hl0 : 0 ≤ l) (hlu : l ≤ u)
    (hu1 : u ≤ 1) (he0 : 0 ≤ e) (he1 : e ≤ 1/4)
    (hq0 : 0 ≤ q) (hq1 : q ≤ 1) :
    robustValue l u e ≤ max (excessZero l e q) (excessOne u e q) := by
  have hs := robustReport_mem l u e hl0 hlu hu1 he0 he1
  rcases le_total (robustReport l u e) q with h | h
  · have hsq : (robustReport l u e)^2 ≤ q^2 := by nlinarith
    have hz : robustValue l u e ≤ excessZero l e q := by
      unfold robustValue excessZero
      linarith
    exact hz.trans (le_max_left _ _)
  · have hsq : (1-robustReport l u e)^2 ≤ (1-q)^2 := by nlinarith
    have ho : robustValue l u e ≤ excessOne u e q := by
      rw [← robust_crossing]
      unfold excessOne
      linarith
    exact ho.trans (le_max_right _ _)

/-- A complete certificate: tolerance is feasible exactly at or above the
explicit minimax value. Negative tolerances mean common strict improvement. -/
theorem robust_repair_exists_iff (l u e eta : ℝ) (hl0 : 0 ≤ l) (hlu : l ≤ u)
    (hu1 : u ≤ 1) (he0 : 0 ≤ e) (he1 : e ≤ 1/4) :
    (∃ q, RobustGood l u e eta q) ↔ robustValue l u e ≤ eta := by
  constructor
  · rintro ⟨q,hq⟩
    have h := (robustGood_iff_endpoints l u e eta q hlu he0 (by linarith)).mp hq
    exact (robustValue_le_max l u e q hl0 hlu hu1 he0 he1 h.1 h.2.1).trans
      (max_le h.2.2.1 h.2.2.2)
  · intro h
    refine ⟨robustReport l u e, ?_⟩
    apply (robustGood_iff_endpoints l u e eta _ hlu he0 (by linarith)).mpr
    have hs := robustReport_mem l u e hl0 hlu hu1 he0 he1
    exact ⟨hs.1.le,hs.2.le,h,by rw [robust_crossing]; exact h⟩

/-- The midpoint and half-width polynomial, in the same fixed score units. -/
theorem robustValue_polynomial (m d e : ℝ) :
    robustValue (m-d) (m+d) e =
      d*e-m*(1-m)*e^2-2*m*d*e^3+d^2*e^4 := by
  unfold robustValue robustReport excessZero
  ring


/-- The crossing is the unique coherent minimax report. -/
theorem robustReport_unique (l u e q : ℝ) (hl0 : 0 ≤ l) (hlu : l ≤ u)
    (hu1 : u ≤ 1) (he0 : 0 ≤ e) (he1 : e ≤ 1/4)
    (hq0 : 0 ≤ q) (hq1 : q ≤ 1)
    (h : max (excessZero l e q) (excessOne u e q) ≤ robustValue l u e) :
    q = robustReport l u e := by
  have hs := robustReport_mem l u e hl0 hlu hu1 he0 he1
  have hz := (le_max_left (excessZero l e q) (excessOne u e q)).trans h
  have ho := (le_max_right (excessZero l e q) (excessOne u e q)).trans h
  have hv := robust_crossing l u e
  unfold robustValue excessZero at hz
  rw [← hv] at ho
  unfold excessOne at ho
  nlinarith

/-- At any selected time, interval coverage and the computable value check
suffice. The choice of time or disturbance may depend on the data. -/
theorem covered_certificate_sound {Ω : Type*} (a : ℝ)
    (lower upper disturbance tolerance : Ω → ℕ → ℝ)
    (covered : ∀ w n, lower w n ≤ a ∧ a ≤ upper w n)
    (valid : ∀ w n, 0 ≤ lower w n ∧ upper w n ≤ 1 ∧
      0 ≤ disturbance w n ∧ disturbance w n ≤ 1/4)
    (w : Ω) (n : ℕ)
    (cert : robustValue (lower w n) (upper w n) (disturbance w n) ≤ tolerance w n) :
    let q := robustReport (lower w n) (upper w n) (disturbance w n)
    0 ≤ q ∧ q ≤ 1 ∧ excessZero a (disturbance w n) q ≤ tolerance w n ∧
      excessOne a (disturbance w n) q ≤ tolerance w n := by
  have hc := covered w n
  have hv := valid w n
  have hg := (robustGood_iff_endpoints (lower w n) (upper w n) (disturbance w n)
    (tolerance w n) (robustReport (lower w n) (upper w n) (disturbance w n))
    (hc.1.trans hc.2) hv.2.2.1 (by linarith [hv.2.2.2])).mpr
    ⟨(robustReport_mem _ _ _ hv.1 (hc.1.trans hc.2) hv.2.1 hv.2.2.1 hv.2.2.2).1.le,
     (robustReport_mem _ _ _ hv.1 (hc.1.trans hc.2) hv.2.1 hv.2.2.1 hv.2.2.2).2.le,
     cert, by rw [robust_crossing]; exact cert⟩
  exact ⟨hg.1,hg.2.1,(hg.2.2 a hc.1 hc.2).1,(hg.2.2 a hc.1 hc.2).2⟩

/-- A convenient sufficient information width. The exact value check remains
sharper and includes the boundary cases. -/
theorem width_sufficient (m d e : ℝ) (hm0 : 0 ≤ m)
    (hd0 : 0 ≤ d) (hdm : d ≤ m) (he0 : 0 ≤ e) (he1 : e ≤ 1/4)
    (hwidth : d ≤ m*(1-m)*e) : robustValue (m-d) (m+d) e ≤ 0 := by
  rw [robustValue_polynomial]
  have hmain := mul_le_mul_of_nonneg_right hwidth he0
  have hde : d*e ≤ m := by nlinarith
  have htail := mul_nonneg (mul_nonneg hd0 (pow_nonneg he0 3))
    (by linarith : 0 ≤ 2*m-d*e)
  nlinarith

/-- Insufficient interval resolution forces positive worst-case regret. -/
theorem robustValue_lower_width (m d e : ℝ) (hm1 : m ≤ 1)
    (hd0 : 0 ≤ d) (he0 : 0 ≤ e) (he1 : e ≤ 1/4) :
    (7/8)*d*e-(1/4)*e^2 ≤ robustValue (m-d) (m+d) e := by
  rw [robustValue_polynomial]
  have hme : m*e^2 ≤ 1/16 := by
    have h := mul_le_mul_of_nonneg_right hm1 (sq_nonneg e)
    nlinarith
  have hx := mul_nonneg (mul_nonneg hd0 he0) (by linarith : 0 ≤ 1/8-2*m*e^2)
  have hy := mul_nonneg (sq_nonneg (m-1/2)) (sq_nonneg e)
  have hz := mul_nonneg (sq_nonneg d) (pow_nonneg he0 4)
  nlinarith

/-- A non-worsening certificate necessarily has half-width O(epsilon). -/
theorem width_necessary (m d e : ℝ) (hm1 : m ≤ 1)
    (hd0 : 0 ≤ d) (he0 : 0 < e) (he1 : e ≤ 1/4)
    (h : robustValue (m-d) (m+d) e ≤ 0) : d ≤ (2/7)*e := by
  have hb := robustValue_lower_width m d e hm1 hd0 he0.le he1
  nlinarith

end
end Orthemology.Tranche3

#print axioms Orthemology.Tranche3.robustGood_iff_endpoints
#print axioms Orthemology.Tranche3.robust_repair_exists_iff
#print axioms Orthemology.Tranche3.robustValue_polynomial

#print axioms Orthemology.Tranche3.robustReport_unique
#print axioms Orthemology.Tranche3.covered_certificate_sound
#print axioms Orthemology.Tranche3.width_sufficient
#print axioms Orthemology.Tranche3.width_necessary
