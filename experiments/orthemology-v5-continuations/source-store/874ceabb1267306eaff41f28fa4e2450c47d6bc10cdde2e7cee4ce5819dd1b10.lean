import CommonObservationFiniteActions

noncomputable section
open MeasureTheory Filter Set
open scoped Topology BigOperators

namespace Orthemology.Tranche2.CompactObservationBoundary

/-- One compact set that eventually contains the shared output under the
nonzero reference is sufficient; the entire action space need not be compact.
All target sets are closed in the declared ambient action topology. -/
theorem common_action_of_compact_confinement
    {Θ Ω A : Type*} [TopologicalSpace A] [MeasurableSpace Ω]
    (μ : Measure Ω) [NeZero μ] (ν : Θ → Measure Ω)
    (X : Ω → ℕ → A) (good : Θ → Set A) (C : Set A)
    (hcompact : IsCompact C) (hclosed : ∀ θ, IsClosed (good θ))
    (hdom : ∀ θ, μ ≪ ν θ)
    (hconfined : ∀ᵐ ω ∂μ, ∀ᶠ n in atTop, X ω n ∈ C)
    (hsuccess : ∀ θ, ∀ᵐ ω ∂ν θ, ∀ᶠ n in atTop, X ω n ∈ good θ) :
    ∃ a ∈ C, ∀ θ, a ∈ good θ := by
  classical
  have hs : ∀ θ, ∀ᵐ ω ∂μ, ∀ᶠ n in atTop, X ω n ∈ good θ := by
    intro θ
    exact (Measure.ae_le_iff_absolutelyContinuous.mpr (hdom θ)) (hsuccess θ)
  have hf : ∀ u : Finset Θ, (C ∩ ⋂ θ ∈ u, good θ).Nonempty := by
    intro u
    have hu : ∀ᵐ ω ∂μ, ∀ θ ∈ u, ∀ᶠ n in atTop, X ω n ∈ good θ :=
      (Filter.eventually_all_finset u).mpr (fun θ _ => hs θ)
    obtain ⟨ω,hωC,hω⟩ := (hconfined.and hu).exists
    have ht : ∀ᶠ n in atTop, ∀ θ ∈ u, X ω n ∈ good θ :=
      (Filter.eventually_all_finset u).mpr hω
    obtain ⟨n,hnC,hn⟩ := (hωC.and ht).exists
    exact ⟨X ω n, hnC, Set.mem_iInter₂.mpr hn⟩
  obtain ⟨a,haC,ha⟩ := hcompact.inter_iInter_nonempty good hclosed hf
  exact ⟨a,haC,Set.mem_iInter.mp ha⟩

/-- Compact whole action space is a special case, not a finiteness restriction
on the target index. -/
theorem common_action_of_compact_space
    {Θ Ω A : Type*} [TopologicalSpace A] [CompactSpace A] [MeasurableSpace Ω]
    (μ : Measure Ω) [NeZero μ] (ν : Θ → Measure Ω)
    (X : Ω → ℕ → A) (good : Θ → Set A)
    (hclosed : ∀ θ, IsClosed (good θ)) (hdom : ∀ θ, μ ≪ ν θ)
    (hsuccess : ∀ θ, ∀ᵐ ω ∂ν θ, ∀ᶠ n in atTop, X ω n ∈ good θ) :
    ∃ a, ∀ θ, a ∈ good θ := by
  obtain ⟨a,_,ha⟩ := common_action_of_compact_confinement μ ν X good Set.univ isCompact_univ
    hclosed hdom (Filter.Eventually.of_forall (fun _ => Filter.Eventually.of_forall (fun _ => Set.mem_univ _))) hsuccess
  exact ⟨a,ha⟩

/-- One compact target already supplies reference-law confinement, provided
success is available for that target and the AC direction is preserved. -/
theorem common_action_of_one_compact_target
    {Θ Ω A : Type*} [TopologicalSpace A] [MeasurableSpace Ω]
    (μ : Measure Ω) [NeZero μ] (ν : Θ → Measure Ω)
    (X : Ω → ℕ → A) (good : Θ → Set A) (θ0 : Θ)
    (hcompact : IsCompact (good θ0)) (hclosed : ∀ θ, IsClosed (good θ))
    (hdom : ∀ θ, μ ≪ ν θ)
    (hsuccess : ∀ θ, ∀ᵐ ω ∂ν θ, ∀ᶠ n in atTop, X ω n ∈ good θ) :
    ∃ a, ∀ θ, a ∈ good θ := by
  have hc := (Measure.ae_le_iff_absolutelyContinuous.mpr (hdom θ0)) (hsuccess θ0)
  obtain ⟨a,_,ha⟩ := common_action_of_compact_confinement μ ν X good (good θ0)
    hcompact hclosed hdom hc hsuccess
  exact ⟨a,ha⟩

