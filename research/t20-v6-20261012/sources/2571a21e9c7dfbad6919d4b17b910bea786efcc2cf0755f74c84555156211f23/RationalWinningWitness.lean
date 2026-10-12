import RationalWinningCorrectness

noncomputable section
open scoped BigOperators
open Finset
open Orthemology.Tranche2
namespace Orthemology.Tranche4.RationalWinning
variable {m k l : ℕ}

/-- A displayed list satisfies the original recursive source-certificate
interface. This is not yet a compiled infinite restoring controller. -/
def PlanCertificate (T : Tables m k l) (B : Finset (Fin m)) (θ : Fin m)
    (acts : List (Fin k)) : Prop :=
  acts ≠ [] ∧ acts.toFinset ⊆ T.menu B ∧
    (∀ a ∈ acts, ∀ y, (supportUpdate (realKernel T) B a y).Nonempty →
      supportUpdate (realKernel T) B a y ≠ B →
        RecursiveWinning (realKernel T) T.good T.menu (supportUpdate (realKernel T) B a y)) ∧
    ((∃ a ∈ acts, ∃ y, supportStay (realKernel T) B a y = false ∧ 0 < realKernel T θ a y) ∨
      LiveSelfVerifying (realKernel T) T.good B θ acts)

@[simp] lemma mem_orderedActions (U : Finset (Fin k)) (a : Fin k) : a ∈ orderedActions U ↔ a ∈ U := by
  simp [orderedActions,List.mem_finRange]

lemma checked_support_certificate (T : Tables m k l) (B : Finset (Fin m))
    (θ : Fin m) (U : Finset (Fin k))
    (h : planCheck T (wins T (B.card-1)) B θ U = true) :
    PlanCertificate T B θ (orderedActions U) := by
  classical
  have hd : U.Nonempty ∧ (∀ a ∈ U, admissible T (wins T (B.card-1)) B a = true) ∧
      ((∃ a ∈ U, ∃ y, update T B a y ≠ B ∧ 0 < T.kernel θ a y) ∨ verifies T B θ U) := by
    simpa only [planCheck,decide_eq_true_eq,progresses_iff] using h
  refine ⟨orderedActions_ne_nil U hd.1,?_,?_,?_⟩
  · rw [orderedActions_toFinset]
    intro a ha
    exact ((admissible_iff T _ B a).mp (hd.2.1 a ha)).1
  · intro a ha y hy hne
    rw [supportUpdate_cast] at hy hne ⊢
    have hw := ((admissible_iff T _ B a).mp (hd.2.1 a ((mem_orderedActions U a).mp ha))).2 y hy hne
    have hc := update_card_lt T B a y hne
    exact (wins_correct_of_card_le T (B.card-1) _ (by omega)).mp hw
  · rcases hd.2.2 with hp | hv
    · left
      obtain ⟨a,ha,y,hne,hpos⟩ := hp
      refine ⟨a,(mem_orderedActions U a).mpr ha,y,?_,?_⟩
      · simpa only [supportStay_false,supportUpdate_cast] using hne
      · change (0:ℝ) < (T.kernel θ a y : ℝ)
        exact_mod_cast hpos
    · right
      refine ⟨?_,?_⟩
      · simpa only [orderedActions_toFinset] using hv.1
      · intro η hη heq
        rw [orderedActions_toFinset]
        apply hv.2 η hη
        intro a ha
        exact (realKernel_eq_iff T θ η a).mp (heq a ((mem_orderedActions U a).mpr ha))

/-- The public winning result yields a concrete deterministic list for every
live candidate, using one less fuel for proper support continuations. -/
theorem winningPlan_exists (T : Tables m k l) (B : Finset (Fin m))
    (hw : decideWinning T B = .winning) (θ : Fin m) (hθ : θ ∈ B) :
    ∃ acts, winningPlan T B θ = some acts := by
  have hr := (decideWinning_winning_iff T B).mp hw |>.2
  have hb := recursiveWinning_nonempty (realKernel T) T.good T.menu hr
  have he : B.card-1+1 = B.card := Nat.sub_add_cancel (card_pos.mpr hb)
  have hh : wins T (B.card-1+1) B = true := by
    rw [he]
    exact (wins_card_iff T B).mpr hr
  obtain ⟨U,hU⟩ := selectedSupport_exists T (B.card-1) B hh θ hθ
  exact ⟨orderedActions U,by simp [winningPlan,hw,selectedActions,hU]⟩

/-- Every returned list is valid; invalid/empty/losing inputs return no public
witness. No Classical.choose enters the executable selection definition. -/
theorem winningPlan_spec (T : Tables m k l) (B : Finset (Fin m)) (θ : Fin m)
    (acts : List (Fin k)) (h : winningPlan T B θ = some acts) :
    validTable T = true ∧ θ ∈ B ∧ PlanCertificate T B θ acts := by
  classical
  by_cases hw : decideWinning T B = .winning
  · have hv := ((decideWinning_winning_iff T B).mp hw).1
    cases hs : selectedSupport T (B.card-1) B θ with
    | none => simp [winningPlan,hw,selectedActions,hs] at h
    | some U =>
      have he : orderedActions U = acts := by simpa [winningPlan,hw,selectedActions,hs] using h
      rw [←he]
      have hu := selectedSupport_spec T (B.card-1) B θ U hs
      exact ⟨hv,hu.1,checked_support_certificate T B θ U hu.2⟩
  · simp [winningPlan,hw] at h

theorem winningPlan_none_of_not_live (T : Tables m k l) (B : Finset (Fin m)) (θ : Fin m)
    (hθ : θ ∉ B) : winningPlan T B θ = none := by
  simp [winningPlan,selectedActions,selectedSupport,hθ]

/-- Returned plans lead only to children that this same executable checker
classifies as winning, whenever an observation causes a live proper shrink. -/
theorem winningPlan_successors_win (T : Tables m k l) (B : Finset (Fin m)) (θ : Fin m)
    (acts : List (Fin k)) (h : winningPlan T B θ = some acts)
    (a : Fin k) (ha : a ∈ acts) (y : Fin l)
    (hy : (update T B a y).Nonempty) (hne : update T B a y ≠ B) :
    decideWinning T (update T B a y) = .winning := by
  have hs := winningPlan_spec T B θ acts h
  apply (decideWinning_winning_iff T _).mpr
  refine ⟨hs.1,?_⟩
  have hc := hs.2.2.2.2.1 a ha y
  simpa only [supportUpdate_cast] using hc (by simpa only [supportUpdate_cast] using hy)
    (by simpa only [supportUpdate_cast] using hne)

end Orthemology.Tranche4.RationalWinning
