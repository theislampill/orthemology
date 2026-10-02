import Mathlib.Data.Finset.Powerset
import Mathlib.Data.Finset.Card
import Mathlib.Tactic

/-!
# Exact finite self-verifying target support

This file proves the finite combinatorial support kernel used by the ordinary
controlled-information restoration theorem. It does not formalize path measures,
likelihood convergence, or the almost-sure restoration equivalence.
-/

namespace Orthemology.Tranche2

variable {Θ A : Type*}

/-- Indistinguishability on every action of a proposed support. -/
def AgreeOn (same : Θ → Θ → A → Prop) (θ σ : Θ) (U : Finset A) : Prop :=
  ∀ a ∈ U, same θ σ a

/-- A support is accepted by its own target and every indistinguishable rival. -/
def SelfVerifying (good : Θ → Finset A) (same : Θ → Θ → A → Prop)
    (θ : Θ) (U : Finset A) : Prop :=
  U ⊆ good θ ∧ ∀ σ, AgreeOn same θ σ U → U ⊆ good σ

/-- Delete actions rejected by a rival still indistinguishable on the whole support. -/
noncomputable def prune (good : Θ → Finset A) (same : Θ → Θ → A → Prop)
    (θ : Θ) (U : Finset A) : Finset A := by
  classical
  exact U.filter (fun a => ∀ σ, AgreeOn same θ σ U → a ∈ good σ)

@[simp] theorem mem_prune (good : Θ → Finset A) (same : Θ → Θ → A → Prop)
    (θ : Θ) (U : Finset A) (a : A) :
    a ∈ prune good same θ U ↔ a ∈ U ∧ ∀ σ, AgreeOn same θ σ U → a ∈ good σ := by
  classical
  simp [prune]

theorem prune_subset (good : Θ → Finset A) (same : Θ → Θ → A → Prop)
    (θ : Θ) (U : Finset A) : prune good same θ U ⊆ U := by
  intro a ha
  exact (mem_prune good same θ U a).mp ha |>.1

theorem agreeOn_mono (same : Θ → Θ → A → Prop) (θ σ : Θ)
    {U V : Finset A} (hUV : U ⊆ V) (h : AgreeOn same θ σ V) :
    AgreeOn same θ σ U := by
  intro a ha
  exact h a (hUV ha)

theorem prune_mono (good : Θ → Finset A) (same : Θ → Θ → A → Prop)
    (θ : Θ) {U V : Finset A} (hUV : U ⊆ V) :
    prune good same θ U ⊆ prune good same θ V := by
  intro a ha
  rcases (mem_prune good same θ U a).mp ha with ⟨haU, hgood⟩
  exact (mem_prune good same θ V a).mpr
    ⟨hUV haU, fun σ h => hgood σ (agreeOn_mono same θ σ hUV h)⟩

theorem selfVerifying_empty (good : Θ → Finset A)
    (same : Θ → Θ → A → Prop) (θ : Θ) : SelfVerifying good same θ ∅ := by
  constructor
  · exact Finset.empty_subset _
  · intro σ _
    exact Finset.empty_subset _

theorem selfVerifying_union [DecidableEq A] (good : Θ → Finset A)
    (same : Θ → Θ → A → Prop) (θ : Θ) {U V : Finset A}
    (hU : SelfVerifying good same θ U) (hV : SelfVerifying good same θ V) :
    SelfVerifying good same θ (U ∪ V) := by
  constructor
  · exact Finset.union_subset hU.1 hV.1
  · intro σ h a ha
    rcases Finset.mem_union.mp ha with haU | haV
    · exact hU.2 σ (agreeOn_mono same θ σ Finset.subset_union_left h) haU
    · exact hV.2 σ (agreeOn_mono same θ σ Finset.subset_union_right h) haV

theorem selfVerifying_iff_fixed (good : Θ → Finset A)
    (same : Θ → Θ → A → Prop) (θ : Θ) (U : Finset A) :
    SelfVerifying good same θ U ↔ U ⊆ good θ ∧ prune good same θ U = U := by
  constructor
  · intro h
    refine ⟨h.1, Finset.Subset.antisymm (prune_subset good same θ U) ?_⟩
    intro a ha
    exact (mem_prune good same θ U a).mpr ⟨ha, fun σ heq => h.2 σ heq ha⟩
  · rintro ⟨hsub, hfix⟩
    refine ⟨hsub, ?_⟩
    intro σ heq a ha
    have hp : a ∈ prune good same θ U := by rw [hfix]; exact ha
    exact (mem_prune good same θ U a).mp hp |>.2 σ heq

/-- The descending iteration starts at the declared target. -/
noncomputable def pruneIter (good : Θ → Finset A)
    (same : Θ → Θ → A → Prop) (θ : Θ) : ℕ → Finset A
  | 0 => good θ
  | n + 1 => prune good same θ (pruneIter good same θ n)

theorem pruneIter_step_subset (good : Θ → Finset A)
    (same : Θ → Θ → A → Prop) (θ : Θ) (n : ℕ) :
    pruneIter good same θ (n+1) ⊆ pruneIter good same θ n :=
  prune_subset good same θ _

