import CountableHistoryTower

noncomputable section
open MeasureTheory
open scoped ENNReal BigOperators Function
namespace HiddenParity.Cost

/-- A prefix-free countable family plus the no-start complement supports a
weighted nonnegative tower step. Past accumulated weight need only be constant
on each finite-start cylinder; it may vary freely on the no-start complement. -/
theorem prefix_family_weighted_bound {Ω ι : Type*} [MeasurableSpace Ω] [Countable ι]
    (μ : Measure Ω) (E : ι → Set Ω) (hE : ∀ i,MeasurableSet (E i))
    (hd : Pairwise (Disjoint on E)) (past factor : Ω → ℝ≥0∞)
    (hpast : Measurable past) (hfactor : Measurable factor)
    (value : ι → ℝ≥0∞) (hknown : ∀ i ω,ω∈E i → past ω=value i)
    (K : ℝ≥0∞) (hK : 1≤K)
    (hbound : ∀ i,(∫⁻ ω in E i,factor ω ∂μ)≤K*μ (E i))
    (hOutside : ∀ ω,ω∉⋃ i,E i → factor ω=1) :
    (∫⁻ ω,past ω*factor ω ∂μ)≤K*(∫⁻ ω,past ω ∂μ) := by
  have hU : MeasurableSet (⋃ i,E i) := MeasurableSet.iUnion hE
  have hIn : (∫⁻ ω in ⋃ i,E i,past ω*factor ω ∂μ)≤K*(∫⁻ ω in ⋃ i,E i,past ω ∂μ) := by
    rw [lintegral_iUnion hE hd,lintegral_iUnion hE hd,← ENNReal.tsum_mul_left]
    apply ENNReal.tsum_le_tsum
    intro i
    have h₁ : (∫⁻ ω in E i,past ω*factor ω ∂μ)=value i*(∫⁻ ω in E i,factor ω ∂μ) := by
      rw [← lintegral_const_mul _ hfactor]
      apply setLIntegral_congr_fun (hE i)
      filter_upwards [] with ω hω
      rw [hknown i ω hω]
    have h₂ : (∫⁻ ω in E i,past ω ∂μ)=value i*μ (E i) := by
      rw [← setLIntegral_const]
      apply setLIntegral_congr_fun (hE i)
      filter_upwards [] with ω hω
      exact hknown i ω hω
    rw [h₁,h₂]
    simpa only [mul_assoc,mul_left_comm K (value i)] using mul_le_mul_left' (hbound i) (value i)
  have hOut : (∫⁻ ω in (⋃ i,E i)ᶜ,past ω*factor ω ∂μ)≤K*(∫⁻ ω in (⋃ i,E i)ᶜ,past ω ∂μ) := by
    have he : (∫⁻ ω in (⋃ i,E i)ᶜ,past ω*factor ω ∂μ)=(∫⁻ ω in (⋃ i,E i)ᶜ,past ω ∂μ) := by
      apply setLIntegral_congr_fun hU.compl
      filter_upwards [] with ω hω
      rw [hOutside ω hω,mul_one]
    rw [he]
    simpa only [one_mul] using mul_le_mul_right' hK (∫⁻ ω in (⋃ i,E i)ᶜ,past ω ∂μ)
  rw [← lintegral_add_compl (fun ω => past ω*factor ω) hU,
    ← lintegral_add_compl past hU,mul_add]
  exact add_le_add hIn hOut

end HiddenParity.Cost
