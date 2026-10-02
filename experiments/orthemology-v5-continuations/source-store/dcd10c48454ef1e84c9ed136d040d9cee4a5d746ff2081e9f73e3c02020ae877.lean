import SourceTypeOps
namespace P03Source
open OrthemologyV2 OrthemologyV3

/-- Independent equations matching reference.py::_head_step on validated terms. -/
def sourceHeadStep : Term → Option Term
  | .app .i x => some x
  | .app (.app .k x) _ => some x
  | .app (.app (.app .s f) g) x => some (.app (.app f x) (.app g x))
  | .app f x => (sourceHeadStep f).map (fun g => .app g x)
  | _ => none

theorem sourceHeadStep_eq (t : Term) :
    (certifiedHeadStep t).map Subtype.val = sourceHeadStep t := by
  induction t with
  | i => rfl
  | k => rfl
  | s => rfl
  | zero => rfl
  | one => rfl
  | app f x ihf ihx =>
      cases f with
      | i => rfl
      | k => rfl
      | s => rfl
      | zero => rfl
      | one => rfl
      | app g y =>
          cases g with
          | k => rfl
          | i => rfl
          | zero => rfl
          | one => rfl
          | s => rfl
          | app h z =>
              cases h with
              | s => rfl
              | i => rfl
              | k => rfl
              | zero => rfl
              | one => rfl
              | app a b =>
                  simp only [certifiedHeadStep, sourceHeadStep] at ihf ⊢
                  cases hc : certifiedHeadStep (.app (.app (.app a b) z) y) <;>
                    simp only [hc, Option.map] at ihf ⊢ <;>
                    rw [← ihf] <;> rfl

#print axioms sourceHeadStep_eq
end P03Source
