import ClosedScalarInstances
import P01Certificates

/- A finite, kernel-replayed address certificate for the actual open SKI carrier.
   No typing judgement is inferred from a certificate or from JSON labels. -/
namespace ScalarCertificates
open OpenTermStandardness (T Conv)
open P01D (Poly)
open P01AC.Intensional.Plus (PolyConvPlus)
open ImportedOpenTermTransport (interp)
open ClosedScalarInstances (scalarLeft scalarRight)
open P01Certificate (Direction Address)
set_option maxRecDepth 16384
set_option maxHeartbeats 8000000

def root (t : T) : Option {u : T // Conv t u} := match t with
  | .app .i x => some ⟨x,.i x⟩
  | .app (.app .k x) y => some ⟨x,.k x y⟩
  | .app (.app (.app .s f) g) x => some ⟨.app (.app f x) (.app g x),.s f g x⟩
  | _ => none

def stepAt : (t : T) → Address → Option {u : T // Conv t u}
  | t, [] => root t
  | .app f x, .left::rest => match stepAt f rest with
      | none => none
      | some g => some ⟨.app g.val x,.app g.property (.refl _)⟩
  | .app f x, .right::rest => match stepAt x rest with
      | none => none
      | some y => some ⟨.app f y.val,.app (.refl _) y.property⟩
  | _, _ => none

def replay : (t : T) → List Address → Option {u : T // Conv t u}
  | t, [] => some ⟨t,.refl t⟩
  | t, a::rest => match stepAt t a with
      | none => none
      | some u => match replay u.val rest with
          | none => none
          | some v => some ⟨v.val,u.property.trans v.property⟩

def replayTo (t u : T) (p : List Address) : Option (PLift (Conv t u)) :=
  match replay t p with
  | none => none
  | some v => if h : v.val = u then some ⟨h ▸ v.property⟩ else none

def checkScalar (n : Poly) (k : Nat) (l r : List Address) :
    Option (PLift (PolyConvPlus (scalarLeft n) (scalarRight n))) :=
  match replayTo (interp (scalarLeft n) T.var) (OpenTermStandardness.iter (.var 1) (.var 0) k) l,
    replayTo (interp (scalarRight n) T.var) (OpenTermStandardness.iter (.var 1) (.var 0) k) r with
  | some hl, some hr => some ⟨ClosedScalarInstances.generic_conversion_reflect
      (hl.down.trans hr.down.symm)⟩
  | _, _ => none

theorem optionProof {P : Prop} (v : Option (PLift P)) (h : v.isSome = true) : P := by
  cases v with
  | none => contradiction
  | some p => exact p.down

/-- A true finite checker result produces the actual source conversion. -/
theorem checkedScalar (n : Poly) (k : Nat) (l r : List Address)
    (h : (checkScalar n k l r).isSome = true) :
    PolyConvPlus (scalarLeft n) (scalarRight n) :=
  optionProof (checkScalar n k l r) h

/-- Count binding is to the exact generic iteration, not an arbitrary join. -/
theorem checkedIteration (n : Poly) (k : Nat) (l : List Address)
    (h : (replayTo (interp (scalarLeft n) T.var)
      (OpenTermStandardness.iter (.var 1) (.var 0) k) l).isSome = true) :
    PolyConvPlus (scalarLeft n) (P01AC.EffectiveCompleteness.iterationPoly k) := by
  apply ClosedScalarInstances.generic_conversion_reflect
  rw [ClosedScalarInstances.iteration_interp]
  exact optionProof _ h

#print axioms checkedScalar
#print axioms checkedIteration
end ScalarCertificates

namespace ScalarCertificates
open OpenTermStandardness (T)
open P01D P01AC
open P01AC.Intensional.Plus (PolyConvPlus)
open P01AC.ExtensionalRepair
open P01AC.ExtensionalRepair.ExactScalarFusion (A End Leaf c3 i)
open P01AC.EffectiveCompleteness (iterationPoly)
open ImportedOpenTermTransport (interp)
open ClosedScalarInstances (scalarLeft scalarRight scalarInstance c2)
open P01Certificate (Address)

theorem checkedRightIteration (n : Poly) (k : Nat) (r : List Address)
    (h : (replayTo (interp (scalarRight n) T.var)
      (OpenTermStandardness.iter (.var 1) (.var 0) k) r).isSome = true) :
    PolyConvPlus (scalarRight n) (iterationPoly k) := by
  apply ClosedScalarInstances.generic_conversion_reflect
  rw [ClosedScalarInstances.iteration_interp]
  exact optionProof _ h

/-- Positive finite evidence has a wholly source-syntactic typing reconstruction.
    Scope is checked separately. No inference of HasE [] n N is made or needed.
    This proof does not invoke semantic standardness or its closed-instance theorem. -/
theorem sourceInstanceFromConversions {n : Poly} (hn : Scoped 0 n) (k : Nat)
    (hl : PolyConvPlus (scalarLeft n) (iterationPoly k))
    (hr : PolyConvPlus (scalarRight n) (iterationPoly k)) :
    HasE [] c2 (scalarInstance n) := by
  have hΔ : Ctx [A,End] := .ext (.ext .nil (ExactScalarFusion.End_form .nil))
    (ExactScalarFusion.A_form (.ext .nil (ExactScalarFusion.End_form .nil)))
  have ha := form_inclusion (ExactScalarFusion.A_form hΔ)
  have li : HasE [A,End] (scalarLeft n) A :=
    .conv ha (has_inclusion (ClosedScalarInstances.iteration_has k)) hl.symm
      (ClosedScalarInstances.scalarLeft_scoped hn)
  have ri : HasE [A,End] (scalarRight n) A :=
    .conv ha (has_inclusion (ClosedScalarInstances.iteration_has k)) hr.symm
      (ClosedScalarInstances.scalarRight_scoped hn)
  have leaf : HasE [A,End] i (.identity A (scalarLeft n) (scalarRight n)) :=
    .identityIntro (.identity ha li ri) li ri (hl.trans hr.symm)
  have hleaf := ClosedProofCanonicalisation.formed leaf
  have he := form_inclusion (ExactScalarFusion.End_form (Γ := []) .nil)
  have ha' := form_inclusion (ExactScalarFusion.A_form
    (Ctx.ext .nil (ExactScalarFusion.End_form .nil)))
  have inner := FormE.pi ha' hleaf
  have outer := FormE.pi he inner
  exact .allIntro (.all .nil outer)
    (.piIntro outer (.piIntro inner leaf (scoped_abstract trivial))
      (scoped_abstract (scoped_abstract trivial)))

theorem exactSourceInstanceFromConversions {n : Poly} (hn : Scoped 0 n) (k : Nat)
    (hl : PolyConvPlus (scalarLeft n) (iterationPoly k))
    (hr : PolyConvPlus (scalarRight n) (iterationPoly k)) :
    HasE [] (.app c3 n)
      (inst (.all (.pi End (.pi A (Leaf FullPER.Application.originalQ)))) n) := by
  rw [ClosedScalarInstances.scalarInstance_exact hn]
  have h := sourceInstanceFromConversions hn k hl hr
  exact .conv (ClosedProofCanonicalisation.formed h) h
    (ClosedScalarInstances.c3_apply n).symm ⟨ExactScalarFusion.c3_scoped 0,hn⟩

/-- A source instance reconstructed from finite address certificates. Its scope
    obligation is an actual Lean Scoped proof, not a JSON HasE label. -/
theorem checkedSourceInstance (n : Poly) (hn : Scoped 0 n) (k : Nat) (l r : List Address)
    (hl : (replayTo (interp (scalarLeft n) T.var)
      (OpenTermStandardness.iter (.var 1) (.var 0) k) l).isSome = true)
    (hr : (replayTo (interp (scalarRight n) T.var)
      (OpenTermStandardness.iter (.var 1) (.var 0) k) r).isSome = true) :
    HasE [] (.app c3 n)
      (inst (.all (.pi End (.pi A (Leaf FullPER.Application.originalQ)))) n) :=
  exactSourceInstanceFromConversions hn k (checkedIteration n k l hl) (checkedRightIteration n k r hr)

#print axioms sourceInstanceFromConversions
#print axioms exactSourceInstanceFromConversions
#print axioms checkedSourceInstance
end ScalarCertificates

namespace ScalarCertificates
open OrthemologyV2 P01D P01AC
open P01AC.ExtensionalRepair
open P01AC.EffectiveCompleteness (N inputNumeral inputNumeral_has)
open P01AC.Intensional.Plus (PolyConvPlus)

def erasingOmegaNumeral (k : Nat) : Poly :=
  .app (.app (.atom .k) (inputNumeral k)) (.atom OrthemologyV3.omega)

/-- HasE is conversion-closed; its numeral inputs need not be strongly normalizing. -/
theorem erasingOmegaNumeral_has (k : Nat) : HasE [] (erasingOmegaNumeral k) N := by
  have hn := has_inclusion (inputNumeral_has k)
  exact .conv (ClosedProofCanonicalisation.formed hn) hn
    (PolyConvPlus.k (inputNumeral k) (.atom OrthemologyV3.omega)).symm
    ⟨⟨trivial,has_scoped (inputNumeral_has k)⟩,trivial⟩

theorem erasingOmegaNumeral_not_SN (k : Nat) (η : Env) :
    ¬ OrthemologyV3.StronglyNormalising (eval (erasingOmegaNumeral k) η) := by
  exact OrthemologyV3.three_cycle_not_SN
    (Step.right (.app .k (eval (inputNumeral k) η)) OrthemologyV3.omega_step1)
    (Step.right (.app .k (eval (inputNumeral k) η)) OrthemologyV3.omega_step2)
    (Step.right (.app .k (eval (inputNumeral k) η)) OrthemologyV3.omega_step3)

#print axioms erasingOmegaNumeral_has
#print axioms erasingOmegaNumeral_not_SN
end ScalarCertificates
