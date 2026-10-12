/- Actual source weakening; no old-Has weakening or semantic reflection. -/
import HasEStructuralRename
import ScalarFusionCore
namespace P01AC.ExtensionalRepair.Structural
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01AC.EffectiveCompleteness (N NBody)
open P01AC.ExtensionalRepair.ExactScalarFusion (End)

/-- The empty source telescope renames into any well-formed HasE telescope.
    The original polynomial and original type are preserved literally. -/
theorem has_closed {p : Poly} {A : Ty} (h : HasE [] p A)
    {Γ : Tel} (hΓ : CtxE Γ) : HasE Γ p A := by
  have hr : Renaming [] Γ id := ⟨by simp, by intro n A h; cases h⟩
  have ht := has_rename h hΓ hr
  change HasE Γ (psub Poly.var p) (subst Poly.var A) at ht
  simpa only [psub_id, subst_id] using ht

/-- Exact weakening needed to compare any derivable closed Church term. -/
theorem closed_church_weaken {n : Poly} (hn : HasE [] n N) : HasE [End] n N :=
  has_closed hn (.ext .nil (form_inclusion (ExactScalarFusion.End_form .nil)))

#print axioms has_closed
#print axioms closed_church_weaken
end P01AC.ExtensionalRepair.Structural
