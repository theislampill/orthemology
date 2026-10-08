import ModalUnion

namespace ModalUnion.IndependentReview
universe u w
variable {V : Type u} {W : Type w}

/-- The pure/faithful interpretation class is nonempty for every frame. -/
theorem every_frame_has_interpretation (F : Frame V W) :
    Nonempty (FaithfulInterpretation F) :=
  ⟨identityExpansion (Quotient (componentSetoid F)) (component F)
    (component_edgeLaw F)⟩

/-- The checked consequence is about the fixed equality language. -/
theorem exact_statement_contract (F : Frame V W) (x y : V) :
    (∀ (S : Type u) (a : V → S),
      (∀ z p q, F.admissible z → F.crossing z p q → a p = a q) → a x = a y)
      ↔ Connected F x y :=
  forcedEqual_iff_connected F x y

#print axioms every_frame_has_interpretation
#print axioms exact_statement_contract
end ModalUnion.IndependentReview
