import Mathlib

/-! Executable finite directed reachability, with soundness and completeness
against Mathlib's ordinary reflexive-transitive closure. -/
namespace HiddenParity.FiniteReachability

variable {State : Type*} [Fintype State] [DecidableEq State]
variable (r : State → State → Prop) [DecidableRel r]

/-- One exact forward-closure round. -/
def grow (R : Finset State) : Finset State :=
  R ∪ R.biUnion (fun s => Finset.univ.filter (r s))

@[simp] theorem mem_grow {R : Finset State} {t : State} :
    t ∈ grow r R ↔ t ∈ R ∨ ∃ s ∈ R, r s t := by
  simp [grow]

theorem subset_grow (R : Finset State) : R ⊆ grow r R := Finset.subset_union_left

/-- Finite fuel computes a forward-closed superset after at most |State| rounds. -/
def saturate : ℕ → Finset State → Finset State
  | 0, R => R
  | n + 1, R => saturate n (grow r R)

theorem subset_saturate (n : ℕ) (R : Finset State) : R ⊆ saturate r n R := by
  induction n generalizing R with
  | zero => exact Finset.Subset.refl R
  | succ n ih => exact (subset_grow r R).trans (ih _)

theorem saturate_eq_of_stable {R : Finset State} (h : grow r R = R) (n : ℕ) :
    saturate r n R = R := by
  induction n with
  | zero => rfl
  | succ n ih => simpa only [saturate, h] using ih

/-- A cardinal bound proves saturation; no maximum simple-path lemma is assumed. -/
theorem saturate_stable (n : ℕ) (R : Finset State)
    (hBound : Fintype.card State - R.card ≤ n) :
    grow r (saturate r n R) = saturate r n R := by
  induction n generalizing R with
  | zero =>
      have hCard : R.card = Fintype.card State := by
        have := Finset.card_le_card (Finset.subset_univ R)
        simp only [Finset.card_univ] at this
        omega
      have hR : R = Finset.univ :=
        Finset.eq_of_subset_of_card_le (Finset.subset_univ R) (by simp [hCard])
      subst R
      simp [saturate, grow]
  | succ n ih =>
      by_cases hs : grow r R = R
      · rw [saturate_eq_of_stable r hs]
        exact hs
      · have hStrict : R ⊂ grow r R :=
          Finset.ssubset_iff_subset_ne.mpr ⟨subset_grow r R, Ne.symm hs⟩
        have hCard := Finset.card_lt_card hStrict
        have hTop : (grow r R).card ≤ Fintype.card State := by
          simpa using Finset.card_le_card (Finset.subset_univ (grow r R))
        exact ih (grow r R) (by omega)

theorem saturate_sound (s : State) (n : ℕ) (R : Finset State)
    (hR : ∀ t ∈ R, Relation.ReflTransGen r s t) :
    ∀ t ∈ saturate r n R, Relation.ReflTransGen r s t := by
  induction n generalizing R with
  | zero => exact hR
  | succ n ih =>
      apply ih
      intro t ht
      rcases (mem_grow r).mp ht with ht | ⟨u, hu, hut⟩
      · exact hR t ht
      · exact (hR u hu).tail hut

/-- Executable complete reachable-state set, with fixed fuel |State|. -/
def reachable (s : State) : Finset State := saturate r (Fintype.card State) {s}

/-- Sound and complete with respect to unbounded ordinary directed reachability. -/
theorem reachable_iff (s t : State) :
    t ∈ reachable r s ↔ Relation.ReflTransGen r s t := by
  constructor
  · exact saturate_sound r s (Fintype.card State) {s} (by
      intro u hu
      have : u = s := Finset.mem_singleton.mp hu
      subst u
      exact Relation.ReflTransGen.refl) t
  · intro h
    have hClosed : ∀ u ∈ reachable r s, ∀ v, r u v → v ∈ reachable r s := by
      intro u hu v huv
      have hst : grow r (reachable r s) = reachable r s :=
        saturate_stable r (Fintype.card State) {s} (Nat.sub_le _ _)
      rw [← hst]
      exact (mem_grow r).mpr (Or.inr ⟨u, hu, huv⟩)
    have hStart : s ∈ reachable r s := subset_saturate r _ _ (Finset.mem_singleton_self s)
    induction h with
    | refl => exact hStart
    | tail _ hyz ih => exact hClosed _ ih _ hyz

end HiddenParity.FiniteReachability
