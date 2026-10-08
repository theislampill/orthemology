import CertificateComposition
namespace OrthemicCertificate.CompositionControls

def I : Input 2 2 2 := {
  rows := ((List.finRange 2).flatMap fun σ => (List.finRange 2).flatMap fun s =>
    (List.finRange 2).flatMap fun a => (List.finRange 2).map fun y =>
      if (a = 0 ∧ y = s) ∨ (a = 1 ∧ y = σ) then (1 : ℚ) else 0).toArray
  priorities := Array.replicate 8 0
  menus := [⟨[0],0,[0,1]⟩,⟨[0],1,[0]⟩,⟨[1],0,[0]⟩,⟨[1],1,[0]⟩,⟨[0,1],0,[1]⟩]
  interpretation := ⟨["alpha","beta"],["s0","s1"],["loop","split"],"composition-v1","states","fixture","test grants"⟩ }

def child (σ : Fin 2) (s : Fin 2) : Node 2 2 2 :=
  ⟨{σ},{s},{(s,0)},[⟨s,σ,.target ⟨s,[]⟩ ⟨{(s,0)},s,[⟨s,⟨s,[]⟩,⟨s,[]⟩⟩]⟩ s⟩]⟩

def alternateChild : Node 2 2 2 :=
  ⟨{0},{0},{(0,1)},[⟨0,0,.target ⟨0,[]⟩ ⟨{(0,1)},0,[⟨0,⟨0,[]⟩,⟨0,[]⟩⟩]⟩ 0⟩]⟩

def parent : Node 2 2 2 :=
  ⟨{0,1},{0},{(0,1)},[⟨0,0,.exit ⟨0,[]⟩ (0,1) 0⟩,⟨0,1,.exit ⟨0,[]⟩ (0,1) 1⟩]⟩

def c0 : Body 2 2 2 := [child 0 0]
def c1 : Body 2 2 2 := [child 1 1]
def united : Body 2 2 2 := merge c0 c1

def results : List (String × Bool) := [
  ("left_body_valid",bodyCheck I c0),
  ("right_body_valid",bodyCheck I c1),
  ("union_body_valid",bodyCheck I united),
  ("left_query_preserved",queryLookup united {0} 0),
  ("right_query_preserved",queryLookup united {1} 1),
  ("union_no_parent",!queryLookup united {0,1} 0),
  ("same_support_state_union",check I (merge c0 [child 0 1]) {0} 1),
  ("alternative_component_valid",bodyCheck I [alternateChild]),
  ("overlapping_key_left_retained",decide ((merge c0 [alternateChild]).map Node.obligations = [(child 0 0).obligations])),
  ("reverse_collision_retains_alternative",decide ((merge [alternateChild] c0).map Node.obligations = [alternateChild.obligations])),
  ("components_not_unioned",bodyCheck I (merge c0 [alternateChild])),
  ("checked_merge_accepts",decide (checkedMerge I c0 c1 = some united)),
  ("malformed_duplicate_body_rejects",decide (checkedMerge I (c0 ++ c0) c1 = none)),
  ("unrelated_invalid_node_rejects",decide (checkedMerge I (c0 ++ [{child 1 0 with obligations := []}]) c1 = none)),
  ("checked_link_accepts",decide (checkedLinkParent I united parent = some (linkParent united parent))),
  ("checked_link_existing_key_rejects",decide (checkedLinkParent I c0 (child 0 0) = none)),
  ("checked_link_missing_child_rejects",decide (checkedLinkParent I c0 parent = none)),
  ("checked_parent_accepts",check I (linkParent united parent) {0,1} 0),
  ("missing_left_child_rejects",!bodyCheck I (linkParent c1 parent)),
  ("missing_right_child_rejects",!bodyCheck I (linkParent c0 parent)),
  ("bad_parent_still_rejects",!bodyCheck I (linkParent united {parent with obligations := []})),
  ("fresh_changed_input_rejects",!bodyCheck {I with menus := []} united),
  ("actual_input_binding_differs",!I.sameInput {I with interpretation := {I.interpretation with modelRevision := "composition-v2"}})]

#eval results
#guard results.all Prod.snd

#check @mergeObligations_mem_iff
#print axioms mergeObligations_mem_iff
#check @bodyCheck_merge
#check @queryLookup_merge_left
#check @queryLookup_merge_right
#check @merge_support_iff
#check @bodyCheck_linkParent
#check @queryLookup_linkParent
#print axioms bodyCheck_merge
#print axioms queryLookup_merge_left
#print axioms queryLookup_merge_right
#print axioms merge_support_iff
#print axioms bodyCheck_linkParent
#print axioms queryLookup_linkParent
#check @checkedMerge_some_iff
#check @checkedLinkParent_some_iff
#print axioms checkedMerge_valid
#print axioms checkedLinkParent_valid
end OrthemicCertificate.CompositionControls
