import EndpointAtoms

/-! New sixth-tranche kernels. The actual full cluster classification remains
an ordinary theorem unless explicitly promoted in the qualification record. -/
namespace ClusterGeometry
noncomputable section
open AnnularLiteral Set

def interval (a d : ℝ) : Set ℝ := Icc ((1-d)*a) ((1+d)*a)

def centre (a e : ℝ) : ℝ := 1/2+e*a

lemma centre_D0 (a e x : ℝ) :
    D0 x e (centre a e) = -e^2*a*(1-a)+(a-x)*e*(1+e) := by
  unfold D0 centre
  ring

lemma centre_D1 (a e x : ℝ) :
    D1 x e (centre a e) = -e^2*a*(1-a)+(x-a)*e*(1-e) := by
  unfold D1 centre
  ring

lemma cluster_enclosure {a d x : ℝ} (ha : 0≤a) (hd : d≤1/16)
    (hx : x ∈ interval a d) : 15*a/16≤x ∧ x≤17*a/16 := by
  obtain ⟨hl,hu⟩ := hx
  have h := mul_le_mul_of_nonneg_right hd ha
  constructor <;> nlinarith

lemma centre_margin {a d e x : ℝ} (ha : 0<a) (ha2 : a≤1/2)
    (he : 0<e) (he4 : e≤1/4) (hd : d≤e/4)
    (hx : x ∈ interval a d) :
    D0 x e (centre a e) ≤ -(3/16)*e^2*a ∧
      D1 x e (centre a e) ≤ -(1/4)*e^2*a := by
  obtain ⟨hxl,hxu⟩ := hx
  have hda : d*a≤(e/4)*a := mul_le_mul_of_nonneg_right hd ha.le
  have hlo : a-x≤e*a/4 := by nlinarith
  have hup : x-a≤e*a/4 := by nlinarith
  have hbase : -e^2*a*(1-a)≤-e^2*a/2 := by
    have h := mul_nonneg (show 0≤e^2*a by positivity) (show 0≤1/2-a by linarith)
    nlinarith
  have h0 := mul_le_mul_of_nonneg_right hlo (show 0≤e*(1+e) by positivity)
  have h1 := mul_le_mul_of_nonneg_right hup (show 0≤e*(1-e) by nlinarith)
  have hmul := mul_le_mul_of_nonneg_right he4 (show 0≤e^2*a by positivity)
  constructor
  · rw [centre_D0]
    nlinarith
  · rw [centre_D1]
    have hpos : 0≤e^3*a := by positivity
    nlinarith

/-- Every point of the whole interval, including both boundaries, is accepted. -/
theorem centre_accepts_cluster {a d e x : ℝ} (ha : 0<a) (ha2 : a≤1/2)
    (he : 0<e) (he4 : e≤1/4) (hd : d≤e/4)
    (hx : x ∈ interval a d) : Accepted x e (centre a e) := by
  obtain ⟨h0,h1⟩ := centre_margin ha ha2 he he4 hd hx
  have hp : 0≤e^2*a := by positivity
  exact ⟨by nlinarith,by nlinarith⟩

lemma centre_coherent {a e : ℝ} (ha : 0≤a) (ha2 : a≤1/2)
    (he : 0≤e) (he4 : e≤1/4) : 0≤centre a e ∧ centre a e≤1 := by
  have h := mul_le_mul ha2 he4 he (by norm_num : (0:ℝ)≤1/2)
  have hp : 0≤e*a := mul_nonneg he ha
  unfold centre
  constructor <;> nlinarith

/-- Half-separated centres remain literally incompatible after epsilon/4
relative smoothing. No factor-two separation of the perturbed points is assumed. -/
theorem distinct_cluster_separation {a b d e x y q : ℝ}
    (ha : 0<a) (hb : 0<b) (hb2 : b≤1/2) (hba : 2*b≤a)
    (he : 0<e) (he4 : e≤1/4) (hd : d≤e/4)
    (hx : x ∈ interval b d) (hy : y ∈ interval a d) :
    ¬ (Accepted x e q ∧ Accepted y e q) := by
  have hd16 : d≤1/16 := by linarith
  obtain ⟨hxl,hxu⟩ := cluster_enclosure hb.le hd16 hx
  obtain ⟨hyl,hyu⟩ := cluster_enclosure ha.le hd16 hy
  have hx0 : 0≤x := by nlinarith
  have hx1 : x≤1 := by nlinarith
  rintro ⟨hxq,hyq⟩
  have hq := accepted_range hx0 hx1 he he4 hxq
  have hx' := (accepted_iff_bounds he he4).mp hxq
  have hy' := (accepted_iff_bounds he he4).mp hyq
  have hw := left_width he he4 hq.1
  nlinarith

def boundaryConstant : ℝ := 320/3

def boundary (a r : ℝ) : ℝ :=
  a * min (3/4) (max (3*r/2) (1/(boundaryConstant*Real.log (1/r))))

/-- The clipped logarithmic boundary always remains in the protected gap. -/
theorem boundary_range {a r : ℝ} (ha : 0≤a) (_hr : 0≤r) (hr2 : r≤1/2) :
    (3/2)*(a*r)≤boundary a r ∧ boundary a r≤(3/4)*a := by
  have hlo : 3*r/2 ≤ min (3/4) (max (3*r/2) (1/(boundaryConstant*Real.log (1/r)))) :=
    le_min (by linarith) (le_max_left _ _)
  have hup := min_le_left (3/4 : ℝ) (max (3*r/2) (1/(boundaryConstant*Real.log (1/r))))
  have hl := mul_le_mul_of_nonneg_left hlo ha
  have hu := mul_le_mul_of_nonneg_left hup ha
  unfold boundary
  constructor <;> nlinarith

lemma boundary_pos {a r : ℝ} (ha : 0<a) (hr : 0<r) (hr2 : r≤1/2) :
    0<boundary a r := by
  have h := (boundary_range ha.le hr.le hr2).1
  have hp : 0<(3/2)*(a*r) := by positivity
  exact hp.trans_le h

lemma lower_boundary_relative {a d x b : ℝ} (ha : 0≤a) (hd : d≤1/16)
    (hx : x ∈ interval a d) (hb : b≤(3/4)*a) : b≤(4/5)*x := by
  have h := (cluster_enclosure ha hd hx).1
  nlinarith

lemma upper_boundary_relative {a d x b : ℝ} (ha : 0≤a) (hd : d≤1/16)
    (hx : x ∈ interval a d) (hb : (3/2)*a≤b) : x≤(4/5)*b := by
  have h := (cluster_enclosure ha hd hx).2
  nlinarith

#print axioms centre_margin
#print axioms centre_accepts_cluster
#print axioms centre_coherent
#print axioms distinct_cluster_separation
#print axioms boundary_range
#print axioms boundary_pos
#print axioms lower_boundary_relative
#print axioms upper_boundary_relative
end
end ClusterGeometry
