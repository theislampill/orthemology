import MixedScore

set_option maxHeartbeats 1200000

noncomputable section
open scoped BigOperators Topology
open Set Filter PolynomialAND ANDCorrection MixedHull MixedScore
open ANDScore (mean variance gRem fRem variance_pos)

namespace MixedRepair

def insideG (p h : Vec) (i : Fin 6) (eps : ℝ) : ℝ :=
  leadG (p 0) (p 2+p 3) (variance (h 0) (h 1)) (truth i 0) (truth i 2+truth i 3)+
    normalEnergy h+eps*gRemMixed h
      (beta (p 0) (p 2+p 3) (variance (h 0) (h 1)))
      (gamma (p 0) (p 2+p 3) (variance (h 0) (h 1))) eps

def insideF (p h : Vec) (i : Fin 6) (eps : ℝ) : ℝ :=
  leadF (p 0) (p 2+p 3) (variance (h 0) (h 1)) (truth i 0) (truth i 2+truth i 3)+
    100*normalEnergy h+eps*fRemMixed p h (truth i 0)
      (beta (p 0) (p 2+p 3) (variance (h 0) (h 1)))
      (gamma (p 0) (p 2+p 3) (variance (h 0) (h 1))) eps

lemma truth_classes (i : Fin 6) :
    (truth i 0=0 ∧ truth i 2+truth i 3=0) ∨
    (truth i 0=0 ∧ truth i 2+truth i 3=1) ∨
    (truth i 0=1 ∧ truth i 2+truth i 3=2) := by
  fin_cases i
  · change ((1:ℝ)=0 ∧ 1+1=0) ∨ (1=0 ∧ 1+1=1) ∨ (1=1 ∧ 1+1=2)
    norm_num
  · change ((0:ℝ)=0 ∧ 1+0=0) ∨ (0=0 ∧ 1+0=1) ∨ (0=1 ∧ 1+0=2)
    norm_num
  · change ((0:ℝ)=0 ∧ 1+0=0) ∨ (0=0 ∧ 1+0=1) ∨ (0=1 ∧ 1+0=2)
    norm_num
  · change ((0:ℝ)=0 ∧ 0+1=0) ∨ (0=0 ∧ 0+1=1) ∨ (0=1 ∧ 0+1=2)
    norm_num
  · change ((0:ℝ)=0 ∧ 0+1=0) ∨ (0=0 ∧ 0+1=1) ∨ (0=1 ∧ 0+1=2)
    norm_num
  · change ((0:ℝ)=0 ∧ 0+0=0) ∨ (0=0 ∧ 0+0=1) ∨ (0=1 ∧ 0+0=2)
    norm_num

lemma gainG (p h : Vec) (eps : ℝ) (i : Fin 6)
    (hp01 : p 0=p 1) (hpsum : highSum p=2) :
    scoreG (truth i) (p+eps • h)-scoreG (truth i) (MixedHull.candidate p h eps) =
      eps^2*insideG p h i eps := by
  have hh := MixedScore.gainG p h
    (beta (p 0) (p 2+p 3) (variance (h 0) (h 1)))
    (gamma (p 0) (p 2+p 3) (variance (h 0) (h 1))) eps i hp01 hpsum
  dsimp [MixedHull.candidate,insideG,leadG]
  convert hh using 1 <;> ring

lemma gainF (p h : Vec) (eps : ℝ) (i : Fin 6)
    (hp01 : p 0=p 1) (hpsum : highSum p=2) :
    scoreF (truth i) (p+eps • h)-scoreF (truth i) (MixedHull.candidate p h eps) =
      eps^2*insideF p h i eps := by
  have hh := MixedScore.gainF p h
    (beta (p 0) (p 2+p 3) (variance (h 0) (h 1)))
    (gamma (p 0) (p 2+p 3) (variance (h 0) (h 1))) eps i hp01 hpsum
  dsimp [MixedHull.candidate,insideF,leadF]
  convert hh using 1 <;> ring

lemma inside_zero_positive (p h : Vec) (hp : p ∈ intrinsicInterior ℝ MixedHull.hull)
    (htrans : h 0 ≠ h 1 ∨ highSum h ≠ 0) :
    ∀ i : Fin 6, 0 < insideG p h i 0 ∧ 0 < insideF p h i 0 := by
  obtain ⟨hp01,hpsum,hs,hz,hw,hsum,hcube⟩ := interior_parameters p hp
  have hs1 : p 0 < 1 := by linarith
  have hT0 : 2*(p 0)<p 2+p 3 := by linarith
  have hEH : 0 ≤ normalEnergy h := by dsimp [normalEnergy]; positivity
  by_cases hflag : h 0 ≠ h 1
  · have hall := all_leading_positive (p 0) (p 2+p 3) (variance (h 0) (h 1))
      hs hs1 hT0 hsum (variance_pos (h 0) (h 1) hflag)
    intro i
    rcases truth_classes i with ⟨ha,hj⟩ | ⟨ha,hj⟩ | ⟨ha,hj⟩
    · simp only [insideG,insideF,zero_mul,add_zero,ha,hj]
      constructor <;> linarith [hall.1,hall.2.2.2.1]
    · simp only [insideG,insideF,zero_mul,add_zero,ha,hj]
      constructor <;> linarith [hall.2.1,hall.2.2.2.2.1]
    · simp only [insideG,insideF,zero_mul,add_zero,ha,hj]
      constructor <;> linarith [hall.2.2.1,hall.2.2.2.2.2]
  · have heq : h 0=h 1 := not_not.mp hflag
    have hh : highSum h ≠ 0 := htrans.resolve_left hflag
    have hk : kappa h ≠ 0 := div_ne_zero hh (by norm_num)
    have hpE : 0 < normalEnergy h := by
      dsimp [normalEnergy]
      exact mul_pos (by norm_num) (sq_pos_of_ne_zero hk)
    intro i
    simp [insideG,insideF,variance,heq,leadG,leadF,beta,gamma]
    exact hpE

