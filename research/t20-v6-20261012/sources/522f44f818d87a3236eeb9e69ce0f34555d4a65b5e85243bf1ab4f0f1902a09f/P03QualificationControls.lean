import P03GuardedVCT
namespace P03Qualification
open P03A2

def graph : P03Q1f.ReasonDAG where
  size := 3
  Edge := fun a b => a.val < b.val
  rank := Fin.val
  rising := fun h => h

def frame (n : Nat) : Frame Unit Nat Nat Nat where
  graph := graph
  reasons := { required := fun _ => True, discharged := fun _ => True, valid := fun _ => True }
  semantics := { World := Bool, meaning := fun x => x = true }
  version := n
  root := n
  claim := n

def policy : Policy Unit Nat Nat Nat where
  epoch := 7
  authority := fun a b => b.version = a.version + 1
  redelegate := fun a => a.version = 1
  versionAllowed := fun v => v ≤ 2
  invalidatorsClosed := fun _ => True
  rootStep := fun a b => b = a + 1

def hop (n : Nat) (hn : n + 1 ≤ 2) : Hop policy (frame n) (frame (n + 1)) where
  graphMap := P03Q1f.Hom.identity graph
  onto := fun v => ⟨v, rfl⟩
  reasons := {
    preserved := fun _ => True
    revalidated := fun _ => False
    kept := fun _ _ => True.intro
    carry := fun _ _ h => h
    fresh := fun _ h => False.elim h
    outExact := fun _ => ⟨fun h => Or.inl h, fun _ => True.intro⟩
    coverage := fun _ h => Or.inl h }
  semantics := { map := id, square := fun _ => Iff.rfl }
  authority := rfl
  targetVersion := hn
  noOpenInvalidator := True.intro
  rootCustody := rfl

def twoHops : Path policy (frame 0) (frame 2) :=
  .cons (hop 0 (by decide)) (.one (hop 1 (by decide))) rfl

theorem nonvacuous_guarded_path : AuthorityPath policy (frame 0) (frame 2) :=
  (guarded_reason_version_composition twoHops (fun _ _ => True.intro)).2.2.2.2.2.2

theorem path_does_not_imply_direct_authority :
    AuthorityPath policy (frame 0) (frame 2) ∧ ¬ policy.authority (frame 0) (frame 2) :=
  ⟨nonvacuous_guarded_path, by change ¬ (2 = 0 + 1); decide⟩

theorem root_trace_does_not_imply_endpoint_equality :
    Via policy.rootStep (frame 0).root (frame 2).root ∧ (frame 0).root ≠ (frame 2).root :=
  ⟨Path.rootTrace twoHops, by decide⟩

theorem nontrivial_graph_edge_transports :
    (frame 2).graph.Edge ((Path.graph twoHops).node ⟨0, by decide⟩)
      ((Path.graph twoHops).node ⟨2, by decide⟩) :=
  Path.mapEdge twoHops (by change 0 < 2; decide)

theorem false_source_world_remains_false :
    ¬ (frame 2).semantics.meaning ((Path.semantics twoHops).map false) := by
  change ¬ (false = true)
  decide

theorem frozen_claim_coordinate_can_change :
    (frame 0).claim ≠ (frame 2).claim := by decide

#print axioms nonvacuous_guarded_path
#print axioms path_does_not_imply_direct_authority
#print axioms root_trace_does_not_imply_endpoint_equality
#print axioms nontrivial_graph_edge_transports
#print axioms false_source_world_remains_false
#print axioms frozen_claim_coordinate_can_change
end P03Qualification
