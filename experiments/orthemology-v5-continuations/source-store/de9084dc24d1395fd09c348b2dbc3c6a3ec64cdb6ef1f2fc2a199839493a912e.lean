import ClusterWidthBoundary

namespace CriticalUniform
noncomputable section
open AnnularLiteral

def centreShift (a e : ℝ) : ℝ := e*a*(1-e^2)
def reportShift (a e : ℝ) : ℝ := 2*e^2*a^2
def leftReport (a e : ℝ) : ℝ := 1/2+centreShift a e-reportShift a e
def rightReport (a e : ℝ) : ℝ := 1/2+centreShift a e+reportShift a e
def stripWidth (a e : ℝ) : ℝ := 4*e*a^2

lemma small_control {a e : ℝ} (ha : 0<a) (ha8 : a≤1/8) (he : 0<e) (he16 : e≤1/16) :
    0≤centreShift a e ∧ centreShift a e≤e*a ∧
    (centreShift a e)^2≤e^2*a^2 ∧
    (reportShift a e)^2≤(3/4)*e^2*a^2 ∧
    2*centreShift a e*reportShift a e+(reportShift a e)^2≤e^2*a^2 := by
  let v := e*a
  have hv : 0<v := mul_pos he ha
  have hv128 : v≤1/128 := by
    dsimp [v]
    have h := mul_le_mul he16 ha8 ha.le (by norm_num : (0:ℝ)≤1/16)
    norm_num at h ⊢
    exact h
  have he2 : e^2≤1/256 := by nlinarith
  have hs0 : 0≤centreShift a e := by
    unfold centreShift
    have hf : 0≤1-e^2 := by nlinarith
    positivity
  have hsv : centreShift a e≤v := by
    have h := mul_nonneg hv.le (sq_nonneg e)
    dsimp [v,centreShift] at *
    nlinarith
  have hs2 : (centreShift a e)^2≤v^2 := by nlinarith
  have hv2 : v^2≤1/16384 := by nlinarith
  have hv3 := mul_le_mul_of_nonneg_right hv128 (sq_nonneg v)
  have hv4 := mul_le_mul_of_nonneg_right hv2 (sq_nonneg v)
  have hh : reportShift a e=2*v^2 := by dsimp [reportShift,v];ring
  have hcross := mul_le_mul_of_nonneg_right hsv (show 0≤2*v^2 by positivity)
  refine ⟨hs0,hsv,?_,?_,?_⟩
  · dsimp [v] at hs2
    nlinarith
  · rw [hh]
    have hid : e^2*a^2=v^2 := by dsimp [v];ring
    rw [mul_assoc (3/4:ℝ) (e^2) (a^2),hid]
    nlinarith
  · rw [hh]
    have hid : e^2*a^2=v^2 := by dsimp [v];ring
    rw [hid]
    nlinarith

/-- Exact non-asymptotic endpoint geometry of the two polynomial reports. -/
theorem endpoint_margins {a e : ℝ} (ha : 0<a) (ha8 : a≤1/8)
    (he : 0<e) (he16 : e≤1/16) :
    D0 ((1-e)*a) e (leftReport a e)≤0 ∧
    D1 ((1+e)*a-stripWidth a e) e (leftReport a e)≤0 ∧
    D0 ((1-e)*a+stripWidth a e) e (rightReport a e)≤0 ∧
    D1 ((1+e)*a) e (rightReport a e)≤0 := by
  obtain ⟨hs0,hsv,hs2,hh2,hcross⟩ := small_control ha ha8 he he16
  have hh : 0≤reportShift a e := by unfold reportShift;positivity
  have hsh : 0≤2*centreShift a e*reportShift a e := by positivity
  have hW1 : (15/4)*e^2*a^2≤stripWidth a e*e*(1-e) := by
    have h := mul_nonneg (show 0≤e^2*a^2 by positivity) (show 0≤1/16-e by linarith)
    unfold stripWidth
    nlinarith
  have hW2 : 4*e^2*a^2≤stripWidth a e*e*(1+e) := by
    have h := mul_nonneg (show 0≤e^2*a^2 by positivity) he.le
    unfold stripWidth
    nlinarith
  have h0 : D0 ((1-e)*a) e (leftReport a e)=
      (centreShift a e)^2-reportShift a e-2*centreShift a e*reportShift a e+(reportShift a e)^2 := by
    unfold D0 leftReport centreShift reportShift
    ring
  have h1 : D1 ((1+e)*a-stripWidth a e) e (leftReport a e)=
      (centreShift a e)^2+reportShift a e-2*centreShift a e*reportShift a e+(reportShift a e)^2-
        stripWidth a e*e*(1-e) := by
    unfold D1 leftReport centreShift reportShift stripWidth
    ring
  have h2 : D0 ((1-e)*a+stripWidth a e) e (rightReport a e)=
      (centreShift a e)^2+reportShift a e+2*centreShift a e*reportShift a e+(reportShift a e)^2-
        stripWidth a e*e*(1+e) := by
    unfold D0 rightReport centreShift reportShift stripWidth
    ring
  have h3 : D1 ((1+e)*a) e (rightReport a e)=
      (centreShift a e)^2-reportShift a e+2*centreShift a e*reportShift a e+(reportShift a e)^2 := by
    unfold D1 rightReport centreShift reportShift
    ring
  have hhdef : reportShift a e=2*e^2*a^2 := rfl
  refine ⟨?_,?_,?_,?_⟩
  · rw [h0]
    nlinarith
  · rw [h1]
    nlinarith
  · rw [h2]
    nlinarith
  · rw [h3]
    nlinarith

