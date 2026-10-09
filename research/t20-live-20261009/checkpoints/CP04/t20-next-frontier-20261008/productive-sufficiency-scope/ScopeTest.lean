import BridgeControls
import EndpointLaw

/-!
Exact-interface diagnostic, not a metaphysical model.
`positive` and all seven inherited FullPremises are imported unchanged.
The one-route law is an instance of the existing RouteProbability model.
A realized success bit is an argument of endpoint; it is NOT thereby a
causally antecedent hidden variable, a reason for itself, or an actual cause.
The correspondence below is mathematical. The full source's perfection,
causal interpretation and wise particular determination are not established.
-/
namespace ProductiveSufficiencyScope
open Orthemology.Tranche20.OriginalBearerBridge
open Orthemology.Tranche20.OriginalBearerBridge.Controls
open Orthemology.Tranche3.SourceIdentity
open RouteProbability
open scoped BigOperators

/-- Exactly the inherited positive fixture, not a weakened reconstruction. -/
theorem all_seven_preserved : FullPremises positive := positive_full

/-- Same original witness and same cross-world existence and receipt facts. -/
theorem original_same_witness :
    ∃ t r g, OriginalWitness positive t r g ∧ Necessary positive.existsAt g ∧
      UniformRoot positive.existsAt positive.dep g ∧ EssentialNonreceipt positive g :=
  positive_same_witness

/-- One genuinely nonempty declared route; all calibration and enabling are inherited. -/
def oneRoute : Model Unit Unit where
  kind := fun _ => .a
  outputs := fun _ => {()}
  outputs_nonempty := by intro _; simp

/-- Realization coordinate for two represented indices, not metaphysical world certification. -/
def realization (w : Bool) : Unit → Bool := fun _ => !w

theorem normalized_law :
    (∑ V : Finset Unit, endpointProbability oneRoute .A V) = 1 :=
  endpointProbability_normalized oneRoute .A

theorem both_realizations_have_positive_mass :
    bernoulliWeight (fun r => failure (oneRoute.kind r)) (realization false) = 1/2 ∧
    bernoulliWeight (fun r => failure (oneRoute.kind r)) (realization true) = 1/2 := by
  norm_num [bernoulliWeight, oneRoute, realization, RouteProbability.failure]

theorem success_endpoint : endpoint oneRoute .A (realization false) = {()} := by
  simp [endpoint, oneRoute, realization, enabled]

theorem failure_endpoint : endpoint oneRoute .A (realization true) = ∅ := by
  simp [endpoint, oneRoute, realization, enabled]

/-- Bridge target existence matches this selected probability-model endpoint.
This correspondence supplies neither a causal-production proof nor perfection. -/
theorem occurrence_coherence (w : Bool) :
    positive.existsAt w true ↔ () ∈ endpoint oneRoute .A (realization w) := by
  cases w <;> simp [positive, endpoint, oneRoute, realization, enabled]

theorem necessary_bearer_nonnecessary_target :
    Necessary positive.existsAt false ∧ ¬ Necessary positive.existsAt true := by
  simp only [Necessary, positive]
  decide

/-- Necessary standing existence and one fixed law are compatible in this
interface with both target outcomes. No full-cause principle is claimed here. -/
theorem standing_basis_does_not_select :
    positive.existsAt false false ∧ positive.existsAt true false ∧
    endpoint oneRoute .A (realization false) ≠ endpoint oneRoute .A (realization true) := by
  simp [positive, success_endpoint, failure_endpoint]

/-- Fixing the full assignment fixes the endpoint, regardless of how the
assignment was selected. This is functional determination, not a cause theorem. -/
theorem full_record_determines (u v : Unit → Bool) (h : u = v) :
    endpoint oneRoute .A u = endpoint oneRoute .A v := congrArg (endpoint oneRoute .A) h

/-- No one endpoint-valued function of the unchanged standing record alone
reproduces both realizations. This does not preclude a primitive causal process. -/
theorem no_standing_record_selector :
    ¬ ∃ f : Unit → Finset Unit, ∀ w : Bool, f () = endpoint oneRoute .A (realization w) := by
  rintro ⟨f, hf⟩
  have hs := hf false
  have ht := hf true
  rw [success_endpoint] at hs
  rw [failure_endpoint] at ht
  have bad : ({()} : Finset Unit) = ∅ := hs.symm.trans ht
  simp at bad

/-- Act-token occurrence has a different type from whole-bearer existence. -/
inductive Act | left | right deriving DecidableEq

def actOccurs (w : Bool) (a : Act) : Prop :=
  (w = false ∧ a = .left) ∨ (w = true ∧ a = .right)

theorem act_genus_without_fixed_token :
    (∀ w, ∃ a, actOccurs w a) ∧ actOccurs false .left ∧
    ¬ (∀ w, actOccurs w .left) := by
  constructor
  · intro w
    cases w
    · exact ⟨.left, Or.inl ⟨rfl, rfl⟩⟩
    · exact ⟨.right, Or.inr ⟨rfl, rfl⟩⟩
  · constructor
    · exact Or.inl ⟨rfl, rfl⟩
    · intro h
      have ht := h true
      simp [actOccurs] at ht

/-- The exact existential premises coexist with the distinct variable act
interface. No act is inserted into positive's bearer domain by this conjunction. -/
theorem existential_premises_do_not_fix_act_token :
    FullPremises positive ∧ (∀ w, ∃ a, actOccurs w a) ∧
    ¬ (∀ w, actOccurs w .left) :=
  ⟨positive_full, act_genus_without_fixed_token.1, act_genus_without_fixed_token.2.2⟩

#print axioms all_seven_preserved
#print axioms original_same_witness
#print axioms normalized_law
#print axioms both_realizations_have_positive_mass
#print axioms occurrence_coherence
#print axioms necessary_bearer_nonnecessary_target
#print axioms standing_basis_does_not_select
#print axioms full_record_determines
#print axioms no_standing_record_selector
#print axioms act_genus_without_fixed_token
#print axioms existential_premises_do_not_fix_act_token
end ProductiveSufficiencyScope
