import RobustBinaryRepair

namespace Orthemology.Tranche3

def rationalReport (l u e : ℚ) : ℚ := 1/2+(l+u)/2*e-(u-l)/2*e^2
def rationalValue (l u e : ℚ) : ℚ :=
  (rationalReport l u e)^2-(l*(1/2+e)^2+(1-l)*(1/2)^2)

def RationalValid (l u e : ℚ) : Prop :=
  0 ≤ l ∧ l ≤ u ∧ u ≤ 1 ∧ 0 ≤ e ∧ e ≤ 1/4
instance (l u e : ℚ) : Decidable (RationalValid l u e) :=
  inferInstanceAs (Decidable (0 ≤ l ∧ l ≤ u ∧ u ≤ 1 ∧ 0 ≤ e ∧ e ≤ 1/4))

/-- Executable exact-rational certificate. It does not read a hidden standard. -/
def rationalCertificate (l u e eta : ℚ) : Option ℚ :=
  if RationalValid l u e ∧ rationalValue l u e ≤ eta
  then some (rationalReport l u e) else none

lemma rationalReport_cast (l u e : ℚ) :
    (rationalReport l u e : ℝ) = robustReport l u e := by
  simp only [rationalReport, robustReport]
  push_cast
  ring

lemma rationalValue_cast (l u e : ℚ) :
    (rationalValue l u e : ℝ) = robustValue l u e := by
  simp only [rationalValue, robustValue, excessZero]
  push_cast
  rw [rationalReport_cast]

lemma rationalValid_cast (l u e : ℚ) (h : RationalValid l u e) :
    0 ≤ (l:ℝ) ∧ (l:ℝ) ≤ u ∧ (u:ℝ) ≤ 1 ∧ 0 ≤ (e:ℝ) ∧ (e:ℝ) ≤ 1/4 := by
  rcases h with ⟨h0,h1,h2,h3,h4⟩
  refine ⟨by exact_mod_cast h0, by exact_mod_cast h1, by exact_mod_cast h2,
    by exact_mod_cast h3, ?_⟩
  have hx : (e:ℝ) ≤ ((1/4:ℚ):ℝ) := by exact_mod_cast h4
  norm_num at hx ⊢
  exact hx

/-- Every emitted rational report is sound for the full real interval,
not just for standards on a tested rational grid. -/
theorem rationalCertificate_sound (l u e eta q : ℚ)
    (h : rationalCertificate l u e eta = some q) : RobustGood l u e eta q := by
  unfold rationalCertificate at h
  split_ifs at h with hc
  · have hq : rationalReport l u e = q := Option.some.inj h
    have hv := rationalValid_cast l u e hc.1
    have hb : robustValue l u e ≤ (eta:ℝ) := by
      rw [← rationalValue_cast]
      exact_mod_cast hc.2
    rw [← hq, rationalReport_cast]
    apply (robustGood_iff_endpoints _ _ _ _ _ hv.2.1 hv.2.2.2.1 (by linarith [hv.2.2.2.2])).mpr
    have hm := robustReport_mem _ _ _ hv.1 hv.2.1 hv.2.2.1 hv.2.2.2.1 hv.2.2.2.2
    exact ⟨hm.1.le,hm.2.le,hb,by rw [robust_crossing]; exact hb⟩

/-- Under valid input bounds, rejection exactly means that no coherent real
report can meet the supplied tolerance for every possible real standard. -/
theorem rationalCertificate_reject_iff (l u e eta : ℚ) (hv : RationalValid l u e) :
    rationalCertificate l u e eta = none ↔ ¬ ∃ q : ℝ, RobustGood l u e eta q := by
  have h := rationalValid_cast l u e hv
  rw [robust_repair_exists_iff _ _ _ _ h.1 h.2.1 h.2.2.1 h.2.2.2.1 h.2.2.2.2]
  rw [← rationalValue_cast]
  unfold rationalCertificate
  simp only [hv, true_and]
  split_ifs with hc
  · simp only [reduceCtorEq, false_iff, not_not]
    exact_mod_cast hc
  · simp only [true_iff]
    exact_mod_cast hc

end Orthemology.Tranche3

#print axioms Orthemology.Tranche3.rationalCertificate_sound
#print axioms Orthemology.Tranche3.rationalCertificate_reject_iff
#eval Orthemology.Tranche3.rationalCertificate (49/100) (51/100) (1/10) 0
#eval Orthemology.Tranche3.rationalCertificate 0 1 (1/10) 0
