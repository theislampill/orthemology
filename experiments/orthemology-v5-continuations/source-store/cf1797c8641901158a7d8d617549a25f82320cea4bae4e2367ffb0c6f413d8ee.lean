import ANDScore

noncomputable section
open scoped BigOperators Topology
open Set Filter PolynomialAND ANDCorrection ANDScore

namespace ANDRepair

def insideG (s z w h1 h2 hz hw : ℝ) (i : Fin 4) (eps : ℝ) : ℝ :=
  leadG s (z+w) (variance h1 h2) (truth i 0) (truth i 2+truth i 3) +
    eps*gRem h1 h2 hz hw (beta s (z+w) (variance h1 h2))
      (gamma s (z+w) (variance h1 h2)) eps

def insideF (s z w h1 h2 hz hw : ℝ) (i : Fin 4) (eps : ℝ) : ℝ :=
  leadF s (z+w) (variance h1 h2) (truth i 0) (truth i 2+truth i 3) +
    eps*fRem s (truth i 0) h1 h2 hz hw (beta s (z+w) (variance h1 h2))
      (gamma s (z+w) (variance h1 h2)) eps

def bary (s z w h1 h2 hz hw eps : ℝ) : Fin 4 → ℝ :=
  let c := candidate s z w h1 h2 hz hw eps
  ![1+c 0-c 2-c 3,c 2-c 0,c 3-c 0,c 0]

lemma gainG (s z w h1 h2 hz hw eps : ℝ) (i : Fin 4) :
    scoreG (truth i) (baseline s z w h1 h2 hz hw eps) -
      scoreG (truth i) (candidate s z w h1 h2 hz hw eps) =
        eps^2*insideG s z w h1 h2 hz hw i eps := by
  have hh := g_gain_identity s z w h1 h2 hz hw
    (beta s (z+w) (variance h1 h2)) (gamma s (z+w) (variance h1 h2))
    (truth i 0) (truth i 2) (truth i 3) eps
  dsimp [scoreG, baseline, candidate, insideG, leadG]
  convert hh using 1 <;> ring

lemma gainF (s z w h1 h2 hz hw eps : ℝ) (i : Fin 4) :
    scoreF (truth i) (baseline s z w h1 h2 hz hw eps) -
      scoreF (truth i) (candidate s z w h1 h2 hz hw eps) =
        eps^2*insideF s z w h1 h2 hz hw i eps := by
  have hh := f_gain_identity s z w h1 h2 hz hw
    (beta s (z+w) (variance h1 h2)) (gamma s (z+w) (variance h1 h2))
    (truth i 0) (truth i 2) (truth i 3) eps
  dsimp [scoreF, baseline, candidate, insideF, leadF]
  convert hh using 1 <;> ring

