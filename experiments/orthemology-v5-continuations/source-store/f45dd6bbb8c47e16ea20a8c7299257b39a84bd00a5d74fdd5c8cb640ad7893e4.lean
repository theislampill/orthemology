import ANDRepair

noncomputable section
open scoped BigOperators Topology
open Set Filter PolynomialAND ANDCorrection ANDScore ANDRepair

namespace ANDPotentialBinding

abbrev Vec := Fin 4 → ℝ

def coordF (i : Fin 4) (t : ℝ) : ℝ := if i.val < 2 then psi t else 50*t^2
def coordDF (i : Fin 4) (t : ℝ) : ℝ := if i.val < 2 then dpsi t else 100*t
def coordDDF (i : Fin 4) (t : ℝ) : ℝ := if i.val < 2 then curvature t else 100

def coordG (_i : Fin 4) (t : ℝ) : ℝ := t^2/2
def coordDG (_i : Fin 4) (t : ℝ) : ℝ := t

lemma coordF_deriv (i : Fin 4) (t : ℝ) : HasDerivAt (coordF i) (coordDF i t) t := by
  by_cases h : i.val < 2
  · have hh : coordF i = psi := by funext x; simp [coordF, h]
    rw [hh]
    simpa [coordDF, h] using psi_deriv t
  · have hh : coordF i = fun x => 50*x^2 := by funext x; simp [coordF, h]
    rw [hh]
    convert (((hasDerivAt_id t).pow 2).const_mul 50) using 1 <;>
      simp [coordDF, h] <;> ring

lemma coordDF_deriv (i : Fin 4) (t : ℝ) : HasDerivAt (coordDF i) (coordDDF i t) t := by
  by_cases h : i.val < 2
  · have hh : coordDF i = dpsi := by funext x; simp [coordDF, h]
    rw [hh]
    simpa [coordDDF, h] using dpsi_deriv t
  · have hh : coordDF i = fun x => 100*x := by funext x; simp [coordDF, h]
    rw [hh]
    convert (hasDerivAt_id t).const_mul 100 using 1 <;> simp [coordDDF, h]

lemma coordG_deriv (i : Fin 4) (t : ℝ) : HasDerivAt (coordG i) (coordDG i t) t := by
  change HasDerivAt (fun x : ℝ => x^2/2) t t
  convert ((hasDerivAt_id t).pow 2).div_const 2 using 1 <;> simp <;> ring

lemma coordF_curvature_positive (i : Fin 4) (t : ℝ) : 0 < coordDDF i t := by
  by_cases h : i.val < 2
  · simpa [coordDDF, h] using curvature_pos t
  · norm_num [coordDDF, h]

def potential (f : Fin 4 → ℝ → ℝ) (x : Vec) : ℝ := ∑ i, f i (x i)
def gradient (df : Fin 4 → ℝ → ℝ) (x : Vec) : Vec →L[ℝ] ℝ :=
  ∑ i, df i (x i) • (ContinuousLinearMap.proj i : Vec →L[ℝ] ℝ)

def divergence (f df : Fin 4 → ℝ → ℝ) (v b : Vec) : ℝ :=
  potential f v-potential f b-gradient df b (v-b)

lemma potential_hasFDerivAt (f df : Fin 4 → ℝ → ℝ)
    (h : ∀ i t, HasDerivAt (f i) (df i t) t) (p : Vec) :
    HasFDerivAt (potential f) (gradient df p) p := by
  have hi : ∀ i : Fin 4, HasFDerivAt (fun x : Vec => f i (x i))
      (df i (p i) • (ContinuousLinearMap.proj i : Vec →L[ℝ] ℝ)) p := by
    intro i
    exact (h i (p i)).comp_hasFDerivAt p (ContinuousLinearMap.proj i : Vec →L[ℝ] ℝ).hasFDerivAt
  simpa [potential, gradient] using HasFDerivAt.sum (u := Finset.univ) (fun i _ => hi i)

