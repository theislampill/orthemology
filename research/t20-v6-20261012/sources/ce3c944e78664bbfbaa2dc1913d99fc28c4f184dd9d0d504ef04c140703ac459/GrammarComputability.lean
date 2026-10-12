import CoreGrammar
namespace ExactSyntaxValidity
open Encodable SourceFamilyComputability CodedScope
set_option maxRecDepth 8192
set_option maxHeartbeats 200000

theorem primrec_nullary : Primrec nullary :=
  primrec_node.comp primrec_leaf (Primrec.const _)
theorem primrec_unary (t : Nat) : Primrec (unary t) :=
  primrec_node.comp (Primrec.const _) (primrec_node.comp Primrec.id (Primrec.const _))
theorem primrec_binary (t : Nat) : Primrec₂ (binary t) :=
  primrec_node.comp₂ (.const _) (primrec_node.comp₂ .left (primrec_node.comp₂ .right (.const _)))
theorem primrec_ternary (t : Nat) : Primrec (fun p : Nat × Nat × Nat => ternary t p.1 p.2.1 p.2.2) :=
  primrec_node.comp (Primrec.const _) (primrec_node.comp Primrec.fst
    (primrec_node.comp (Primrec.fst.comp Primrec.snd)
      (primrec_node.comp (Primrec.snd.comp Primrec.snd) (Primrec.const _))))
theorem primrec_arg3 : Primrec arg3 :=
  primrec_first.comp (primrec_rest.comp (primrec_rest.comp primrec_rest))

theorem primrec_termShape : Primrec termShape :=
  Primrec.ite (Primrec.nat_lt.comp primrec_tag (Primrec.const 5))
    (Primrec.eq.comp Primrec.id (primrec_nullary.comp primrec_tag))
    (Primrec.ite (Primrec.eq.comp primrec_tag (Primrec.const 5))
      (Primrec.eq.comp Primrec.id ((primrec_binary 5).comp primrec_arg1 primrec_arg2))
      (Primrec.const false))

theorem primrec_typeShape : Primrec typeShape :=
  Primrec.ite (Primrec.eq.comp primrec_tag (Primrec.const 0))
    (Primrec.eq.comp Primrec.id ((primrec_unary 0).comp (primrec_leaf.comp (primrec_rest.comp primrec_arg1))))
    (Primrec.ite (Primrec.eq.comp primrec_tag (Primrec.const 1))
      (Primrec.eq.comp Primrec.id ((primrec_binary 1).comp primrec_arg1 primrec_arg2))
      (Primrec.ite (Primrec.eq.comp primrec_tag (Primrec.const 2))
        (Primrec.eq.comp Primrec.id ((primrec_unary 2).comp primrec_arg1))
        (Primrec.ite (Primrec.eq.comp primrec_tag (Primrec.const 3))
          (Primrec.eq.comp Primrec.id (Primrec.const _)) (Primrec.const false))))

theorem primrec_polyShape : Primrec polyShape :=
  Primrec.ite (Primrec.eq.comp primrec_tag (Primrec.const 0))
    (Primrec.eq.comp Primrec.id ((primrec_unary 0).comp (primrec_leaf.comp (primrec_rest.comp primrec_arg1))))
    (Primrec.ite (Primrec.eq.comp primrec_tag (Primrec.const 1))
      (Primrec.eq.comp Primrec.id ((primrec_unary 1).comp (primrec_leaf.comp (primrec_rest.comp primrec_arg1))))
      (Primrec.ite (Primrec.eq.comp primrec_tag (Primrec.const 2))
        (Primrec.eq.comp Primrec.id ((primrec_binary 2).comp primrec_arg1 primrec_arg2))
        (Primrec.const false)))

theorem primrec_tyShape : Primrec tyShape := by
  unfold tyShape
  apply Primrec.ite (Primrec.eq.comp primrec_tag (Primrec.const 0))
  · exact Primrec.eq.comp Primrec.id
      ((primrec_unary 0).comp (primrec_leaf.comp (primrec_rest.comp primrec_arg1)))
  apply Primrec.ite (Primrec.eq.comp primrec_tag (Primrec.const 1))
  · exact Primrec.eq.comp Primrec.id (Primrec.const _)
  apply Primrec.ite (Primrec.eq.comp primrec_tag (Primrec.const 2))
  · exact Primrec.eq.comp Primrec.id ((primrec_unary 2).comp primrec_arg1)
  apply Primrec.ite (Primrec.eq.comp primrec_tag (Primrec.const 3))
  · exact Primrec.eq.comp Primrec.id (Primrec.const _)
  apply Primrec.ite (Primrec.eq.comp primrec_tag (Primrec.const 4))
  · exact Primrec.eq.comp Primrec.id ((primrec_binary 4).comp primrec_arg1 primrec_arg2)
  apply Primrec.ite (Primrec.eq.comp primrec_tag (Primrec.const 5))
  · exact Primrec.eq.comp Primrec.id ((primrec_binary 5).comp primrec_arg1 primrec_arg2)
  apply Primrec.ite (Primrec.eq.comp primrec_tag (Primrec.const 6))
  · apply Primrec.eq.comp Primrec.id
    unfold ternary
    apply primrec_node.comp (Primrec.const _)
    apply primrec_node.comp primrec_arg1
    apply primrec_node.comp (primrec_leaf.comp (primrec_rest.comp primrec_arg2))
    exact primrec_node.comp (primrec_leaf.comp (primrec_rest.comp primrec_arg3)) (Primrec.const _)
  · exact Primrec.const false