/-- Literal finite-hull nonlinear repair: every interior AND context, every
transverse direction, and every sufficiently small positive real scale.
The candidate is defined explicitly and has an epsilon-squared correction. -/
theorem universal_strict_repair (s z w h1 h2 hz hw : ℝ)
    (hs : 0 < s) (hzs : s < z) (hws : s < w) (hsum : z+w < 1+s)
    (hne : h1 ≠ h2) :
    ∃ delta > 0, ∀ eps : ℝ, 0 < eps → eps < delta →
      (∀ j : Fin 4, baseline s z w h1 h2 hz hw eps j ∈ Ioo 0 1) ∧
      candidate s z w h1 h2 hz hw eps ∈ hull ∧
      (∀ i : Fin 4,
        scoreG (truth i) (candidate s z w h1 h2 hz hw eps) <
          scoreG (truth i) (baseline s z w h1 h2 hz hw eps) ∧
        scoreF (truth i) (candidate s z w h1 h2 hz hw eps) <
          scoreF (truth i) (baseline s z w h1 h2 hz hw eps)) := by
  have hs1 : s < 1 := by linarith
  have hT0 : 2*s < z+w := by linarith
  have he := variance_pos h1 h2 hne
  have hall := all_leading_positive s (z+w) (variance h1 h2) hs hs1 hT0 hsum he
  have hG0 : ∀ i : Fin 4, 0 < insideG s z w h1 h2 hz hw i 0 := by
    intro i
    fin_cases i
    · simpa [insideG, truth] using hall.1
    · simpa [insideG, truth] using hall.2.1
    · simpa [insideG, truth] using hall.2.1
    · norm_num [insideG, truth]
      change 0 < leadG s (z+w) (variance h1 h2) 1 ((1:ℝ)+1)
      norm_num
      exact hall.2.2.1
  have hF0 : ∀ i : Fin 4, 0 < insideF s z w h1 h2 hz hw i 0 := by
    intro i
    fin_cases i
    · simpa [insideF, truth] using hall.2.2.2.1
    · simpa [insideF, truth] using hall.2.2.2.2.1
    · simpa [insideF, truth] using hall.2.2.2.2.1
    · norm_num [insideF, truth]
      change 0 < leadF s (z+w) (variance h1 h2) 1 ((1:ℝ)+1)
      norm_num
      exact hall.2.2.2.2.2
  have hGe : ∀ᶠ eps : ℝ in 𝓝 0, ∀ i : Fin 4, 0 < insideG s z w h1 h2 hz hw i eps := by
    apply Filter.eventually_all.mpr
    intro i
    have hc : Continuous (insideG s z w h1 h2 hz hw i) :=
      g_loss_inside_continuous s z w h1 h2 hz hw (truth i 0) (truth i 2+truth i 3)
    exact hc.continuousAt.tendsto.eventually (eventually_gt_nhds (hG0 i))
  have hFe : ∀ᶠ eps : ℝ in 𝓝 0, ∀ i : Fin 4, 0 < insideF s z w h1 h2 hz hw i eps := by
    apply Filter.eventually_all.mpr
    intro i
    have hc : Continuous (insideF s z w h1 h2 hz hw i) :=
      f_loss_inside_continuous s z w h1 h2 hz hw (truth i 0) (truth i 2+truth i 3)
    exact hc.continuousAt.tendsto.eventually (eventually_gt_nhds (hF0 i))
  have hb0 : ∀ i : Fin 4, 0 < bary s z w h1 h2 hz hw 0 i := by
    intro i
    fin_cases i <;> simp [bary, candidate] <;> linarith
  have hbe : ∀ᶠ eps : ℝ in 𝓝 0, ∀ i : Fin 4, 0 < bary s z w h1 h2 hz hw eps i := by
    apply Filter.eventually_all.mpr
    intro i
    have hc : Continuous (fun eps : ℝ => bary s z w h1 h2 hz hw eps i) := by
      fin_cases i <;> unfold bary candidate <;> simp <;> fun_prop
    exact hc.continuousAt.tendsto.eventually (eventually_gt_nhds (hb0 i))
  have hbase0 : ∀ i : Fin 4, baseline s z w h1 h2 hz hw 0 i ∈ Ioo 0 1 := by
    intro i
    fin_cases i <;> simp [baseline] <;> constructor <;> linarith
  have hbase : ∀ᶠ eps : ℝ in 𝓝 0, ∀ i : Fin 4,
      baseline s z w h1 h2 hz hw eps i ∈ Ioo 0 1 := by
    apply Filter.eventually_all.mpr
    intro i
    have hc : Continuous (fun eps : ℝ => baseline s z w h1 h2 hz hw eps i) := by
      fin_cases i <;> unfold baseline <;> simp <;> fun_prop
    exact hc.continuousAt.tendsto.eventually (isOpen_Ioo.mem_nhds (hbase0 i))
  have hgood : ∀ᶠ eps : ℝ in 𝓝 0,
      (∀ i : Fin 4, 0 < insideG s z w h1 h2 hz hw i eps) ∧
      (∀ i : Fin 4, 0 < insideF s z w h1 h2 hz hw i eps) ∧
      (∀ i : Fin 4, 0 < bary s z w h1 h2 hz hw eps i) ∧
      (∀ i : Fin 4, baseline s z w h1 h2 hz hw eps i ∈ Ioo 0 1) := by
    filter_upwards [hGe, hFe, hbe, hbase] with eps hg hf hb hba
    exact ⟨hg,hf,hb,hba⟩
  obtain ⟨delta, hd, hdelta⟩ := Metric.eventually_nhds_iff.mp hgood
  refine ⟨delta, hd, ?_⟩
  intro eps heps hsmall
  have hg := hdelta (show dist eps 0 < delta by simpa [Real.dist_eq, abs_of_pos heps] using hsmall)
  refine ⟨hg.2.2.2, ?_, ?_⟩
  · let c := candidate s z w h1 h2 hz hw eps
    have hh0 := hg.2.2.1 0
    have hh1 := hg.2.2.1 1
    have hh2 := hg.2.2.1 2
    have hh3 := hg.2.2.1 3
    have hc : candidate s z w h1 h2 hz hw eps = ![c 0,c 0,c 2,c 3] := by
      ext i
      fin_cases i <;> rfl
    rw [hc]
    apply hull_of_inequalities
    · simpa [bary, c] using hh3.le
    · simpa [bary, c] using hh1.le
    · simpa [bary, c] using hh2.le
    · have hh : 0 ≤ 1+c 0-c 2-c 3 := by simpa [bary, c] using hh0.le
      linarith
  · intro i
    have hsq : 0 < eps^2 := pow_pos heps 2
    have hgp : 0 < eps^2*insideG s z w h1 h2 hz hw i eps := mul_pos hsq (hg.1 i)
    have hfp : 0 < eps^2*insideF s z w h1 h2 hz hw i eps := mul_pos hsq (hg.2.1 i)
    rw [← gainG s z w h1 h2 hz hw eps i] at hgp
    rw [← gainF s z w h1 h2 hz hw eps i] at hfp
    constructor <;> linarith

#print axioms universal_strict_repair

end ANDRepair
