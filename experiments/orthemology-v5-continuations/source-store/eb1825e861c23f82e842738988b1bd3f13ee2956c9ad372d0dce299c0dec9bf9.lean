import SupportStageCertificate

namespace Orthemology.Tranche2.Fixtures

/-- Models 0 and 1 agree on both actions; model 2 differs only at action 1. -/
def cascadeSame (θ σ : Fin 3) (a : Fin 2) : Prop :=
  (θ = 2 ∧ a = 1) ↔ (σ = 2 ∧ a = 1)

def cascadeGood (θ : Fin 3) : Finset (Fin 2) :=
  if θ = 0 then {0,1} else if θ = 1 then {0} else {1}

theorem cascade_no_nonempty_support (U : Finset (Fin 2))
    (h : SelfVerifying cascadeGood cascadeSame 0 U) : U = ∅ := by
  have hzero : U ⊆ ({0} : Finset (Fin 2)) := by
    have hsame : AgreeOn cascadeSame 0 1 U := by
      intro a ha
      simp [cascadeSame]
    simpa [cascadeGood] using h.2 1 hsame
  have hone : U ⊆ ({1} : Finset (Fin 2)) := by
    have hsame : AgreeOn cascadeSame 0 2 U := by
      intro a ha
      have ha0 : a = 0 := Finset.mem_singleton.mp (hzero ha)
      simp [cascadeSame, ha0]
    simpa [cascadeGood] using h.2 2 hsame
  apply Finset.eq_empty_iff_forall_not_mem.mpr
  intro a ha
  have h0 : a = 0 := Finset.mem_singleton.mp (hzero ha)
  have h1 : a = 1 := Finset.mem_singleton.mp (hone ha)
  have hf : (0 : Fin 2) = 1 := h0.symm.trans h1
  exact (by decide : (0 : Fin 2) ≠ 1) hf

theorem cascade_kernel_empty : supportKernel cascadeGood cascadeSame 0 = ∅ :=
  cascade_no_nonempty_support _ (supportKernel_selfVerifying cascadeGood cascadeSame 0)

/-- One pruning round keeps action 0, even though no nonempty valid support exists. -/
theorem cascade_first_round : prune cascadeGood cascadeSame 0 (cascadeGood 0) = {0} := by
  ext a
  fin_cases a <;> simp [prune, cascadeGood, cascadeSame, AgreeOn, Fin.forall_fin_succ]

theorem cascade_second_round : prune cascadeGood cascadeSame 0 {0} = ∅ := by
  ext a
  fin_cases a <;> simp [prune, cascadeGood, cascadeSame, AgreeOn, Fin.forall_fin_succ]

def informativeGood (θ : Fin 2) : Finset (Fin 2) := {θ}
def informativeSame (θ σ : Fin 2) (_a : Fin 2) : Prop := θ = σ

theorem informative_singleton_valid (θ : Fin 2) :
    SelfVerifying informativeGood informativeSame θ {θ} := by
  constructor
  · exact Finset.Subset.refl _
  · intro σ heq
    have hθσ : θ = σ := heq θ (Finset.mem_singleton_self _)
    subst σ
    exact Finset.Subset.refl _

theorem informative_kernel (θ : Fin 2) :
    supportKernel informativeGood informativeSame θ = {θ} := by
  apply Finset.Subset.antisymm
  · exact (supportKernel_selfVerifying informativeGood informativeSame θ).1
  · exact supportKernel_greatest informativeGood informativeSame θ (informative_singleton_valid θ)

theorem informative_all_kernels_nonempty :
    ∀ θ : Fin 2, (supportKernel informativeGood informativeSame θ).Nonempty := by
  intro θ
  rw [informative_kernel]
  exact Finset.singleton_nonempty _

theorem informative_no_common_target :
    ¬ ∃ a : Fin 2, ∀ θ : Fin 2, a ∈ informativeGood θ := by
  rintro ⟨a, ha⟩
  have h0 : a = 0 := Finset.mem_singleton.mp (ha 0)
  have h1 : a = 1 := Finset.mem_singleton.mp (ha 1)
  exact (by decide : (0 : Fin 2) ≠ 1) (h0.symm.trans h1)

end Orthemology.Tranche2.Fixtures
