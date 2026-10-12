import ActualUseControls
import ActualProvisionReview
import BeginninglessProvision

/-! Integrated consumers of the repaired author interface and independent
controls. No source-warrant or metaphysical-possibility claim is added. -/
namespace IntegratedConsumers
open ExplanatoryGeneration ActualUseControls

-- Fixed original G is nonidle and has actual broad support to the target;
-- the resource/bearer binding does not substitute the independently active K.
def nonidleSupply : Supply ActualProvisionReview.Resource ActualProvisionReview.Rule where
  original := ActualProvisionReview.original
  needs := ActualProvisionReview.needs
  output := ActualProvisionReview.output

theorem nonidle_sound : UsedSound nonidleSupply ActualProvisionReview.Used
    ActualProvisionReview.actual := by
  intro i _
  exact (ActualProvisionReview.all_rules_used_and_sound i).2

theorem nonidle_seeds : SeedSound nonidleSupply ActualProvisionReview.Used
    ActualProvisionReview.actual := by
  intro r original
  refine ⟨trivial, ?_⟩
  intro receipt
  obtain ⟨i, hi, out⟩ := receipt
  obtain ⟨p, hp⟩ := ActualProvisionReview.no_empty_rules i
  exact ActualProvisionReview.originals_receive_no_support r original ⟨p,i,hi,hp,out⟩

theorem nonidle_nonempty : NoEmptyRules (usedSupply nonidleSupply ActualProvisionReview.Used) := by
  intro i; exact ActualProvisionReview.no_empty_rules i.1

theorem nonidle_positive_G_path : PositiveUsedPath nonidleSupply ActualProvisionReview.Used
    .gStock .target := by
  refine ⟨.targetProduction, .hPower, trivial, Or.inl rfl, rfl, ?_⟩
  exact SupplyPath.step (s := usedSupply nonidleSupply ActualProvisionReview.Used) ⟨ActualProvisionReview.Rule.grounding,trivial⟩ (SupplyPath.refl ActualProvisionReview.Resource.gStock) rfl

theorem nonidle_repaired_interface_and_target_failure :
    UsedSound nonidleSupply ActualProvisionReview.Used ActualProvisionReview.actual ∧
    SeedSound nonidleSupply ActualProvisionReview.Used ActualProvisionReview.actual ∧
    PositiveUsedPath nonidleSupply ActualProvisionReview.Used .gStock .target ∧
    ActualProvisionReview.OriginalResource ActualProvisionReview.control .gStock ∧
    ActualProvisionReview.control.intrinsic .g .gStock ∧
    ActualProvisionReview.OriginalBearer ActualProvisionReview.control .g ∧
    ¬ ActualProvisionReview.Contributor ActualProvisionReview.control .g .target := by
  exact ⟨nonidle_sound, nonidle_seeds, nonidle_positive_G_path,
    ActualProvisionReview.g_original_resource,
    ActualProvisionReview.g_same_original_bearer.1,
    ActualProvisionReview.g_same_original_bearer.2,
    ActualProvisionReview.g_is_target_noncontributor⟩

-- This calls the author's repaired generic theorem on the SAME data.
-- Its existential resource conclusion is deliberately not called productive.
theorem nonidle_generic_support_witness :
    ActualProvisionReview.actual .target ∧ ∃ o, ActualProvisionReview.actual o ∧
    nonidleSupply.original o ∧ ¬ UsedReceipt nonidleSupply ActualProvisionReview.Used o ∧
    PositiveUsedPath nonidleSupply ActualProvisionReview.Used o .target :=
  actual_anchor_original_witness nonidleSupply ActualProvisionReview.Used
    ActualProvisionReview.actual nonidle_sound nonidle_seeds nonidle_nonempty
    (target := .target)
    ⟨ActualProvisionReview.Resource.gStock, Generated.original (Or.inl rfl),
      nonidle_positive_G_path⟩

def beginninglessSupply : Supply BeginninglessProvision.Resource Nat where
  original := BeginninglessProvision.original
  needs := BeginninglessProvision.needs
  output := BeginninglessProvision.output

theorem beginningless_sound : UsedSound beginninglessSupply BeginninglessProvision.used
    BeginninglessProvision.actual := by
  intro n _; exact ⟨trivial, fun _ _ => trivial⟩

theorem beginningless_seeds : SeedSound beginninglessSupply BeginninglessProvision.used
    BeginninglessProvision.actual := by
  intro r original
  change r = none at original
  subst r
  refine ⟨trivial, ?_⟩
  intro receipt; obtain ⟨n, _, bad⟩ := receipt
  cases bad

theorem beginningless_nonempty :
    NoEmptyRules (usedSupply beginninglessSupply BeginninglessProvision.used) :=
  fun _ => ⟨none, Or.inl rfl⟩

theorem beginningless_positive_path (n : Nat) :
    PositiveUsedPath beginninglessSupply BeginninglessProvision.used none (some n) :=
  ⟨n, none, trivial, Or.inl rfl, rfl, SupplyPath.refl none⟩

theorem beginningless_generic_support_witness (n : Nat) :
    BeginninglessProvision.actual (some n) ∧ ∃ o, BeginninglessProvision.actual o ∧
    beginninglessSupply.original o ∧ ¬ UsedReceipt beginninglessSupply BeginninglessProvision.used o ∧
    PositiveUsedPath beginninglessSupply BeginninglessProvision.used o (some n) :=
  actual_anchor_original_witness beginninglessSupply BeginninglessProvision.used
    BeginninglessProvision.actual beginningless_sound beginningless_seeds beginningless_nonempty
    (target := some n)
    ⟨none, Generated.original rfl, beginningless_positive_path n⟩

theorem generation_maps_to_review {r}
    (h : Generated (usedSupply beginninglessSupply BeginninglessProvision.used) r) :
    BeginninglessProvision.Generated r := by
  induction h with
  | original h => exact BeginninglessProvision.Generated.seed h
  | rule i _ ih => exact BeginninglessProvision.Generated.rule i.1 ih

theorem beginningless_consumer_keeps_same_bearer_without_full_generation (n : Nat) :
    PositiveUsedPath beginninglessSupply BeginninglessProvision.used none (some n) ∧
    ActualProvisionReview.OriginalResource BeginninglessProvision.bridge none ∧
    ActualProvisionReview.OriginalBearer BeginninglessProvision.bridge none ∧
    BeginninglessProvision.bridge.intrinsic none none ∧
    ActualProvisionReview.Contributor BeginninglessProvision.bridge none (some n) ∧
    ¬ Generated (usedSupply beginninglessSupply BeginninglessProvision.used) (some n) := by
  have fixed := BeginninglessProvision.same_bearer_productive_without_token_generation n
  exact ⟨beginningless_positive_path n, fixed.1, fixed.2.1, fixed.2.2.1,
    fixed.2.2.2.1, fun h => fixed.2.2.2.2 (generation_maps_to_review h)⟩

end IntegratedConsumers
