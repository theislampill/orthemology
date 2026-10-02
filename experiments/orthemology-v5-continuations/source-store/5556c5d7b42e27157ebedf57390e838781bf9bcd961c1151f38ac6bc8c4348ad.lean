import ContaminationAlgebra

/-! A separately scoped successor: the explicit cluster selector is defined on
all finite words and proved causal, coherent, and correct between its boundaries.
It does not take a true parameter or within-cluster distribution as input. -/
namespace ClusterPolicy
noncomputable section
open MeasureTheory Set ClusterGeometry ClusterConcentration EmpiricalGeometry EndpointProcess
open scoped ENNReal

def boundaries (a : ℕ → ℝ) (i : ℕ) : ℝ := boundary (a i) (a (i+1)/a i)

lemma boundaries_range (a : ℕ → ℝ) (hp : ∀ i, 0<a i)
    (hs : ∀ i, a (i+1)≤a i/2) (i : ℕ) :
    (3/2)*a (i+1)≤boundaries a i ∧ boundaries a i≤(3/4)*a i := by
  have hr : a (i+1)/a i≤1/2 := (div_le_iff₀ (hp i)).mpr (by nlinarith [hs i])
  have h := boundary_range (hp i).le (div_nonneg (hp (i+1)).le (hp i).le) hr
  have he : a i*(a (i+1)/a i)=a (i+1) := by field_simp [ne_of_gt (hp i)]
  simpa [boundaries,he] using h

lemma boundaries_pos (a : ℕ → ℝ) (hp : ∀ i, 0<a i)
    (hs : ∀ i, a (i+1)≤a i/2) (i : ℕ) : 0<boundaries a i := by
  have h := (boundaries_range a hp hs i).1
  have hh : 0<(3/2)*a (i+1) := mul_pos (by norm_num) (hp (i+1))
  exact hh.trans_le h

lemma boundaries_half (a : ℕ → ℝ) (hp : ∀ i, 0<a i)
    (hs : ∀ i, a (i+1)≤a i/2) (i : ℕ) : boundaries a (i+1)≤boundaries a i/2 := by
  have h1 := (boundaries_range a hp hs i).1
  have h2 := (boundaries_range a hp hs (i+1)).2
  linarith

lemma boundaries_antitone (a : ℕ → ℝ) (hp : ∀ i, 0<a i)
    (hs : ∀ i, a (i+1)≤a i/2) : Antitone (boundaries a) := by
  apply antitone_nat_of_succ_le
  intro i
  have h1 := boundaries_half a hp hs i
  have h2 := boundaries_pos a hp hs i
  linarith

lemma boundaries_geometric (a : ℕ → ℝ) (hp : ∀ i, 0<a i)
    (hs : ∀ i, a (i+1)≤a i/2) (i : ℕ) : boundaries a i≤boundaries a 0*(1/2:ℝ)^i := by
  induction i with
  | zero => simp
  | succ i ih =>
    have h := boundaries_half a hp hs i
    rw [pow_succ]
    nlinarith

lemma exists_boundary_below (a : ℕ → ℝ) (hp : ∀ i, 0<a i)
    (hs : ∀ i, a (i+1)≤a i/2) {x : ℝ} (hx : 0<x) : ∃ i, boundaries a i<x := by
  have hb := boundaries_pos a hp hs 0
  obtain ⟨i,hi⟩ := exists_pow_lt_of_lt_one (div_pos hx hb) (by norm_num : (1/2:ℝ)<1)
  refine ⟨i,(boundaries_geometric a hp hs i).trans_lt ?_⟩
  have h := (lt_div_iff₀ hb).mp hi
  nlinarith

def selector (a : ℕ → ℝ) (hp : ∀ i, 0<a i) (hs : ∀ i, a (i+1)≤a i/2) (x : ℝ) : ℕ := by
  classical
  exact if hx : 0<x then Nat.find (exists_boundary_below a hp hs hx) else 0

lemma selector_zero_iff (a : ℕ → ℝ) (hp : ∀ i, 0<a i)
    (hs : ∀ i, a (i+1)≤a i/2) {x : ℝ} (hx : 0<x) :
    selector a hp hs x=0 ↔ boundaries a 0<x := by
  classical
  simp [selector,hx,Nat.find_eq_zero]

