import LikelihoodProducts
import SelfVerifyingSupport
import Mathlib.Data.Nat.Nth
import Mathlib.Order.Filter.Cofinite

/-!
# Verified maximum-likelihood support-block controller rule

Every selected block samples each action of its supplied support exactly once.
The prefix counters are defined, not assumed fair. The sole policy rule is that
its selected candidate maximizes the exact current finite likelihood product.
-/

noncomputable section
open MeasureTheory ProbabilityTheory Filter Finset
open scoped Topology

namespace Orthemology.Tranche2

variable {Θ A Y Ω : Type*} [Fintype Θ] [Fintype A] [Fintype Y]

/-- Exact number of samples from an action before a support block. -/
def blockCount (support : Θ → Finset A) (selected : ℕ → Θ) (a : A) (n : ℕ) : ℕ := by
  classical
  exact Nat.count (fun i => a ∈ support (selected i)) n

lemma count_tendsto_of_infinite {p : ℕ → Prop} [DecidablePred p]
    (hp : {n | p n}.Infinite) : Tendsto (Nat.count p) atTop atTop := by
  apply tendsto_atTop_atTop_of_monotone (Nat.count_monotone p)
  intro b
  exact ⟨Nat.nth p b, (Nat.count_nth_of_infinite hp b).ge⟩

omit [Fintype Θ] [Fintype A] in
lemma blockCount_tendsto_of_selected_infinite (support : Θ → Finset A)
    (selected : ℕ → Θ) (σ : Θ) (a : A) (ha : a ∈ support σ)
    (hinf : {n | selected n = σ}.Infinite) :
    Tendsto (blockCount support selected a) atTop atTop := by
  classical
  have ht := count_tendsto_of_infinite hinf
  apply tendsto_atTop_mono _ ht
  intro n
  unfold blockCount
  exact Nat.count_mono_left (fun i hi => by simpa [hi] using ha)

section Probability
variable [MeasurableSpace Y] [MeasurableSingletonClass Y]
variable [MeasurableSpace Ω] {μ : Measure Ω} [IsProbabilityMeasure μ]

/-- The central sufficient controller connection: actual finite observation laws
and the maximum-likelihood block rule imply eventual target-good blocks. -/
theorem likelihood_block_controller_eventually_good
    (P : Θ → A → Y → ℝ) (good support : Θ → Finset A) (θ : Θ)
    (X : A → ℕ → Ω → Y) (selected : Ω → ℕ → Θ)
    (hP : ∀ σ a y, 0 < P σ a y)
    (hPsum : ∀ σ a, ∑ y, P σ a y = 1)
    (hnonempty : ∀ σ, (support σ).Nonempty)
    (hsupport : ∀ σ, SelfVerifying good (fun η ζ a => P η a = P ζ a) σ (support σ))
    (hX : ∀ a n, Measurable (X a n))
    (hindep : iIndepFun (fun an : A × ℕ => X an.1 an.2) μ)
    (hident : ∀ a n, IdentDistrib (X a n) (X a 0) μ μ)
    (hLaw : ∀ a y, (Measure.map (X a 0) μ).real {y} = P θ a y)
    (hchoose : ∀ ω n σ,
      prefixLikelihood (P σ) X (fun a => blockCount support (selected ω) a n) ω ≤
      prefixLikelihood (P (selected ω n)) X
        (fun a => blockCount support (selected ω) a n) ω) :
    ∀ᵐ ω ∂μ, ∀ᶠ n : ℕ in atTop,
      (support (selected ω n)).Nonempty ∧ support (selected ω n) ⊆ good θ := by
  classical
  have hdrift : ∀ σ, ∀ᵐ ω ∂μ, ∀ N : A → ℕ → ℕ,
      (∃ a, P θ a ≠ P σ a ∧ Tendsto (N a) atTop atTop) →
      Tendsto (fun t => prefixLikelihood (P σ) X (fun a => N a t) ω /
        prefixLikelihood (P θ) X (fun a => N a t) ω) atTop (𝓝 0) := by
    intro σ
    exact sampled_false_likelihood_ratio_tendsto_zero (P θ) (P σ) X
      (hP θ) (hP σ) (hPsum θ) (hPsum σ) hX hindep hident hLaw
  have hall := ae_all_iff.mpr hdrift
  filter_upwards [hall] with ω hω
  have hav : ∀ σ, ∀ᶠ n : ℕ in atTop,
      selected ω n = σ → support σ ⊆ good θ := by
    intro σ
    by_cases hgood : support σ ⊆ good θ
    · exact Filter.Eventually.of_forall (fun _ _ => hgood)
    have hwitness : ∃ a ∈ support σ, P θ a ≠ P σ a := by
      by_contra! h
      apply hgood
      apply (hsupport σ).2 θ
      intro a ha
      exact (h a ha).symm
    obtain ⟨a, ha, hne⟩ := hwitness
    have hstop : ∀ᶠ n : ℕ in atTop, selected ω n ≠ σ := by
      by_contra hnot
      have hfreq : ∃ᶠ n : ℕ in atTop, selected ω n = σ := by
        simpa only [not_not] using (Filter.not_eventually.mp hnot)
      have hinf := Nat.frequently_atTop_iff_infinite.mp hfreq
      have hcount := blockCount_tendsto_of_selected_infinite support (selected ω) σ a ha hinf
      have hratio := hω σ (fun a n => blockCount support (selected ω) a n) ⟨a, hne, hcount⟩
      have hsmall : ∀ᶠ n : ℕ in atTop,
          prefixLikelihood (P σ) X (fun a => blockCount support (selected ω) a n) ω /
            prefixLikelihood (P θ) X (fun a => blockCount support (selected ω) a n) ω < 1 :=
        hratio.eventually (gt_mem_nhds (by norm_num : (0 : ℝ) < 1))
      have hexclude : ∀ᶠ n : ℕ in atTop, selected ω n ≠ σ := by
        filter_upwards [hsmall] with n hn
        intro heq
        have hmax := hchoose ω n θ
        rw [heq] at hmax
        have hden := prefixLikelihood_pos (P θ) X (hP θ)
          (fun a => blockCount support (selected ω) a n) ω
        have hlarge : 1 ≤ prefixLikelihood (P σ) X
            (fun a => blockCount support (selected ω) a n) ω /
              prefixLikelihood (P θ) X (fun a => blockCount support (selected ω) a n) ω := by
          apply (le_div_iff₀ hden).mpr
          simpa using hmax
        exact (not_le_of_gt hn) hlarge
      exact hnot hexclude
    filter_upwards [hstop] with n hn
    exact fun heq => False.elim (hn heq)
  filter_upwards [Filter.eventually_all.mpr hav] with n hn
  exact ⟨hnonempty _, hn (selected ω n) rfl⟩

end Probability
end Orthemology.Tranche2