theorem left_accepts {a e x : ℝ} (ha : 0<a) (ha8 : a≤1/8)
    (he : 0<e) (he16 : e≤1/16)
    (hx : (1-e)*a≤x ∧ x≤(1+e)*a-stripWidth a e) : Accepted x e (leftReport a e) := by
  obtain ⟨h0,h1,h2,h3⟩ := endpoint_margins ha ha8 he he16
  have hm0 := mul_le_mul_of_nonneg_right hx.1 (show 0≤e*(1+e) by positivity)
  have hm1 := mul_le_mul_of_nonneg_right hx.2 (show 0≤e*(1-e) by nlinarith)
  constructor
  · dsimp [D0] at *
    nlinarith
  · dsimp [D1] at *
    nlinarith

theorem right_accepts {a e x : ℝ} (ha : 0<a) (ha8 : a≤1/8)
    (he : 0<e) (he16 : e≤1/16)
    (hx : (1-e)*a+stripWidth a e≤x ∧ x≤(1+e)*a) : Accepted x e (rightReport a e) := by
  obtain ⟨h0,h1,h2,h3⟩ := endpoint_margins ha ha8 he he16
  have hm0 := mul_le_mul_of_nonneg_right hx.1 (show 0≤e*(1+e) by positivity)
  have hm1 := mul_le_mul_of_nonneg_right hx.2 (show 0≤e*(1-e) by nlinarith)
  constructor
  · dsimp [D0] at *
    nlinarith
  · dsimp [D1] at *
    nlinarith

lemma strips_away_from_centre {a e : ℝ} (ha : 0≤a) (ha8 : a≤1/8) (he : 0≤e) :
    (1-e)*a+stripWidth a e≤a-e*a/2 ∧
      a+e*a/2≤(1+e)*a-stripWidth a e := by
  have hsq : a^2≤a/8 := by nlinarith
  have hm := mul_le_mul_of_nonneg_left hsq he
  unfold stripWidth
  constructor <;> nlinarith


lemma reports_coherent {a e : ℝ} (ha : 0<a) (ha8 : a≤1/8) (he : 0<e) (he16 : e≤1/16) :
    (0≤leftReport a e ∧ leftReport a e≤1) ∧
    (0≤rightReport a e ∧ rightReport a e≤1) := by
  have hgap := strips_away_from_centre ha.le ha8 he.le
  have hmul := mul_le_mul he16 ha8 ha.le (by norm_num : (0:ℝ)≤1/16)
  have hl0 : 0≤(1-e)*a := by
    have he1 : 0≤1-e := by linarith
    exact mul_nonneg he1 ha.le
  have hu0 : 0≤(1+e)*a := by positivity
  have hl1 : (1-e)*a≤1 := by nlinarith [mul_nonneg he.le ha.le]
  have hu1 : (1+e)*a≤1 := by nlinarith
  have hleft := left_accepts ha ha8 he he16 (x := (1-e)*a) ⟨le_rfl,by nlinarith [hgap.2]⟩
  have hright := right_accepts ha ha8 he he16 (x := (1+e)*a) ⟨by nlinarith [hgap.1],le_rfl⟩
  have hL := accepted_range hl0 hl1 he (by linarith) hleft
  have hR := accepted_range hu0 hu1 he (by linarith) hright
  constructor <;> constructor <;> linarith

#print axioms reports_coherent
#print axioms endpoint_margins
#print axioms left_accepts
#print axioms right_accepts
#print axioms strips_away_from_centre
end
end CriticalUniform