def nonworseningTarget {Θ J A : Type*} (loss : Θ → J → A → ℝ)
    (baseline : Θ → J → ℝ) (θ : Θ) : Set A := {a | ∀ j, loss θ j a ≤ baseline θ j}

/-- Arbitrary intersections of continuous real-valued score sublevel sets are
closed. No finite number of standards or truth constraints is assumed. -/
lemma nonworseningTarget_closed {Θ J A : Type*} [TopologicalSpace A]
    (loss : Θ → J → A → ℝ) (baseline : Θ → J → ℝ)
    (hcont : ∀ θ j, Continuous (loss θ j)) (θ : Θ) :
    IsClosed (nonworseningTarget loss baseline θ) := by
  simp only [nonworseningTarget, Set.setOf_forall]
  exact isClosed_iInter (fun j => isClosed_le (hcont θ j) continuous_const)

/-- A direct bridge from actual full-path laws to one common coherent
nonworsening output on a compact action domain. -/
theorem common_nonworsening_of_continuous_scores
    {Θ J Ω A : Type*} [TopologicalSpace A] [MeasurableSpace Ω]
    (μ : Measure Ω) [NeZero μ] (ν : Θ → Measure Ω) (X : Ω → ℕ → A)
    (loss : Θ → J → A → ℝ) (baseline : Θ → J → ℝ)
    (hcont : ∀ θ j, Continuous (loss θ j)) (C : Set A) (hcompact : IsCompact C)
    (hdom : ∀ θ, μ ≪ ν θ)
    (hconfined : ∀ᵐ ω ∂μ, ∀ᶠ n in atTop, X ω n ∈ C)
    (hsuccess : ∀ θ, ∀ᵐ ω ∂ν θ, ∀ᶠ n in atTop, ∀ j, loss θ j (X ω n) ≤ baseline θ j) :
    ∃ a ∈ C, ∀ θ j, loss θ j a ≤ baseline θ j :=
  common_action_of_compact_confinement μ ν X (nonworseningTarget loss baseline) C hcompact
    (nonworseningTarget_closed loss baseline hcont) hdom hconfined hsuccess

section Quadratic
variable {ι : Type*} [Fintype ι]

def quadraticLoss (w v b : ι → ℝ) : ℝ := ∑ i, w i * (b i - v i)^2
lemma quadraticLoss_continuous (w v : ι → ℝ) : Continuous (quadraticLoss w v) := by
  unfold quadraticLoss
  fun_prop

/-- Concrete finite truth-hull / weighted-quadratic application. Positivity of
weights is not needed for closedness; normative score legitimacy is separate. -/
theorem common_finite_hull_quadratic_repair
    {Θ J Ω : Type*} [Fintype J] [MeasurableSpace Ω]
    (μ : Measure Ω) [NeZero μ] (ν : Θ → Measure Ω) (X : Ω → ℕ → (ι → ℝ))
    (w : Θ → ι → ℝ) (v : J → ι → ℝ) (b : ι → ℝ)
    (hdom : ∀ θ, μ ≪ ν θ)
    (hconfined : ∀ᵐ ω ∂μ, ∀ᶠ n in atTop, X ω n ∈ convexHull ℝ (Set.range v))
    (hsuccess : ∀ θ, ∀ᵐ ω ∂ν θ, ∀ᶠ n in atTop,
      ∀ j, quadraticLoss (w θ) (v j) (X ω n) ≤ quadraticLoss (w θ) (v j) b) :
    ∃ c ∈ convexHull ℝ (Set.range v), ∀ θ j,
      quadraticLoss (w θ) (v j) c ≤ quadraticLoss (w θ) (v j) b :=
  common_nonworsening_of_continuous_scores μ ν X
    (fun θ j => quadraticLoss (w θ) (v j)) (fun θ j => quadraticLoss (w θ) (v j) b)
    (fun θ j => quadraticLoss_continuous (w θ) (v j)) _
    (Set.finite_range v).isCompact_convexHull hdom hconfined hsuccess

end Quadratic
#print axioms common_action_of_compact_confinement
#print axioms common_action_of_compact_space
#print axioms common_action_of_one_compact_target
#print axioms nonworseningTarget_closed
#print axioms common_nonworsening_of_continuous_scores
#print axioms common_finite_hull_quadratic_repair
#check common_finite_hull_quadratic_repair
end Orthemology.Tranche2.CompactObservationBoundary