theorem primrec_shape : Primrec shape :=
  Primrec.ite (Primrec.eq.comp Primrec.fst (Primrec.const 0))
    (primrec_termShape.comp Primrec.snd)
    (Primrec.ite (Primrec.eq.comp Primrec.fst (Primrec.const 1))
      (primrec_typeShape.comp Primrec.snd)
      (Primrec.ite (Primrec.eq.comp Primrec.fst (Primrec.const 2))
        (primrec_polyShape.comp Primrec.snd)
        (Primrec.ite (Primrec.eq.comp Primrec.fst (Primrec.const 3))
          (primrec_tyShape.comp Primrec.snd) (Primrec.const false))))

theorem primrec_pairCode (s : Nat) {f : Nat → Nat} (hf : Primrec f) :
    Primrec (fun c => (s, f c)) := Primrec.pair (Primrec.const s) hf

theorem primrec_oneChild (s : Nat) {f : Nat → Nat} (hf : Primrec f) :
    Primrec (fun c => [(s, f c)]) :=
  Primrec.list_cons.comp (primrec_pairCode s hf) (Primrec.const [])
theorem primrec_twoChildren (s : Nat) : Primrec (fun c => [(s, arg1 c), (s, arg2 c)]) :=
  Primrec.list_cons.comp (primrec_pairCode s primrec_arg1) (primrec_oneChild s primrec_arg2)

theorem primrec_termChildren : Primrec termChildren :=
  Primrec.ite (Primrec.eq.comp primrec_tag (Primrec.const 5))
    (primrec_twoChildren 0) (Primrec.const [])
theorem primrec_typeChildren : Primrec typeChildren :=
  Primrec.ite (Primrec.eq.comp primrec_tag (Primrec.const 1))
    (primrec_twoChildren 1)
    (Primrec.ite (Primrec.eq.comp primrec_tag (Primrec.const 2))
      (primrec_oneChild 1 primrec_arg1) (Primrec.const []))
theorem primrec_polyChildren : Primrec polyChildren :=
  Primrec.ite (Primrec.eq.comp primrec_tag (Primrec.const 1))
    (primrec_oneChild 0 (primrec_rest.comp primrec_arg1))
    (Primrec.ite (Primrec.eq.comp primrec_tag (Primrec.const 2))
      (primrec_twoChildren 2) (Primrec.const []))
theorem primrec_tyChildren : Primrec tyChildren :=
  Primrec.ite (Primrec.eq.comp primrec_tag (Primrec.const 2))
    (primrec_oneChild 3 primrec_arg1)
    (Primrec.ite (PrimrecPred.or (Primrec.eq.comp primrec_tag (Primrec.const 4))
        (Primrec.eq.comp primrec_tag (Primrec.const 5)))
      (primrec_twoChildren 3)
      (Primrec.ite (Primrec.eq.comp primrec_tag (Primrec.const 6))
        (Primrec.list_cons.comp (primrec_pairCode 3 primrec_arg1)
          (Primrec.list_cons.comp (primrec_pairCode 2 (primrec_rest.comp primrec_arg2))
            (primrec_oneChild 2 (primrec_rest.comp primrec_arg3))))
        (Primrec.const [])))
theorem primrec_children : Primrec children :=
  Primrec.ite (Primrec.eq.comp Primrec.fst (Primrec.const 0))
    (primrec_termChildren.comp Primrec.snd)
    (Primrec.ite (Primrec.eq.comp Primrec.fst (Primrec.const 1))
      (primrec_typeChildren.comp Primrec.snd)
      (Primrec.ite (Primrec.eq.comp Primrec.fst (Primrec.const 2))
        (primrec_polyChildren.comp Primrec.snd)
        (Primrec.ite (Primrec.eq.comp Primrec.fst (Primrec.const 3))
          (primrec_tyChildren.comp Primrec.snd) (Primrec.const []))))

theorem primrec_valid : Primrec₂ valid :=
  (primrec_evaluate primrec_shape primrec_children).to₂

end ExactSyntaxValidity