lemma divergence_eq_sum (f df : Fin 4 → ℝ → ℝ) (v b : Vec) :
    divergence f df v b = ∑ i, (f i (v i)-f i (b i)-df i (b i)*(v i-b i)) := by
  simp [divergence, potential, gradient, Finset.sum_sub_distrib]

lemma scoreF_is_actual_Bregman (i : Fin 4) (b : Vec) :
    scoreF (truth i) b = divergence coordF coordDF (truth i) b := by
  rw [divergence_eq_sum]
  fin_cases i <;> simp [scoreF, fLoss, truth, coordF, coordDF, Fin.sum_univ_succ, scalarDiv] <;> ring

lemma scoreG_is_actual_Bregman (i : Fin 4) (b : Vec) :
    scoreG (truth i) b = divergence coordG coordDG (truth i) b := by
  rw [divergence_eq_sum]
  fin_cases i <;> simp [scoreG, gLoss, truth, coordG, coordDG, Fin.sum_univ_succ] <;> ring

def tangentProjection (h : Vec) : Vec :=
  ![(h 0+h 1)/2,(h 0+h 1)/2,h 2,h 3]

lemma common_hessian_normal (s z w : ℝ) (h u : Vec) (hu : u 0 = u 1) :
    (∑ i : Fin 4, (h i-tangentProjection h i)*u i)=0 ∧
    (∑ i : Fin 4, coordDDF i (![s,s,z,w] i)*(h i-tangentProjection h i)*u i)=0 := by
  constructor <;> simp [coordDDF, tangentProjection, Fin.sum_univ_succ, hu] <;> ring

lemma coordF_contDiff (i : Fin 4) : ContDiff ℝ ⊤ (coordF i) := by
  by_cases h : i.val < 2
  · change ContDiff ℝ ⊤ (fun t => if i.val < 2 then psi t else 50*t^2)
    simp only [h, ite_true]
    unfold psi
    simp only [div_eq_mul_inv]
    fun_prop
  · change ContDiff ℝ ⊤ (fun t => if i.val < 2 then psi t else 50*t^2)
    simp only [h, ite_false]
    fun_prop

lemma potentialF_contDiff : ContDiff ℝ ⊤ (potential coordF) := by
  unfold potential
  apply ContDiff.sum
  intro i _
  exact (coordF_contDiff i).comp (contDiff_apply ℝ ℝ i)

/-- The nonlinear global repair theorem is bound to true Bregman divergences
of explicit polynomial potentials with their proved derivatives. -/
theorem universal_Bregman_repair (s z w h1 h2 hz hw : ℝ)
    (hs : 0 < s) (hzs : s < z) (hws : s < w) (hsum : z+w < 1+s)
    (hne : h1 ≠ h2) :
    ∃ delta > 0, ∀ eps : ℝ, 0 < eps → eps < delta →
      (∀ j : Fin 4, baseline s z w h1 h2 hz hw eps j ∈ Ioo 0 1) ∧
      candidate s z w h1 h2 hz hw eps ∈ hull ∧
      (∀ i : Fin 4,
        divergence coordG coordDG (truth i) (candidate s z w h1 h2 hz hw eps) <
          divergence coordG coordDG (truth i) (baseline s z w h1 h2 hz hw eps) ∧
        divergence coordF coordDF (truth i) (candidate s z w h1 h2 hz hw eps) <
          divergence coordF coordDF (truth i) (baseline s z w h1 h2 hz hw eps)) := by
  obtain ⟨delta, hd, hh⟩ := universal_strict_repair s z w h1 h2 hz hw hs hzs hws hsum hne
  refine ⟨delta, hd, ?_⟩
  intro eps he hsmall
  obtain ⟨hb, hc, hgain⟩ := hh eps he hsmall
  refine ⟨hb,hc,?_⟩
  intro i
  simpa only [scoreF_is_actual_Bregman, scoreG_is_actual_Bregman] using hgain i

#print axioms universal_Bregman_repair
#print axioms potential_hasFDerivAt
end ANDPotentialBinding
