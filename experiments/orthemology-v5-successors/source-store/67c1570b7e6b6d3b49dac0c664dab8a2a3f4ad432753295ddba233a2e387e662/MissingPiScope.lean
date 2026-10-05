import ExtensionalRepairTheorems
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC P01AC.Intensional

-- Expected type rejection only; no logical independence claim.
open P01AC.ExtensionalRepair
example : HasE [] (.atom .i) (.identity repairC separationP separationQ) :=
  HasE.piExt
    (.param .nil)
    (.param (ctx_inclusion repair_singleton_ctx))
    (form_inclusion (old_arrow_form .nil))
    (has_inclusion arrowP_empty_has)
    (has_inclusion arrowQ_empty_has)
    pointwise_form pointwise_product_form pointwise_evidence_has arrow_identity_form
