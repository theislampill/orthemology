/- Exact bounded theorem and constructor interfaces, checked by Lean. -/
import ExtensionalRepairTheorems

open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.Intensional (separationP separationQ separationE separationA separationB)
open P01AC.ExtensionalRepair

example (r : Poly) : ¬ P01AC.Has [] r separationB :=
  P01AC.Intensional.separation_no_has r
example (r : Poly) : ¬ P01AC.Intensional.Plus.HasPlus [] r separationB :=
  P01AC.Intensional.separation_no_hasPlus r
example : HasE [] separationE separationB := separation_has
example : HasE [] (.app (.atom .k) (.atom .i)) (.pi repairX pointwiseM) :=
  pointwise_evidence_has
example : HasE [] (.atom .i) (.identity repairC separationP separationQ) :=
  arrow_identity_has
example (r : Poly) : ¬ HasE [] r (.identity .raw separationP separationQ) :=
  raw_separation_no_has r
example : FormE [] (.identity .raw separationP separationQ) := raw_separation_form
example {r p q : Poly} (h : HasE [] r (.identity .raw p q)) :
    Conv (eval p zeroEnv) (eval q zeroEnv) := closed_raw_identity_conversion h
example : ¬ P01AC.Intensional.Plus.PolyConvPlus separationP separationQ :=
  separation_not_polyConvPlus
example : HasE [] separationE .raw := separation_proof_erases

example {Γ p A} (h : HasE Γ p A) : P01AC.TermSound Γ p A := has_sound h
example {Γ A} (h : FormE Γ A) : P01AC.FormSound Γ A := form_sound h
example {Γ} (h : CtxE Γ) : P01AC.ContextLaws Γ := context_sound h
example {Γ p A} (h : HasE Γ p A) : P01AC.Fundamental Γ p A := fundamental h
example {Γ p A} (h : P01AC.Has Γ p A) : HasE Γ p A := has_inclusion h
example {Γ p A} (h : P01AC.Intensional.Plus.HasPlus Γ p A) : HasE Γ p A :=
  plus_has_inclusion h

example : HasE [] separationE separationB ∧
    (¬ ∃ r, P01AC.Has [] r separationB) ∧
    (¬ ∃ r, P01AC.Intensional.Plus.HasPlus [] r separationB) ∧
    (¬ ∃ r, HasE [] r (.identity .raw separationP separationQ)) ∧
    (¬ P01AC.Intensional.Plus.PolyConvPlus separationP separationQ) :=
  strict_typed_identity_extension

-- Exact schemas include every formation, endpoint typing, evidence, and scope premise.
example {Γ : Tel} {A B : Ty} {p q h : Poly} :
    FormE Γ A → FormE (A :: Γ) B → FormE Γ (.pi A B) →
    HasE Γ p (.pi A B) → HasE Γ q (.pi A B) →
    FormE (A :: Γ) (.identity B (.app (pren Nat.succ p) (.var 0))
      (.app (pren Nat.succ q) (.var 0))) →
    FormE Γ (.pi A (.identity B (.app (pren Nat.succ p) (.var 0))
      (.app (pren Nat.succ q) (.var 0)))) →
    HasE Γ h (.pi A (.identity B (.app (pren Nat.succ p) (.var 0))
      (.app (pren Nat.succ q) (.var 0)))) →
    FormE Γ (.identity (.pi A B) p q) →
    Scoped Γ.length p → Scoped Γ.length q → Scoped Γ.length h →
    TyScoped Γ.length A → TyScoped (Γ.length + 1) B →
    HasE Γ (.atom .i) (.identity (.pi A B) p q) := HasE.piExt

example {Γ : Tel} {B : Ty} {p q h : Poly} :
    FormE (twkTel Γ) B → FormE Γ (.all B) →
    HasE Γ p (.all B) → HasE Γ q (.all B) →
    FormE (twkTel Γ) (.identity B p q) →
    HasE (twkTel Γ) h (.identity B p q) →
    FormE Γ (.identity (.all B) p q) →
    Scoped Γ.length p → Scoped Γ.length q → Scoped Γ.length h →
    TyScoped Γ.length B → HasE Γ (.atom .i) (.identity (.all B) p q) := HasE.allExt

#check @P01AC.ExtensionalRepair.strict_typed_identity_extension
#check @P01AC.ExtensionalRepair.has_sound
#check @P01AC.ExtensionalRepair.separation_has
#check @P01AC.ExtensionalRepair.closed_raw_identity_conversion
#check @P01AC.ExtensionalRepair.raw_separation_no_has
