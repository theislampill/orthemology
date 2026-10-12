import P03QualificationControls
import SourceControls
namespace IndependentBoundaryChecks
open P03A2 P03Source OrthemologyV2 OrthemologyV3

def retagEpoch {O V R C : Type} (p : Policy O V R C) (epoch : Nat) : Policy O V R C :=
  { p with epoch := epoch }

/-- The epoch number itself has no constraint connecting it to the predicates. -/
def retagHop {O V R C : Type} {p : Policy O V R C} {a b : Frame O V R C}
    (h : Hop p a b) (epoch : Nat) : Hop (retagEpoch p epoch) a b where
  graphMap := h.graphMap
  onto := h.onto
  reasons := h.reasons
  semantics := h.semantics
  authority := h.authority
  targetVersion := h.targetVersion
  noOpenInvalidator := h.noOpenInvalidator
  rootCustody := h.rootCustody

noncomputable def retagPath {O V R C : Type} {p : Policy O V R C} {a b : Frame O V R C}
    (q : Path p a b) (epoch : Nat) : Path (retagEpoch p epoch) a b := by
  induction q with
  | one h => exact .one (retagHop h epoch)
  | cons h rest allowMiddle ih => exact .cons (retagHop h epoch) ih allowMiddle

theorem every_epoch_can_carry_same_path (epoch : Nat) :
    Nonempty (Path (retagEpoch P03Qualification.policy epoch)
      (P03Qualification.frame 0) (P03Qualification.frame 2)) :=
  ⟨retagPath P03Qualification.twoHops epoch⟩

-- Target acceptance remains weaker than source acceptance after trace erasure.
theorem accepted_target_does_not_validate_source_trace :
    sourceCheck 0 (.reduce P03SourceControls.pid [.k]) = none ∧
      (check 0 (encode (.reduce P03SourceControls.pid [.k]))).isSome = true := by decide

#print axioms every_epoch_can_carry_same_path
#print axioms accepted_target_does_not_validate_source_trace
end IndependentBoundaryChecks

namespace IndependentGraphBoundary
open P03Q1f

def emptyEdges : ReasonDAG where
  size := 2
  Edge := fun _ _ => False
  rank := Fin.val
  rising := fun h => False.elim h

def orderedEdges : ReasonDAG where
  size := 2
  Edge := fun x y => x.val < y.val
  rank := Fin.val
  rising := fun h => h

def addEdgeHom : Hom emptyEdges orderedEdges where
  node := id
  edge := fun h => False.elim h

theorem surjective_node_map_allows_new_target_edges :
    (∀ v : Fin 2, ∃ u : Fin 2, addEdgeHom.node u = v) ∧
      orderedEdges.Edge ⟨0, by decide⟩ ⟨1, by decide⟩ ∧
      ¬ emptyEdges.Edge ⟨0, by decide⟩ ⟨1, by decide⟩ := by
  exact ⟨fun v => ⟨v,rfl⟩, by change (0 : Nat) < 1; decide, fun h => h⟩

#print axioms surjective_node_map_allows_new_target_edges
end IndependentGraphBoundary
