import Mathlib.SetTheory.Cardinal.Finite
import Mathlib.Data.Fintype.EquivFin
import Mathlib.Tactic

/-!
# A sharp finite-height potential for partial-equivalence refinement

A partial equivalence relation is symmetric and transitive, but its diagonal domain
may shrink. Completing it on two tagged copies makes each removed state contribute
two singleton classes; active classes contribute one class each. Thus quotient
cardinality is the potential `2 * (m - domain.card) + active_classes` in the paper.
The proof below needs no arbitrary representative choice in the relation itself.
-/

namespace Orthemology.Frontier

structure PER (S : Type*) where
  rel : S → S → Prop
  symm : Symmetric rel
  trans : Transitive rel

namespace PER

variable {S : Type*}

/-- A total equivalence on two tagged copies of each state. -/
def completion (R : PER S) : Setoid (S × Bool) where
  r x y := x = y ∨ R.rel x.1 y.1
  iseqv := {
    refl := fun _ => Or.inl rfl
    symm := by
      intro x y h
      exact h.elim (fun e => Or.inl e.symm) (fun r => Or.inr (R.symm r))
    trans := by
      intro x y z hxy hyz
      rcases hxy with rfl | hxy
      · exact hyz
      rcases hyz with rfl | hyz
      · exact Or.inr hxy
      · exact Or.inr (R.trans hxy hyz) }

noncomputable def potential (R : PER S) : ℕ := Nat.card (Quotient R.completion)

/-- Refinement induces a surjection from fine classes onto coarse classes. -/
def coarseMap (R E : PER S) (sub : ∀ s t, E.rel s t → R.rel s t) :
    Quotient E.completion → Quotient R.completion :=
  Quotient.map id (by
    intro x y h
    exact h.elim Or.inl (fun hr => Or.inr (sub _ _ hr)))

theorem coarseMap_surjective (R E : PER S)
    (sub : ∀ s t, E.rel s t → R.rel s t) :
    Function.Surjective (coarseMap R E sub) := by
  intro q
  refine Quotient.inductionOn q ?_
  intro x
  exact ⟨Quotient.mk _ x, rfl⟩

/-- A lost pair always separates the opposite-tag representatives. -/
theorem coarseMap_not_injective (R E : PER S)
    (sub : ∀ s t, E.rel s t → R.rel s t)
    (strict : ∃ s t, R.rel s t ∧ ¬ E.rel s t) :
    ¬ Function.Injective (coarseMap R E sub) := by
  intro hinj
  obtain ⟨s, t, hR, hE⟩ := strict
  have hcoarse : coarseMap R E sub (Quotient.mk _ (s, false)) =
      coarseMap R E sub (Quotient.mk _ (t, true)) :=
    Quotient.sound (Or.inr hR)
  have hfine := Quotient.exact (hinj hcoarse)
  rcases hfine with heq | hrel
  · have : false = true := congrArg Prod.snd heq
    contradiction
  · exact hE hrel

/-- Every proper partial-equivalence refinement strictly raises the potential. -/
theorem potential_strict [Finite S] (R E : PER S)
    (sub : ∀ s t, E.rel s t → R.rel s t)
    (strict : ∃ s t, R.rel s t ∧ ¬ E.rel s t) :
    R.potential < E.potential := by
  have hs := coarseMap_surjective R E sub
  have hn := coarseMap_not_injective R E sub strict
  by_contra h
  exact hn (hs.bijective_of_nat_card_le (Nat.le_of_not_gt h)).1

/-- There are at most two classes per original state. -/
theorem potential_le [Finite S] (R : PER S) : R.potential ≤ 2 * Nat.card S := by
  have h := Nat.card_le_card_of_surjective (Quotient.mk R.completion)
    Quotient.mk_surjective
  have hb : Nat.card Bool = 2 := by simp [Nat.card_eq_fintype_card]
  rw [Nat.card_prod, hb] at h
  simpa [potential, Nat.mul_comm] using h

/-- The starting universal relation has exactly one class when the state set is nonempty. -/
def universal : PER S where
  rel _ _ := True
  symm := by intro _ _ _; trivial
  trans := by intro _ _ _ _ _; trivial

