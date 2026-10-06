import CertificateComposition
import CertificateBinding
import ReviewerControls

namespace IndependentCompositionControls
open OrthemicCertificate IndependentCertificateControls

-- Raw canonicalizers have prevalidated-input contracts. These controls pin
-- the checked admission wrappers, including a concrete duplicate-laundering case.
def malformedChildren : Body 3 3 3 := [child0,{child0 with obligations := []},child1]
def revealPackage : BoundBody 3 3 3 := ⟨reveal,[child0,child1,parent]⟩
def revisedReveal : Input 3 3 3 :=
  {reveal with interpretation := {reveal.interpretation with modelRevision := "r2"}}

def results : List (String × Bool) :=
  [("checked_merge_two_separate_queries",(checkedMerge reveal [child0] [child1]).isSome),
   ("actual_merge_no_parent_query",!check reveal (merge [child0] [child1]) {0,1,2} 0),
   ("checked_parent_complete_children",(checkedLinkParent reveal (merge [child0] [child1]) parent).isSome),
   ("actual_link_parent_query",check reveal (linkParent (merge [child0] [child1]) parent) {0,1,2} 0),
   ("checked_parent_missing_child0",(checkedLinkParent reveal [child1] parent).isNone),
   ("checked_parent_missing_child1",(checkedLinkParent reveal [child0] parent).isNone),
   ("checked_parent_already_present",(checkedLinkParent reveal [child0,child1,parent] parent).isNone),
   ("invalid_new_node_at_existing_support_rejected",(checkedLinkParent reveal [child0,child1,parent] {parent with obligations := []}).isNone),
   ("malformed_source_body_rejected",!bodyCheck reveal malformedChildren),
   ("raw_normalization_can_drop_duplicate",bodyCheck reveal (merge malformedChildren [])),
   ("checked_merge_prevents_duplicate_laundering",(checkedMerge reveal malformedChildren []).isNone),
   ("checked_link_prevents_duplicate_laundering",(checkedLinkParent reveal malformedChildren parent).isNone),
   ("checked_merge_invalid_unrelated_node",(checkedMerge reveal [invalidExtra,child0] [child1]).isNone),
   ("same_input_envelope_accepts",boundCheck reveal revealPackage {0,1,2} 0),
   ("actual_structure_revision_envelope_rejects",!boundCheck revisedReveal revealPackage {0,1,2} 0),
   ("fresh_revision_recheck_accepts",check revisedReveal revealPackage.body {0,1,2} 0),
   ("distinct_target_left_witness_retained",decide ((merge [tinyNode 0] [tinyNode 1]).map Node.obligations = [(tinyNode 0).obligations])),
   ("distinct_path_left_witness_retained",decide ((merge [routeNode false] [routeNode true]).map Node.obligations = [(routeNode false).obligations]))]
#eval results
#guard results.all Prod.snd

-- Union of the components themselves would be disconnected. The successful
-- merge must retain each obligation's original singleton component instead.
def islands : Input 1 2 1 :=
  ⟨#[1,0,0,1],#[2,2],[⟨[0],0,[0]⟩,⟨[0],1,[0]⟩],
   ⟨["m"],["left","right"],["stay"],"v1","state","declared","declared"⟩⟩
def islandNode (s : Fin 2) : Node 1 2 1 :=
  ⟨{0},{s},{(s,0)},[⟨s,0,.target (ep s) (singletonComponent s 0) s⟩]⟩
#guard bodyCheck islands [islandNode 0]
#guard bodyCheck islands [islandNode 1]
#guard check islands (merge [islandNode 0] [islandNode 1]) {0} 0
#guard check islands (merge [islandNode 0] [islandNode 1]) {0} 1
#guard (merge [islandNode 0] [islandNode 1]).map Node.obligations =
  [(islandNode 0).obligations ++ (islandNode 1).obligations]

#check @bodyCheck_merge
#check @checkedMerge_valid
#check @bodyCheck_linkParent
#check @checkedLinkParent_valid
#check @merge_support_iff
#check @boundCheck_iff
#check @boundCheck_stale
#print axioms bodyCheck_merge
#print axioms checkedMerge_valid
#print axioms bodyCheck_linkParent
#print axioms checkedLinkParent_valid
#print axioms merge_support_iff
#print axioms boundCheck_iff
#print axioms boundCheck_stale
end IndependentCompositionControls
