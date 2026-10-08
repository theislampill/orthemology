/-
An exact finite derivation for the separately named, unadopted candidate.
The endpoint atoms and final type are the frozen Intensional witness definitions.
No soundness result, semantic admission, or closed-packing converse is used.
-/
import ExtensionalRepairSyntax
import IntensionalIdentityWitness

namespace P01AC.ExtensionalRepair
open OrthemologyV2 OrthemologyV3 P01D P01R
open Intensional.Plus (PolyConvPlus)

/-- The free type parameter is not a term coordinate. -/
def repairX : Ty := .param 0

/-- Literally the body of the frozen finite polymorphic identity type. -/
def repairC : Ty := .pi repairX repairX

/-- The exact inner identity family required by `HasE.piExt`. -/
def pointwiseM : Ty := .identity repairX
  (.app (pren Nat.succ Intensional.separationP) (.var 0))
  (.app (pren Nat.succ Intensional.separationQ) (.var 0))

theorem separationA_eq_all_repairC :
    Intensional.separationA = .all repairC := rfl

theorem repair_singleton_ctx : P01AC.Ctx [repairX] :=
  .ext .nil (.param .nil)

/-- Each endpoint import uses the existing finite image/support construction. -/
theorem old_arrowP_has {Γ : Tel} (hΓ : P01AC.Ctx Γ) :
    P01AC.Has Γ Intensional.separationP repairC :=
  finite_import hΓ (.i (.var 0))

theorem old_arrowQ_has {Γ : Tel} (hΓ : P01AC.Ctx Γ) :
    P01AC.Has Γ Intensional.separationQ repairC :=
  finite_import hΓ (finite_skk_identity (.var 0))

theorem old_arrow_form {Γ : Tel} (hΓ : P01AC.Ctx Γ) :
    P01AC.Form Γ repairC :=
  form_fin (.arrow (.var 0) (.var 0)) hΓ

/-- Explicit imports in each of the two term telescopes used below. -/
theorem arrowP_empty_has : P01AC.Has [] Intensional.separationP repairC :=
  old_arrowP_has .nil

theorem arrowQ_empty_has : P01AC.Has [] Intensional.separationQ repairC :=
  old_arrowQ_has .nil

theorem arrowP_singleton_has :
    P01AC.Has [repairX] Intensional.separationP repairC :=
  old_arrowP_has repair_singleton_ctx

theorem arrowQ_singleton_has :
    P01AC.Has [repairX] Intensional.separationQ repairC :=
  old_arrowQ_has repair_singleton_ctx

theorem variable_has : P01AC.Has [repairX] (.var 0) repairX :=
  .var (.param repair_singleton_ctx) .zero

/-- These are old finite derivations, not an assumed weakening theorem for E. -/
theorem pointwiseP_has : P01AC.Has [repairX]
    (.app (pren Nat.succ Intensional.separationP) (.var 0)) repairX :=
  .piElim (old_arrow_form repair_singleton_ctx) (.param repair_singleton_ctx)
    arrowP_singleton_has variable_has

theorem pointwiseQ_has : P01AC.Has [repairX]
    (.app (pren Nat.succ Intensional.separationQ) (.var 0)) repairX :=
  .piElim (old_arrow_form repair_singleton_ctx) (.param repair_singleton_ctx)
    arrowQ_singleton_has variable_has

theorem pointwise_form : FormE [repairX] pointwiseM :=
  form_inclusion (.identity (.param repair_singleton_ctx) pointwiseP_has pointwiseQ_has)

theorem pointwise_product_form : FormE [] (.pi repairX pointwiseM) :=
  .pi (.param .nil) pointwise_form

theorem arrow_identity_form :
    FormE [] (.identity repairC Intensional.separationP Intensional.separationQ) :=
  form_inclusion (.identity (old_arrow_form .nil) arrowP_empty_has arrowQ_empty_has)