theorem potential_universal [Nonempty S] : (universal : PER S).potential = 1 := by
  apply Nat.card_eq_one_iff_unique.mpr
  refine ⟨⟨?_⟩, ?_⟩
  · intro x y
    refine Quotient.inductionOn₂ x y ?_
    intro a b
    exact Quotient.sound (Or.inr trivial)
  · obtain ⟨s⟩ := ‹Nonempty S›
    exact ⟨Quotient.mk _ (s, false)⟩

@[ext] theorem ext {R E : PER S} (h : ∀ s t, R.rel s t ↔ E.rel s t) : R = E := by
  cases R with
  | mk r rs rt =>
    cases E with
    | mk e es et =>
      have : r = e := funext (fun s => funext (fun t => propext (h s t)))
      cases this
      rfl

/-- Strictness as inequality of the represented partial equivalences. -/
theorem potential_strict_of_ne [Finite S] (R E : PER S)
    (sub : ∀ s t, E.rel s t → R.rel s t) (hne : E ≠ R) :
    R.potential < E.potential := by
  apply potential_strict R E sub
  by_contra h
  push_neg at h
  apply hne
  apply ext
  intro s t
  exact ⟨sub s t, h s t⟩

/-- No strictly refining chain from the universal relation has length above `2m-1`. -/
theorem strict_chain_length [Finite S] [Nonempty S]
    (chain : ℕ → PER S) (initial : chain 0 = universal)
    (decreasing : ∀ n s t, (chain (n+1)).rel s t → (chain n).rel s t)
    (n : ℕ) (strict : ∀ k < n, chain (k+1) ≠ chain k) :
    n ≤ 2 * Nat.card S - 1 := by
  have growth : ∀ k ≤ n, k + 1 ≤ (chain k).potential := by
    intro k
    induction k with
    | zero =>
      intro _
      rw [initial, potential_universal]
    | succ k ih =>
      intro hk
      have hp := potential_strict_of_ne (chain k) (chain (k+1))
        (decreasing k) (strict k (by omega))
      have hg := ih (by omega)
      omega
  have hg := growth n le_rfl
  have hb := potential_le (chain n)
  omega

/-- Deterministic update turns one equality into permanent stationarity. -/
theorem stationary_after
    (chain : ℕ → PER S) (update : PER S → PER S)
    (recurrence : ∀ n, chain (n+1) = update (chain n))
    {n : ℕ} (eqn : chain (n+1) = chain n) (k : ℕ) :
    chain (n+k) = chain n := by
  induction k with
  | zero => simp
  | succ k ih =>
    rw [show n + (k+1) = (n+k)+1 by omega, recurrence, ih, ← recurrence, eqn]

/-- Any decreasing deterministic partial-equivalence iteration from top stabilizes by `2m-1`.
This uses an actual finite-state potential, not a supplied bound on chain length. -/
theorem stabilization_bound [Finite S] [Nonempty S]
    (chain : ℕ → PER S) (update : PER S → PER S)
    (initial : chain 0 = universal)
    (recurrence : ∀ n, chain (n+1) = update (chain n))
    (decreasing : ∀ n s t, (chain (n+1)).rel s t → (chain n).rel s t) :
    chain (2 * Nat.card S) = chain (2 * Nat.card S - 1) := by
  have positive : 0 < Nat.card S := Nat.card_pos
  by_contra hlast
  have strict : ∀ k < 2 * Nat.card S, chain (k+1) ≠ chain k := by
    intro k hk heq
    have ha := stationary_after chain update recurrence heq (2 * Nat.card S - k)
    have hb := stationary_after chain update recurrence heq (2 * Nat.card S - 1 - k)
    apply hlast
    have hka : k + (2 * Nat.card S - k) = 2 * Nat.card S := by omega
    have hkb : k + (2 * Nat.card S - 1 - k) = 2 * Nat.card S - 1 := by omega
    rw [hka] at ha
    rw [hkb] at hb
    exact ha.trans hb.symm
  have hbound := strict_chain_length chain initial decreasing (2 * Nat.card S) strict
  omega

end PER
end Orthemology.Frontier