theorem pruneIter_subset_target (good : Θ → Finset A)
    (same : Θ → Θ → A → Prop) (θ : Θ) (n : ℕ) :
    pruneIter good same θ n ⊆ good θ := by
  induction n with
  | zero => exact Finset.Subset.refl _
  | succ n ih => exact Finset.Subset.trans (pruneIter_step_subset good same θ n) ih

theorem selfVerifying_survives (good : Θ → Finset A)
    (same : Θ → Θ → A → Prop) (θ : Θ) {U : Finset A}
    (hU : SelfVerifying good same θ U) (n : ℕ) :
    U ⊆ pruneIter good same θ n := by
  induction n with
  | zero => exact hU.1
  | succ n ih =>
    intro a ha
    apply (mem_prune good same θ (pruneIter good same θ n) a).mpr
    exact ⟨ih ha, fun σ heq => hU.2 σ (agreeOn_mono same θ σ ih heq) ha⟩

theorem pruneIter_fixed_propagates (good : Θ → Finset A)
    (same : Θ → Θ → A → Prop) (θ : Θ) {n : ℕ}
    (h : pruneIter good same θ (n+1) = pruneIter good same θ n) (k : ℕ) :
    pruneIter good same θ (n+k) = pruneIter good same θ n := by
  induction k with
  | zero => simp
  | succ k ih =>
    calc
      pruneIter good same θ (n+(k+1)) =
          prune good same θ (pruneIter good same θ (n+k)) := by
            simp only [Nat.add_succ, pruneIter]
            rfl
      _ = prune good same θ (pruneIter good same θ n) := by rw [ih]
      _ = pruneIter good same θ n := h

theorem pruneIter_card_bound_of_no_fixed (good : Θ → Finset A)
    (same : Θ → Θ → A → Prop) (θ : Θ) (n : ℕ)
    (h : ∀ k < n, pruneIter good same θ (k+1) ≠ pruneIter good same θ k) :
    (pruneIter good same θ n).card + n ≤ (good θ).card := by
  induction n with
  | zero => simp [pruneIter]
  | succ n ih =>
    have hind := ih (fun k hk => h k (Nat.lt_trans hk (Nat.lt_succ_self n)))
    have hsub := pruneIter_step_subset good same θ n
    have hne := h n (Nat.lt_succ_self n)
    have hlt : (pruneIter good same θ (n+1)).card <
        (pruneIter good same θ n).card := by
      apply Finset.card_lt_card
      exact Finset.ssubset_iff_subset_ne.mpr ⟨hsub, hne⟩
    omega

theorem pruneIter_exists_fixed (good : Θ → Finset A)
    (same : Θ → Θ → A → Prop) (θ : Θ) :
    ∃ n ≤ (good θ).card,
      pruneIter good same θ (n+1) = pruneIter good same θ n := by
  by_contra h
  push_neg at h
  have hc := pruneIter_card_bound_of_no_fixed good same θ ((good θ).card+1)
    (fun k hk => h k (by omega))
  omega

/-- A number of rounds equal to the original action count is always enough. -/
theorem pruneIter_card_fixed (good : Θ → Finset A)
    (same : Θ → Θ → A → Prop) (θ : Θ) :
    pruneIter good same θ ((good θ).card+1) =
      pruneIter good same θ (good θ).card := by
  obtain ⟨n, hn, hfix⟩ := pruneIter_exists_fixed good same θ
  have heq : n + ((good θ).card-n) = (good θ).card := Nat.add_sub_of_le hn
  have h0 := pruneIter_fixed_propagates good same θ hfix ((good θ).card-n)
  have h1 := pruneIter_fixed_propagates good same θ hfix ((good θ).card-n+1)
  simpa only [Nat.add_succ, heq] using h1.trans h0.symm

noncomputable def supportKernel (good : Θ → Finset A)
    (same : Θ → Θ → A → Prop) (θ : Θ) : Finset A :=
  pruneIter good same θ (good θ).card

theorem supportKernel_selfVerifying (good : Θ → Finset A)
    (same : Θ → Θ → A → Prop) (θ : Θ) :
    SelfVerifying good same θ (supportKernel good same θ) := by
  apply (selfVerifying_iff_fixed good same θ _).mpr
  exact ⟨pruneIter_subset_target good same θ _, pruneIter_card_fixed good same θ⟩

theorem supportKernel_greatest (good : Θ → Finset A)
    (same : Θ → Θ → A → Prop) (θ : Θ) {U : Finset A}
    (hU : SelfVerifying good same θ U) : U ⊆ supportKernel good same θ :=
  selfVerifying_survives good same θ hU _

theorem supportKernel_nonempty_iff (good : Θ → Finset A)
    (same : Θ → Θ → A → Prop) (θ : Θ) :
    (supportKernel good same θ).Nonempty ↔
      ∃ U : Finset A, U.Nonempty ∧ SelfVerifying good same θ U := by
  constructor
  · intro h
    exact ⟨_, h, supportKernel_selfVerifying good same θ⟩
  · rintro ⟨U, ⟨a, ha⟩, hU⟩
    exact ⟨a, supportKernel_greatest good same θ hU ha⟩

end Orthemology.Tranche2
