import ResetHellinger

noncomputable section
open scoped BigOperators
open Finset

namespace Orthemology.Tranche2
variable {Θ A Y : Type*} [DecidableEq Θ] [DecidableEq A] [Fintype Y]

def LiveSelfVerifying (P : Θ → A → Y → ℝ) (good : Θ → Finset A)
    (live : Finset Θ) (σ : Θ) (acts : List A) : Prop :=
  acts.toFinset ⊆ good σ ∧ ∀ η ∈ live, (∀ a ∈ acts, P σ a = P η a) → acts.toFinset ⊆ good η

omit [DecidableEq Θ] in
/-- Only rivals still in the support enter the self-verification test. -/
theorem live_certificate_implies_strict_residual
    (P : Θ → A → Y → ℝ) (good : Θ → Finset A) (stay : A → Y → Bool)
    (live : Finset Θ) (hP : ∀ θ a y, 0 ≤ P θ a y) (hNorm : ∀ θ a, ∑ y, P θ a y = 1)
    (θ σ : Θ) (hθ : θ ∈ live) (acts : List A)
    (hcert : (∃ a ∈ acts, ∃ y, stay a y = false ∧ 0 < P σ a y) ∨
      LiveSelfVerifying P good live σ acts)
    (hbad : ¬ acts.toFinset ⊆ good θ) :
    0 < 1-survivalAffinity (P θ) (P σ) stay acts := by
  apply sub_pos.mpr
  rcases hcert with hp | hs
  · exact survivalAffinity_lt_one_of_progress (P θ) (P σ) stay
      (hP θ) (hP σ) (hNorm θ) (hNorm σ) acts hp
  · have hi : ∃ a ∈ acts, P θ a ≠ P σ a := by
      by_contra! h
      exact hbad (hs.2 θ hθ (fun a ha => (h a ha).symm))
    exact survivalAffinity_lt_one_of_informative (P θ) (P σ) stay
      (hP θ) (hP σ) (hNorm θ) (hNorm σ) acts hi

omit [DecidableEq Θ] [DecidableEq A] [Fintype Y] in
lemma greedyMax_mem (score : Θ → ℝ) (initial : Θ) (cs : List Θ) :
    greedyMax score initial cs = initial ∨ greedyMax score initial cs ∈ cs := by
  induction cs generalizing initial with
  | nil => exact Or.inl rfl
  | cons c cs ih =>
    unfold greedyMax
    split_ifs
    · rcases ih c with heq | hmem
      · exact Or.inr (List.mem_cons.mpr (Or.inl heq))
      · exact Or.inr (List.mem_cons.mpr (Or.inr hmem))
    · rcases ih initial with heq | hmem
      · exact Or.inl heq
      · exact Or.inr (List.mem_cons.mpr (Or.inr hmem))

section Select
variable {B : Θ → Type*} [Fintype Θ] [∀ a, Fintype (B a)]

omit [DecidableEq Θ] [Fintype Θ] in
theorem greedyMax_live_mem (score : Θ → ℝ) (live : Finset Θ) (initial : Θ)
    (hi : initial ∈ live) : greedyMax score initial live.toList ∈ live := by
  rcases greedyMax_mem score initial live.toList with heq | hmem
  · simpa only [heq] using hi
  · simpa using hmem

end Select
end Orthemology.Tranche2
