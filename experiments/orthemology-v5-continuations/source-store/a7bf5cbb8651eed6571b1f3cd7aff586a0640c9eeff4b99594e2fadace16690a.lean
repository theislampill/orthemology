import MixedHull

set_option maxHeartbeats 1200000

noncomputable section
open scoped BigOperators Topology
open Set Filter PolynomialAND ANDCorrection MixedHull
open ANDScore (mean variance gRem fRem variance_pos)

namespace MixedScore

-- Explicit coordinate potentials and their genuine derivatives.
def coordF (i : Fin 6) (t : ℝ) : ℝ := if i.val < 2 then psi t else 50*t^2
def coordDF (i : Fin 6) (t : ℝ) : ℝ := if i.val < 2 then dpsi t else 100*t
def coordDDF (i : Fin 6) (t : ℝ) : ℝ := if i.val < 2 then curvature t else 100
def coordG (_i : Fin 6) (t : ℝ) : ℝ := t^2/2
def coordDG (_i : Fin 6) (t : ℝ) : ℝ := t

lemma coordF_deriv (i : Fin 6) (t : ℝ) : HasDerivAt (coordF i) (coordDF i t) t := by
  by_cases h : i.val < 2
  · have hh : coordF i = psi := by funext x; simp [coordF,h]
    rw [hh]
    simpa [coordDF,h] using psi_deriv t
  · have hh : coordF i = fun x => 50*x^2 := by funext x; simp [coordF,h]
    rw [hh]
    convert (((hasDerivAt_id t).pow 2).const_mul 50) using 1 <;> simp [coordDF,h] <;> ring

lemma coordDF_deriv (i : Fin 6) (t : ℝ) : HasDerivAt (coordDF i) (coordDDF i t) t := by
  by_cases h : i.val < 2
  · have hh : coordDF i = dpsi := by funext x; simp [coordDF,h]
    rw [hh]
    simpa [coordDDF,h] using dpsi_deriv t
  · have hh : coordDF i = fun x => 100*x := by funext x; simp [coordDF,h]
    rw [hh]
    convert (hasDerivAt_id t).const_mul 100 using 1 <;> simp [coordDDF,h]

lemma coordG_deriv (i : Fin 6) (t : ℝ) : HasDerivAt (coordG i) (coordDG i t) t := by
  change HasDerivAt (fun x : ℝ => x^2/2) t t
  convert ((hasDerivAt_id t).pow 2).div_const 2 using 1 <;> simp <;> ring

lemma coordF_curvature_positive (i : Fin 6) (t : ℝ) : 0 < coordDDF i t := by
  by_cases h : i.val < 2
  · simpa [coordDDF,h] using curvature_pos t
  · norm_num [coordDDF,h]

def potential (f : Fin 6 → ℝ → ℝ) (x : Vec) : ℝ := ∑ i, f i (x i)
def gradient (df : Fin 6 → ℝ → ℝ) (x : Vec) : Vec →L[ℝ] ℝ :=
  ∑ i, df i (x i) • (ContinuousLinearMap.proj i : Vec →L[ℝ] ℝ)
def divergence (f df : Fin 6 → ℝ → ℝ) (v b : Vec) : ℝ :=
  potential f v-potential f b-gradient df b (v-b)

lemma potential_hasFDerivAt (f df : Fin 6 → ℝ → ℝ)
    (h : ∀ i t, HasDerivAt (f i) (df i t) t) (p : Vec) :
    HasFDerivAt (potential f) (gradient df p) p := by
  have hi : ∀ i : Fin 6, HasFDerivAt (fun x : Vec => f i (x i))
      (df i (p i) • (ContinuousLinearMap.proj i : Vec →L[ℝ] ℝ)) p := by
    intro i
    exact (h i (p i)).comp_hasFDerivAt p (ContinuousLinearMap.proj i : Vec →L[ℝ] ℝ).hasFDerivAt
  simpa [potential,gradient] using HasFDerivAt.sum (u := Finset.univ) (fun i _ => hi i)

lemma potentialF_hasFDerivAt (p : Vec) :
    HasFDerivAt (potential coordF) (gradient coordDF p) p :=
  potential_hasFDerivAt coordF coordDF coordF_deriv p

