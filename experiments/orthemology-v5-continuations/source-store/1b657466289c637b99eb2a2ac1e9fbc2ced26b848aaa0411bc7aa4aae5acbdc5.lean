import ClusterPolicy

namespace ClusterWidthBoundary
noncomputable section
open AnnularLiteral ClusterGeometry

def shiftedCentre (a e d : ℝ) : ℝ := 1/2+e*a*(1-d*e)

/-- The minimax endpoint excess of the shifted common report, exactly. -/
theorem shifted_worst_excess (a e d : ℝ) :
    D0 ((1-d)*a) e (shiftedCentre a e d)=e*a*(d-e+e*a*(1-d*e)^2) ∧
    D1 ((1+d)*a) e (shiftedCentre a e d)=e*a*(d-e+e*a*(1-d*e)^2) := by
  unfold D0 D1 shiftedCentre
  constructor <;> ring

lemma shifted_coherent {a e d : ℝ} (ha : 0≤a) (ha2 : a≤1/2)
    (he : 0≤e) (he4 : e≤1/4) (hd : 0≤d) (hd16 : d≤1/16) :
    0≤shiftedCentre a e d ∧ shiftedCentre a e d≤1 := by
  have hde : d*e≤(1/16:ℝ)*(1/4) := mul_le_mul hd16 he4 he (by norm_num)
  have hdep : 0≤d*e := mul_nonneg hd he
  have hfac : 0≤1-d*e := by linarith
  have hea : e*a≤1/8 := by nlinarith [mul_le_mul he4 ha2 ha (by norm_num : (0:ℝ)≤1/4)]
  have hp : 0≤e*a := mul_nonneg he ha
  have h1 := mul_nonneg hp hfac
  have h2 := mul_nonneg hp hdep
  unfold shiftedCentre
  constructor <;> nlinarith

/-- Every sufficiently small cluster is accepted whenever its width is STRICTLY
below epsilon. The finite head is deliberately left to the empirical policy. -/
theorem shifted_tail_accepts {a e d x : ℝ} (ha : 0<a) (ha2 : a≤1/2)
    (he : 0<e) (he4 : e≤1/4) (hd : 0≤d) (hd16 : d≤1/16)
    (hgap : d<e) (hasmall : a≤(e-d)/(2*e)) (hx : x∈interval a d) :
    Accepted x e (shiftedCentre a e d) := by
  have hde : d*e≤(1/16:ℝ)*(1/4) := mul_le_mul hd16 he4 he.le (by norm_num)
  have hdep : 0≤d*e := mul_nonneg hd he.le
  have hfac : (1-d*e)^2≤1 := by nlinarith
  have hea : 0≤e*a := mul_nonneg he.le ha.le
  have hmul := mul_le_mul_of_nonneg_left hfac hea
  have hasmall' : a*(2*e)≤e-d := (le_div_iff₀ (by positivity : 0<2*e)).mp hasmall
  have hcore : d-e+e*a*(1-d*e)^2≤0 := by nlinarith
  have hw := mul_nonpos_of_nonneg_of_nonpos hea hcore
  have hd0 : D0 ((1-d)*a) e (shiftedCentre a e d)≤0 := by
    rw [(shifted_worst_excess a e d).1]
    exact hw
  have hd1 : D1 ((1+d)*a) e (shiftedCentre a e d)≤0 := by
    rw [(shifted_worst_excess a e d).2]
    exact hw
  obtain ⟨hxl,hxu⟩ := hx
  have h0 := mul_le_mul_of_nonneg_right hxl (show 0≤e*(1+e) by positivity)
  have h1 := mul_le_mul_of_nonneg_right hxu (show 0≤e*(1-e) by nlinarith)
  constructor
  · unfold D0 at *
    nlinarith
  · unfold D1 at *
    nlinarith