/-- Exactly two bridge instances expose the SKK head; the variable stays open. -/
theorem skk_head_exposure : PolyConvPlus (.atom P01R.skk)
    (.app (.app (.atom .s) (.atom .k)) (.atom .k)) :=
  (PolyConvPlus.bridge (.app .s .k) .k).trans
    (.app (.bridge .s .k) (.refl (.atom .k)))

/-- An explicit open-polynomial reduction at var(0), using only the old S/K
    generators after exposing the closed head. No closed-packing lemma applies. -/
theorem skk_at_var0_conversion :
    PolyConvPlus (.app (.atom P01R.skk) (.var 0)) (.var 0) :=
  (PolyConvPlus.app skk_head_exposure (.refl (.var 0))).trans
    ((PolyConvPlus.s (.atom .k) (.atom .k) (.var 0)).trans
      (.k (.var 0) (.app (.atom .k) (.var 0))))

/-- The exact open conversion used by identity introduction in [param(0)]. -/
theorem pointwise_conversion :
    PolyConvPlus (.app (.atom .i) (.var 0))
      (.app (.atom P01R.skk) (.var 0)) :=
  (PolyConvPlus.i (.var 0)).trans skk_at_var0_conversion.symm

theorem pointwise_identity_has : HasE [repairX] (.atom .i) pointwiseM :=
  .identityIntro pointwise_form (has_inclusion pointwiseP_has)
    (has_inclusion pointwiseQ_has) pointwise_conversion

/-- This is evaluation of the imported bracket compiler's absent-variable branch. -/
theorem bracket_I_exact :
    abstract (.atom .i) = .app (.atom .k) (.atom .i) := by
  simp [abstract, freeZero, drop, pren, psub]

theorem pointwise_evidence_scoped :
    Scoped 0 (.app (.atom .k) (.atom .i)) := ⟨True.intro, True.intro⟩

/-- The one finite product proof has the actual polynomial K I as evidence. -/
theorem pointwise_evidence_has :
    HasE [] (.app (.atom .k) (.atom .i)) (.pi repairX pointwiseM) := by
  rw [← bracket_I_exact]
  exact .piIntro pointwise_product_form pointwise_identity_has
    (by rw [bracket_I_exact]; exact pointwise_evidence_scoped)

/-- Exactly one new Pi-extensionality instance, with every formation and scope
    premise supplied. The endpoints are the exact frozen atoms. -/
theorem arrow_identity_has :
    HasE [] (.atom .i)
      (.identity repairC Intensional.separationP Intensional.separationQ) :=
  .piExt
    (.param .nil)
    (.param (ctx_inclusion repair_singleton_ctx))
    (form_inclusion (old_arrow_form .nil))
    (has_inclusion arrowP_empty_has)
    (has_inclusion arrowQ_empty_has)
    pointwise_form
    pointwise_product_form
    pointwise_evidence_has
    arrow_identity_form
    Intensional.separationP_scoped
    Intensional.separationQ_scoped
    pointwise_evidence_scoped
    True.intro
    True.intro

/-- The outer endpoint typings are current finite imports, including All's
    original uniform-membership requirements. -/
theorem allP_has : HasE [] Intensional.separationP Intensional.separationA :=
  has_inclusion (finite_import .nil P01R.finite_polymorphic_I)

theorem allQ_has : HasE [] Intensional.separationQ Intensional.separationA :=
  has_inclusion (finite_import .nil P01R.finite_polymorphic_skk)

theorem repairC_scoped : TyScoped 0 repairC := ⟨True.intro, True.intro⟩

/-- Exactly one All-extensionality instance over twkTel [] = []; together with
    `arrow_identity_has`, this derives the exact frozen separation judgment. -/
theorem separation_has :
    HasE [] P01AC.Intensional.separationE P01AC.Intensional.separationB :=
  .allExt
    (form_inclusion (old_arrow_form .nil))
    (form_inclusion Intensional.separationA_form)
    allP_has
    allQ_has
    arrow_identity_form
    arrow_identity_has
    (form_inclusion Intensional.separationB_form)
    Intensional.separationP_scoped
    Intensional.separationQ_scoped
    Intensional.separationE_scoped
    repairC_scoped

end P01AC.ExtensionalRepair