lemma selector_succ_iff (a : ℕ → ℝ) (hp : ∀ i, 0<a i)
    (hs : ∀ i, a (i+1)≤a i/2) {x : ℝ} (hx : 0<x) (i : ℕ) :
    selector a hp hs x=i+1 ↔ boundaries a (i+1)<x ∧ x≤boundaries a i := by
  classical
  rw [selector,dif_pos hx,Nat.find_eq_iff]
  constructor
  · rintro ⟨h1,h2⟩
    exact ⟨h1,le_of_not_gt (h2 i (by omega))⟩
  · rintro ⟨h1,h2⟩
    refine ⟨h1,?_⟩
    intro j hj hbad
    have hm := boundaries_antitone a hp hs (show j ≤ i by omega)
    linarith

def flooredMean (n : ℕ) (w : Fin n → Bool) : ℝ := max (empiricalMean n w) (1/(n:ℝ))

lemma flooredMean_pos (n : ℕ) (hn : 0<n) (w : Fin n → Bool) : 0<flooredMean n w := by
  have hn' : (0:ℝ)<n := by exact_mod_cast hn
  exact (one_div_pos.mpr hn').trans_le (le_max_right _ _)

def report {Z : Type*} (a : ℕ → ℝ) (hp : ∀ i, 0<a i)
    (hs : ∀ i, a (i+1)≤a i/2) (e : ℝ) : ReportFamily Z :=
  fun n w _z => centre (a (selector a hp hs (flooredMean n w))) e

lemma report_measurable {Z : Type*} [MeasurableSpace Z]
    (a : ℕ → ℝ) (hp : ∀ i, 0<a i) (hs : ∀ i, a (i+1)≤a i/2) (e : ℝ) :
    ∀ n w, Measurable (report (Z := Z) a hp hs e n w) := by
  intro n w
  exact measurable_const

lemma report_coherent {Z : Type*} (a : ℕ → ℝ) (hp : ∀ i, 0<a i)
    (hh : ∀ i, a i≤1/2) (hs : ∀ i, a (i+1)≤a i/2)
    {e : ℝ} (he : 0≤e) (he4 : e≤1/4) :
    ∀ n w z, 0≤report (Z := Z) a hp hs e n w z ∧ report a hp hs e n w z≤1 := by
  intro n w z
  exact centre_coherent (hp _).le (hh _) he he4

lemma correct_cluster_accepted {Z : Type*} (a : ℕ → ℝ) (hp : ∀ i, 0<a i)
    (hh : ∀ i, a i≤1/2) (hs : ∀ i, a (i+1)≤a i/2)
    {e d x : ℝ} (he : 0<e) (he4 : e≤1/4) (hd : d≤e/4)
    (i n : ℕ) (w : Fin n → Bool) (z : Z) (hx : x ∈ interval (a i) d)
    (hi : selector a hp hs (flooredMean n w)=i) :
    AnnularLiteral.Accepted x e (report a hp hs e n w z) := by
  unfold report
  rw [hi]
  exact centre_accepts_cluster (hp i) (hh i) he he4 hd hx

/-- Exact zero-cluster event containment for the constructed shared policy. -/
lemma zero_failure_implies_lower {Z : Type*} (a : ℕ → ℝ) (hp : ∀ i, 0<a i)
    (hh : ∀ i, a i≤1/2) (hs : ∀ i, a (i+1)≤a i/2)
    {e d x : ℝ} (he : 0<e) (he4 : e≤1/4) (hd : d≤e/4)
    (n : ℕ) (hn : 0<n) (w : Fin n → Bool) (z : Z)
    (hx : x ∈ interval (a 0) d)
    (hf : ¬AnnularLiteral.Accepted x e (report a hp hs e n w z)) :
    flooredMean n w≤boundaries a 0 := by
  by_contra h
  have hb : boundaries a 0<flooredMean n w := lt_of_not_ge h
  have hi := (selector_zero_iff a hp hs (flooredMean_pos n hn w)).mpr hb
  exact hf (correct_cluster_accepted a hp hh hs he he4 hd 0 n w z hx hi)

/-- No latent parameter is used to choose the report. The true cluster index
appears only in the external loss-bound theorem. -/
lemma successor_failure_implies_boundary {Z : Type*} (a : ℕ → ℝ) (hp : ∀ i, 0<a i)
    (hh : ∀ i, a i≤1/2) (hs : ∀ i, a (i+1)≤a i/2)
    {e d x : ℝ} (he : 0<e) (he4 : e≤1/4) (hd : d≤e/4)
    (i n : ℕ) (hn : 0<n) (w : Fin n → Bool) (z : Z)
    (hx : x ∈ interval (a (i+1)) d)
    (hf : ¬AnnularLiteral.Accepted x e (report a hp hs e n w z)) :
    boundaries a i<flooredMean n w ∨ flooredMean n w≤boundaries a (i+1) := by
  by_contra h
  push_neg at h
  have hi := (selector_succ_iff a hp hs (flooredMean_pos n hn w) i).mpr ⟨h.2,h.1⟩
  exact hf (correct_cluster_accepted a hp hh hs he he4 hd (i+1) n w z hx hi)

lemma floor_upper_event {n : ℕ} (w : Fin n → Bool) {b : ℝ}
    (hf : 1/(n:ℝ)≤b) (h : b<flooredMean n w) : b<empiricalMean n w := by
  unfold flooredMean at h
  rcases lt_max_iff.mp h with h|h
  · exact h
  · exact False.elim (not_lt_of_ge hf h)

lemma floor_lower_event {n : ℕ} (w : Fin n → Bool) {b : ℝ}
    (h : flooredMean n w≤b) : empiricalMean n w≤b ∧ 1/(n:ℝ)≤b :=
  max_le_iff.mp h


def upperEvent (n : ℕ) (b : ℝ) (w : Fin n → Bool) : ℝ≥0∞ := by
  classical
  exact if b<flooredMean n w then 1 else 0

def lowerEvent (n : ℕ) (b : ℝ) (w : Fin n → Bool) : ℝ≥0∞ := by
  classical
  exact if flooredMean n w≤b then 1 else 0

def upperEnvelope (n : ℕ) (b : ℝ) : ℝ≥0∞ :=
  if b<1/(n:ℝ) then 1 else ENNReal.ofReal (Real.exp (-((n:ℝ)*b/100)))

def lowerEnvelope (n : ℕ) (x b : ℝ) : ℝ≥0∞ :=
  if 1/(n:ℝ)≤b then ENNReal.ofReal (Real.exp (-((n:ℝ)*x/100))) else 0

lemma actual_floored_upper (n : ℕ) (hn : 0<n) {x b : ℝ}
    (hx : 0≤x) (hx1 : x≤1) (hxb : x≤(4/5)*b) :
    (∫⁻ u, upperEvent n b (observedWord n x u) ∂innovationLaw)≤upperEnvelope n b := by
  classical
  unfold upperEnvelope
  split_ifs with h
  · calc
      _ ≤ ∫⁻ _u : Innovations, (1:ℝ≥0∞) ∂innovationLaw := by
        apply lintegral_mono
        intro u
        dsimp only
        unfold upperEvent
        split_ifs <;> simp
      _ = _ := by simp
  · apply le_trans _ (actual_upper_tail_bound n hn hx hx1 hxb)
    apply lintegral_mono
    intro u
    dsimp only
    unfold upperEvent
    split_ifs with he hu
    · rfl
    · have hh := floor_upper_event (observedWord n x u) (le_of_not_gt h) he
      exact False.elim (hu hh.le)
    · simp
    · simp

lemma actual_floored_lower (n : ℕ) (hn : 0<n) {x b : ℝ}
    (hx : 0≤x) (hx1 : x≤1) (hbx : b≤(4/5)*x) :
    (∫⁻ u, lowerEvent n b (observedWord n x u) ∂innovationLaw)≤lowerEnvelope n x b := by
  classical
  unfold lowerEnvelope
  split_ifs with h
  · apply le_trans _ (actual_lower_tail_bound n hn hx hx1 hbx)
    apply lintegral_mono
    intro u
    dsimp only
    unfold lowerEvent
    split_ifs with he hl
    · rfl
    · exact False.elim (hl (floor_lower_event (observedWord n x u) he).1)
    · simp
    · simp
  · have hz : (fun u => lowerEvent n b (observedWord n x u))=(fun _u : Innovations => (0:ℝ≥0∞)) := by
      funext u
      unfold lowerEvent
      split_ifs with he
      · exact False.elim (h (floor_lower_event (observedWord n x u) he).2)
      · rfl
    rw [hz]
    simp

lemma measurable_prefix_function (n : ℕ) (x : ℝ) (f : (Fin n → Bool) → ℝ≥0∞) :
    Measurable (fun u => f (observedWord n x u)) :=
  (measurable_of_finite f).comp ((prefix_measurable n).comp (measurable_const.prodMk measurable_id))

/-- A concrete actual-stream prefix bound for the constructed policy at every
point of a noninitial cluster. No word-law or risk equality is a premise. -/
theorem actual_successor_stage_bound {Z : Type*}
    (a : ℕ → ℝ) (hp : ∀ i, 0<a i) (hh : ∀ i, a i≤1/2)
    (hs : ∀ i, a (i+1)≤a i/2) {e d x : ℝ}
    (he : 0<e) (he4 : e≤1/4) (hd : d≤e/4)
    (i n : ℕ) (hn : 0<n) (z : Z) (hx : x∈interval (a (i+1)) d) :
    (∫⁻ u, AnnularLiteral.failureIndicator e
      (report a hp hs e n (observedWord n x u) z) x ∂innovationLaw) ≤
      upperEnvelope n (boundaries a i)+lowerEnvelope n x (boundaries a (i+1)) := by
  classical
  have hd16 : d≤1/16 := by linarith
  have hxx := cluster_enclosure (hp (i+1)).le hd16 hx
  have hx0 : 0≤x := by nlinarith [hp (i+1)]
  have hx1 : x≤1 := by nlinarith [hh (i+1)]
  have hpoint : ∀ w : Fin n → Bool, AnnularLiteral.failureIndicator e (report a hp hs e n w z) x ≤
      upperEvent n (boundaries a i) w+lowerEvent n (boundaries a (i+1)) w := by
    intro w
    unfold AnnularLiteral.failureIndicator
    split_ifs with hg
    · simp
    · have hbad := successor_failure_implies_boundary a hp hh hs he he4 hd i n hn w z hx hg
      rcases hbad with hbad|hbad
      · simp [upperEvent,hbad]
      · simp [lowerEvent,hbad]
  have hle := lintegral_mono (μ := innovationLaw) (fun u => hpoint (observedWord n x u))
  rw [lintegral_add_left (measurable_prefix_function n x (upperEvent n (boundaries a i)))] at hle
  apply hle.trans
  apply add_le_add
  · apply actual_floored_upper n hn hx0 hx1
    exact upper_boundary_relative (hp (i+1)).le hd16 hx (boundaries_range a hp hs i).1
  · apply actual_floored_lower n hn hx0 hx1
    exact lower_boundary_relative (hp (i+1)).le hd16 hx (boundaries_range a hp hs (i+1)).2

/-- Initial cluster has only the lower-boundary error term. -/
theorem actual_zero_stage_bound {Z : Type*}
    (a : ℕ → ℝ) (hp : ∀ i, 0<a i) (hh : ∀ i, a i≤1/2)
    (hs : ∀ i, a (i+1)≤a i/2) {e d x : ℝ}
    (he : 0<e) (he4 : e≤1/4) (hd : d≤e/4)
    (n : ℕ) (hn : 0<n) (z : Z) (hx : x∈interval (a 0) d) :
    (∫⁻ u, AnnularLiteral.failureIndicator e
      (report a hp hs e n (observedWord n x u) z) x ∂innovationLaw) ≤
      lowerEnvelope n x (boundaries a 0) := by
  classical
  have hd16 : d≤1/16 := by linarith
  have hxx := cluster_enclosure (hp 0).le hd16 hx
  have hx0 : 0≤x := by nlinarith [hp 0]
  have hx1 : x≤1 := by nlinarith [hh 0]
  apply le_trans _ (actual_floored_lower n hn hx0 hx1
    (lower_boundary_relative (hp 0).le hd16 hx (boundaries_range a hp hs 0).2))
  apply lintegral_mono
  intro u
  dsimp only
  unfold AnnularLiteral.failureIndicator
  split_ifs with hg
  · simp
  · have hbad := zero_failure_implies_lower a hp hh hs he he4 hd n hn _ z hx hg
    simp [lowerEvent,hbad]

#print axioms actual_floored_upper
#print axioms actual_floored_lower
#print axioms actual_successor_stage_bound
#print axioms actual_zero_stage_bound
#print axioms boundaries_range
#print axioms boundaries_geometric
#print axioms exists_boundary_below
#print axioms selector_zero_iff
#print axioms selector_succ_iff
#print axioms report_measurable
#print axioms report_coherent
#print axioms zero_failure_implies_lower
#print axioms successor_failure_implies_boundary
#print axioms floor_upper_event
#print axioms floor_lower_event
end
end ClusterPolicy
