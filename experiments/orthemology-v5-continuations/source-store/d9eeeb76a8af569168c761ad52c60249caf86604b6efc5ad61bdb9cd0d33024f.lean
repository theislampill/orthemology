import RecursiveWinningCertificate

noncomputable section
open Finset

namespace Orthemology.Tranche2
variable {Θ A Y : Type*} [Fintype Θ] [DecidableEq Θ] [DecidableEq A]

def recursiveProgress (P : Θ → A → Y → ℝ) (good : Θ → Finset A)
    (menu : Finset Θ → Finset A) (B : Finset Θ) (σ : {θ // θ ∈ B}) : Prop :=
  ∃ a ∈ recursiveAllowed P good menu B, ∃ y, supportStay P B a y = false ∧ 0 < P σ.val a y

omit [Fintype Θ] in
/-- The recursive witness predicate agrees exactly with the greatest-support
kernel test at each nonempty support. This binds the extracted controller to the
bottom-up criterion, rather than substituting a policy-success premise. -/
theorem recursiveWinning_iff_stage (P : Θ → A → Y → ℝ) (good : Θ → Finset A)
    (menu : Finset Θ → Finset A) (B : Finset Θ) :
    RecursiveWinning P good menu B ↔ B.Nonempty ∧
      StageCertificate (fun σ : {θ // θ ∈ B} => good σ.val)
        (fun η ζ a => P η.val a = P ζ.val a)
        (recursiveAllowed P good menu B) (recursiveProgress P good menu B) := by
  classical
  rw [stageCertificate_iff_witness]
  constructor
  · intro h
    refine ⟨recursiveWinning_nonempty P good menu h, ?_⟩
    intro σ
    obtain ⟨as,hn,hm,hc,hs⟩ := recursiveWinning_witness P good menu h σ.val σ.property
    have hadm := recursive_witness_allowed P good menu B as hm hc
    rcases hs with hp | hs
    · left
      obtain ⟨a,ha,y,hy,hpos⟩ := hp
      exact ⟨a,hadm (List.mem_toFinset.mpr ha),y,hy,hpos⟩
    · right
      refine ⟨as.toFinset, ?_, hadm, hs.1, ?_⟩
      · obtain ⟨a,ha⟩ := List.exists_mem_of_ne_nil as hn
        exact ⟨a,List.mem_toFinset.mpr ha⟩
      · intro η heq
        exact hs.2 η.val η.property (fun a ha => heq a (List.mem_toFinset.mpr ha))
  · rintro ⟨hb,hs⟩
    have hall : ∀ σ ∈ B, ∃ as : List A,
        as ≠ [] ∧ as.toFinset ⊆ menu B ∧
        (∀ a ∈ as, ∀ y, (supportUpdate P B a y).Nonempty → supportUpdate P B a y ≠ B →
          RecursiveWinning P good menu (supportUpdate P B a y)) ∧
        ((∃ a ∈ as, ∃ y, supportStay P B a y = false ∧ 0 < P σ a y) ∨
          LiveSelfVerifying P good B σ as) := by
      intro σ hσ
      rcases hs ⟨σ,hσ⟩ with hp | ⟨U,hU,hallow,hsv⟩
      · obtain ⟨a,ha,y,hy,hpos⟩ := hp
        obtain ⟨hm,hc⟩ := Finset.mem_filter.mp ha
        refine ⟨[a], by simp, ?_, ?_, Or.inl ⟨a,by simp,y,hy,hpos⟩⟩
        · simpa using hm
        · intro b hba z hz hne
          have he : b = a := by simpa using hba
          subst b
          exact hc z hz hne
      · refine ⟨U.toList, ?_, ?_, ?_, Or.inr ?_⟩
        · simpa using hU.ne_empty
        · intro a ha
          exact (Finset.mem_filter.mp (hallow (by simpa using ha))).1
        · intro a ha y hy hne
          exact (Finset.mem_filter.mp (hallow (Finset.mem_toList.mp ha))).2 y hy hne
        · constructor
          · simpa using hsv.1
          · intro η hη heq
            have h := hsv.2 ⟨η,hη⟩ (fun a ha => heq a (Finset.mem_toList.mpr ha))
            simpa using h
    let as : Θ → List A := fun σ => if h : σ ∈ B then Classical.choose (hall σ h) else []
    have has : ∀ σ (hσ : σ ∈ B), as σ = Classical.choose (hall σ hσ) := by
      intro σ hσ
      simp only [as, dif_pos hσ]
    apply RecursiveWinning.intro B hb as
    · intro σ hσ
      rw [has σ hσ]
      exact (Classical.choose_spec (hall σ hσ)).1
    · intro σ hσ
      rw [has σ hσ]
      exact (Classical.choose_spec (hall σ hσ)).2.1
    · intro σ hσ
      rw [has σ hσ]
      exact (Classical.choose_spec (hall σ hσ)).2.2.1
    · intro σ hσ
      rw [has σ hσ]
      exact (Classical.choose_spec (hall σ hσ)).2.2.2

end Orthemology.Tranche2
