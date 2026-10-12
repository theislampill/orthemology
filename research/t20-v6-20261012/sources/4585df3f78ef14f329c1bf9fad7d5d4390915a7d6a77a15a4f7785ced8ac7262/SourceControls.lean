import ExtensionalRepairSyntax

/- Actual-source controls for proposed type-indexed family semantics.
No new grammar, interpretation, source-completeness premise, or axiom. -/
namespace TypeIndexedSourceControls
open P01AC P01D P01AC.ExtensionalRepair

def ConstantAll : Ty := .all .raw

theorem constantAll_form_empty : FormE [] ConstantAll := .all .nil (.raw .nil)

theorem constantAll_context : CtxE [ConstantAll] := .ext .nil constantAll_form_empty

theorem constantAll_form : FormE [ConstantAll] ConstantAll :=
  .all constantAll_context (.raw constantAll_context)

/-- Direct variable route. -/
theorem constantAll_direct : HasE [ConstantAll] (.var 0) ConstantAll :=
  .var constantAll_form .zero

/-- Instantiate at the actually formed Raw type; the polynomial stays var 0. -/
theorem constantAll_at_raw : HasE [ConstantAll] (.var 0) .raw :=
  .allElim constantAll_form (.raw constantAll_context) (.raw constantAll_context)
    constantAll_direct

/-- Reintroduce the irrelevant parameter. Literally the same entire judgement. -/
theorem constantAll_reabstract : HasE [ConstantAll] (.var 0) ConstantAll :=
  .allIntro constantAll_form constantAll_at_raw

/-- Same unannotated endpoint occurs in actual identity syntax. -/
theorem same_endpoint_identity :
    HasE [ConstantAll] (.atom .i) (.identity ConstantAll (.var 0) (.var 0)) :=
  .identityIntro (.identity constantAll_form constantAll_direct constantAll_reabstract)
    constantAll_direct constantAll_reabstract (.refl _)

def DiscriminatorBody : Ty := arr (.param 0) .raw
def Discriminator : Ty := .all DiscriminatorBody

theorem discriminator_form_empty : FormE [] Discriminator :=
  .all .nil (.pi (.param .nil) (.raw (.ext .nil (.param .nil))))

theorem discriminator_context : CtxE [Discriminator] :=
  .ext .nil discriminator_form_empty

theorem discriminator_form : FormE [Discriminator] Discriminator :=
  .all discriminator_context
    (.pi (.param discriminator_context)
      (.raw (.ext discriminator_context (.param discriminator_context))))

theorem discriminator_var : HasE [Discriminator] (.var 0) Discriminator :=
  .var discriminator_form .zero

/-- Full impredicative self-instantiation occurs in the unchanged actual grammar. -/
theorem discriminator_self_instance :
    HasE [Discriminator] (.var 0) (arr Discriminator .raw) :=
  .allElim discriminator_form discriminator_form
    (.pi discriminator_form (.raw (.ext discriminator_context discriminator_form)))
    discriminator_var

/-- The diagonal application is a legal source term, not an untyped surrogate. -/
theorem discriminator_diagonal :
    HasE [Discriminator] (.app (.var 0) (.var 0)) .raw :=
  .piElim (.pi discriminator_form
    (.raw (.ext discriminator_context discriminator_form)))
    (.raw discriminator_context) discriminator_self_instance discriminator_var

#print axioms constantAll_reabstract
#print axioms same_endpoint_identity
#print axioms discriminator_diagonal
end TypeIndexedSourceControls