/-- Critical equality still forbids a shared accepted report. This exact
quadratic obstruction is stronger than the coarse five-thirds ratio bound. -/
theorem critical_pair_incompatible {a e d q : ℝ} (ha : 0<a)
    (he : 0<e) (he4 : e≤1/4) (hde : e≤d) :
    ¬ (Accepted ((1-d)*a) e q ∧ Accepted ((1+d)*a) e q) := by
  rintro ⟨hlo,hhi⟩
  have h0 := hlo.1
  have h1 := hhi.2
  have hp := mul_nonneg (show 0≤e*a by positivity) (show 0≤d-e by linarith)
  have hid : D0 ((1-d)*a) e q+D1 ((1+d)*a) e q =
      2*(q-1/2)^2+2*e*a*(d-e) := by unfold D0 D1;ring
  have ht : q=1/2 := by nlinarith [sq_nonneg (q-1/2)]
  rw [ht] at h1
  have hbad : 0<((1+d)*a)*e*(1-e) := by
    have hd : 0<d := he.trans_le hde
    have he1 : 0<1-e := by linarith
    positivity
  unfold D1 at h1
  nlinarith

/-- Two narrow positive-width edge strips are pairwise incompatible even at
critical width. This supports an absolutely continuous bad component law. -/
theorem critical_strips_incompatible {a e l u q : ℝ} (ha : 0<a) (ha2 : a≤1/2)
    (he : 0<e) (he4 : e≤1/4)
    (hl : (1-e)*a≤l ∧ l≤(1-e)*a+e*a^2/16)
    (hu : (1+e)*a-e*a^2/16≤u ∧ u≤(1+e)*a) :
    ¬ (Accepted l e q ∧ Accepted u e q) := by
  have hsq : a^2≤a/2 := by nlinarith
  have hmul := mul_le_mul_of_nonneg_left hsq he.le
  have hua : a≤u := by
    have hp := mul_nonneg he.le ha.le
    nlinarith [hu.1]
  have hu0 : 0≤u := ha.le.trans hua
  have hu1 : u≤1 := by
    have hprod := mul_le_mul he4 ha2 ha.le (by norm_num : (0:ℝ)≤1/4)
    nlinarith [hu.2]
  rintro ⟨hlq,huq⟩
  have hq := (accepted_range hu0 hu1 he he4 huq).1
  let t : ℝ := q-1/2
  let v : ℝ := e*a
  have ht : 0≤t := by dsimp [t];linarith
  have hv : 0<v := mul_pos he ha
  have huweight : (3/4)*v≤u*e*(1-e) := by
    have h1 := mul_nonneg (show 0≤u-a by linarith) (show 0≤e*(1-e) by nlinarith)
    have h2 := mul_nonneg (show 0≤e*a by positivity) (show 0≤1/4-e by linarith)
    dsimp [v]
    nlinarith
  have hD1 := huq.2
  have htd : t^2-t+u*e*(1-e)≤0 := by
    dsimp [t]
    unfold D1 at hD1
    nlinarith
  have htlower : (3/4)*v≤t := by
    have hle : u*e*(1-e)≤t-t^2 := by linarith only [htd]
    exact huweight.trans (hle.trans (sub_le_self t (sq_nonneg t)))
  have hlow := mul_le_mul_of_nonneg_right hl.2 (show 0≤e*(1+e) by positivity)
  have hhigh := mul_le_mul_of_nonneg_right hu.1 (show 0≤e*(1-e) by nlinarith)
  have hD0 := hlq.1
  have htsq : t^2≤v^2/16 := by
    dsimp [t,v]
    dsimp [D0,D1] at hD0 hD1
    nlinarith
  have hfactor := mul_nonneg (show 0≤t-(3/4)*v by linarith) (show 0≤t+(3/4)*v by linarith)
  nlinarith [sq_pos_of_pos hv]

#print axioms shifted_worst_excess
#print axioms shifted_coherent
#print axioms shifted_tail_accepts
#print axioms critical_pair_incompatible
#print axioms critical_strips_incompatible
end
end ClusterWidthBoundary
