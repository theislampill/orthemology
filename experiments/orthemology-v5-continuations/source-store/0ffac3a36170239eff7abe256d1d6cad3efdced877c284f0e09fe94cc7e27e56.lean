import ANDScore
import FiniteHullWeights

noncomputable section
open scoped BigOperators Topology
open Set Filter PolynomialAND ANDCorrection ANDScore

namespace MixedHull

abbrev Vec := Fin 6 → ℝ

def truth : Fin 6 → Vec :=
  ![![1,1,1,1,0,0], ![0,0,1,0,1,0], ![0,0,1,0,0,1],
    ![0,0,0,1,1,0], ![0,0,0,1,0,1], ![0,0,0,0,1,1]]

def hull : Set Vec := convexHull ℝ (Set.range truth)
def highSum (p : Vec) : ℝ := p 2+p 3+p 4+p 5
def kappa (h : Vec) : ℝ := highSum h/4
def normalEnergy (h : Vec) : ℝ := 2*(kappa h)^2

def candidateWith (p h : Vec) (b g eps : ℝ) : Vec :=
  let q := p 0+eps*mean (h 0) (h 1)+eps^2*b
  ![q,q,p 2+eps*(h 2-kappa h)+eps^2*g/2,
    p 3+eps*(h 3-kappa h)+eps^2*g/2,
    p 4+eps*(h 4-kappa h)-eps^2*g/2,
    p 5+eps*(h 5-kappa h)-eps^2*g/2]

def candidate (p h : Vec) (eps : ℝ) : Vec :=
  candidateWith p h (beta (p 0) (p 2+p 3) (variance (h 0) (h 1)))
    (gamma (p 0) (p 2+p 3) (variance (h 0) (h 1))) eps

def coefficients (d : Vec) : Fin 6 → ℝ :=
  ![d 0,0,d 2-d 0,d 4-d 0+d 2+d 3,-d 4-d 2,d 0-d 2-d 3]

lemma coefficients_sum (d : Vec) : ∑ i, coefficients d i = 0 := by
  simp [coefficients,Fin.sum_univ_succ]
  ring

lemma coefficients_center (d : Vec) (h01 : d 0 = d 1) (hsum : highSum d = 0) :
    (∑ i, coefficients d i • truth i) = d := by
  have hd5 : d 5 = -d 2-d 3-d 4 := by dsimp [highSum] at hsum; linarith
  ext i
  fin_cases i <;> simp [coefficients,truth,Fin.sum_univ_succ,h01,hd5] <;> ring

lemma candidate_zero (p h : Vec) (b g : ℝ) (h01 : p 0 = p 1) :
    candidateWith p h b g 0 = p := by
  ext i
  fin_cases i <;> simp [candidateWith,h01]

lemma candidate_affine (p h : Vec) (b g eps : ℝ) (h01 : p 0 = p 1) :
    (candidateWith p h b g eps-p) 0 = (candidateWith p h b g eps-p) 1 ∧
      highSum (candidateWith p h b g eps-p) = 0 := by
  constructor
  · simp [candidateWith,h01]
  · dsimp [highSum,candidateWith,kappa]
    ring

lemma interior_parameters (p : Vec) (hp : p ∈ intrinsicInterior ℝ hull) :
    p 0=p 1 ∧ highSum p=2 ∧ 0<p 0 ∧ p 0<p 2 ∧ p 0<p 3 ∧
      p 2+p 3<1+p 0 ∧ (∀ i : Fin 6, p i ∈ Ioo 0 1) := by
  obtain ⟨a,ha,hmass,hcenter⟩ :=
    FiniteHullWeights.intrinsicInterior_positive_barycentric truth p hp
  have h0 := congrArg (fun v : Vec => v 0) hcenter
  have h1 := congrArg (fun v : Vec => v 1) hcenter
  have h2 := congrArg (fun v : Vec => v 2) hcenter
  have h3 := congrArg (fun v : Vec => v 3) hcenter
  have h4 := congrArg (fun v : Vec => v 4) hcenter
  have h5 := congrArg (fun v : Vec => v 5) hcenter
  simp [truth,Fin.sum_univ_succ] at h0 h1 h2 h3 h4 h5 hmass
  have ha0 := ha 0
  have ha1 := ha 1
  have ha2 := ha 2
  have ha3 := ha 3
  have ha4 := ha 4
  have ha5 := ha 5
  refine ⟨?_,?_,?_,?_,?_,?_,?_⟩
  · linarith
  · dsimp [highSum]
    linarith
  · linarith
  · linarith
  · linarith
  · linarith
  · intro i
    fin_cases i <;> dsimp <;> constructor <;> linarith

/-- Any explicitly tangent polynomial correction stays in the actual six-vertex
hull near an intrinsic-interior point. The proof supplies positive weights. -/
lemma candidate_eventually_mem (p h : Vec) (b g : ℝ)
    (hp : p ∈ intrinsicInterior ℝ hull) :
    ∀ᶠ eps : ℝ in 𝓝 0, candidateWith p h b g eps ∈ hull := by
  obtain ⟨a,ha,hmass,hcenter⟩ :=
    FiniteHullWeights.intrinsicInterior_positive_barycentric truth p hp
  have h01 := (interior_parameters p hp).1
  let weights : ℝ → Fin 6 → ℝ := fun eps i => a i+coefficients (candidateWith p h b g eps-p) i
  have hw0 : ∀ i : Fin 6, 0 < weights 0 i := by
    intro i
    dsimp [weights]
    rw [candidate_zero p h b g h01,sub_self]
    fin_cases i <;> simpa [coefficients] using ha _
  have hwe : ∀ᶠ eps : ℝ in 𝓝 0, ∀ i : Fin 6, 0 < weights eps i := by
    apply Filter.eventually_all.mpr
    intro i
    have hc : Continuous (fun eps : ℝ => weights eps i) := by
      fin_cases i <;> dsimp [weights,coefficients,candidateWith] <;> fun_prop
    exact hc.continuousAt.tendsto.eventually (eventually_gt_nhds (hw0 i))
  filter_upwards [hwe] with eps heps
  have haff := candidate_affine p h b g eps h01
  have hcoeff := coefficients_center (candidateWith p h b g eps-p) haff.1 haff.2
  apply mem_convexHull_of_exists_fintype (weights eps) truth
  · intro i
    exact (heps i).le
  · dsimp [weights]
    rw [Finset.sum_add_distrib,hmass,coefficients_sum]
    ring
  · intro i
    exact Set.mem_range_self i
  · dsimp [weights]
    simp only [add_smul,Finset.sum_add_distrib,hcenter,hcoeff]
    abel

end MixedHull
