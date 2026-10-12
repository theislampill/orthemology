import ActualUseControls
import ActualProvisionReview
import BeginninglessProvision

/-!
Direct integration against the independently replayed author interface.
These adapters make the semantic respect explicit; the author theorem does
not invent efficient attribution from broad actual support.
-/
namespace IntegratedActualUseReview
open ExplanatoryGeneration ActualUseControls
namespace MixedSupport
open ActualProvisionReview

def supply : Supply Resource ActualProvisionReview.Rule where
  original := original
  needs := needs
  output := output

theorem used_sound : UsedSound supply Used actual := by
  intro i _; exact (all_rules_used_and_sound i).2

theorem seed_sound : SeedSound supply Used actual := by
  intro r hr
  refine ⟨trivial, ?_⟩
  intro receipt
  obtain ⟨i, hi, out⟩ := receipt
  obtain ⟨p, hp⟩ := no_empty_rules i
  exact originals_receive_no_support r hr ⟨p, i, hi, hp, out⟩

theorem no_empty : NoEmptyRules (usedSupply supply Used) := by
  intro i; exact no_empty_rules i.1

theorem g_positive_actual_path : PositiveUsedPath supply Used Resource.gStock Resource.target := by
  refine ⟨ActualProvisionReview.Rule.targetProduction, Resource.hPower, trivial, Or.inl rfl, rfl, ?_⟩
  exact SupplyPath.step (s := usedSupply supply Used) ⟨ActualProvisionReview.Rule.grounding, trivial⟩ (SupplyPath.refl Resource.gStock) rfl

theorem g_actual_generated_anchor :
    ∃ q, ExplanatoryGeneration.Generated (usedSupply supply Used) q ∧
      PositiveUsedPath supply Used q Resource.target := by
  exact ⟨Resource.gStock, ExplanatoryGeneration.Generated.original (Or.inl rfl), g_positive_actual_path⟩

theorem repaired_author_witness_applies :
    actual Resource.target ∧ ∃ o, actual o ∧ supply.original o ∧
      ¬ UsedReceipt supply Used o ∧ PositiveUsedPath supply Used o Resource.target :=
  actual_anchor_original_witness supply Used actual used_sound seed_sound no_empty g_actual_generated_anchor

/-- The repaired support witness succeeds while the fixed G witness does not
acquire productive target attribution. G's original bearer and exercise elsewhere
remain present; the missing relation cannot be repaired by choosing K instead. -/
theorem guarded_actual_support_does_not_become_productive :
    UsedSound supply Used actual ∧ SeedSound supply Used actual ∧
    NoEmptyRules (usedSupply supply Used) ∧
    OriginalResource control Resource.gStock ∧
    control.intrinsic Bearer.g Resource.gStock ∧ OriginalBearer control Bearer.g ∧
    PositiveUsedPath supply Used Resource.gStock Resource.target ∧
    Contributor control Bearer.g Resource.side ∧ ¬ Contributor control Bearer.g Resource.target := by
  exact ⟨used_sound, seed_sound, no_empty, g_original_resource,
    g_same_original_bearer.1, g_same_original_bearer.2,
    g_positive_actual_path,
    ⟨Resource.gStock, rfl, StrictPath.edge g_actually_produces_side⟩,
    g_is_target_noncontributor⟩
end MixedSupport

namespace InfiniteTokens
open BeginninglessProvision

def supply : Supply Resource Nat where
  original := original
  needs := needs
  output := output

theorem used_sound : UsedSound supply used actual := by
  intro n _; exact ⟨trivial, fun _ _ => trivial⟩

theorem seed_sound : SeedSound supply used actual := by
  intro r hr
  change r = none at hr
  subst r
  refine ⟨trivial, ?_⟩
  intro receipt; obtain ⟨n, _, hn⟩ := receipt; cases hn

theorem no_empty : NoEmptyRules (usedSupply supply used) := by
  intro _; exact ⟨none, Or.inl rfl⟩

theorem same_original_positive_path (n : Nat) :
    PositiveUsedPath supply used none (some n) :=
  ⟨n, none, trivial, Or.inl rfl, rfl, SupplyPath.refl none⟩

theorem original_generated_anchor (n : Nat) :
    ∃ q, ExplanatoryGeneration.Generated (usedSupply supply used) q ∧
      PositiveUsedPath supply used q (some n) :=
  ⟨none, ExplanatoryGeneration.Generated.original rfl, same_original_positive_path n⟩

/-- The positive-path repair retains the exact same original in a genuinely
beginningless productive history; whole-token generation is not needed. -/
theorem repaired_author_witness_keeps_same_original (n : Nat) :
    actual (some n) ∧ actual none ∧ ¬ UsedReceipt supply used none ∧
      PositiveUsedPath supply used none (some n) := by
  obtain ⟨ht, o, ho, horiginal, hreceipt, hpath⟩ :=
    actual_anchor_original_witness supply used actual used_sound seed_sound no_empty (original_generated_anchor n)
  change o = none at horiginal
  subst o
  exact ⟨ht, ho, hreceipt, hpath⟩

theorem integrated_same_bearer_without_full_generation (n : Nat) :
    PositiveUsedPath supply used none (some n) ∧
    ActualProvisionReview.OriginalResource bridge none ∧
    ActualProvisionReview.OriginalBearer bridge none ∧
    ActualProvisionReview.Contributor bridge none (some n) ∧
    ¬ BeginninglessProvision.Generated (some n) := by
  have h := same_bearer_productive_without_token_generation n
  exact ⟨same_original_positive_path n, h.1, h.2.1, h.2.2.2.1, h.2.2.2.2⟩

end InfiniteTokens
end IntegratedActualUseReview
