import GeneratedLiveController
import SupportStageCertificate

noncomputable section
open scoped BigOperators
open Finset

namespace Orthemology.Tranche2
variable {Θ A Y : Type*} [DecidableEq Θ] [DecidableEq A]

def supportUpdate (P : Θ → A → Y → ℝ) (B : Finset Θ) (a : A) (y : Y) : Finset Θ := by
  classical
  exact B.filter (fun θ => 0 < P θ a y)

omit [DecidableEq Θ] [DecidableEq A] in
lemma supportUpdate_subset (P : Θ → A → Y → ℝ) (B : Finset Θ) (a : A) (y : Y) :
    supportUpdate P B a y ⊆ B := Finset.filter_subset _ _

omit [DecidableEq Θ] [DecidableEq A] in
lemma mem_supportUpdate (P : Θ → A → Y → ℝ) (B : Finset Θ) (a : A) (y : Y) (θ : Θ) :
    θ ∈ supportUpdate P B a y ↔ θ ∈ B ∧ 0 < P θ a y := by simp [supportUpdate]

def supportStay (P : Θ → A → Y → ℝ) (B : Finset Θ) (a : A) (y : Y) : Bool := by
  classical
  exact decide (supportUpdate P B a y = B)

omit [DecidableEq A] in
lemma supportStay_false (P : Θ → A → Y → ℝ) (B : Finset Θ) (a : A) (y : Y) :
    supportStay P B a y = false ↔ supportUpdate P B a y ≠ B := by simp [supportStay]

/-- The recursive witness form of SE-CIRS. Recursive premises occur only at
nonempty strict observation successors. The relation contains no probability
of winning, controller existence, or almost-sure conclusion. -/
inductive RecursiveWinning (P : Θ → A → Y → ℝ) (good : Θ → Finset A)
    (menu : Finset Θ → Finset A) : Finset Θ → Prop
  | intro (B : Finset Θ) (nonempty : B.Nonempty) (acts : Θ → List A)
      (hne : ∀ σ ∈ B, acts σ ≠ [])
      (licensed : ∀ σ ∈ B, (acts σ).toFinset ⊆ menu B)
      (continuation : ∀ σ ∈ B, ∀ a ∈ acts σ, ∀ y, (supportUpdate P B a y).Nonempty →
          supportUpdate P B a y ≠ B → RecursiveWinning P good menu (supportUpdate P B a y))
      (certificate : ∀ σ ∈ B,
        (∃ a ∈ acts σ, ∃ y, supportStay P B a y = false ∧ 0 < P σ a y) ∨
          LiveSelfVerifying P good B σ (acts σ)) : RecursiveWinning P good menu B

lemma recursiveWinning_nonempty (P : Θ → A → Y → ℝ) (good : Θ → Finset A)
    (menu : Finset Θ → Finset A) {B : Finset Θ} (h : RecursiveWinning P good menu B) : B.Nonempty := by
  cases h with
  | intro B hn _ _ _ _ _ => exact hn

lemma recursiveWinning_witness (P : Θ → A → Y → ℝ) (good : Θ → Finset A)
    (menu : Finset Θ → Finset A) {B : Finset Θ} (h : RecursiveWinning P good menu B) :
    ∀ σ ∈ B, ∃ acts : List A,
      acts ≠ [] ∧ acts.toFinset ⊆ menu B ∧
      (∀ a ∈ acts, ∀ y, (supportUpdate P B a y).Nonempty →
        supportUpdate P B a y ≠ B → RecursiveWinning P good menu (supportUpdate P B a y)) ∧
      ((∃ a ∈ acts, ∃ y, supportStay P B a y = false ∧ 0 < P σ a y) ∨
        LiveSelfVerifying P good B σ acts) := by
  cases h with
  | intro B _ acts hn hm hc hs =>
    intro σ hσ
    exact ⟨acts σ, hn σ hσ, hm σ hσ, hc σ hσ, hs σ hσ⟩

/-- This is exactly the continuation menu used by the bottom-up recursion. -/
def recursiveAllowed (P : Θ → A → Y → ℝ) (good : Θ → Finset A)
    (menu : Finset Θ → Finset A) (B : Finset Θ) : Finset A := by
  classical
  exact (menu B).filter (fun a => ∀ y, (supportUpdate P B a y).Nonempty →
    supportUpdate P B a y ≠ B → RecursiveWinning P good menu (supportUpdate P B a y))

/-- Every recursive witness list lies in the exact admissible continuation menu. -/
lemma recursive_witness_allowed (P : Θ → A → Y → ℝ) (good : Θ → Finset A)
    (menu : Finset Θ → Finset A) (B : Finset Θ) (acts : List A)
    (hm : acts.toFinset ⊆ menu B)
    (hc : ∀ a ∈ acts, ∀ y, (supportUpdate P B a y).Nonempty →
      supportUpdate P B a y ≠ B → RecursiveWinning P good menu (supportUpdate P B a y)) :
    acts.toFinset ⊆ recursiveAllowed P good menu B := by
  classical
  intro a ha
  exact Finset.mem_filter.mpr ⟨hm ha, hc a (List.mem_toFinset.mp ha)⟩

end Orthemology.Tranche2
