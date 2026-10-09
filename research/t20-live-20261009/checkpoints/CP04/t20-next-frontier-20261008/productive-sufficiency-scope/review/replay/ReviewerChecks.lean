import ScopeTest
open ProductiveSufficiencyScope
open Orthemology.Tranche20.OriginalBearerBridge
open Orthemology.Tranche20.OriginalBearerBridge.Controls
open Orthemology.Tranche3.SourceIdentity
open RouteProbability

-- The actual-only target predicate is distinct from cross-world bearer existence.
theorem target_predicate_does_not_track_bearer_in_alternative :
    positive.targetReceived () ∧ ¬ positive.existsAt true true := by
  simp [positive]

-- An empty new act occurrence relation also coexists with all inherited premises.
-- Thus act-genus nonemptiness is a chosen extension, not a FullPremises consequence.
def emptyActOccurs (_ : Bool) (_ : Act) : Prop := False

theorem act_genus_nonemptiness_is_additional :
    FullPremises positive ∧ (∀ w a, ¬ emptyActOccurs w a) := by
  exact ⟨positive_full, by intro w a; simp [emptyActOccurs]⟩

#print axioms success_endpoint
#print axioms failure_endpoint
#print axioms RouteProbability.endpointProbability_normalized
#print axioms RouteProbability.assignment_distribution
#print axioms Orthemology.Tranche20.OriginalBearerBridge.Controls.positive_full
#print axioms Orthemology.Tranche20.OriginalBearerBridge.Controls.positive_nonvacuous
#print axioms target_predicate_does_not_track_bearer_in_alternative
#print axioms act_genus_nonemptiness_is_additional
