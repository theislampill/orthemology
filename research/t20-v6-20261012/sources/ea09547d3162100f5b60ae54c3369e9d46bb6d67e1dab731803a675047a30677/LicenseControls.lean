import StaticLicensedEquivalence

noncomputable section
open MeasureTheory ProbabilityTheory Filter Finset Set
open scoped BigOperators
open Orthemology.Tranche2 Orthemology.Tranche2.PolicyEmbedding Orthemology.Tranche2.MicroPolicy
namespace LicenseAudit
local instance : MeasurableSpace Bool := ⊤
local instance : MeasurableSingletonClass Bool := ⟨fun _ => trivial⟩

def safeSupport (_σ : Bool) : Finset Bool := {false}

theorem output_licensed_even_with_bad_default (P : Bool → Bool → Bool → ℝ)
    (r : Bool) (h : History Bool Bool) :
    sharedPolicy P safeSupport false true r h = false := by
  have hm := sharedPolicy_mem_menu P safeSupport false true ({false} : Finset Bool)
    (by intro σ; simp [safeSupport]) (by intro σ; simp [safeSupport]) r h
  simpa using hm

theorem unreachable_history_still_licensed (P : Bool → Bool → Bool → ℝ) :
    sharedPolicy P safeSupport false true false [(true,true),(true,false)] = false :=
  output_licensed_even_with_bad_default P _ _

theorem default_really_outside : true ∉ ({false} : Finset Bool) := by simp

theorem malformed_past_contains_unlicensed :
    ∃ z ∈ ([(true,true),(true,false)] : History Bool Bool), z.1 ∉ ({false} : Finset Bool) := by
  exact ⟨(true,true),by simp,by simp⟩

theorem no_pointwise_empty_menu_policy :
    ¬ ∃ π : Bool → History Bool Bool → Bool, ∀ r h, π r h ∈ (∅ : Finset Bool) := by
  rintro ⟨π,h⟩
  simpa using h false []

theorem empty_target_kernel (same : Bool → Bool → Bool → Prop) (θ : Bool) :
    supportKernel (fun (_ : Bool) => (∅ : Finset Bool)) same θ = ∅ := by
  apply Finset.eq_empty_iff_forall_not_mem.mpr
  intro a ha
  have h := (supportKernel_selfVerifying (fun (_ : Bool) => (∅ : Finset Bool)) same θ).1 ha
  simpa using h

theorem empty_menu_kernel (G : Bool → Finset Bool) (same : Bool → Bool → Bool → Prop) (θ : Bool) :
    supportKernel (fun θ => G θ ∩ ∅) same θ = ∅ := by
  simpa using empty_target_kernel same θ

theorem disjoint_target_menu_kernel (same : Bool → Bool → Bool → Prop) (θ : Bool) :
    supportKernel (fun (_ : Bool) => ({true} : Finset Bool) ∩ {false}) same θ = ∅ := by
  simpa using empty_target_kernel same θ

theorem empty_plans_satisfy_menu_inclusion :
    ∀ (σ : Bool) a, a ∈ ([] : List Bool) → a ∈ ({false} : Finset Bool) := by simp

theorem empty_plan_exposes_unlicensed_default :
    policy (fun (_ : Bool) => ([] : List Bool)) (fun (_ : History Bool Bool) => false) true () [] ∉
      ({false} : Finset Bool) := by simp [policy,queue]

theorem unlicensed_nonempty_plan :
    (∀ σ : Bool, ([true] : List Bool) ≠ []) ∧
      policy (fun (_ : Bool) => [true]) (fun (_ : History Bool Bool) => false) false () [] ∉
        ({false} : Finset Bool) := by simp [policy,queue]

theorem legal_can_be_target_bad :
    true ∈ (Finset.univ : Finset Bool) ∧ true ∉ ({false} : Finset Bool) := by simp

theorem all_time_license_does_not_follow_from_eventual_target :
    (∀ᶠ n in atTop, (if n = 0 then true else false) ∈ ({false} : Finset Bool)) ∧
      ¬ (∀ n : ℕ, (if n = 0 then true else false) ∈ ({false} : Finset Bool)) := by
  constructor
  · apply eventually_atTop.mpr
    refine ⟨1,?_⟩
    intro n hn
    have h : n ≠ 0 := by omega
    simp [h]
  · intro h
    simpa using h 0

end LicenseAudit
