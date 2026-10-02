import SeededPolicyEquivalence

noncomputable section
open MeasureTheory ProbabilityTheory Filter Finset
open scoped BigOperators
namespace Orthemology.Tranche2.MicroPolicy
open PolicyEmbedding
universe u v w
variable {R : Type v} {A Y : Type u} {Θ : Type w}
    [Fintype Θ] [Fintype A] [Fintype Y] [DecidableEq A] [Inhabited Y]
    [MeasurableSpace R] [MeasurableSpace A] [MeasurableSingletonClass A]
    [MeasurableSpace Y] [MeasurableSingletonClass Y]

omit [Fintype Θ] [Fintype A] [Fintype Y] [Inhabited Y] [MeasurableSpace A] [MeasurableSingletonClass A] [MeasurableSpace Y] [MeasurableSingletonClass Y] in
lemma queue_mem_menu (plan : Θ → List A) (choose : History A Y → Θ) (Γ : Finset A)
    (hplan : ∀ σ a, a ∈ plan σ → a ∈ Γ) (h : History A Y) :
    ∀ a ∈ queue plan choose h, a ∈ Γ := by
  induction h with
  | nil => exact hplan _
  | cons z h ih =>
    simp only [queue]
    split_ifs with he
    · exact hplan _
    · intro a ha
      exact ih a (List.mem_of_mem_tail ha)

omit [Fintype A] [MeasurableSpace R] [Inhabited Y] [Fintype Y] [MeasurableSpace A] [MeasurableSingletonClass A] [MeasurableSpace Y] [MeasurableSingletonClass Y] in
/-- Every action issued on every history is licensed. This concerns the common
static menu, separately from eventual true-target acceptance. -/
theorem sharedPolicy_mem_menu (P : Θ → A → Y → ℝ) (support : Θ → Finset A)
    (initial : Θ) (d : A) (Γ : Finset A)
    (hne : ∀ σ, (support σ).Nonempty) (hmenu : ∀ σ, support σ ⊆ Γ)
    (r : R) (h : History A Y) : sharedPolicy P support initial d r h ∈ Γ := by
  apply queue_mem_menu (supportPlan support) (chooseMLE P initial) Γ
    (fun σ a ha => hmenu σ (by simpa [supportPlan] using ha)) h
  exact headD_mem_of_nonempty _ d
    (queue_nonempty _ _ (supportPlan_nonempty support hne) h)

omit [Fintype A] [DecidableEq A] in
lemma measurableSet_always_mem (Γ : Finset A) :
    MeasurableSet {x : ℕ → A | ∀ n, x n ∈ Γ} := by
  have he : {x : ℕ → A | ∀ n, x n ∈ Γ} = ⋂ n : ℕ, {x : ℕ → A | x n ∈ Γ} := by
    ext x
    simp
  rw [he]
  exact MeasurableSet.iInter (fun n => Γ.measurableSet.preimage (measurable_pi_apply n))

/-- A pointwise licensed history policy produces only licensed actions under
its actual canonical experiment. -/
theorem actionLaw_always_licensed (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1)
    (d : A) (Γ : Finset A) (hlegal : ∀ r h, π r h ∈ Γ) :
    ∀ᵐ x ∂actionLaw π ρ P hP hN d, ∀ n, x n ∈ Γ := by
  apply actionLaw_ae_of_stack π hπ ρ P hP hN d _ (measurableSet_always_mem Γ)
  exact Filter.Eventually.of_forall (fun z n => hlegal _ _)

/-- Explicit common-static-menu version of the exact same-runner theorem.
All issued actions are licensed, including the finitely many target errors. -/
theorem licensed_seeded_policy_exists_iff_kernel_nonempty
    (P : Θ → A → Y → ℝ) (good : Θ → Finset A) (Γ : Finset A) (initial : Θ) (d : A)
    (ρ : Measure R) [IsProbabilityMeasure ρ]
    (hP : ∀ σ a y, 0 < P σ a y) (hN : ∀ σ a, ∑ y, P σ a y = 1) :
    (∃ π : R → History A Y → A,
      Measurable (fun z : R × History A Y => π z.1 z.2) ∧
      (∀ r h, π r h ∈ Γ) ∧
      ∀ θ, ∀ᵐ x ∂actionLaw π ρ (P θ) (fun a y => (hP θ a y).le) (hN θ) d,
        ∀ᶠ t in atTop, x t ∈ good θ) ↔
      ∀ θ, (supportKernel (fun θ => good θ ∩ Γ)
        (fun η ζ a => P η a = P ζ a) θ).Nonempty := by
  constructor
  · rintro ⟨π,hπ,hlegal,hgood⟩ θ
    apply seeded_policy_kernel_nonempty P (fun θ => good θ ∩ Γ) hP hN π hπ ρ d
    intro η
    have hall := actionLaw_always_licensed π hπ ρ (P η) (fun a y => (hP η a y).le) (hN η) d Γ hlegal
    filter_upwards [hgood η,hall] with x hx hl
    filter_upwards [hx] with t ht
    exact Finset.mem_inter.mpr ⟨ht,hl t⟩
  · intro hk
    let target := fun θ => good θ ∩ Γ
    let support := fun θ => supportKernel target (fun η ζ a => P η a = P ζ a) θ
    have hsv : ∀ θ, SelfVerifying target (fun η ζ a => P η a = P ζ a) θ (support θ) :=
      fun θ => supportKernel_selfVerifying target _ θ
    refine ⟨sharedPolicy P support initial d, sharedPolicy_measurable P support initial d, ?_, ?_⟩
    · exact sharedPolicy_mem_menu P support initial d Γ hk
        (fun θ a ha => (Finset.mem_inter.mp ((hsv θ).1 ha)).2)
    · intro θ
      have hs := shared_policy_actionLaw_eventually_good P target support θ initial d ρ hP hN hk hsv
      filter_upwards [hs] with x hx
      filter_upwards [hx] with t ht
      exact (Finset.mem_inter.mp ht).1

end Orthemology.Tranche2.MicroPolicy
