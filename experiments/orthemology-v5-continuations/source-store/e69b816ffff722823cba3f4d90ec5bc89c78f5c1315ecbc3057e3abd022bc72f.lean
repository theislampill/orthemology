import SelfVerifyingSupport

/-!
# Support-stage certificate interface

An exact finite equivalence between the maximal-support certificate and the
existence of explicit action supports. The stochastic interpretation and
well-founded support recursion are stated/proved in the ordinary report, not
silently introduced as axioms here.
-/

namespace Orthemology.Tranche2

variable {Θ A Y : Type*} [DecidableEq A]

/-- At one live-model stage, each candidate either progresses or supplies a
nonempty support accepted by every rival it cannot distinguish on that support. -/
def StageWitness (good : Θ → Finset A) (same : Θ → Θ → A → Prop)
    (allowed : Finset A) (progress : Θ → Prop) : Prop :=
  ∀ θ, progress θ ∨ ∃ U : Finset A,
    U.Nonempty ∧ U ⊆ allowed ∧ SelfVerifying good same θ U

/-- Restrict every model's target by the exact common action menu. -/
def RestrictedTargets (good : Θ → Finset A) (allowed : Finset A) (θ : Θ) : Finset A :=
  good θ ∩ allowed

theorem selfVerifying_restrict_iff (good : Θ → Finset A)
    (same : Θ → Θ → A → Prop) (allowed : Finset A) (θ : Θ) (U : Finset A) :
    SelfVerifying (RestrictedTargets good allowed) same θ U ↔
      U ⊆ allowed ∧ SelfVerifying good same θ U := by
  constructor
  · rintro ⟨hbase, hothers⟩
    have hallow : U ⊆ allowed := by
      intro a ha
      exact (Finset.mem_inter.mp (hbase ha)).2
    refine ⟨hallow, ?_, ?_⟩
    · intro a ha
      exact (Finset.mem_inter.mp (hbase ha)).1
    · intro σ heq a ha
      exact (Finset.mem_inter.mp (hothers σ heq ha)).1
  · rintro ⟨hallow, hbase, hothers⟩
    constructor
    · intro a ha
      exact Finset.mem_inter.mpr ⟨hbase ha, hallow ha⟩
    · intro σ heq a ha
      exact Finset.mem_inter.mpr ⟨hothers σ heq ha, hallow ha⟩

/-- No implication about actual almost-sure winning is hidden in this definition. -/
def StageCertificate (good : Θ → Finset A) (same : Θ → Θ → A → Prop)
    (allowed : Finset A) (progress : Θ → Prop) : Prop :=
  ∀ θ, progress θ ∨ (supportKernel (RestrictedTargets good allowed) same θ).Nonempty

theorem stageCertificate_iff_witness (good : Θ → Finset A)
    (same : Θ → Θ → A → Prop) (allowed : Finset A) (progress : Θ → Prop) :
    StageCertificate good same allowed progress ↔ StageWitness good same allowed progress := by
  constructor
  · intro h θ
    rcases h θ with hp | hk
    · exact Or.inl hp
    · right
      obtain ⟨U, hU, hv⟩ :=
        (supportKernel_nonempty_iff (RestrictedTargets good allowed) same θ).mp hk
      obtain ⟨ha, hs⟩ := (selfVerifying_restrict_iff good same allowed θ U).mp hv
      exact ⟨U, hU, ha, hs⟩
  · intro h θ
    rcases h θ with hp | ⟨U, hU, ha, hs⟩
    · exact Or.inl hp
    · right
      apply (supportKernel_nonempty_iff (RestrictedTargets good allowed) same θ).mpr
      exact ⟨U, hU, (selfVerifying_restrict_iff good same allowed θ U).mpr ⟨ha, hs⟩⟩

omit [DecidableEq A] in
/-- A signal garbling may add indistinguishable rivals, never remove them. -/
theorem selfVerifying_signal_refinement (good : Θ → Finset A)
    (fine coarse : Θ → Θ → A → Prop)
    (h : ∀ θ σ a, fine θ σ a → coarse θ σ a)
    (θ : Θ) (U : Finset A) (hv : SelfVerifying good coarse θ U) :
    SelfVerifying good fine θ U := by
  refine ⟨hv.1, ?_⟩
  intro σ heq
  apply hv.2 σ
  intro a ha
  exact h θ σ a (heq a ha)

omit [DecidableEq A] in
theorem supportKernel_signal_refinement (good : Θ → Finset A)
    (fine coarse : Θ → Θ → A → Prop)
    (h : ∀ θ σ a, fine θ σ a → coarse θ σ a) (θ : Θ) :
    supportKernel good coarse θ ⊆ supportKernel good fine θ := by
  apply supportKernel_greatest good fine θ
  exact selfVerifying_signal_refinement good fine coarse h θ _
    (supportKernel_selfVerifying good coarse θ)

omit [DecidableEq A] in
theorem supportKernel_target_enlargement (good better : Θ → Finset A)
    (same : Θ → Θ → A → Prop) (h : ∀ θ, good θ ⊆ better θ) (θ : Θ) :
    supportKernel good same θ ⊆ supportKernel better same θ := by
  apply supportKernel_greatest better same θ
  have hv := supportKernel_selfVerifying good same θ
  refine ⟨Finset.Subset.trans hv.1 (h θ), ?_⟩
  intro σ heq
  exact Finset.Subset.trans (hv.2 σ heq) (h σ)

end Orthemology.Tranche2