/-- Exact common repair on a Boolean hull with rank-one and rank-three
constrained blocks and no free singleton coordinates. -/
theorem universal_strict_Bregman_repair (p h : Vec)
    (hp : p ∈ intrinsicInterior ℝ MixedHull.hull)
    (htrans : h 0 ≠ h 1 ∨ highSum h ≠ 0) :
    ∃ delta > 0, ∀ eps : ℝ, 0 < eps → eps < delta →
      (∀ j : Fin 6, (p+eps • h) j ∈ Ioo 0 1) ∧
      MixedHull.candidate p h eps ∈ MixedHull.hull ∧
      (∀ i : Fin 6,
        scoreG (truth i) (MixedHull.candidate p h eps)<scoreG (truth i) (p+eps • h) ∧
        scoreF (truth i) (MixedHull.candidate p h eps)<scoreF (truth i) (p+eps • h)) := by
  obtain ⟨hp01,hpsum,hs,hz,hw,hsum,hcube⟩ := interior_parameters p hp
  have hzpos := inside_zero_positive p h hp htrans
  have hG : ∀ᶠ eps : ℝ in 𝓝 0, ∀ i : Fin 6, 0 < insideG p h i eps := by
    apply Filter.eventually_all.mpr
    intro i
    have hc : Continuous (insideG p h i) := by
      unfold insideG gRemMixed gRem highRem
      fun_prop
    exact hc.continuousAt.tendsto.eventually (eventually_gt_nhds (hzpos i).1)
  have hF : ∀ᶠ eps : ℝ in 𝓝 0, ∀ i : Fin 6, 0 < insideF p h i eps := by
    apply Filter.eventually_all.mpr
    intro i
    have hc : Continuous (insideF p h i) := by
      unfold insideF fRemMixed fRem highRem
      fun_prop
    exact hc.continuousAt.tendsto.eventually (eventually_gt_nhds (hzpos i).2)
  have hC : ∀ᶠ eps : ℝ in 𝓝 0, MixedHull.candidate p h eps ∈ MixedHull.hull :=
    candidate_eventually_mem p h
      (beta (p 0) (p 2+p 3) (variance (h 0) (h 1)))
      (gamma (p 0) (p 2+p 3) (variance (h 0) (h 1))) hp
  have hbase : ∀ᶠ eps : ℝ in 𝓝 0, ∀ i : Fin 6, (p+eps • h) i ∈ Ioo 0 1 := by
    apply Filter.eventually_all.mpr
    intro i
    have hc : Continuous (fun eps : ℝ => (p+eps • h) i) := by fun_prop
    have hh : (p+(0:ℝ) • h) i ∈ Ioo 0 1 := by simpa using hcube i
    exact hc.continuousAt.tendsto.eventually (isOpen_Ioo.mem_nhds hh)
  have hgood : ∀ᶠ eps : ℝ in 𝓝 0,
      (∀ i : Fin 6, 0 < insideG p h i eps) ∧ (∀ i : Fin 6, 0 < insideF p h i eps) ∧
      MixedHull.candidate p h eps ∈ MixedHull.hull ∧
      (∀ i : Fin 6, (p+eps • h) i ∈ Ioo 0 1) := by
    filter_upwards [hG,hF,hC,hbase] with eps hg hf hc hb
    exact ⟨hg,hf,hc,hb⟩
  obtain ⟨delta,hd,hdelta⟩ := Metric.eventually_nhds_iff.mp hgood
  refine ⟨delta,hd,?_⟩
  intro eps he hsmall
  have hh := hdelta (show dist eps 0 < delta by simpa [Real.dist_eq,abs_of_pos he] using hsmall)
  refine ⟨hh.2.2.2,hh.2.2.1,?_⟩
  intro i
  have hsquare : 0 < eps^2 := pow_pos he 2
  have hgp := mul_pos hsquare (hh.1 i)
  have hfp := mul_pos hsquare (hh.2.1 i)
  rw [← gainG p h eps i hp01 hpsum] at hgp
  rw [← gainF p h eps i hp01 hpsum] at hfp
  constructor <;> linarith

#print axioms universal_strict_Bregman_repair
end MixedRepair
