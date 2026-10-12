import JointTypeInstantiation
import JointControls

namespace JointCompletion.MixedControls
open P01AC P01D OrthemologyV2 OrthemologyV3 P01R
open P01F (cons)
open JointCompletion.Structural
open JointCompletion.Controls
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

theorem arrow_formed {Γ A B} (hA : FormJ Γ A) (hB : FormJ Γ B) :
    FormJ Γ (arr A B) := .pi hA (Structural.form_wk hB (Structural.form_ctx hA) hA)

def sourceType : Ty := .all (arr (.param 1) (.param 1))
def sourcePoly : Poly := .atom .i

theorem source_typing : HasJ [] sourcePoly sourceType := by
  have hf : FormJ [] (arr (.param 1) (.param 1)) := arrow_formed (.param .nil) (.param .nil)
  exact .allIntro (.all .nil hf) (.i (.param .nil) hf)

/-- One replacement type is simultaneously beyond old E formation and dependent
on an actual free variable in the target term telescope. -/
def mixedImage : Ty := .pi newMotive (.identity .raw (.var 1) (.var 1))
def mixedTypes : Nat → Ty := cons mixedImage Ty.param

theorem raw_context : CtxJ [.raw] := .ext .nil (.raw .nil)

theorem mixed_image_formed : FormJ [.raw] mixedImage := by
  have hn : FormJ [.raw] newMotive := new_motive_form (.ext .nil (.raw .nil))
  have hc := CtxJ.ext raw_context hn
  have hx : HasJ [newMotive,.raw] (.var 1) .raw := .var (.raw hc) (.succ .zero)
  exact .pi hn (.identity (.raw hc) hx hx)

theorem mixed_images_formed : ∀ n, FormJ [.raw] (mixedTypes n) := by
  intro n
  cases n with
  | zero => exact mixed_image_formed
  | succ n => exact .param raw_context

/-- A single application of the new theorem crosses both All and term binders. -/
theorem dependent_new_type_instance : HasJ [.raw] sourcePoly (.all (arr mixedImage mixedImage)) :=
  has_closed_tsubst source_typing raw_context mixed_images_formed

private def codomainEndpoint : Ty → Nat
  | .all (.pi _ (.pi _ (.identity _ (.var n) _))) => n + 1
  | _ => 0

/-- Failure to lift a target-relative image under Pi would capture its endpoint. -/
theorem wrong_unlifted_codomain :
    tsubst mixedTypes sourceType ≠ .all (.pi mixedImage mixedImage) := by
  intro h
  have he := congrArg codomainEndpoint h
  change 3 = 2 at he
  contradiction

/-- The domain really requires the new completion rules; old E cannot form it. -/
theorem mixed_image_not_old : ¬ P01AC.ExtensionalRepair.FormE [.raw] mixedImage := by
  intro h
  cases h with
  | pi hM _ =>
      have hi : P01AC.ExtensionalRepair.HasE [] (.atom .i) .raw := .rawAtom (.raw .nil)
      have hs : P01AC.ExtensionalRepair.Structural.TypedSubstitution [.raw] []
          (cons (.atom .i) Poly.var) :=
        P01AC.ExtensionalRepair.Structural.TypedSubstitution.single .nil hi
      have hm := P01AC.ExtensionalRepair.Structural.form_subst hM .nil hs
      exact new_motive_not_old (by simpa only [newMotive_subst] using hm)

theorem mixed_result_not_old (p : Poly) :
    ¬ P01AC.ExtensionalRepair.HasE [.raw] p (.all (arr mixedImage mixedImage)) := by
  intro h
  have hf := P01AC.ExtensionalRepair.ClosedProofCanonicalisation.formed h
  cases hf with
  | all _ hB => cases hB with | pi hI _ => exact mixed_image_not_old hI

/-- Erased All instantiation now accepts a newly Joint-formed type without
requiring the conclusion's formation as a separate premise. -/
theorem all_eliminate_new_type : HasJ [] (.atom .i) (arr newMotive newMotive) := by
  have hf : FormJ [] (arr (.param 0) (.param 0)) := arrow_formed (.param .nil) (.param .nil)
  have hp : HasJ [] (.atom .i) (.all (arr (.param 0) (.param 0))) :=
    .allIntro (.all .nil hf) (.i (.param .nil) hf)
  exact allElim_formed hp (new_motive_form .nil)

def closeTerm : Nat → Poly := cons (.atom .i) Poly.var

theorem close_term_typed : TypedSubstitution [.raw] [] closeTerm :=
  TypedSubstitution.instantiate .nil (.rawAtom (.raw .nil))

theorem type_then_term_instance : HasJ [] (psub closeTerm sourcePoly)
    (mixed closeTerm (fun n => subst closeTerm (mixedTypes n)) sourceType) :=
  has_type_then_term source_typing raw_context (TypeSubstitution.empty mixed_images_formed)
    .nil close_term_typed

/-- Applying term substitution must act on the injected type images too. -/
theorem unchanged_type_images_wrong :
    mixed closeTerm mixedTypes sourceType ≠
      mixed closeTerm (fun n => subst closeTerm (mixedTypes n)) sourceType := by
  intro h
  have he := congrArg codomainEndpoint h
  change 3 = 0 at he
  contradiction

#print axioms dependent_new_type_instance
#print axioms wrong_unlifted_codomain
#print axioms mixed_image_not_old
#print axioms mixed_result_not_old
#print axioms all_eliminate_new_type
#print axioms type_then_term_instance
#print axioms unchanged_type_images_wrong
end JointCompletion.MixedControls
