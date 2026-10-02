import P03GuardedVCT
set_option pp.universes true
#check @P03Q1f.Chain.mapEdge
#print P03Q1f.Chain.mapEdge
#print axioms P03Q1f.Chain.mapEdge
#check @P03Q1f.walkRank
#print P03Q1f.walkRank
#print axioms P03Q1f.walkRank
#check @P03Q1f.Hom.mapWalk
#print P03Q1f.Hom.mapWalk
#print axioms P03Q1f.Hom.mapWalk
#check @P03Q1f.noClosedWalk
#print P03Q1f.noClosedWalk
#print axioms P03Q1f.noClosedWalk
#check @P03Q1f.Hom.noCollapseOfWalk
#print P03Q1f.Hom.noCollapseOfWalk
#print axioms P03Q1f.Hom.noCollapseOfWalk
#check @P03A2.EvidenceHop.sound
#print P03A2.EvidenceHop.sound
#print axioms P03A2.EvidenceHop.sound
#check @P03A2.EvidenceHop.closed
#print P03A2.EvidenceHop.closed
#print axioms P03A2.EvidenceHop.closed
#check @P03A2.SemanticHop.composite_square
#print P03A2.SemanticHop.composite_square
#print axioms P03A2.SemanticHop.composite_square
#check @P03A2.Path.mapEdge
#print P03A2.Path.mapEdge
#print axioms P03A2.Path.mapEdge
#check @P03A2.guarded_reason_version_composition
#print P03A2.guarded_reason_version_composition
#print axioms P03A2.guarded_reason_version_composition
#check @P03A2.Path.semantic_truth_transport
#print P03A2.Path.semantic_truth_transport
#print axioms P03A2.Path.semantic_truth_transport
#check @P03A2.Via.eq_endpoints
#print P03A2.Via.eq_endpoints
#print axioms P03A2.Via.eq_endpoints
#check @P03A2.Path.no_collapse
#print P03A2.Path.no_collapse
#print axioms P03A2.Path.no_collapse

example {O V R C : Type} {p : P03A2.Policy O V R C}
    {a b : P03A2.Frame O V R C} (q : P03A2.Path p a b) (hs : P03A2.Sound a.reasons) :
    P03A2.Sound b.reasons ∧ P03A2.Closed b.reasons ∧
    (∀ w, b.semantics.meaning ((P03A2.Path.semantics q).map w) ↔ a.semantics.meaning w) ∧
    p.versionAllowed b.version ∧ p.invalidatorsClosed b ∧
    P03A2.Via p.rootStep a.root b.root ∧ P03A2.AuthorityPath p a b :=
  P03A2.guarded_reason_version_composition q hs

#check @P03A2.Path.preimage
#print P03A2.Path.preimage
#print axioms P03A2.Path.preimage

-- Model-definition readbacks are separate from the fourteen theorem targets.
#check @P03A2.EvidenceState
#print P03A2.EvidenceState
#check @P03A2.EvidenceHop
#print P03A2.EvidenceHop
#check @P03A2.SemanticState
#print P03A2.SemanticState
#check @P03A2.SemanticHop
#print P03A2.SemanticHop
#check @P03A2.Frame
#print P03A2.Frame
#check @P03A2.Policy
#print P03A2.Policy
#check @P03A2.Hop
#print P03A2.Hop
#check @P03A2.Path
#print P03A2.Path
#check @P03A2.AuthorityPath
#print P03A2.AuthorityPath