lemma potentialG_hasFDerivAt (p : Vec) :
    HasFDerivAt (potential coordG) (gradient coordDG p) p :=
  potential_hasFDerivAt coordG coordDG coordG_deriv p

lemma coordF_contDiff (i : Fin 6) : ContDiff ℝ ⊤ (coordF i) := by
  by_cases h : i.val < 2
  · change ContDiff ℝ ⊤ (fun t => if i.val < 2 then psi t else 50*t^2)
    simp only [h,ite_true]
    unfold psi
    simp only [div_eq_mul_inv]
    fun_prop
  · change ContDiff ℝ ⊤ (fun t => if i.val < 2 then psi t else 50*t^2)
    simp only [h,ite_false]
    fun_prop

lemma potentialF_contDiff : ContDiff ℝ ⊤ (potential coordF) := by
  unfold potential
  apply ContDiff.sum
  intro i _
  exact (coordF_contDiff i).comp (contDiff_apply ℝ ℝ i)

lemma potentialG_contDiff : ContDiff ℝ ⊤ (potential coordG) := by
  unfold potential
  apply ContDiff.sum
  intro i _
  simp only [coordG,div_eq_mul_inv]
  fun_prop

lemma divergence_eq_sum (f df : Fin 6 → ℝ → ℝ) (v b : Vec) :
    divergence f df v b = ∑ i, (f i (v i)-f i (b i)-df i (b i)*(v i-b i)) := by
  simp [divergence,potential,gradient,Finset.sum_sub_distrib]

def scoreG (v c : Vec) : ℝ := divergence coordG coordDG v c
def scoreF (v c : Vec) : ℝ := divergence coordF coordDF v c

def highRem (h : Vec) (g eps : ℝ) : ℝ :=
  -(g/2)*(h 2+h 3-h 4-h 5)-eps*g^2/2

def gRemMixed (h : Vec) (b g eps : ℝ) : ℝ :=
  gRem (h 0) (h 1) 0 0 b 0 eps+highRem h g eps

def fRemMixed (p h : Vec) (a b g eps : ℝ) : ℝ :=
  fRem (p 0) a (h 0) (h 1) 0 0 b 0 eps+100*highRem h g eps

/-- Exact nonlinear gain identities, including the independently incoherent
higher-rank block; the extra normal energy is derived, not postulated. -/
theorem gainG (p h : Vec) (b g eps : ℝ) (i : Fin 6)
    (hp01 : p 0=p 1) (hpsum : highSum p=2) :
    scoreG (truth i) (p+eps • h)-scoreG (truth i) (candidateWith p h b g eps) =
      eps^2*(variance (h 0) (h 1)-2*(p 0-truth i 0)*b+
        (truth i 2+truth i 3-p 2-p 3)*g+normalEnergy h+eps*gRemMixed h b g eps) := by
  have hp1 := hp01.symm
  have hp5 : p 5=2-p 2-p 3-p 4 := by dsimp [highSum] at hpsum; linarith
  simp only [scoreG,divergence_eq_sum]
  fin_cases i <;>
    simp [coordG,coordDG,truth,Fin.sum_univ_succ,candidateWith,variance,mean,
      normalEnergy,kappa,highSum,gRemMixed,gRem,highRem,hp1,hp5] <;> ring

theorem gainF (p h : Vec) (b g eps : ℝ) (i : Fin 6)
    (hp01 : p 0=p 1) (hpsum : highSum p=2) :
    scoreF (truth i) (p+eps • h)-scoreF (truth i) (candidateWith p h b g eps) =
      eps^2*(curvature (p 0)*variance (h 0) (h 1)+
        (p 0-truth i 0)*(96*(p 0)*variance (h 0) (h 1)-2*curvature (p 0)*b)+
        100*(truth i 2+truth i 3-p 2-p 3)*g+100*normalEnergy h+eps*fRemMixed p h (truth i 0) b g eps) := by
  have hp1 := hp01.symm
  have hp5 : p 5=2-p 2-p 3-p 4 := by dsimp [highSum] at hpsum; linarith
  simp only [scoreF,divergence_eq_sum]
  fin_cases i <;>
    simp [coordF,coordDF,psi,dpsi,truth,Fin.sum_univ_succ,candidateWith,variance,mean,
      curvature,normalEnergy,kappa,highSum,fRemMixed,fRem,highRem,hp1,hp5] <;> ring

end MixedScore
